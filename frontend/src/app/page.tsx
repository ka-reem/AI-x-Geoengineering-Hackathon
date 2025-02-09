'use client';

import { Card, Title, AreaChart } from '@tremor/react';

export default function Home() {
  const chartdata = [
    { date: '2023-01-01', Temperature: 20, CO2: 415 },
    { date: '2023-02-01', Temperature: 21, CO2: 417 },
    { date: '2023-03-01', Temperature: 22, CO2: 419 },
  ];

  return (
    <div className="p-4 md:p-10 mx-auto max-w-7xl">
      <h1 className="text-2xl font-bold mb-8">Climate Engineering Dashboard</h1>
      
      <div className="grid gap-6">
        <Card>
          <Title>Global Temperature and CO2 Trends</Title>
          <div className="mt-4 h-72">
            <AreaChart
              data={chartdata}
              index="date"
              categories={["Temperature", "CO2"]}
              colors={["indigo", "cyan"]}
            />
          </div>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <Title>Key Metrics</Title>
            <div className="mt-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Average Temperature</p>
                  <p className="text-2xl font-semibold text-indigo-600">21°C</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">CO2 Levels</p>
                  <p className="text-2xl font-semibold text-cyan-600">417 ppm</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <Title>Status Updates</Title>
            <div className="mt-4 space-y-2">
              <div className="p-2 bg-green-50 rounded text-sm text-green-700">
                Systems operating normally
              </div>
              <div className="p-2 bg-blue-50 rounded text-sm text-blue-700">
                Data last updated: 2 hours ago
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
