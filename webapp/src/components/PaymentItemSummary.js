import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {currencyLang, xurlBaseUrl} from '../env';


export const ShopPaymentItemSummary = ({paymentItem, shop_id}) => {
    let image='https://picsum.photos/200/200';
    if (paymentItem.inventory_item.images.length>0) {
        image = paymentItem.inventory_item.images[0]['data_url']
    }

    let navigate = useNavigate();
    
    return (<>
        <div className="m-1" id={paymentItem.id}>
            
            <div className="p-1 max-w-sm rounded overflow-hidden shadow-md hover:border-pink-300 hover:border-2 hover:cursor-pointer"
                 onClick={()=>navigate(`/shop/details/${shop_id}/paymentitem/${paymentItem.id}`)}>
                {/* <div className='flex justify-end'>
                    <button className="text-xs flex underline hover:text-pink-500 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div> */}
                <img className="card-img-top" src={image} alt={paymentItem.inventory_item.name} />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.inventory_item.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.inventory_item.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2 flex flex-col">
                    <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                        {Intl.NumberFormat(currencyLang[paymentItem.fiat_i8n_currency], { style: 'currency', currency: paymentItem.fiat_i8n_currency }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                    </span>
                    <div className='w-full text-right'>{paymentItem.verb}</div>

                    {/* <div className='flex justify-end flex-wrap'>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/shop/details/${address}/${paymentItem.id}`)}>
                            View</button>
                    </div> */}

                </div>
                
        </div>


        </div>
    </>);
};

const PaymentItemSummary = ({ 
    shop_id,
    paymentItem,
    handleDeleteCallback
    }) => {

    let image='https://picsum.photos/200/200';
    if (paymentItem.inventory_item.images.length>0) {
        image = paymentItem.inventory_item.images[0]['data_url']
    }

    //`http://8d810387b7.localhost:5005/xurlapi/xurl/subject/paymentitem/${paymentItem.id}`
    const pi_shop_url = `${xurlBaseUrl(shop_id)}/xurlapi/xurl/subject/paymentitem/${paymentItem.id}`;

    let navigate = useNavigate();
    

    let handleDelete = () => {
        handleDeleteCallback(paymentItem.id);
    };

    return (<>
        <div className="m-1" id={paymentItem.inventory_item.id}>
            
            <div className="p-1 max-w-sm rounded overflow-hidden shadow-md">
                {/* <div className='flex justify-end'>
                    <button className="text-xs flex underline hover:text-pink-500 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div> */}
                <img className="card-img-top" src={image} alt={paymentItem.inventory_item.name} />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.inventory_item.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.inventory_item.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2">
                    <div className='w-full flex flex-row justify-center'>
                        <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                            {Intl.NumberFormat(currencyLang[paymentItem.fiat_i8n_currency], { style: 'currency', currency: paymentItem.fiat_i8n_currency }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                        </span>
                    </div>
                    <div className='w-full flex flex-row justify-center'>
                        {paymentItem.verb}
                    </div>
                    <div className='flex justify-end flex-wrap'>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/item/details/${paymentItem.id}`)}>
                            View</button>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/item/edit/${paymentItem.id}`)}>
                            Edit</button>
                        <button className="btn-common-pink text-xs" onClick={()=>handleDelete()}>
                            {/* <Trash className='w-3 mr-1'/> */}Delete</button>   

                        {paymentItem.is_xurl_item && <button className="btn-common-pink text-xs" onClick={()=>window.open(pi_shop_url,'_blank')}>
                            xurl</button>}                    

                    </div>

                </div>
        </div>


        </div>
    </>);
}

export default PaymentItemSummary;