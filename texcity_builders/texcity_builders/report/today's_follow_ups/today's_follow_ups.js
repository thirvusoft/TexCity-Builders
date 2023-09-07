// Copyright (c) 2022, Thirvusoft Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Today's Follow Ups"] = {
	"filters": [
		{
			fieldname:'follow_date',
			label:'Follow Up Date',
			fieldtype:'Date',
			default:'Today'
		},
		{
			fieldname:'site',
			label:'Site',
			fieldtype:'Link',
			options:'Site',
			filters:{'sold_out':0, 'disabled':0}
		},
		{
			fieldname:'follow_up_by',
			label:'Follow Up By',
			fieldtype:'Link',
			options:'Users List'
		},
		{
			fieldname:'show_unassigned_lead',
			label:'Show Unassigned Lead',
			fieldtype:'Check',
			default:1
		}
	]
};
