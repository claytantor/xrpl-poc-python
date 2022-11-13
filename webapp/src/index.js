import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
const isStrict = false;

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <>
        {isStrict ? 
        <React.StrictMode>
          <App />
        </React.StrictMode>:
        <App />
        }
    </>

);


  