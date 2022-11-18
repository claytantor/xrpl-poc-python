import React, {useEffect, useState } from "react"
// import QRCode from "react-qr-code";

import { SiXrp } from "react-icons/si"

import xummLogo from "../assets/img/xumm_logo.png"

import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import {BiCheckCircle} from "react-icons/bi"


const PaymentRequest = ({xummState, paymentRequest, setPaymentRequest}) => {
    

    const [xummPayload, setXummPayload] = useState();
    const [customPayloadMeta, setCustomPayloadMeta] = useState();
    const [expiresSecs, setExpiresSecs] = useState();
    const [payloadState, setPayloadState] = useState("CREATED");
    const [error, setError] = useState();

    useEffect(() => {

      console.log("PaymentRequest", paymentRequest);
      if(xummState.sdk){
        const Sdk = xummState.sdk;

        const client = new W3CWebSocket(paymentRequest.refs.websocket_status);
        client.onopen = () => {
          console.log('WebSocket Client Connected');
        };
        client.onmessage = (message) => {
          console.log("GOT MESSAGE", message);
          const m_payload = JSON.parse(message.data);
          console.log("GOT MESSAGE parsed", m_payload);
          if ("expires_in_seconds" in m_payload) {
            setExpiresSecs(m_payload.expires_in_seconds);
          } else if ("payload_uuidv4" in m_payload) {
            client.close();
            setExpiresSecs(null);
            setPayloadState("RESOLVED");
          } else if ("expired" in m_payload) {
            client.close();
            setExpiresSecs(null);
            setPayloadState(null);    
            setPaymentRequest(null);
          }
        };

        Sdk.payload.get(paymentRequest.uuid).then((res) => {
          console.log("payload", res);
          setXummPayload(res);
  
          if(res && res.custom_meta) {
            let meta = JSON.parse(res.custom_meta.blob);
            console.log("meta", meta);
            setCustomPayloadMeta(meta);
          }
  
        });


      } else {
        console.log("no sdk");
        setError("No xumm sdk");
      }
      

      

    }, [paymentRequest])


    return (
      <>
        <div className="p-4">
          <div className="rounded bg-slate-100 w-96 p-3">
            {error && <div className="text-red-500 text-2xl w-full rounded bg-pink-200">{error}</div>}
            <div className="flex flex-row font-bold text-2xl justify-center">
              <div>SCAN TO PAY</div>
            </div>
            <div className="flex flex-row justify-center">
              <div><img src={xummLogo} className="w-24" /></div>
            </div>

            {expiresSecs && <div className="flex flex-row justify-center">{expiresSecs} seconds left</div>}

            {customPayloadMeta && <><div className="flex flex-row mt-2 w-full justify-center">
                <span className="w-24 inline-flex justify-center items-center p-2 m-2 text-sm font-medium text-gray-800 bg-pink-200 rounded-full dark:bg-gray-700 dark:text-gray-300">{customPayloadMeta.network_type.toUpperCase()}</span>   
            </div>
            <div>
                <div className="flex justify-center text-4xl font-bold font-monospace text-pink-600 link-align-center">{parseFloat(customPayloadMeta.amount)} <SiXrp className="ml-1"/></div>
            </div></>}
            <div className="w-full">
              <div className="w-full flex justify-center">

                <div className="p-2 rounded-xl bg-white flex items-center">
                    {paymentRequest && payloadState == "CREATED" && (
                        <img src={paymentRequest.refs.qr_png} />
                    )}
                    {paymentRequest && payloadState == "RESOLVED" && (
                        <BiCheckCircle className="text-green-600 text-9xl"/>
                    )}
                </div>

              </div>
            </div>

            <div className="flex flex-col justify-content-center p-3">
              <button className="btn-common-pink" onClick={() => setPaymentRequest(null)}>Back</button>
            </div>
          </div>

          {/* ================================================================ */}

        </div>
      </>
    );
}

export default PaymentRequest