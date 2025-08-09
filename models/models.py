import json
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, constr, field_validator

class Person(BaseModel):
    FirstName: Optional[str] = None
    MiddleNames: Optional[str] = None
    LastName: str
    Nationality: Optional[str] = None
    CountryOfResidence: Optional[str] = None
    DateOfBirth: Optional[str] = None
    Roles: Optional[List[str]] = None


class Company(BaseModel):
    CompanyName: str
    CompanyNumber: str
    CompanyStatus: Literal["active", "dissolved", "liquidation", "receivership", "voluntary-arrangement"]
    CompanyType: Literal["ltd", "plc", "llp", "ltd-by-guarantee", "other"]
    RegisteredOfficeAddress1: Optional[str] = None
    RegisteredOfficeAddress2: Optional[str] = None
    RegisteredOfficeCountry: Optional[str] = None
    RegisteredOfficeLocality: Optional[str] = None
    RegisteredOfficePostalCode: Optional[str] = None
    Sector: Optional[List[str]] = None
    DateOfIncorporation: Optional[str] = None
    InsolvencyStatus: Optional[bool] = None
    Charges: Optional[bool] = None  
    Persons: Optional[List[Person]] = None