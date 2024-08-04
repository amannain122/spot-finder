import Link from "next/link";

const BackBtn = () => {
  return (
    <div className="flex mb-3 h-8 w-8 items-center justify-center rounded-md border border-gray-400 transition-all hover:bg-black/5 cursor-pointer">
      <Link className="cursor-pointer" href={"/"}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="2"
          stroke="currentColor"
          aria-hidden="true"
          className="h-5 w-5 text-gray-800"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M11 17l-5-5m0 0l5-5m-5 5h12"
          ></path>
        </svg>
      </Link>
    </div>
  );
};

export default BackBtn;
