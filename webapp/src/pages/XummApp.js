import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
const { XummSdkJwt } = require('xumm-sdk')

import Page from "../components/Page";
import { Alert } from "../components/Base";

import { AiOutlineCheckCircle } from "react-icons/ai";
import { whitepaperUrl } from "../env";
import {xummConfig} from "../env"
import xummLogo from "../assets/img/xumm_logo.png"


const XummApp = ({xummState, xAppLoginError}) => {

  const { payloadid } = useParams();

  const [xummPayload, setXummPayload] = useState(null);

  useEffect(() => {
    console.log(`SignPayload useEffect`, payloadid); 
    if (xummState?.sdk?.payload) {
      xummState?.sdk.payload.get(payloadid).then((payload) => {
        console.log(`payload`, payload, xummState?.me);
        setXummPayload(payload);
        xummState?.sdk?.xapp.openSignRequest(payload)       
      }).catch((err) => {
        console.log(`payload error`, err);
      });
    }

  }, [payloadid, xummState?.sdk]);
  

  return (
    <>
      <Page xummState={xummState}>
        <div className="p-4">
          <div className="flex flex-col items-center justify-center w-full">
                <div className="text-4xl font-bold text-pink-800">
                  xurlpay.org xApp
                </div>
          </div>
          {xAppLoginError && <Alert background="bg-red-100" text="text-red-800">{xAppLoginError}</Alert>}
          {payloadid && <div>payloadid: {payloadid}</div>}
          {xummPayload && <div className="flex flex-row justify-start">
            {/* <pre>{JSON.stringify(xummPayload, null, 4)}</pre> */}
            { xummPayload?.payload?.tx_type }
          </div>}    
          {xummState?.me && <div>{xummState?.me?.scope}</div>}
          {xummState && <div>
            xummState: {xummState.constructor.name} {typeof(xummState)} 
            <pre>{JSON.stringify(xummState, null, 4)}</pre>
            </div>}

        </div>
      </Page>
    </>
  );
};

export default XummApp;
