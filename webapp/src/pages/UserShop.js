import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import {BsShop} from "react-icons/bs";
import Page from "../components/Page";
import XummQrCode from "../components/XummQrCode";
import {ShopPaymentItemList} from "../components/PaymentItemList";
import { useStore } from "../zstore"
import XurlService from "../services/XurlService";
import { xurlBaseUrl } from "../env";


const CreateCustomerAccountModal = ({ xummState, showModal, setShowModal, shop_id}) => {

  const xumm_url = `https://xumm.app/detect/xapp:sandbox.32849dc99872?uri_base=http://${shop_id}.localhost:5005/xurlapi/xurl&uri=xurl://payload/customeraccount/0/createaccount`;

  return (<>
   {showModal && 
   <>
      <div className="flex justify-center items-start overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
        <div className="relative w-auto my-6 mx-auto max-w-[380]">
          <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
            <div className="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t ">
              <h3 className="text-2xl font=semibold">Create Customer Account for Shop {shop_id}</h3>
            </div>
            <div className="flex flex-row justify-center bg-white w-96 p-3 rounded-b-lg">
                <XummQrCode url={xumm_url} />
            </div>
            <div onClick={()=>setShowModal(false)} className="btn-common">Cancel</div>
          </div>
        </div>
      </div>   
   </>}
  </>);
};


const UserShopCustomer = ({ xummState, shop_id}) => {

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [shopInfo, setShopInfo] = useState(null);
  const [error, setError] = useState(null);
  const [showModalLocal, setShowModalLocal] = useState(false);

  useEffect(() => {
    if (xummState && xummState.me) {
      console.log(`UserShopCustomer useEffect`, xummState.me);
      XurlService.getInfo(xurlBaseUrl(shop_id)).then((response) => {
        console.log(`UserShopCustomer getInfo`, response.data);
        setShopInfo(response.data);
        setIsAuthenticated(true);
      }).catch((error) => {
        console.log(`UserShopCustomer getInfo error`, error);
        setIsAuthenticated(false);
        setError(error);
      });
      
    } else {
      setIsAuthenticated(false);
    }
  }, [xummState]);


  return (
    <div className="flex flex-col justify-center text-center items-center">
      {isAuthenticated ? <div>is authenticated</div> : <div>is not authenticated</div>}
      {shopInfo && shopInfo?.xurl_user ? 
        <div>{shopInfo?.xurl_user} is a customer</div> : 
        <div>
          <div>{xummState?.me?.sub} is not a customer</div>
          {isAuthenticated && <>
          <div className="btn-common" onClick={()=>setShowModalLocal(true)}>Become a customer of {shop_id}</div>
          <CreateCustomerAccountModal xummState={xummState} showModal={showModalLocal} setShowModal={setShowModalLocal} shop_id={shop_id}/>
          </>}
        </div>}
      {error && <>error</>}

    </div>
  );

};

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
            <div className="flex flex-row justify-center">
              <UserShopCustomer xummState={xummState} shop_id={shopid}/>
            </div>
            {/* <div className="mb-3">
              <HelpAlert 
                helpLink='/docs/#/UserShop'>Payment items are "Scan to pay" items that can be used to automatically receive payment with no activity required for the receiver. <strong>Just scan to pay!</strong> Our backend will convert the fiat amount to XRP and send a Payment Tx to your wallet. If you want to use a cart and allow fulfillment via shipping you will need to build a cart.</HelpAlert>
            </div> */}
            <div><ShopPaymentItemList shop_id={shopid}/></div>
            <div className="mt-6">
              <div onClick={()=>window.open(`${xurlBaseUrl(shopid)}/info`,'_blank')} className="link-common">{xurlBaseUrl(shopid)}/info</div>
              {xurlBaseUrl(shopid) && <div className='text-xs'>xurlBaseUrl: {xurlBaseUrl(shopid)}</div>}
            </div>
        </div>
      </div>

    </Page>
  );
};

export default UserShop;
