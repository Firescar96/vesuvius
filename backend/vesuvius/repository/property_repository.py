from vesuvius.repository.repository import db, Repository
from vesuvius.model.property import Property

class PropertyRepository(Repository):
    COLLECTION = db["property"]
    MODEL = Property
