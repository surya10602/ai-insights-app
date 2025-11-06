// app/page.tsx
"use client"; // This must be a Client Component

import { useState, useEffect, useRef } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

// Define a type for our insight
type Insight = {
  id: number;
  created_at: string;
  type: string;
  output_analysis: string;
};

export default function HomePage() {
  const [insights, setInsights] = useState<Insight[]>([]);
  // Use a ref to store the interval ID
  const pollingInterval = useRef<NodeJS.Timeout | null>(null);

  // Function to fetch insights from our backend
  const fetchInsights = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/insights`
      );
      if (res.ok) {
        const data = await res.json();
        setInsights(data);
      }
    } catch (error) {
      console.error("Failed to fetch insights:", error);
    }
  };

  // 1. Fetch the initial data when the page loads
  useEffect(() => {
    fetchInsights();
  }, []); // Empty array means this runs once on load

  // 2. Set up the polling logic
  useEffect(() => {
    // Check if any insights are still processing
    const isProcessing = insights.some(
      (insight) => insight.output_analysis === "Processing..."
    );

    if (isProcessing) {
      // If we are processing AND an interval isn't already running
      if (!pollingInterval.current) {
        console.log("Starting polling...");
        pollingInterval.current = setInterval(() => {
          console.log("Polling for updates...");
          fetchInsights();
        }, 3000); // Poll every 3 seconds
      }
    } else {
      // If nothing is processing, stop any existing interval
      if (pollingInterval.current) {
        console.log("Stopping polling.");
        clearInterval(pollingInterval.current);
        pollingInterval.current = null;
      }
    }

    // Clean up interval when the component is unmounted
    return () => {
      if (pollingInterval.current) {
        clearInterval(pollingInterval.current);
      }
    };
  }, [insights]); // This effect re-runs every time the 'insights' state changes

  return (
    <div className="max-w-2xl mx-auto p-8 space-y-4">
      <h1 className="text-2xl font-bold">Your Insight Feed</h1>

      <div className="flex gap-4">
        <Button asChild>
          <Link href="/transcript">New Transcript Insight</Link>
        </Button>
        <Button asChild>
          <Link href="/linkedin">New LinkedIn Icebreaker</Link>
        </Button>
      </div>

      {insights.length === 0 && <p>No insights yet. Go generate one!</p>}

      {insights.map((insight) => (
        <Card key={insight.id}>
          <CardHeader>
            <CardTitle className="capitalize">{insight.type} Insight</CardTitle>
            <p className="text-sm text-gray-500">
              {new Date(insight.created_at).toLocaleString()}
            </p>
          </CardHeader>
          <CardContent>
            {insight.output_analysis === "Processing..." ? (
              <p className="text-gray-500 italic">Processing...</p>
            ) : (
              <p className="whitespace-pre-wrap">{insight.output_analysis}</p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}