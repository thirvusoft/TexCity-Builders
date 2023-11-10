import frappe

def warehouse_creation(doc,event):
    if doc.is_new():
        warehouse=frappe.new_doc("Warehouse")
        warehouse.warehouse_name=doc.project_name
        warehouse.is_group=doc.is_group
        if doc.get("parent_project"):
            warehouse.parent_warehouse=frappe.get_value('Project', doc.parent_project, 'custom_warehouse')
            
        warehouse.company=doc.company
        warehouse.save(ignore_permissions = True)
        doc.custom_warehouse=warehouse.name
    else:
        warehouse_doc=frappe.get_doc("Warehouse",{"warehouse_name":doc.name})
        warehouse_doc.update({
            'is_group': doc.is_group,
            **({
                'parent_warehouse': frappe.get_value('Project', doc.parent_project, 'custom_warehouse')
            } if doc.get("parent_project") else {})
        })
        warehouse_doc.save()
