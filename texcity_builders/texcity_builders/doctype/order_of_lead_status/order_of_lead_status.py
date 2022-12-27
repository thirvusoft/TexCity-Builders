# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OrderofLeadStatus(Document):
	def validate(self):
		status = []
		for i in self.select_order:
			status.append(i.status)
		msg = ''
		for i in set(status):
			if(status.count(i)>1):
				msg += f'<p>{i} appears {status.count(i)} times</p>'
		if(msg):
			frappe.throw(title='Duplicate Entry', msg=msg)
