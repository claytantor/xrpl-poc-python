import React, { useState, useEffect } from "react";
import {backendBaseUrl} from '../env';

const XummQrCode = ({ url }) => {
    const [qrCodeUrl, setQrCodeUrl] = useState(null)
    
    useEffect(() => {
        const qr_url = `${backendBaseUrl}/xumm/qr?url=${encodeURIComponent(url)}`
        console.log("XummQrCode", qr_url, url)
        setQrCodeUrl(qr_url);
    }, [url])
    
    return (
        <>{qrCodeUrl && <img src={qrCodeUrl}/>}</>
    )
};

export default XummQrCode;