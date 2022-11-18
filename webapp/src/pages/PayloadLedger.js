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

  // useEffect(() => {
  //   console.log(payload, xummConfig);
  // }, [payload]);
  
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
                  onClick={() => {window.location.href = `${xummConfig.xrp_endpoint_explorer}/transactions/${payload.txid}`}}/>
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
                  onClick={() => {window.location.href = `${xummConfig.xrp_endpoint_explorer}/transactions/${payload.txid}`}}/>
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
