import React , { useState, useEffect }from 'react'
import { useNavigate } from 'react-router-dom';

import PaymentItemSummary, {ShopPaymentItemSummary} from "./PaymentItemSummary";
import {AddressService} from '../services/AddressService';
import ConfirmModal from "./ConfirmModal";
import { Spinner } from './Base';

// import { Row, Col, Spinner } from 'react-bootstrap';

import {xummConfig, currencyLang, xurlBaseUrl} from "../env"


const AddressList = ({addressItems, currentPage}) => {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);

    const [showModal, setShowModal] = useState(false);
    const [deleteId, setDeleteId] = useState();

    let deletePaymentItem = (id) => {
        console.log("set deletePaymentItem", id);
        setDeleteId(id);
        setShowModal(true);
    }

    let handleConfirmDelete = () => {
        AddressService.deletePaymentItem(deleteId)
        .then(res => {
            fetchAddressItems(currentPage);
            navigate('/items');
        })
        .catch(err => {
            console.error(err);
        });
        setShowModal(false);
    }
    
    const listItems = addressItems.map((address) => (
        <div onClick={() => navigate(`/address/${address.id}`)} 
            className="hover:cursor-pointer flex flex-wrap w-full my-2 p-1 rounded bg-slate-300 hover:bg-pink-200" key={address.id}>             
            <span className="ml-1 mr-3 font-bold">{address.name}</span>
            <span className="mr-1">{address.first_name}</span>
            <span className="mr-2">{address.last_name}</span>
            <span className="mr-2">{address.street_address}</span>
            <span className="mr-2">{address.city}</span>
            <span className="mr-2">{address.state}</span>
            <span className="mr-2">{address.postal_code}</span>
            <span className="mr-2">{address.country}</span>
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            
            {addressItems.length>0 ? 
                // <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                <div className='flex flex-col w-full'>
                    <div className='flex flex-col w-full'>{listItems}</div>
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


export default AddressList;

