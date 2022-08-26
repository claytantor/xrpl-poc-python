import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import { WalletService } from "../services/WalletService"


const Home = ({useStore}) => {
    const [version, setVersion] = useState();
    // const [paymentRequest, setPaymentRequest] = useState();

    // useEffect(() => {
    //     WalletService.getVersion().then(r => {
    //         setVersion(r.data.version)
    //     }).catch(error => {
    //         console.log(error)
    //     }).finally(() => {
    //         console.log("finally")
    //     });
    // } , [version])

    // useEffect(() => {
    //     WalletService.getPayRequest().then(r => {
    //         setPaymentRequest(r.data.paymentRequest)
    //     }).catch(error => {
    //         console.log(error)
    //     }).finally(() => {
    //         // console.log("finally")
    //     });
    // } , [])



    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-4"> 
                <h2 className="text-2xl">Welcome to xurlpay.org</h2>
                <p className="text-lg">
                    This is a simple web app that allows you to send and receive payments using xurlpay.org.
                </p>
            </div>
        </Page> 
        </>

    )
}

export default Home