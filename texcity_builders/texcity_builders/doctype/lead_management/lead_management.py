# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.integrations.doctype.google_contacts.google_contacts import insert_contacts_to_google_contacts
# from frappe.integrations.doctype.google_contacts.google_contacts import update_contacts_to_google_contacts
from frappe.integrations.doctype.google_contacts.google_contacts import get_google_contacts_object
from googleapiclient.errors import HttpError


class LeadManagement(Document):
	def before_save(self):
		if(self.mobile_no):
			if(len(self.mobile_no.split('-')[-1]) < 1):
				self.mobile_no = ''
	def validate(self):
		if(len(self.follow_ups)>0):
			status = self.follow_ups[-1].get('status')
			if(status):
				self.status = status
	def after_insert(self):
		frappe.enqueue(self.create_contact, queue='long')

	def create_contact(self, is_new_contact=1):
		try:
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
				if len(wa_no)>1:
					phone.append({'phone':wa_no[-1] if len(wa_no)>0 else self.whatsapp_no, 'is_primary_phone':1, 'is_primary_mobile_no':1})
			if(self.mobile_no):
				ph_no = str(self.mobile_no).split('-')
				if len(ph_no)>1:
					phone.append({'phone':ph_no[-1] if len(ph_no)>0 else self.mobile_no})
			if(self.email):
				email.append({'email_id':self.email, 'is_primary':1} )
			contact.update({
				'first_name':self.lead_name,
				'email_ids':email,
				'phone_nos':phone,
				'links':links
			})
			contact.flags.ignore_validate = True
			contact.save()
			contact.reload()
			contact_name = contact.name
			google_contacts = self.get_google_contact_for_site()
			last_contact = ''
			for i in google_contacts:
				last_contact = i
				contact.update({
					'sync_with_google_contacts':1,
					'google_contacts':i,
				})
				if is_new_contact:
					insert_contacts_to_google_contacts(contact, 'after_insert')
				else:
					if not self.update_contacts_to_google_contacts(contact, 'on_update'):
						insert_contacts_to_google_contacts(contact, 'after_insert')
			contact.reload()
			if(last_contact):
				contact.update({
					'sync_with_google_contacts':1,
					'google_contacts':last_contact,
				})
			contact.run_post_save_methods = lambda **args:0
			contact.insert = lambda **args:0
			contact.flags.ignore_validate = True
			contact.save()
			frappe.log_error(message=f"Contact {'Synced Successfully for '+ self.name if len(google_contacts) else 'Not Synced '+ self.name}", title=f'G-Contact {"Synced Successfully" if len(google_contacts) else "Sync Disabled or No Contact is mentioned for those sites"}')
		except Exception as e:
			frappe.log_error(message=f'{e}\n\n\n<b>DOC:</b>\n{frappe.as_json(contact)}\n\n\n<b>Traceback:</b>\n{frappe.get_traceback()}', title=f'Google Contact Sync Error {self.name}')

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

	def update_contacts_to_google_contacts(self,doc, method=None):
		"""
		Syncs Contacts from Google Contacts.
		https://developers.google.com/people/api/rest/v1/people/updateContact
		"""
		# Workaround to avoid triggering updation when Event is being inserted since
		# creation and modified are same when inserting doc
		if (
			not frappe.db.exists("Google Contacts", {"name": doc.google_contacts})
			or doc.modified == doc.creation
			or not doc.sync_with_google_contacts
		):
			return

		if doc.sync_with_google_contacts and not doc.google_contacts_id:
			# If sync_with_google_contacts is checked later, then insert the contact rather than updating it.
			insert_contacts_to_google_contacts(doc)
			return

		google_contacts, account = get_google_contacts_object(doc.google_contacts)

		if not account.push_to_google_contacts:
			return

		names = {"givenName": doc.first_name, "middleName": doc.middle_name, "familyName": doc.last_name}

		phoneNumbers = [{"value": phone_no.phone} for phone_no in doc.phone_nos]
		emailAddresses = [{"value": email_id.email_id} for email_id in doc.email_ids]

		try:
			contact = (
				google_contacts.people()
				.get(
					resourceName=doc.google_contacts_id,
					personFields="names,emailAddresses,organizations,phoneNumbers",
				)
				.execute()
			)

			contact["names"] = [names]
			contact["phoneNumbers"] = phoneNumbers
			contact["emailAddresses"] = emailAddresses

			google_contacts.people().updateContact(
				resourceName=doc.google_contacts_id,
				body={
					"names": [names],
					"phoneNumbers": phoneNumbers,
					"emailAddresses": emailAddresses,
					"etag": contact.get("etag"),
				},
				updatePersonFields="names,emailAddresses,organizations,phoneNumbers",
			).execute()
			frappe.msgprint(_("Contact Synced with Google Contacts."))
			return True
		except HttpError as err:
			frappe.msgprint(
				_("Google Contacts - Could not update contact in Google Contacts {0}, error code {1}.").format(
					account.name, err.resp.status
				)
			)
			return False

	def on_trash(self):
		if(frappe.db.exists('Dynamic Link', {'link_doctype':'Lead Management', 'link_name':self.name, 'parenttype': "Contact"})):
				contact_name = frappe.db.get_all('Dynamic Link', filters={'link_doctype':'Lead Management', 'link_name':self.name, 'parenttype': "Contact"}, pluck = 'parent')
				for i in contact_name:
					frappe.delete_doc('Contact', i)
