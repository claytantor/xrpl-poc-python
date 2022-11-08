import React, {useEffect, useState} from "react"

import Header from "./Header"
import Footer from "./Footer"

const Page = ({useStore, children,}) => {

  let [appDetails, setAppDetails] = useState();

  useEffect(() => {
    if (useStore) {
      console.log(`useStore get app details ${JSON.stringify(useStore.getState())}`);
      setAppDetails(useStore.getState().appDetails);
    }

  }, [useStore]);


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
              
              <Footer xummAppDetails={appDetails}/>
              </div>
          </div>  


      {/* </div> */}
    </>
  );
};
  
export default Page