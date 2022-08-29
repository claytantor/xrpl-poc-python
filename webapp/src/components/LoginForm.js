import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { AuthenticationService, setUser } from "../services/AuthenticationService";

const LoginForm = ({ setAccessToken }) => {

    let navigate = useNavigate();

    // "classic_address":"rU32wptoF4YPK3USvuYipUeDMqjF371B9J",
    // "private_key":"0044BE2DCC155D18A093F12D4E990C7DB61655D935F86CF0D818359679DAF3BD35"

    const [formState, setFormState] = useState({ 'classic_address':null, 'private_key':null });
    const [loading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormState({ ...formState, [e.target.name]: e.target.value });
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formState);
        AuthenticationService.login(formState['classic_address'],formState['private_key']).then(r => {
            let user = r.data;
            user.classic_address = formState['classic_address'];
            console.log("logged in user",user);
            setUser(user);
            navigate("/wallet");

        }).catch(error => {
            console.log(error);
            setError(error);
        }).finally(() => {
            console.log("finally");
        });

    };   


    return (
    <>
      <div className="p-1 flex w-full justify-center">
        <div>
            <h2 className="text-2xl">Login</h2>    

            {error && 
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-2 mb-2 max-w-lg" role="alert">
                <strong className="font-bold">Error!</strong>
                <span className="block sm:inline"> There was a problem logging in. Are you sure you are using the right address and private key?</span>
            </div>}


          <form className="mt-3 w-full max-w-lg">
            {/* ===== */}
            <div className="flex flex-wrap -mx-3 mb-6">
              <div className="w-full px-3">
                <label
                  className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                >
                  Wallet Address (classic)
                </label>
                <input
                  className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  id="grid-address"
                  name="classic_address"
                  type="text"
                  onChange={handleChange}
                  placeholder="Enter the wallet address"
                />
                <p className="text-red-600 text-xs italic">
                  Required. Needs to be a valid classic wallet address.
                </p>
              </div>
            </div>

            {/* ===== */}
            <div className="flex flex-wrap -mx-3 mb-6">
              <div className="w-full px-3">
                <label
                  className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
                  Private Key
                </label>
                <input
                  className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  id="grid-private-key"
                  name="private_key"
                  type="text"
                  onChange={handleChange}
                  placeholder="Enter private key"
                />
                <p className="text-red-600 text-xs italic">
                  Required. Needs to be the private key for the wallet you created. Can be as long as needed.
                </p>
              </div>
            </div>

            {/* ===== */}

            {/* =========== */}
            <div className="m-1 p-2 flex justify-end w-full">
              <button className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded-xl focus:outline-none focus:shadow-outline" onClick={handleSubmit}>
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
    );
};

export default LoginForm;
