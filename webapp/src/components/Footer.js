import React from "react"

const Footer = () => {
    return (
        <footer className="sticky top-[100vh] text-white bg-slate-900">

            <div className="p-6 w-full">
                <div className="grid gap-x-0.8 grid-cols-1 md:grid-cols-2">
                    <div className="mb-6 w-1/2">
                        <h5 className="mb-2.5 font-bold text-white">xurlpay.org</h5>
                        <p>Blog messenger bag scenester, health goth flannel letterpress semiotics mumblecore. Street art hell of</p>
                    </div>

                    

                    <div className="mb-6">
                        <h5 className="mb-2.5 font-bold uppercase text-slate-300">Links</h5>

                            <ul className="mb-0 list-none">
                                <li>
                                <a href="#!" className="text-slate-200">Github</a>
                                </li>
                                <li>
                                <a href="#!" className="text-slate-200">License</a>
                                </li>
                                <li>
                                <a href="#!" className="text-slate-200">Link 3</a>
                                </li>
                                <li>
                                <a href="#!" className="text-slate-200">Link 4</a>
                                </li>
                            </ul>
                    </div>
                </div>
            </div>

        </footer>
    );
  };
  
export default Footer