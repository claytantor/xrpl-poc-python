import Axios from "axios";
import moment from 'moment';
import { useNavigate } from "react-router-dom";
import {useStore} from "../store";
import { backendBaseUrl } from '../env';

Axios.defaults.withCredentials = false; 

const handleAxiosError = (error) => {
    let error_model = {
        message: "There was an error",
        status: 500,
        data: null,
        request:null
    };
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        // console.log(error.response.data);
        // console.log(error.response.status);
        // console.log(error.response.headers);

        error_model.message = error.response.data.message;
        error_model.status = error.response.status;
        error_model.data = error.response.data;
        

      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        // console.log(error.request);
        error_model.request = error.request;

      } else {
        // Something happened in setting up the request that triggered an Error
        // console.log('Error', error.message);
        error_model.message = error.message;
      }

      return error_model;
};

const axiosInstance = Axios.create({
    baseURL: backendBaseUrl,
    responseType: 'json',
    responseEncoding: 'utf8'
});



axiosInstance.interceptors.request.use((config) => { 

    // // const navigate = useNavigate();
    // const xummAuthState = useStore((state) => state.xummState);
    // const setXummState = useStore((state) => state.setXummState);


    console.log('interceptors.request.use', config);
    if (
        config.url.endsWith('/version')
    ) {
        // Without this, calling refresh_token 
        // will trigger infinite recursion
        return config;
    }

    // cachedUser = xummAuthState;

    if (!cachedUser || cachedUser.jwt === undefined) {
        console.log('cached user NOT found, sending to login', config);
        return config;
    } else if (cachedUser) {
        console.log('cached user found', config, cachedUser);
        const info = getAccessTokenInfo(cachedUser.jwt);
        if (info.expirationDate && info.expirationDate.isBefore(moment.utc().add(1, 'minutes'))) {
            console.log('token expired');
            // setXummState(null);
            // navigate('/login');
        }
    }
    config.headers.authorization = cachedUser.access_token;
    return config;

}, function (error) {
    return Promise.reject(error);
});


function get(url) {
    return axiosInstance.get(url)
}

function post(url, data) {
    return axiosInstance.post(url, data);
}

function put(url, data) {
    return axiosInstance.put(url, data);
}

function destroy(url, data) {
    return axiosInstance.destroy(url, data);
}

function del(url) {
    return axiosInstance.delete(url);
}

function setUser(user) {
    console.log('setUser', user);
    cachedUser = user;
}


export const AxiosService = {
    axiosInstance,
    get,
    post,
    put,
    del,
    destroy,
    handleAxiosError,
    backendBaseUrl,
    setUser
};
