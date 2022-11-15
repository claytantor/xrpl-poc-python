import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Page from "../components/Page";

import { PaymentItemService } from "../services/PaymentItemService";

const PaymentItemViewer = () => {

  const { id } = useParams();

  const navigate = useNavigate();
  const [paymentItem, setPaymentItem] = useState();

  useEffect(() => {
    console.log("useEffect", id)
    PaymentItemService.getById(id).then(r => {
      console.log(r.data);
      setPaymentItem(r.data);
    });
      
  }, [id]); 
  
  return (
    <Page withSidenav={true}>
      <div className='p-4'>
        <h2 className="text-2xl">Payment Item</h2>
        {paymentItem && 
          <div className="p-1 rounded bg-slate-700 text-gray-100 font-mono">
            {JSON.stringify(paymentItem, null, 2)}   
          </div>}
      </div>
    </Page>
  );
};

export default PaymentItemViewer;