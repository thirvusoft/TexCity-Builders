import frappe
from frappe.utils import now_datetime, nowdate
from hrms.hr.doctype.shift_assignment.shift_assignment import get_employee_shift


def get_default_shift(employee=None):
    if not employee:
        return ""
    shift_details = get_employee_shift(employee)
    if shift_details:
        return shift_details["shift_type"]["name"]
    return ""

@frappe.whitelist()
def create_checkin(lat=None, long=None):
    emp = frappe.db.get_value("Employee", {"status":"Active", "user_id":frappe.session.user}, "name")
    doc = frappe.new_doc("Employee Checkin")
    shift_type = get_default_shift(emp)
    doc.update({
        "user":frappe.session.user,
        "employee":emp,
        "log_type":"IN",
        "time":now_datetime(),
        "checkin_latitude":lat,
        "checkin_longitude":long,
        "shift":shift_type
    })
    doc.flags.ignore_mandatory = True
    doc.insert()
    return True

@frappe.whitelist()
def create_checkout(lat=None, long=None):
    emp = frappe.db.get_value("Employee", {"status":"Active", "user_id":frappe.session.user}, "name")
    doc = frappe.new_doc("Employee Checkin")
    shift_type = get_default_shift(emp)
    doc.update({
        "user":frappe.session.user,
        "employee":emp,
        "log_type":"OUT",
        "time":now_datetime(),
        "checkout_latitude":lat,
        "checkout_longitude":long,
        "shift":shift_type
    })
    doc.flags.ignore_mandatory = True
    doc.insert()
    return True