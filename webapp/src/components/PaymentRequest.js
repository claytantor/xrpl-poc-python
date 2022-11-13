import React, {useEffect, useState } from "react"
// import QRCode from "react-qr-code";

import Page  from "../components/Page"
import { WalletService } from "../services/WalletService"
import { SiXrp } from "react-icons/si"
import {BiCopy} from "react-icons/bi"


import xummLogo from "../assets/img/xumm_logo.png"

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


    return (
      <>
        <div className="p-4">
          <div className="rounded bg-slate-100 w-96 p-3">
            <div className="flex flex-row font-bold text-2xl justify-center">
              <div>SCAN NOW</div>
            </div>
            <div className="flex flex-row justify-center">
              <div><img src={xummLogo} className="w-24" /></div>
            </div>
            <div>
                <div className="flex justify-center text-4xl font-bold font-monospace text-pink-600 link-align-center">{parseFloat(paymentRequest.payment_request.amount)} <SiXrp className="ml-1"/></div>
            </div>
            <div className="w-full">
              <div className="w-full flex justify-center">

                <div className="p-2 rounded-xl bg-white flex items-center">
                    {paymentRequest && (
                        // <QRCode className="m-2" value={paymentRequest.payment_request} size={300} />
                        <>
                        {/* <div>
                          <pre>{JSON.stringify(paymentRequest, null, 2)}</pre>
                        </div> */}
                        <img src={paymentRequest.payload.refs.qr_png} />
                        </>
                    )}
                </div>
              </div>
              {/* <div className="d-flex flex-col justify-content-center mb-2">
                <div className="w-full text-center text-xs font-bold">
                  expires:
                </div>
                <div className="text-center text-sm text-gray-500">
                    Thursday, Aug 25, 2022, 3:15 PM -{" "}
                    <time
                        className="italic text-slate-600"
                        dateTime="2022-08-25T22:15:11.634Z"
                        title="Thursday, August 25, 2022 at 3:15:11 PM"
                    >
                        in 7 hours
                    </time>
                </div>
                <div className="w-full text-center font-bold text-pink-600 font-mono">00:00:29:04</div>
              </div> */}
            </div>
            {/* <div className="bg-slate-700 rounded-md p-3">
                <div className="break-all font-bold text-sm font-mono text-pink-400">{paymentRequest.payment_request}</div>                
            </div>
            <div className="flex flex-col justify-content-center">
              <button className="bg-blue hover:bg-pink-600 hover:text-white rounded flex m-1 p-1 justify-center items-center hover:underline">
                <BiCopy/>
                Copy
              </button>{" "}

              <button
                className="btn-common-pink"
                onClick={() => setPaymentRequest(null)}
                >
                Create New Request
                </button>

            </div> */}
          </div>

          {/* ================================================================ */}

        </div>
      </>
    );
}

export default PaymentRequest