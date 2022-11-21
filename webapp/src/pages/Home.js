import React, { useState } from "react";

import Page from "../components/Page";
import { AiOutlineCheckCircle } from "react-icons/ai";
import {FiAlertCircle} from "react-icons/fi";

import { Alert } from "../components/Base";
import {xummConfig, deploymentEnv, whitepaperUrl} from "../env"


const Home = ({xummState}) => {

  return (
    <>
      <Page xummState={xummState}>
        <div className="p-4">

          <div className="p-8 flex-col justify-center overflow-hidden">
            <div className="rounded z-10 relative bg-white px-6 pt-6 pb-6 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-10">
              <div className="mx-auto max-w-md">
                <div className="text-4xl font-bold text-pink-800">
                  xurlpay.org
                </div>
                {deploymentEnv === 'local' && 
                <div className="flex flex-row mt-3">
                  <Alert background={"bg-pink-100"} text={"text-pink-800 text-lg font-bold"}>
                    <div className="mr-2">
                      <FiAlertCircle className="text-2xl"/>
                    </div>
                    <div>
                      NOTE: This project is currently in development. If you would like early access please <a href="mailto:claytantor@gmail.com" className="underline">contact us</a>
                    </div>
                  </Alert>
                </div>}
                <div className="divide-y divide-gray-300/50">
                  <div className="space-y-6 py-8 text-base leading-7 text-gray-600">
                    <div>
                      This site is an online proof of concept to show how the{" "}
                      <span className="font-bold text-pink-500">xURL</span>{" "}
                      protocol can be applied to enable numerous payment and
                      point of use sale cases for the XRP ecosystem:
                    </div>
                    <ul className="space-y-4">
                      <li className="flex items-center">
                        <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                        <div className="ml-2 w-11/12">
                          Allows for <a className="underline cursor-pointer" href="https://xumm.readme.io/docs/what-are-xapps" target="_new">xApp </a>deeplink signed payment requests aka. {" "}
                          <span className="font-bold text-pink-500">
                            xURLs
                          </span>{" "}
                          that can guarantee payment to the correct requestor.
                        </div>
                      </li>
                      <li className="flex items-center">
                        <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                        <div className="ml-2 w-11/12">
                          Provides stateful tracking of payment state for
                          payment requests as{" "}
                          <span className="font-bold text-pink-500">xURL</span>{" "}
                          via backend.
                        </div>
                      </li>

                      <li className="flex items-center">
                        <AiOutlineCheckCircle className="text-pink-500 text-6xl w-1/12" />
                        <div className="ml-2 w-11/12">
                          <span className="font-bold text-pink-500">xURL</span>{" "}
                          automation of notifications to externals systems.
                        </div>
                      </li>
                    </ul>
                    <div>
                      This site gives you everything you need to use the
                      proposed protocols on the{" "}
                      <a
                        className="underline"
                        href={xummConfig.xrp_endpoint_explorer}
                        target="_new"
                      >
                        XRP {xummConfig.xrp_network} blockchain
                      </a>
                      . Including xApp xumm wallet integration via OAuth2,{" "}
                      <span className="font-bold text-pink-500">xURL</span>{" "}
                      creation and "Scan To Pay" printable items.
                    </div>
                  </div>
                  <div className="pt-8 text-base font-semibold leading-7">
                    <div className="text-gray-900">
                      Want to dig deeper into the{" "}
                      <span className="font-bold text-pink-500">xURL</span>{" "}
                      protocol specification?
                    </div>
                    <div>
                      <a
                        href={whitepaperUrl}
                        className="text-pink-500 underline hover:text-pink-600"
                      >
                        Read the whitepaper
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Page>
    </>
  );
};

export default Home;
