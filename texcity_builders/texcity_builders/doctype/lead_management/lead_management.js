// Copyright (c) 2022, Thirvusoft Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lead Management', {
	refresh: function(frm){
		frm.set_query('site', 'site_visit', function(){
			return {
				filters:{ disabled:0, sold_out:0 }
			}
		})
	},
	request_for_site: function(frm){
		if(frm.doc.request_for_site.find(element => element.site=='Others')){
			frm.set_value('site__others_checked', 1)
		}
		else{
			frm.set_value('site__others_checked', 0)
		}
	}
});

frappe.ui.form.on('Follow Ups', {
	status: function(frm, cdt, cdn){
		var row = locals[cdt][cdn]
		frm.set_value('status', row.status)
	}
})