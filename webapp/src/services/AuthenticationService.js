import jwtdecode from 'jwt-decode';
import moment from 'moment';
import Axios from 'axios';

import {AxiosService} from './AxiosService';
// import {useStore} from "../store";

Axios.defaults.withCredentials = false; 

// export const AuthenticationService = {
//     login(classic_address, private_key){
//       return AxiosService.post(`/auth/access_token`, {classic_address, private_key});
//     },
//     isCachedUser(){
//       let cachedUser = getUser();
//       if (!cachedUser || cachedUser.access_token === undefined || cachedUser.refresh_token === undefined) {
//         return false;
//       } else {
//         return true;
//       }
//     }
// };

export const isBrowser = () => typeof window !== 'undefined';

export const disconnect = () => {
  AxiosService.setUser(null);
  window.localStorage.removeItem('xurlUser');
};

// export const setUser = (user) => {
//   AxiosService.setUser(user);
//   window.localStorage.setItem('xurlUser', JSON.stringify(user));
// };

// export const getUser = () => {
//   if (isBrowser() && window.localStorage.getItem('xurlUser')) {
//     let wallet = JSON.parse(window.localStorage.getItem('xurlUser'));
//     // console.log(wallet);
//     return wallet;
//   } else {
//     // console.log('cant get wallet');
//     return {};
//   }
// };

/*
{ 
  user, 
  password, 
  token 
}
*/
export const getAccessTokenInfo = (token, caller = 'default') => {

  console.log('getAccessTokenInfo A:', token);

  if(token !== undefined){
    // const token = userInfo.jwt;

    // get the decoded payload and header for kid
    const decoded_header = jwtdecode(token, { header: true });
    const decoded_payload = jwtdecode(token);

    let expirationMoment = moment(`${decoded_payload.exp}`, 'X');
    let active = moment(`${decoded_payload.exp}`, 'X').isAfter(moment.utc());
    console.log('getAccessTokenInfo B:', decoded_payload, decoded_header, expirationMoment, active, moment.utc());

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
  
};

// export const getAccessToken = (code, state) => {
//   return Axios.post(`${AxiosService.backendBaseUrl}/auth/access_token`, {
//     env: `${deploymentEnv}`,
//     code: code,
//     state: state,
//   }).then((res) => {
//     setUser(res.data.result);
//     return res;
//   });
// };

// export const refreshToken = () => {
//   console.log('refreshing tokens');

//   if(getUser().refresh_token !== undefined){
//     return Axios.post(`${AxiosService.backendBaseUrl}/auth/refresh_token`, {
//       env: `${deploymentEnv}`,
//       refresh_token: getUser().refresh_token,
//     }).then((res) => {
//       console.log('refresh token response', res);
//       const { access_token, refresh_token } = res.data;
//       setUser({ ...getUser(), access_token, refresh_token });
//       return res;
//     });
//   } else {
//     // remove the user
//     setUser(null);
//   }
// };


