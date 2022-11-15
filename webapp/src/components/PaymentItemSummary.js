import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
// import { Trash, Edit,  Printer, PlusCircle } from "react-feather";

// import { useStore } from '../zstore';


const PaymentItemSummary = ({ 
    paymentItem,
    handleDeleteCallback
    }) => {

    // const { addPaymentItemToCart } = useStore();
    // const addPaymentItemToCart = useStore(state => state.addPaymentItemToCart);
    // const { addPaymentItemToCart } = useStore(state => state);

    const addPaymentItemToCart = (paymentItem) => {};

    let image='https://picsum.photos/200/200';
    if (paymentItem.images) {
        image = paymentItem.images[0]['data_url']
    }
    
    
    // let price=paymentItem.fiat_i8n_price;
    let id=paymentItem.id;
    let edit_url='/item/edit/' + paymentItem.id;
    let details_url='/item/details/' + paymentItem.id;    

    let navigate = useNavigate();
    

    let handleDelete = () => {
        handleDeleteCallback(id);
    };

    return (<>
        <div className="m-1" id={id}>
            
            <div className="p-1 max-w-sm rounded overflow-hidden shadow-md">
                {/* <div className='flex justify-end'>
                    <button className="text-xs flex underline hover:text-pink-500 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div> */}
                <img className="card-img-top" src={image} alt="" />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2">
                    <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                        {Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                    </span>
                    <div className='flex justify-end flex-wrap'>
                        <button className="btn-common-pink text-xs" onClick={()=>navigate(`/item/details/${paymentItem.payment_item_id}`)}>
                            View</button>
                        {/* <button className="btn-common-pink text-xs" onClick={()=>navigate(details_url)}>
                            Print</button> */}
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