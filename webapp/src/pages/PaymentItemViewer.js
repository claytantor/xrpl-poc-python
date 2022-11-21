import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import QRCode from "react-qr-code";

import {IoMdQrScanner} from "react-icons/io";

import Page from "../components/Page";
import XummQrCode from "../components/XummQrCode";
import { PaymentItemService } from "../services/PaymentItemService";
import { WalletService } from "../services/WalletService";

import xurlIcon32 from "../assets/favicon_io/favicon-32x32.png";
import xummLogo from "../assets/img/xumm_logo.png"

import { xummConfig } from "../env";

const PaymentItemViewer = ({xummState}) => {

  const { id } = useParams();

  const [paymentItem, setPaymentItem] = useState();
  let [xrpPrice, setXrpPrice] = useState(null);
  let [xrpAmount, setXrpAmount] = useState(null);
  let [itemImage, setItemImage] = useState('https://picsum.photos/200/200');



  useEffect(() => {
    console.log("useEffect", id)
    PaymentItemService.getById(id).then(r => {
      let p_i = r.data;
      console.log("PaymentItemViewer", p_i);
      setPaymentItem(p_i);
      if (p_i.images && p_i.images.length > 0) {
        setItemImage(p_i.images[0]['data_url'])
      }
      WalletService.getXrpPrice(p_i.fiat_i8n_currency).then((xrpPrice) => {
        // {
        //   "USD": 1,
        //   "XRP": 0.37289,
        //   "__meta": {
        //     "currency": {
        //       "code": "USD",
        //       "en": "US Dollar",
        //       "isoDecimals": 4,
        //       "symbol": "$"
        //     }
        //   }
        // }

        setXrpPrice(xrpPrice.data.XRP);
        setXrpAmount((p_i.fiat_i8n_price * xrpPrice.data.XRP).toFixed(6));
      });
    });
      
  }, [id]); 
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className='p-4'>
        
        {paymentItem && 
          <div className="w-full">
            <div className='flex flex-row justify-center w-full'>
                
                <div className='rounded bg-slate-200 w-fit p-3'>
                  <div className="m-1 flex flex-row justify-center">
                    <img src={xummLogo} className="mr-2 w-32"/><div className="text-slate-900 rounded-lg bg-pink-200 w-fit pr-1 pl-1">{xummConfig.xrp_network}</div>
                  </div>                  
                  <div className="m-1 flex flex-row justify-center">
                    <div className="p-1 font-bold rounded-t-lg bg-black text-white items-center flex flex-row">
                      <IoMdQrScanner className="font-bold mr-1 text-2xl"/>Scan QR Code</div>
                  </div>
                  <div className="m-1 flex flex-row justify-center">
                    <h2 className="text-2xl break-words w-96 text-center">{paymentItem.name}</h2>
                  </div>
                  <div className="m-1 flex flex-row justify-center w-96 rounded p-1">
                    <img className="card-img-top w-64 rounded drop-shadow-xl" src={itemImage} alt="{paymentItem.name}" />
                  </div>
                  <div className="m-1 flex flex-row justify-center">
                    <div className="text-xs w-96 text-slate-700 text-center">{paymentItem.description}</div>
                  </div>
                  <div className="m-1 flex flex-row justify-center">
                    <span className="flex justify-end px-1 py-1 text-3xl font-bold font-monospace text-pink-700 mr-1 mb-2">
                        {Intl.NumberFormat('en-US', { style: 'currency', currency: paymentItem.fiat_i8n_currency }).format(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}
                    </span>

                  </div>
                  <div className="m-1 flex flex-row justify-center bg-white w-96 p-3 rounded-md">
                    <XummQrCode url={paymentItem.xurl} />
                  </div>
                </div>

            </div>
          </div>
        }
      </div>
    </Page>
  );
};

export default PaymentItemViewer;