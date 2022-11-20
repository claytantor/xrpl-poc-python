import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import lodash from 'lodash';
import { FiShoppingCart } from "react-icons/fi";

import Page from "../components/Page";
import { Alert, HelpAlert, Badge, Modal } from "../components/Base";
import PaymentItemList from "../components/PaymentItemList";
import { PaymentItemService } from "../services/PaymentItemService";

import { useStore } from "../zstore"

const FileUpload = ({setShowModal}) => {
  const [selectedFile, setSelectedFile] = useState();
	const [isFilePicked, setIsFilePicked] = useState(false);
  const [error, setError] = useState();

	const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsFilePicked(true);
	};

	const handleSubmission = () => {
		const formData = new FormData();

		formData.append('File', selectedFile);
    PaymentItemService.uploadPaymentItemsCSVFile(formData)
      .then((response) => {
        console.log("response", response);
        if (response.status === 200) {
          console.log("File uploaded successfully.");
          setShowModal(false);
          window.location.reload();
        }
      })
      .catch((error) => {
        setError(error.message);
        console.log("error", error);
      });
	};

  return(
    <div>
      { error && <Alert variant="danger">There was a problem attempting to upload paymentItems. {error} please <a href="mailto:support@rapaygo.com">contact support.</a></Alert>}
       <input className="rounded bg-slate-300 p-2" type="file" name="file" onChange={changeHandler} />
       {isFilePicked ? (
         <div>
           <p>Filename: {selectedFile.name}</p>
           <p>Filetype: {selectedFile.type}</p>
           <p>Size in bytes: {selectedFile.size}</p>
           <p>
             lastModifiedDate:{' '}
             {selectedFile.lastModifiedDate.toLocaleDateString()}
           </p>
         </div>
       ) : (
         <p>Select a file to show details</p>
       )}
       <div className="flex flex-row justify-end">
         <button className="btn-common-gray">Cancel</button>
         <button className="btn-common-blue" onClick={handleSubmission}>Submit</button>
       </div>
     </div>
   )
};

const PaymentItemUploadModal = ({showModal, setShowModal}) => {

  return (
    <>
    { showModal && 
      <Modal show={showModal}>
        {/* <Modal.Header>
          <Modal.Title>Upload PaymentItems From CSV</Modal.Title>
        </Modal.Header>

        <Modal.Body>       
          <FileUpload setShowModal={setShowModal}/>
        </Modal.Body> */}

      </Modal> }
    
    </>
  );

};

const PaymentItems = ({ xummState}) => {

  const navigate = useNavigate();

  const [showModalLocal, setShowModalLocal] = useState(false);

  const paymentItemCart = useStore(state => state.paymentItemCart);
  const getCartSize = useStore(state => state.getCartSize);
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className='p-4'>
        <div className="p-1 flex justify-between">        
          <h2 className="text-2xl">Payment Items </h2>
          <div className="flex md:max-h-10">
            
              <>
                <button className="btn-common-pink" onClick={() => navigate('/item/create')}>New Payment Item</button>
                {/* <button className="p-1 rounded bg-blue hover:bg-blue-600 m-1 flex" onClick={() => setShowModalLocal(true)}>Import PaymentItems</button> */}
              </>

            {paymentItemCart.length > 0 && <>
              <button onClick={() => navigate('/cart')} className="p-1 rounded bg-orange hover:bg-orange-600 m-1 flex">PaymentItem Cart <FiShoppingCart className="mr-1"/> <Badge className="text-dark" bg="light">{getCartSize()}</Badge></button>
            </>}
          </div>
        </div>
        {/* <div className="p-1"><FileUpload/></div> */}
        <div className="mb-3">
          <HelpAlert 
            helpLink='/docs/#/paymentItems'>Payment items are your "Scan to pay" items that can be used to automatically receive payment with no activity required for the receiver. You can also use paymentItems to collect "ad hoc" payments using the cart.</HelpAlert>
        </div>
        <div><PaymentItemList/></div>
      </div>
      <div><PaymentItemUploadModal showModal={showModalLocal} setShowModal={setShowModalLocal}/></div>


    </Page>
  );
};

export default PaymentItems;
