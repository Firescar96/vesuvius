import axios from "axios";

export default class RentalService {
  baseURL: string;
  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  async getRentals() {
    const {data} = await axios.post(this.baseURL + "/rental/search");
    return data;
  }
}