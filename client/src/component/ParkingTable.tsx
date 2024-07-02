// components/ParkingTable.tsx
import React from "react";

interface ParkingTableProps {
  data: Array<{ location: string; availability: number }>;
}

export const ParkingTable: React.FC<ParkingTableProps> = ({ data }) => {
  return (
    <div className="w-1/2 ml-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Location
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Availability
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr key={index}>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {row.location}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {row.availability}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
