from vesuvius.repository.repository import db, Repository
from vesuvius.model.rental import Rental

class RentalRepository(Repository):
    COLLECTION = db["rental"]
    MODEL = Rental
