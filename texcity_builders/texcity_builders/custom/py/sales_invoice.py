import frappe

def project_value_updation_si(doc, action):
    if doc.project:
        if doc.is_return != 1:
            si_project=frappe.get_doc("Project", {"name": doc.project})
            si_project.custom_total_net_total += doc.net_total or 0
            si_project.custom_total_taxes_and_charges += doc.total_taxes_and_charges or 0
            si_project.custom_total_value += doc.grand_total or 0
            si_project.save()
        else:
            si_project=frappe.get_doc("Project", {"name": doc.project})
            si_project.custom_return_total_net_sales += doc.net_total or 0
            si_project.custom_return_total_tax_sales += doc.total_taxes_and_charges or 0
            si_project.custom_return_total_sales += doc.grand_total or 0
            si_project.save()
            
            
def project_value_reduction_si(doc, action):
    if doc.project:
        if doc.is_return != 1:
            si_project=frappe.get_doc("Project", {"name": doc.project})
            si_project.custom_total_net_total -= doc.net_total or 0
            si_project.custom_total_taxes_and_charges -= doc.total_taxes_and_charges or 0
            si_project.custom_total_value -= doc.grand_total or 0
            si_project.save()  
        else:
            si_project=frappe.get_doc("Project", {"name": doc.project})
            si_project.custom_return_total_net_sales -= doc.net_total or 0
            si_project.custom_return_total_tax_sales -= doc.total_taxes_and_charges or 0
            si_project.custom_return_total_sales -= doc.grand_total or 0
            si_project.save()