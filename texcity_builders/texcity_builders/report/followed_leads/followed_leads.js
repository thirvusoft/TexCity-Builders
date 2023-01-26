// Copyright (c) 2023, Thirvusoft Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Followed Leads"] = {
	"filters": [
		{
			fieldname:'site',
			label:'Site',
			fieldtype:'Link',
			options:'Site',
			filters:{'sold_out':0, 'disabled':0}
		},
		{
			fieldname:'follow_date',
			label:'Follow Up Date',
			fieldtype:'Date',
			default:'Today'
		}
	]
};
