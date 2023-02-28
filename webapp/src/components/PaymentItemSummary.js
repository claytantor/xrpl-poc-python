import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {currencyLang} from '../env';


export const ShopPaymentItemSummary = ({paymentItem, address}) => {
    let image='https://picsum.photos/200/200';
    if (paymentItem.images.length>0) {
        image = paymentItem.images[0]['data_url']
    }

    let navigate = useNavigate();
    
    return (<>
        <div className="m-1" id={paymentItem.payment_item_id}>
            
            <div className="p-1 max-w-sm rounded overflow-hidden shadow-md hover:border-pink-300 hover:border-2 hover:cursor-pointer"
                 onClick={()=>navigate(`/shop/details/${address}/${paymentItem.payment_item_id}`)}>
                {/* <div className='flex justify-end'>
                    <button className="text-xs flex underline hover:text-pink-500 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div> */}
                <img className="card-img-top" src={image} alt={paymentItem.name} />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2">
                    <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                        {Intl.NumberFormat(currencyLang[paymentItem.fiat_i8n_currency], { style: 'currency', currency: paymentItem.fiat_i8n_currency }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                    </span>
                    {/* <div className='flex justify-end flex-wrap'>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/shop/details/${address}/${paymentItem.payment_item_id}`)}>
                            View</button>
                    </div> */}

                </div>
        </div>


        </div>
    </>);
};

const PaymentItemSummary = ({ 
    paymentItem,
    handleDeleteCallback
    }) => {

    let image='https://picsum.photos/200/200';
    if (paymentItem.images.length>0) {
        image = paymentItem.images[0]['data_url']
    }

    let navigate = useNavigate();
    

    let handleDelete = () => {
        handleDeleteCallback(paymentItem.payment_item_id);
    };

    return (<>
        <div className="m-1" id={paymentItem.payment_item_id}>
            
            <div className="p-1 max-w-sm rounded overflow-hidden shadow-md">
                {/* <div className='flex justify-end'>
                    <button className="text-xs flex underline hover:text-pink-500 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div> */}
                <img className="card-img-top" src={image} alt={paymentItem.name} />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2">
                    <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                        {Intl.NumberFormat(currencyLang[paymentItem.fiat_i8n_currency], { style: 'currency', currency: paymentItem.fiat_i8n_currency }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                    </span>
                    <div className='flex justify-end flex-wrap'>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/item/details/${paymentItem.payment_item_id}`)}>
                            View</button>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/item/edit/${paymentItem.payment_item_id}`)}>
                            Edit</button>
                        <button className="btn-common-pink text-xs" onClick={()=>handleDelete()}>
                            {/* <Trash className='w-3 mr-1'/> */}Delete</button>                    

                    </div>

                </div>
        </div>


        </div>
    </>);
}

export default PaymentItemSummary;