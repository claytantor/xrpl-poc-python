import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const PayloadService = {
    getAll(){
        return AxiosService.get(`/payload`);     
    }, 
};
