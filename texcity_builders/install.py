import frappe

def after_install():
    create_roles()
    create_lead_types()
    create_plot_type()

def create_roles():
    if(not frappe.db.exists('Role', 'Texcity Admin')):
        doc = frappe.new_doc('Role', 'Texcity Admin')
        doc.role_name = 'Texcity Admin'
        doc.save()

def create_lead_types():
    lead_types = ['Channel Partner', 'Client', 'Consultant']
    for i in lead_types:
        if(not frappe.db.exists('Lead Type', i)):
            doc = frappe.new_doc('Lead Type', i)
            doc.lead_type = i
            doc.save()

def create_plot_type():
    plot_types = ['Appartment', 'Land Only', 'Land With Building', 'Ready TO Occupy']
    for i in plot_types:
        if(not frappe.db.exists('Plot Type', i)):
            doc = frappe.new_doc('Plot Type', i)
            doc.plot_type = i
            doc.save()