import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
  Route,
} from "react-router-dom";

import Home from "./pages/Home";
import ErrorPage from "./pages/ErrorPage";
import "./index.css"


const router = createBrowserRouter([

  {
    path: "/",
    element: <Home/>,
    errorElement: <ErrorPage />,
  },
  {
    path: "/foo",
    element: <div>Hello world!</div>,
    errorElement: <ErrorPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);


// import React from "react"
// import ReactDOM from "react-dom/client";
// import App from "./App"

// import './style.css';

// const root = ReactDOM.createRoot(document.getElementById('app'));
 
// const isStrictMode = true; //this causes the re-rendering of the entire app

// root.render(
//   <> 
//   {isStrictMode ? 
//     <React.StrictMode>
//       <App timestamp={new Date().valueOf()} />
//     </React.StrictMode>:
//     <App timestamp={new Date().valueOf()} />}
//   </>
// );

