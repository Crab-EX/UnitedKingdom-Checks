import requests

from helpers.api_calls import (
    get_company_from_company_house,
    get_company_person_data_from_company_house
)
from helpers.parsing import parse_name

from models.models import Company,Person

def fetch_company_data(registration_number: str) -> Company:
    """
    Fetch company data from the UK Companies House API and return a Company model instance.
    
    :param registration_number: The registration number of the company.
    :return: An instance of the Company model with the fetched data.
    """
    persons = []

    data = get_company_from_company_house(registration_number)
    address = data.get("registered_office_address", {})

    
    ubos = get_company_person_data_from_company_house("persons-with-significant-control", registration_number)
    if ubos:
        ubos_list = ubos.get("items", [])
        for ubo in ubos_list:
            person = {
                "FirstName": ubo.get('name_elements', {}).get("forename", "").upper(),
                "MiddleNames": ubo.get('name_elements', {}).get("middle_name", "").upper(),
                "LastName": ubo.get('name_elements', {}).get("surname", "").upper(),
                "Nationality": ubo.get("nationality", ""),
                "CountryOfResidence": ubo.get("country_of_residence", ""),
                "DateOfBirth": f"{ubo.get('date_of_birth', {}).get('year', '')}-{ubo.get('date_of_birth', {}).get('month', '')}",
                "Roles": ubo.get("natures_of_control", [])
            }
            persons.append(person)

    directors = get_company_person_data_from_company_house("officers", registration_number)
    if directors:
        directors_list = directors.get("items", [])
        for director in directors_list:
            if director.get("name"):
                first_name, middle_names, last_name = parse_name(director["name"])
            else:
                first_name, middle_names, last_name = "", "", ""
            person = {
                "FirstName": first_name.upper(),
                "MiddleNames": middle_names.upper(),
                "LastName": last_name.upper(),
                "Nationality": director.get("nationality", ""),
                "CountryOfResidence": director.get("country_of_residence", ""),
                "DateOfBirth": f"{director.get('date_of_birth', {}).get('year', '')}-{director.get('date_of_birth', {}).get('month', '')}",
                "Roles": [director.get("officer_role", [])]
            }
            persons.append(person)


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
        Charges=data.get("has_charges", False),
        Persons=persons
    )
    
    return company