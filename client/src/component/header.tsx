"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { cn } from "@/lib/utils";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";
import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarTrigger,
} from "@/components/ui/menubar";
import { getJwtToken } from "@/lib/server";

export const GitHubIcons = () => {
  return (
    <svg
      className="ml-4 h-6 w-6 fill-slate-400 dark:fill-slate-100 "
      viewBox="0 0 16 16"
    >
      <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z"></path>
    </svg>
  );
};

export function NavigationMenuDemo() {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuTrigger>Navigation</NavigationMenuTrigger>
          <NavigationMenuContent>
            <ul className="grid gap-3 p-4 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]">
              <li className="row-span-3">
                <NavigationMenuLink asChild>
                  <a
                    className="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                    href="/"
                  >
                    <img src="/logo.jpeg" className=" w-12" />
                    <div className="mb-2 mt-4 text-lg font-medium">
                      Spot Finder
                    </div>
                    <p className="text-sm leading-tight text-muted-foreground">
                      AI and DS Step Group Project/Parking Spot Finder
                    </p>
                  </a>
                </NavigationMenuLink>
              </li>
              <ListItem href="/about" title="About">
                About The Project, Teams Members
              </ListItem>

              <ListItem href="/parking-qr" title="QR Codes">
                Parking QR
              </ListItem>
              <ListItem href="/live-stream" title="Live Stream">
                Live Stream of Parking Lots
              </ListItem>
              <ListItem
                href="/login"
                title="Login"
                className="lg:hidden md:hidden sm:block"
              ></ListItem>
              <ListItem
                href="/register"
                title="Register"
                className="lg:hidden md:hidden sm:block"
              ></ListItem>
            </ul>
          </NavigationMenuContent>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
}

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className
          )}
          {...props}
        >
          <div className="text-sm font-medium leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  );
});

ListItem.displayName = "ListItem";

export const Header = () => {
  const router = useRouter();
  const [token, setToken] = useState("");

  useEffect(
    () => () => {
      const token = getJwtToken();
      setToken(token || "");
    },
    []
  );
  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };
  const handleProfile = () => {
    router.push("/profile");
  };
  return (
    <div className="flex items-center h-16 justify-between">
      <div className="flex items-center">
        <img src="/logo.jpeg" className="w-12 mr-6" />
        <NavigationMenuDemo />
      </div>
      <div className="flex justify-center items-center gap-4">
        {token ? (
          <Menubar>
            <MenubarMenu>
              <MenubarTrigger>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="size-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                </svg>
              </MenubarTrigger>
              <MenubarContent>
                <MenubarItem onClick={handleProfile}>Profile</MenubarItem>
                <MenubarSeparator />
                <MenubarItem onClick={handleLogout}>Logout</MenubarItem>
              </MenubarContent>
            </MenubarMenu>
          </Menubar>
        ) : (
          <div className="hidden lg:block md:block">
            <Link href="/login">
              <button
                aria-label="Login"
                aria-live="polite"
                className="bg-gray-100 text-black py-2 px-4 mr-2 rounded-sm"
              >
                Login
              </button>
            </Link>

            <Link className="" href="/register">
              <button
                aria-label="Register"
                aria-live="polite"
                className="bg-green-300 text-black py-2 px-4 rounded-sm"
              >
                Register
              </button>
            </Link>
          </div>
        )}

        <a href="https://github.com/amannain122/spot-finder" target="_blank">
          <GitHubIcons />
        </a>
      </div>
    </div>
  );
};
