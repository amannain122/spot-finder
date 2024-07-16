// // src/component/QRCodeComponent.tsx
// import React from 'react';
// import QRCode from 'qrcode.react';

// interface QRCodeComponentProps {
//   url: string;
// }

// const QRCodeComponent: React.FC<QRCodeComponentProps> = ({ url }) => {
//   return (
//     <div>
//       <QRCode value={url} />
//     </div>
//   );
// };

// export default QRCodeComponent;
// src/components/QRCodeComponent.tsx
import React from 'react';
import QRCode from 'qrcode.react';

interface QRCodeComponentProps {
  value: string; // Renamed prop to match 'value' instead of 'url' for clarity
  size?: number;
  bgColor?: string;
  fgColor?: string;
}

const QRCodeComponent: React.FC<QRCodeComponentProps> = ({
  value,
  size = 128, // Default size if not provided
  bgColor = '#FFFFFF', // Default background color
  fgColor = '#000000' // Default foreground color
}) => {
  return (
    <div>
      <QRCode value={value} size={size} bgColor={bgColor} fgColor={fgColor} />
    </div>
  );
};

export default QRCodeComponent;

