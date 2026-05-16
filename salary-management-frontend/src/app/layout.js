import { AuthProvider } from "@/hooks/useAuth";
import { AuthMiddleware } from "@/hooks/AuthMiddleware";
import { Geist, Geist_Mono } from "next/font/google";
import ClientLayout from "./ClientLayout";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Salary Management",
  description: "Employee salary management system",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-full flex">
        <AuthProvider>
          <AuthMiddleware>
            <ClientLayout>{children}</ClientLayout>
          </AuthMiddleware>
        </AuthProvider>
      </body>
    </html>
  );
}