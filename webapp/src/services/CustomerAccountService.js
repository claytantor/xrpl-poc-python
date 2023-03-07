import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const CustomerAccountService = {
    fetchPage(query = {location: '/customer_account', page: 1, page_size: 15}) {
        return AxiosService.fetchPage(query.location, query);
    },
    getById(id) {
        console.log("getById", id);
        return AxiosService.get(`/customer_account/${id}`);
    },
    createCustomerAccount(formData) {
        return AxiosService.post(`/customer_account`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    updateCustomerAccount(formData) {
        return AxiosService.put(`/customer_account`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    deleteCustomerAccount(customerAccountId) {
        return AxiosService.del(`/customer_account/${customerAccountId}`);
    },
    getCustomerAccounts (){
        return AxiosService.get(`/customer_account`);
    },
    getShopItems (account){
        return AxiosService.get(`/customer_account/shop/${account}`);
    },
    getCustomerAccountsPaged (pageInfo={page: 1, page_size: 15}){
        return AxiosService.getPage(`/customer_account`, pageInfo);
    },
    uploadProductsCSVFile(formData) {
        return AxiosService.post(`/customer_account/csv`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    }
};
