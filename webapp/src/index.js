import React from "react"
import ReactDOM from "react-dom/client";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import App from "./App"
import Home from "./pages/Home"

import './style.css';


const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// const root = ReactDOM.createRoot(
//   document.getElementById("app")
// );
// root.render(
//     <>Foo
//  <BrowserRouter>
//   <Routes>
//     <Route path="/" element={<App />}>
//       <Route index element={<Home />} />
//     </Route>
//   </Routes>
// </BrowserRouter> 
    
//     </>

// );