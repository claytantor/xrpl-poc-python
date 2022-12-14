import React, {useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ImageUploading from 'react-images-uploading';
import { PaymentItemService } from '../services/PaymentItemService'
import { Alert, Spinner } from './Base'

import { useStore } from '../zstore';

const PaymentItemForm = ({ paymentItem, formType }) => {

  const userCurrency = useStore(state => state.userCurrency);

  const maxNumber = 1;

  const navigate = useNavigate();

  const [formState, setFormState] = useState(paymentItem);
  const [images, setImages] = useState([]);
  const [savedStatus, setSavedStatus] = useState("start");
  const [wallet] = useState(null);
  const [errors, setErrors] = useState([]);


  useEffect(() => {
    if(formType==='edit' && paymentItem){
      const returnedTarget = Object.assign({}, paymentItem);
      console.log("setting form state", returnedTarget);
      setFormState(returnedTarget);
      if(paymentItem.images && paymentItem.images.length>0){
        setImages(paymentItem.images);
      }
    } else {
      setFormState({
        name: "",
        description: "",
        fiat_i8n_price: 0.00,
        fiat_i8n_currency: userCurrency, 
      });
      setErrors([]);
      setSavedStatus("start")
    }
  }, [paymentItem]);


  function isNumber(n) { return /^-?[\d.]+(?:e-?\d+)?$/.test(n); }

  const handleInputChange = event => {
      const target = event.target
      let value = target.value
      const name = target.name
      console.log(name, value);

      if(name === 'price'){
        value = value.replace(/[^\d.-]/g, '');
      }
  
      setFormState((formState) => ({
        ...formState,
        [name]: value
      }));  
  };  

  const onImagesChange = (imageList, addUpdateIndex) => {
      // data for submit
      console.log("onImagesChange", imageList, addUpdateIndex);
      // if we do this we will allow the new changed 
      // image to be what is used, otherwise the o
      // image will be used
      delete formState.images;
      setImages(imageList);
  };


  const formSchema = {
      type: "object",
      properties: {
          name:           {type: "string", "nullable": false, minLength: 4, maxLength: 64},
          description:    {type: "string", "nullable": false, minLength: 4, maxLength: 127},
          fiat_i8n_price:          {type: "number", "nullable": false},
          fiat_i8n_currency:      {type: "string", "nullable": false, minLength: 3, maxLength: 3},
      },
      required: [ "name", "description", "price" ],
      additionalProperties: true
  };

  let renderErrors = (errors) => {
    console.log(errors);
    return errors.map((error, index) => (
        <div key={index}>Invalid {error.instancePath} {error.keyword} {error.message}</div>
    ));
  };

  const onCancel = () => {
    setFormState({
      name: "",
      description: "",
      price: "" 
    });
    setErrors([]);
    navigate("/items");
  };

  const onSaveButton = (e) => {
    e.preventDefault();
    setErrors([]);
    
    console.log("onSaveButton", formState);
    let saveObject = Object.assign({images},formState);
    console.log("saving object", saveObject);


    //set price to number or set errors
    console.log("saving object", saveObject, isNumber(saveObject.fiat_i8n_price));
    if(isNumber(saveObject.fiat_i8n_price)){
      saveObject.fiat_i8n_price = parseFloat(saveObject.fiat_i8n_price);
      saveObject.fiat_i8n_currency = userCurrency;
      formState.fiat_i8n_price = parseFloat(formState.fiat_i8n_price);
      formState.fiat_i8n_currency = userCurrency;

      let schemaValid = true;

      if (!schemaValid) {
        console.log("validation errors:", validate.errors, formState)
        let allErrors = [];
        allErrors.push(...validate.errors);
        setErrors(allErrors);
      } else {
        if(saveObject.payment_item_id){
          console.log("updating payment item", saveObject);
      
          PaymentItemService.updatePaymentItem(saveObject).then(r=>{
            setSavedStatus("done");
          }).catch(e=>{
            setErrors([{
              "instancePath": "/save",             
              "keyword": "unknown error, try again.",
              "message": "problem saving paymentItem"
            }]);
            setSavedStatus("error");
          });
    
        } else {
          console.log("creating payment item", saveObject);
          PaymentItemService.createPaymentItem(saveObject).then(r=>{
            setSavedStatus("done");
          }).catch(e=>{
            setErrors([{
              "instancePath": "/save",             
              "keyword": "unknown error, try again.",
              "message": "problem saving paymentItem"
            }]);
            setSavedStatus("error");
          });
        }
      }
    } else {
      setErrors([{
        "instancePath": "/fiat_i8n_price",              
        "keyword": "type price must be a numeric value.",
        "message": "problem saving paymentItem"
      }]);
      setSavedStatus("error");
    }

  };

  return (

    <>{formState?
    <>
      {/* {formState.id?<>ITEM ID:{formState.id}</>:<></>} */}
      {errors && errors.length>0 && <Alert background="bg-red-200" text="text-red-800">
        <div className="font-bold">Validation Errors Found {renderErrors(errors)}</div>
        </Alert>}
      {savedStatus==="done" && <Alert background="bg-green-200" text="text-green-800">Item successfully saved.</Alert>}
      <div>
        <div className="flex flex-col w-full mt-3 mb-2">
          <label className='text-gray-600'>Item Name</label>
          <input
            name="name" onChange={handleInputChange} type="text" placeholder="Enter descriptive name" value={formState.name}
            className="px-4 py-2 border-2 border-gray-300 outline-none focus:border-pink-400 rounded"
          />
        </div>

        <div className="w-full">
          <label className="text-gray-600">Description</label>
          <textarea
            name="description"
            value={formState.description}
            onChange={handleInputChange}
            className="w-full h-32 px-4 py-3 border-2 border-gray-300
              rounded outline-none  focus:border-pink-400"
            placeholder="A few sentences about the item"
          ></textarea>
        </div>

        <div className="w-full flex flex-row justify-between">
          <div className="flex flex-col w-1/2 mt-3 mb-2">
            <label className='text-gray-600'>Fiat Price ({userCurrency})</label>
            <input
              name="fiat_i8n_price" onChange={handleInputChange} type="text" placeholder={`Enter fiat price in ${userCurrency}`} value={formState.fiat_i8n_price}
              className="px-4 py-2 border-2 border-gray-300 outline-none focus:border-pink-400 rounded"
            />
          </div>
          <div className='w-1/2 flex flex-col justify-start p-2'>
            <label className='text-gray-600'>Images</label>
            <ImageUploading
                    multiple
                    value={images}
                    onChange={onImagesChange}
                    maxNumber={maxNumber}
                    dataURLKey="data_url"
                >
                {({
                    imageList,
                    onImageUpload,
                    onImageRemoveAll,
                    onImageUpdate,
                    onImageRemove,
                    isDragging,
                    dragProps,
                    }) => (
                    // write your building UI
                    <div className="upload__image-wrapper">
                        <div className='w-100 flex mb-2'>
                          <div className='p-1 payment-item-image-drag'
                            style={isDragging ? { color: 'red' } : undefined}
                            onClick={onImageUpload}
                            {...dragProps}
                            >
                            Click or Drop here
                          </div>
                          {' '}
                          <button className='ml-2 p-1 rounded bg-pink-200 hover:bg-pink-600' onClick={onImageRemoveAll}>Remove</button>
                        </div>

                        {imageList.map((image, index) => (
                        <div key={index} className="image-item">
                            <img src={image['data_url']} alt="" width="100" />
                            <div className="image-item__btn-wrapper">
                            </div>
                        </div>
                        ))}
                    </div>
                    )}
                </ImageUploading>

          </div>
        </div>
        <div className='border-2'></div>
        <div className='flex flex-row justify-end mt-3'>
          <button className='p-2 rounded bg-pink-200 hover:bg-pink-600' onClick={onSaveButton}>Save Payment Item</button>
        </div>
      </div>  
    </>:
    <>Loading <Spinner animation="border"/></>}</>
    
  );
};


export default PaymentItemForm

