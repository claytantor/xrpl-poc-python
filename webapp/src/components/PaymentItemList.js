import React , { useState, useEffect }from 'react'
import PaymentItemSummary, {ShopPaymentItemSummary} from "./PaymentItemSummary";
import { PaymentItemService } from '../services/PaymentItemService';
import XurlService from '../services/XurlService';
import { useNavigate } from 'react-router-dom';
import ConfirmModal from "./ConfirmModal";

// import { Row, Col, Spinner } from 'react-bootstrap';

import {xummConfig, currencyLang, xurlBaseUrl} from "../env"

const Spinner = ({animation}) => {
    return (
        <div className={`spinner-border ${animation ? 'spinner-border-sm' : ''}`} role="status">
            <span className="sr-only">Loading...</span>
        </div>
    )
};


const PaymentItemList = ({shop_id}) => {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [paymentItems, setPaymentItems] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});

    const [showModal, setShowModal] = useState(false);
    const [deleteId, setDeleteId] = useState();

    useEffect(() => {
        fetchPaymentItems(currentPage);
    },[currentPage]);
    
    let fetchPaymentItems = (pageInfo) => {
        setLoading(true);
        PaymentItemService.getPaymentItems().then(res => {
            setPaymentItems(res.data);
            setLoading(false);
        }).catch(err => {      
            console.error(err);
        });       
    };


    let deletePaymentItem = (id) => {
        console.log("set deletePaymentItem", id);
        setDeleteId(id);
        setShowModal(true);
    }

    let handleConfirmDelete = () => {
        PaymentItemService.deletePaymentItem(deleteId)
        .then(res => {
            fetchPaymentItems(currentPage);
            navigate('/items');
        })
        .catch(err => {
            console.error(err);
        });
        setShowModal(false);
    }
    

    const listItems = paymentItems.map((paymentItem) => (
        <div className="w-64 p-2 m-1 rounded" key={paymentItem.payment_item_id}>  
            <PaymentItemSummary
                shop_id={shop_id}
                handleDeleteCallback={deletePaymentItem}
                paymentItem={paymentItem}/>       
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            
            {paymentItems.length>0 ? 
                // <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                <div className='flex'>
                    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>{listItems}</div>
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

export const ShopPaymentItemList = ({shop_id}) => {

    const [loading, setLoading] = useState(true);
    const [paymentItems, setPaymentItems] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});


    useEffect(() => {
        fetchPaymentItems(shop_id, currentPage);
    },[currentPage]);
    
    let fetchPaymentItems = (shop_id, pageInfo) => {
        setLoading(true);
        XurlService.getSubjectItems(xurlBaseUrl(shop_id),'paymentitem')
        .then(res => {
            console.log("getSubject", res.data);
            setPaymentItems(res.data);
            setLoading(false);
        });
    };
    
    const listItems = paymentItems.map((paymentItem) => (
        <div className="w-64 p-2 m-1 rounded" key={paymentItem.id}>  
            <ShopPaymentItemSummary
                paymentItem={paymentItem}
                shop_id={shop_id}/>       
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            {/* <div onClick={()=>window.open(`${xurlBaseUrl(shop_id)}/info`,'_blank')} className="link-common">{xurlBaseUrl(shop_id)}/info</div>
            {xurlBaseUrl(shop_id) && <div className='text-xs'>xurlBaseUrl: {xurlBaseUrl(shop_id)}</div>} */}
            {paymentItems.length>0 ? 
                // <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                <div className='flex flex-row justify-center'>
                    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>{listItems}</div>
                </div>
            : 
                <div>No Payment Items</div>}
        </div>

    </>);
};



export default PaymentItemList;

