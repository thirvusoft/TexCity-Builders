import frappe
from frappe.utils import now_datetime, nowdate

@frappe.whitelist()
def create_checkin(lat=None, long=None):
    emp = frappe.db.get_value("Employee", {"status":"Active", "user_id":frappe.session.user}, "name")
    doc = frappe.new_doc("Employee Checkin")
    doc.update({
        "user":frappe.session.user,
        "employee":emp,
        "log_type":"IN",
        "time":now_datetime(),
        "checkin_latitude":lat,
        "checkin_longitude":long
    })
    doc.flags.ignore_mandatory = True
    doc.insert()
    return True

@frappe.whitelist()
def create_checkout(lat=None, long=None):
    emp = frappe.db.get_value("Employee", {"status":"Active", "user_id":frappe.session.user}, "name")
    doc = frappe.new_doc("Employee Checkin")
    doc.update({
        "user":frappe.session.user,
        "employee":emp,
        "log_type":"OUT",
        "time":now_datetime(),
        "checkout_latitude":lat,
        "checkout_longitude":long
    })
    doc.flags.ignore_mandatory = True
    doc.insert()
    return True