import axios from 'axios';
const url = 'https://www.redfin.com/stingray/do/location-autocomplete';

const sendRequest = async () => {
  try {
    // const response = await axios.get(url,{ 
    //   params: {
    //     location: '2603 north richards street',
    //   }
    // });
    const response = await axios.get('https://www.redfin.com/stingray/do/location-autocomplete?location=2603%20north&start=0&count=10&v=2&market=wisconsin&al=2&iss=true&ooa=true&mrs=false&region_id=NaN&region_type=NaN&lat=43.0658442&lng=-87.9081331&includeAddressInfo=false')

    console.log(response.data);
  } catch (error) {
    console.error('Error sending request:', error.response?.data || error.message);
  }
};

sendRequest();