from typing import Optional
from vesuvius.model.base import VesuviusModel


class MailingAddress(VesuviusModel):
    id: str
    formatted_address: Optional[str] = None
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    zip_code: str


class Owner(VesuviusModel):
    names: Optional[list[str]] = None
    type: Optional[str] = None
    mailing_address: Optional[MailingAddress] = None


class Features(VesuviusModel):
    architecture_type: Optional[str] = None
    cooling: Optional[bool] = None
    cooling_type: Optional[str] = None
    exterior_type: Optional[str] = None
    floor_count: Optional[int] = None
    garage: Optional[bool] = None
    garage_type: Optional[str] = None
    heating: Optional[bool] = None
    heating_type: Optional[str] = None
    room_count: Optional[int] = None
    unit_count: Optional[int] = None


class TaxAssessment(VesuviusModel):
    year: int
    value: int
    land: int
    improvements: int


class PropertyTaxes(VesuviusModel):
    year: int
    total: int


class HistoryEvent(VesuviusModel):
    event: str
    date: str
    price: int


class Property(VesuviusModel):
    rent_cast_id: str
    formatted_address: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None
    latitude: float
    longitude: float
    property_type: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_footage: Optional[int] = None
    lot_size: Optional[int] = None
    year_built: Optional[int] = None
    assessor_id: Optional[str] = None
    legal_description: Optional[str] = None
    subdivision: Optional[str] = None
    zoning: Optional[str] = None
    last_sale_date: Optional[str] = None
    last_sale_price: Optional[int] = None
    features: Optional[Features] = None
    tax_assessments: Optional[dict[int, TaxAssessment]] = None
    property_taxes: Optional[dict[int, PropertyTaxes]] = None
    history: Optional[dict[str, HistoryEvent]] = None
    owner: Optional[Owner] = None
    owner_occupied: Optional[bool] = None
