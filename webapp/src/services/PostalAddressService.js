import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const PostalAddressService = {
    getById(id) {
        console.log("getById", id);
        return AxiosService.get(`/postal_address/${id}`);
    },
    createAddressItem(formData) {
        return AxiosService.post(`/address`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    updateAddressItem(formData) {
        return AxiosService.put(`/address`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    deleteAddressItem(addressId) {
        return AxiosService.del(`/address/${addressId}`);
    },
    getAddressItems (){
        return AxiosService.get(`/address`);
    },
    
};
