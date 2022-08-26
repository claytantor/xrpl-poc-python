import React from "react"

import Header from "./Header"
import Footer from "./Footer"

const Page = ({useStore,children,}) => {
    return (
      <>
        {/* <div id="container" className="flex min-h-screen flex-col">
            <Header useStore={useStore} />
            <div>{children}</div>
            <Footer/>  */}
            
            <div id="container" className="flex min-h-screen flex-col">
                <div id="header" className="flex"><Header useStore={useStore}/></div>
                <div id="main" className="flex flex-grow flex-col md:flex-row">
                    <div className="flex-grow">{children}</div>
                </div>
                <div id="footer" className="p-0 bg-black color-white">
                <Footer/>
                </div>
            </div>  


        {/* </div> */}
      </>
    );
  };
  
export default Page