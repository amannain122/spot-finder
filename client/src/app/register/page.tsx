import Link from "next/link";
import { Metadata } from "next";
import { RegisterForm } from "@/component/form";
import { Layout } from "@/component/layout";

export const metadata: Metadata = {
  title: "Register | Spot Finder",
  description: "Step Project",
};

const RegisterPage = () => {
  return (
    <Layout>
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-r">
        {/* <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-200 to-green-200"> */}
        <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
          <h2 className="mb-2 text-2xl font-bold text-center">
            Create Account
          </h2>
          <p className="mb-4 text-center">
            Sign Up with{" "}
            <Link href={"/"}>
              <span className="font-bold text-blue-600">Spot Finder</span>
            </Link>{" "}
            and Find Your best Parking
          </p>
          <RegisterForm />
          <div className="text-center mt-4 flex flex-col justify-center items-center gap-4">
            <p>Already have an account?</p>
            <Link href="/login" className="text-sm text-blue-600">
              Login
            </Link>
            <Link href={"/"} className="text-center">
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
                  d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
                />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default RegisterPage;
