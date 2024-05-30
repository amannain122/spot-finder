const SearchBox = () => {
  return (
    <div className="flex justify-center items-center">
      <div className="relative w-full">
        <input
          type="text"
          placeholder="Address, city or postal code"
          className="w-full py-3 px-4 pl-10 text-gray-500 placeholder-gray-300 border border-transparent rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
        />
        <svg
          className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-300"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          fill="currentColor"
          viewBox="0 0 16 16"
        >
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001a1 1 0 0 0-.195.195l3.85 3.85a1 1 0 0 0 1.414-1.414l-3.85-3.85a1 1 0 0 0-.195-.195zm-5.742 1a5 5 0 1 1 0-10 5 5 0 0 1 0 10z" />
        </svg>
      </div>
    </div>
  );
};

export { SearchBox };
