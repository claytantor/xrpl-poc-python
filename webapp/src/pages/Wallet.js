import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import Spinner from "../components/Spinner"
import { WalletService } from "../services/WalletService"

import { AiOutlineEye } from "react-icons/ai"
import { SiXrp } from "react-icons/si"

const AccountInfo = ({accountInfo}) => {
    return (
        <div className="mt-2">
            <div className="text-lg">Account Info</div>
            <div className="bg-slate-700 p-1 rounded-md m-2">
                <div className="font-mono mt-2">
                    <pre className="text-pink-300 text-xs">
                    {JSON.stringify(accountInfo, null, 2)}
                    </pre>
                </div>
                </div>
        </div>
    )
};


const Wallet = ({useStore}) => {

    let [walletInfo, setWalletInfo] = useState(null);

    let dropsToXrp = (drops) => {
        return (drops / 1000000).toFixed(2);
    };

    useEffect(() => {
        if (!walletInfo) {
            WalletService.getWallet().then(r => {
                console.log(r.data);
                setWalletInfo(r.data);
            }).catch(error => {
                console.log(error)
            }).finally(() => {
                // console.log("finally")
            });
        }
    } , [])


    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-4"> 
                <h2 className="text-2xl">Wallet</h2>
                {walletInfo ? <div className="flex flex-col">
                    <div className="flex flex-row justify-between">
                        <div className="grow flex">
                            <button className="text-lg font-mono underline hover:text-pink-600 cursor-pointer" onClick={()=>window.location.href=`https://testnet.xrpl.org/accounts/${walletInfo.classic_address}`}>{walletInfo.classic_address}</button></div>
                            <div className="shrink text-3xl font-mono font-bold text-pink-600 flex link-align-center">{dropsToXrp(parseInt(walletInfo.account_info.account_data.Balance))} <SiXrp className="ml-1"/></div>
                    </div>
                    <div className="break-words flex-col flex mt-2">
                        <div className="text-sm">Public Key</div>
                        <div className="font-mono text-pink-900">{walletInfo.public_key}</div>
                    </div>
                    <AccountInfo accountInfo={walletInfo.account_info.account_data}/> 

                </div> : <Spinner/>}
            </div>
        </Page> 
        </>

    )
}

export default Wallet