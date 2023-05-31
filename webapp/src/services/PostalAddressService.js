import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const PostalAddressService = {
    getById(id) {
        console.log("getById", id);
        return AxiosService.get(`/postal_address/${id}`);
    },
    createAddressItem(address_id, shop_id) {
        return AxiosService.post(`/postal_address`, {address_id, shop_id}, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    updateAddressItem(id, address_id, shop_id) {
        return AxiosService.put(`/postal_address`, {id, address_id, shop_id}, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    deleteAddressItem(postal_addressId) {
        return AxiosService.del(`/postal_address/${postal_addressId}`);
    },
    getAddressItems (){
        return AxiosService.get(`/postal_address`);
    },
    
};
