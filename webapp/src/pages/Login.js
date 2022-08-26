import React, {useEffect, useState } from "react"
import QRCode from "react-qr-code";

import Page  from "../components/Page"
import LoginForm from "../components/LoginForm";
import { WalletService } from "../services/WalletService"


const Login = ({useStore}) => {

    return (
        <>
        <Page useStore={useStore}> 
            <div className="p-4"> 
                <LoginForm/>
            </div>
        </Page> 
        </>

    )
}

export default Login