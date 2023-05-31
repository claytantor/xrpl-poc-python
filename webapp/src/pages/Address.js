import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import Page from "../components/Page";
import AddressForm from "../components/AddressForm";
import { useStore } from "../zstore"
import { AddressService } from "../services/AddressService";
import { PostalAddressService } from "../services/PostalAddressService";
import { CustomerAccountService } from "../services/CustomerAccountService";

import XummQrCode from "../components/XummQrCode";


const PostalNftApproveModal = ({postalAddress}) => {

  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <div className="flex flex-row">
        <div className="btn-common" onClick={()=>setShowModal(true)}>Approve NFT</div>
      </div>
      {showModal && postalAddress && (
        
        <div className="justify-center items-top flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none bg-black/50">
          <div className="relative w-auto my-6 mx-auto max-w-3xl">
            {/*content*/}
            <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
              {/*header*/}
              <div className="flex flex-row justify-between p-2 border-b border-solid border-blueGray-200 rounded-t">
                <h3 className="text-2xl font-semibold">
                  Approve Sharing of Postal Address with Shop {postalAddress.shop_id}
                </h3>
              </div>
              {/*body*/}
              <div className="relative p-2 flex-auto">
                <div className="m-1 p-2 rounded-lg text-cyan-700 bg-cyan-200 border-2 border-cyan-700">
                  By approving this transaction in xumm you will be sharing your shipping information with the shop in an encrypted format. To withdraw access to this information burn the associated NFT.

                </div>
                <div className="text-xs">{JSON.stringify(postalAddress)}</div>
                <XummQrCode url={postalAddress.xumm_url} /> 
              </div>
              {/*footer*/}
              <div className="flex items-center justify-end p-2 border-t border-solid border-blueGray-200 rounded-b">
                <button
                  className="btn-common"
                  type="button"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                {/* <button
                  className="btn-common-pink"
                  type="button"
                  onClick={()=>{}}
                >
                  Approve
                </button> */}
              </div>
            </div>
          </div>
        </div>
      )}        
    </>
  );  

};

const PostalAddressList = ({addressItems}) => {
  
  const listItems = addressItems.map((address) => (
      <div onClick={() => {}} 
          className="flex flex-row w-full my-2 p-1 rounded bg-slate-300 justify-between" key={address.id}>  
          <div className="w-fit">           
            <span className="ml-1 mr-3 font-bold">{address.shop_id}</span>
            <span className="mr-1">{address.status}</span>
          </div>
          <div className="w-fit">

            {address.status === 'CREATED' && 
              <>
              {/* {JSON.stringify(address)} */}
              <PostalNftApproveModal postalAddress={address}/>
              </>
              }
          </div>          
      </div>    
  ));

  return (<>

      <div>
          
          {addressItems.length>0 ? 
              <div className='flex flex-col w-full'>
                  <div className='flex flex-col w-full'>{listItems}</div>
              </div>
          : 
              <div>No Shop Postal Addresses</div>}
      </div>

  </>);
};

const SellersListDropdown = ({ shops, selection, setSelection }) => {

  const [open, setOpen] = useState(false);

  useEffect(() => {
    console.log("shops", shops);
  }, [open]);

  const setSelect = (e) => {
    e.preventDefault();
    // console.log(e);
    console.log("_selected", e.target.dataset.selection);
    setSelection(e.target.dataset.selection);   
    // setSelected(e.target.dataset.selection);
    setOpen(!open);
  };

  const handleClick = (e) => {
    e.preventDefault();
    // console.log("handleClick");
    // selection && setSelected(selection);
    // console.log(e);
    setOpen(!open);
  };

  return (
    <div className="mt-2 dropdown bg-slate-200 flex flex-row justify-start w-[170]">
      <button className="bg-slate-200 rounded p-2" onClick={handleClick}>
        {selection ? <>{selection}</>:<>Select Seller</>} 
        <span className="caret"></span>
      </button>
      <ul className="dropdown-menu">
        {shops.map((shop, index) => (
          <li key={shop.shop_id} onClick={setSelect} data-selection={shop.shop_id} 
            className="p-2 hover:bg-pink-100 flex flex-row text-left">
            <span className="m-2">{shop.shop_id}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};


const Address = ({xummState}) => {

  const { id } = useParams();

  const [showModal, setShowModal] = useState(false);
  const [address, setAddress] = useState();
  const [currentPage, setCurrentPage] = useState({page:1, page_size:5});
  const [customerShops, setCustomerShops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('view');
  const [selection, setSelection] = useState();
  const [postalAddress, setPostalAddress] = useState();

  const shop_id = useStore(state => state.shop_id);

  let fetchCustomerShops = () => {
    setLoading(true);
    CustomerAccountService.getCustomerShops().then(res => {
        setCustomerShops(res.data);
        setLoading(false);
    }).catch(err => {      
        console.error(err);
    });       
  };

  useEffect(() => {
    fetchAddress(id);
    fetchCustomerShops();
  },[id]);

  let fetchAddress = (id) => {
      setLoading(true);
      AddressService.getById(id).then(res => {
          setAddress(res.data);
          setLoading(false);
      }).catch(err => {      
          console.error(err);
      });       
  };
  
  const handleSubmit = (formData) => {
        console.log(formData);
        setShowModal(false);
        AddressService.createAddressItem(formData).then((res) => {
            console.log(res);
        }).catch((err) => {
            console.log(err);
        });
  };

  const handleShare = (selectedValue) => {
    console.log("share", selectedValue);
    // const pa_data ={
    //   address_id: address.id,
    //   shop_id: selectedValue
    // };
    PostalAddressService.createAddressItem(address.id, selectedValue).then((res) => {
      console.log("postal address",res.data);
      setPostalAddress(res.data);
    }).catch((err) => {
      console.log(err);
    });
    setMode('view');
  };

  const handleCancel = () => {
    console.log('cancel');
    setMode('view');
  };
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className='p-4 flex flex-col w-full'>
        <div className="p-1 flex justify-between">        
          <h2 className="text-3xl">Address</h2>
          {/* <div className="btn-common">Edit</div> */}
        </div> 
        {mode === 'view' && address && 
          <>   
          <div className="flex flex-col w-full bg-slate-100 rounded p-2">
            <div className="flex flex-row justify-between">
              <div className="text-2xl">{address.name}</div>
              <button className="btn-common-pink" onClick={() => setMode('edit')}>Edit</button>

            </div>
            <div className="text-xs">
              <pre>{JSON.stringify(address, null,4)}</pre>
            </div>
            <div className="flex flex-row justify-start">
              <div className="flex flex-row w-fit">
                <SellersListDropdown shops={customerShops} selection={selection} setSelection={setSelection}/>
                { selection && <button className="btn-common-pink" onClick={() => handleShare(selection)}>Share With Seller</button>}      
              </div>                  
            </div> 
                       
          </div>
          <div>
            <div className="text-2xl">Shop Postal Addresses</div>
            <PostalAddressList addressItems={address.postal_addresses}/>
          </div>
          </>
        }



        {mode === 'edit' && address &&
          <div className="flex flex-col w-full bg-slate-100 rounded p-2">
            <AddressForm address={address} handleSubmit={handleSubmit} handleCancel={handleCancel}/>
          </div>
        }
      </div>
    </Page>
  );
};

export default Address;
