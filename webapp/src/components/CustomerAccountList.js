import React , { useState, useEffect }from 'react'
// import CustomerAccountSummary, {ShopCustomerAccountSummary} from "./CustomerAccountSummary";
import { CustomerAccountService } from '../services/CustomerAccountService';
import XurlService from '../services/XurlService';
import { useNavigate } from 'react-router-dom';
import ConfirmModal from "./ConfirmModal";
import { Spinner } from './Base';
import {FaWallet, FaShoppingBag, FaUserTie} from "react-icons/fa";

// import { Row, Col, Spinner } from 'react-bootstrap';

import {xummConfig, currencyLang, xurlBaseUrl} from "../env"

// const Spinner = ({animation}) => {
//     return (
//         <div className={`spinner-border ${animation ? 'spinner-border-sm' : ''}`} role="status">
//             <span className="sr-only">Loading...</span>
//         </div>
//     )
// };


const CustomerAccountList = () => {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [customerAccounts, setCustomerAccounts] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});

    const [showModal, setShowModal] = useState(false);
    const [deleteId, setDeleteId] = useState();

    useEffect(() => {
        fetchCustomerAccounts(currentPage);
    },[currentPage]);
    
    let fetchCustomerAccounts = (pageInfo) => {
        setLoading(true);
        CustomerAccountService.getCustomerAccounts().then(res => {
            setCustomerAccounts(res.data);
            setLoading(false);
        }).catch(err => {      
            console.error(err);
        });       
    };


    let deleteCustomerAccount = (id) => {
        console.log("set deleteCustomerAccount", id);
        setDeleteId(id);
        setShowModal(true);
    }

    let handleConfirmDelete = () => {
        CustomerAccountService.deleteCustomerAccount(deleteId)
        .then(res => {
            fetchCustomerAccounts(currentPage);
            navigate('/items');
        })
        .catch(err => {
            console.error(err);
        });
        setShowModal(false);
    }
    

    const listItems = customerAccounts.map((customerAccount) => (
        <div className="w-full p-2 m-1 rounded-lg bg-slate-100 flex flex-row items-center" key={customerAccount.id}>  
            <FaUserTie className='mr-2'/> {customerAccount.account_wallet.classic_address} 
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            
            {customerAccounts.length>0 ? 
                // <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                <div className='flex'>
                    <div className='flex flex-row'>{listItems}</div>
                    <div>
                        <ConfirmModal showModal={showModal} setShowModal={setShowModal} actionName={'Delete Payment Item'} 
                        actionDescription={'delete this product'} actionCallback={handleConfirmDelete}/>
                    </div>
                </div>
            : 
                <div>No Payment Items</div>}
        </div>

    </>);
};

export const ShopCustomerAccountList = ({shop_id}) => {

    const [loading, setLoading] = useState(true);
    const [customerAccounts, setCustomerAccounts] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});


    useEffect(() => {
        fetchCustomerAccounts(shop_id, currentPage);
    },[currentPage]);
    
    let fetchCustomerAccounts = (shop_id, pageInfo) => {
        setLoading(true);
        XurlService.getSubjectItems(xurlBaseUrl(shop_id),'paymentitem')
        .then(res => {
            console.log("B getSubject", res.data);
            setCustomerAccounts(res.data);
            setLoading(false);
        });
    };
    
    const listItems = customerAccounts.map((customerAccount) => (
        <div className="w-64 p-2 m-1 rounded" key={customerAccount.id}>  
            {/* <ShopCustomerAccountSummary
                customerAccount={customerAccount}
                shop_id={shop_id}/>        */}
            {customerAccount.id}
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            <div onClick={()=>window.open(`${xurlBaseUrl(shop_id)}/info`,'_blank')} className="link-common">{xurlBaseUrl(shop_id)}/info</div>
            {xurlBaseUrl(shop_id) && <div className='text-xs'>xurlBaseUrl: {xurlBaseUrl(shop_id)}</div>}
            {customerAccounts.length>0 ? 
                // <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                <div className='flex flex-row justify-center'>
                    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>{listItems}</div>
                </div>
            : 
                <div>No Payment Items</div>}
        </div>

    </>);
};



export default CustomerAccountList;

