"use client";
import React from 'react';
import QRCodeComponent from '@/component/QRCodeComponent';

const QRcodeconfirmation: React.FC = () => {
    const url = "http://example.com/your-parking-slot"; // Replace with the actual URL for the QR code

    return (
        <div style={{ padding: '20px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <img
                src="https://cdn0.iconfinder.com/data/icons/df_On_Stage_Icon_Set/128/Symbol_-_Check.png"
                alt="Booking Success"
                style={{ width: '100px', height: '100px', marginBottom: '20px' }}
            />
            <h1 style={{ fontWeight: 'bold', fontSize: '2em', marginBottom: '20px' }}>BOOKING SUCCESS!</h1>
            <p style={{ marginBottom: '20px' }}>Your parking slot is booked successfully.</p>
            <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'center' }}>
                <QRCodeComponent url={url} />
            </div>
            <p style={{ marginTop: '20px', fontSize: '1.2em' }}>Location Details: Your location address here</p>
            <div style={{ marginTop: '40px', display: 'flex', justifyContent: 'center', gap: '20px' }}>
                <button style={{ padding: '10px 20px', fontSize: '1em', fontWeight: 'bold' }} onClick={() => window.location.href = '/'}>
                    Home Page
                </button>
                <button style={{ padding: '10px 20px', fontSize: '1em', fontWeight: 'bold' }} onClick={() => window.location.href = '/booking'}>
                    Previous Bookings
                </button>
            </div>
        </div>
    );
};

export default QRcodeconfirmation;

