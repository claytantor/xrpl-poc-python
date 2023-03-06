import React, {useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, Outlet, Navigate, useNavigate } from "react-router-dom";


import Home from "./pages/Home";
import Wallet from "./pages/Wallet";
import XummApp from "./pages/XummApp";
import ReceivePayment from "./pages/ReceivePayment";
import PayloadLedger from "./pages/PayloadLedger";
import PaymentItems from "./pages/PaymentItems";
import PaymentItemViewer from "./pages/PaymentItemViewer";
import ShopItemViewer from "./pages/ShopItemViewer";
import PaymentItemEditor from "./pages/PaymentItemEditor";

import { AxiosService } from "./services/AxiosService";
import { AuthenticationService } from "./services/AuthenticationService";
import { XummService } from "./services/XummService";


import { xummConfig } from "./env";

import "./styles.css";
import "./App.css";

var sBrowser, sUsrAg = navigator.userAgent;

import { XummPkce } from 'xumm-oauth2-pkce';
import UserSettings from "./pages/UserSettings";
import UserShop from "./pages/UserShop";
const xummPkce = new XummPkce(xummConfig["api-key"]);

const { XummSdkJwt } = require('xumm-sdk')
const url = new URL(window.location.href);
const xAppToken = url.searchParams.get("xAppToken") || '';
const xummSdkJwt = new XummSdkJwt(xummConfig["api-key"], xAppToken);


const getSdkJwtStorage = () => {
  const ls_sdk = localStorage.getItem('XummSdkJwt');
  if (ls_sdk) {
    const sdk = JSON.parse(ls_sdk.substring("121f6616-f25d-45fc-a258-b5bac5b03609:".length, ls_sdk.length));
    console.log("getSdkJwtStorage", sdk);
    return sdk;
  } else {
    return null;
  }
};


const PrivateRoute = ({xummState}) => {

  const [xummPkceJwt, setXummPkceJwt] = useState(
    JSON.parse(localStorage.getItem('XummPkceJwt')) || false
  );
  const [xummSdkJwt, setXummSdkJwt] = useState(
    getSdkJwtStorage() || false
  );

  const xummSignInHandler = (jwt, sdk) => {
    const accessTokenInfo = AuthenticationService.getAccessTokenInfo(jwt);
    const _xummState = {
      jwt: jwt,
      me: accessTokenInfo.payload,
      sdk: sdk
    }
    AxiosService.setUser(_xummState);
  };
  

  console.log("PrivateRoute", xummPkceJwt, xummSdkJwt);
  if (xummSdkJwt.jwt) {
    xummSignInHandler(xummSdkJwt.jwt, null);
    return <Outlet />;
  } else if (xummPkceJwt.jwt) {
    xummSignInHandler(xummPkceJwt.jwt, null);
    return <Outlet />;
  } else { 
    console.log("PrivateRoute xumm state accessTokenInfo not active");
    // setXummState(null);
    return <Navigate to="/" />;
  }
};

const App = () => {

  
  const [xAppLoginError, setXAppLoginError] = useState();
  const [xummState, setXummState] = useState();

  const [xummSdkJwt, setXummSdkJwt] = useState(
    getSdkJwtStorage() || false
  );

  const [xummPkceJwt, setXummPkceJwt] = useState(
    JSON.parse(localStorage.getItem('XummPkceJwt')) || false
  );


  useEffect(() => {

    //normalize state
    if (sUsrAg.indexOf("xumm") > -1){
      sBrowser = "xumm";
      console.log("xumm detected");

      if (!xummSdkJwt) {
        XummService.authorize(xummConfig["api-key"], xAppToken).then((response) => {
          console.log("XummService.authorize response", response.data);
          xummSignInHandler(response.data.jwt, xummSdkJwt);

        }).catch((error) => {
          setXummState({jwt: 'none'});
          setXAppLoginError(`JWT ERROR api-key:${xummConfig["api-key"]} authToken:${xAppToken} ${JSON.stringify(error)}`);
        });
      } else {
        xummSignInHandler(xummSdkJwt.jwt, xummSdkJwt);
        // setXAppLoginError(`JWT Found ${JSON.stringify(xummSdkJwt)}`);

      }

      xummPkce.on("retrieved", async () => {
        setXAppLoginError("Retrieved: from localStorage or mobile browser redirect")
        const authorized = await xummPkce.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
        // console.log('Authorized', /* authorized.jwt, */ authorized);
        xummSignInHandler(authorized.jwt, authorized.sdk);
      });

    } else {
      console.log("Not xumm");
      if (xummPkceJwt.jwt) {
        xummSignInHandler(xummPkceJwt.jwt, null);
      } else if (xummSdkJwt.jwt) {
        xummSignInHandler(xummSdkJwt.jwt, null);
      } else { 
        console.log("PrivateRoute xumm state accessTokenInfo not active");
        setXummState({sdk:xummPkce, me:null, jwt:null}); //needed to login
      }

      xummPkce.on("success", async () => {
          console.log("success");
          const authorized = await xummPkce.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
          console.log('Authorized', /* authorized.jwt, */ authorized);
          xummSignInHandler(authorized.jwt, authorized.sdk);
      });

      xummPkce.on("retrieved", async () => {
          console.log("Retrieved: from localStorage or mobile browser redirect")
          const authorized = await xummPkce.state() // state.sdk = instance of https://www.npmjs.com/package/xumm-sdk
          console.log('Authorized', /* authorized.jwt, */ authorized);
          xummSignInHandler(authorized.jwt, authorized.sdk);
      });
    }
  }, []);

  const xummSignInHandler = (jwt, sdk) => {
    const accessTokenInfo = AuthenticationService.getAccessTokenInfo(jwt);
    const _xummState = {
      jwt: jwt,
      me: accessTokenInfo.payload,
      sdk: sdk
    }
    setXummState(_xummState);
    AxiosService.setUser(_xummState);
  };
  
  return (
    <>
      {/* <div>browser: {JSON.stringify(sUsrAg)}</div> */}
      <BrowserRouter>
        <Routes>
          <Route exact path="/wallet" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/wallet"
              element={<Wallet 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/ledger" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/ledger"
              element={<PayloadLedger 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/items" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/items"
              element={<PaymentItems 
                xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/edit/:id" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/item/edit/:id"
              element={<PaymentItemEditor 
                xummState={xummState}/>}
            />
          </Route>
          <Route exact path="/item/create" element={<PrivateRoute xummState={xummState}/>}>
            <Route exact 
              path="/item/create" 
              element={<PaymentItemEditor 
                xummState={xummState}/>} />
          </Route>
          <Route exact path="/item/details/:id" element={<PrivateRoute xummState={xummState}/>}>
            <Route
              exact
              path="/item/details/:id"
              element={<PaymentItemViewer 
                xummState={xummState}/>}
            />
          </Route>

          <Route exact path="/receive" element={<PrivateRoute  xummState={xummState}/>}>
            <Route
              exact
              path="/receive"
              element={<ReceivePayment 
                xummState={xummState}/>}
            />
          </Route> 

          <Route exact path="/settings" element={<PrivateRoute  xummState={xummState}/>}>
            <Route
              exact
              path="/settings"
              element={<UserSettings 
                xummState={xummState}/>}
            />
          </Route> 
          <Route path="/shop/:shopid" element={<UserShop xummState={xummState} xAppLoginError={xAppLoginError}/>} />
          <Route path="/shop/details/:shopid/:id" element={<ShopItemViewer xummState={xummState} xAppLoginError={xAppLoginError}/>} />

          <Route path="/xapp" element={<XummApp xummState={xummState} xAppLoginError={xAppLoginError}/>} />         
          <Route path="/" element={<Home xummState={xummState}/>} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
