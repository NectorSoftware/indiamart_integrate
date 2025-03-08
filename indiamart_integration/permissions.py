# # File: /home/ubuntu/frappe-bench/apps/indiamart_integration/indiamart_integration/permissions.py

# def lead_permission(doc, ptype, user, debug=False):
#     """Dummy permission function to avoid import errors."""
#     return True
# # Problematic permissions.py
from indiamart_integration import __version__
import frappe

def lead_permission(doc, user):
    return frappe.has_permission("Lead", "read", user=user)