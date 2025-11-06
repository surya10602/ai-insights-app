// app/page.tsx
export const dynamic = 'force-dynamic';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button"; // Import the Shadcn Button
import Link from "next/link"; // Import the Next.js Link

// This is a Server Component, so we fetch data directly
async function getInsights() {
  try {
    // This URL must match your FastAPI server
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/insights`, {
      cache: "no-store", // Don't cache data, always get fresh
    });
    
    if (!res.ok) throw new Error("Failed to fetch");
    return res.json();
  } catch (error) {
    console.error("Failed to fetch insights:", error);
    return [];
  }
}

export default async function HomePage() {
  const insights: any[] = await getInsights();

  return (
    <div className="max-w-2xl mx-auto p-8 space-y-4">
      <h1 className="text-2xl font-bold">Your Insight Feed</h1>

      {/* --- ADD THIS SECTION --- */}
      <div className="flex gap-4">
        <Button asChild>
          <Link href="/transcript">New Transcript Insight</Link>
        </Button>
        <Button asChild>
          <Link href="/linkedin">New LinkedIn Icebreaker</Link>
        </Button>
      </div>
      {/* --- END OF NEW SECTION --- */}

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
            <p className="text-gray-500 italic">
            {/* You could add a loading spinner here */}
            Processing...
            </p>
            ) : (
            <p className="whitespace-pre-wrap">
            {insight.output_analysis}
            </p>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}