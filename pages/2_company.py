import streamlit as st

from geopy.geocoders import Nominatim

# Disable unsecure warning
import urllib3

from functions import fetch_company_data

from models.models import Company
import polars as pl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.title("Find a company")

registration_number = st.text_input("Enter the company registration number:")

if st.button("Search"):
    if registration_number:
        company = fetch_company_data(registration_number)
        address1 = f"{company.RegisteredOfficeAddress1}, {company.RegisteredOfficeAddress2 or ''}, {company.RegisteredOfficeLocality or ''}, {company.RegisteredOfficeCountry or ''}, {company.RegisteredOfficePostalCode or ''}"
        address2 = f"{company.RegisteredOfficeAddress2 or ''}, {company.RegisteredOfficeLocality or ''}, {company.RegisteredOfficeCountry or ''}, {company.RegisteredOfficePostalCode or ''}"
        
        geolocator = Nominatim(user_agent="crabex_company_locator")
        location = geolocator.geocode(address1)
        if location is None:
            location = geolocator.geocode(address2)
        
        if company:
            df = pl.read_csv("data/SICcodes.csv")
            sectors = df.filter(pl.col("SIC Code").cast(pl.String).str.contains_any(company.Sector))["Description"].to_list()
            sectors_text = ", ".join(sectors) if sectors else "No sectors available."

            st.markdown(f"""
                ## {company.CompanyName}
                * Company Number: {company.CompanyNumber}
                * Company Status: {company.CompanyStatus}
                * Company Type: {company.CompanyType}
                * Sector: {sectors_text}
                * Date of Incorporation: {company.DateOfIncorporation}
                * Insolvency Status: {company.InsolvencyStatus}
                * Charges: {company.Charges}
                * Registered Office Address: {address1}
            """)
            if location:
                st.map(data={"lat": [location.latitude], "lon": [location.longitude]})
        else:
            st.error("Company not found.")
    else:
        st.error("Please enter a registration number.")