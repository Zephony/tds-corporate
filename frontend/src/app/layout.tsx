import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import '../css/main.css'
import '../css/variable.css'

const inter = Inter({
    subsets: ['latin'],
    weight: ['300', '400', '500', '600', '700', '800', '900'],
    display: 'swap',
    variable: '--font-inter',
});

export const metadata: Metadata = {
    title: 'The Data Supermarket | Mobile KYC & Trust Scoring',
    description: 'Carrier-derived Mobile KYC & Trust Scoring. Identify fraud, verify identity, and reduce risk using mobile network signals.',
    icons: {
        icon: '/logo.png',
    }
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang='en' className={inter.variable}>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            </head>
            <body className={inter.className}>
            <div className='main'>
                {children}
            </div>
            </body>
        </html>
    );
}
