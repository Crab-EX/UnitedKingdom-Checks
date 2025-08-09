import time
from functools import wraps
import streamlit as st

import requests

company_house_base_url = st.secrets["COMPANY_HOUSE_BASE_URL"]
company_house_api_key = st.secrets["COMPANY_HOUSE_API_KEY"]

# Simple rate limiter
def rate_limited(max_calls, period):
    """
    Decorator that limits the number of times a function can be called
    within a specified time period (in seconds).
    """
    calls = 0
    last_reset = time.time()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls, last_reset
            current_time = time.time()
            elapsed = current_time - last_reset

            if elapsed > period:
                calls = 0
                last_reset = current_time

            if calls >= max_calls:
                time.sleep(1)
                calls = 0
                last_reset = current_time
            calls += 1
            # Call the original function and return its result
            return func(*args, **kwargs)

        return wrapper

    return decorator

@rate_limited(1, 1)
def get_company_from_company_house(RegistrationNumber: str) -> dict:

    url = f"{company_house_base_url}/company/{RegistrationNumber}"

    response = requests.get(url, auth=(company_house_api_key, ""), verify=False)
    response.raise_for_status()

    data = response.json()

    return data

@rate_limited(1, 1)
def get_company_from_company_house(RegistrationNumber: str) -> dict:

    url = f"{company_house_base_url}/company/{RegistrationNumber}"

    response = requests.get(url, auth=(company_house_api_key, ""), verify=False)
    response.raise_for_status()

    data = response.json()

    return data

@rate_limited(1, 1)
def get_company_person_data_from_company_house(PersonType: str, RegistrationNumber: str) -> dict:
    """
    Fetches data for either a director or UBO of a specific company.

    Args:
        person_type: One of "officers" or "persons-with-significant-control".
    """
    allowed_types = {"officers", "persons-with-significant-control"}
    if PersonType not in allowed_types:
        raise ValueError(f"person_type must be one of {allowed_types}")

    url = f"{company_house_base_url}/company/{RegistrationNumber}/{PersonType}"

    response = requests.get(url, auth=(company_house_api_key, ""), verify=False)
    response.raise_for_status() 
    
    data = response.json()

    return data