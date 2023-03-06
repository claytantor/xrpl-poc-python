import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import { FiShoppingCart } from "react-icons/fi";
import {BsShop} from "react-icons/bs";
import Page from "../components/Page";
import { HelpAlert, Badge } from "../components/Base";
import PaymentItemList, {ShopPaymentItemList} from "../components/PaymentItemList";
import { useStore } from "../zstore"

const UserShop = ({ xummState}) => {

  const { shopid } = useParams();

  const navigate = useNavigate();

  const [showModalLocal, setShowModalLocal] = useState(false);

  const paymentItemCart = useStore(state => state.paymentItemCart);
  const getCartSize = useStore(state => state.getCartSize);
  
  return (
    <Page withSidenav={false} 
      xummState={xummState}>
      <div className='p-4 flex flex-row justify-center'>
        <div className="flex flex-col">
            <div className="p-1 flex flex-col justify-center text-center items-center">      
              <div className="flex flex-row justify-center rounded-full bg-pink-100 w-48 h-48 items-center">
                <BsShop className="text-8xl text-pink-700"/>
              </div>  
              <h2 className="text-2xl text-center">{shopid}'s Shop</h2>
            </div>
            {/* <div className="mb-3">
              <HelpAlert 
                helpLink='/docs/#/UserShop'>Payment items are "Scan to pay" items that can be used to automatically receive payment with no activity required for the receiver. <strong>Just scan to pay!</strong> Our backend will convert the fiat amount to XRP and send a Payment Tx to your wallet. If you want to use a cart and allow fulfillment via shipping you will need to build a cart.</HelpAlert>
            </div> */}
            <div><ShopPaymentItemList shop_id={shopid}/></div>
        </div>
      </div>

    </Page>
  );
};

export default UserShop;
