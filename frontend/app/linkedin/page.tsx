// app/linkedin/page.tsx
"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link"; // <-- 1. IMPORT LINK

export default function LinkedInPage() {
  const [bio, setBio] = useState("");
  const [deck, setDeck] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // This URL must match your running FastAPI server
    const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/insights/linkedin`; 

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          linkedin_bio: bio,
          pitch_deck: deck,
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok");
      
      const result = await response.json();
      console.log("Success:", result);
      alert("Icebreaker generated and saved!");
      // Clear form
      setBio("");
      setDeck("");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate icebreaker.");
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
        <h1 className="text-2xl font-bold">New LinkedIn Icebreaker</h1>
        
        <Textarea
          placeholder="Paste the LinkedIn 'About' section here..."
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          rows={10}
        />
        <Textarea
          placeholder="Paste your pitch deck summary or key value props..."
          value={deck}
          onChange={(e) => setDeck(e.target.value)}
          rows={10}
        />
        
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Icebreaker"}
        </Button>
      </form>
    </div>
  );
}