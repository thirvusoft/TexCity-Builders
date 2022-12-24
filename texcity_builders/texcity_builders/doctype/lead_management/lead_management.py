# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
