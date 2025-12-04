import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: 'Diabetes Prediction | Medical Risk Assessment',
    description: 'Professional diabetes risk prediction and patient management system',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}
