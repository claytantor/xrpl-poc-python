import React, {useEffect, useState } from "react"

import Page  from "../components/Page"
import { PayloadService } from "../services/PayloadService"

import { SiXrp } from "react-icons/si"
import {GoLinkExternal} from "react-icons/go"
import {MdNoteAdd} from "react-icons/md"
import {FaMoneyCheck} from "react-icons/fa"
import {FaShoppingBag} from "react-icons/fa"

import { xummConfig } from "../env"


const BasePayload = ({payload}) => {
  return (
    <div key={payload.payload_uuidv4} className="rounded border-0 bg-slate-100 mb-2">
      <div className="flex flex-row mb-2 justify-start w-full bg-slate-200 rounded-t items-center">
          <MdNoteAdd className="ml-2"/>
          <span className="ml-2">{payload.payload_uuidv4}</span>
          <div className="flex flex-row justify-center">
              {!payload.is_signed && <div className="m-1 mr-3 h-6 rounded bg-gray-400 p-1 text-xs font-bold text-white text-center">
                PENDING</div>}
              {payload.is_signed &&  <div className="m-1 mr-3 h-6 rounded bg-green-600 p-1 text-xs font-bold text-white text-center">
                SIGNED</div>}   
          </div>
        </div>
        <div className="font-mono text-xs break-all p-1">
            {JSON.stringify(payload)}
        </div>
      </div>      
  );
};

const PaymentItemPayload = ({payload}) => {
  
  let payloadCustomMeta = JSON.parse(payload.webhook_body.custom_meta.blob.replaceAll("\\",""));
  //"{\"type\": \"payment_item\", \"payment_item_id\": 1, \"xrp_quote\": 0.38509692500000003, \"fiat_i8n_currency\": \"USD\", \"fiat_i8n_price\": 0.15, \"request_hash\": \"Aed73UUPkHNc2G6LjxHKXP\"}",
  let xrpAmount = payloadCustomMeta.fiat_i8n_price/payloadCustomMeta.xrp_quote;
  return (
      <div key={payload.payload_uuidv4} className="rounded border-0 bg-slate-100 mb-2">
        <div className="flex flex-row mb-2 justify-between w-full bg-slate-200 rounded-t">
                  
            <div className="flex items-center p-1">
              <FaShoppingBag className="ml-2"/>
              <span className="ml-2">{payload.payload_uuidv4}</span>
              <div className="flex flex-row justify-center">
                {!payload.is_signed && <div className="m-1 mr-3 h-6 rounded bg-gray-400 p-1 text-xs font-bold text-white text-center">
                  PENDING</div>}
                {payload.is_signed &&  <div className="m-1 mr-3 h-6 rounded bg-green-600 p-1 text-xs font-bold text-white text-center">
                  SIGNED</div>} 
              </div>
              {payload.is_signed && payload.txid && <div className="flex flex-row justify-center text-2xl">
                <GoLinkExternal className="hover:text-pink-600" 
                  onClick={() => {window.location.href = `${xummConfig.xrp_explorer}/transactions/${payload.txid}`}}/>
              </div>}
            </div>
            <div>
                <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2 items-center">
                    {xrpAmount.toLocaleString('fullwide', {maximumFractionDigits:4})} <SiXrp />
                </span>
            </div>
        </div>
        <div className="font-mono text-xs break-all p-1">
          {JSON.stringify(payload)}
        </div>
    </div>
  ) 
};

const PaymentRequestPayload = ({payload}) => {
  // let mockPayload =
  // {
  //   "body": {
  //     "next": {
  //       "always": "https://xumm.app/sign/f3c97ac6-526b-45ab-90c6-328d9dfa03cc"
  //     },
  //     "pushed": false,
  //     "refs": {
  //       "qr_matrix": "https://xumm.app/sign/f3c97ac6-526b-45ab-90c6-328d9dfa03cc_q.json",
  //       "qr_png": "https://xumm.app/sign/f3c97ac6-526b-45ab-90c6-328d9dfa03cc_q.png",
  //       "qr_uri_quality_opts": ["m", "q", "h"],
  //       "websocket_status": "wss://xumm.app/sign/f3c97ac6-526b-45ab-90c6-328d9dfa03cc"
  //     },
  //     "uuid": "f3c97ac6-526b-45ab-90c6-328d9dfa03cc"
  //   },
  //   "created_at": "Tue, 15 Nov 2022 22:06:40 GMT",
  //   "is_signed": true,
  //   "payload_uuidv4": "f3c97ac6-526b-45ab-90c6-328d9dfa03cc",
  //   "txid": "41D38A8FB62663D3E972A0834D89B40967D25D9411D74018F5ED599BAF078657",
  //   "updated_at": "Tue, 15 Nov 2022 22:06:40 GMT",
  //   "webhook_body": {
  //     "custom_meta": {
  //       "blob": "{\"amount\": 1.25, \"amount_drops\": 1250000, \"address\": \"rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y\", \"network_endpoint\": \"https://s.altnet.rippletest.net:51234/\", \"network_type\": \"testnet\", \"memo\": \"its for the kids man 2\", \"request_hash\": \"L3CQhKWChSkEDG9JAnEuDv\"}",
  //       "identifier": "payment_request:TxYBpVLMRQ22",
  //       "instruction": "its for the kids man 2"
  //     },
  //     "meta": {
  //       "application_uuidv4": "1b144141-440b-4fbc-a064-bfd1bdd3b0ce",
  //       "opened_by_deeplink": true,
  //       "payload_uuidv4": "f3c97ac6-526b-45ab-90c6-328d9dfa03cc",
  //       "url": "https://devapi.xurlpay.org/v1/xumm/webhook"
  //     },
  //     "payloadResponse": {
  //       "payload_uuidv4": "f3c97ac6-526b-45ab-90c6-328d9dfa03cc",
  //       "reference_call_uuidv4": "d6fdf336-1cd5-421f-90ab-feb7194ba28c",
  //       "return_url": {
  //         "app": null,
  //         "web": null
  //       },
  //       "signed": true,
  //       "txid": "41D38A8FB62663D3E972A0834D89B40967D25D9411D74018F5ED599BAF078657",
  //       "user_token": true
  //     },
  //     "userToken": {
  //       "token_expiration": 1671142027,
  //       "token_issued": 1668293195,
  //       "user_token": "83234d7d-54d6-4240-89a3-e86cb97603cd"
  //     }
  //   },
  //   "xumm_payload_id": 5
  // }
  let payloadCustomMeta = JSON.parse(payload.webhook_body.custom_meta.blob.replaceAll("\\",""));

  return (
      <div key={payload.payload_uuidv4} className="rounded border-0 bg-slate-100 mb-2">
          <div className="flex flex-row mb-2 justify-between w-full bg-slate-200 rounded-t">
                     
              <div className="flex items-center p-1">
                <FaMoneyCheck className="ml-2"/>
                <span className="ml-2">{payload.payload_uuidv4}</span>
                <div className="flex flex-row justify-center">
                  {!payload.is_signed && <div className="m-1 mr-3 h-6 rounded bg-gray-400 p-1 text-xs font-bold text-white text-center">
                  PENDING</div>}
                  {payload.is_signed &&  <div className="m-1 mr-3 h-6 rounded bg-green-600 p-1 text-xs font-bold text-white text-center">
                    SIGNED</div>} 
                </div>
                {payload.is_signed && payload.txid && <div className="flex flex-row justify-center text-2xl">
                <GoLinkExternal className="hover:text-pink-600" 
                  onClick={() => {window.location.href = `${xummConfig.xrp_explorer}/transactions/${payload.txid}`}}/>
              </div>}
              </div>
              <div>
                  <span className="flex justify-end px-1 py-1 text-2xl font-semibold text-gray-700 mr-1 mb-2 items-center">
                      {payloadCustomMeta.amount.toLocaleString('fullwide', {maximumFractionDigits:4})} <SiXrp />
                  </span>
              </div>
          </div>
          <div className="font-mono text-xs break-all p-1">
            {JSON.stringify(payload)}
          </div>
      </div>
  ) 
};

const PayloadItem = ({payload}) => {
    
    if (payload.webhook_body) {

      switch (payload.webhook_body.custom_meta.identifier.split(":")[0]) {
        case "payment_item":
            return <PaymentItemPayload payload={payload} />
        case "payment_request":
            return <PaymentRequestPayload payload={payload} />
        default:
            return <div>Unknown payload type</div>
      }
    } else {
      return <BasePayload payload={payload} />
    }
 
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
