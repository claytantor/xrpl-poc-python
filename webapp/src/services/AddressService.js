import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const AddressService = {
    fetchPage(query = {location: '/address', page: 1, page_size: 15}) {
        return AxiosService.fetchPage(query.location, query);
    },
    getById(id) {
        console.log("getById", id);
        return AxiosService.get(`/address/${id}`);
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
    getShopItems (account){
        return AxiosService.get(`/address/shop/${account}`);
    },
    getAddressItemsPaged (pageInfo={page: 1, page_size: 15}){
        return AxiosService.getPage(`/address`, pageInfo);
    },
    uploadProductsCSVFile(formData) {
        return AxiosService.post(`/address/csv`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    }
};
