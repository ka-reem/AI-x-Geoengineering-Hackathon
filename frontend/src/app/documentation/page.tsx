import { Card } from '@tremor/react';

export default function Documentation() {
  return (
    <div className="max-w-3xl mx-auto px-4">
      <Card className="p-4">
        <h1 className="text-lg font-semibold mb-3">Climate Engineering Documentation</h1>
        <div className="prose prose-sm">
          <h2 className="text-xl font-semibold mb-2">Overview</h2>
          <p className="mb-4">
            This dashboard provides insights into various climate engineering initiatives and their impacts on global climate patterns.
          </p>
          
          <h2 className="text-xl font-semibold mb-2">Data Sources</h2>
          <p className="mb-4">
            Our data is collected from multiple reliable sources including satellite measurements, ground stations, and atmospheric sensors.
          </p>
          
          <h2 className="text-xl font-semibold mb-2">Methodology</h2>
          <p className="mb-4">
            We analyze climate data using state-of-the-art models and visualization techniques to provide actionable insights.
          </p>
        </div>
      </Card>
    </div>
  );
}
