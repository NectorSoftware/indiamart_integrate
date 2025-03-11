# # be carefull with above codr unning fine only issue is of sync button  06-Mar-2025
from __future__ import unicode_literals
import frappe
from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
from frappe import throw, msgprint, _
from datetime import datetime, timedelta
import re
import json
import traceback
import requests
import time
import urllib

@frappe.whitelist()
def add_source_lead():
    """Add India Mart as a Lead Source if it doesn't exist."""
    if not frappe.db.exists("Lead Source", "India Mart"):
        doc = frappe.get_doc({
            "doctype": "Lead Source",
            "source_name": "India Mart"
        }).insert(ignore_permissions=True)
        if doc:
            frappe.msgprint(_("Lead Source Added For India Mart"))
    else:
        frappe.msgprint(_("India Mart Lead Source Already Available"))

@frappe.whitelist()
def sync_india_mart_lead(from_date=None, to_date=None, **kwargs):
    frappe.log_error("Starting IndiaMART lead sync", "IndiaMART Sync Debug")
    print("Starting IndiaMART lead sync")  # Added
    try:
        # Fetch IndiaMart settings
        india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
        if not india_mart_setting.url or not india_mart_setting.key:
            frappe.throw(
                msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
                title=_("Missing Setting Fields")
            )

        # Set default dates if not provided
        if not from_date or not to_date:
            from_date = from_date or today()
            to_date = to_date or today()
        
        # Validate date range
        try:
            from_date = getdate(from_date)
            to_date = getdate(to_date)
            if from_date > to_date:
                frappe.throw(_("From Date cannot be greater than To Date."))
            if date_diff(to_date, from_date) > 7:
                frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
        except ValueError:
            frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

        # Construct request URL
        request_url = get_request_url(india_mart_setting, from_date, to_date)
        
        # Update last sync time
        current_time = now_datetime()
        india_mart_setting.last_api_call_time = current_time
        india_mart_setting.save(ignore_permissions=True)
        frappe.log_error(f"Updated last_api_call_time to {india_mart_setting.last_api_call_time}", "IndiaMART Sync Debug")
        print(f"Request URL: {request_url}")  # Added

        # Truncate the log title to fit within 140 characters
        log_title = f"Making API request to {request_url}"
        if len(log_title) > 140:
            log_title = log_title[:137] + "..."  # Truncate and add ellipsis
        frappe.log_error(log_title, "IndiaMART Sync Debug")
        
        # Make API request
        response = requests.get(request_url, timeout=30)
        response.raise_for_status()
        frappe.log_error("API request successful", "IndiaMART Sync Debug")

        # Parse response
        lead_data = response.json()
        frappe.log_error(f"IndiaMART API Response: {json.dumps(lead_data, indent=2)}", "IndiaMART Sync Debug")
        print(f"API Response: {json.dumps(lead_data, indent=2)}")  # Added

        if not lead_data or "RESPONSE" not in lead_data:
            frappe.log_error("No leads found in IndiaMART response", "IndiaMART Sync Warning")
            print("No new leads found from IndiaMART")  # Added
            frappe.msgprint(_("No new leads found from IndiaMART for the specified date range."))
            return

        leads = lead_data.get("RESPONSE", [])
        if not isinstance(leads, list):
            frappe.throw(_("Invalid response format from IndiaMART API. Expected a list of leads."))

        # Process each lead
        synced_lead_count = 0
        for lead in leads:
            frappe.log_error(f"Processing lead: {json.dumps(lead, indent=2)}", "IndiaMART Sync Debug")
            new_lead = add_lead(lead)
            if new_lead:
                synced_lead_count += 1
                frappe.log_error(f"Successfully synced lead: {new_lead.name}", "IndiaMART Sync Success")
                print(f"Synced lead: {new_lead.name}")  # Added
            else:
                frappe.log_error(f"Failed to sync lead: {json.dumps(lead, indent=2)}", "IndiaMART Sync Warning")

        print(f"Successfully synced {synced_lead_count} leads from IndiaMART")  # Added
        frappe.msgprint(_(f"Successfully synced {synced_lead_count} leads from IndiaMART."))

    except requests.exceptions.RequestException as e:
        frappe.log_error(f"API request failed: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Sync Error")
        india_mart_setting.retry_count = (india_mart_setting.retry_count or 0) + 1
        india_mart_setting.last_retry_time = current_time
        india_mart_setting.save(ignore_permissions=True)
        frappe.throw(_(f"Failed to sync IndiaMART leads: {str(e)}"))
    except Exception as e:
        # Truncate the error message if necessary to avoid further CharacterLengthExceededError
        error_message = f"Error syncing IndiaMART leads: {str(e)}"
        if len(error_message) > 140:
            error_message = error_message[:137] + "..."
        frappe.log_error(frappe.get_traceback(), "IndiaMART Sync Error")
        frappe.throw(_(error_message))

def get_request_url(india_mart_setting, from_date, to_date):
    """Construct the IndiaMART API URL."""
    base_url = india_mart_setting.url.strip()
    api_endpoint = "/wservce/crm/crmListing/v2/"

    if not base_url.endswith('/'):
        base_url += '/'

    formatted_from_date = from_date.strftime("%d-%b-%Y")  # e.g., "06-Mar-2025"
    formatted_to_date = to_date.strftime("%d-%b-%Y")

    params = {
        "glusr_crm_key": india_mart_setting.key,
        "start_time": formatted_from_date,
        "end_time": formatted_to_date
    }

    return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
# Assuming get_request_url is defined elsewhere (as per your earlier code)
def get_request_url(india_mart_setting, from_date, to_date):
    """Construct the IndiaMART API URL."""
    base_url = india_mart_setting.url.strip()
    api_endpoint = "/wservce/crm/crmListing/v2/"

    if not base_url.endswith('/'):
        base_url += '/'

    formatted_from_date = from_date.strftime("%d-%b-%Y")  # e.g., "06-Mar-2025"
    formatted_to_date = to_date.strftime("%d-%b-%Y")

    params = {
        "glusr_crm_key": india_mart_setting.key,
        "start_time": formatted_from_date,
        "end_time": formatted_to_date
    }

    return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

@frappe.whitelist()
def cron_sync_lead(from_date=None, to_date=None):
    """Scheduled job with rate limit awareness."""
    try:
        india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")

        if not from_date or not to_date:
            current_date = today()
            from_date = from_date or current_date
            to_date = to_date or current_date
        
        sync_india_mart_lead(from_date, to_date)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

def get_country_name(iso_code):
    """Map ISO country code to ERPNext country name."""
    country_map = {
        "IN": "India",
        "US": "United States",
        "GB": "United Kingdom",
    }
    
    country_name = country_map.get(iso_code)
    if not country_name and frappe.db.exists("Country", {"code": iso_code}):
        country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
    elif not country_name and frappe.db.exists("Country", iso_code):
        country_name = iso_code
    elif not country_name:
        frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
        country_name = "India"
    
    return country_name

@frappe.whitelist()
def add_lead(lead_data):
    """Create a Lead document aligned with customized ERPNext Lead DocType."""
    try:
        # Extract required fields with fallbacks
        unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
        if not unique_query_id:
            frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
            return None

        if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
            frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
            return None

        # Parse query time
        query_time = None
        if lead_data.get("QUERY_TIME"):
            try:
                query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

        # Get country name
        country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

        # Handle required fields with sensible defaults
        sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
        product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
        mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
        email = lead_data.get("SENDER_EMAIL", "")
        mobile = lead_data.get("SENDER_MOBILE", "")
        subject = lead_data.get("SUBJECT", "")

        # Determine lead status dynamically
        call_duration = cint(lead_data.get("CALL_DURATION", "0"))
        lead_status = "Open"  # Default status for new leads

        # Enhanced status logic based on IndiaMART data
        if email and frappe.db.exists("Customer", {"email_id": email}):
            lead_status = "Converted"
        elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
            lead_status = "Converted"
        elif call_duration > 0:
            lead_status = "Opportunity"
        elif "replied" in subject.lower():
            lead_status = "Replied"  # If the subject indicates a reply
        elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
            lead_status = "Interested"  # If the message indicates interest

        # Construct lead_name (required by ERPNext)
        suffix = f" (IM-{unique_query_id[-4:]})"
        lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
        if email and frappe.db.exists("Lead", {"email_id": email}):
            lead_name = (lead_name + suffix)[:140]
        elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
            lead_name = (lead_name + suffix)[:140]

        # Log the query type for debugging
        frappe.log_error(f"Assigning custom_query_type: {lead_data.get('QUERY_TYPE', 'Not Specified')}", "IndiaMART Lead Query Type Debug")

        # Create Lead document with mapped fields
        doc = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": lead_name,
            "source": "India Mart",
            "email_id": email,
            "mobile_no": mobile,
            "whatsapp_no": mobile,
            "phone": lead_data.get("SENDER_PHONE", ""),
            "company_name": lead_data.get("SENDER_COMPANY", ""),
            "city": lead_data.get("SENDER_CITY", ""),
            "state": lead_data.get("SENDER_STATE", ""),
            "country": country_name,
            "status": lead_status,
            "creation": query_time or now_datetime(),
            "modified": now_datetime(),
            "owner": frappe.session.user,
            "modified_by": frappe.session.user,
            "docstatus": 0,
            "idx": 0,
            "lead_owner": frappe.session.user,
            "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
            "custom_unique_query_id": unique_query_id,
            "custom_query_type": (lead_data.get("QUERY_TYPE", "Unknown") or "Unknown").upper(),
            "custom_sender_name": sender_name,
            "custom_subject": lead_data.get("SUBJECT", ""),
            "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
            "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
            "custom_sender_city": lead_data.get("SENDER_CITY", ""),
            "custom_sender_state": lead_data.get("SENDER_STATE", ""),
            "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
            "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
            "custom_query_product_name": product_name,
            "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
            "custom_query_mcat_name": mcat_name,
            "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
            "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
        }).insert(ignore_permissions=True)
        
        # Lead response based on status
        if lead_status == "Opportunity":
            opportunity = frappe.get_doc({
                "doctype": "Opportunity",
                "opportunity_from": "Lead",
                "lead": doc.name,
                "party_name": doc.name,
                "status": "Open",
                "contact_email": email,
                "contact_mobile": mobile,
                "opportunity_owner": frappe.session.user,
            }).insert(ignore_permissions=True)
            frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

        elif lead_status == "Converted" and email:
            if not frappe.db.exists("Customer", {"email_id": email}):
                customer = frappe.get_doc({
                    "doctype": "Customer",
                    "customer_name": sender_name,
                    "customer_type": "Individual",
                    "email_id": email,
                    "mobile_no": mobile,
                }).insert(ignore_permissions=True)
                frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

        elif lead_status == "Replied":
            frappe.sendmail(
                recipients=[frappe.session.user],
                subject=f"Lead Replied: {lead_name}",
                message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
            )
            frappe.get_doc({
                "doctype": "Communication",
                "communication_type": "Communication",
                "communication_medium": "Email",
                "subject": f"Lead Replied: {lead_name}",
                "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
                "reference_doctype": "Lead",
                "reference_name": doc.name,
                "sender": frappe.session.user,
                "recipients": frappe.session.user,
            }).insert(ignore_permissions=True)

        elif lead_status == "Interested":
            frappe.get_doc({
                "doctype": "ToDo",
                "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
                "reference_type": "Lead",
                "reference_name": doc.name,
                "owner": frappe.session.user,
                "priority": "Medium",
                "status": "Open",
                "date": add_days(today(), 2),
            }).insert(ignore_permissions=True)

        # Log with detailed information
        log_title = f"Lead created: {unique_query_id}"
        log_message = (
            f"Lead Name: {lead_name}\n"
            f"Status: {lead_status}\n"
            f"Product: {product_name}\n"
            f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
            f"Subject: {lead_data.get('SUBJECT', '')}\n"
            f"MCat Name: {mcat_name}\n"
            f"Email: {email}\n"
            f"Mobile: {mobile}"
        )
        frappe.log_error(log_message, log_title)
        
        return doc

    except Exception as e:
        frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
        return None

@frappe.whitelist()
def update_existing_leads_status():
    """Update existing leads with the new status logic."""
    try:
        leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
        for lead in leads:
            doc = frappe.get_doc("Lead", lead.name)
            call_duration = cint(doc.custom_call_duration)
            subject = doc.custom_subject or ""
            message = doc.custom_query_message or ""
            new_status = "Open"

            if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
                new_status = "Converted"
            elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
                new_status = "Converted"
            elif call_duration > 0:
                new_status = "Opportunity"
            elif "replied" in subject.lower():
                new_status = "Replied"
            elif "interested" in message.lower():
                new_status = "Interested"

            doc.status = new_status
            doc.lead_owner = frappe.session.user
            doc.save(ignore_permissions=True)

            if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
                opportunity = frappe.get_doc({
                    "doctype": "Opportunity",
                    "opportunity_from": "Lead",
                    "lead": doc.name,
                    "party_name": doc.name,
                    "status": "Open",
                    "contact_email": doc.email_id,
                    "contact_mobile": doc.mobile_no,
                    "opportunity_owner": frappe.session.user,
                }).insert(ignore_permissions=True)
                frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

            elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
                customer = frappe.get_doc({
                    "doctype": "Customer",
                    "customer_name": doc.lead_name,
                    "customer_type": "Individual",
                    "email_id": doc.email_id,
                    "mobile_no": doc.mobile_no,
                }).insert(ignore_permissions=True)
                frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

            elif new_status == "Replied":
                frappe.sendmail(
                    recipients=[frappe.session.user],
                    subject=f"Lead Replied: {doc.lead_name}",
                    message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
                )
                frappe.get_doc({
                    "doctype": "Communication",
                    "communication_type": "Communication",
                    "communication_medium": "Email",
                    "subject": f"Lead Replied: {doc.lead_name}",
                    "content": f"Lead marked as Replied. Message: {message}",
                    "reference_doctype": "Lead",
                    "reference_name": doc.name,
                    "sender": frappe.session.user,
                    "recipients": frappe.session.user,
                }).insert(ignore_permissions=True)

            elif new_status == "Interested":
                frappe.get_doc({
                    "doctype": "ToDo",
                    "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
                    "reference_type": "Lead",
                    "reference_name": doc.name,
                    "owner": frappe.session.user,
                    "priority": "Medium",
                    "status": "Open",
                    "date": add_days(today(), 2),
                }).insert(ignore_permissions=True)

        frappe.db.commit()
        frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
        frappe.throw(_(f"Error updating lead statuses: {str(e)}"))

def get_indiamart_leads(query_type=None, from_date=None, to_date=None):
    """Fetch all IndiaMART leads for the frontend, optionally filtered by query_type and date range."""
    try:
        filters = {"source": "India Mart"}
        
        # Apply date filters if provided
        if from_date and to_date:
            try:
                from_date = getdate(from_date)
                to_date = getdate(to_date)
                filters["creation"] = ["between", [from_date, to_date]]
            except ValueError:
                frappe.log_error(f"Invalid date format: from_date={from_date}, to_date={to_date}", "Get IndiaMART Leads Warning")
                # Fallback to a default date range
                from_date = to_date = getdate(today())
                filters["creation"] = ["between", [from_date, to_date]]
        
        # Apply query type filter
        if query_type:
            query_type_map = {
                "Direct Enquiries": "W",
                "Buy-Leads": "B",
                "PNS Calls": "P",
                "Catalog-view Leads": ["V", "BIZ"],  # Updated to include both V and BIZ
                "WhatsApp Enquiries": "WA"
            }
            query_type_value = query_type_map.get(query_type)
            if query_type_value:
                if isinstance(query_type_value, list):
                    filters["custom_query_type"] = ["in", [v.upper() for v in query_type_value]]
                else:
                    filters["custom_query_type"] = query_type_value.upper()

        leads = frappe.get_all("Lead", 
            filters=filters,
            fields=[
                "name", "custom_unique_query_id", "custom_sender_name", 
                "custom_query_product_name", "custom_sender_address", "status", 
                "creation", "mobile_no", "email_id", "custom_query_message", "city",
                "custom_query_type"
            ]
        )
        
        frappe.log_error(f"Filtered leads for query_type '{query_type}': {len(leads)} leads", "IndiaMART Leads Fetch Debug")
        for lead in leads:
            frappe.log_error(f"Lead: {lead['name']}, Query Type: {lead['custom_query_type']}", "IndiaMART Leads Fetch Debug Detail")

        return leads
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
        return []

@frappe.whitelist()
def get_query_type_counts(from_date=None, to_date=None):
    """Return counts of leads by query type for the Query Type Funnel."""
    try:
        filters = {"source": "India Mart"}
        
        if from_date and to_date:
            try:
                from_date = getdate(from_date)
                to_date = getdate(to_date)
                filters["creation"] = ["between", [from_date, to_date]]
            except ValueError:
                frappe.throw(_("Invalid date format for from_date or to_date. Use YYYY-MM-DD."))

        leads = frappe.get_all("Lead", 
            filters=filters,
            fields=["custom_query_type"]
        )

        query_type_counts = {
            "Direct Enquiries": 0,
            "Buy-Leads": 0,
            "PNS Calls": 0,
            "Catalog-view Leads": 0,
            "WhatsApp Enquiries": 0
        }

        for lead in leads:
            query_type = (lead.get("custom_query_type") or "").upper()
            if query_type == "W":
                query_type_counts["Direct Enquiries"] += 1
            elif query_type == "B":
                query_type_counts["Buy-Leads"] += 1
            elif query_type == "P":
                query_type_counts["PNS Calls"] += 1
            elif query_type in ["V", "BIZ"]:
                query_type_counts["Catalog-view Leads"] += 1
            elif query_type == "WA":
                query_type_counts["WhatsApp Enquiries"] += 1

        frappe.log_error(f"Query Type Counts: {query_type_counts}", "IndiaMART Query Type Counts Debug")

        return query_type_counts
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Query Type Counts Error")
        frappe.throw(_("Error fetching query type counts: {0}").format(str(e)))

@frappe.whitelist()
def fix_custom_query_types():
    """Update existing leads to ensure custom_query_type is uppercase."""
    try:
        leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "custom_query_type"])
        for lead in leads:
            if lead.custom_query_type:
                doc = frappe.get_doc("Lead", lead.name)
                doc.custom_query_type = lead.custom_query_type.upper()
                doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(_("Updated custom_query_type to uppercase for all India Mart leads."))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Fix Custom Query Types Error")
        frappe.throw(_("Error fixing custom_query_type: {0}").format(str(e)))

@frappe.whitelist()
def update_lead_status(lead_id, status):
    """Update the status of a lead."""
    try:
        lead = frappe.get_doc("Lead", lead_id)
        lead.status = status
        lead.save(ignore_permissions=True)
        frappe.db.commit()

        if status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": lead.name}):
            opportunity = frappe.get_doc({
                "doctype": "Opportunity",
                "opportunity_from": "Lead",
                "lead": lead.name,
                "party_name": lead.name,
                "status": "Open",
                "contact_email": lead.email_id,
                "contact_mobile": lead.mobile_no,
                "opportunity_owner": frappe.session.user,
            }).insert(ignore_permissions=True)
            frappe.log_error(f"Opportunity created for lead {lead.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

        elif status == "Converted" and lead.email_id and not frappe.db.exists("Customer", {"email_id": lead.email_id}):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": lead.lead_name,
                "customer_type": "Individual",
                "email_id": lead.email_id,
                "mobile_no": lead.mobile_no,
            }).insert(ignore_permissions=True)
            frappe.log_error(f"Customer created for lead {lead.name}: {customer.name}", "IndiaMART Customer Creation")

        elif status == "Replied":
            frappe.sendmail(
                recipients=[frappe.session.user],
                subject=f"Lead Replied: {lead.lead_name}",
                message=f"The lead {lead.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead.custom_query_message or 'No message'}",
            )
            frappe.get_doc({
                "doctype": "Communication",
                "communication_type": "Communication",
                "communication_medium": "Email",
                "subject": f"Lead Replied: {lead.lead_name}",
                "content": f"Lead marked as Replied. Message: {lead.custom_query_message or 'No message'}",
                "reference_doctype": "Lead",
                "reference_name": lead.name,
                "sender": frappe.session.user,
                "recipients": frappe.session.user,
            }).insert(ignore_permissions=True)

        elif status == "Interested":
            frappe.get_doc({
                "doctype": "ToDo",
                "description": f"Follow up with interested lead: {lead.lead_name}\nMessage: {lead.custom_query_message or 'No message'}",
                "reference_type": "Lead",
                "reference_name": lead.name,
                "owner": frappe.session.user,
                "priority": "Medium",
                "status": "Open",
                "date": frappe.utils.add_days(today(), 2),
            }).insert(ignore_permissions=True)

        return {"success": True}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Update Lead Status Error")
        frappe.throw(_("Error updating lead status: {0}").format(str(e)))

def add_lead_hook(doc, method):
    """Hook to run after Lead insertion."""
    frappe.log_error(f"Lead {doc.name} inserted via hook", "Lead Hook")

