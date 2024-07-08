import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

// helper function to merge class names
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
