# from homeharvest import scrape_property
# from datetime import datetime

# # Generate filename based on current timestamp
# current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"HomeHarvest_{current_timestamp}.csv"

# properties = scrape_property(
#   location="2603 North Richards Street, Milwaukee, WI",  # address, city, state
#   listing_type="sold",  # or (for_sale, for_rent, pending)
#   past_days=30,  # sold in last 30 days - listed in last 30 days if (for_sale, for_rent)

#   # property_type=['single_family','multi_family'],
#   # date_from="2023-05-01", # alternative to past_days
#   # date_to="2023-05-28",
#   # foreclosure=True
#   # mls_only=True,  # only fetch MLS listings
# )
# print(f"Number of properties: {len(properties)}")

# # Export to csv
# properties.to_csv(filename, index=False)
# print(properties.head())

ADDRESS_AUTOCOMPLETE_URL = "https://parser-external.geo.moveaws.com/suggest"
NUM_PROPERTY_WORKERS = 20
DEFAULT_PAGE_SIZE = 200


class ListingType(Enum):
    FOR_SALE = "FOR_SALE"
    FOR_RENT = "FOR_RENT"
    PENDING = "PENDING"
    SOLD = "SOLD"


def handle_location():
    params = {
        "input": '2603 North Richards Street, Milwaukee, WI',
        "client_id": ListingType.SOLD.value.lower().replace("_", "-"),
        "limit": "1",
        "area_types": "city,state,county,postal_code,address,street,neighborhood,school,school_district,university,park",
    }

    response = self.session.get(
        ADDRESS_AUTOCOMPLETE_URL,
        params=params,
    )
    response_json = response.json()

    result = response_json["autocomplete"]

    if not result:
        return None

    return result[0]

handle_location()