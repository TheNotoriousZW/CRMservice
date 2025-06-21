from requests import Session
from vonage import Auth, Vonage
from dotenv import load_dotenv
from vonage_numbers import NumberParams, SearchAvailableNumbersFilter
import os
from typing import Optional


load_dotenv()

api_key = os.getenv("VONAGE_API_KEY")
api_secret = os.getenv("VONAGE_SECRET_KEY")

def find_number(country: str = "US") -> Optional[str]:
    print(api_key, api_secret)
    client = Vonage(Auth(api_key=api_key, api_secret=api_secret))

    # Step 1: Search for available numbers
    available = client.numbers.search_available_numbers(SearchAvailableNumbersFilter(country=country))[0][0]

    if not available:
        return None

    # Step 2: Buy the number
    buy_status = client.numbers.buy_number(params=NumberParams(country=country, msisdn=available.msisdn))

    if buy_status.error_code != "0":
        return None

    return available.msisdn


print(find_number())


