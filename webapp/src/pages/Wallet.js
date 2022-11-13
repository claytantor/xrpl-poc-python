import React, {useEffect, useState } from "react"

import Page  from "../components/Page"
import Spinner from "../components/Spinner"
import { WalletService } from "../services/WalletService"


import { SiXrp } from "react-icons/si"
import {BiLinkExternal} from "react-icons/bi"

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


const Wallet = () => {

    let [walletInfo, setWalletInfo] = useState(null);

    let dropsToXrp = (drops) => {
        return (drops / 1000000).toFixed(2);
    };

    useEffect(() => {
        WalletService.getWallet().then((walletInfo) => {
            setWalletInfo(walletInfo.data);
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

    // {
    //     "account_data": {
    //         "Account": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
    //         "Balance": "1164749860",
    //         "Flags": 0,
    //         "LedgerEntryType": "AccountRoot",
    //         "OwnerCount": 0,
    //         "PreviousTxnID": "FE79F77E2E534E447ACEADD5F4F8593F7A7ECC80DC99B034F929FF11E8F78B90",
    //         "PreviousTxnLgrSeq": 32728668,
    //         "Sequence": 30500470,
    //         "index": "65185161A7ACD5512FD5FC9047E057A125699D4FF84CACACF80E476F2EA69E2E"
    //     },
    //     "classic_address": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
    //     "wallet_info": {
    //         "app_name": "dev-xurlpay",
    //         "app_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
    //         "aud": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
    //         "client_id": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
    //         "email": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce+rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y@xumm.me",
    //         "exp": 1668310104,
    //         "iat": 1668223704,
    //         "iss": "https://oauth2.xumm.app",
    //         "network_endpoint": "wss://s.altnet.rippletest.net:51233",
    //         "network_type": "TESTNET",
    //         "payload_uuidv4": "a9d8f45a-16ff-48ee-8ef1-163ce3b10f7c",
    //         "scope": "XummPkce",
    //         "sub": "rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y",
    //         "usertoken_uuidv4": "4de21968-8c2f-4fb3-9bb6-94b589a13a8c"
    //     }
    // }

    return (
        <>
        <Page withSidenav={true}> 
            <div className="p-4"> 
                <h2 className="text-2xl">Wallet </h2>
                {walletInfo ? <div className="flex flex-col">
                    <div className="flex flex-col">
                        <span className="w-24 inline-flex justify-center items-center px-2 text-sm font-medium text-gray-800 bg-pink-200 rounded-full dark:bg-gray-700 dark:text-gray-300">{walletInfo.wallet_info.network_type}</span>   
                    </div>
                    <div className="flex md:flex-row justify-between">
                        
                        <div className="grow flex flex-col md:flex-row md:justify-between items-center ">
                            <button className="flex sm:text-sm md:text-lg font-mono underline hover:text-pink-600 cursor-pointer" onClick={()=>window.location.href=`https://testnet.xrpl.org/accounts/${walletInfo.classic_address}`}>{walletInfo.classic_address}<BiLinkExternal className="items-center ml-1 mt-1"/></button>

                            <div className="shrink text-3xl font-mono font-bold text-pink-600 flex link-align-center md:text-right">{dropsToXrp(parseInt(walletInfo.account_data.Balance))} <SiXrp className="ml-1"/></div> 

                        </div>


                    </div>
                    <div className="break-words flex-col flex mt-2">
                        {/* <div className="text-sm">Public Key</div> */}
                        {/* <div className="font-mono text-pink-900">{walletInfo.public_key}</div> */}
                    </div>
                    <AccountInfo accountInfo={walletInfo.account_data}/>  

                </div> : <Spinner/>}
            </div>
        </Page> 
        </>

    )
}

export default Wallet