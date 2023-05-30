import React, { useState, useEffect } from "react";
import { renderMatches, useNavigate, useParams } from 'react-router-dom';
import {BsShop} from "react-icons/bs";
import Page from "../components/Page";
import XummQrCode from "../components/XummQrCode";
import {ShopPaymentItemList} from "../components/PaymentItemList";
import { useStore } from "../zstore"
import XurlService from "../services/XurlService";
import {SimpleLink} from "../components/Base";
import { CustomerAccountService } from "../services/CustomerAccountService";
import { xurlBaseUrl, backendBaseUrl, env } from "../env";

const CustomerPostalAddresses = ({shopInfo}) => {
  return(<div className="flex flex-row justify-center">
    <div className="flex flex-col justify-center p-2">
      <div className="font-bold">Postal Addresses</div>
      <div className="flex flex-row justify-center">
        <div className="m-1 bg-purple-300 rounded text-purple-900 p-1">
          123 Main St
        </div>
      </div>
    </div>
  </div>);
};


const CreateCustomerAccountModal = ({ xummState, showModal, setShowModal, shop_id}) => {

  const [error, setError] = useState();

  //const paragraph = backendBaseUrl();
  const regex = /localhost/g;
  const found = backendBaseUrl.match(regex); 

  const xumm_url = `https://xumm.app/detect/xapp:sandbox.32849dc99872?uri_base=${xurlBaseUrl(shop_id)}/xurlapi/xurl&uri=xurl://payload/customeraccount/0/createaccount`;

  const addLocalhostAccount = () => {
    // console.log("addLocalhostAccount", xummState.me);

    const saveObject = {
      "shop_id": shop_id,
      "classic_address": xummState.me.sub
    }

    console.log("saveObject", saveObject);
        

    CustomerAccountService.createCustomerAccountLocal(saveObject, shop_id).then(r=>{
      setShowModal(false);
    }).catch(e=>{
      setError("Error saving account");
    });

    
  };

  return (<>
   {showModal && 
   <>
      <div className="flex justify-center items-start overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
        <div className="relative w-auto my-6 mx-auto max-w-[380]">
          <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
            <div className="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t ">
              <h3 className="text-2xl font=semibold">Create Customer Account for Shop {shop_id}</h3>
            </div>
            <div className="p-2">
              

              {error ?
                <div className="rounded bg-red-200 text-red-600">
                  <div className="flex flex-row justify-center">
                      <div className="flex flex-col justify-center p-2">
                      ERROR:{error}
                      </div>
                  </div>
              </div>              
              :<div className="rounded bg-cyan-200 text-cyan-600">
                  <div className="flex flex-row justify-center">
                      <div className="flex flex-col justify-center p-2">
                      By creating a customer account you will be able to purchase items from this shop that do not require your shipping address. Only your XRP account id will be stored in the shop database.
                      </div>
                  </div>
              </div>}
            </div>
            {found && found.length > 0 ?
            <div>
              <div className="uppercase">localhost</div>
              <div className="btn-common" onClick={()=>addLocalhostAccount()}>Add Account As Customer</div>
            </div>:
            <div>
              <div className="flex flex-row justify-center bg-white w-96 p-3 rounded-b-lg">
                  <XummQrCode url={xumm_url} />
              </div>
              <div className="p-1 break-words">{xumm_url}</div>
            </div>}
        
            <div onClick={()=>setShowModal(false)} className="btn-common">Cancel</div>
          </div>
        </div>
      </div>   
   </>}
  </>);
};


const CustomerCapabilities = ({verbs}) => {
  return(<div className="flex flex-row justify-center">
  {
    verbs.map((verb, index) => {
      return (<div key={index} className="flex flex-row justify-center">
        <div className="m-1 bg-purple-300 rounded text-purple-900 p-1">
          {verb.type}
        </div>
      </div>);
    })
  }
  </div>);
};

const CapabilitiesDropdown = ({ options, setSelected }) => {
  const [open, setOpen] = useState(false);
  const [dropdownStyle, setDropdownStyle] = useState({});
  const [selection, setSelection] = useState();

  useEffect(() => {
    //style={open ? '' : 'display: none'}
  }, [open]);

  const setSelect = (e) => {
    e.preventDefault();
    // console.log(e);
    console.log("selected", e.target.dataset.selection);
    setSelection(e.target.dataset.selection);
    setSelected(e.target.dataset.selection);
    setOpen(!open);
  };

  const handleClick = (e) => {
    e.preventDefault();
    console.log(e);
    setOpen(!open);
  };

  return (
    <div className="dropdown bg-slate-100 flex flex-row justify-start">
      <button className="bg-slate-100 rounded p-2" onClick={handleClick}>
        {selection ? <>{selection}</>:<>Select Capability</>} 
        <span className="caret"></span>
      </button>
      <ul className="dropdown-menu">
        {options.map((option, index) => (
          <li key={index} onClick={setSelect} data-selection={option} 
            className="p-2 hover:bg-pink-100 flex flex-row text-left">
            <span className="m-2">{option}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};



const CustomerVerbForm = ({shop_id, verbSelected}) => {

  const [form, setForm] = useState({
    name: "",
    address: "",
    city: "",
    state: "",
    zip: "",
    country: "",
    email: "",
    phone: "",
    shop_id: shop_id
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  return(<>
  {verbSelected === "SHIP" && 
  <div className="flex flex-col justify-start">
    <div className="m-1 bg-purple-300 rounded text-purple-900 p-1">
      {verbSelected}
    </div>
    <div className="flex flex-row justify-start w-full p-2">


      <form className="space-y-4 w-full">
        <div className="w-full">
          <label className="block" htmlFor="name">Name</label>
          <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="name" name="name" value={form.name} onChange={handleChange} required />
        </div>

        <div>
          <label className="block" htmlFor="address">Address</label>
          <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="address" name="address" value={form.address} onChange={handleChange} required />
        </div>

        <div>
          <label className="block" htmlFor="city">City</label>
          <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="city" name="city" value={form.city} onChange={handleChange} required />
        </div>

        <div>
          <label className="block" htmlFor="state">State</label>
          <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="state" name="state" value={form.state} onChange={handleChange} required />
        </div>

        <div>
          <label className="block" htmlFor="zip">Zip Code</label>
          <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="zip" name="zip" value={form.zip} onChange={handleChange} required />
        </div>

        <div className="flex flexr-row justify-end">

          <button
            className="text-pink-800 bg-pink-400 font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 rounded hover:bg-pink-200"
                      type="button"
                      onClick={() => handleSubmit()}
                    >
                      Save
          </button>

        </div>
        

      </form>


    </div> 
  </div>
  }
  </>);
};

const AddCustomerCapabilitiesModal = ({showModal, setShowModal}) => {

  const actionName = "Add Customer Capabilities";
  const actionDescription = "add customer capabilities";
  
  const [error, setError] = useState();
  const [verbSelected, setVerbSelected] = useState(null);
  
  const actionCallback = () => {
    setShowModal(false);
  };
  const actionClose = () => {
    setVerbSelected(null);
    setShowModal(false);
  };
  
  return(<>
        <div>
          <div onClick={()=>setShowModal(true)} className="btn-common">Add Customer Capabilities</div>
        </div>
        {showModal && (
        <>
          <div className="flex justify-center items-start overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none bg-slate-900/50">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                <div className="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t ">
                  <h3 className="text-3xl font=semibold">{actionName}</h3>
                </div>
                <div className="relative p-6 flex flex-col justify-start text-left">      
                  {verbSelected ? 
                  <CustomerVerbForm verbSelected={verbSelected}/>: 
                  <>
                    <div>Choose the capability you would like to add to your customer account.</div>
                    <CapabilitiesDropdown options={["NOOP", "CARRY", "SHIP"]} setSelected={setVerbSelected} />
                  </>}
                </div>
                <div className="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
                  <button
                    className="text-slate-800 bg-slate-400 hover:bg-slate-200 font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 rounded"
                    type="button"
                    onClick={() => actionClose()}
                  >
                    Cancel
                  </button>
                  {/* <button
                    className="text-pink-800 bg-pink-400 font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 rounded hover:bg-pink-200"
                    type="button"
                    onClick={() => actionCallback()}
                  >
                    Save
                  </button> */}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
  </>);
};

const UserShopCustomer = ({ xummState, shop_id, shopInfo, setShopInfo}) => {

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // const [shopInfo, setShopInfo] = useState(null);
  const [error, setError] = useState(null);
  const [showModalLocal, setShowModalLocal] = useState(false);
  const [showModalCapabilities, setShowModalCapabilities] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  

  const store_shop_id = useStore(state => state.shop_id);

  useEffect(() => {
    setIsOwner(store_shop_id === shop_id);
    if (xummState && xummState.me) {
      console.log(`UserShopCustomer useEffect`, xummState.me);
      XurlService.setXrpUserAddress(xummState.me.sub);
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
        <>
        {/* <div>{JSON.stringify(shopInfo,null,4)}</div> */}
        {isOwner ? 
          <div>is owner</div> : 
          <div>
              <div>is a customer</div>
              {shopInfo?.xurl_customer && 
              <div className="p-1 bg-slate-100 rounded">
                <div className="font-bold">Customer Capabilities</div>
                <CustomerCapabilities verbs={shopInfo?.xurl_customer?.supported_verbs} />
                {/* <AddCustomerCapabilitiesModal setShowModal={setShowModalCapabilities} showModal={showModalCapabilities} /> */}
              </div>}
          </div>
        }
        
        </> : 
        <div>           
          {!isOwner && <>
            <div>is not a customer</div>
            {isAuthenticated && <>
            <div className="btn-common" 
              onClick={()=>setShowModalLocal(true)}>Become a customer of {shop_id}</div>
            <CreateCustomerAccountModal 
              xummState={xummState} 
              showModal={showModalLocal} 
              setShowModal={setShowModalLocal} 
              shop_id={shop_id}/>
            </>}
          </>}
        </div>}
      {error && <>error</>}

    </div>
  );

};

const UserShop = ({xummState}) => {

  const { shopid } = useParams();

  const [showModalLocal, setShowModalLocal] = useState(false);
  const [shopInfo, setShopInfo] = useState(null);
  const [wellKnown, setWellKnown] = useState(null);

  const paymentItemCart = useStore(state => state.paymentItemCart);
  const getCartSize = useStore(state => state.getCartSize);

  useEffect(() => {
    if(shopInfo?.well_known_domain){

      const scheme = env === 'local' ? 'http' : 'https';

      setWellKnown(`${scheme}://${shopInfo.well_known_domain}/.well-known/xurl-shop-jwks.json?shop_id=${shopInfo.shop_id}`);
    }
  }, [shopInfo]);
  
  return (
    <Page withSidenav={false} 
      xummState={xummState}>
      <div className='p-4 flex flex-row justify-center'>
        <div className="flex flex-col w-full ml-12 mr-12">
            <div className="p-1 flex flex-col justify-center text-center items-center">      
              <div className="flex flex-row justify-center rounded-full bg-pink-100 w-48 h-48 items-center">
                <BsShop className="text-8xl text-pink-700"/>
              </div>  
              <h2 className="text-2xl text-center">{shopid}'s Shop</h2>
            </div>
            <div className="flex flex-row justify-center">
              <UserShopCustomer xummState={xummState} shop_id={shopid} shopInfo={shopInfo} setShopInfo={setShopInfo}/>
            </div>

            <div><ShopPaymentItemList shop_id={shopid} xummState={xummState}/></div>
            {shopInfo && 
            <>
              <div className="flex flex-col w-full items-start">
                <div className="flex flex-row items-center">endpoint: <SimpleLink url={shopInfo.endpoint}/></div>
                <div className="flex flex-row items-center">key: <SimpleLink url={wellKnown}/></div>
                

              </div>
              <div className="flex flex-row w-full p-2 text-xs bg-slate-100 rounded">
                <pre>{JSON.stringify(shopInfo,null,4)}</pre>
              </div>
              <div>
                <CustomerPostalAddresses shopInfo={shopInfo}/>
              </div>
            
            </>}
            
            {/* <div className="mt-6">
              <div onClick={()=>window.open(`${xurlBaseUrl(shopid)}/info`,'_blank')} className="link-common">{xurlBaseUrl(shopid)}/info</div>
              {xurlBaseUrl(shopid) && <div className='text-xs'>xurlBaseUrl: {xurlBaseUrl(shopid)}</div>}
            </div>
            <div>
            http://bd8445ea.localhost:5005/.well-known/xurl-shop-jwks.json?shop_id=bd8445ea
            </div> */}
        </div>
      </div>

    </Page>
  );
};

export default UserShop;
