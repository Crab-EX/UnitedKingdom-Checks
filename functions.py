import requests

from helpers.api_calls import (
    get_company_from_company_house
)

from models.models import Company

def fetch_company_data(registration_number: str) -> Company:
    """
    Fetch company data from the UK Companies House API and return a Company model instance.
    
    :param registration_number: The registration number of the company.
    :return: An instance of the Company model with the fetched data.
    """
    data = get_company_from_company_house(registration_number)
    
    address = data.get("registered_office_address", {})

    company = Company(
        CompanyName=data.get("company_name"),
        CompanyNumber=data.get("company_number"),
        CompanyStatus=data.get("company_status"),
        CompanyType=data.get("type"),
        RegisteredOfficeAddress1=address.get("address_line_1"),
        RegisteredOfficeAddress2=address.get("address_line_2"),
        RegisteredOfficeLocality=address.get("locality"),
        RegisteredOfficeCountry=address.get("country"),
        RegisteredOfficePostalCode=address.get("postal_code"),
        Sector=data.get("sic_codes", [None]),
        DateOfIncorporation=data.get("date_of_creation"),
        InsolvencyStatus=data.get("has_insolvency_history", False),
        Charges=data.get("has_charges", False)
    )
    
    return company