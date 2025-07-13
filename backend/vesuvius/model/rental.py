from typing import Optional
from vesuvius.model.base import VesuviusModel

class HistoryEvent(VesuviusModel):
    event: str
    price: int
    listing_type: str
    listed_date: str
    removed_date: Optional[str] = None
    days_on_market: int


class Rental(VesuviusModel):
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
    bedrooms: int
    bathrooms: float
    status: str
    price: int
    listing_type: Optional[str] = None
    listed_date: Optional[str] = None
    removed_date: Optional[str]
    created_date: str
    last_seen_date: str
    days_on_market: Optional[int] = None
    history: Optional[dict[str, HistoryEvent]] = None
