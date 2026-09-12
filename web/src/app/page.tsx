"use client";

import { useState } from "react";

const CATEGORIES = ["Organic", "Plastic", "E-Waste", "Paper", "Hazardous", "Sanitary", "Glass", "Metal", "Other/Unknown"];

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [needsConfirmation, setNeedsConfirmation] = useState(false);
  const [needsManualSelection, setNeedsManualSelection] = useState(false);
  const [manualCategory, setManualCategory] = useState(CATEGORIES[0]);
  const [preview, setPreview] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      // Reset state
      setResult(null);
      setError("");
      setNeedsConfirmation(false);
      setNeedsManualSelection(false);
    }
  };

  const analyzeImage = async (confirmedCategory?: string) => {
    if (!file && !confirmedCategory) return;
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      if (file) formData.append("file", file);
      if (confirmedCategory) formData.append("manualCategory", confirmedCategory);

      const res = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Analysis failed");

      if (data.needsManualSelection) {
        setNeedsManualSelection(true);
        setResult(data);
      } else if (data.needsConfirmation) {
        setNeedsConfirmation(true);
        setResult(data);
      } else {
        setResult(data);
        setNeedsConfirmation(false);
        setNeedsManualSelection(false);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetFlow = () => {
    setFile(null);
    setPreview("");
    setResult(null);
    setNeedsConfirmation(false);
    setNeedsManualSelection(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Header */}
      <header className="bg-green-700 text-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">♻️ EcoSort AI</h1>
            <p className="text-green-100 text-sm mt-1">AI-Powered Waste Identification & Disposal Assistant</p>
          </div>
          <div className="text-xs bg-green-800 px-3 py-1 rounded-full border border-green-600">
            Prototype Demo Mode
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Left Column: Input and Results */}
        <div className="md:col-span-2 space-y-6">
          
          {/* Upload Section */}
          {!result && !loading && (
            <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 text-center">
              <h2 className="text-xl font-semibold mb-4">Upload a waste image</h2>
              <label className="cursor-pointer flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-green-300 rounded-lg bg-green-50 hover:bg-green-100 transition">
                <span className="text-green-700 font-medium">Click to browse or drag image here</span>
                <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
              </label>
              {preview && (
                <div className="mt-4">
                  <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded-lg shadow-sm" />
                  <button 
                    onClick={() => analyzeImage()} 
                    className="mt-4 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium shadow-sm transition"
                  >
                    Analyze Image
                  </button>
                </div>
              )}
              {error && <p className="mt-4 text-red-600 font-medium">{error}</p>}
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="bg-white p-12 rounded-xl shadow-sm border border-gray-200 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600 font-medium">Analyzing item and fetching local disposal rules...</p>
            </div>
          )}

          {/* Results Section */}
          {result && !loading && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="bg-gray-100 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-800">Analysis Result</h2>
                <button onClick={resetFlow} className="text-sm text-gray-500 hover:text-gray-800 underline">Start Over</button>
              </div>

              <div className="p-6">
                <div className="flex items-start space-x-6">
                  {preview && <img src={preview} alt="Uploaded" className="w-32 h-32 object-cover rounded-lg shadow-sm" />}
                  
                  <div className="flex-1">
                    <p className="text-sm text-gray-500 uppercase font-semibold">Detected Item</p>
                    <p className="text-2xl font-bold text-gray-900 mb-2">{result.itemName || "Unknown Item"}</p>
                    
                    <div className="flex items-center space-x-3 mb-4">
                      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full font-medium text-sm">
                        Category: {result.category}
                      </span>
                      <span className={`px-3 py-1 rounded-full font-medium text-sm ${result.confidence >= 0.8 ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        Confidence: {(result.confidence * 100).toFixed(0)}%
                      </span>
                    </div>

                    {/* Human in the loop dialogs */}
                    {needsManualSelection && (
                      <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-red-800 font-medium mb-3">⚠️ Confidence too low. Please select manually:</p>
                        <select 
                          className="w-full p-2 border border-gray-300 rounded mb-3"
                          value={manualCategory}
                          onChange={(e) => setManualCategory(e.target.value)}
                        >
                          {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                        </select>
                        <button onClick={() => analyzeImage(manualCategory)} className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">Confirm Category</button>
                      </div>
                    )}

                    {needsConfirmation && !needsManualSelection && (
                      <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-yellow-800 font-medium mb-3">⚠️ {result.message}</p>
                        <div className="flex space-x-3">
                          <button onClick={() => analyzeImage(result.category)} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Yes, proceed</button>
                          <button onClick={() => { setNeedsConfirmation(false); setNeedsManualSelection(true); }} className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">No, manual selection</button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Final Recommendation */}
                {result.success && !needsConfirmation && !needsManualSelection && (
                  <div className="mt-8 space-y-4">
                    {result.isHazardous && (
                      <div className="p-4 bg-red-100 border-l-4 border-red-500 rounded-r-lg">
                        <p className="text-red-900 font-bold flex items-center">
                          <span className="mr-2">🛑</span> WARNING: Special handling required
                        </p>
                        <p className="text-red-800 text-sm mt-1">This item is classified as E-Waste or Hazardous. Follow verified local disposal guidance strictly to avoid fire or toxic risks.</p>
                      </div>
                    )}
                    
                    <div className="p-5 bg-green-50 border border-green-200 rounded-xl">
                      <h3 className="text-lg font-bold text-green-900 mb-2 flex items-center">
                        <span className="mr-2">💡</span> Disposal Recommendation
                      </h3>
                      <div className="prose prose-green max-w-none text-gray-800 whitespace-pre-line">
                        {result.recommendation}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

        </div>

        {/* Right Column: RAG Trace & Info */}
        <div className="space-y-6">
          
          {/* Debug / RAG Trace */}
          {result && result.success && !needsConfirmation && !needsManualSelection && (
            <div className="bg-gray-900 rounded-xl p-5 text-gray-300 shadow-sm font-mono text-sm">
              <h3 className="text-white font-bold mb-3 border-b border-gray-700 pb-2 flex items-center">
                <span className="mr-2">🔍</span> RAG Evidence Trace
              </h3>
              
              <div className="space-y-4">
                <div>
                  <span className="text-gray-500">Query generated:</span>
                  <p className="text-green-400">"{result.query}"</p>
                </div>
                
                <div>
                  <span className="text-gray-500">Retrieved from Knowledge Base:</span>
                  {result.retrievedInfo && result.retrievedInfo.length > 0 ? (
                    <div className="mt-2 space-y-2">
                      {result.retrievedInfo.map((r: any, idx: number) => (
                        <div key={idx} className="bg-gray-800 p-3 rounded border border-gray-700">
                          <p className="text-xs text-yellow-400 mb-1">Source: {r.source}</p>
                          <p className="text-xs text-blue-300 mb-1">Status: {r.verification}</p>
                          <p className="text-gray-300">{r.disposal_guidance}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-red-400 mt-1">No verified rules found.</p>
                  )}
                </div>
                
                <div>
                  <span className="text-gray-500">LLM Status:</span>
                  <p className="text-gray-300">Grounding context injected. Safety validator checked.</p>
                </div>
              </div>
            </div>
          )}

          {/* Project Fact Sheet / SDG info */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
            <h3 className="font-bold text-gray-900 mb-3 border-b border-gray-100 pb-2">🌍 Project Impact</h3>
            <div className="space-y-3 text-sm">
              <p><span className="font-semibold text-green-700">Primary SDG 12:</span> Responsible Consumption and Production</p>
              <p><span className="font-semibold text-blue-700">Secondary SDGs:</span> 11 (Sustainable Cities), 13 (Climate Action)</p>
              <p className="text-gray-600 mt-2">EcoSort AI reduces "wish-cycling" by combining AI image detection with localized, verified disposal knowledge (RAG).</p>
            </div>
          </div>

          {/* Model Status & Limitations */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
            <h3 className="font-bold text-gray-900 mb-3 border-b border-gray-100 pb-2">⚙️ Model Status</h3>
            <ul className="space-y-2 text-xs text-gray-700 mb-4">
              <li><strong>Vision Engine:</strong> Prototype Demonstration Classifier</li>
              <li><strong>RAG Engine:</strong> Local Token Matching</li>
              <li><strong>Generative AI:</strong> OpenAI / Fallback</li>
              <li><strong>Human-in-loop:</strong> Enabled</li>
            </ul>
            
            <details className="text-xs bg-red-50 p-3 rounded border border-red-100 text-red-800">
              <summary className="font-bold cursor-pointer outline-none">🚨 Prototype Limitations</summary>
              <div className="mt-2 space-y-1">
                <p>• <strong>Vision:</strong> Uses deterministic filename mapping, not real pixel analysis.</p>
                <p>• <strong>Knowledge Base:</strong> Limited coverage prototype DB.</p>
                <p>• <strong>Deployment:</strong> Not for public field use. Ensure local guidelines are verified.</p>
              </div>
            </details>
          </div>

        </div>
      </main>
    </div>
  );
}
