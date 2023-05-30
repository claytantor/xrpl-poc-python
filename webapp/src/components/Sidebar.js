import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {FaWallet, FaShoppingBag, FaUserTie} from "react-icons/fa";
import {BsCardChecklist,BsCashCoin,BsShop, BsCart, BsPostageFill} from "react-icons/bs";

import { useStore } from '../zstore';

const Sidebar = () => {

    const shop_id = useStore(state => state.shop_id);

    const navigate = useNavigate();
    return (
        <div className="p-2 flex flex-row md:flex-col flex-grow bg-pink-100 text-white">
    
            <aside className="w-full md:w-48" aria-label="Sidebar">
                <div className="py-3 px-3">
                    <ul className="flex flex-wrap md:flex-col items-center md:items-start">
                        <li>
                            <div onClick={()=>navigate('/wallet')} className="btn-sidebar">
                            <FaWallet className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Wallet</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/ledger')} className="btn-sidebar">
                            <BsCardChecklist className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Payloads</span>
                            </div> 
                        </li>
                        <li>
                            <div onClick={()=>navigate('/receive')} className="btn-sidebar">
                            <BsCashCoin className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Receive Payment</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/items')} className="btn-sidebar">
                            <FaShoppingBag className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Payment Items</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/customers')} className="btn-sidebar">
                            <FaUserTie className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Customers</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate('/addresses')} className="btn-sidebar">
                            <BsPostageFill className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Addresses</span>
                            </div>
                        </li>
                        <li>
                            <div onClick={()=>navigate(`/shop/${shop_id}`)} className="btn-sidebar">
                            <BsCart className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">My Shop</span>
                            </div>
                        </li>    
                        <li>
                            <div onClick={()=>navigate('/customer/shops')} className="btn-sidebar">
                            <BsShop className="text-2xl"/>
                            <span className="flex-1 ml-3 whitespace-nowrap">Where I Shop</span>
                            </div>
                        </li>                        
                    </ul>
                </div>
            </aside>






        </div>
    );
};

export default Sidebar;