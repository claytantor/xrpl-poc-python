import React, {useEffect, useState} from "react"

import Header from "./Header"
import Footer from "./Footer"
import Sidebar from "./Sidebar"

const Page = ({
    withSidenav=false,
    xummState,
    children,
  }) => {

  return (
    <>
      <div id="container" className="flex min-h-screen flex-col">
        <div id="header" className="flex"><Header xummState={xummState}/></div>
        {withSidenav ? <div id="main" className="flex flex-grow flex-col md:flex-row">
          <div className="flex bg-gray-900  md:bg-gray-800 text-white"><Sidebar/></div>
          <div className="flex-grow">{children}</div>
        </div>:
        <div id="main" className="flex flex-grow flex-col md:flex-row">
            <div className="flex-grow">{children}</div>
        </div>
        }
        <div id="footer" className="p-0 bg-black color-white">
         <Footer/>
        </div>
      </div>   

    </>
  );
};
  
export default Page