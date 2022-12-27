import frappe

def after_install():
    create_roles()

def create_roles():
    if(not frappe.db.exists('Role', 'Texcity Admin')):
        doc = frappe.new_doc('Role', 'Texcity Admin')
        doc.role_name = 'Texcity Admin'
        doc.save()