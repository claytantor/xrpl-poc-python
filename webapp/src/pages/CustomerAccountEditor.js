import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from 'react-router-dom';

import Page from "../components/Page";

// import { CustomerAccountService } from '../services/CustomerAccountService'
import CustomerAccountForm from "../components/CustomerAccountForm";



const CustomerAccountEditor = ({xummState}) => {

  const { id } = useParams();

  const { pathname } = useLocation();
  const [customerAccount, setCustomerAccount] = useState();
  const [editFormType, setEditFormType] = useState("create");

  useEffect(() => {
    // console.log("payment item id", pathname.replace("/item/create", "create"));
    let pathCreate = pathname.replace("/customer/create", "create");
    let pathEdit = pathname.replace("/customer/edit/", "");
    console.log("pathname", pathname, pathCreate, pathEdit);
    
    if (pathCreate === "create") {
      setEditFormType("Create");
    } else {
      // setCustomerAccountId(parseInt(pathname.replace("/item/edit/", "")));
      console.log("payment item id", id);
      setEditFormType("Edit");
      CustomerAccountService.getById(id).then(r => {
        setCustomerAccount(r.data);
      });
    
    }
      
  }, [id]); 
  
  return (
    <Page withSidenav={true} 
      xummState={xummState}>
      <div className="p-4">
        <div className="row">
          {/* <Breadcrumb>
            <Breadcrumb.Item href="#" onClick={()=>navigate("/items")}>CustomerAccounts</Breadcrumb.Item>
            <Breadcrumb.Item active>{editFormType} Payment Item</Breadcrumb.Item>
          </Breadcrumb> */}
          <h2 className="text-2xl">{editFormType} Customer Account</h2>
          {(customerAccount && editFormType === 'Edit') && 
          <CustomerAccountForm customerAccount={customerAccount} formType={editFormType.toLowerCase()}/>}          
          {(editFormType === 'Create') && 
          <CustomerAccountForm formType={editFormType.toLowerCase()}/>}        
        </div>
      </div>

    </Page>
  );
};

export default CustomerAccountEditor;