import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import lodash from 'lodash';
import { FiShoppingCart } from "react-icons/fi";

import Page from "../components/Page";
import { Alert, HelpAlert, Badge, Modal } from "../components/Base";
import AddressList from "../components/AddressList";
import AddressForm from "../components/AddressForm";

import { useStore } from "../zstore"
import { AddressService } from "../services/AddressService";



const AddressModal = ({showModal, setShowModal, handleSubmit}) => {

    const handleCancel = () => {
        setShowModal(false);
    };
    
    return (
        <>
        {showModal && 
            <div className="bg-slate-800/50 flex justify-center items-start overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
                <div className="relative my-6 mx-auto w-[330] md:w-[580]">
                    <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                        <div className="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t ">
                            <h3 className="text-2xl font=semibold">Create Address</h3>
                        </div>
                        <div className="p-2">
                            <AddressForm handleCancel={handleCancel} handleSubmit={handleSubmit}/>
                        </div>
                    </div>
                </div>
            </div>
        }
        </>
    );
};

const Addresses = ({xummState}) => {

  const navigate = useNavigate();

  const [showModal, setShowModal] = useState(false);
  const [addressItems, setAddressItems] = useState([]);
  const [currentPage, setCurrentPage] = useState({page:1, page_size:5});
  const [loading, setLoading] = useState(false);

  const shop_id = useStore(state => state.shop_id);

  useEffect(() => {
    fetchAddressItems(currentPage);
  },[currentPage]);

  let fetchAddressItems = (pageInfo) => {
      setLoading(true);
      AddressService.getAddressItems().then(res => {
          setAddressItems(res.data);
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
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className='p-4'>
        <div className="p-1 flex justify-between">        
          <h2 className="text-2xl">Addresses</h2>
          <div className="flex md:max-h-10">      
            <button className="btn-common-pink" onClick={() =>  setShowModal(true)}>New Address</button>
          </div>
        </div>
        {/* <div className="p-1"><FileUpload/></div> */}
        <div className="mb-3">
          <HelpAlert 
            helpLink='/docs/#/paymentItems'>Addresses allow customers to provide information to sellers on where to ship items.</HelpAlert>
        </div>
        <div className="p-1">
          <AddressList 
            addressItems={addressItems} 
            // setAddressItems={setAddressItems}
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}/>
        </div>
        <div>
            <AddressModal 
              showModal={showModal} 
              setShowModal={setShowModal} 
              handleSubmit={handleSubmit}/>
        </div>
      </div>


    </Page>
  );
};

export default Addresses;
