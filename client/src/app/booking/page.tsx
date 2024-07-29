import React from 'react';
import { Header } from "@/component/header";
import BookingCard from "@/component/bookings-card"; 

// Image URL
const parkingIconUrl = 'https://cdn1.iconfinder.com/data/icons/city-elements-56/520/416_Car_Parking_Transport-512.png';

const BookingsPage: React.FC = () => {
    // Example condition for displaying the sorry text
    const hasBookings = false; // Replace with your actual logic to determine if there are bookings

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <Header />
            <h1 style={{ fontWeight: 'bold', fontSize: '2em', marginBottom: '20px' }}>My Bookings</h1>

            {/* Sorry text conditionally rendered */}
            {!hasBookings && (
                <p style={{ marginBottom: '40px' }}>Sorry, you currently have no bookings.</p>
            )}

            {/* Table to display column headings */}
            <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #ccc', marginBottom: '40px' }}>
                <thead>
                    <tr>
                        <th style={{ border: '1px solid #ccc', padding: '12px', textAlign: 'left' }}>Sl No</th>
                        <th style={{ border: '1px solid #ccc', padding: '12px', textAlign: 'left' }}>Location</th>
                        <th style={{ border: '1px solid #ccc', padding: '12px', textAlign: 'left' }}>Date</th>
                        <th style={{ border: '1px solid #ccc', padding: '12px', textAlign: 'left' }}>Status</th>
                    </tr>
                </thead>
                {/* Table body can be added for actual booking data if available */}
            </table>

            {/* Render BookingCard component */}
            {hasBookings && (
                <BookingCard />
            )}

            {/* Book Now button */}
            {!hasBookings && (
                <div style={{ marginBottom: '40px' }}>
                    <button style={{ padding: '12px 24px', fontSize: '1.2em', fontWeight: 'bold' }}>Book Now</button>
                </div>
            )}

            {/* Image */}
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '60px' }}>
                <img src={parkingIconUrl} alt="Parking Icon" style={{ width: '180px', height: '180px' }} />
            </div>
        </div>
    );
};

export default BookingsPage;
