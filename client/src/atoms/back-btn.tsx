import { Link } from "react-router-dom";

const BackBtn = () => {
  return (
    <div className="flex h-7 w-7 items-center justify-center rounded-md border transition-all hover:bg-black/5 cursor-pointer">
      <Link className="cursor-pointer" to={"/"}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="2"
          stroke="currentColor"
          aria-hidden="true"
          className="h-5 w-5 text-gray-400"
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
