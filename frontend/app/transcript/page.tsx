// app/transcript/page.tsx
"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link"; // <-- 1. IMPORT LINK

export default function TranscriptPage() {
  const [company, setCompany] = useState("");
  const [attendees, setAttendees] = useState("");
  const [date, setDate] = useState("");
  const [transcript, setTranscript] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // This URL must match your running FastAPI server
    const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/insights/transcript`;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_name: company,
          attendees: attendees.split(","), // Simple split by comma
          date: date,
          transcript_text: transcript,
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok");
      
      const result = await response.json();
      console.log("Success:", result);
      alert("Insight generated and saved!");
      // Clear form
      setCompany("");
      setAttendees("");
      setDate("");
      setTranscript("");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate insight.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      {/* --- 2. ADD THIS BUTTON --- */}
      <Button asChild variant="outline" className="mb-4">
        <Link href="/">&larr; Back to Home</Link>
      </Button>
      {/* --- END OF NEW SECTION --- */}

      <form onSubmit={handleSubmit} className="space-y-4">
        <h1 className="text-2xl font-bold">New Transcript Insight</h1>
        <Input placeholder="Company Name" value={company} onChange={(e) => setCompany(e.target.value)} />
        <Input placeholder="Attendees (comma-separated)" value={attendees} onChange={(e) => setAttendees(e.target.value)} />
        <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        <Textarea
          placeholder="Paste your transcript here..."
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          rows={15}
        />
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Insight"}
        </Button>
      </form>
    </div>
  );
}