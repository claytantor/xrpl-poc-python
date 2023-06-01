import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';

import Page from "../components/Page";
import { Alert } from "../components/Base";

import { AiOutlineCheckCircle } from "react-icons/ai";
import { whitepaperUrl } from "../env";
import {xummConfig} from "../env"
import xummLogo from "../assets/img/xumm_logo.png"



const XummApp = ({xummState, xAppLoginError}) => {

  const { payloadid } = useParams();

  useEffect(() => {
    console.log(`SignPayload useEffect`, payloadid);
  }, [payloadid]);
  

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

        </div>
      </Page>
    </>
  );
};

export default XummApp;
