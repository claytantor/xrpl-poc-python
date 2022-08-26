import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import Spinner from "../components/Spinner"
import { WalletService } from "../services/WalletService"

const WalletSecrets = ({walletInfo}) => {
    return (<>  
    
        <div className="m-4 flex border-spacing-2 flex-col rounded-lg border-2 border-dashed border-pink-300 p-4">
            <div className="flex-1 mb-1">
                <h2 className="text-xl">Wallet created. <span className="text-pink-700 font-bold">Save this info now!</span></h2>
            </div>
            <div className="w-fill mb-2 flex flex-col border-b-2">
                <div className="text-sm text-pink-400">classic address</div>
                <div className="mb-2 font-mono">{walletInfo.classic_address}</div>
            </div>
            <div className="w-fill mb-2 flex flex-col border-b-2">
                <div className="text-sm text-pink-400">private key</div>
                <div className="mb-2 font-mono">{walletInfo.private_key}</div>
            </div>
            <div className="w-fill mb-2 flex flex-col border-b-2">
                <div className="text-sm text-pink-400">public key</div>
                <div className="mb-2 font-mono">{walletInfo.public_key}</div>
            </div>
            <div className="w-fill flex flex-col">
                <div className="text-sm text-pink-400">seed</div>
                <div className="mb-2 font-mono">{walletInfo.seed}</div>
            </div>
        </div>    
    
    </>);
};


const CreateWallet = ({useStore}) => {

    let [walletInfo, setWalletInfo] = useState();
    let [loading, setIsLoading] = useState(false);

    let createWallet = () => {
        setIsLoading(true);
        WalletService.create().then(r => {
            setWalletInfo(r.data);
            setIsLoading(false);
        }).catch(error => {
            console.log(error)
            setIsLoading(false);
        }).finally(() => {
            console.log("finally")
        });
        // let wallet = await WalletService.create();
        // setWalletInfo(wallet);
        // setIsLoading(false);
    }

    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-4"> 
                <h2 className="text-2xl">Create Wallet</h2>
                <div className="text-lg mt-2">
                    
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                        <strong className="font-bold">Take Notice!</strong>
                        <span className="block sm:inline"> This action will create a new empty wallet, with a new seed and provide all the secrets needed to login to the site and recover your wallet. You will need to write down the information and keep it in a safe place. No one has the ability to recover information if it is lost.</span>
                    </div>

                    {!walletInfo && <div className="mt-4">
                        <button className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded-xl" onClick={() => {createWallet()}}>Make Wallet</button>
                    </div>}

                    {loading && <div className="mt-3"><Spinner spinnerColor="fill-pink-600"/></div>}
                    {walletInfo && <div className="mt-3">
                        <WalletSecrets walletInfo={walletInfo}/>
                    </div>}

                    {/* <div className="mt-4">Wallet Info</div>
                    <Spinner spinnerColor="fill-pink-600"/> */}


                </div>
            </div>
        </Page> 
        </>

    )
}

export default CreateWallet