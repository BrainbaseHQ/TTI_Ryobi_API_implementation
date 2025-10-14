import requests
import logging
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://l250727-iflmap.hcisbp.us3.hana.ondemand.com/http"

USERNAME = os.getenv("RYOBI_USERNAME")
if not USERNAME:
    raise ValueError("RYOBI_USERNAME is not set")
PASSWORD = os.getenv("RYOBI_PASSWORD")
if not PASSWORD:
    raise ValueError("RYOBI_PASSWORD is not set")

def create_customer(
    secondary_customer_id,
    email,
    first_name,
    last_name,
    country="US",
    brand="RYOBI",
    primary_customer_id="NA",
    nickname=None,
    lat=None,
    lon=None,
    ryobi_terms_consent=True,
    ryobi_terms_doc_date="2020-06-12T00:00:00Z",
    ryobi_privacy_consent=True,
    ryobi_privacy_doc_date="2020-05-21T00:00:00Z",
    reg_source="https://registrations.ryobitools.com/",
    # username="S0027393889",
    # password="J(2H6-.(5di46B="
):
    """
    Create a new customer with the specified details.
    
    Args:
        secondary_customer_id: Customer ID (e.g., "N003000361")
        email: Customer email address
        first_name: Customer first name
        last_name: Customer last name
        country: Country code (e.g., "US")
        brand: Brand name (default: "RYOBI")
        primary_customer_id: Primary customer ID (default: "NA")
        nickname: Display name (defaults to first_name + last_name)
        lat: Latitude coordinate
        lon: Longitude coordinate
        ryobi_terms_consent: Terms of service consent (default: True)
        ryobi_terms_doc_date: Terms document date
        ryobi_privacy_consent: Privacy policy consent (default: True)
        ryobi_privacy_doc_date: Privacy policy document date
        reg_source: Registration source URL
        username: Basic auth username
        password: Basic auth password
    
    Returns:
        dict: Response data if successful
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    endpoint = "/CustomerShippingAddressUpdate"
    
    # Set nickname to first + last if not provided
    if nickname is None:
        nickname = f"{first_name} {last_name}"
    
    # Get current timestamp and generate unique IDs
    current_time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    current_timestamp = int(datetime.utcnow().timestamp() * 1000)
    provider_uid = str(uuid.uuid4()).replace('-', '')
    
    # Build XML payload matching the example structure
    payload = f"""<?xml version='1.0' encoding='UTF-8'?>
<root>
  <data>
    <secondaryCustomerId>{secondary_customer_id}</secondaryCustomerId>
    <primaryCustomerId>{primary_customer_id}</primaryCustomerId>
    <brand>{brand}</brand>
  </data>
  <subscriptions/>
  <preferences>
    <terms>
      <ryobiTermsOfService>
        <isConsentGranted>{str(ryobi_terms_consent).lower()}</isConsentGranted>
        <docDate>{ryobi_terms_doc_date}</docDate>
        <lastConsentModified>{current_time}</lastConsentModified>
        <actionTimestamp>{current_time}</actionTimestamp>
        <tags/>
        <customData/>
        <entitlements/>
      </ryobiTermsOfService>
    </terms>
    <privacy>
      <ryobiPrivacyPolicy>
        <isConsentGranted>{str(ryobi_privacy_consent).lower()}</isConsentGranted>
        <docDate>{ryobi_privacy_doc_date}</docDate>
        <lastConsentModified>{current_time}</lastConsentModified>
        <actionTimestamp>{current_time}</actionTimestamp>
        <tags/>
        <customData/>
        <entitlements/>
      </ryobiPrivacyPolicy>
    </privacy>
  </preferences>
  <emails>
    <verified/>
    <unverified>{email}</unverified>
  </emails>
  <identities>
    <provider>site</provider>
    <providerUID>{provider_uid}</providerUID>
    <allowsLogin>true</allowsLogin>
    <isLoginIdentity>true</isLoginIdentity>
    <isExpiredSession>false</isExpiredSession>
    <lastUpdated>{current_time}</lastUpdated>
    <lastUpdatedTimestamp>{current_timestamp}</lastUpdatedTimestamp>
    <oldestDataUpdated>{current_time}</oldestDataUpdated>
    <oldestDataUpdatedTimestamp>{current_timestamp}</oldestDataUpdatedTimestamp>
    <firstName>{first_name}</firstName>
    <lastName>{last_name}</lastName>
    <nickname>{nickname}</nickname>
    <country>{country}</country>
    <email>{email}</email>
  </identities>
  <isActive>true</isActive>
  <isLockedOut>false</isLockedOut>
  <isRegistered>true</isRegistered>
  <isVerified>false</isVerified>
  <lastLogin>{current_time}</lastLogin>
  {f'''<lastLoginLocation>
    <country>{country}</country>
    <coordinates>
      <lat>{lat}</lat>
      <lon>{lon}</lon>
    </coordinates>
  </lastLoginLocation>''' if lat is not None and lon is not None else ''}
  <lastLoginTimestamp>{current_timestamp}</lastLoginTimestamp>
  <lastUpdated>{current_time}</lastUpdated>
  <lastUpdatedTimestamp>{current_timestamp}</lastUpdatedTimestamp>
  <loginProvider>site</loginProvider>
  <loginIDs>
    <emails>{email}</emails>
    <unverifiedEmails/>
  </loginIDs>
  <rbaPolicy>
    <riskPolicyLocked>false</riskPolicyLocked>
  </rbaPolicy>
  <oldestDataUpdated>{current_time}</oldestDataUpdated>
  <oldestDataUpdatedTimestamp>{current_timestamp}</oldestDataUpdatedTimestamp>
  <registered>{current_time}</registered>
  <regSource>{reg_source}</regSource>
  <socialProviders>site</socialProviders>
  <userInfo>
    <UID>{provider_uid}</UID>
    <isSiteUser>true</isSiteUser>
    <isConnected>true</isConnected>
    <isTempUser>false</isTempUser>
    <isLoggedIn>true</isLoggedIn>
    <loginProvider>site</loginProvider>
    <loginProviderUID>{provider_uid}</loginProviderUID>
    <isSiteUID>true</isSiteUID>
    <identities>
      <provider>site</provider>
      <providerUID>{provider_uid}</providerUID>
      <allowsLogin>true</allowsLogin>
      <isLoginIdentity>true</isLoginIdentity>
      <isExpiredSession>false</isExpiredSession>
      <lastUpdated>{current_time}</lastUpdated>
      <lastUpdatedTimestamp>{current_timestamp}</lastUpdatedTimestamp>
      <oldestDataUpdated>{current_time}</oldestDataUpdated>
      <oldestDataUpdatedTimestamp>{current_timestamp}</oldestDataUpdatedTimestamp>
      <firstName>{first_name}</firstName>
      <lastName>{last_name}</lastName>
      <nickname>{nickname}</nickname>
      <country>{country}</country>
      <email>{email}</email>
    </identities>
    <nickname>{nickname}</nickname>
    <firstName>{first_name}</firstName>
    <lastName>{last_name}</lastName>
    <email>{email}</email>
    <country>{country}</country>
    <capabilities>None</capabilities>
    <providers>site</providers>
    <oldestDataUpdatedTimestamp>{int(current_timestamp/1000)}</oldestDataUpdatedTimestamp>
  </userInfo>
</root>"""
    
    url = f"{BASE_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/xml'
    }
    
    # Set up basic authentication
    auth = (USERNAME, PASSWORD)
    
    logger.info(f"Creating customer with ID: {secondary_customer_id}, email: {email}")
    logger.debug(f"Full XML payload:\n{payload}")
    
    try:
        response = requests.post(url, data=payload, headers=headers, auth=auth)
        
        # Log response details
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        # Raise exception for 4xx/5xx status codes
        response.raise_for_status()
        
        logger.info(f"Successfully created customer: {secondary_customer_id}")
        logger.debug(f"Response body: {response.text[:500]}...")  # Log first 500 chars
        
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.text,
            "message": "Customer created successfully"
        }
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        logger.error(f"Response status: {response.status_code}")
        logger.error(f"Response body: {response.text}")
        return {
            "success": False,
            "status_code": response.status_code,
            "error": str(e),
            "data": response.text,
            "message": f"HTTP error: {response.status_code}"
        }
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error occurred: {e}")
        return {
            "success": False,
            "status_code": None,
            "error": str(e),
            "message": "Failed to connect to the server"
        }
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error occurred: {e}")
        return {
            "success": False,
            "status_code": None,
            "error": str(e),
            "message": "Request timed out"
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return {
            "success": False,
            "status_code": None,
            "error": str(e),
            "message": "Request failed"
        }

def get_customer():
    ...

def register_recall_product_for_customer():
    ...
def log_customer_recall_to_crm():
    ...
def check_serial_number_for_recall():
    ...
def check_model_number_for_recall():
    ...


if __name__ == "__main__":
    result = create_customer(
        secondary_customer_id="N003000361",
        email="matthewkoen@gmail.com",
        first_name="Matthew",
        last_name="Koen"
    )
    
    if result["success"]:
        print(f"Success! Status: {result['status_code']}")
        print(f"Message: {result['message']}")
    else:
        print(f"Failed! Error: {result['message']}")
        if result.get("error"):
            print(f"Details: {result['error']}")