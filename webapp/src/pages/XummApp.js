import React, { useState } from "react";

import Page from "../components/Page";
import { AiOutlineCheckCircle } from "react-icons/ai";
import { whitepaperUrl } from "../env";
import {xummConfig} from "../env"


const XummApp = ({xumm, xummState, setXummState}) => {
  return (
    <>
      <Page xumm={xumm} xummState={xummState} setXummState={setXummState}>
        <div className="p-1">
          <div className="p-8 flex-col justify-center overflow-hidden">
            <div className="rounded z-10 relative bg-white px-6 pt-6 pb-6 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-10">
              <div className="mx-auto max-w-md">
                <div className="text-4xl font-bold text-pink-800">
                  xurlpay.org
                </div>
              </div>
            </div>
          </div>
        </div>
      </Page>
    </>
  );
};

export default XummApp;
