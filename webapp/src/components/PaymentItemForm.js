// import React, {useState, useEffect } from 'react';
import React, {useState, useEffect } from 'react';
// import Ajv from "ajv";
import { useNavigate } from 'react-router-dom';
// import { createSignal } from "@react-rxjs/utils"
// import { bind } from "@react-rxjs/core"
// import {
//     Button, Form, Spinner, ListGroup, Row, Alert
// } from 'react-bootstrap';
import ImageUploading from 'react-images-uploading';
// import { Trash, Edit } from "react-feather";
import { PaymentItemService } from '../services/PaymentItemService'
import { Alert, Spinner } from './Base'

// const [tagChange$, setTags] = createSignal();
// const [useTags] = bind(tagChange$, []);

// const TagTypeList = ({ typeTags }) => {
//   return (
//     <ListGroup>
//     {typeTags.map((tag, index) => (
//       <ListGroup.Item key={index}>{tag.type} | {tag.name} | {tag.description}</ListGroup.Item>
//       ))}
//     </ListGroup>
//   );

// };

// const ItemTagFormGroup = () => {

//   let tags = useTags();

//   return (
//   <Form.Group>
//     <h4>Payment Item Item Attributes</h4>
//     <TagTypeList typeTags={tags}/>
//     <ItemTagFormControl/>
//   </Form.Group>  
//   );

// };

// const ItemTagFormControl = () => {

//   let tags = useTags();

//   const [formState, setFormState] = useState({
//     name: "",
//     description: "",
//     value: "",
//     price: "",
//     shipping_cost_usps_5:0.0,
//     shipping_cost_ups_3:0.0
//   });


//   const handleInputChange = event => {
//     let target = event.target
//     let value = target.value
//     let name = target.name

//     // if (name === "price") {
//     //   value = value.replace(/\D/g,'');
//     // }

//     setFormState((formState) => ({
//         ...formState,
//         [name]: value
//       }));  
//   };  

//   const addTag = (e) => {
//     let tagsCopy = [...tags];
//     tagsCopy.push({name:formState.name, type:formState.type, description:formState.description});
//     console.log(tagsCopy);
//     setTags(tagsCopy);
//   };

//   return (
//     <div className='mt-3 d-flex'>
//         <Form.Control onChange={(e)=>{handleInputChange(e)}} className='col w-25 m-1' type="text" name="type" placeholder="type of attribute"/>
//         <Form.Control onChange={(e)=>{handleInputChange(e)}} className='col w-25 m-1' type="text" name="name" placeholder="value of attribute"/>
//         <Form.Control onChange={(e)=>{handleInputChange(e)}} className='col w-50 m-1' type="text" name="description" placeholder="longer description"/>
//         <Button variant="primary" onClick={(e)=>{addTag(e)}}>Add Tag</Button>
//     </div>
//   );
// };


// const Spinner = () => {
//   return (
//     <div className="d-flex justify-content-center">
//       <div className="spinner-border" role="status">
//         <span className="sr-only">Loading...</span>
//       </div>
//     </div>
//   );
// };

const PaymentItemForm = ({ paymentItem, formType }) => {

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
        price: "" 
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

      // if(name === 'price' && isNumber(target.value)){
      //   console.log("price is a number A", target.value, value);
      //   value = parseFloat(target.value).toFixed(2);
      //   console.log("price is a number B", target.value, value);
      // } else {
      //   setErrors(['please enter a number for price']);
      // }

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
          price:          {type: "number", "nullable": false},
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
    // formState.price = parseFloat(formState.price);
    console.log("saving object", saveObject);


    //set price to number or set errors
    console.log("saving object", saveObject, isNumber(saveObject.price));
    if(isNumber(saveObject.price)){
      saveObject.price = parseFloat(saveObject.price);
      formState.price = parseFloat(formState.price);
          // setup formats
      // const ajv = new Ajv();
      // const validate = ajv.compile(formSchema); //we dont want to validate the images
      // const schemaValid = validate(formState);

      let schemaValid = true;

      if (!schemaValid) {
        console.log("validation errors:", validate.errors, formState)
        let allErrors = [];
        allErrors.push(...validate.errors);
        setErrors(allErrors);
      } else {
        if(saveObject.id){
      
          PaymentItemService.updatePaymentItem(saveObject).then(r=>{
            // console.log("done", r);
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
        "instancePath": "/price",              
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
      {errors && errors.length>0 && <Alert background="bg-red-200">
        <div className="font-bold">Validation Errors Found {renderErrors(errors)}</div>
        </Alert>}
      {savedStatus==="done" && <Alert variant="green-200">Item successfully saved.</Alert>}
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
            onChange={handleInputChange}
            className="w-full h-32 px-4 py-3 border-2 border-gray-300
              rounded outline-none  focus:border-pink-400"
            placeholder="A few sentences about the item"
          ></textarea>
        </div>

        <div className="w-full flex flex-row justify-between">
          <div className="flex flex-col w-1/2 mt-3 mb-2">
            <label className='text-gray-600'>Fiat Price (USD)</label>
            <input
              name="price" onChange={handleInputChange} type="text" placeholder="Enter fiat price" value={formState.price}
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

