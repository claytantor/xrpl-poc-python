import React, {useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";

import Page from "../components/Page"

const Customers = ({xummState}) => {
   
    const navigate = useNavigate();
    return (
        <>
        <Page withSidenav={true} 
            xummState={xummState}>
            <div className='p-4'>
                <div className="p-1 flex flex-row justify-between">        
                    <h2 className="text-2xl">Customers </h2>
                    <div onClick={()=>navigate('/customer/create')} className="btn-common">Add Customer</div>
                </div>
            </div>
        </Page> 
        </>
    )
}

export default Customers