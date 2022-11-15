import React, {useEffect, useState } from "react"

import Page  from "../components/Page"
import { PayloadService } from "../services/PayloadService"

import { SiXrp } from "react-icons/si"
import {BiLinkExternal} from "react-icons/bi"

const PayloadItem = ({payload}) => {

  // {
  //   "next": {
  //     "always": "https://xumm.app/sign/621688ee-e446-4eff-a6a2-720942aa7e9e"
  //   },
  //   "pushed": false,
  //   "refs": {
  //     "qr_matrix": "https://xumm.app/sign/621688ee-e446-4eff-a6a2-720942aa7e9e_q.json",
  //     "qr_png": "https://xumm.app/sign/621688ee-e446-4eff-a6a2-720942aa7e9e_q.png",
  //     "qr_uri_quality_opts": [
  //       "m",
  //       "q",
  //       "h"
  //     ],
  //     "websocket_status": "wss://xumm.app/sign/621688ee-e446-4eff-a6a2-720942aa7e9e"
  //   },
  //   "uuid": "621688ee-e446-4eff-a6a2-720942aa7e9e"
  // }
    return (
        <div className="payload-item rounded border-0 bg-slate-100 p-2 mb-2">
            <div className="payload-item__icon flex flex-row items-center mb-2">
                <SiXrp /> <span className="ml-2">{payload.payload_uuidv4}</span>
            </div>
            <div className="font-mono text-xs">
              {JSON.stringify(payload)}
            </div>
            <div className="payload-item__content">
                <div className="payload-item__content__title">
                    {payload.payloadType}
                </div>
                <div className="payload-item__content__description">
                    {payload.payloadType}
                </div>
            </div>
        </div>
    ) 
};



const PayloadLedger = () => {

  const [payloads, setPayloads] = useState(null);
  
  useEffect(() => {
    PayloadService.getAll().then((payloads) => {
      setPayloads(payloads.data);
    });
  }, []);

  return (
    <Page withSidenav={true}>
      <div className="p-4">
        <h2 className="text-2xl">Ledger</h2>
        {payloads && payloads.length > 0 && payloads.map((payload) => {
            return <PayloadItem payload={payload} />
        })}
      </div>
    </Page>
  );
};

export default PayloadLedger;
