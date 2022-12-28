# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.integrations.doctype.google_contacts.google_contacts import insert_contacts_to_google_contacts
from frappe.integrations.doctype.google_contacts.google_contacts import update_contacts_to_google_contacts

class LeadManagement(Document):
	def before_save(self):
		if(self.mobile_no):
			if(len(self.mobile_no.split('-')[-1]) < 1):
				self.mobile_no = ''
	def validate(self):
		self.create_contact()
		if(len(self.follow_ups)>0):
			status = self.follow_ups[-1].get('status')
			if(status):
				self.status = status

	def create_contact(self, is_new_contact=1):
		contact = frappe.new_doc('Contact')
		if(frappe.db.exists('Dynamic Link', {'link_doctype':'Lead Management', 'link_name':self.name, 'parenttype': "Contact"})):
			contact_name = frappe.db.get_value('Dynamic Link', {'link_doctype':'Lead Management', 'link_name':self.name, 'parenttype': "Contact"}, 'parent')
			contact = frappe.get_doc('Contact', contact_name)
			is_new_contact = 0
		email = []
		phone = []
		links = [{
			'link_doctype':'Lead Management', 'link_name':self.name, 'parenttype':'Contact'
		}]
		if(self.whatsapp_no):
			wa_no = str(self.whatsapp_no).split('-')
			phone.append({'phone':wa_no[-1] if len(wa_no)>0 else self.whatsapp_no, 'is_primary_phone':1, 'is_primary_mobile_no':1})
		if(self.mobile_no):
			ph_no = str(self.mobile_no).split('-')
			phone.append({'phone':ph_no[-1] if len(ph_no)>0 else self.mobile_no})
		if(self.email):
			email.append({'email_id':self.email, 'is_primary':1})
		contact.update({
			'first_name':self.lead_name,
			'email_ids':email,
			'phone_nos':phone,
			'links':links
		})
		contact.save()
		contact_name = contact.name
		google_contacts = self.get_google_contact_for_site()
		for i in google_contacts:
			contact.update({
				'sync_with_google_contacts':1,
				'google_contacts':i,
			})
			if is_new_contact:
				insert_contacts_to_google_contacts(contact, 'after_insert')
			else:
				update_contacts_to_google_contacts(contact, 'on_update')
		contact.save()

	def get_google_contact_for_site(self, request_for_site=[]):
		site = []
		if(not len(request_for_site)):
			request_for_site = frappe.db.get_all('Multiselect Site', filters={'parent':self.name}, pluck='site')
		for i in request_for_site:
			if isinstance(i, dict):
				site.append(i['site'])
			else:
				site.append(i)
		google_contacts = frappe.db.get_all('Multiselect Google Contacts', filters={'parent':['in', site]}, pluck='google_contacts')
		google_contacts = [i for i in google_contacts if(frappe.db.get_value('Google Contacts', i, 'enable'))]
		return google_contacts


