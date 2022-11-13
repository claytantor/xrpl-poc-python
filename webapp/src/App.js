import React, {useEffect, useState} from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Outlet,
  Navigate,
} from "react-router-dom";


import Home from "./pages/Home"
import ReceivePayment from "./pages/ReceivePayment"
import SendPayment from "./pages/SendPayment";
import Wallet from "./pages/Wallet";
import Login from "./pages/Login";
import {getAccessTokenInfo} from "./services/AuthenticationService";
import {useStore} from "./store";

import "./App.css"



const About = () => <div>About</div>;

const PrivateRoute = () => {
  const xummAuthState = useStore((state) => state.xummState);
  const setXummState = useStore((state) => state.setXummState);
  console.log('PrivateRoute xumm state', xummAuthState);
  if (xummAuthState && xummAuthState.jwt) {
    console.log('PrivateRoute xumm state jwt', xummAuthState.jwt);
    const accessTokenInfo = getAccessTokenInfo(xummAuthState.jwt);
    console.log('PrivateRoute xumm state accessTokenInfo', accessTokenInfo);
    if (accessTokenInfo && accessTokenInfo.active) {
      return <Outlet />;
    } else {
      console.log('PrivateRoute xumm state accessTokenInfo not active');
      setXummState(null);
      return <Navigate to="/login" />;
    }

  } else {
    console.log('PrivateRoute xumm state accessTokenInfo not active');
    setXummState(null);
    return <Navigate to="/login" />;
  }
};


const App = ({timestamp}) => {

  useEffect(() => {
    console.log(`timestamp ${timestamp}`);
  }, [timestamp]);

  return (  
    <>
    <BrowserRouter>
        <Routes>

            {/* <Route exact path="/wallet" element={<PrivateRoute />}>
                <Route exact path="/wallet" element={<Wallet useStore={useStore}/>} />
            </Route>
            <Route exact path="/send" element={<PrivateRoute />}>
                <Route exact path="/send" element={<SendPayment useStore={useStore}/>} />
            </Route>
            <Route exact path="/receive" element={<PrivateRoute />}>
                <Route exact path="/receive" element={<ReceivePayment useStore={useStore}/>} />
            </Route>

            <Route path="/about" element={<About />} />
            <Route path="/create" element={<CreateWallet />} /> */}
            <Route path="/login" element={<Login/>} />
            <Route path="/" element={<Home/>} />
        </Routes>
    </BrowserRouter>
    </>)};

export default App