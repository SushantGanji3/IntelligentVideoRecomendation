import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Intelligent Video Recommendation',
  description: 'YouTube-like recommendation system with ML-powered similarity search',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}

