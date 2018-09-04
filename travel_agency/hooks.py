# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "travel_agency"
app_title = "Travel Agency"
app_publisher = "Element Labs"
app_description = "ERPNext Module for Travel Agents"
app_icon = "fa fa-plane"
app_color = "blue"
app_email = "saeed@elementlabs.xyz"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/travel_agency/css/travel_agency.css"
# app_include_js = "/assets/travel_agency/js/travel_agency.js"

# include js, css files in header of web template
# web_include_css = "/assets/travel_agency/css/travel_agency.css"
# web_include_js = "/assets/travel_agency/js/travel_agency.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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

# Website user home page (by function)
# get_website_user_home_page = "travel_agency.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "travel_agency.install.before_install"
# after_install = "travel_agency.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "travel_agency.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"travel_agency.tasks.all"
# 	],
# 	"daily": [
# 		"travel_agency.tasks.daily"
# 	],
# 	"hourly": [
# 		"travel_agency.tasks.hourly"
# 	],
# 	"weekly": [
# 		"travel_agency.tasks.weekly"
# 	]
# 	"monthly": [
# 		"travel_agency.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "travel_agency.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "travel_agency.event.get_events"
# }

