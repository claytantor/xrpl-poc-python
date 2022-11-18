import React, {useEffect, useState } from "react"


import Page from "../components/Page"

import xummLogo from "../assets/img/xumm_logo.png"


const Login = ({xumm, xummState, setXummState, xummSignInHandler}) => {
   

    let login = () => {
        xumm.authorize().then((session) => {
            xummSignInHandler(session);
         }).catch((err) => {
            console.log("error on authorize",err);
         });        
    };
    
    xumm.on("error", (error) => {
        console.log("error", error)
    })


    return (
        <>
        <Page xumm={xumm} xummState={xummState} setXummState={setXummState}> 
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