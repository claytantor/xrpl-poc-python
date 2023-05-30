import React , { useState, useEffect }from 'react'
// import CustomerShopSummary, {ShopCustomerShopSummary} from "./CustomerShopSummary";
import { CustomerAccountService } from '../services/CustomerAccountService';
import XurlService from '../services/XurlService';
import { useNavigate } from 'react-router-dom';
import ConfirmModal from "./ConfirmModal";
import { Spinner } from './Base';
import {BsCardChecklist,BsCashCoin,BsShop, BsCart} from "react-icons/bs";

import {xummConfig, currencyLang, xurlBaseUrl} from "../env"

const CustomerShopList = () => {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [customerShops, setCustomerShops] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});

    const [showModal, setShowModal] = useState(false);
    const [deleteId, setDeleteId] = useState();

    useEffect(() => {
        fetchCustomerShops(currentPage);
    },[currentPage]);
    
    let fetchCustomerShops = (pageInfo) => {
        setLoading(true);
        CustomerAccountService.getCustomerShops().then(res => {
            setCustomerShops(res.data);
            setLoading(false);
        }).catch(err => {      
            console.error(err);
        });       
    };

    let deleteCustomerShop = (id) => {
        console.log("set deleteCustomerShop", id);
        setDeleteId(id);
        setShowModal(true);
    }

    let handleConfirmDelete = () => {
        CustomerAccountService.deleteCustomerShop(deleteId)
        .then(res => {
            fetchCustomerShops(currentPage);
            navigate('/items');
        })
        .catch(err => {
            console.error(err);
        });
        setShowModal(false);
    }
    

    const listItems = customerShops.map((customerShop) => (
        <div className="w-full p-2 m-1 rounded-lg bg-slate-100 flex flex-row items-center hover:bg-cyan-200 hover:cursor-pointer" 
        onClick={()=>navigate(`/shop/${customerShop.shop_id}`)}
        key={customerShop.id}>  
            <BsShop className='mr-2'/> {customerShop.shop_id} 
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}       
            {customerShops.length>0 ? 
                <div className='flex'>
                    <div className='flex flex-row'>{listItems}</div>
                </div>
            : 
                <div>You have not added yourself as a customer to any shops yet.</div>}
        </div>

    </>);
};

export const ShopCustomerShopList = ({shop_id}) => {

    const [loading, setLoading] = useState(true);
    const [customerShops, setCustomerShops] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});


    useEffect(() => {
        fetchCustomerShops(shop_id, currentPage);
    },[currentPage]);
    
    let fetchCustomerShops = (shop_id, pageInfo) => {
        setLoading(true);
        XurlService.getSubjectItems(xurlBaseUrl(shop_id),'paymentitem')
        .then(res => {
            console.log("B getSubject", res.data);
            setCustomerShops(res.data);
            setLoading(false);
        });
    };
    
    const listItems = customerShops.map((customerShop) => (
        <div className="w-64 p-2 m-1 rounded" key={customerShop.id}>  
            {customerShop.id}
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            <div onClick={()=>window.open(`${xurlBaseUrl(shop_id)}/info`,'_blank')} className="link-common">{xurlBaseUrl(shop_id)}/info</div>
            {xurlBaseUrl(shop_id) && <div className='text-xs'>xurlBaseUrl: {xurlBaseUrl(shop_id)}</div>}
            {customerShops.length>0 ? 
                <div className='flex flex-row justify-center'>
                    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>{listItems}</div>
                </div>
            : 
                <div>No Payment Items</div>}
        </div>

    </>);
};



export default CustomerShopList;

