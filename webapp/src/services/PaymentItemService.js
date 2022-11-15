import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const PaymentItemService = {
    fetchPage(query = {location: '/payment_item', page: 1, page_size: 15}) {
        return AxiosService.fetchPage(query.location, query);
    },
    getById(id) {
        console.log("getById", id);
        return AxiosService.get(`/payment_item/${id}`);
    },
    createPaymentItem(formData) {
        return AxiosService.post(`/payment_item`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    updatePaymentItem(formData) {
        return AxiosService.put(`/payment_item`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    },
    deletePaymentItem(paymentItemId) {
        return AxiosService.del(`/payment_item/${paymentItemId}`);
    },
    getPaymentItems (){
        return AxiosService.get(`/payment_item`);
    },
    getPaymentItemsPaged (pageInfo={page: 1, page_size: 15}){
        return AxiosService.getPage(`/payment_item`, pageInfo);
    },
    uploadProductsCSVFile(formData) {
        return AxiosService.post(`/payment_item/csv`, formData, {
            headers: {'Content-Type': 'multipart/form-data'}
        });
    }
};
