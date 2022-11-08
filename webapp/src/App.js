import React, {useEffect, useState} from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Outlet,
  Navigate,
} from "react-router-dom";

import create from "zustand";
import { persist } from "zustand/middleware";

import Home from "./pages/Home"
import ReceivePayment from "./pages/ReceivePayment"
import SendPayment from "./pages/SendPayment";
import Wallet from "./pages/Wallet";
import CreateWallet from "./pages/CreateWallet";
import Login from "./pages/Login";
import {getAccessTokenInfo, getUser} from "./services/AuthenticationService";
import {XummService} from "./services/XummService";


import "./App.css"


const useStore = create(
    persist(
      (set, get) => ({
        isLoading: false,
        appDetails: {},
        setIsLoading: (isLoading) => set({ isLoading: isLoading }),
        getIsLoading: () => get({ isLoading }),
        getXummAppDetails: () => get({ 'foo':'bar' }),
        setXummAppDetails: (appDetails) => set({
          appDetails: appDetails
        }),
      }),
      {
        name: "xurlpay-storage", // unique name
        getStorage: () => localStorage, // (optional) by default, 'localStorage' is used
      }
    )
  );

const About = () => <div>About</div>;

const PrivateRoute = () => {
  const [tokenInfo] = useState(getAccessTokenInfo(getUser()));
  return tokenInfo.active ? <Outlet /> : <Navigate to="/" />;
};


const App = () => {
  useEffect(() => {
    XummService.ping().then((response) => {
      useStore.getState().setXummAppDetails(response.data);
    });    
    
  }, []);

  return (  
    <>
    <BrowserRouter>
        <Routes>

            <Route exact path="/wallet" element={<PrivateRoute />}>
                <Route exact path="/wallet" element={<Wallet useStore={useStore}/>} />
            </Route>
            <Route exact path="/send" element={<PrivateRoute />}>
                <Route exact path="/send" element={<SendPayment useStore={useStore}/>} />
            </Route>
            <Route exact path="/receive" element={<PrivateRoute />}>
                <Route exact path="/receive" element={<ReceivePayment useStore={useStore}/>} />
            </Route>

            <Route path="/about" element={<About />} />
            <Route path="/create" element={<CreateWallet />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Home />} />
        </Routes>
    </BrowserRouter>
    </>)};

export default App