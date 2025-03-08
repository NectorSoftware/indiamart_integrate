# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import date
# import re
# import json
# import traceback
# import urllib
# from urllib.request import urlopen
# import requests

# @frappe.whitelist()
# def add_source_lead():
# 	if not frappe.db.exists("Lead Source","India Mart"):
# 		doc=frappe.get_doc(dict(
# 			doctype = "Lead Source",
# 			source_name = "India Mart"
# 		)).insert(ignore_permissions=True)
# 		if doc:
# 			frappe.msgprint(_("Lead Source Added For India Mart"))
# 	else:
# 		frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date,to_date):
# 	try:
# 		india_mart_setting = frappe.get_doc("IndiaMart Setting","IndiaMart Setting")
# 		if (not india_mart_setting.url
# 			or not india_mart_setting.mobile
# 			or not india_mart_setting.key):
# 				frappe.throw(
# 					msg=_('URL, Mobile, Key mandatory for Indiamart API Call. Please set them and try again.'),
# 					title=_('Missing Setting Fields')
# 				)
# 		req = get_request_url
# 		res = requests.post(url=req)
# 		if res.text:
# 			count = 0
# 			for row in json.loads(res.text):
# 				if not row.get("Error_Message")==None:
# 					frappe.throw(row["Error_Message"])
# 				else:
# 					doc=add_lead(row["SENDERNAME"],row["SENDEREMAIL"],row["MOB"],row["SUBJECT"],row["QUERY_ID"])
# 					if doc:
# 						count += 1
# 			if not count == 0:
# 				frappe.msgprint(_("{0} Lead Created").format(count))

# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

# def get_request_url(india_mart_setting):
# 	req = str(india_mart_setting.url)+'GLUSR_MOBILE/'+str(india_mart_setting.mobile)+'/GLUSR_MOBILE_KEY/'+str(india_mart_setting.key)+'/Start_Time/'+str(india_mart_setting.from_date)+'/End_Time/'+str(india_mart_setting.to_date)+'/'
# 	return req

# @frappe.whitelist()
# def cron_sync_lead():
# 	try:
# 		sync_india_mart_lead(today(),today())
# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

# @frappe.whitelist()
# def add_lead(lead_data):
# 	try:
# 		if not frappe.db.exists("Lead",{"india_mart_id":lead_data["QUERY_ID"]}):
# 			doc = frappe.get_doc(dict(
# 				doctype="Lead",
# 				lead_name=lead_data["SENDERNAME"],
# 				email_address=lead_data["SENDEREMAIL"],
# 				phone=lead_data["MOB"],
# 				requirement=lead_data["SUBJECT"],
# 				india_mart_id=lead_data["QUERY_ID"],
# 				source="India Mart"           
# 			)).insert(ignore_permissions = True)
# 			return doc
# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback())

# code is running but error  in response
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import date
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc(dict(
#             doctype="Lead Source",
#             source_name="India Mart"
#         )).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_('URL and Key are mandatory for Indiamart API Call. Please set them and try again.'),
#                 title=_('Missing Setting Fields')
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Use GET request instead of POST, as per IndiaMART documentation
#         res = requests.get(url=request_url, timeout=30)
        
#         if res.status_code == 200:
#             response_data = res.json()
#             if isinstance(response_data, dict) and response_data.get("CODE") == "404":
#                 frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Authentication Failed')}"))
#             elif isinstance(response_data, list) or (isinstance(response_data, dict) and response_data.get("data")):
#                 count = 0
#                 # Assuming the response contains a list of leads under 'data' or directly as a list
#                 leads = response_data.get("data", response_data) if isinstance(response_data, dict) else response_data
#                 for row in leads:
#                     if row.get("Error_Message"):
#                         frappe.throw(row["Error_Message"])
#                     else:
#                         doc = add_lead({
#                             "SENDERNAME": row.get("sender_name", ""),
#                             "SENDEREMAIL": row.get("sender_email", ""),
#                             "MOB": row.get("sender_mobile", ""),
#                             "SUBJECT": row.get("query_message", ""),
#                             "QUERY_ID": row.get("query_id", "")
#                         })
#                         if doc:
#                             count += 1
#                 if count > 0:
#                     frappe.msgprint(_("{0} Lead(s) Created").format(count))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart API Connection Error"))
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time for any date range.
#     """
#     base_url = india_mart_setting.url or "https://mapi.indiamart.com/wservice/crm/crmListing/v2/"
    
#     # Ensure the URL ends with a slash if it's not already there
#     if not base_url.endswith('/'):
#         base_url += '/'
    
#     # Format dates according to IndiaMART requirements (DD-MON-YYYY)
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025
    
#     # Construct the URL with query parameters
#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }
    
#     # Build the URL with parameters
#     url = base_url + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, allowing custom date ranges or defaulting to today.
#     """
#     try:
#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         # Sync leads for the specified or default date range
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

# @frappe.whitelist()
# def add_lead(lead_data):
#     try:
#         if not frappe.db.exists("Lead", {"india_mart_id": lead_data["QUERY_ID"]}):
#             doc = frappe.get_doc(dict(
#                 doctype="Lead",
#                 lead_name=lead_data["SENDERNAME"],
#                 email_address=lead_data["SENDEREMAIL"],
#                 phone=lead_data["MOB"],
#                 requirement=lead_data["SUBJECT"],
#                 india_mart_id=lead_data["QUERY_ID"],
#                 source="India Mart"           
#             )).insert(ignore_permissions=True)
#             return doc
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback())
#     return None
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import date
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc(dict(
#             doctype="Lead Source",
#             source_name="India Mart"
#         )).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_('URL and Key are mandatory for Indiamart API Call. Please set them and try again.'),
#                 title=_('Missing Setting Fields')
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Use GET request instead of POST, as per IndiaMART documentation
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log the raw response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             # Handle IndiaMART specific response format
#             if isinstance(response_data, dict):
#                 if response_data.get("CODE") == "404" or (response_data.get("STATUS") == "FAILURE"):
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Authentication Failed')}"))
#                 elif response_data.get("CODE") == "200" and response_data.get("STATUS") == "SUCCESS" and response_data.get("RESPONSE"):
#                     # Extract leads from the RESPONSE array
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead({
#                                 "SENDERNAME": row.get("SENDER_NAME", ""),
#                                 "SENDEREMAIL": row.get("SENDER_EMAIL", ""),
#                                 "MOB": row.get("SENDER_MOBILE", ""),
#                                 "SUBJECT": row.get("QUERY_MESSAGE", "") or row.get("SUBJECT", ""),
#                                 "QUERY_ID": row.get("UNIQUE_QUERY_ID", "")
#                             })
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped."))
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart API Connection Error"))
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time for any date range.
#     """
#     base_url = india_mart_setting.url or "https://mapi.indiamart.com/wservice/crm/crmListing/v2/"
    
#     # Ensure the URL ends with a slash if it's not already there
#     if not base_url.endswith('/'):
#         base_url += '/'
    
#     # Format dates according to IndiaMART requirements (DD-MMM-YYYY)
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025
    
#     # Construct the URL with query parameters
#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }
    
#     # Build the URL with parameters
#     url = base_url + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, allowing custom date ranges or defaulting to today.
#     """
#     try:
#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         # Sync leads for the specified or default date range
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

# @frappe.whitelist()
# def add_lead(lead_data):
#     try:
#         if not frappe.db.exists("Lead", {"india_mart_id": lead_data["QUERY_ID"]}):
#             doc = frappe.get_doc(dict(
#                 doctype="Lead",
#                 lead_name=lead_data["SENDERNAME"],
#                 email_address=lead_data["SENDEREMAIL"],
#                 phone=lead_data["MOB"],
#                 requirement=lead_data["SUBJECT"],
#                 india_mart_id=lead_data["QUERY_ID"],
#                 source="India Mart"           
#             )).insert(ignore_permissions=True)
#             # Log successful creation
#             frappe.log_error(f"Lead created successfully: {lead_data['QUERY_ID']}", "IndiaMART Lead Creation")
#             return doc
#         else:
#             # Log that lead already exists
#             frappe.log_error(f"Lead already exists: {lead_data['QUERY_ID']}", "IndiaMART Lead Duplicate")
#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#     return None
# 

# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import date
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc(dict(
#             doctype="Lead Source",
#             source_name="India Mart"
#         )).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_('URL and Key are mandatory for Indiamart API Call. Please set them and try again.'),
#                 title=_('Missing Setting Fields')
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Use GET request instead of POST, as per IndiaMART documentation
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log the raw response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             # Handle IndiaMART specific response format
#             if isinstance(response_data, dict):
#                 if response_data.get("CODE") == "404" or (response_data.get("STATUS") == "FAILURE"):
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Authentication Failed')}"))
#                 elif response_data.get("CODE") == "200" and response_data.get("STATUS") == "SUCCESS" and response_data.get("RESPONSE"):
#                     # Extract leads from the RESPONSE array
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead({
#                                 "SENDERNAME": row.get("SENDER_NAME", ""),
#                                 "SENDEREMAIL": row.get("SENDER_EMAIL", ""),
#                                 "MOB": row.get("SENDER_MOBILE", ""),
#                                 "SUBJECT": row.get("QUERY_MESSAGE", "") or row.get("SUBJECT", ""),
#                                 "QUERY_ID": row.get("UNIQUE_QUERY_ID", "")
#                             })
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped."))
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart API Connection Error"))
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time for any date range.
#     """
#     # Use the base URL from the settings
#     base_url = india_mart_setting.url.strip()  # Remove any trailing whitespace
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     # Ensure the URL ends with a slash if it's not already there
#     if not base_url.endswith('/'):
#         base_url += '/'

#     # Format dates according to IndiaMART requirements (DD-MMM-YYYY)
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy").replace("-", "-")  # e.g., 24-Feb-2025

#     # Construct the URL with query parameters
#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     # Build the URL with parameters
#     url = base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, allowing custom date ranges or defaulting to today.
#     """
#     try:
#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         # Sync leads for the specified or default date range
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

# @frappe.whitelist()
# def add_lead(lead_data):
#     try:
#         if not frappe.db.exists("Lead", {"india_mart_id": lead_data["QUERY_ID"]}):
#             doc = frappe.get_doc(dict(
#                 doctype="Lead",
#                 lead_name=lead_data["SENDERNAME"],
#                 email_address=lead_data["SENDEREMAIL"],
#                 phone=lead_data["MOB"],
#                 requirement=lead_data["SUBJECT"],
#                 india_mart_id=lead_data["QUERY_ID"],
#                 source="India Mart"           
#             )).insert(ignore_permissions=True)
#             # Log successful creation
#             frappe.log_error(f"Lead created successfully: {lead_data['QUERY_ID']}", "IndiaMART Lead Creation")
#             return doc
#         else:
#             # Log that lead already exists
#             frappe.log_error(f"Lead already exists: {lead_data['QUERY_ID']}", "IndiaMART Lead Duplicate")
#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#     return None
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             # Handle IndiaMART response format
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped."))
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time.
#     """
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     # Format dates as DD-MMM-YYYY per IndiaMART spec
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")  # e.g., 08-Dec-2021
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")      # e.g., 08-Dec-2021

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     url = base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, defaulting to today or using custom dates.
#     """
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document from IndiaMART API response data."""
#     try:
#         if not frappe.db.exists("Lead", {"india_mart_id": lead_data.get("UNIQUE_QUERY_ID")}):
#             # Parse QUERY_TIME to ERPNext-compatible datetime
#             query_time = datetime.strptime(lead_data.get("QUERY_TIME"), "%Y-%m-%d %H:%M:%S") if lead_data.get("QUERY_TIME") else None

#             doc = frappe.get_doc({
#                 "doctype": "Lead",
#                 "lead_name": lead_data.get("SENDER_NAME", "IndiaMART Buyer"),
#                 "email_id": lead_data.get("SENDER_EMAIL", ""),  # Changed to email_id (standard ERPNext field)
#                 "mobile_no": lead_data.get("SENDER_MOBILE", ""),  # Changed to mobile_no (standard ERPNext field)
#                 "company_name": lead_data.get("SENDER_COMPANY", ""),
#                 "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#                 "city": lead_data.get("SENDER_CITY", ""),
#                 "state": lead_data.get("SENDER_STATE", ""),
#                 "pincode": lead_data.get("SENDER_PINCODE", ""),
#                 "country": lead_data.get("SENDER_COUNTRY_ISO", ""),
#                 "source": "India Mart",
#                 # Custom fields
#                 "india_mart_id": lead_data.get("UNIQUE_QUERY_ID", ""),
#                 "query_type": lead_data.get("QUERY_TYPE", ""),
#                 "query_time": query_time,
#                 "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#                 "query_message": lead_data.get("QUERY_MESSAGE", ""),
#                 "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#                 "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#                 "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#             }).insert(ignore_permissions=True)
            
#             frappe.log_error(f"Lead created successfully: {lead_data.get('UNIQUE_QUERY_ID')}", "IndiaMART Lead Creation")
#             return doc
#         else:
#             frappe.log_error(f"Lead already exists: {lead_data.get('UNIQUE_QUERY_ID')}", "IndiaMART Lead Duplicate")
#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#     return None
# working code  only email duplicate issue
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             # Handle IndiaMART response format
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped."))
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time.
#     """
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     # Format dates as DD-MMM-YYYY per IndiaMART spec
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")  # e.g., 08-Dec-2021
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")      # e.g., 08-Dec-2021

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     url = base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, defaulting to today or using custom dates.
#     """
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     # Basic mapping for common codes; extend as needed
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#         # Add more mappings if other country codes appear in your data
#     }
    
#     # Check if the ISO code exists in the mapping
#     country_name = country_map.get(iso_code)
    
#     # If not in mapping, check ERPNext Country Doctype
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
    
#     # If still not found, check by name directly or log a warning
#     if not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = None  # Let ERPNext handle it as blank or trigger validation
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document from IndiaMART API response data."""
#     try:
#         if not frappe.db.exists("Lead", {"india_mart_id": lead_data.get("UNIQUE_QUERY_ID")}):
#             # Parse QUERY_TIME to ERPNext-compatible datetime
#             query_time = datetime.strptime(lead_data.get("QUERY_TIME"), "%Y-%m-%d %H:%M:%S") if lead_data.get("QUERY_TIME") else None
            
#             # Map ISO country code to full name
#             country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#             doc = frappe.get_doc({
#                 "doctype": "Lead",
#                 "lead_name": lead_data.get("SENDER_NAME", "IndiaMART Buyer"),
#                 "email_id": lead_data.get("SENDER_EMAIL", ""),
#                 "mobile_no": lead_data.get("SENDER_MOBILE", ""),
#                 "company_name": lead_data.get("SENDER_COMPANY", ""),
#                 "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#                 "city": lead_data.get("SENDER_CITY", ""),
#                 "state": lead_data.get("SENDER_STATE", ""),
#                 "pincode": lead_data.get("SENDER_PINCODE", ""),
#                 "country": country_name,  # Use mapped country name
#                 "source": "India Mart",
#                 # Custom fields
#                 "india_mart_id": lead_data.get("UNIQUE_QUERY_ID", ""),
#                 "query_type": lead_data.get("QUERY_TYPE", ""),
#                 "query_time": query_time,
#                 "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#                 "query_message": lead_data.get("QUERY_MESSAGE", ""),
#                 "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#                 "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#                 "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#             }).insert(ignore_permissions=True)
            
#             frappe.log_error(f"Lead created successfully: {lead_data.get('UNIQUE_QUERY_ID')}", "IndiaMART Lead Creation")
#             return doc
#         else:
#             frappe.log_error(f"Lead already exists: {lead_data.get('UNIQUE_QUERY_ID')}", "IndiaMART Lead Duplicate")
#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#     return None
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import date
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Ensure 'India Mart' lead source exists."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """Fetch leads from IndiaMART API and create/update in ERPNext."""
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(_("URL and Key are mandatory for Indiamart API Call. Please set them and try again."),
#                          title=_("Missing Setting Fields"))

#         # Default to today if no dates provided
#         from_date = getdate(from_date or today())
#         to_date = getdate(to_date or today())

#         if from_date > to_date:
#             frappe.throw(_("From Date cannot be greater than To Date."))
#         if date_diff(to_date, from_date) > 7:
#             frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))

#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make API request
#         res = requests.get(url=request_url, timeout=30)
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")

#         if res.status_code == 200:
#             response_data = res.json()
            
#             if response_data.get("CODE") == "404" or response_data.get("STATUS") == "FAILURE":
#                 frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Authentication Failed')}"))

#             if response_data.get("CODE") == "200" and response_data.get("STATUS") == "SUCCESS" and response_data.get("RESPONSE"):
#                 leads = response_data.get("RESPONSE", [])
#                 if not leads:
#                     frappe.msgprint(_("No new leads found for the selected date range."))
#                     return
                
#                 count = 0
#                 for row in leads:
#                     if row.get("UNIQUE_QUERY_ID"):
#                         doc = add_lead({
#                             "SENDERNAME": row.get("SENDER_NAME", ""),
#                             "SENDEREMAIL": row.get("SENDER_EMAIL", ""),
#                             "MOB": row.get("SENDER_MOBILE", ""),
#                             "SUBJECT": row.get("QUERY_MESSAGE", "") or row.get("SUBJECT", ""),
#                             "QUERY_ID": row.get("UNIQUE_QUERY_ID", "")
#                         })
#                         if doc:
#                             count += 1

#                 frappe.msgprint(_("{0} Lead(s) Created/Updated").format(count))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), _("IndiaMART API Connection Error"))
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("IndiaMART Sync Error"))
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct IndiaMART API URL with dynamic dates."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy").replace("-", "-")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy").replace("-", "-")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job to sync IndiaMART leads."""
#     try:
#         from_date = from_date or today()
#         to_date = to_date or today()
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("IndiaMART Sync Error"))

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create or update a lead from IndiaMART data."""
#     try:
#         existing_lead = frappe.db.exists("Lead", {"india_mart_id": lead_data["QUERY_ID"]})

#         if existing_lead:
#             frappe.log_error(f"Lead already exists: {lead_data['QUERY_ID']}", "IndiaMART Lead Duplicate")
#             return None

#         existing_lead_by_email = frappe.get_all("Lead", filters={"email_address": lead_data["SENDEREMAIL"]}, fields=["name"])

#         if existing_lead_by_email:
#             lead_name = existing_lead_by_email[0]["name"]
#             lead_doc = frappe.get_doc("Lead", lead_name)
#             lead_doc.requirement = lead_data["SUBJECT"]  # Update existing lead's message
#             lead_doc.append("custom_queries", {  # Track multiple queries from same sender
#                 "query_id": lead_data["QUERY_ID"],
#                 "query_message": lead_data["SUBJECT"]
#             })
#             lead_doc.save(ignore_permissions=True)
#             frappe.log_error(f"Lead updated: {lead_doc.name}", "IndiaMART Lead Update")
#             return lead_doc

#         # Create a new lead
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_data["SENDERNAME"],
#             "email_address": lead_data["SENDEREMAIL"],
#             "phone": lead_data["MOB"],
#             "requirement": lead_data["SUBJECT"],
#             "india_mart_id": lead_data["QUERY_ID"],
#             "source": "India Mart"
#         }).insert(ignore_permissions=True)

#         frappe.log_error(f"Lead created successfully: {lead_data['QUERY_ID']}", "IndiaMART Lead Creation")
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating/updating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Error")
#     return None
#         
# 
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Ensure 'India Mart' lead source exists."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """Fetch leads from IndiaMART API and create/update in ERPNext."""
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                          title=_("Missing Setting Fields"))

#         # Default to today if no dates provided
#         from_date = getdate(from_date or today())
#         to_date = getdate(to_date or today())

#         if from_date > to_date:
#             frappe.throw(_("From Date cannot be greater than To Date."))
#         if date_diff(to_date, from_date) > 7:
#             frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))

#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make API request
#         res = requests.get(url=request_url, timeout=30)
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")

#         if res.status_code == 200:
#             response_data = res.json()
            
#             if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                 frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))

#             if response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS" and response_data.get("RESPONSE"):
#                 leads = response_data.get("RESPONSE", [])
#                 if not leads:
#                     frappe.msgprint(_("No new leads found for the selected date range."))
#                     return
                
#                 count = 0
#                 for row in leads:
#                     if row.get("UNIQUE_QUERY_ID"):
#                         doc = add_lead(row)  # Pass full row instead of remapped dict
#                         if doc:
#                             count += 1

#                 frappe.msgprint(_("{0} Lead(s) Created/Updated").format(count))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "IndiaMART API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "IndiaMART Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct IndiaMART API URL with dynamic dates."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy").replace("-", "-")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy").replace("-", "-")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job to sync IndiaMART leads."""
#     try:
#         from_date = from_date or today()
#         to_date = to_date or today()
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "IndiaMART Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#         # Add more as needed
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"  # Default to India as fallback
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create or update a lead from IndiaMART data."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Error")
#             return None

#         # Check for existing lead by UNIQUE_QUERY_ID
#         existing_lead = frappe.db.exists("Lead", {"india_mart_id": unique_query_id})
#         if existing_lead:
#             frappe.log_error(f"Lead already exists: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Check for existing lead by email
#         sender_email = lead_data.get("SENDER_EMAIL", "")
#         existing_lead_by_email = frappe.get_all("Lead", filters={"email_id": sender_email}, fields=["name"])  # Changed to email_id

#         # Parse QUERY_TIME
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Error")

#         # Map country code to name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#         if existing_lead_by_email:
#             lead_name = existing_lead_by_email[0]["name"]
#             lead_doc = frappe.get_doc("Lead", lead_name)
#             lead_doc.query_message = lead_data.get("QUERY_MESSAGE", "")  # Update message
#             lead_doc.append("custom_queries", {
#                 "query_id": unique_query_id,
#                 "query_message": lead_data.get("QUERY_MESSAGE", "")
#             })
#             lead_doc.save(ignore_permissions=True)
#             frappe.log_error(f"Lead updated: {lead_doc.name}", "IndiaMART Lead Update")
#             return lead_doc

#         # Create new lead
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_data.get("SENDER_NAME", "IndiaMART Buyer"),
#             "email_id": sender_email,  # Changed to email_id
#             "mobile_no": lead_data.get("SENDER_MOBILE", ""),  # Changed to mobile_no
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             # Custom fields
#             "india_mart_id": unique_query_id,
#             "query_type": lead_data.get("QUERY_TYPE", ""),
#             "query_time": query_time,
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", ""),
#             "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#             "query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "mcat_name": lead_data.get("QUERY_MCAT_NAME", "")
#         }).insert(ignore_permissions=True)

#         frappe.log_error(f"Lead created successfully: {unique_query_id}", "IndiaMART Lead Creation")
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating/updating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Error")
#         return None
# 
#Testing 
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads for a specified date range. If no dates are provided, use today.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Use provided dates or default to today if none provided
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL with dynamic dates
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             # Handle IndiaMART response format
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """
#     Construct the IndiaMART API URL with glusr_crm_key, start_time, and end_time.
#     """
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     # Format dates as DD-MMM-YYYY per IndiaMART spec
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     url = base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
#     return url

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads dynamically via cron, defaulting to today or using custom dates.
#     """
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"  # Default to India as a fallback
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document from IndiaMART API response data, allowing duplicates on email/mobile."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         # Only check for duplicate by UNIQUE_QUERY_ID
#         if frappe.db.exists("Lead", {"india_mart_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with india_mart_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse QUERY_TIME to ERPNext-compatible datetime
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Map ISO country code to full name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#         # Generate a unique suffix for lead_name if duplicate email/mobile is a concern
#         sender_name = lead_data.get("SENDER_NAME", "IndiaMART Buyer")
#         email_id = lead_data.get("SENDER_EMAIL", "")
#         mobile_no = lead_data.get("SENDER_MOBILE", "")
        
#         # Check for existing email or mobile and append a suffix if needed
#         suffix = f" (IM-{unique_query_id[-4:]})"  # Use last 4 digits of UNIQUE_QUERY_ID
#         if email_id and frappe.db.exists("Lead", {"email_id": email_id}):
#             sender_name += suffix
#         elif mobile_no and frappe.db.exists("Lead", {"mobile_no": mobile_no}):
#             sender_name += suffix

#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": sender_name,
#             "email_id": email_id,
#             "mobile_no": mobile_no,
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             # Custom fields
#             "india_mart_id": unique_query_id,
#             "query_type": lead_data.get("QUERY_TYPE", ""),
#             "query_time": query_time,
#             "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#             "query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#         }).insert(ignore_permissions=True)
        
#         frappe.log_error(f"Lead created successfully: {unique_query_id}", "IndiaMART Lead Creation")
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# 

# CODE IS COMPLTELY WORKING FINE ONLY PRINTING FULL JSON

# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate, now_datetime
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting to avoid 429 errors.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.indiamart_integration.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document, using custom fields to avoid email/mobile uniqueness issues."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"india_mart_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with india_mart_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#         sender_name = lead_data.get("SENDER_NAME", "IndiaMART Buyer")
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
        
#         # Append suffix to lead_name to ensure uniqueness
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         if email and frappe.db.exists("Lead", {"custom_email": email}):
#             sender_name += suffix
#         elif mobile and frappe.db.exists("Lead", {"custom_mobile": mobile}):
#             sender_name += suffix

#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": sender_name,
#             # Use custom fields instead of email_id and mobile_no to avoid uniqueness constraint
#             "custom_email": email,
#             "custom_mobile": mobile,
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             "india_mart_id": unique_query_id,
#             "query_type": lead_data.get("QUERY_TYPE", ""),
#             "query_time": query_time,
#             "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#             "query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#         }).insert(ignore_permissions=True)
        
#         frappe.log_error(f"Lead created successfully: {unique_query_id}", "IndiaMART Lead Creation")
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# GPT CODE FOR PRINTING ROWDAT IN JSON FPORMAT
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate, now_datetime
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Ensure 'India Mart' exists as a Lead Source in ERPNext."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         frappe.msgprint(_("Lead Source 'India Mart' added."))
#     else:
#         frappe.msgprint(_("Lead Source 'India Mart' already exists."))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """Fetch leads from IndiaMART API and store them in ERPNext."""
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(_("URL and Key are required for IndiaMART API. Please set them and try again."))

#         # Enforce API rate limit (5-minute gap between requests)
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit reached. Please wait {0} seconds before retrying.").format(time_remaining))

#         # Default to today if no dates provided
#         from_date = getdate(from_date or today())
#         to_date = getdate(to_date or today())

#         # Validate date range (max 7 days)
#         if from_date > to_date:
#             frappe.throw(_("From Date cannot be greater than To Date."))
#         if date_diff(to_date, from_date) > 7:
#             frappe.throw(_("Date range cannot exceed 7 days per IndiaMART API limits."))

#         # Prepare API request
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
#         res = requests.get(url=request_url, timeout=30)

#         # Ensure response_data is initialized
#         response_data = {}

#         # Log raw API response for debugging
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")

#         if res.status_code == 200:
#             try:
#                 response_data = res.json()
#             except json.JSONDecodeError:
#                 frappe.throw(_("Failed to parse IndiaMART API response."))

#             # Log structured response data
#             frappe.log_error(f"Parsed API Response: {json.dumps(response_data, indent=2)}", "IndiaMART API Response")

#             if isinstance(response_data, dict) and response_data.get("STATUS") == "SUCCESS":
#                 leads = response_data.get("RESPONSE", [])
#                 if not leads:
#                     frappe.msgprint(_("No new leads found for the selected date range."))
#                     return

#                 count = 0
#                 for row in leads:
#                     if row.get("UNIQUE_QUERY_ID"):
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1

#                 frappe.msgprint(_("{0} Lead(s) Created").format(count) if count > 0 else _("No new leads created."))

#                 # Update last API call time
#                 india_mart_setting.last_api_call_time = current_time
#                 india_mart_setting.save(ignore_permissions=True)

#             else:
#                 frappe.throw(_("IndiaMART API Error: {0}").format(response_data.get("MESSAGE", "Unknown Error")))

#         else:
#             frappe.throw(_("IndiaMART API Request Failed. Status Code: {0}, Response: {1}").format(res.status_code, res.text))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_("Failed to connect to IndiaMART API: {0}").format(str(e)))

#     except Exception as e:
#         frappe.log_error(f"Error syncing IndiaMART leads: {str(e)}\n{traceback.format_exc()}", "IndiaMART Sync Error")
#         frappe.throw(_("Error syncing IndiaMART leads: {0}").format(str(e)))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct IndiaMART API request URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"
#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return f"{base_url.rstrip('/')}{api_endpoint}?{urllib.parse.urlencode(params)}"

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document from IndiaMART API data."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"india_mart_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with india_mart_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         country_name = lead_data.get("SENDER_COUNTRY_ISO", "IN")  # Default to India
#         sender_name = lead_data.get("SENDER_NAME", "IndiaMART Buyer")
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")

#         # Append suffix if duplicate email/mobile exists
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         if email and frappe.db.exists("Lead", {"custom_email": email}):
#             sender_name += suffix
#         elif mobile and frappe.db.exists("Lead", {"custom_mobile": mobile}):
#             sender_name += suffix

#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": sender_name,
#             "custom_email": email,
#             "custom_mobile": mobile,
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             "india_mart_id": unique_query_id,
#             "query_product_name": lead_data.get("QUERY_PRODUCT_NAME", ""),
#             "query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "gender": lead_data.get("SENDER_GENDER", ""),  # Extracting gender
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#         }).insert(ignore_permissions=True)

#         frappe.log_error(f"Lead created successfully: {unique_query_id}", "IndiaMART Lead Creation")
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{traceback.format_exc()}", "IndiaMART Lead Creation Error")
#         return None

#CODE IS WORKING FULLY CORECT DAE - 27/02/2025
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate, now_datetime
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting to avoid 429 errors.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.indiamart_integration.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document with enhanced details about the lead's purpose."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"india_mart_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with india_mart_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#         sender_name = lead_data.get("SENDER_NAME", "IndiaMART Buyer")
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         product_name = lead_data.get("QUERY_PRODUCT_NAME", "Unknown Product")
#         query_message = lead_data.get("QUERY_MESSAGE", "No message provided")
        
#         # Enhance lead_name with product name for clarity
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"
#         if email and frappe.db.exists("Lead", {"custom_email": email}):
#             lead_name += suffix
#         elif mobile and frappe.db.exists("Lead", {"custom_mobile": mobile}):
#             lead_name += suffix

#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_name,
#             "custom_email": email,
#             "custom_mobile": mobile,
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             "india_mart_id": unique_query_id,
#             "query_type": lead_data.get("QUERY_TYPE", ""),
#             "query_time": query_time,
#             "query_product_name": product_name,
#             "query_message": query_message,
#             "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#         }).insert(ignore_permissions=True)
        
#         # Log with short title and full details in message
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = f"Product: {product_name}\nMessage: {query_message}"
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None
####updaton in code regards with json 
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, nowdate, now_datetime
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting to avoid 429 errors.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.indiamart_integration.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         if row.get("UNIQUE_QUERY_ID"):
#                             doc = add_lead(row)
#                             if doc:
#                                 count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document with enhanced details about the lead's purpose."""
#     try:
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"india_mart_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with india_mart_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", ""))

#         sender_name = lead_data.get("SENDER_NAME", "IndiaMART Buyer")
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         product_name = lead_data.get("QUERY_PRODUCT_NAME", "Unknown Product")
#         query_message = lead_data.get("QUERY_MESSAGE", "No message provided")
        
#         # Enhance lead_name with product name for clarity
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"
#         if email and frappe.db.exists("Lead", {"custom_email": email}):
#             lead_name += suffix
#         elif mobile and frappe.db.exists("Lead", {"custom_mobile": mobile}):
#             lead_name += suffix

#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_name,
#             "custom_email": email,
#             "custom_mobile": mobile,
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "address_line1": lead_data.get("SENDER_ADDRESS", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "pincode": lead_data.get("SENDER_PINCODE", ""),
#             "country": country_name,
#             "source": "India Mart",
#             "india_mart_id": unique_query_id,
#             "query_type": lead_data.get("QUERY_TYPE", ""),
#             "query_time": query_time,
#             "query_product_name": product_name,
#             "query_message": query_message,
#             "mcat_name": lead_data.get("QUERY_MCAT_NAME", ""),
#             "alternate_mobile": lead_data.get("SENDER_MOBILE_ALT", ""),
#             "alternate_email": lead_data.get("SENDER_EMAIL_ALT", "")
#         }).insert(ignore_permissions=True)
        
#         # Log with short title and full details in message
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = f"Product: {product_name}\nMessage: {query_message}"
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None
####new code working fine as well as handling  database correctly 
# issue is that it only fech staus as lead

# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.indiamart_integration.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             frappe.log_error(f"Skipping lead due to missing required fields: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))  # Default to "IN"

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"  # Maps to custom_sender_name
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"  # Maps to custom_query_product_name
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"  # Maps to custom_query_mcat_name
        
#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name += suffix
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name += suffix

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             # Default ERPNext fields
#             "lead_name": lead_name,  # Required
#             "source": "India Mart",  # Likely required
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,  # Assuming same as mobile_no if not separate
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": "Lead",  # Default status
#             "creation": query_time or now_datetime(),  # Use query time or current time
#             "modified": now_datetime(),
#             "owner": frappe.session.user,  # Current user
#             "modified_by": frappe.session.user,
#             "docstatus": 0,  # Draft
#             "idx": 0,
#             # Custom fields from your list
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,  # Required
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,  # Required
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,  # Required
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),  # Can be null
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None
#working fine frtching status  of lead, open , opportunity
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.indiamart_integration.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not row.get("QUERY_MCAT_NAME"):
#                             row["QUERY_MCAT_NAME"] = "Not Specified"
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
#                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Check if the lead is a repeat customer (potential "Converted")
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         # Check if a follow-up call happened (potential "Opportunity")
#         elif call_duration > 0:
#             lead_status = "Opportunity"

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             # Default ERPNext fields
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,  # Dynamically set status
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,  # Ensure lead_owner matches the current user
#             # Custom fields
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # If status is "Opportunity", create an Opportunity document
#         if lead_status == "Opportunity":
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         # If status is "Converted", create a Customer document (if not exists)
#         if lead_status == "Converted" and email:
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             new_status = "Open"

#             # Check if the lead is a repeat customer (potential "Converted")
#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             # Check if a follow-up call happened (potential "Opportunity")
#             elif call_duration > 0:
#                 new_status = "Opportunity"

#             # Update the lead status
#             doc.status = new_status
#             doc.lead_owner = frappe.session.user  # Ensure lead_owner is set
#             doc.save(ignore_permissions=True)

#             # Create Opportunity if applicable
#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             # Create Customer if applicable
#             if new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))
# code is working completely fine- 01 march
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not row.get("QUERY_MCAT_NAME"):
#                             row["QUERY_MCAT_NAME"] = "Not Specified"
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
#                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         subject = lead_data.get("SUBJECT", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Enhanced status logic based on IndiaMART data
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         elif call_duration > 0:
#             lead_status = "Opportunity"
#         elif "replied" in subject.lower():
#             lead_status = "Replied"  # If the subject indicates a reply
#         elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
#             lead_status = "Interested"  # If the message indicates interest

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             # Default ERPNext fields
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,  # Dynamically set status
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,  # Ensure lead_owner matches the current user
#             # Custom fields
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Lead response based on status
#         if lead_status == "Opportunity":
#             # Create an Opportunity document
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif lead_status == "Converted" and email:
#             # Create a Customer document (if not exists)
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif lead_status == "Replied":
#             # Notify the lead owner (e.g., send an email or create a communication record)
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead_name}",
#                 message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#             )
#             # Create a communication record
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_doctype": "Lead",
#                 "reference_name": doc.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif lead_status == "Interested":
#             # Create a ToDo for the lead owner to follow up
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_type": "Lead",
#                 "reference_name": doc.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": add_days(today(), 2),  # Due in 2 days
#             }).insert(ignore_permissions=True)

#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             subject = doc.custom_subject or ""
#             message = doc.custom_query_message or ""
#             new_status = "Open"

#             # Check if the lead is a repeat customer (potential "Converted")
#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             # Check if a follow-up call happened (potential "Opportunity")
#             elif call_duration > 0:
#                 new_status = "Opportunity"
#             elif "replied" in subject.lower():
#                 new_status = "Replied"
#             elif "interested" in message.lower():
#                 new_status = "Interested"

#             # Update the lead status
#             doc.status = new_status
#             doc.lead_owner = frappe.session.user  # Ensure lead_owner is set
#             doc.save(ignore_permissions=True)

#             # Lead response based on status
#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#             elif new_status == "Replied":
#                 frappe.sendmail(
#                     recipients=[frappe.session.user],
#                     subject=f"Lead Replied: {doc.lead_name}",
#                     message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
#                 )
#                 frappe.get_doc({
#                     "doctype": "Communication",
#                     "communication_type": "Communication",
#                     "communication_medium": "Email",
#                     "subject": f"Lead Replied: {doc.lead_name}",
#                     "content": f"Lead marked as Replied. Message: {message}",
#                     "reference_doctype": "Lead",
#                     "reference_name": doc.name,
#                     "sender": frappe.session.user,
#                     "recipients": frappe.session.user,
#                 }).insert(ignore_permissions=True)

#             elif new_status == "Interested":
#                 frappe.get_doc({
#                     "doctype": "ToDo",
#                     "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
#                     "reference_type": "Lead",
#                     "reference_name": doc.name,
#                     "owner": frappe.session.user,
#                     "priority": "Medium",
#                     "status": "Open",
#                     "date": add_days(today(), 2),
#                 }).insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))
# code created for handling UI too
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not row.get("QUERY_MCAT_NAME"):
#                             row["QUERY_MCAT_NAME"] = "Not Specified"
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
#                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         subject = lead_data.get("SUBJECT", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Enhanced status logic based on IndiaMART data
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         elif call_duration > 0:
#             lead_status = "Opportunity"
#         elif "replied" in subject.lower():
#             lead_status = "Replied"  # If the subject indicates a reply
#         elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
#             lead_status = "Interested"  # If the message indicates interest

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             # Default ERPNext fields
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,  # Dynamically set status
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,  # Ensure lead_owner matches the current user
#             # Custom fields
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Lead response based on status
#         if lead_status == "Opportunity":
#             # Create an Opportunity document
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif lead_status == "Converted" and email:
#             # Create a Customer document (if not exists)
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif lead_status == "Replied":
#             # Notify the lead owner (e.g., send an email or create a communication record)
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead_name}",
#                 message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#             )
#             # Create a communication record
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_doctype": "Lead",
#                 "reference_name": doc.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif lead_status == "Interested":
#             # Create a ToDo for the lead owner to follow up
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_type": "Lead",
#                 "reference_name": doc.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": add_days(today(), 2),  # Due in 2 days
#             }).insert(ignore_permissions=True)

#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             subject = doc.custom_subject or ""
#             message = doc.custom_query_message or ""
#             new_status = "Open"

#             # Check if the lead is a repeat customer (potential "Converted")
#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             # Check if a follow-up call happened (potential "Opportunity")
#             elif call_duration > 0:
#                 new_status = "Opportunity"
#             elif "replied" in subject.lower():
#                 new_status = "Replied"
#             elif "interested" in message.lower():
#                 new_status = "Interested"

#             # Update the lead status
#             doc.status = new_status
#             doc.lead_owner = frappe.session.user  # Ensure lead_owner is set
#             doc.save(ignore_permissions=True)

#             # Lead response based on status
#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#             elif new_status == "Replied":
#                 frappe.sendmail(
#                     recipients=[frappe.session.user],
#                     subject=f"Lead Replied: {doc.lead_name}",
#                     message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
#                 )
#                 frappe.get_doc({
#                     "doctype": "Communication",
#                     "communication_type": "Communication",
#                     "communication_medium": "Email",
#                     "subject": f"Lead Replied: {doc.lead_name}",
#                     "content": f"Lead marked as Replied. Message: {message}",
#                     "reference_doctype": "Lead",
#                     "reference_name": doc.name,
#                     "sender": frappe.session.user,
#                     "recipients": frappe.session.user,
#                 }).insert(ignore_permissions=True)

#             elif new_status == "Interested":
#                 frappe.get_doc({
#                     "doctype": "ToDo",
#                     "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
#                     "reference_type": "Lead",
#                     "reference_name": doc.name,
#                     "owner": frappe.session.user,
#                     "priority": "Medium",
#                     "status": "Open",
#                     "date": add_days(today(), 2),
#                 }).insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))

# @frappe.whitelist()
# def get_leads_for_dashboard():
#     """
#     Fetch leads and counts for the Lead Management dashboard.
#     Returns a dictionary with lead counts for the funnel and a list of leads for the table.
#     """
#     try:
#         # Fetch counts for the Sales Funnel Overview
#         funnel_counts = {
#             "New": frappe.db.count("Lead", filters={"status": "Open", "source": "India Mart"}),
#             "Contact": frappe.db.count("Lead", filters={"status": "Replied", "source": "India Mart"}),
#             "Qualified": frappe.db.count("Lead", filters={"status": "Interested", "source": "India Mart"}),
#             "Proposal": frappe.db.count("Lead", filters={"status": "Opportunity", "source": "India Mart"}),
#             # Negotiation, Won, and Lost are mapped to Opportunity statuses
#             "Negotiation": frappe.db.count("Opportunity", filters={"status": "Open", "opportunity_from": "Lead"}),
#             "Won": frappe.db.count("Opportunity", filters={"status": "Converted", "opportunity_from": "Lead"}),
#             "Lost": frappe.db.count("Opportunity", filters={"status": "Lost", "opportunity_from": "Lead"}),
#         }

#         # Fetch leads for the table
#         leads = frappe.get_all(
#             "Lead",
#             fields=[
#                 "lead_name as name",
#                 "custom_query_product_name as product",
#                 "status",
#                 "priority",
#                 "creation as date"
#             ],
#             filters={"source": "India Mart"},
#             order_by="creation desc",
#             limit=50  # Limit to avoid performance issues
#         )

#         # Format the date for display
#         for lead in leads:
#             lead["date"] = format_datetime(lead["date"], "d-MMM-yyyy")

#         return {
#             "funnel_counts": funnel_counts,
#             "leads": leads
#         }

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Fetch Leads for Dashboard Error")
#         frappe.throw(_("Error fetching leads for dashboard: {0}").format(str(e)))
# testing code
# indiamart_integration/indiamart_integration/api.py

# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def get_leads_for_dashboard():
#     """
#     Fetch leads and counts for the Lead Management dashboard.
#     Returns a dictionary with lead counts for the funnel and a list of leads for the table.
#     """
#     try:
#         # Check permissions
#         if not frappe.has_permission("Lead", "read"):
#             frappe.throw(_("You do not have permission to view leads."), frappe.PermissionError)
#         if not frappe.has_permission("Opportunity", "read"):
#             frappe.throw(_("You do not have permission to view opportunities."), frappe.PermissionError)

#         # Fetch counts for the Sales Funnel Overview
#         funnel_counts = {
#             "New": frappe.db.count("Lead", filters={"status": "Open", "source": "India Mart"}),
#             "Contact": frappe.db.count("Lead", filters={"status": "Replied", "source": "India Mart"}),
#             "Qualified": frappe.db.count("Lead", filters={"status": "Interested", "source": "India Mart"}),
#             "Proposal": frappe.db.count("Lead", filters={"status": "Opportunity", "source": "India Mart"}),
#             "Negotiation": frappe.db.count("Opportunity", filters={"status": "Open", "opportunity_from": "Lead"}),
#             "Won": frappe.db.count("Opportunity", filters={"status": "Converted", "opportunity_from": "Lead"}),
#             "Lost": frappe.db.count("Opportunity", filters={"status": "Lost", "opportunity_from": "Lead"}),
#         }

#         # Fetch leads for the table
#         leads = frappe.get_all(
#             "Lead",
#             fields=[
#                 "lead_name as name",
#                 "custom_query_product_name as product",
#                 "status",
#                 "priority",
#                 "creation as date"
#             ],
#             filters={"source": "India Mart"},
#             order_by="creation desc",
#             limit=50  # Limit to avoid performance issues
#         )

#         # Format the date for display
#         for lead in leads:
#             lead["date"] = format_datetime(lead["date"], "d-MMM-yyyy") if lead["date"] else ""

#         return {
#             "funnel_counts": funnel_counts,
#             "leads": leads
#         }

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Fetch Leads for Dashboard Error")
#         frappe.throw(_("Error fetching leads for dashboard: {0}").format(str(e)))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not row.get("QUERY_MCAT_NAME"):
#                             row["QUERY_MCAT_NAME"] = "Not Specified"
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
#                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         subject = lead_data.get("SUBJECT", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Enhanced status logic based on IndiaMART data
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         elif call_duration > 0:
#             lead_status = "Opportunity"
#         elif "replied" in subject.lower():
#             lead_status = "Replied"
#         elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
#             lead_status = "Interested"

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             # Default ERPNext fields
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,
#             # Custom fields
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Lead response based on status
#         if lead_status == "Opportunity":
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif lead_status == "Converted" and email:
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif lead_status == "Replied":
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead_name}",
#                 message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#             )
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_doctype": "Lead",
#                 "reference_name": doc.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif lead_status == "Interested":
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_type": "Lead",
#                 "reference_name": doc.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": add_days(today(), 2),
#             }).insert(ignore_permissions=True)

#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             subject = doc.custom_subject or ""
#             message = doc.custom_query_message or ""
#             new_status = "Open"

#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             elif call_duration > 0:
#                 new_status = "Opportunity"
#             elif "replied" in subject.lower():
#                 new_status = "Replied"
#             elif "interested" in message.lower():
#                 new_status = "Interested"

#             doc.status = new_status
#             doc.lead_owner = frappe.session.user
#             doc.save(ignore_permissions=True)

#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#             elif new_status == "Replied":
#                 frappe.sendmail(
#                     recipients=[frappe.session.user],
#                     subject=f"Lead Replied: {doc.lead_name}",
#                     message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
#                 )
#                 frappe.get_doc({
#                     "doctype": "Communication",
#                     "communication_type": "Communication",
#                     "communication_medium": "Email",
#                     "subject": f"Lead Replied: {doc.lead_name}",
#                     "content": f"Lead marked as Replied. Message: {message}",
#                     "reference_doctype": "Lead",
#                     "reference_name": doc.name,
#                     "sender": frappe.session.user,
#                     "recipients": frappe.session.user,
#                 }).insert(ignore_permissions=True)

#             elif new_status == "Interested":
#                 frappe.get_doc({
#                     "doctype": "ToDo",
#                     "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
#                     "reference_type": "Lead",
#                     "reference_name": doc.name,
#                     "owner": frappe.session.user,
#                     "priority": "Medium",
#                     "status": "Open",
#                     "date": add_days(today(), 2),
#                 }).insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None, **kwargs):
#     """
#     Sync IndiaMART leads with rate limiting and validation.
#     """
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Make GET request
#         res = requests.get(url=request_url, timeout=30)
        
#         # Log raw response
#         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
#         if res.status_code == 200:
#             response_data = res.json()
            
#             if isinstance(response_data, dict):
#                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401, 429]:
#                     if response_data.get("CODE") == 429:
#                         frappe.log_error("Rate limit hit, scheduling retry in 5 minutes", "IndiaMART API Rate Limit")
#                         frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
#                                      queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=300)
#                         frappe.msgprint(_("Rate limit exceeded. Retrying in 5 minutes."))
#                         return
#                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
#                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
#                     leads = response_data.get("RESPONSE", [])
#                     if not leads:
#                         frappe.msgprint(_("No new leads found for the selected date range."))
#                         return
                    
#                     count = 0
#                     for row in leads:
#                         # Validate required fields before processing
#                         if not row.get("QUERY_MCAT_NAME"):
#                             row["QUERY_MCAT_NAME"] = "Not Specified"
#                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
#                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
#                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
#                             continue
#                         doc = add_lead(row)
#                         if doc:
#                             count += 1
#                     if count > 0:
#                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
#                     else:
#                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
#                     # Update last API call time
#                     india_mart_setting.last_api_call_time = current_time
#                     india_mart_setting.save(ignore_permissions=True)
#                 else:
#                     frappe.throw(_("Invalid response format from IndiaMART API"))
#             else:
#                 frappe.throw(_("Invalid response format from IndiaMART API"))
#         else:
#             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

#     except requests.RequestException as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
#         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         subject = lead_data.get("SUBJECT", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Enhanced status logic based on IndiaMART data
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         elif call_duration > 0:
#             lead_status = "Opportunity"
#         elif "replied" in subject.lower():
#             lead_status = "Replied"  # If the subject indicates a reply
#         elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
#             lead_status = "Interested"  # If the message indicates interest

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": lead_data.get("QUERY_TYPE", ""),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Lead response based on status
#         if lead_status == "Opportunity":
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif lead_status == "Converted" and email:
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif lead_status == "Replied":
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead_name}",
#                 message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#             )
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_doctype": "Lead",
#                 "reference_name": doc.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif lead_status == "Interested":
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_type": "Lead",
#                 "reference_name": doc.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": add_days(today(), 2),
#             }).insert(ignore_permissions=True)

#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             subject = doc.custom_subject or ""
#             message = doc.custom_query_message or ""
#             new_status = "Open"

#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             elif call_duration > 0:
#                 new_status = "Opportunity"
#             elif "replied" in subject.lower():
#                 new_status = "Replied"
#             elif "interested" in message.lower():
#                 new_status = "Interested"

#             doc.status = new_status
#             doc.lead_owner = frappe.session.user
#             doc.save(ignore_permissions=True)

#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#             elif new_status == "Replied":
#                 frappe.sendmail(
#                     recipients=[frappe.session.user],
#                     subject=f"Lead Replied: {doc.lead_name}",
#                     message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
#                 )
#                 frappe.get_doc({
#                     "doctype": "Communication",
#                     "communication_type": "Communication",
#                     "communication_medium": "Email",
#                     "subject": f"Lead Replied: {doc.lead_name}",
#                     "content": f"Lead marked as Replied. Message: {message}",
#                     "reference_doctype": "Lead",
#                     "reference_name": doc.name,
#                     "sender": frappe.session.user,
#                     "recipients": frappe.session.user,
#                 }).insert(ignore_permissions=True)

#             elif new_status == "Interested":
#                 frappe.get_doc({
#                     "doctype": "ToDo",
#                     "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
#                     "reference_type": "Lead",
#                     "reference_name": doc.name,
#                     "owner": frappe.session.user,
#                     "priority": "Medium",
#                     "status": "Open",
#                     "date": add_days(today(), 2),
#                 }).insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))

# # @frappe.whitelist()
# # def get_indiamart_leads():
# #     """Fetch all IndiaMART leads for the frontend."""
# #     try:
# #         leads = frappe.get_all("Lead", 
# #             filters={"source": "India Mart"},
# #             fields=[
# #                 "name", "custom_unique_query_id", "custom_sender_name", 
# #                 "custom_query_product_name", "custom_sender_address", "status", 
# #                 "creation", "mobile_no", "email_id", "custom_query_message", "city"
# #             ]
# #         )
# #         return leads
# #     except Exception as e:
# #         frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
# #         frappe.throw(_("Error fetching leads: {0}").format(str(e)))
# @frappe.whitelist()
# def get_indiamart_leads(query_type=None):
#     """Fetch all IndiaMART leads for the frontend, optionally filtered by query_type."""
#     try:
#         filters = {"source": "India Mart"}
#         if query_type:
#             # Map the frontend query type to the backend custom_query_type values
#             query_type_map = {
#                 "Direct Enquiries": "W",
#                 "Buy-Leads": "B",
#                 "PNS Calls": "P",
#                 "Catalog-view Leads": ["V", "BIZ"],  # Handles multiple values
#                 "WhatsApp Enquiries": "WA"
#             }
#             query_type_value = query_type_map.get(query_type)
#             if query_type_value:
#                 if isinstance(query_type_value, list):
#                     filters["custom_query_type"] = ["in", query_type_value]
#                 else:
#                     filters["custom_query_type"] = query_type_value

#         leads = frappe.get_all("Lead", 
#             filters=filters,
#             fields=[
#                 "name", "custom_unique_query_id", "custom_sender_name", 
#                 "custom_query_product_name", "custom_sender_address", "status", 
#                 "creation", "mobile_no", "email_id", "custom_query_message", "city",
#                 "custom_query_type"  # Include custom_query_type in the fields
#             ]
#         )
#         return leads
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
#         frappe.throw(_("Error fetching leads: {0}").format(str(e)))

# @frappe.whitelist()
# def update_lead_status(lead_id, status):
#     """Update the status of a lead."""
#     try:
#         lead = frappe.get_doc("Lead", lead_id)
#         lead.status = status
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()

#         if status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": lead.name}):
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": lead.name,
#                 "party_name": lead.name,
#                 "status": "Open",
#                 "contact_email": lead.email_id,
#                 "contact_mobile": lead.mobile_no,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {lead.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif status == "Converted" and lead.email_id and not frappe.db.exists("Customer", {"email_id": lead.email_id}):
#             customer = frappe.get_doc({
#                 "doctype": "Customer",
#                 "customer_name": lead.lead_name,
#                 "customer_type": "Individual",
#                 "email_id": lead.email_id,
#                 "mobile_no": lead.mobile_no,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Customer created for lead {lead.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif status == "Replied":
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead.lead_name}",
#                 message=f"The lead {lead.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead.custom_query_message or 'No message'}",
#             )
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead.lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead.custom_query_message or 'No message'}",
#                 "reference_doctype": "Lead",
#                 "reference_name": lead.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif status == "Interested":
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead.lead_name}\nMessage: {lead.custom_query_message or 'No message'}",
#                 "reference_type": "Lead",
#                 "reference_name": lead.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": frappe.utils.add_days(today(), 2),
#             }).insert(ignore_permissions=True)

#         return {"success": True}
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Update Lead Status Error")
#         frappe.throw(_("Error updating lead status: {0}").format(str(e)))

# def add_lead_hook(doc, method):
#     """Hook to run after Lead insertion."""
#     frappe.log_error(f"Lead {doc.name} inserted via hook", "Lead Hook")
# till date code is running fine only ratelimit issue  - 05/03/2025
# from __future__ import unicode_literals
# import frappe
# from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, flt, now_datetime, nowdate
# from frappe import throw, msgprint, _
# from datetime import datetime, timedelta
# import re
# import json
# import traceback
# import requests
# import time
# import urllib

# @frappe.whitelist()
# def add_source_lead():
#     """Add India Mart as a Lead Source if it doesn't exist."""
#     if not frappe.db.exists("Lead Source", "India Mart"):
#         doc = frappe.get_doc({
#             "doctype": "Lead Source",
#             "source_name": "India Mart"
#         }).insert(ignore_permissions=True)
#         if doc:
#             frappe.msgprint(_("Lead Source Added For India Mart"))
#     else:
#         frappe.msgprint(_("India Mart Lead Source Already Available"))

# # @frappe.whitelist()
# # def sync_india_mart_lead(from_date=None, to_date=None, **kwargs):
# #     """
# #     Sync IndiaMART leads with improved rate limiting, retry counter, and validation.
# #     """
# #     try:
# #         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
# #         if not india_mart_setting.url or not india_mart_setting.key:
# #             frappe.throw(
# #                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
# #                 title=_("Missing Setting Fields")
# #             )

# #         # Reset retry_count if last retry was more than 1 hour ago
# #         last_retry_time = india_mart_setting.get("last_retry_time")
# #         current_time = now_datetime()
# #         if last_retry_time and (current_time - last_retry_time) > timedelta(hours=1):
# #             india_mart_setting.retry_count = 0
# #             india_mart_setting.last_retry_time = None
# #             india_mart_setting.save(ignore_permissions=True)

# #         # Check last API call time for rate limiting (IndiaMART allows ~12 requests per minute)
# #         last_call_time = india_mart_setting.get("last_api_call_time")
# #         if last_call_time and (current_time - last_call_time) < timedelta(seconds=5):
# #             time_remaining = (last_call_time + timedelta(seconds=5) - current_time).seconds
# #             frappe.log_error(f"Rate limit: Waiting {time_remaining} seconds before retrying", "IndiaMART API Rate Limit Check")
# #             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

# #         # Use provided dates or default to today
# #         if not from_date or not to_date:
# #             from_date = from_date or today()
# #             to_date = to_date or today()
        
# #         # Validate dates
# #         try:
# #             from_date = getdate(from_date)
# #             to_date = getdate(to_date)
# #             if from_date > to_date:
# #                 frappe.throw(_("From Date cannot be greater than To Date."))
# #             if date_diff(to_date, from_date) > 7:
# #                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
# #         except ValueError:
# #             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

# #         # Prepare the request URL
# #         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
# #         # Update last_api_call_time before making the request
# #         india_mart_setting.last_api_call_time = current_time
# #         india_mart_setting.save(ignore_permissions=True)
        
# #         # Make GET request
# #         res = requests.get(url=request_url, timeout=30)
        
# #         # Log raw response
# #         frappe.log_error(f"Raw API Response: {res.text}", "IndiaMART API Raw Response")
        
# #         if res.status_code == 200:
# #             response_data = res.json()
            
# #             if isinstance(response_data, dict):
# #                 if response_data.get("STATUS") == "FAILURE" or response_data.get("CODE") in ["404", 401]:
# #                     frappe.throw(_(f"IndiaMART API Error: {response_data.get('MESSAGE', 'Unknown Error')}"))
# #                 elif response_data.get("CODE") == 200 and response_data.get("STATUS") == "SUCCESS":
# #                     leads = response_data.get("RESPONSE", [])
# #                     if not leads:
# #                         frappe.msgprint(_("No new leads found for the selected date range."))
# #                         return
                    
# #                     # Log all QUERY_TYPE values to debug
# #                     query_types = [lead.get("QUERY_TYPE", "Not Specified") for lead in leads]
# #                     frappe.log_error(f"Query Types in API Response: {query_types}", "IndiaMART API Query Types Debug")

# #                     count = 0
# #                     for row in leads:
# #                         if not row.get("QUERY_MCAT_NAME"):
# #                             row["QUERY_MCAT_NAME"] = "Not Specified"
# #                         if not (row.get("UNIQUE_QUERY_ID") and row.get("SENDER_NAME") and row.get("QUERY_MCAT_NAME")):
# #                             missing = [k for k in ["UNIQUE_QUERY_ID", "SENDER_NAME", "QUERY_MCAT_NAME"] if not row.get(k)]
# #                             frappe.log_error(f"Skipping lead due to missing required fields {missing}: {row}", "IndiaMART Lead Validation")
# #                             continue
# #                         doc = add_lead(row)
# #                         if doc:
# #                             count += 1
# #                     if count > 0:
# #                         frappe.msgprint(_("{0} Lead(s) Created").format(count))
# #                     else:
# #                         frappe.msgprint(_("No new leads created. Possible duplicates were skipped or handled."))
                    
# #                     # Reset retry count and last retry time on success
# #                     india_mart_setting.retry_count = 0
# #                     india_mart_setting.last_retry_time = None
# #                     india_mart_setting.save(ignore_permissions=True)
# #                 else:
# #                     frappe.throw(_("Invalid response format from IndiaMART API"))
# #             else:
# #                 frappe.throw(_("Invalid response format from IndiaMART API"))
# #         elif res.status_code == 429:
# #             # Handle rate limit exceeded with retry counter
# #             india_mart_setting.retry_count = (india_mart_setting.retry_count or 0) + 1
# #             india_mart_setting.last_retry_time = current_time
# #             if india_mart_setting.retry_count > 3:
# #                 frappe.log_error("Max retries reached for rate limit, stopping retries", "IndiaMART API Rate Limit")
# #                 frappe.msgprint(_("Max retries reached for IndiaMART API rate limit. Please try again later."))
# #                 return
# #             frappe.log_error(f"Rate limit hit (Retry {india_mart_setting.retry_count}/3), scheduling retry in 1 minute", "IndiaMART API Rate Limit")
# #             frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
# #                          queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=60)
# #             frappe.msgprint(_("Rate limit exceeded. A retry has been scheduled in 1 minute."))
# #             india_mart_setting.save(ignore_permissions=True)
# #             return
# #         else:
# #             frappe.throw(_(f"IndiaMART API Request Failed with status code: {res.status_code}, Response: {res.text}"))

# #     except requests.RequestException as e:
# #         frappe.log_error(frappe.get_traceback(), "India Mart API Connection Error")
# #         frappe.throw(_(f"Failed to connect to IndiaMART API: {str(e)}"))
# #     except Exception as e:
# #         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
# #         if "429" in str(e):
# #             india_mart_setting.retry_count = (india_mart_setting.retry_count or 0) + 1
# #             india_mart_setting.last_retry_time = current_time
# #             if india_mart_setting.retry_count > 3:
# #                 frappe.log_error("Max retries reached for rate limit in exception handler, stopping retries", "IndiaMART API Rate Limit")
# #                 frappe.msgprint(_("Max retries reached for IndiaMART API rate limit. Please try again later."))
# #                 return
# #             frappe.log_error(f"Rate limit error caught in exception handler (Retry {india_mart_setting.retry_count}/3), scheduling retry in 1 minute", "IndiaMART API Rate Limit")
# #             frappe.enqueue("indiamart_integration.api.sync_india_mart_lead",
# #                          queue="long", timeout=600, from_date=from_date, to_date=to_date, delay=60)
# #             frappe.msgprint(_("Rate limit exceeded. A retry has been scheduled in 1 minute."))
# #             india_mart_setting.save(ignore_permissions=True)
# #         else:
# #             frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# # def get_request_url(india_mart_setting, from_date, to_date):
# #     """Construct the IndiaMART API URL."""
# #     base_url = india_mart_setting.url.strip()
# #     api_endpoint = "/wservce/crm/crmListing/v2/"

# #     if not base_url.endswith('/'):
# #         base_url += '/'

# #     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
# #     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

# #     params = {
# #         "glusr_crm_key": india_mart_setting.key,
# #         "start_time": formatted_from_date,
# #         "end_time": formatted_to_date
# #     }

# #     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)
# @frappe.whitelist()
# def sync_india_mart_lead(from_date=None, to_date=None, **kwargs):
#     from .__version__ import __version__
#     frappe.log_error("Starting IndiaMART lead sync", "IndiaMART Sync Debug")
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         if not india_mart_setting.url or not india_mart_setting.key:
#             frappe.throw(
#                 msg=_("URL and Key are mandatory for IndiaMART API Call. Please set them and try again."),
#                 title=_("Missing Setting Fields")
#             )

#         # Check last API call time for rate limiting (IndiaMART allows 1 request every 5 minutes)
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
#         if last_call_time and (current_time - last_call_time) < timedelta(minutes=5):
#             time_remaining = (last_call_time + timedelta(minutes=5) - current_time).seconds
#             frappe.log_error(f"Rate limit: Waiting {time_remaining} seconds before retrying", "IndiaMART API Rate Limit Check")
#             frappe.throw(_("API rate limit: Please wait {0} seconds before retrying.").format(time_remaining))

#         # Use provided dates or default to today
#         if not from_date or not to_date:
#             from_date = from_date or today()
#             to_date = to_date or today()
        
#         # Validate dates
#         try:
#             from_date = getdate(from_date)
#             to_date = getdate(to_date)
#             if from_date > to_date:
#                 frappe.throw(_("From Date cannot be greater than To Date."))
#             if date_diff(to_date, from_date) > 7:
#                 frappe.throw(_("Date range cannot exceed 7 days as per IndiaMART API limits."))
#         except ValueError:
#             frappe.throw(_("Invalid date format. Use YYYY-MM-DD or similar."))

#         # Prepare the request URL
#         request_url = get_request_url(india_mart_setting, from_date, to_date)
        
#         # Update last_api_call_time before making the request
#         india_mart_setting.last_api_call_time = current_time
#         india_mart_setting.save(ignore_permissions=True)
#         frappe.log_error(f"Updated last_api_call_time to {india_mart_setting.last_api_call_time}", "IndiaMART Sync Debug")
        
#         # Rest of the function (API call, response handling, etc.)...
#         # ...
        
#         # Reset retry count and last retry time on success
#         india_mart_setting.retry_count = 0
#         india_mart_setting.last_retry_time = None
#         india_mart_setting.save(ignore_permissions=True)

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")
#         frappe.throw(_(f"Error syncing IndiaMART leads: {str(e)}"))

# def get_request_url(india_mart_setting, from_date, to_date):
#     """Construct the IndiaMART API URL."""
#     base_url = india_mart_setting.url.strip()
#     api_endpoint = "/wservce/crm/crmListing/v2/"

#     if not base_url.endswith('/'):
#         base_url += '/'

#     formatted_from_date = format_datetime(from_date, "d-MMM-yyyy")
#     formatted_to_date = format_datetime(to_date, "d-MMM-yyyy")

#     params = {
#         "glusr_crm_key": india_mart_setting.key,
#         "start_time": formatted_from_date,
#         "end_time": formatted_to_date
#     }

#     return base_url + api_endpoint + "?" + urllib.parse.urlencode(params)

# @frappe.whitelist()
# def cron_sync_lead(from_date=None, to_date=None):
#     """Scheduled job with rate limit awareness."""
#     try:
#         india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
#         last_call_time = india_mart_setting.get("last_api_call_time")
#         current_time = now_datetime()
        
#         # Skip if last API call was less than 5 seconds ago
#         if last_call_time and (current_time - last_call_time) < timedelta(seconds=5):
#             frappe.log_error("Cron job skipped due to recent API call", "IndiaMART Cron Rate Limit")
#             return
        
#         # Skip if max retries have been reached
#         if india_mart_setting.retry_count and india_mart_setting.retry_count > 3:
#             frappe.log_error("Cron job skipped due to max retries reached", "IndiaMART Cron Rate Limit")
#             return

#         if not from_date or not to_date:
#             current_date = today()
#             from_date = from_date or current_date
#             to_date = to_date or current_date
        
#         sync_india_mart_lead(from_date, to_date)
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Sync Error")

# def get_country_name(iso_code):
#     """Map ISO country code to ERPNext country name."""
#     country_map = {
#         "IN": "India",
#         "US": "United States",
#         "GB": "United Kingdom",
#     }
    
#     country_name = country_map.get(iso_code)
#     if not country_name and frappe.db.exists("Country", {"code": iso_code}):
#         country_name = frappe.db.get_value("Country", {"code": iso_code}, "name")
#     elif not country_name and frappe.db.exists("Country", iso_code):
#         country_name = iso_code
#     elif not country_name:
#         frappe.log_error(f"Could not find Country: {iso_code}", "IndiaMART Country Mapping")
#         country_name = "India"
    
#     return country_name

# @frappe.whitelist()
# def add_lead(lead_data):
#     """Create a Lead document aligned with customized ERPNext Lead DocType."""
#     try:
#         # Extract required fields with fallbacks
#         unique_query_id = lead_data.get("UNIQUE_QUERY_ID")
#         if not unique_query_id:
#             frappe.log_error("Missing UNIQUE_QUERY_ID in lead data", "IndiaMART Lead Creation Error")
#             return None

#         if frappe.db.exists("Lead", {"custom_unique_query_id": unique_query_id}):
#             frappe.log_error(f"Lead already exists with custom_unique_query_id: {unique_query_id}", "IndiaMART Lead Duplicate")
#             return None

#         # Parse query time
#         query_time = None
#         if lead_data.get("QUERY_TIME"):
#             try:
#                 query_time = datetime.strptime(lead_data["QUERY_TIME"], "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 frappe.log_error(f"Invalid QUERY_TIME format: {lead_data['QUERY_TIME']}", "IndiaMART Lead Creation Error")

#         # Get country name
#         country_name = get_country_name(lead_data.get("SENDER_COUNTRY_ISO", "IN"))

#         # Handle required fields with sensible defaults
#         sender_name = lead_data.get("SENDER_NAME") or "Unknown Buyer"
#         product_name = lead_data.get("QUERY_PRODUCT_NAME") or "Unknown Product"
#         mcat_name = lead_data.get("QUERY_MCAT_NAME") or "Not Specified"
#         email = lead_data.get("SENDER_EMAIL", "")
#         mobile = lead_data.get("SENDER_MOBILE", "")
#         subject = lead_data.get("SUBJECT", "")

#         # Determine lead status dynamically
#         call_duration = cint(lead_data.get("CALL_DURATION", "0"))
#         lead_status = "Open"  # Default status for new leads

#         # Enhanced status logic based on IndiaMART data
#         if email and frappe.db.exists("Customer", {"email_id": email}):
#             lead_status = "Converted"
#         elif mobile and frappe.db.exists("Customer", {"mobile_no": mobile}):
#             lead_status = "Converted"
#         elif call_duration > 0:
#             lead_status = "Opportunity"
#         elif "replied" in subject.lower():
#             lead_status = "Replied"  # If the subject indicates a reply
#         elif "interested" in lead_data.get("QUERY_MESSAGE", "").lower():
#             lead_status = "Interested"  # If the message indicates interest

#         # Construct lead_name (required by ERPNext)
#         suffix = f" (IM-{unique_query_id[-4:]})"
#         lead_name = f"{sender_name} - {product_name}"[:140]  # Truncate to avoid title length issues
#         if email and frappe.db.exists("Lead", {"email_id": email}):
#             lead_name = (lead_name + suffix)[:140]
#         elif mobile and frappe.db.exists("Lead", {"mobile_no": mobile}):
#             lead_name = (lead_name + suffix)[:140]

#         # Log the query type for debugging
#         frappe.log_error(f"Assigning custom_query_type: {lead_data.get('QUERY_TYPE', 'Not Specified')}", "IndiaMART Lead Query Type Debug")

#         # Create Lead document with mapped fields
#         doc = frappe.get_doc({
#             "doctype": "Lead",
#             "lead_name": lead_name,
#             "source": "India Mart",
#             "email_id": email,
#             "mobile_no": mobile,
#             "whatsapp_no": mobile,
#             "phone": lead_data.get("SENDER_PHONE", ""),
#             "company_name": lead_data.get("SENDER_COMPANY", ""),
#             "city": lead_data.get("SENDER_CITY", ""),
#             "state": lead_data.get("SENDER_STATE", ""),
#             "country": country_name,
#             "status": lead_status,
#             "creation": query_time or now_datetime(),
#             "modified": now_datetime(),
#             "owner": frappe.session.user,
#             "modified_by": frappe.session.user,
#             "docstatus": 0,
#             "idx": 0,
#             "lead_owner": frappe.session.user,
#             "custom_call_duration": lead_data.get("CALL_DURATION", "0"),
#             "custom_unique_query_id": unique_query_id,
#             "custom_query_type": (lead_data.get("QUERY_TYPE", "Unknown") or "Unknown").upper(),
#             "custom_sender_name": sender_name,
#             "custom_subject": lead_data.get("SUBJECT", ""),
#             "custom_sender__company": lead_data.get("SENDER_COMPANY", ""),
#             "custom_sender_address": lead_data.get("SENDER_ADDRESS", ""),
#             "custom_sender_city": lead_data.get("SENDER_CITY", ""),
#             "custom_sender_state": lead_data.get("SENDER_STATE", ""),
#             "custom_sender_pincode": lead_data.get("SENDER_PINCODE", ""),
#             "custom_sender_country_iso": lead_data.get("SENDER_COUNTRY_ISO", "IN"),
#             "custom_query_product_name": product_name,
#             "custom_query_message": lead_data.get("QUERY_MESSAGE", ""),
#             "custom_query_mcat_name": mcat_name,
#             "custom_reciever_mobile": lead_data.get("RECEIVER_MOBILE"),
#             "custom_reciever_catalog": lead_data.get("RECEIVER_CATALOG", "")
#         }).insert(ignore_permissions=True)
        
#         # Lead response based on status
#         if lead_status == "Opportunity":
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": doc.name,
#                 "party_name": doc.name,
#                 "status": "Open",
#                 "contact_email": email,
#                 "contact_mobile": mobile,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif lead_status == "Converted" and email:
#             if not frappe.db.exists("Customer", {"email_id": email}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": sender_name,
#                     "customer_type": "Individual",
#                     "email_id": email,
#                     "mobile_no": mobile,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif lead_status == "Replied":
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead_name}",
#                 message=f"The lead {lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#             )
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_doctype": "Lead",
#                 "reference_name": doc.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif lead_status == "Interested":
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead_name}\nMessage: {lead_data.get('QUERY_MESSAGE', 'No message')}",
#                 "reference_type": "Lead",
#                 "reference_name": doc.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": add_days(today(), 2),
#             }).insert(ignore_permissions=True)

#         # Log with detailed information
#         log_title = f"Lead created: {unique_query_id}"
#         log_message = (
#             f"Lead Name: {lead_name}\n"
#             f"Status: {lead_status}\n"
#             f"Product: {product_name}\n"
#             f"Message: {lead_data.get('QUERY_MESSAGE', 'No message')}\n"
#             f"Subject: {lead_data.get('SUBJECT', '')}\n"
#             f"MCat Name: {mcat_name}\n"
#             f"Email: {email}\n"
#             f"Mobile: {mobile}"
#         )
#         frappe.log_error(log_message, log_title)
        
#         return doc

#     except Exception as e:
#         frappe.log_error(f"Error creating lead: {str(e)}\n{frappe.get_traceback()}", "IndiaMART Lead Creation Error")
#         return None

# @frappe.whitelist()
# def update_existing_leads_status():
#     """Update existing leads with the new status logic."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "email_id", "mobile_no", "custom_call_duration", "custom_subject", "custom_query_message"])
#         for lead in leads:
#             doc = frappe.get_doc("Lead", lead.name)
#             call_duration = cint(doc.custom_call_duration)
#             subject = doc.custom_subject or ""
#             message = doc.custom_query_message or ""
#             new_status = "Open"

#             if doc.email_id and frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 new_status = "Converted"
#             elif doc.mobile_no and frappe.db.exists("Customer", {"mobile_no": doc.mobile_no}):
#                 new_status = "Converted"
#             elif call_duration > 0:
#                 new_status = "Opportunity"
#             elif "replied" in subject.lower():
#                 new_status = "Replied"
#             elif "interested" in message.lower():
#                 new_status = "Interested"

#             doc.status = new_status
#             doc.lead_owner = frappe.session.user
#             doc.save(ignore_permissions=True)

#             if new_status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": doc.name}):
#                 opportunity = frappe.get_doc({
#                     "doctype": "Opportunity",
#                     "opportunity_from": "Lead",
#                     "lead": doc.name,
#                     "party_name": doc.name,
#                     "status": "Open",
#                     "contact_email": doc.email_id,
#                     "contact_mobile": doc.mobile_no,
#                     "opportunity_owner": frappe.session.user,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Opportunity created for lead {doc.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#             elif new_status == "Converted" and doc.email_id and not frappe.db.exists("Customer", {"email_id": doc.email_id}):
#                 customer = frappe.get_doc({
#                     "doctype": "Customer",
#                     "customer_name": doc.lead_name,
#                     "customer_type": "Individual",
#                     "email_id": doc.email_id,
#                     "mobile_no": doc.mobile_no,
#                 }).insert(ignore_permissions=True)
#                 frappe.log_error(f"Customer created for lead {doc.name}: {customer.name}", "IndiaMART Customer Creation")

#             elif new_status == "Replied":
#                 frappe.sendmail(
#                     recipients=[frappe.session.user],
#                     subject=f"Lead Replied: {doc.lead_name}",
#                     message=f"The lead {doc.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {message}",
#                 )
#                 frappe.get_doc({
#                     "doctype": "Communication",
#                     "communication_type": "Communication",
#                     "communication_medium": "Email",
#                     "subject": f"Lead Replied: {doc.lead_name}",
#                     "content": f"Lead marked as Replied. Message: {message}",
#                     "reference_doctype": "Lead",
#                     "reference_name": doc.name,
#                     "sender": frappe.session.user,
#                     "recipients": frappe.session.user,
#                 }).insert(ignore_permissions=True)

#             elif new_status == "Interested":
#                 frappe.get_doc({
#                     "doctype": "ToDo",
#                     "description": f"Follow up with interested lead: {doc.lead_name}\nMessage: {message}",
#                     "reference_type": "Lead",
#                     "reference_name": doc.name,
#                     "owner": frappe.session.user,
#                     "priority": "Medium",
#                     "status": "Open",
#                     "date": add_days(today(), 2),
#                 }).insert(ignore_permissions=True)

#         frappe.db.commit()
#         frappe.msgprint(_(f"Updated {len(leads)} leads with new status logic."))

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "India Mart Lead Status Update Error")
#         frappe.throw(_(f"Error updating lead statuses: {str(e)}"))

# # @frappe.whitelist()
# # def get_indiamart_leads(query_type=None, from_date=None, to_date=None):
# #     """Fetch all IndiaMART leads for the frontend, optionally filtered by query_type and date range."""
# #     try:
# #         filters = {"source": "India Mart"}
        
# #         # Apply date filters if provided
# #         if from_date and to_date:
# #             try:
# #                 from_date = getdate(from_date)
# #                 to_date = getdate(to_date)
# #                 filters["creation"] = ["between", [from_date, to_date]]
# #             except ValueError:
# #                 frappe.throw(_("Invalid date format for from_date or to_date. Use YYYY-MM-DD."))
        
# #         # Apply query type filter
# #         if query_type:
# #             query_type_map = {
# #                 "Direct Enquiries": "W",
# #                 "Buy-Leads": "B",
# #                 "PNS Calls": "P",
# #                 "Catalog-view Leads": "BIZ",
# #                 "WhatsApp Enquiries": "WA"
# #             }
# #             query_type_value = query_type_map.get(query_type)
# #             if query_type_value:
# #                 if isinstance(query_type_value, list):
# #                     filters["custom_query_type"] = ["in", [v.upper() for v in query_type_value]]
# #                 else:
# #                     filters["custom_query_type"] = query_type_value.upper()

# #         leads = frappe.get_all("Lead", 
# #             filters=filters,
# #             fields=[
# #                 "name", "custom_unique_query_id", "custom_sender_name", 
# #                 "custom_query_product_name", "custom_sender_address", "status", 
# #                 "creation", "mobile_no", "email_id", "custom_query_message", "city",
# #                 "custom_query_type"
# #             ]
# #         )
        
# #         frappe.log_error(f"Filtered leads for query_type '{query_type}': {len(leads)} leads", "IndiaMART Leads Fetch Debug")
# #         for lead in leads:
# #             frappe.log_error(f"Lead: {lead['name']}, Query Type: {lead['custom_query_type']}", "IndiaMART Leads Fetch Debug Detail")

# #         return leads
# #     except Exception as e:
# #         frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
# #         frappe.throw(_("Error fetching leads: {0}").format(str(e)))
# @frappe.whitelist()
# def get_indiamart_leads(query_type=None, from_date=None, to_date=None):
#     """Fetch all IndiaMART leads for the frontend, optionally filtered by query_type and date range."""
#     try:
#         filters = {"source": "India Mart"}
        
#         # Apply date filters if provided
#         if from_date and to_date:
#             try:
#                 from_date = getdate(from_date)
#                 to_date = getdate(to_date)
#                 filters["creation"] = ["between", [from_date, to_date]]
#             except ValueError:
#                 frappe.log_error(f"Invalid date format: from_date={from_date}, to_date={to_date}", "Get IndiaMART Leads Warning")
#                 # Fallback to a default date range
#                 from_date = to_date = getdate(today())
#                 filters["creation"] = ["between", [from_date, to_date]]
        
#         # Apply query type filter
#         if query_type:
#             query_type_map = {
#                 "Direct Enquiries": "W",
#                 "Buy-Leads": "B",
#                 "PNS Calls": "P",
#                 "Catalog-view Leads": ["V", "BIZ"],  # Updated to include both V and BIZ
#                 "WhatsApp Enquiries": "WA"
#             }
#             query_type_value = query_type_map.get(query_type)
#             if query_type_value:
#                 if isinstance(query_type_value, list):
#                     filters["custom_query_type"] = ["in", [v.upper() for v in query_type_value]]
#                 else:
#                     filters["custom_query_type"] = query_type_value.upper()

#         leads = frappe.get_all("Lead", 
#             filters=filters,
#             fields=[
#                 "name", "custom_unique_query_id", "custom_sender_name", 
#                 "custom_query_product_name", "custom_sender_address", "status", 
#                 "creation", "mobile_no", "email_id", "custom_query_message", "city",
#                 "custom_query_type"
#             ]
#         )
        
#         frappe.log_error(f"Filtered leads for query_type '{query_type}': {len(leads)} leads", "IndiaMART Leads Fetch Debug")
#         for lead in leads:
#             frappe.log_error(f"Lead: {lead['name']}, Query Type: {lead['custom_query_type']}", "IndiaMART Leads Fetch Debug Detail")

#         return leads
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
#         return []

# @frappe.whitelist()
# def get_query_type_counts(from_date=None, to_date=None):
#     """Return counts of leads by query type for the Query Type Funnel."""
#     try:
#         filters = {"source": "India Mart"}
        
#         if from_date and to_date:
#             try:
#                 from_date = getdate(from_date)
#                 to_date = getdate(to_date)
#                 filters["creation"] = ["between", [from_date, to_date]]
#             except ValueError:
#                 frappe.throw(_("Invalid date format for from_date or to_date. Use YYYY-MM-DD."))

#         leads = frappe.get_all("Lead", 
#             filters=filters,
#             fields=["custom_query_type"]
#         )

#         query_type_counts = {
#             "Direct Enquiries": 0,
#             "Buy-Leads": 0,
#             "PNS Calls": 0,
#             "Catalog-view Leads": 0,
#             "WhatsApp Enquiries": 0
#         }

#         for lead in leads:
#             query_type = (lead.get("custom_query_type") or "").upper()
#             if query_type == "W":
#                 query_type_counts["Direct Enquiries"] += 1
#             elif query_type == "B":
#                 query_type_counts["Buy-Leads"] += 1
#             elif query_type == "P":
#                 query_type_counts["PNS Calls"] += 1
#             elif query_type in ["V", "BIZ"]:
#                 query_type_counts["Catalog-view Leads"] += 1
#             elif query_type == "WA":
#                 query_type_counts["WhatsApp Enquiries"] += 1

#         frappe.log_error(f"Query Type Counts: {query_type_counts}", "IndiaMART Query Type Counts Debug")

#         return query_type_counts
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get Query Type Counts Error")
#         frappe.throw(_("Error fetching query type counts: {0}").format(str(e)))
# @frappe.whitelist()
# def get_indiamart_leads(query_type=None, from_date=None, to_date=None):
#     """Fetch all IndiaMART leads for the frontend, optionally filtered by query_type and date range."""
#     try:
#         filters = {"source": "India Mart"}
        
#         # Apply date filters if provided
#         if from_date and to_date:
#             try:
#                 from_date = getdate(from_date)
#                 to_date = getdate(to_date)
#                 filters["creation"] = ["between", [from_date, to_date]]
#             except ValueError:
#                 frappe.log_error(f"Invalid date format: from_date={from_date}, to_date={to_date}", "Get IndiaMART Leads Warning")
#                 # Fallback to a default date range
#                 from_date = to_date = getdate(today())
#                 filters["creation"] = ["between", [from_date, to_date]]
        
#         # Apply query type filter
#         if query_type:
#             query_type_map = {
#                 "Direct Enquiries": "W",
#                 "Buy-Leads": "B",
#                 "PNS Calls": "P",
#                 "Catalog-view Leads": ["V", "BIZ"],  # Updated to include both V and BIZ
#                 "WhatsApp Enquiries": "WA"
#             }
#             query_type_value = query_type_map.get(query_type)
#             if query_type_value:
#                 if isinstance(query_type_value, list):
#                     filters["custom_query_type"] = ["in", [v.upper() for v in query_type_value]]
#                 else:
#                     filters["custom_query_type"] = query_type_value.upper()

#         leads = frappe.get_all("Lead", 
#             filters=filters,
#             fields=[
#                 "name", "custom_unique_query_id", "custom_sender_name", 
#                 "custom_query_product_name", "custom_sender_address", "status", 
#                 "creation", "mobile_no", "email_id", "custom_query_message", "city",
#                 "custom_query_type"
#             ]
#         )
        
#         frappe.log_error(f"Filtered leads for query_type '{query_type}': {len(leads)} leads", "IndiaMART Leads Fetch Debug")
#         for lead in leads:
#             frappe.log_error(f"Lead: {lead['name']}, Query Type: {lead['custom_query_type']}", "IndiaMART Leads Fetch Debug Detail")

#         return leads
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Get IndiaMART Leads Error")
#         return []

# @frappe.whitelist()
# def fix_custom_query_types():
#     """Update existing leads to ensure custom_query_type is uppercase."""
#     try:
#         leads = frappe.get_all("Lead", filters={"source": "India Mart"}, fields=["name", "custom_query_type"])
#         for lead in leads:
#             if lead.custom_query_type:
#                 doc = frappe.get_doc("Lead", lead.name)
#                 doc.custom_query_type = lead.custom_query_type.upper()
#                 doc.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.msgprint(_("Updated custom_query_type to uppercase for all India Mart leads."))
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Fix Custom Query Types Error")
#         frappe.throw(_("Error fixing custom_query_type: {0}").format(str(e)))

# @frappe.whitelist()
# def update_lead_status(lead_id, status):
#     """Update the status of a lead."""
#     try:
#         lead = frappe.get_doc("Lead", lead_id)
#         lead.status = status
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()

#         if status == "Opportunity" and not frappe.db.exists("Opportunity", {"lead": lead.name}):
#             opportunity = frappe.get_doc({
#                 "doctype": "Opportunity",
#                 "opportunity_from": "Lead",
#                 "lead": lead.name,
#                 "party_name": lead.name,
#                 "status": "Open",
#                 "contact_email": lead.email_id,
#                 "contact_mobile": lead.mobile_no,
#                 "opportunity_owner": frappe.session.user,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Opportunity created for lead {lead.name}: {opportunity.name}", "IndiaMART Opportunity Creation")

#         elif status == "Converted" and lead.email_id and not frappe.db.exists("Customer", {"email_id": lead.email_id}):
#             customer = frappe.get_doc({
#                 "doctype": "Customer",
#                 "customer_name": lead.lead_name,
#                 "customer_type": "Individual",
#                 "email_id": lead.email_id,
#                 "mobile_no": lead.mobile_no,
#             }).insert(ignore_permissions=True)
#             frappe.log_error(f"Customer created for lead {lead.name}: {customer.name}", "IndiaMART Customer Creation")

#         elif status == "Replied":
#             frappe.sendmail(
#                 recipients=[frappe.session.user],
#                 subject=f"Lead Replied: {lead.lead_name}",
#                 message=f"The lead {lead.lead_name} has been marked as Replied. Follow up as needed.\n\nMessage: {lead.custom_query_message or 'No message'}",
#             )
#             frappe.get_doc({
#                 "doctype": "Communication",
#                 "communication_type": "Communication",
#                 "communication_medium": "Email",
#                 "subject": f"Lead Replied: {lead.lead_name}",
#                 "content": f"Lead marked as Replied. Message: {lead.custom_query_message or 'No message'}",
#                 "reference_doctype": "Lead",
#                 "reference_name": lead.name,
#                 "sender": frappe.session.user,
#                 "recipients": frappe.session.user,
#             }).insert(ignore_permissions=True)

#         elif status == "Interested":
#             frappe.get_doc({
#                 "doctype": "ToDo",
#                 "description": f"Follow up with interested lead: {lead.lead_name}\nMessage: {lead.custom_query_message or 'No message'}",
#                 "reference_type": "Lead",
#                 "reference_name": lead.name,
#                 "owner": frappe.session.user,
#                 "priority": "Medium",
#                 "status": "Open",
#                 "date": frappe.utils.add_days(today(), 2),
#             }).insert(ignore_permissions=True)

#         return {"success": True}
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Update Lead Status Error")
#         frappe.throw(_("Error updating lead status: {0}").format(str(e)))

# def add_lead_hook(doc, method):
#     """Hook to run after Lead insertion."""
#     frappe.log_error(f"Lead {doc.name} inserted via hook", "Lead Hook")
# be carefull with above codr unning fine only issue is of sync button  06-Mar-2025
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