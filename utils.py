from requests import Session
from vonage import Auth, Vonage
from vonage_application import (ApplicationConfig, ApplicationData,
                                ApplicationUrl, Capabilities, Messages,
                                MessagesWebhooks, Region, Verify,
                                VerifyWebhooks, Voice, VoiceUrl, VoiceWebhooks, Rtc, RtcWebhooks)
from dotenv import load_dotenv
from vonage_numbers import NumberParams, SearchAvailableNumbersFilter, UpdateNumberParams
import os
from typing import Optional
from models import Company, Application
from database import SessionLocal, Session
from fastapi import Depends
from typing import Annotated
# create functions for all the steps in our flow 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = Annotated[Session, Depends(get_db)]

load_dotenv()

api_key = os.getenv("VONAGE_API_KEY")
api_secret = os.getenv("VONAGE_SECRET_KEY")

def find_number( api_key: str | None, api_secret: str | None, country: str = "US") -> Optional[str]:
    print(api_key, api_secret)
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))

    # Step 1: Search for available numbers
    available = client.numbers.search_available_numbers(SearchAvailableNumbersFilter(
        country=country,
        search_pattern=None,  # Add empty search pattern
        size=1,            # Request 1 number
        index=1            # Start from first result
    ))[0][0]

    if not available:
        return None

    return available.msisdn

def buy_number(number: str, country: str = "US", api_key: str | None = None, api_secret: str | None = None):
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))
    buy_status = client.numbers.buy_number(params=NumberParams(country=country, msisdn=number))
    if buy_status.error_code != "0":
        return None
    return number


def create_application(db: db, domain: str, name: str,api_key: str | None = None, api_secret: str | None = None):
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))

    voice = Voice(
    webhooks=VoiceWebhooks(
        answer_url=VoiceUrl(
            address=f'{domain}/answer',
            http_method='POST',
            connect_timeout=500,
            socket_timeout=3000,
        ),
        fallback_answer_url=VoiceUrl(
            address=f'{domain}/fallback',
            http_method='POST',
            connect_timeout=500,
            socket_timeout=3000,
        ),
        event_url=VoiceUrl(
            address=f'{domain}/event',
            http_method='POST',
            connect_timeout=500,
            socket_timeout=3000,
        ),
    ),
    signed_callbacks=True,
    conversations_ttl=8000,
    leg_persistence_time=14,
    region=Region.NA_EAST,
    )

    # Messages application options
    messages = Messages(
        version='v1',
        webhooks=MessagesWebhooks(
        inbound_url=ApplicationUrl(
            address=f'{domain}/inbound', http_method='POST'
        ),
        status_url=ApplicationUrl(
            address=f'{domain}/status', http_method='POST'
        ),
    ),
    authenticate_inbound_media=True,
    )

    # Verify application options
    verify = Verify(
        webhooks=VerifyWebhooks(
            status_url=ApplicationUrl(address=f'{domain}/status', http_method='GET')
        ),
    )

    rtc = Rtc(
        webhooks=RtcWebhooks(
            event_url=ApplicationUrl(address=f'{domain}/event', http_method='POST')
        )
    )


    capabilities = Capabilities(
    voice=voice,
    messages=messages,
    verify=verify,
    rtc=rtc
)

    params = ApplicationConfig(
        name=name,
        capabilities=capabilities,
    )

    # Call the API
    response: ApplicationData = client.application.create_application(params)
    application = Application(name=name, application_id=response.id, private_key=response.keys.private_key)
    db.add(application)
    db.commit()
    return response


    

def link_number_to_application(number: str, application_id: str, country: str = "US", api_key: str | None = None, api_secret: str | None = None):
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))

    response = client.numbers.update_number(params=UpdateNumberParams(country=country,
                                                                       msisdn=number, 
                                                                       app_id=application_id, 
                                                                       mo_http_url=None, 
                                                                       mo_smpp_sytem_type=None, 
                                                                       voice_callback_type=None, 
                                                                       voice_callback_value=None, 
                                                                       voice_status_callback=None,
                                                                       ))
    if response.error_code != "200":
        return None

    return number


from vonage_application import Region

def get_vonage_region(
    country: str = "", 
    state: str = "", 
    zip_code: str = ""
) -> Region:
    """
    Maps a country, state, or ZIP code to a Vonage media region.

    Parameters:
        country (str): 2-letter ISO country code (e.g. 'US', 'IN', 'DE')
        state (str): Region or state (optional, used mainly for US/CA)
        zip_code (str): Postal code (optional, used for US ZIP inference)

    Returns:
        Region: A value from vonage_application.Region
    """

    country = country.upper().strip()
    state = state.upper().strip()
    zip_code = zip_code.strip()

    # United States routing (state + ZIP support)
    if country == "US":
        west_states = {"CA", "WA", "OR", "NV", "AZ", "UT", "CO", "ID", "NM"}
        east_states = {
            "NY", "NJ", "PA", "MA", "FL", "VA", "GA", "NC", "SC", "MD", "CT", "IL", "OH", "MI"
        }

        if state in west_states:
            return Region.NA_WEST
        elif state in east_states:
            return Region.NA_EAST
        elif zip_code:
            first_digit = zip_code[0]
            if first_digit in {"9", "8"}:
                return Region.NA_WEST
            elif first_digit in {"0", "1", "2", "3", "4", "5"}:
                return Region.NA_EAST
        return Region.NA_EAST

    # Canada → use East for now
    if country == "CA":
        return Region.NA_EAST

    # European countries → EU_WEST
    if country in {"GB", "FR", "DE", "NL", "IT", "ES", "SE", "NO", "DK", "PL", "CH", "BE"}:
        return Region.EU_WEST

    # # South Asia (India, Pakistan, Bangladesh)
    # if country in {"IN", "PK", "BD", "LK", "NP"}:
    #     return Region.ASIA_SOUTH

    # # East Asia (Japan, South Korea, China, etc.)
    # if country in {"JP", "KR", "CN", "TW", "HK", "MO"}:
    #     return Region.ASIA_EAST

    # # Australia, New Zealand
    # if country in {"AU", "NZ"}:
    #     return Region.AUSTRALIA

    # Default fallback
    return Region.EU_WEST


def get_list_of_applications():
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))
    applications = client.application.list_applications()
    return applications
    


print(get_list_of_applications())