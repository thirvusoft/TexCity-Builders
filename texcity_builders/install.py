import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_install():
    create_property_setters()
    create_default_site()
    create_roles()
    create_lead_types()
    create_plot_type()

def create_property_setters():
    make_property_setter('Territory', 'quick_entry', 'quick_entry',1, 'Check', for_doctype=1)
    make_property_setter('Territory', 'territory_name', 'allow_in_quick_entry', 1, 'Check')
    make_property_setter('Territory', 'territory_name', 'bold', 1, 'Check')

def create_roles():
    if(not frappe.db.exists('Role', 'Texcity Admin')):
        doc = frappe.new_doc('Role')
        doc.role_name = 'Texcity Admin'
        doc.save()

def create_lead_types():
    lead_types = ['Channel Partner', 'Client', 'Consultant']
    for i in lead_types:
        if(not frappe.db.exists('Lead Type', i)):
            doc = frappe.new_doc('Lead Type')
            doc.lead_type = i
            doc.save()

def create_plot_type():
    plot_types = ['Appartment', 'Land Only', 'Land With Building', 'Ready To Occupy']
    for i in plot_types:
        if(not frappe.db.exists('Plot Type', i)):
            doc = frappe.new_doc('Plot Type')
            doc.plot_type = i
            doc.save()

def create_default_site():
    if(not frappe.db.exists('Site', 'Others')):
        doc = frappe.new_doc('Site')
        doc.site_name = 'Others'
        doc.save()