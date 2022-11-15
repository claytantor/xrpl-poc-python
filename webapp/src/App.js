import React, {useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, Outlet, Navigate } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Wallet from "./pages/Wallet";
import ReceivePayment from "./pages/ReceivePayment";
import PayloadLedger from "./pages/PayloadLedger";
import PaymentItems from "./pages/PaymentItems";
import PaymentItemViewer from "./pages/PaymentItemViewer";
import PaymentItemEditor from "./pages/PaymentItemEditor";

import {AuthenticationService} from "./services/AuthenticationService";

import {useStore} from "./zstore";

import "./styles.css";
import "./App.css";



const PrivateRoute = () => {
  const xummAuthState = useStore((state) => state.xummState);
  const setXummState = useStore((state) => state.setXummState);
  console.log("PrivateRoute xumm state", xummAuthState);
  if (xummAuthState && xummAuthState.jwt) {
    console.log("PrivateRoute xumm state jwt", xummAuthState.jwt);
    const accessTokenInfo = AuthenticationService.getAccessTokenInfo(xummAuthState.jwt);
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
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/wallet" element={<PrivateRoute />}>
            <Route
              exact
              path="/wallet"
              element={<Wallet />}
            />
          </Route>

          <Route exact path="/ledger" element={<PrivateRoute />}>
            <Route
              exact
              path="/ledger"
              element={<PayloadLedger />}
            />
          </Route>

          <Route exact path="/items" element={<PrivateRoute />}>
            <Route
              exact
              path="/items"
              element={<PaymentItems />}
            />
          </Route>
          <Route exact path="/item/edit/:id" element={<PrivateRoute />}>
            <Route
              exact
              path="/item/edit/:id"
              element={<PaymentItemEditor/>}
            />
          </Route>
          <Route exact path="/item/create" element={<PrivateRoute/>}>
            <Route exact path="/item/create" element={<PaymentItemEditor/>} />
          </Route>
          <Route exact path="/item/details/:id" element={<PrivateRoute/>}>
            <Route
              exact
              path="/item/details/:id"
              element={<PaymentItemViewer/>}
            />
          </Route>

          <Route exact path="/receive" element={<PrivateRoute />}>
            <Route
              exact
              path="/receive"
              element={<ReceivePayment />}
            />
          </Route>

          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
