# Copyright (c) 2023, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UsersList(Document):
	def before_save(self):
		if(self.mobile_no):
			frappe.errprint(self.mobile_no)
			frappe.errprint(len(self.mobile_no.split('-')[-1]))
			if(len(self.mobile_no.split('-')[-1]) < 1):
				frappe.errprint(self.mobile_no)
				self.mobile_no = ''
		if(self.whatsapp_no):
			if(len(self.whatsapp_no.split('-')[-1]) < 1):
				self.whatsapp_no = ''

