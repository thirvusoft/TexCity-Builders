from . import __version__ as app_version

app_name = "texcity_builders"
app_title = "Texcity Builders"
app_publisher = "Thirvusoft Private Limited"
app_description = "Lead Management"
app_email = "info@thirvusoft.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/texcity_builders/css/texcity_builders.css"
app_include_js = ["assets/texcity_builders/js/lead_management_quick_entry.js", "assets/texcity_builders/js/desk.js"]

# include js, css files in header of web template
# web_include_css = "/assets/texcity_builders/css/texcity_builders.css"
# web_include_js = "/assets/texcity_builders/js/texcity_builders.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "texcity_builders/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Contact" : "texcity_builders/custom/js/contact.js",
	"Project" : "texcity_construction/custom/js/project.js",
    "User":"texcity_builders/custom/js/user.js",
    "Employee Checkin":"texcity_builders/custom/js/employee_checkin.js"
    }
doctype_list_js = {"Employee Checkin" : "/texcity_builders/custom/js/employee_checkin_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "texcity_builders.utils.jinja_methods",
#	"filters": "texcity_builders.utils.jinja_filters"
# }
after_migrate = "texcity_builders.install.after_install"
# Installation
# ------------

# before_install = "texcity_builders.install.before_install"
after_install = "texcity_builders.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "texcity_builders.uninstall.before_uninstall"
# after_uninstall = "texcity_builders.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "texcity_builders.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Project": {
		"validate": "texcity_builders.texcity_construction.custom.py.project.warehouse_creation",
		
	},
	"Purchase Invoice":{
		"on_submit":"texcity_builders.texcity_builders.custom.py.purchase_invoice.project_value_updation",
		"on_cancel":"texcity_builders.texcity_builders.custom.py.purchase_invoice.project_value_reduction"
	},
	"Sales Invoice":{
		"on_submit":"texcity_builders.texcity_builders.custom.py.sales_invoice.project_value_updation_si",
		"on_cancel":"texcity_builders.texcity_builders.custom.py.sales_invoice.project_value_reduction_si"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"frappe.integrations.doctype.google_contacts.google_contacts.sync",
        "texcity_builders.texcity_builders.custom.py.location.get_current_location"
	],
}
#	"daily": [
#		"texcity_builders.tasks.daily"
#	],
#	"hourly": [
#		"texcity_builders.tasks.hourly"
#	],
#	"weekly": [
#		"texcity_builders.tasks.weekly"
#	],
#	"monthly": [
#		"texcity_builders.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "texcity_builders.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "texcity_builders.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "texcity_builders.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"texcity_builders.auth.validate"
# ]
