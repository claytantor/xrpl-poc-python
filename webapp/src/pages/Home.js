import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import { WalletService } from "../services/WalletService"
import {AiOutlineCheckCircle} from "react-icons/ai"

const Home = ({useStore}) => {
    const [version, setVersion] = useState();

    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-1"> 
                <div className="relative flex min-h-screen flex-col justify-center overflow-hidden bg-gray-50">
                <div className="relative bg-white px-6 pt-6 pb-6 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-10">
                    <div className="mx-auto max-w-md">
                    <div className="text-4xl font-bold text-pink-800">xurlpay.org</div>
                    <div className="divide-y divide-gray-300/50">
                        <div className="space-y-6 py-8 text-base leading-7 text-gray-600">
                        <div>This site is an online proof of concept to show how the <span className="font-bold text-pink-500">xInvoice</span> and <span className="font-bold text-pink-500">xURL</span> protocols can be applied to enable numerous payment and point of use sale cases for the XRP ecosystem:</div>
                        <ul className="space-y-4">
                            <li className="flex items-center">
                                <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                                <div className="ml-2 w-11/12">Allows for signed payment request <span className="font-bold text-pink-500">xInvoices</span> that can guarantee payment to the correct requestor.</div>
                            </li>
                            <li className="flex items-center">
                                <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                                <div className="ml-2 w-11/12">Provides stateful tracking of payment state for payment requests as <span className="font-bold text-pink-500">xInvoices</span> via backend.</div>
                            </li>

                            <li className="flex items-center">
                                <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                                <div className="ml-2 w-11/12"><span className="font-bold text-pink-500">xURL</span> automation of payment request creation by a live backend automation empowering payment with POS, instant currency conversion, and non expiring "scan to pay" capabilities.</div>
                            </li>

                        </ul>
                        <div>This site gives you everything you need to use the proposed protocols on the <a className="underline" href="https://testnet.xrpl.org/" target="_new">XRP testnet</a>. Including wallet creation, <span className="font-bold text-pink-500">xInvoice</span> creation, <span className="font-bold text-pink-500">xURL</span> creation and "Scan To Pay"</div>
                        </div>
                        <div className="pt-8 text-base font-semibold leading-7">
                        <div className="text-gray-900">Want to dig deeper into <span className="font-bold text-pink-500">xInvoice</span> and the <span className="font-bold text-pink-500">xURL</span> protocol specification?</div>
                        <div>
                            <a href="https://github.com/claytantor/xrpl-poc-python/blob/main/docs/whitepaper.md" className="text-pink-500 underline hover:text-pink-600">Read the whitepaper</a>
                        </div>
                        </div>
                    </div>
                    </div>
                </div>
                </div>

            </div>
        </Page> 
        </>

    )
}

export default Home