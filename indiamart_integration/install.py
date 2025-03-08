import frappe

def after_install():
    """Run after app installation."""
    from .api import add_source_lead  # Moved inside the function
    add_source_lead()  # Ensure "India Mart" Lead Source is created

def after_migrate():
    """Run after migration to ensure custom fields exist."""
    create_custom_fields()

def before_tests():
    """Run before tests."""
    frappe.db.truncate("Lead")  # Clear Leads for a clean test slate
    from .api import add_source_lead  # Moved inside the function
    add_source_lead()

def create_custom_fields():
    """Create custom fields for Lead doctype."""
    custom_fields = {
        "Lead": [
            {"fieldname": "custom_call_duration", "label": "Call Duration", "fieldtype": "Data"},
            {"fieldname": "custom_unique_query_id", "label": "Unique Query ID", "fieldtype": "Data", "unique": 1},
            {"fieldname": "custom_query_type", "label": "Query Type", "fieldtype": "Data"},
            {"fieldname": "custom_sender_name", "label": "Sender Name", "fieldtype": "Data"},
            {"fieldname": "custom_subject", "label": "Subject", "fieldtype": "Data"},
            {"fieldname": "custom_sender__company", "label": "Sender Company", "fieldtype": "Data"},
            {"fieldname": "custom_sender_address", "label": "Sender Address", "fieldtype": "Small Text"},
            {"fieldname": "custom_sender_city", "label": "Sender City", "fieldtype": "Data"},
            {"fieldname": "custom_sender_state", "label": "Sender State", "fieldtype": "Data"},
            {"fieldname": "custom_sender_pincode", "label": "Sender Pincode", "fieldtype": "Data"},
            {"fieldname": "custom_sender_country_iso", "label": "Sender Country ISO", "fieldtype": "Data"},
            {"fieldname": "custom_query_product_name", "label": "Query Product Name", "fieldtype": "Data"},
            {"fieldname": "custom_query_message", "label": "Query Message", "fieldtype": "Text"},
            {"fieldname": "custom_query_mcat_name", "label": "Query MCAT Name", "fieldtype": "Data"},
            {"fieldname": "custom_reciever_mobile", "label": "Receiver Mobile", "fieldtype": "Data"},
            {"fieldname": "custom_reciever_catalog", "label": "Receiver Catalog", "fieldtype": "Data"}
        ]
    }
    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    **field
                }).insert(ignore_permissions=True)