# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe


def execute(filters={}):
	columns, data = get_columns() or [], get_data(filters) or []
	return columns, data



def get_columns():
	columns = [
		{
			'fieldname':'name',
			'fieldtype':'Link',
			'options':'Lead Management',
			'label':'Lead',
			'width':200
		},
		{
			'fieldname':'lead_name',
			'fieldtype':'Data',
			'label':'Lead Name',
			'width':200
		},
		{
			'fieldname':'status',
			'fieldtype':'Data',
			'label':'Status',
			'width':200
		},
		{
			'fieldname':'wa_number',
			'fieldtype':'Phone',
			'label':'Whatsapp No',
			'width':200
		},
		{
			'fieldname':'plot_type',
			'fieldtype':'Data',
			'label':'Plot Type',
			'width':200
		},
		{
			'fieldname':'site',
			'fieldtype':'Link',
			'label':'Site',
			'width':200,
			'options':'site'
		},
	]
	return columns


def get_data(filters):
	follow_up_filter = {}
	site_filter = {'parenttype':'Lead Management'}
	lead_filter = {'status':['not in', ['Do Not Contact']]}
	if(filters.get('follow_date')):
		follow_up_filter['next_follow_up_date'] = filters.get('follow_date')
	if(filters.get('site')):
		site_filter['site'] = filters.get('site')

	leads = frappe.db.get_all('Follow Ups', filters=follow_up_filter, pluck='parent')
	site_filter['parent'] = ['in', leads]
	site_lead = frappe.db.get_all('Multiselect Site', filters=site_filter, pluck='parent')
	lead_filter['name'] = ['in', site_lead]

	leads = frappe.db.get_all('Lead Management', filters=lead_filter, fields=['name', 'lead_name', 'whatsapp_no as wa_number', 'status', 'plot_type'])
	
	return leads