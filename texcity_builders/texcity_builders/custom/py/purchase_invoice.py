import frappe

def project_value_updation(doc, action):
    if doc.project:
        if doc.is_return != 1:
            pi_project=frappe.get_doc("Project", {"name": doc.project})
            pi_project.custom_net_total_purchase += doc.net_total or 0
            pi_project.custom_total_taxes_purchase += doc.total_taxes_and_charges or 0
            pi_project.custom_total_value_purchase += doc.grand_total or 0
            pi_project.save()
        else:
            pi_project=frappe.get_doc("Project", {"name": doc.project})
            pi_project.custom_return_total_net_purchase += doc.net_total or 0
            pi_project.custom_return_total_taxes_purchase += doc.total_taxes_and_charges or 0
            pi_project.custom_return_total_purchase += doc.grand_total or 0
            pi_project.save()
            
            
def project_value_reduction(doc, action):
    if doc.project:
        if doc.is_return != 1:
            pi_project=frappe.get_doc("Project", {"name": doc.project})
            pi_project.custom_net_total_purchase -= doc.net_total or 0
            pi_project.custom_total_taxes_purchase -= doc.total_taxes_and_charges or 0
            pi_project.custom_total_value_purchase -= doc.grand_total or 0
            pi_project.save()
        else:
            pi_project=frappe.get_doc("Project", {"name": doc.project})
            pi_project.custom_return_total_net_purchase -= doc.net_total or 0
            pi_project.custom_return_total_taxes_purchase -= doc.total_taxes_and_charges or 0
            pi_project.custom_return_total_purchase -= doc.grand_total or 0
            pi_project.save()
            
              
