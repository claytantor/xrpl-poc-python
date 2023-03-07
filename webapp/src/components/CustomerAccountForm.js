import React, {useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ImageUploading from 'react-images-uploading';
import { CustomerAccountService } from '../services/CustomerAccountService'
import { Alert, Spinner } from './Base'

import { useStore } from '../zstore';


export const DropdownComponent = ({onChange, value, name}) => {

  const handleSelectChange = (e) => {
      console.log("handleSelectChange", e.target.value);
      onChange(e);
  }

  return (
      <div className="relative w-full lg:max-w-sm">
          <select name={name} onChange={handleSelectChange} value={value}
                className="w-full p-2.5 text-gray-500 bg-white border rounded-md shadow-sm outline-none appearance-none focus:border-indigo-600">
              <option value="noop">Nothing</option>
              <option value="carry">Carry On Sign</option>
              <option value="ship1">Basic Customer Shipping</option>
          </select>
      </div>
  );
}

const CustomerAccountForm = ({ customerAccount, formType }) => {

  const userCurrency = useStore(state => state.userCurrency);

  const maxNumber = 1;

  const navigate = useNavigate();

  const [formState, setFormState] = useState(customerAccount);
  const [images, setImages] = useState([]);
  const [savedStatus, setSavedStatus] = useState("start");
  const [wallet] = useState(null);
  const [errors, setErrors] = useState([]);


  // const xformState = (customerAccount) => {
  //   const returnedTarget = Object.assign({}, customerAccount.inventory_item);
  //   returnedTarget.id = customerAccount.id;
  //   returnedTarget.is_xurl_item = customerAccount.is_xurl_item;
  //   returnedTarget.fiat_i8n_price = parseFloat(customerAccount.fiat_i8n_price);
  //   returnedTarget.fiat_i8n_currency = customerAccount.fiat_i8n_currency.toUpperCase();
  //   returnedTarget.verb = customerAccount.verb;
  //   return returnedTarget;
  // }

  useEffect(() => {
    if(formType==='edit' && customerAccount){
      // const returnedTarget = xformState(customerAccount);
      console.log("setting form state", returnedTarget);
      setFormState(returnedTarget);
      if(returnedTarget.images && returnedTarget.images.length>0){
        setImages(returnedTarget.images);
      }
    } else {
      setFormState({
        classic_address: "",
      });
      setErrors([]);
      setSavedStatus("start")
    }
  }, [customerAccount]);

  function isNumber(n) { return /^-?[\d.]+(?:e-?\d+)?$/.test(n); }

  const handleInputChange = event => {
      const target = event.target
      let value = target.value
      const name = target.name
      console.log('handleInputChange', name, value);

      if(name === 'price'){
        value = value.replace(/[^\d.-]/g, '');
      }
  
      setFormState((formState) => ({
        ...formState,
        [name]: value
      }));  
  };  

  const handleChecked = event => {
    const target = event.target
    let value = target.checked
    const name = target.name
    console.log('handleChecked', name, value);

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


    CustomerAccountService.createCustomerAccount(saveObject).then(r=>{
      setSavedStatus("done");
    }).catch(e=>{
      setErrors([{
        "instancePath": "/save",             
        "keyword": "unknown error, try again.",
        "message": "problem saving customerAccount"
      }]);
      setSavedStatus("error");
    });


    // if(isNumber(saveObject.fiat_i8n_price)){
    //   saveObject.fiat_i8n_price = parseFloat(saveObject.fiat_i8n_price);
    //   saveObject.fiat_i8n_currency = userCurrency;
    //   saveObject.verb = formState.verb;
    //   formState.fiat_i8n_price = parseFloat(formState.fiat_i8n_price);
    //   formState.fiat_i8n_currency = userCurrency;

    //   let schemaValid = true;

    //   if (!schemaValid) {
    //     console.log("validation errors:", validate.errors, formState)
    //     let allErrors = [];
    //     allErrors.push(...validate.errors);
    //     setErrors(allErrors);
    //   } else {
    //     if(saveObject.id){
    //       console.log("updating payment item", saveObject);
      
    //       // CustomerAccountService.updateCustomerAccount(saveObject).then(r=>{
    //       //   setSavedStatus("done");
    //       // }).catch(e=>{
    //       //   setErrors([{
    //       //     "instancePath": "/save",             
    //       //     "keyword": "unknown error, try again.",
    //       //     "message": "problem saving customerAccount"
    //       //   }]);
    //       //   setSavedStatus("error");
    //       // });
    
    //     } else {
    //       console.log("creating payment item", saveObject);
    //       CustomerAccountService.createCustomerAccount(saveObject).then(r=>{
    //         setSavedStatus("done");
    //       }).catch(e=>{
    //         setErrors([{
    //           "instancePath": "/save",             
    //           "keyword": "unknown error, try again.",
    //           "message": "problem saving customerAccount"
    //         }]);
    //         setSavedStatus("error");
    //       });
    //     }
    //   }
    // } else {
    //   setErrors([{
    //     "instancePath": "/fiat_i8n_price",              
    //     "keyword": "type price must be a numeric value.",
    //     "message": "problem saving customerAccount"
    //   }]);
    //   setSavedStatus("error");
    // }

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
          <label className='text-gray-600'>Account Address</label>
          <input
            name="classic_address" onChange={handleInputChange} type="text" placeholder="Enter account address" value={formState.classic_address}
            className="px-4 py-2 border-2 border-gray-300 outline-none focus:border-pink-400 rounded"
          />
        </div>

        {/* <div className="w-full">
          <label className="text-gray-600">Description</label>
          <textarea
            name="description"
            value={formState.description}
            onChange={handleInputChange}
            className="w-full h-32 px-4 py-3 border-2 border-gray-300
              rounded outline-none  focus:border-pink-400"
            placeholder="A few sentences about the item"
          ></textarea>
        </div> */}

        {/* <div className='flex flex-row flex-wrap w-full justify-start'>
          <div className='items-center flex flex-row justify-start m-2'>
            {formState.is_xurl_item ? 
              <input checked
              name="is_xurl_item"
              onChange={handleChecked}
              id="default-checkbox" type="checkbox" value={formState.is_xurl_item} className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/> :
              <input
              name="is_xurl_item"
              onChange={handleChecked}
              id="default-checkbox" type="checkbox" value={formState.is_xurl_item} className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>}

            <label className="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Published to xurl</label>
          </div>

          <div className='items-center flex flex-row m-2 w-fit '>
            <label className="ml-4 text-sm font-medium text-gray-900 dark:text-gray-300 w-[160]">Action On Sign</label>
            <DropdownComponent onChange={handleInputChange} value={formState.verb} name="verb"/>
          </div>

          
        </div> */}
{/* 
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
        </div> */}
        {/* <div className='border-2'></div> */}
        <div className='flex flex-row justify-end mt-3'>
          <button className='p-2 rounded bg-pink-200 hover:bg-pink-600' onClick={onSaveButton}>Save Customer Account</button>
        </div>
      </div>  
    </>:
    <>Loading <Spinner animation="border"/></>}
    </>
    
  );
};


export default CustomerAccountForm

