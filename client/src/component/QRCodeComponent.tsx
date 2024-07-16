"use client";
// src/component/QRCodeComponent.tsx
import React from 'react';
import QRCode from 'qrcode.react';

interface QRCodeComponentProps {
  url: string;
}

const QRCodeComponent: React.FC<QRCodeComponentProps> = ({ url }) => {
  return (
    <div>
      <QRCode value={url} />
    </div>
  );
};

export default QRCodeComponent;
