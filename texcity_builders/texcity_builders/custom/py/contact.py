import frappe

@frappe.whitelist()
def update_contact_for_lead(cn_name, value=0, lead_doc=None):
    frappe.db.sql(f'''
        update `tabContact` set lead_created={value}
				where name='{cn_name}'
        ''')
    if(value and lead_doc):
      dn = frappe.new_doc('Dynamic Link')
      dn.update({
        'link_doctype':'Lead Management',
        'link_name': lead_doc,
        'link_title':lead_doc,
        'parent':cn_name,
        'parenttype':'Contact',
        'parentfield':'links'
      })
      dn.insert()