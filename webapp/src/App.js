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

import "./styles.css";
import "./App.css";

const PrivateRoute = ({xummState}) => {


  console.log("PrivateRoute xumm state", xummState);
  if (xummState && xummState.jwt) {
    console.log("PrivateRoute xumm state jwt", xummState.jwt);
    const accessTokenInfo = AuthenticationService.getAccessTokenInfo(xummState.jwt);
    console.log("PrivateRoute xumm state accessTokenInfo", accessTokenInfo);
    if (accessTokenInfo && accessTokenInfo.active) {
      return <Outlet />;
    } else {
      console.log("PrivateRoute xumm state accessTokenInfo not active");
      // setXummState(null);
      return <Navigate to="/login" />;
    }
  } else {
    console.log("PrivateRoute xumm state accessTokenInfo not active");
    // setXummState(null);
    return <Navigate to="/login" />;
  }
};

const App = () => {
  
  const xumm = new XummPkce(xummConfig["api-key"]);

  const [xummState, setXummState] = useState();

  const xummSignInHandler = (state) => {
    if (state.me) {
      const { sdk, me } = state;
      setXummState({ sdk, me });
      console.log("state", me);
      // Also: sdk » xumm-sdk (npm)
    }
  };

  // To pick up on mobile client redirects:
  xumm.on("retrieved", async () => {
    console.log("Retrieved: from localStorage or mobile browser redirect");
    xummSignInHandler(await xumm.state());
  });


  // xumm.authorize().then((session) => {
  //   xummSignInHandler(session);
  // });


  // xumm.on("success", async () => {
  //     console.log("success");
  //     const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
  //     console.log('Authorized', /* authorized.jwt, */ authorized);
  //     AxiosService.setUser(authorized);
  //     setXummState(authorized);
  // });

  // xumm.on("retrieved", async () => {
  //     console.log("Retrieved: from localStorage or mobile browser redirect")
  //     const authorized = await xumm.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
  //     console.log('Authorized', /* authorized.jwt, */ authorized);
  //     AxiosService.setUser(authorized);
  //     setXummState(authorized);
  // });

  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/wallet" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/wallet"
              element={<Wallet 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/ledger" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/ledger"
              element={<PayloadLedger 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/items" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/items"
              element={<PaymentItems 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/edit/:id" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/item/edit/:id"
              element={<PaymentItemEditor 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/create" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route exact 
              path="/item/create" 
              element={<PaymentItemEditor 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>} />
          </Route>
          <Route exact path="/item/details/:id" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/item/details/:id"
              element={<PaymentItemViewer 
                xumm={xumm} 
                setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/receive" element={<PrivateRoute setXummState={setXummState} xummState={xummState}/>}>
            <Route
              exact
              path="/receive"
              element={<ReceivePayment 
                xumm={xumm} setXummState={setXummState} 
                xummState={xummState}/>}
            />
          </Route>
          <Route path="/xapp" element={<XummApp xumm={xumm} xummState={xummState} setXummState={setXummState}/>} />
          <Route path="/login" element={<Login xumm={xumm} xummState={xummState} setXummState={setXummState} xummSignInHandler={xummSignInHandler}/>} />
          <Route path="/" element={<Home xumm={xumm} xummState={xummState} setXummState={setXummState}/>} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
