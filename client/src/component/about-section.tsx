export const AboutSection = () => {
  return (
    <div className="py-10 sm:py-8">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">
            Spot Finder
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            A Parking Spot Finder App
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Spot Finder utilizes object detection to identify and locate
            available parking spots. Provides real-time updates on parking
            availability. Offers a user-friendly interface for seamless
            naviation. Spotfinder optimizes urban mobility by streamiling the
            parking process.
          </p>
        </div>
      </div>
    </div>
  );
};
