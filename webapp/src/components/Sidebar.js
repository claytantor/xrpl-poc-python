import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {AiOutlineDashboard, AiOutlineUser, AiOutlineLogout} from "react-icons/ai";
import {FaWallet, FaShoppingBag} from "react-icons/fa";
import {BsCardChecklist} from "react-icons/bs";
import {BsCashCoin} from "react-icons/bs";
const Sidebar = ({ useStore }) => {

    const navigate = useNavigate();
    return (
        <div className="p-2 flex flex-col flex-grow bg-pink-100 text-white">
    
            <aside className="w-48" aria-label="Sidebar">
                <div className="overflow-y-auto py-4 px-3 dark:bg-gray-800">
                    <ul className="space-y-2">
                        {/* <li>
                            <div className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">

                            <AiOutlineDashboard className="text-2xl"/>

                            <span className="ml-3">Dashboard</span>
                            </div>
                        </li> */}
                        <li>
                            <div onClick={()=>navigate('/wallet')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 hover:text-pink-800 dark:hover:bg-gray-700">
                            <FaWallet className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Wallet</span>
                            {/* <span className="inline-flex justify-center items-center px-2 ml-3 text-sm font-medium text-gray-800 bg-gray-200 rounded-full dark:bg-gray-700 dark:text-gray-300">testnet</span> */}
                            </div>
                        </li>
                        {/* <li>
                            <a href="#" className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <svg aria-hidden="true" className="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M8.707 7.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l2-2a1 1 0 00-1.414-1.414L11 7.586V3a1 1 0 10-2 0v4.586l-.293-.293z"></path><path d="M3 5a2 2 0 012-2h1a1 1 0 010 2H5v7h2l1 2h4l1-2h2V5h-1a1 1 0 110-2h1a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5z"></path></svg>
                            <span className="flex-1 ml-3 whitespace-nowrap">Inbox</span>
                            <span className="inline-flex justify-center items-center p-3 ml-3 w-3 h-3 text-sm font-medium text-blue-600 bg-blue-200 rounded-full dark:bg-blue-900 dark:text-blue-200">3</span>
                            </a>
                        </li> */}
                        {/* <li>
                            <a href="#" className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <svg aria-hidden="true" className="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd"></path></svg>
                            <span className="flex-1 ml-3 whitespace-nowrap">Users</span>
                            </a>
                        </li> */}
                        <li>
                            <div onClick={()=>navigate('/ledger')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white  hover:bg-gray-100 dark:hover:bg-gray-700">
                            <BsCardChecklist className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Ledger</span>
                            </div> 
                        </li>
                        <li>
                            <div onClick={()=>navigate('/receive')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <BsCashCoin className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Receive Payment</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/items')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <FaShoppingBag className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Payment Items</span>
                            </div>
                        </li>
                        {/* <li>
                            <a href="#" className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <svg aria-hidden="true" className="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd"></path></svg>
                            <span className="flex-1 ml-3 whitespace-nowrap">Sign In</span>
                            </a>
                        </li> */}
                        {/* <li>
                            <a href="#" className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <svg aria-hidden="true" className="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clipRule="evenodd"></path></svg>
                            <span className="flex-1 ml-3 whitespace-nowrap">Sign Up</span>
                            </a>
                        </li> */}
                    </ul>
                </div>
            </aside>






        </div>
    );
};

export default Sidebar;