import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';

// import Page from "../components/Page";
// // import {HybridPaymentItemDetails} from "../components/PaymentItemDetails"
// import {PaymentItemService} from '../services/PaymentItemService'

// // import { Spinner,  Row, Col, Breadcrumb } from "react-bootstrap";


const PaymentItemViewer = () => {

  // const { pathname } = useLocation();
  // const [paymentItemId] = useState(parseInt(pathname.replace("/item/details/", "")));

  // const navigate = useNavigate();

  // const [paymentItem, setPaymentItem] = useState();

  // useEffect(() => {
  //   console.log("useEffect", paymentItemId)
  //   PaymentItemService.getById(paymentItemId).then(r => {
  //     console.log(r.data);
  //     setPaymentItem(r.data);
  //   });
      
  // }, [paymentItemId]); 
  
  // return (
  //   <Page >
  //     <div className="p-4 flex flex-col">
  //       <div>
  //         {/* <Breadcrumb>
  //           <Breadcrumb.Item href="#" onClick={()=>navigate("/items")}>Payment Item</Breadcrumb.Item>
  //           <Breadcrumb.Item active>View Payment Item</Breadcrumb.Item>
  //         </Breadcrumb> */}
  //       </div>
  //       {/* <div>{ paymentItem ? <HybridPaymentItemDetails paymentItemId={paymentItem.id}/>:
  //         <Spinner animation="border"/> }</div> */}

  //     </div>      
  //   </Page>
  // );

  return (
    <div>PaymentItemViewer</div>
  );
};

export default PaymentItemViewer;