import React, {useEffect, useState } from "react"

import Page  from "../components/Page"

import { useStore } from '../zstore';
import {currencyLang, makeCurrencyList} from "../env"

import { WalletService } from "../services/WalletService"


const CurrencySetting = () => {
    const userCurrency = useStore(state => state.userCurrency);
    const setUserCurrency = useStore(state => state.setUserCurrency);

    const [dataDropdownToggle, setDataDropdownToggle] = useState(false);  

    let [xrpPrice, setXrpPrice] = useState(null);

    useEffect(() => {
        WalletService.getXrpPrice(userCurrency).then((xrpPrice) => {
            setXrpPrice(xrpPrice.data.XRP);
        });
    }, [userCurrency]);    

    const currenciesMenuItems = () => {
        let currencyList = makeCurrencyList();
        console.log("currenciesMenuItems", currencyList);
        return currencyList.map((currency) => {
            return <li onClick={(e)=>currenciesMenuHandler(e)} className="block px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white" data-currency={currency.value} key={currency.value}>{currency.label}</li>
        });
    };

    const currenciesMenuHandler = (e) => {
        console.log("currenciesMenuHandler", e.currentTarget.dataset.currency);
        setDataDropdownToggle(!dataDropdownToggle);
        setUserCurrency(e.currentTarget.dataset.currency);
    };

    
    return (
        <div className="flex flex-row w-full">
            <div className="w-48">
                <button id="dropdownDefault" onClick={()=>setDataDropdownToggle(!dataDropdownToggle)} className="text-white w-48 bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:outline-none focus:ring-pink-300 font-medium rounded-lg text-sm px-4 py-2.5 text-center inline-flex items-center dark:bg-pink-600 dark:hover:bg-pink-700 dark:focus:ring-pink-800 justify-between" type="button">
                        Select User Currency 
                        <svg className="ml-2 w-4 h-4" ariaHidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                </button>
                <div id="dropdown" className={`${dataDropdownToggle ? "block":"hidden"} z-10 w-48 bg-white rounded divide-y divide-gray-100 shadow dark:bg-gray-700`}>
                    <ul className="py-1 text-sm text-gray-700 dark:text-gray-200" ariaLabelledby="dropdownDefault">
                        {currenciesMenuItems()}
                    </ul>
                </div>
            </div>
            <div className="ml-2">{xrpPrice} XRP = 1 {userCurrency}, Lang: {currencyLang[userCurrency]} </div>
        </div>
    );
}

const UserSettings = ({xummState}) => {


    return (
        <>
        <Page withSidenav={true} 
            xummState={xummState}> 
            <div className="p-4"> 
                <h2 className="text-2xl">User Settings</h2>
                <div className="mt-2">
                    <CurrencySetting />
                </div>

            </div>
        </Page> 
        </>

    );
};

export default UserSettings;