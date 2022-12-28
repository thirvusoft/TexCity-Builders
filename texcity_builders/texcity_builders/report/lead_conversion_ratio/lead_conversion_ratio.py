# Copyright (c) 2022, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe
from collections import OrderedDict


def execute(filters={}):
	columns, data = get_columns() or [], get_data(filters) or []
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

def get_columns():
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
			'fieldname':'status',
			'label':'Status',
			'fieldtype':'Data',
			'width':240
		},
		{
			'fieldname':'place_of_call',
			'label':'Place Of Call',
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
		site_filt['site'] = ['in', filters.get('site')]
	leads = frappe.db.get_all('Lead Management', filters=lead_filt, fields=['name', 'lead_name', 'whatsapp_no', 'status', 'posting_date', 'place_of_call', 'area', 'channel_through'], order_by = 'posting_date')
	leads_with_sites = frappe.db.get_all('Multiselect Site', filters=site_filt, pluck='parent')
	if(filters.get('site')):
		leads = [i for i in leads if i['name'] in leads_with_sites]
	return leads