import axios from "axios";

export default class PropertyService {
  baseURL: string;
  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  async getProperties() {
    const {data} =  await axios.post(this.baseURL + "/property/search");
    return data
  }
}