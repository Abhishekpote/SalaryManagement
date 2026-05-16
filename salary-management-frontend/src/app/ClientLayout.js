"use client";

import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";

export default function ClientLayout({ children }) {
  const pathname = usePathname();
  const isAuthPage = pathname === "/login" || pathname === "/signup";

  return (
    <>
      {!isAuthPage && <Sidebar />}
      <main className={isAuthPage ? "w-full" : "flex-1"}>{children}</main>
    </>
  );
}