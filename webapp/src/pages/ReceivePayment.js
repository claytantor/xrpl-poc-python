import React, {useEffect, useState } from "react"
// import QRCode from "react-qr-code";

import Page  from "../components/Page"
import PaymentRequest from "../components/PaymentRequest";
import PaymentRequestForm from "../components/PaymentRequestForm";


const ReceivePayment = ({xummState}) => {
    
    const [paymentRequest, setPaymentRequest] = useState();

    return (
        <>
        <Page withSidenav={true} 
            xummState={xummState}> 
            <div className="p-4"> 
                <div className="p-1 flex w-full justify-center">
                {paymentRequest ? 

                    <>{/* <div>{JSON.stringify(paymentRequest,null,2)}</div> */}
                    <PaymentRequest xummState={xummState} paymentRequest={paymentRequest.body} setPaymentRequest={setPaymentRequest}/>
                    </>
                :
                <PaymentRequestForm setPaymentRequest={setPaymentRequest}/>}
                </div>
            </div>
        </Page> 
        </>
    )
}

export default ReceivePayment