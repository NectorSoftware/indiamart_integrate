# # apps/indiamart_integration/indiamart_integration/hooks.py
# # from .__init__ import app_version  # Import from __init__.py
# # get version from __version__ variable in indiamart_integration/__init__.py

# #from indiamart_integration.__init__ import __version__ as app_version
# from . import __version__ as app_version


# app_name = "indiamart_integration"
# app_title = "IndiaMart Integration"
# app_publisher = "Bhavesh Maheshwari"
# app_description = "IndiaMart Integration"
# app_icon = "octicon octicon-sync"
# app_color = "#38a169"
# app_email = "maheshwaribhavesh95863@gmail.com"
# app_license = "MIT"
# app_version = app_version  # Explicitly set to ensure propagation

# # Includes in <head>
# # app_include_css = "/assets/indiamart_integration/css/indiamart_integration.css"
# # app_include_js = "/assets/indiamart_integration/js/indiamart_integration.js"

# # web_include_css = "/assets/indiamart_integration/css/indiamart_leads.css"
# # web_include_js = "/assets/indiamart_integration/js/indiamart_leads.js"

# # Fixtures
# fixtures = [
#     {
#         "doctype": "Lead Source",
#         "filters": {"source_name": "India Mart"}
#     },
#     {
#         "doctype": "Custom Field",
#         "filters": {"dt": "Lead", "fieldname": ["in", [
#             "custom_call_duration", "custom_unique_query_id", "custom_query_type",
#             "custom_sender_name", "custom_subject", "custom_sender__company",
#             "custom_sender_address", "custom_sender_city", "custom_sender_state",
#             "custom_sender_pincode", "custom_sender_country_iso",
#             "custom_query_product_name", "custom_query_message", "custom_query_mcat_name",
#             "custom_reciever_mobile", "custom_reciever_catalog"
#         ]]}
#     }
# ]

# # Website Routing
# website_route_rules = [
#     {"from_route": "/indiamart-leads", "to_route": "IndiaMART Leads Management"}
# ]

# # Installation
# after_install = "indiamart_integration.install.after_install"
# after_migrate = "indiamart_integration.install.after_migrate"

# # Testing
# before_tests = "indiamart_integration.install.before_tests"

# # Scheduled Tasks
# scheduled_tasks = [
#     {
#         "method": "indiamart_integration.api.cron_sync_lead",
#         "frequency": "Cron",
#         "cron_format": "*/5 * * * *"  # Runs every 5 minutes
#     }
# ]

# # Permissions
# has_permission = {
#     "Lead": "indiamart_integration.permissions.lead_permission"
# }
# # hooks.py

from .api import cron_sync_lead, sync_india_mart_lead, add_lead_hook

# App metadata
app_name = "indiamart_integration"
app_title = "IndiaMart Integration"
app_publisher = "Bhavesh Maheshwari"
app_description = "IndiaMart Integration"
app_icon = "octicon octicon-sync"
app_color = "#38a169"
app_email = "maheshwaribhavesh95863@gmail.com"
app_license = "MIT"
app_version = "0.0.1"

# Scheduler Events
scheduler_events = {
    "cron": {
        "*/6 * * * *": [
            "indiamart_integration.api.cron_sync_lead"
        ]
    }
}

# Document Events
doc_events = {
    "Lead": {
        "after_insert": "indiamart_integration.api.add_lead_hook"
    }
}

# Permissions
fixtures = [
    {
        "doctype": "Custom Role",
        "name": "IndiaMART Sync Manager",
        "role": "System Manager",
        "permissions": [
            {
                "doctype": "IndiaMart Setting",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }
        ]
    },
    {
        "doctype": "DocType",
        "name": "IndiaMart Setting"
    }
]

# Override standard behavior
bootinfo = "indiamart_integration.boot.boot_session"

# Website
website_route_rules = [
    {"from_route": "/indiamart-leads", "to_route": "indiamart_integration.views.leads"}
]