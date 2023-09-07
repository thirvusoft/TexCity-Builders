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
			'width':182
		},
		{
			'fieldname':'lead_name',
			'fieldtype':'Data',
			'label':'Lead Name',
			'width':230
		},
		{
			'fieldname':'status',
			'fieldtype':'Data',
			'label':'Status',
			'width':130
		},
		{
			'fieldname':'wa_number',
			'fieldtype':'Phone',
			'label':'Whatsapp No',
			'width':130
		},
		{
			'fieldname':'next_followup_by',
			'fieldtype':'Data',
			'label':'Follow Up By',
			'width':140
		},
		{
			'fieldname':'remarks',
			'fieldtype':'Data',
			'label':'Remarks',
			'width':400
		},
		{
			'fieldname':'description',
			'fieldtype':'Small Text',
			'label':'Description',
			'width':400
		},
		{
			'fieldname':'for_number_card',
			'fieldtype':'Float',
			'label':'For Number Card',
			'width':1,
			'hidden':1,
			'default':1
		}
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

	all_leads = frappe.db.get_all('Follow Ups', filters=follow_up_filter, fields=['idx', 'parent','next_followup_by','description'])
	all_leads1=[]
	for i in all_leads:
		follow_up_filter['parent'] = i['parent']
		
		if(max(frappe.db.get_all('Follow Ups', filters={'parent':i['parent']}, pluck='idx')) == i['idx']):
			if(not filters.get("follow_up_by") and filters.get("show_unassigned_lead")):
				if(not i.get("next_followup_by")):
					all_leads1.append(i)
			elif(not i.get("next_followup_by") and filters.get("show_unassigned_lead")):
				all_leads1.append(i)
			elif(not filters.get("follow_up_by")):
				all_leads1.append(i)
			elif(filters.get("follow_up_by") and i.get("next_followup_by")==filters.get("follow_up_by")):
				all_leads1.append(i)
	desc={i['parent']:[i['description'],i.get("next_followup_by") or ""] for i in all_leads1}

	leads = [i['parent'] for i in all_leads1]
	site_filter['parent'] = ['in', leads]
	site_lead=leads
	if(filters.get('site')):
		site_lead = frappe.db.get_all('Multiselect Site', filters=site_filter, pluck='parent')
	lead_filter['name'] = ['in', site_lead]

	leads = frappe.db.get_all('Lead Management', filters=lead_filter, fields=['name', 'lead_name', 'whatsapp_no as wa_number', 'status', 'remarks'])
	for i in leads:
		i['for_number_card'] = 1
		i['description']=desc[i["name"]][0]
		i['next_followup_by']=desc[i["name"]][1]
	return leads