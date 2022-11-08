import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import { WalletService } from "../services/WalletService"
import { SiXrp } from "react-icons/si"
import {BiCopy} from "react-icons/bi"

const PaymentRequest = ({paymentRequest, setPaymentRequest}) => {
    

    return (
      <>
        <div className="p-4">
          <div className="rounded bg-slate-100 w-96 p-3">
            <div className="flex flex-row justify-center">
              <div className="m-1 mr-3 h-7 rounded bg-gray-400 p-1 text-sm font-bold text-white">
                PENDING
              </div>
            </div>
            <div className="font-bold text-3xl text-center">SCAN TO PAY</div>

            <div>

                <div className="flex justify-center text-4xl font-bold font-monospace text-pink-600 link-align-center">{parseFloat(paymentRequest.body.amount)} <SiXrp className="ml-1"/></div>


            </div>
            <div className="w-full">
              <div className="w-full flex justify-center">
                <div className="p-2 rounded-xl bg-white flex  items-center">
                    {paymentRequest && (
                        <QRCode className="m-2" value={paymentRequest.payment_request} size={300} />
                    )}
                </div>
              </div>
              <div className="d-flex flex-col justify-content-center mb-2">
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
              </div>
            </div>
            <div className="bg-slate-700 rounded-md p-3">
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

            </div>
          </div>

          {/* ================================================================ */}

          {/* <div className="text-2xl">Receive Payment</div>
          {paymentRequest && (
            <QRCode className="m-2" value={paymentRequest.payment_request} />
          )}
          <div className="break-all font-mono">
            {paymentRequest.payment_request}
          </div>
          <div>
            <button
              className="btn-common-pink"
              onClick={() => setPaymentRequest(null)}
            >
              Create New Request
            </button>
          </div> */}
        </div>
      </>
    );
}

export default PaymentRequest