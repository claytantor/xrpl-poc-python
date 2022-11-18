import React, {useState, useEffect} from "react"
import { useNavigate } from "react-router-dom";
import { SiXrp } from 'react-icons/si';
import { FaUserCircle } from 'react-icons/fa';
import {XummPkce} from 'xumm-oauth2-pkce';
import icon32 from "../assets/favicon_io/favicon-32x32.png"


import { useStore } from "../zstore";
import { xummConfig, whitepaperUrl } from "../env";

const Header = ({
    xumm,
    xummState,
    setXummState,
    children,
  }) => {

    // useEffect(() => {
    //     console.log("Header xumm state", xummState);
    //     if (xummState && xummState.jwt) {
    //         console.log("Header xumm state jwt", xummState.jwt);
    //     }
    // }, [xummState]);

    const navigate = useNavigate();

    let logout = () => {
        console.log(`logout`, xummState);
        setXummState(null);
        xumm.logout();
        navigate("/");
    };

    let login = () => {
        navigate("/login");
    };

    let wallet = () => {
        console.log(`wallet`);
        navigate("/wallet");
    };

    return (
      <div className="w-full">
            
            <nav className="flex flex-col md:flex-row items-center justify-between bg-pink-700 p-3">
                <div className="flex w-full md:w-1/2">
                    <img src={icon32} alt="icon32" className="w-12" />
                    <span className="ml-2 mt-2 items-center font-semibold text-2xl tracking-tight text-white" onClick={()=>navigate('/')}>xurlpay.org</span>
                    <div className="text-slate-900 rounded-lg bg-pink-200 w-fit pr-1 pl-1 ml-2 mt-3 h-6 items-center">{xummConfig.xrp_network}</div>                  
                </div>
                <div className="flex flex-row md:w-1/2 justify-end w-full">
                    <div className="mr-3 mt-3">
                        <a href={whitepaperUrl} className="block mt-4 md:inline-block md:mt-0 text-white hover:underline cursor-pointer">
                        White Paper
                        </a> 
                    </div>

                    {/* ==== IN ==== */}
                    {xummState && xummState.me  ? <>
                            <div>

                                <div className="p-1">
                                    <div className="dropdown inline-block relative">
                                        <button className="bg-pink-300 text-pink-700 font-semibold py-2 px-4 rounded-t inline-flex items-center">
                                            <div className="mr-1 flex flex-row"><FaUserCircle className='mr-1'/>{xummState.me.sub}</div>
                                            <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
                                        </button>
                                        <ul style={{zIndex: 50}} className="dropdown-menu absolute hidden text-gray-700 pt-1 bg-gray-200 rounded-b w-full">
                                            <li className="">
                                                <button onClick={wallet} className="hover:underline font-semibold cursor-pointer text-black  py-2 px-4 block whitespace-no-wrap">Wallet</button>
                                                </li>
                                            <li className="">
                                                <button onClick={()=>logout()} className="hover:underline font-semibold cursor-pointer text-black rounded-b py-2 px-4 block whitespace-no-wrap">Logout</button>
                                            </li>

                                        </ul>
                                    </div>

                                </div>
                            </div>
                        </> :
                        <>

                        <div><button className="inline-block text-sm px-4 py-2 leading-none border rounded-xl text-white border-white hover:border-transparent hover:text-pink-500 hover:bg-white mt-4 md:mt-0" onClick={()=>login()}>Login</button></div></>
                    }                   
                </div>
        
            </nav>
      </div>
    );
};

const dropdownStyle = {
    zIndex: 50
};
  
export default Header