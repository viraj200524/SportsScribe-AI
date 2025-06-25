import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Navbar } from "@/components/navbar"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Cricket Journalism Automation",
  description: "Automated sports journalism platform for cricket statistics and reports",
  keywords: "cricket, sports journalism, statistics, reports, automation",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-gradient-to-br from-green-50 to-green-100`}>
        <Navbar />
        <main className="pt-16">{children}</main>
      </body>
    </html>
  )
}
