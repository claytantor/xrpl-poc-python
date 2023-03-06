import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {FaWallet, FaShoppingBag} from "react-icons/fa";
import {BsCardChecklist} from "react-icons/bs";
import {BsCashCoin} from "react-icons/bs";
const Sidebar = () => {

    const navigate = useNavigate();
    return (
        <div className="p-2 flex flex-col flex-grow bg-pink-100 text-white">
    
            <aside className="w-48" aria-label="Sidebar">
                <div className="overflow-y-auto py-4 px-3 dark:bg-gray-800">
                    <ul className="space-y-2">

                        <li>
                            <div onClick={()=>navigate('/wallet')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 hover:text-pink-800 dark:hover:bg-gray-700">
                            <FaWallet className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Wallet</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/ledger')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white  hover:bg-gray-100 dark:hover:bg-gray-700">
                            <BsCardChecklist className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Payloads</span>
                            </div> 
                        </li>
                        <li>
                            <div onClick={()=>navigate('/receive')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <BsCashCoin className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Receive Payment</span>
                            </div>
                        </li>
                        {/* <li>
                            <div onClick={()=>navigate('/items')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <FaShoppingBag className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Inventory Items</span>
                            </div>
                        </li> */}
                        <li>
                            <div onClick={()=>navigate('/items')} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:text-pink-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700">
                            <FaShoppingBag className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Payment Items</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </aside>






        </div>
    );
};

export default Sidebar;