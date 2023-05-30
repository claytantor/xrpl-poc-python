import React, { useEffect, useState } from "react";

const AddressForm = ({handleCancel, handleSubmit, address}) => {

  // 'id': self.id,
  // 'name': self.name,
  // 'first_name': self.first_name,
  // 'last_name': self.last_name,
  // 'street_address': self.street_address,
  // 'street_address_2': self.street_address_2,
  // 'zip_code': self.zip_code,
  // 'city': self.city,
  // 'state': self.state,
  // 'country': self.country,
  // 'phone_number': self.phone_number,
  // 'postal_code': self.postal_code,
  // 'created_at': str(self.created_at),
  // 'updated_at': str(self.updated_at)

    const [form, setForm] = useState({
      name: "",
      first_name: "",
      last_name: "",
      street_address: "",
      street_address_2: "",
      city: "",
      state: "",
      postal_code: "",
      country: "",
      email: "",
      phone_number: ""
    });
  
    const [error, setError] = useState("");

    useEffect(() => {
      if (address) {
        setForm(address);
      }
    }, [address]);
  
    const handleChange = (e) => {
      console.log("handleChange", e.target.name, e.target.value);
      let n_form = {
        ...form,
        [e.target.name]: e.target.value
      };
      setForm(n_form);
      // console.log("handleChange", e.target, n_form);
    };
  

    return(<>

    <div className="flex flex-col justify-start">
      <div className="flex flex-row justify-start w-full p-2">
  
        <form className="space-y-4 w-full">
          <div className="w-full">
            <label className="block" htmlFor="name">Address Name</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="name" name="name" value={form.name} onChange={handleChange} required />
          </div>
          
          <div className="w-full">
            <label className="block">Receiving Person Name</label>
            <div className="flex flex-row">
              <input className="block w-full mr-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="first_name" name="first_name" value={form.first_name} onChange={handleChange} required />
              <input className="block w-full bg-slate-200 rounded border-2 border-slate-300" type="text" id="last_name" name="last_name" value={form.last_name} onChange={handleChange} required />
            </div>

          </div>
  
          <div>
            <label className="block" htmlFor="street_address">Street Address 1</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="street_address" name="street_address" value={form.street_address} onChange={handleChange} required />
          </div>

          <div>
            <label className="block" htmlFor="street_address_2">Street Address 2</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="street_address_2" name="street_address_2" value={form.street_address_2} onChange={handleChange} required />
          </div>
          
          <div>
            <label className="block" htmlFor="city">City</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="city" name="city" value={form.city} onChange={handleChange} required />
          </div>
  
          <div>
            <label className="block" htmlFor="state">State</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="state" name="state" value={form.state} onChange={handleChange} required />
          </div>
  
          <div>
            <label className="block" htmlFor="postal_code">Postal Code</label>
            <input className="block w-full mt-1 bg-slate-200 rounded border-2 border-slate-300" type="text" id="postal_code" name="postal_code" value={form.postal_code} onChange={handleChange} required />
          </div>
  
          <div className="flex flexr-row justify-end">
            <button
              className="text-slate-800 bg-slate-400 font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 rounded hover:bg-slate-200"
                        type="button"
                        onClick={() => handleCancel()}
                      >
                        Cancel
            </button>
            <button
              className="text-pink-800 bg-pink-400 font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 rounded hover:bg-pink-200"
                        type="button"
                        onClick={() => handleSubmit(form)}
                      >
                        Save
            </button>
          </div>    
        </form>
      </div> 
    </div>

    </>);
};

export default AddressForm;
