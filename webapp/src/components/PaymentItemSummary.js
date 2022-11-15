import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
// import { Trash, Edit,  Printer, PlusCircle } from "react-feather";


const PaymentItemSummary = ({ 
    useStore,
    paymentItem,
    handleDeleteCallback
    }) => {

    const { addPaymentItemToCart } = useStore();

    let image=paymentItem.images.length > 0 ? paymentItem.images[0]['data_url'] : '';
    let price=paymentItem.price;
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
                <div className='flex justify-end'>
                    <button className="text-xs flex hover:bg-orange-600 bg-orange rounded-lg m-1 p-1" onClick={()=>addPaymentItemToCart(paymentItem)}>
                            {/* <PlusCircle className='w-3 mr-1'/> */}
                            <div className='mt-1 align-bottom'>Add to Cart</div></button>
                </div>
                <img className="card-img-top" src={image} alt="" />
                <div className="px-6 py-1">
                    <div className="font-bold text-xl mb-1">{paymentItem.name}</div>
                    <p className="text-gray-700 text-sm">{paymentItem.description}</p>
                </div>
                <div className="px-1 pt-1 pb-2">
                    <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2">
                        {Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price)}
                    </span>
                    <div className='flex justify-end flex-wrap'>
                        <button className="text-xs flex hover:bg-blue-600 bg-blue rounded-lg m-1 p-1" onClick={()=>navigate(details_url)}>
                            {/* <Printer className='w-3 mr-1'/> */}
                            <div className='mt-1 align-bottom'>Print</div></button>
                        <button className="text-xs flex hover:bg-blue-600 bg-blue rounded-lg m-1 p-1" onClick={()=>navigate(edit_url)}>
                            {/* <Edit className='w-3 mr-1'/> */}
                            <div className='mt-1 align-bottom'>Edit</div></button>
                        <button className="text-xs flex hover:bg-blue-600 bg-blue rounded-lg m-1 p-1" onClick={()=>handleDelete()}>
                            {/* <Trash className='w-3 mr-1'/> */}
                            <div className='mt-1 align-bottom'>Delete</div></button>                    

                    </div>

                </div>
        </div>


        </div>
    </>);
}

export default PaymentItemSummary;