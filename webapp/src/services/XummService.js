import Axios from 'axios';
import { AxiosService } from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const XummService = {
// curl --request GET \
//      --url https://xumm.app/api/v1/jwt/authorize \
//      --header 'X-API-Key: 1b144141-440b-4fbc-a064-bfd1bdd3b0ce' \
//      --header 'X-API-OTT: 7acffb42-4c95-4456-aab2-c85d1784bdf7' \
//      --header 'accept: application/json'

    authorize(api_key, ott){
        const authHeaders = {
            'X-API-Key': api_key,
            'X-API-OTT': ott,
            'accept': 'application/json'
        };
        return Axios.get(`https://xumm.app/api/v1/jwt/authorize`, {headers:authHeaders});     
    }, 
    makeXummQr(url){
        return AxiosService.get(`/xumm/qr?url=${encodeURI(url)}`);
    }
};



