import PropertyService from "./propertyService";
import RentalService from "./rentalService";


class VersuviusService {
  property: PropertyService;
  rental: RentalService;

  constructor() {
    const baseURL = import.meta.env.VITE_BACKEND_URL;
    this.property = new PropertyService(baseURL);
    this.rental = new RentalService(baseURL);
  }
}

export default new VersuviusService();