import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';

import Page from "../components/Page"
import CustomerShopList from "../components/CustomerShopList";

const CustomerShops = ({xummState}) => {
   
    const navigate = useNavigate();
    return (
        <>
        <Page withSidenav={true} 
            xummState={xummState}>
            <div className='p-4'>
                <div className="p-1 flex flex-row justify-between">        
                    <h2 className="text-2xl">Where I Shop </h2>
                </div>
                <CustomerShopList xummState={xummState} />
            </div>
        </Page> 
        </>
    )
}

export default CustomerShops