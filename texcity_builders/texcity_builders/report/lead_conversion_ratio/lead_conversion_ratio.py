# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from collections import OrderedDict


def execute(filters={},hide_preferred_site_location=1):
	if(filters.get('site')):
		if(filters.get('site') == 'Others'):hide_preferred_site_location=0
	columns, data = get_columns(hide_preferred_site_location) or [], get_data(filters) or []
	chart_summary = get_chart_summary(data)
	chart_data = get_chart_data(data)
	return columns, data, None, chart_data, chart_summary


def get_chart_summary(data):
	status1 = OrderedDict({i.get('title'):0 for i in frappe.get_meta('Lead Management').get('states') or []})
	for i in data:
		if(i.get('status') not in status1.keys()):
			status1[i.get('status')] = 1
		else:
			status1[i.get('status')] += 1
	status = status1.copy()
	for i in status1:
		if(status[i] == 0):
			status.pop(i)
	color =  OrderedDict({})
	summary = []
	for i in frappe.get_meta('Lead Management').get('states') or []:
		color[i.get('title')] = i.get('color')
	for i in status:
		summary.append(
		{
			"value":  status[i] or "Not Mentioned",
			"label": f'''<p><span style="color:{color.get(i).lower() if color.get(i) else ''}; font-weight: bold; font-size:20px;">{i }</span></p>''',
			"datatype": "Float",
		}
		)
	summary.append(
		{
			"value":  sum(status.values()) or 0,
			"label": "<b style='font-size:20px;color:#ff5500'>Total Enquiry</b>",
			"datatype": "Float",
		}
		)
	return summary

def get_chart_data(data):
	status1 = OrderedDict({i.get('title'):0 for i in frappe.get_meta('Lead Management').get('states') or []})
	for i in data:
		if(i.get('status') not in status1.keys()):
			status1[i.get('status')] = 1
		else:
			status1[i.get('status')] += 1
	status = status1.copy()
	for i in status1:
		if(status[i] == 0):
			status.pop(i)
	color =  OrderedDict({})
	for i in frappe.get_meta('Lead Management').get('states') or []:
		color[i.get('title')] = i.get('color')
	labels = list(status.keys())
	values = list(status.values())
	chart_data = {
		"data": {
			"labels": labels,
			"datasets": [{"name": "Expected Qty", "values": values}],
		},
		"type": "line",
		'colors':['green', 'blue'],
		"barOptions": {"stacked": 1},
	}
	return chart_data

def get_columns(hide_preferred_site_location=1):
	columns = [
		{
			'fieldname':'name',
			'label':'Lead ID',
			'fieldtype':'Link',
			'options':'Lead Management',
			'width':240
		},
		{
			'fieldname':'posting_date',
			'label':'Creation Date',
			'fieldtype':'Date',
			'width':240
		},
		{
			'fieldname':'lead_name',
			'label':'Lead Name',
			'fieldtype':'Data',
			'width':240
		},
		{
			'fieldname':'whatsapp_no',
			'label':'WhatsApp No',
			'fieldtype':'Data',
			'width':240
		},
		{
			'fieldname':'site',
			'label':'Site',
			'fieldtype':'Data',
			'width':240,
			'length':1000
		},
		{
			'fieldname':'description',
			'label':'Description (Last Follow Up)',
			'fieldtype':'Data',
			'width':240,
			'length':1000
		},
		{
			'fieldname':'status',
			'label':'Status',
			'fieldtype':'Data',
			'width':240
		},
		{
			'fieldname':'area',
			'label':'Area(Native)',
			'fieldtype':'Data',
			'width':240
		},
		{
			'fieldname':'preferred_site_location',
			'label':'Preferred Site Location',
			'fieldtype':'Data',
			'width':240,
			'hidden':hide_preferred_site_location
		},
		{
			'fieldname':'channel_through',
			'label':'Channel Through',
			'fieldtype':'Data',
			'width':240
		},
	]
	return columns


def get_data(filters):
	lead_filt = {}
	site_filt = {}
	if(filters.get('start_date')):
		lead_filt['posting_date'] = ['>=', filters.get('start_date')]
	if(filters.get('end_date')):
		lead_filt['posting_date'] = ['<=', filters.get('end_date')]
	if(filters.get('start_date') and filters.get('end_date')):
		lead_filt['posting_date'] = ['between', (filters.get('start_date'), filters.get('end_date'))]
	if(filters.get('site')):
		site_filt['site'] =  filters.get('site')
	leads = frappe.db.get_all('Lead Management', filters=lead_filt, fields=['name', 'lead_name', 'whatsapp_no', 'status', 'posting_date', 'area', 'channel_through', 'preferred_site_location'], order_by = 'posting_date')
	leads_with_sites = frappe.db.get_all('Multiselect Site', filters=site_filt, pluck='parent')
	if(filters.get('site')):
		leads = [i for i in leads if i['name'] in leads_with_sites]
	for i in leads:
		i['site'] = ', '.join(frappe.db.get_all('Multiselect Site', filters={'parent':i['name']}, pluck='site'))
		i['description'] = frappe.db.get_value('Follow Ups', {'parent':i['name']}, 'description', order_by='idx desc')
	return leads