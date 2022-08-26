import jwtdecode from 'jwt-decode';
import moment from 'moment';
import Axios from 'axios';
// import { backendBaseUrl, deploymentEnv } from '../env';
import {AxiosService} from './AxiosService';

Axios.defaults.withCredentials = false; 

export const AuthenticationService = {
    login(classic_address, private_key){
      return AxiosService.post(`/auth/access_token`, {classic_address, private_key});
    },
};

export const isBrowser = () => typeof window !== 'undefined';

export const disconnect = () => {
  AxiosService.setUser(null);
  window.localStorage.removeItem('xurlUser');
};

export const setUser = (user) => {
  AxiosService.setUser(user);
  window.localStorage.setItem('xurlUser', JSON.stringify(user));
};

export const getUser = () => {
  if (isBrowser() && window.localStorage.getItem('xurlUser')) {
    let wallet = JSON.parse(window.localStorage.getItem('xurlUser'));
    // console.log(wallet);
    return wallet;
  } else {
    // console.log('cant get wallet');
    return {};
  }
};

/*
{ user, password, token }
*/
export const getAccessTokenInfo = (userInfo, caller = 'default') => {

  if(userInfo && userInfo.access_token !== undefined){
    const token = userInfo.access_token;

    // get the decoded payload and header for kid
    const decoded_header = jwtdecode(token, { header: true });
    const decoded_payload = jwtdecode(token);

    let expirationMoment = moment(`${decoded_payload.exp}`, 'X');
    let active = moment(`${decoded_payload.exp}`, 'X').isAfter(moment.utc());

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

export const getAccessToken = (code, state) => {
  return Axios.post(`${AxiosService.backendBaseUrl}/auth/access_token`, {
    env: `${deploymentEnv}`,
    code: code,
    state: state,
  }).then((res) => {
    setUser(res.data.result);
    return res;
  });
};

export const refreshToken = () => {
  console.log('refreshing tokens');

  if(getUser().refresh_token !== undefined){
    return Axios.post(`${AxiosService.backendBaseUrl}/auth/refresh_token`, {
      env: `${deploymentEnv}`,
      refresh_token: getUser().refresh_token,
    }).then((res) => {
      console.log('refresh token response', res);
      const { access_token, refresh_token } = res.data;
      setUser({ ...getUser(), access_token, refresh_token });
      return res;
    });
  } else {
    // remove the user
    setUser(null);
  }
};


