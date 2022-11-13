import React, {useEffect, useState } from "react"
// import QRCode from "react-qr-code";

import Page  from "../components/Page"
import PaymentRequest from "../components/PaymentRequest";
import PaymentRequestForm from "../components/PaymentRequestForm";
import { WalletService } from "../services/WalletService"


const ReceivePayment = () => {
    
    const [paymentRequest, setPaymentRequest] = useState();

    return (
        <>
        <Page withSidenav={true}> 
            <div className="p-4"> 
                <div className="p-1 flex w-full justify-center">
                {paymentRequest ? <PaymentRequest paymentRequest={paymentRequest} setPaymentRequest={setPaymentRequest}/>:
                <PaymentRequestForm setPaymentRequest={setPaymentRequest}/>}
                </div>
            </div>
        </Page> 
        </>
    )
}

export default ReceivePayment