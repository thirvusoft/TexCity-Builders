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
			'width':240
		},
		{
			'fieldname':'lead_name',
			'fieldtype':'Data',
			'label':'Lead Name',
			'width':240
		},
		{
			'fieldname':'status',
			'fieldtype':'Data',
			'label':'Status',
			'width':240
		},
		{
			'fieldname':'wa_number',
			'fieldtype':'Phone',
			'label':'Whatsapp No',
			'width':240
		},
		{
			'fieldname':'plot_type',
			'fieldtype':'Data',
			'label':'Plot Type',
			'width':240
		},
	]
	return columns


def get_data(filters):
	follow_up_filter = {}
	site_filter = {'parenttype':'Lead Management'}
	lead_filter = {'status':['not in', ['Do Not Contact']]}
	if(filters.get('follow_date')):
		follow_up_filter['date'] = filters.get('follow_date')
	if(filters.get('site')):
		site_filter['site'] = filters.get('site')

	all_leads1 = frappe.db.get_all('Follow Ups', filters=follow_up_filter, fields=['idx', 'parent'])
	# all_leads1=[]
	# for i in all_leads:
	# 	follow_up_filter['parent'] = i['parent']
		
	# 	if(max(frappe.db.get_all('Follow Ups', filters={'parent':i['parent']}, pluck='idx')) != i['idx']):
	# 		all_leads1.append(i)


	leads = [i['parent'] for i in all_leads1]
	site_filter['parent'] = ['in', leads]
	site_lead=leads
	if(filters.get('site')):
		site_lead = frappe.db.get_all('Multiselect Site', filters=site_filter, pluck='parent')
	lead_filter['name'] = ['in', site_lead]

	leads = frappe.db.get_all('Lead Management', filters=lead_filter, fields=['name', 'lead_name', 'whatsapp_no as wa_number', 'status', 'plot_type'])
	
	return leads