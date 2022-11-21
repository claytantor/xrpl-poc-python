import React, { useEffect, useState } from "react";

import Spinner from "../components/Spinner";
import { WalletService } from "../services/WalletService";

import { useStore } from '../zstore';

const PaymentRequestForm = ({ setPaymentRequest }) => {

  const userCurrency = useStore(state => state.userCurrency);

  const [formState, setFormState] = useState({ 'amount':0.0, 'memo':'' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  let [xrpPrice, setXrpPrice] = useState(null);

  useEffect(() => {
      WalletService.getXrpPrice(userCurrency).then((xrpPrice) => {
          setXrpPrice(xrpPrice.data.XRP);
      });
  }, [userCurrency]);   

  const handleChange = (e) => {
    setError(null);
    setFormState({ ...formState, [e.target.name]: e.target.value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    //check if the amount is a number
    if (isNaN(formState.amount) || formState.amount <= 0) {
        setError('Amount must be a positive number');
        setLoading(false);
        return;
    }

    if(!error) {
      //convert amount to xrp
      const newFormState = { ...formState, 'amount': formState.amount / xrpPrice };
      console.log("newFormState", newFormState);

      WalletService.postPayRequest(newFormState).then(r => {
        console.log("new payment request",r.data);
        setPaymentRequest(r.data);
      }).catch(error => { 
          console.log(error)
      }).finally(() => {
        // console.log("finally")
        setLoading(false);
      }); 
    }
  };   


  return (
    <>
      <div className="p-4 bg-gray-100 w-full md:w-1/2 lg:w-1/3 rounded">
        <div className="text-2xl">Receive Payment</div>
        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Form Error:</strong>
            <span className="block sm:inline"> {error}</span>
        </div>}
        <div>
          <form className="mt-3 w-full max-w-lg">
            {/* ===== */}
            <div className="flex flex-wrap -mx-3 mb-6">
              <div className="w-full px-3">
                <label
                  className="block uppercase tracking-wide text-gray-800 text-xs font-bold mb-2"
                >
                  Amount {userCurrency} {xrpPrice ? `(${(formState.amount / xrpPrice).toFixed(2)} XRP)` : ''}
                </label>
                <input
                  className="appearance-none block w-full bg-gray-300 text-gray-800 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  id="grid-amount"
                  name="amount"
                  type="text"
                  onChange={handleChange}
                  placeholder={`Enter amount of ${userCurrency}`}
                />
                <p className="text-red-600 text-xs italic">
                  Required. Needs to be a positive number.
                </p>
              </div>
            </div>

            {/* ===== */}
            <div className="flex flex-wrap -mx-3 mb-6">
              <div className="w-full px-3">
                <label
                  className="block uppercase tracking-wide text-gray-800 text-xs font-bold mb-2"
                  htmlFor="grid-password"
                >
                  Memo
                </label>
                <input
                  className="appearance-none block w-full bg-gray-300 text-gray-800 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  id="grid-memo"
                  name="memo"
                  type="text"
                  onChange={handleChange}
                  placeholder="Enter memo if needed"
                />
                <p className="text-gray-600 text-xs italic">
                  One sentence memos are best.
                </p>
              </div>
            </div>

            {/* ===== */}

            {/* =========== */}
            <div className="p-2 flex justify-center w-full">
              <button className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded-xl focus:outline-none focus:shadow-outline" onClick={handleSubmit}>
                Create Payment Request
              </button>         
            </div>
            {loading && <div className="fp-2 flex justify-center w-full"><Spinner /></div>}
          </form>
        </div>
      </div>
    </>
  );
};

export default PaymentRequestForm;
