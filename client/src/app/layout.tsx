import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "mapbox-gl/dist/mapbox-gl.css";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Spot Finder",
  description: "Step Project",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="manifest" href="/site.webmanifest" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="Spot Finder" />
        <meta property="og:description" content="Parking Spot Finder" />
        <meta property="og:title" content="Spot Finder" />
        <meta property="og:image" content="/logo.jpeg" />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
