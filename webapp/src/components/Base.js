import React, {useEffect, useState } from "react"

export const Alert = ({ background, text, children }) => {
  return (
    <div className={`p-2 flex flex-row rounded ${background} ${text} w-full`} role="alert">
      {children}
    </div>
  );
};

export const HelpAlert = ({ children, helpLink }) => {
  return (
    <Alert background="bg-pink-100" text="text-slate-800">
        <div className="flex flex-row justify-end">
            <div>{children}</div>
        </div>      
    </Alert>
  );
};

export const Modal = ({ show, children }) => {
  return (
    <div
      className={`modal ${show ? "show" : ""}`}
      style={{ display: show ? "block" : "none" }}
    >
      <div className="modal-dialog">
        <div className="modal-content">{children}</div>
      </div>
    </div>
  );
};

export const Badge = ({ variant, children }) => {
  return <span className={`badge badge-${variant}`}>{children}</span>;
};

export const Spinner = ({ variant, children }) => {
    return (
        <div className="flex flex-row justify-center">
        <div className="spinner-border" role="status">
            <span className="sr-only">Loading...</span>
        </div>
        </div>
    );
};

