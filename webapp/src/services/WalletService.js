import Axios from 'axios';
import { round } from 'lodash';
import {AxiosService} from "./AxiosService";

Axios.defaults.withCredentials = false; 

export const WalletService = {
    getInfo(){
        return AxiosService.get(`/info`);     
    },
    getXrpPrice(currency){
        return AxiosService.get(`/xrp/price/${currency}`);     
    },
    getWallet(){
        console.log("getWallet");
        return AxiosService.get(`/wallet`);     
    },
    getPayRequest(){
        return AxiosService.get(`/wallet/pay_request`);     
    },
    postPayRequest(formData){
        return AxiosService.post(`/pay_request`, formData);;  
    },
    postSendPayment(formData){
        return AxiosService.post(`/send_payment`, formData);;  
    },   
    create(){
        return AxiosService.post(`/wallet`, {
            headers: {
                "Accept": "*/*",
                "Content-Type": "application/json" 
            },
            data: {},
        });     
    }

};
