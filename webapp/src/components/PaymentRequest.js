import React, {useEffect, useState } from "react"
// import QRCode from "react-qr-code";

import { SiXrp } from "react-icons/si"
import {BiCopy} from "react-icons/bi"
import { XummSdkJwt } from 'xumm-sdk';

import Page  from "../components/Page"
import { WalletService } from "../services/WalletService"

import {useStore} from "../zstore"

import xummLogo from "../assets/img/xumm_logo.png"

import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import {BiCheckCircle} from "react-icons/bi"


const PaymentRequest = ({paymentRequest, setPaymentRequest}) => {
    
  // "payload":{
  //   "next": {
  //     "always": "https://xumm.app/sign/8da5753a-0d66-4e32-b36a-c7d7e05c0eef"
  //   },
  //   "pushed": false,
  //   "refs": {
  //     "qr_matrix": "https://xumm.app/sign/8da5753a-0d66-4e32-b36a-c7d7e05c0eef_q.json",
  //     "qr_png": "https://xumm.app/sign/8da5753a-0d66-4e32-b36a-c7d7e05c0eef_q.png",
  //     "qr_uri_quality_opts": [
  //       "m",
  //       "q",
  //       "h"
  //     ],
  //     "websocket_status": "wss://xumm.app/sign/8da5753a-0d66-4e32-b36a-c7d7e05c0eef"
  //   },
  //   "uuid": "8da5753a-0d66-4e32-b36a-c7d7e05c0eef"
  // }

  // payment_request
  // : 
  // {address: "rawGjfwXckcCRtcszxzYBXVze21iqM7VvM", amount: 1.15, amount_drops: 1150000,…}
  // address
  // : 
  // "rawGjfwXckcCRtcszxzYBXVze21iqM7VvM"
  // amount
  // : 
  // 1.15
  // amount_drops
  // : 
  // 1150000
  // expires
  // : 
  // 1668049842.740856
  // memo
  // : 
  // "its for the kids man"
  // public_key
  // : 
  // "ED2FFF132204385B93BEE3744BA2F77E818DB96FBBBF272DC6B613927C301E5C30"
  // request_hash
  // : 
  // "aFhWHgebXTRyPPbsUMGALd"

    const xummAuthState = useStore((state) => state.xummState);

    const [xummPayload, setXummPayload] = useState();
    const [customPayloadMeta, setCustomPayloadMeta] = useState();
    const [expiresSecs, setExpiresSecs] = useState();
    const [payloadState, setPayloadState] = useState("CREATED");

    useEffect(() => {

      console.log("PaymentRequest", paymentRequest, xummAuthState);
      const Sdk = new XummSdkJwt(xummAuthState.jwt)

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

    }, [paymentRequest])


    return (
      <>
        <div className="p-4">
          <div className="rounded bg-slate-100 w-96 p-3">
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