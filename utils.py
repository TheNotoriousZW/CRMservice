from vonage import Auth, Vonage
from dotenv import load_dotenv
from vonage_numbers import NumberParams, SearchAvailableNumbersFilter
import os
from typing import Optional

load_dotenv()

print(os.getenv("VONAGE_API_KEY"), os.getenv("VONAGE_SECRET_KEY"))

# client = Vonage(Auth(api_key=os.getenv("VONAGE_API_KEY"), api_secret=os.getenv("VONAGE_SECRET_KEY")))
# print(client.numbers.list_owned_numbers().count)
# print(client.numbers.search_available_numbers(SearchAvailableNumbersFilter(country="US")))

def assign_number_to_company(company_id: int, number: str, country: str):
    pass

# def find_and_buy_number(company_id: int, country: str = "US") -> Optional[str]:
#     client = Vonage(Auth(api_key=os.getenv("VONAGE_API_KEY"), api_secret=os.getenv("VONAGE_SECRET_KEY")))

#     # Step 1: Search for available numbers
#     results = client.numbers.search_available_numbers(params=SearchAvailableNumbersFilter(country=country))
#     available = results.numbers if hasattr(results, "numbers") else []

#     if not available:
#         print("❌ No available numbers found.")
#         return None

#     selected = available[0]
#     print(f"📞 Found available number: {selected.msisdn}")

#     # Step 2: Buy the number
#     buy_status = client.numbers.buy_number(params=NumberParams(country=country, msisdn=selected.msisdn))

#     if buy_status.error_code != "0":
#         print(f"❌ Error buying number: {buy_status.error_text}")
#         return None

#     # Step 3: Assign to client
#     assign_number_to_client(client_id, selected.msisdn, country)
#     return selected.msisdn





