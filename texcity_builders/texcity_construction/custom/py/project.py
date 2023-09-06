import frappe

def warehouse_creation(doc,event):
    if doc.is_new():
        warehouse=frappe.new_doc("Warehouse")
        warehouse.warehouse_name=doc.project_name
        warehouse.is_group=doc.is_group
        warehouse.parent_project=doc.parent_project
        warehouse.company=doc.company
        warehouse.save(ignore_permissions = True)
    else:
        warehouse_doc=frappe.get_doc("Warehouse",{"warehouse_name":doc.name})
        warehouse_doc.update({
            'is_group': doc.is_group,
            'parent_warehouse': doc.parent_project
        })
        warehouse_doc.save()
