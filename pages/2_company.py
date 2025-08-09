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

        # Prepare address for geocoding
        address1 = f"{company.RegisteredOfficeAddress1}, {company.RegisteredOfficeAddress2 or ''}, {company.RegisteredOfficeLocality or ''}, {company.RegisteredOfficeCountry or ''}, {company.RegisteredOfficePostalCode or ''}"
        address2 = f"{company.RegisteredOfficeAddress2 or ''}, {company.RegisteredOfficeLocality or ''}, {company.RegisteredOfficeCountry or ''}, {company.RegisteredOfficePostalCode or ''}"
        
        geolocator = Nominatim(user_agent="crabex_company_locator")
        location = geolocator.geocode(address1)
        if location is None:
            location = geolocator.geocode(address2)

        # Transform person to polars dataframe
        df_persons = pl.DataFrame(company.Persons if company.Persons else [])
        merged_df_persons = df_persons.group_by(
            ["FirstName", "LastName", "DateOfBirth"]
        ).agg(
            pl.col("MiddleNames").first().alias("MiddleNames"),
            pl.col("Nationality").first().alias("Nationality"),
            pl.col("CountryOfResidence").first().alias("CountryOfResidence"),
            pl.concat_list("Roles").alias("Roles"),
        )

        if company:
            df_codes = pl.read_csv("data/SICcodes.csv")
            sectors = df_codes.filter(pl.col("SIC Code").cast(pl.String).str.contains_any(company.Sector))["Description"].to_list()
            sectors_text = ", ".join(sectors) if sectors else "No sectors available."

            st.markdown(f"## {company.CompanyName} ({company.CompanyNumber})")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    ### Status
                    * Company Number: {company.CompanyNumber}
                    * Company Status: {company.CompanyStatus}
                    * Insolvency Status: {company.InsolvencyStatus}
                    * Charges: {company.Charges}
                """)
            with col2:
                st.markdown(f"""
                    ### Details
                    * Company Type: {company.CompanyType}
                    * Sector: {sectors_text}
                    * Date of Incorporation: {company.DateOfIncorporation}
                """)
            st.markdown(f"""
                ### Address
                * Registered Office Address: {address1}
            """)
            if location:
                st.map(data={"lat": [location.latitude], "lon": [location.longitude]})
            st.markdown("### Persons")
            if merged_df_persons.is_empty():
                st.write("No persons found.")
            else:
                st.dataframe(merged_df_persons)
        else:
            st.error("Company not found.")
    else:
        st.error("Please enter a registration number.")