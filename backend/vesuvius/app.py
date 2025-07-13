from fastapi import FastAPI
from vesuvius.model import Property, Rental
from vesuvius.repository import PropertyRepository, RentalRepository
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
@app.get("/status")
def get_status():
  return True

@app.post("/property/search")
async def get_properties() -> list[Property]:
  return await PropertyRepository.find()


@app.post("/rental/search")
async def get_rentals() -> list[Rental]:
  return await RentalRepository.find()