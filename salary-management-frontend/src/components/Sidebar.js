"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navItems = [
    { href: "/", label: "Home", icon: "🏠" },
    { href: "/employees", label: "Manage Employee", icon: "👥" },
  ];

  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold">Salary Management</h1>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
              pathname === item.href
                ? "bg-slate-800 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-sm font-medium">{user?.name || user?.username}</p>
            <Badge variant="secondary" className="text-xs mt-1">{user?.role || "user"}</Badge>
          </div>
        </div>
        <Button variant="outline" onClick={logout} className="w-full text-slate-900">
          Logout
        </Button>
      </div>
    </aside>
  );
}