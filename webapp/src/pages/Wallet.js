import React, {useEffect, useState } from "react"

import Page  from "../components/Page"
import Spinner from "../components/Spinner"
import { WalletService } from "../services/WalletService"


import { SiXrp } from "react-icons/si"
import {BiLinkExternal} from "react-icons/bi"

import {xummConfig} from "../env"

const AccountInfo = ({accountInfo}) => {
    return (
        <div className="mt-2">
            <div className="text-lg">Account Info (JSON)</div>
            <div className="bg-slate-700 p-1 rounded-md m-2">
                <div className="font-mono mt-2">
                    <div className="text-pink-300 text-xs break-words">
                    <pre>{JSON.stringify(accountInfo, null, 2)}</pre>
                    </div>
                </div>
                </div>
        </div>
    )
};


const Wallet = ({xummState}) => {

    let [walletInfo, setWalletInfo] = useState(null);
    let [xrpPrice, setXrpPrice] = useState(null);

    let dropsToXrp = (drops) => {
        return (drops / 1000000).toFixed(2);
    };

    let fiatAmount = (drops) => {
        return (dropsToXrp(drops) * xrpPrice).toFixed(2);
    };

    useEffect(() => {
        WalletService.getWallet().then((walletInfo) => {
            setWalletInfo(walletInfo.data);
            WalletService.getXrpPrice(walletInfo.data.wallet_info.fiat_i8n_currency).then((xrpPrice) => {
                setXrpPrice(xrpPrice.data.price);
            });
        }).catch((error) => {
            console.log("error", error, error.code, error.message, error.response.status);
            if(error.response && error.response.status === 404) {
                console.log("creating wallet not found");
                WalletService.create().then((walletInfo) => {
                    setWalletInfo(walletInfo.data);
                }).catch((error) => {
                    console.log("error", error, error.code, error.message, error.response.status);
                });
            }
        });
    }, []);

    

    return (
        <>
        <Page withSidenav={true} 
            xummState={xummState}> 
            <div className="p-4"> 
                <h2 className="text-2xl">Wallet </h2>
                {walletInfo ? <div className="flex flex-col">
                    <div className="flex flex-col">
                        <span className="w-24 inline-flex justify-center items-center 
                        px-2 text-sm font-medium text-gray-800 bg-pink-200 
                        rounded-full dark:bg-gray-700 dark:text-gray-300">
                            {walletInfo.wallet_user_info.network_type}</span>   
                    </div>
                    <div className="flex md:flex-row justify-between">
                        
                        <div className="grow flex flex-col md:flex-row 
                        md:justify-between items-center ">
                            <button className="flex sm:text-sm md:text-lg 
                            font-mono underline hover:text-pink-600 cursor-pointer" 
                            onClick={()=>window.location.href=`${xummConfig.xrp_endpoint_explorer}/accounts/${walletInfo.classic_address}`}>
                                {walletInfo.classic_address}<BiLinkExternal className="items-center ml-1 mt-1"/></button>

                            <div className="shrink text-3xl font-mono font-bold text-pink-600 flex link-align-center md:text-right">{dropsToXrp(parseInt(walletInfo.account_data.Balance))} <SiXrp className="ml-1"/></div> 

                        </div>


                    </div>
                    {xrpPrice && 
                        <div className="rounded break-words flex-row flex mt-2 w-full justify-end">
                        <div className="font-mono text-pink-900">{fiatAmount(parseInt(walletInfo.account_data.Balance))} {walletInfo.wallet_info.fiat_i8n_currency}</div>
                    </div>}
                    <AccountInfo accountInfo={walletInfo.account_data}/>  

                </div> : <Spinner/>}
            </div>
        </Page> 
        </>

    )
}

export default Wallet