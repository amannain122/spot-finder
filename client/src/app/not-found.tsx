import Link from "next/link";
import { Layout } from "@/component/layout";

export default function NotFound() {
  return (
    <Layout>
      <div className="flex flex-col items-center text-center justify-center md:flex-row md:items-center md:justify-center md:space-x-6 my-44">
        <div className="space-x-2 pb-8 pt-6 md:space-y-5">
          <h1 className="text-6xl font-extrabold leading-9 tracking-tight text-gray-900 dark:text-gray-100 md:border-r-2 md:px-6 md:text-8xl md:leading-14">
            404
          </h1>
        </div>
        <div className="max-w-md">
          <p className="mb-4 text-xl font-bold leading-normal md:text-2xl">
            Sorry we couldn&apos;t find this page.
          </p>
          <p className="mb-8">
            But dont worry, you can find plenty of other things on our homepage.
          </p>
          <Link
            href="/"
            className="focus:shadow-outline-blue inline rounded-lg border border-transparent bg-green-600 px-4 py-2 text-sm font-medium leading-5 text-white shadow transition-colors duration-150 hover:bg-green-700 focus:outline-none dark:hover:bg-green-500"
          >
            Back to homepage
          </Link>
        </div>
      </div>
    </Layout>
  );
}
