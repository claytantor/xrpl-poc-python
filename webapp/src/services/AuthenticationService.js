import jwtdecode from 'jwt-decode';
import moment from 'moment';
import Axios from 'axios';

Axios.defaults.withCredentials = false; 

export const AuthenticationService = {
  getVersion() {
    return AxiosService.get(`/version`);     
  }, 
  getAccessTokenInfo (token, caller = 'default') {

    // console.log('getAccessTokenInfo A:', token);
  
    if(token !== undefined){
      // const token = userInfo.jwt;
  
      // get the decoded payload and header for kid
      const decoded_header = jwtdecode(token, { header: true });
      const decoded_payload = jwtdecode(token);
  
      let expirationMoment = moment(`${decoded_payload.exp}`, 'X');
      let active = moment(`${decoded_payload.exp}`, 'X').isAfter(moment.utc());
      // console.log('getAccessTokenInfo B:', decoded_payload, decoded_header, expirationMoment, active, moment.utc());
  
      return {
        header: decoded_header,
        payload: decoded_payload,
        expirationDate: expirationMoment,
        active: active,
      };
  
    } else {
      return {
        active: false
      };
  
    }
  }
};


