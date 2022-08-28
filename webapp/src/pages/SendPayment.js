import React, {useEffect, useState } from "react"
import { QrReader } from 'react-qr-reader';

import Page  from "../components/Page"
import Spinner  from "../components/Spinner"

import { WalletService } from "../services/WalletService"

let counter = 0;

const PaymentResponseDetails = ({paymentResponse}) => {

    // Account: "rwuYypKV5JUXeif5yXXjQnHCb4KKLqsUHC"
    // Amount: "11200000"
    // Destination: "rQKg8UHs3xcGtwmhocnJyG3D6ybD5hDvLf"
    // Fee: "10"
    // Flags: 0
    // LastLedgerSequence: 30640100
    // Sequence: 30635795
    // SigningPubKey: "ED706ED2E4C67EC9603327D46F66DB9CAC999C6AA527FC111C8BC47C74A0BC812C"
    // TransactionType: "Payment"
    // TxnSignature: "579E16F80F6DB07EA24EFDE011432CC5A1885C8FF11337B0C20C8B3107D4B1BFF5CA93E016E2580B63968F6205A5FEBD36AA328EAFCC628C1DE5AE16F05BD609"
    // date: 714806771
    // hash: "2F737B392B9580EFDAA5F6499AACD05E924377DEC2EFEF2A8C184A8B5E510E47"
    // inLedger: 30640082
    // ledger_index: 30640082
    // meta: {AffectedNodes: Array(2), TransactionIndex: 0, TransactionResult: 'tesSUCCESS', delivered_amount: '11200000'}
    // validated: true


    return (<>

        <div className="flex border-spacing-2 flex-col rounded-lg bg-gray-200 p-4">
            <div className="flex-1 mb-1">
                <h2 className="text-xl">Payment sent.</h2>
                <div className="w-full bg-slate-800 rounded-md">
                    <pre className="text-pink-300 text-xs">
                    {JSON.stringify(paymentResponse, null, 2)}
                    </pre>
                </div>

            </div>
        </div>
    </>);
};

const SendPayment = ({useStore}) => {
    const [version, setVersion] = useState();
    const [paymentResponse, setPaymentResponse] = useState();
    const [data, setData] = useState();
    const [scanned, setScanned] = useState(false);
    const [showResult, setShowResult] = useState(false);
    const [delayScan , setDelayScan] = useState(500);

    const constraints = {
        facingMode: "environment"
    };



    let stopVideoAction = () =>  {
        navigator.mediaDevices.getUserMedia({
          video: true
        }).then(stream => {
            stream.getVideoTracks()[0].enabled = !(stream.getVideoTracks()[0].enabled)
        })
      
        // this.myStream.getVideoTracks()[0].enabled = !(this.myStream.getVideoTracks()[0].enabled)
        // this.mediaStatus.video = this.myStream.getVideoTracks()[0].enabled
      }

    const handleScan = (data) => {
        if(scanned === false && data !== null) {
            stopVideoAction();
            console.log(data);  
            setData(data);
            setScanned(true);
            setDelayScan(10000000000);

            setTimeout(() => {
                setScanned(true);
                setShowResult(true);       
                WalletService.postSendPayment(data).then(r => {    
                    setPaymentResponse(r.data);
                    console.log(r.data);
                }).catch(error => {
                    console.log(error);
                }).finally(() => {
                    console.log("finally");
                });

            },3000);

        
        }



    };


    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-1 m:p-4"> 
            
               
                { counter=== 0 && scanned === false && <div className="flex justify-center w-full">
                
                    <div className="text-center w-full md:w-1/2 p-1 md:p2" id="qr-reader">
                    <div className="text-2xl">Scan To Send Payment</div>
                    <div className="border-4 rounded-md h-fit border-dashed p-1 border-slate-300">
                        <QrReader
                            scanDelay={delayScan}
                            onError={(err) => console.error(err)}               
                            constraints={ constraints }
                            onResult={(result, error) => {
                                
                                if (!!result && counter === 0)  { 
                                    counter = counter + 1;
                                    handleScan({'payment_request':result?.text});
                                } 
                            }}
                        />
                    </div>
                    </div>
                </div>}

                <div>{data && showResult &&
                    <> 
                        <div>
                            <div className="text-xl">Attempting to make payment...</div>
                            <div className="text-pink-800 text-xs break-all">
                            {data.payment_request}
                            </div>
                        </div>
                        { paymentResponse ? <><PaymentResponseDetails paymentResponse={paymentResponse}/></> : <div><Spinner/></div>}
                        
                    </>}
                    </div>

                {paymentResponse && <div className="break-all">ITEM PAID</div> }
            </div>
        </Page> 
        </>
    )
}

export default SendPayment