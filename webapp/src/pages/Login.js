import React, {useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";

import { XummPkce } from 'xumm-oauth2-pkce';

import Page from "../components/Page"

import { AxiosService } from "../services/AxiosService";
import xummLogo from "../assets/img/xumm_logo.png"
import {useStore} from "../zstore"


const Login = () => {

    const navigate = useNavigate();

    const xumm = new XummPkce('secret');

    const setXummState = useStore((state) => state.setXummState);
    const xummState = useStore((state) => state.xummState);

    let login = () => {
        xumm.authorize()
            .catch(e => console.log('error', e));
    };
    
    xumm.on("error", (error) => {
        console.log("error", error)
    })

    xumm.on("success", async () => {
        console.log("success");
        const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
        console.log('Authorized', /* authorized.jwt, */ authorized);
        if (useStore) {
            console.log('Update use store state', /* authorized.jwt, */ authorized.me)                     
            setXummState({'me':authorized.me,'jwt':authorized.jwt});
            AxiosService.setUser(authorized);
            navigate("/wallet");
        }
    });

    xumm.on("retrieved", async () => {
        console.log("Retrieved: from localStorage or mobile browser redirect")
        const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
        console.log('Authorized', /* authorized.jwt, */ authorized);
        if (useStore) {
            console.log('Update use store state', /* authorized.jwt, */ authorized.me)
            setXummState({'me':authorized.me,'jwt':authorized.jwt});     
            AxiosService.setUser(authorized);    
        }
    });

    return (
        <>
        <Page> 
            <div className="p-4"> 
                <div className="flex flex-row justify-center">
                    {xummState && xummState.me ?<>You are logged in.</>:               
                    <div className="w-64 mt-8">
                        <img src={xummLogo} alt="xummLogo" className="m-5"/>
                        <button className="bg-pink-600 inline-block px-4 py-2 leading-none border rounded-xl text-white border-white hover:border-transparent hover:text-pink-900 hover:bg-pink-400 m-4 text-2xl" onClick={()=>login()}>Login with xumm</button>
                    </div>}
                </div>

            </div>
        </Page> 
        </>

    )
}

export default Login