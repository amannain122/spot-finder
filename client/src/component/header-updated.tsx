"use client";
import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogPanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from "@headlessui/react";
import Link from "next/link";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";
import { getJwtToken } from "@/lib/server";

const navigation = [
  { name: "About", href: "/about" },
  { name: "QR Code", href: "/parking-qr" },
  { name: "Live Stream", href: "/live-stream" },
];

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

export const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const router = useRouter();
  const [token, setToken] = useState("");

  useEffect(() => {
    const token = getJwtToken();
    setToken(token || "");
  }, []);

  console.log(token);
  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };
  const handleProfile = () => {
    router.push("/profile");
  };
  return (
    <>
      <header className="inset-x-0 top-0 z-50 border-b-2">
        <nav
          aria-label="Global"
          className="flex items-center justify-between py-2"
        >
          <div className="flex lg:flex-1 items-center ">
            <Link href="/" className="-m-1.5 p-1.5">
              <span className="sr-only">Spot Finder</span>
              <img alt="" src="/logo.jpeg" className="h-12 w-auto" />
            </Link>
            <Link href={"/"}>
              <h1 className="text-lg font-semibold leading-6 text-gray-900">
                Spot Finder
              </h1>
            </Link>
          </div>
          <div className="flex lg:hidden">
            <a
              href="https://github.com/amannain122/spot-finder"
              target="_blank"
              className="mr-4"
            >
              <GitHubIcons />
            </a>
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon aria-hidden="true" className="h-6 w-6" />
            </button>
          </div>
          <div className="hidden lg:flex lg:gap-x-12">
            {navigation.map((item) => (
              <Link href={item.href} key={item.name} legacyBehavior>
                <a
                  key={item.name}
                  href={item.href}
                  className="text-[1rem] font-semibold leading-6 text-gray-900"
                >
                  {item.name}
                </a>
              </Link>
            ))}
          </div>

          <div className="hidden lg:flex lg:flex-1 lg:justify-end items-center">
            <a
              href="https://github.com/amannain122/spot-finder"
              target="_blank"
              className="mr-4"
            >
              <GitHubIcons />
            </a>
            {!token ? (
              <>
                <Link href="/login">
                  <button
                    aria-label="Login"
                    aria-live="polite"
                    className="bg-gray-100 font-medium text-black py-2 px-4 mr-3 rounded-sm"
                  >
                    Login
                  </button>
                </Link>

                <Link className="" href="/register">
                  <button
                    aria-label="Register"
                    aria-live="polite"
                    className="bg-green-300 font-medium text-black py-2 px-4 rounded-sm"
                  >
                    Register
                  </button>
                </Link>
              </>
            ) : (
              <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                {/* Profile dropdown */}
                <Menu as="div" className="relative ml-3">
                  <div>
                    <MenuButton className="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                      <span className="absolute -inset-1.5" />
                      <span className="sr-only">Open user menu</span>
                      <img
                        alt=""
                        src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                        className="h-8 w-8 rounded-full"
                      />
                    </MenuButton>
                  </div>
                  <MenuItems
                    transition
                    className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                  >
                    <MenuItem>
                      <a
                        href="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                      >
                        Your Profile
                      </a>
                    </MenuItem>
                    <MenuItem>
                      <a
                        href="/booking"
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                      >
                        My Bookings
                      </a>
                    </MenuItem>
                    <MenuItem>
                      <a
                        href="#"
                        onClick={() => handleLogout()}
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                      >
                        Sign out
                      </a>
                    </MenuItem>
                  </MenuItems>
                </Menu>
              </div>
            )}
          </div>
        </nav>

        <Dialog
          open={mobileMenuOpen}
          onClose={setMobileMenuOpen}
          className="lg:hidden"
        >
          <div className="fixed inset-0 z-50" />
          <DialogPanel className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div className="flex items-center justify-between">
              <a href="#" className="-m-1.5 p-1.5">
                <span className="sr-only">Your Company</span>
                <img alt="" src="./logo.jpeg" className="h-8 w-auto" />
              </a>
              <button
                type="button"
                onClick={() => setMobileMenuOpen(false)}
                className="-m-2.5 rounded-md p-2.5 text-gray-700"
              >
                <span className="sr-only">Close menu</span>
                <XMarkIcon aria-hidden="true" className="h-6 w-6" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {navigation.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                    >
                      {item.name}
                    </a>
                  ))}
                </div>
                {!token ? (
                  <div className="py-6">
                    <Link href={"/login"} legacyBehavior>
                      <a
                        href="/login"
                        className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                      >
                        Log in
                      </a>
                    </Link>
                    <Link href="/register" legacyBehavior>
                      <a className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">
                        Register
                      </a>
                    </Link>
                  </div>
                ) : (
                  <>
                    <div className="">
                      <a
                        href="/profile"
                        className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                      >
                        Profile
                      </a>
                    </div>
                    <div className="">
                      <a
                        onClick={() => handleLogout()}
                        href=""
                        className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                      >
                        Logout
                      </a>
                    </div>
                  </>
                )}
              </div>
            </div>
          </DialogPanel>
        </Dialog>
      </header>
    </>
  );
};
