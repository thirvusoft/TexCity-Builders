// Copyright (c) 2022, Thirvusoft Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Conversion Ratio"] = {
	"filters": [
		{
			fieldname:'start_date',
			label:'Start Date',
			fieldtype:'Date',
		},
		{
			fieldname:'end_date',
			label:'End Date',
			fieldtype:'Date',
		},
		{
			"fieldname":"site",
			"label": "Site",
			"fieldtype": "MultiSelectList",
			"options": "Site",
			get_data: function(txt) {
				return frappe.db.get_link_options('Site', txt, {
					
				});
			}
		},
	]
};
