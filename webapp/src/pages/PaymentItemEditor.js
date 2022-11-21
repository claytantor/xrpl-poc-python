import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from 'react-router-dom';

import Page from "../components/Page";

import { PaymentItemService } from '../services/PaymentItemService'
import PaymentItemForm from "../components/PaymentItemForm";



const PaymentItemEditor = ({xummState}) => {

  const { id } = useParams();

  const { pathname } = useLocation();
  const [paymentItem, setPaymentItem] = useState();
  const [editFormType, setEditFormType] = useState("create");

  useEffect(() => {
    // console.log("payment item id", pathname.replace("/item/create", "create"));
    let pathCreate = pathname.replace("/item/create", "create");
    let pathEdit = pathname.replace("/item/edit/", "");
    console.log("pathname", pathname, pathCreate, pathEdit);
    
    if (pathCreate === "create") {
      setEditFormType("Create");
    } else {
      // setPaymentItemId(parseInt(pathname.replace("/item/edit/", "")));
      console.log("payment item id", id);
      setEditFormType("Edit");
      PaymentItemService.getById(id).then(r => {
        setPaymentItem(r.data);
      });
    
    }
      
  }, [id]); 
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className="p-4">
        <div className="row">
          {/* <Breadcrumb>
            <Breadcrumb.Item href="#" onClick={()=>navigate("/items")}>PaymentItems</Breadcrumb.Item>
            <Breadcrumb.Item active>{editFormType} Payment Item</Breadcrumb.Item>
          </Breadcrumb> */}
          <h2 className="text-2xl">{editFormType} Payment Item</h2>
          {(paymentItem && editFormType === 'Edit') && 
          <PaymentItemForm paymentItem={paymentItem} formType={editFormType.toLowerCase()}/>}          
          {(editFormType === 'Create') && 
          <PaymentItemForm formType={editFormType.toLowerCase()}/>}        
        </div>
      </div>

    </Page>
  );
};

export default PaymentItemEditor;