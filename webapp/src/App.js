import React, {useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, Outlet, Navigate, useNavigate } from "react-router-dom";
import { XummPkce } from 'xumm-oauth2-pkce';


import Home from "./pages/Home";
import Login from "./pages/Login";
import Wallet from "./pages/Wallet";
import XummApp from "./pages/XummApp";
import ReceivePayment from "./pages/ReceivePayment";
import PayloadLedger from "./pages/PayloadLedger";
import PaymentItems from "./pages/PaymentItems";
import PaymentItemViewer from "./pages/PaymentItemViewer";
import PaymentItemEditor from "./pages/PaymentItemEditor";

import { AxiosService } from "./services/AxiosService";
import { AuthenticationService } from "./services/AuthenticationService";

import { xummConfig } from "./env";

import {useStore} from "./zstore";


import "./styles.css";
import "./App.css";


const PrivateRoute = ({xummState, setXummState}) => {


  console.log("PrivateRoute xumm state", xummState);
  if (xummState && xummState.jwt) {
    console.log("PrivateRoute xumm state jwt", xummState.jwt);
    const accessTokenInfo = AuthenticationService.getAccessTokenInfo(xummState.jwt);
    console.log("PrivateRoute xumm state accessTokenInfo", accessTokenInfo);
    if (accessTokenInfo && accessTokenInfo.active) {
      return <Outlet />;
    } else {
      console.log("PrivateRoute xumm state accessTokenInfo not active");
      setXummState(null);
      return <Navigate to="/login" />;
    }
  } else {
    console.log("PrivateRoute xumm state accessTokenInfo not active");
    setXummState(null);
    return <Navigate to="/login" />;
  }
};

const App = () => {
  
  const xumm = new XummPkce(xummConfig["api-key"]);
  // const setXummState = useStore((state) => state.setXummState);

  const [xummState, setXummState] = useState();

  xumm.on("success", async () => {
      console.log("success");
      const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
      console.log('Authorized', /* authorized.jwt, */ authorized);
      AxiosService.setUser(authorized);
      setXummState(authorized);
      // if (useStore) {
      //     console.log('Update use store state', /* authorized.jwt, */ authorized.me)                     
      //     setXummState({'me':authorized.me,'jwt':authorized.jwt});
      //     AxiosService.setUser(authorized);
      //     navigate("/wallet");
      // }
  });

  xumm.on("retrieved", async () => {
      console.log("Retrieved: from localStorage or mobile browser redirect")
      const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
      console.log('Authorized', /* authorized.jwt, */ authorized);
      AxiosService.setUser(authorized);
      setXummState(authorized);
      // if (useStore) {
      //     console.log('Update use store state', /* authorized.jwt, */ authorized.me)
      //     setXummState({'me':authorized.me,'jwt':authorized.jwt});     
      //     AxiosService.setUser(authorized);   
      //     navigate("/wallet"); 
      // }
  });

  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/wallet" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/wallet"
              element={<Wallet xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/ledger" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/ledger"
              element={<PayloadLedger xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/items" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/items"
              element={<PaymentItems xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/edit/:id" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/item/edit/:id"
              element={<PaymentItemEditor xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/create" element={<PrivateRoute xummState={xummState}/>}>
            <Route exact path="/item/create" element={<PaymentItemEditor xummState={xummState}/>} />
          </Route>
          <Route exact path="/item/details/:id" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/item/details/:id"
              element={<PaymentItemViewer xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/receive" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/receive"
              element={<ReceivePayment xummState={xummState}/>}
            />
          </Route>
          <Route path="/xapp" element={<XummApp />} />
          <Route path="/login" element={<Login xumm={xumm} xummState={xummState}/>} />
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
