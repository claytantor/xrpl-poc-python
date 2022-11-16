import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import QRCode from "react-qr-code";

import {SiXrp} from "react-icons/si";

import Page from "../components/Page";
import { PaymentItemService } from "../services/PaymentItemService";
import { WalletService } from "../services/WalletService";

import xurlIcon32 from "../assets/favicon_io/favicon-32x32.png";
import xummLogo from "../assets/img/xumm_logo.png"

const PaymentItemViewer = () => {

  const { id } = useParams();

  const navigate = useNavigate();
  const [paymentItem, setPaymentItem] = useState();
  let [xrpPrice, setXrpPrice] = useState(null);
  let [xrpAmount, setXrpAmount] = useState(null);
  let [itemImage, setItemImage] = useState('https://picsum.photos/200/200');



  useEffect(() => {
    console.log("useEffect", id)
    PaymentItemService.getById(id).then(r => {
      let p_i = r.data;
      setPaymentItem(p_i);
      if (p_i.images && p_i.images.length > 0) {
        setItemImage(p_i.images[0]['data_url'])
      }
      WalletService.getXrpPrice(p_i.fiat_i8n_currency).then((xrpPrice) => {
        setXrpPrice(xrpPrice.data.price);
        setXrpAmount((p_i.fiat_i8n_price * xrpPrice.data.price).toFixed(6));
      });
    });
      
  }, [id]); 
  
  return (
    <Page withSidenav={true}>
      <div className='p-4'>
        
        {paymentItem && 
          <div className="w-full">
            <div className='flex flex-row justify-center w-full'>
                
                <div className='rounded bg-slate-200 w-fit p-3'>
                  
                  <div className="m-1 flex flex-row justify-center">
                    <img src={xurlIcon32} className="mr-2"/> <h2 className="text-2xl">SCAN TO PAY</h2>
                  </div>
                  {/* <div className="m-1 flex flex-row justify-center">
                    <img src={xummLogo} className="mr-2 w-32"/>
                  </div> */}
                  <div className="m-1 flex flex-row justify-center">
                    <h2 className="text-2xl break-words w-96 text-center">{paymentItem.name}</h2>
                  </div>
                  <div className="m-1 flex flex-row justify-center w-96 rounded bg-white">
                  <img className="card-img-top w-64" src={itemImage} alt="{paymentItem.name}" />
                  </div>
                  <div className="m-1 flex flex-row justify-center">
                    <span className="text-xs w-96 text-slate-700">{paymentItem.description}</span>
                  </div>
                  <div className="m-1 flex flex-row justify-center">
                    <div className="flex justify-center text-3xl font-bold font-monospace text-pink-700 link-align-center">{parseFloat(paymentItem.fiat_i8n_price)} {paymentItem.fiat_i8n_currency}</div>
                  </div>
                  {/* <div className="m-1 flex flex-row justify-center">
                    <div className="flex justify-center text-xl font-bold font-monospace text-pink-600 link-align-center">EST {parseFloat(xrpAmount)} <SiXrp className="ml-1"/></div>
                  </div> */}

                  <div className="m-1 flex flex-row justify-center bg-white w-96 p-3 rounded-md">
                    <QRCode value={paymentItem.xurl} />
                  </div>
{/* 
                  <div className="m-1 w-96 p-3 rounded bg-slate-700 text-pink-300 font-mono text-xs">
                    {JSON.stringify(paymentItem, null, 2)}
                  </div> */}
                </div>


            </div>
          </div>
        }
      </div>
    </Page>
  );
};

export default PaymentItemViewer;