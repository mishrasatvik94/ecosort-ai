import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import OpenAI from 'openai';

// 1. Prototype Demonstration Classifier
const MOCK_MAPPING: Record<string, [string, number]> = {
  "banana": ["Organic", 0.92],
  "apple": ["Organic", 0.88],
  "bottle": ["Plastic", 0.85],
  "mobile": ["E-Waste", 0.96],
  "battery": ["E-Waste", 0.95],
  "box": ["Paper", 0.82],
  "bleach": ["Hazardous", 0.90],
  "diaper": ["Sanitary", 0.89],
  "glass": ["Glass", 0.84],
  "paper": ["Paper", 0.87],
  "can": ["Metal", 0.81],
  "unknown": ["Other/Unknown", 0.30],
  "blurry": ["Other/Unknown", 0.45]
};

const CATEGORIES = ["Organic", "Plastic", "E-Waste", "Paper", "Hazardous", "Sanitary", "Glass", "Metal", "Other/Unknown"];

function predictCategory(filename: string): { category: string; confidence: number } {
  const name = filename.toLowerCase();
  for (const [key, [cat, conf]] of Object.entries(MOCK_MAPPING)) {
    if (name.includes(key)) {
      return { category: cat, confidence: conf };
    }
  }
  // Fallback random
  const randomCat = CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)];
  const randomConf = parseFloat((Math.random() * (0.99 - 0.4) + 0.4).toFixed(2));
  return { category: randomCat, confidence: randomConf };
}

// 2. RAG Engine
function tokenize(text: string): Set<string> {
  const words = text.toLowerCase().match(/\w+/g) || [];
  const stopwords = new Set(["a", "an", "the", "and", "or", "to", "in", "of", "for", "is"]);
  return new Set(words.filter(w => !stopwords.has(w)));
}

function retrieveRules(query: string) {
  // Use path relative to this file so it works both locally and on Vercel
  const filePath = path.join(process.cwd(), 'data', 'disposal_rules.json');
  const altFilePath = path.join(__dirname, '..', '..', '..', '..', 'data', 'disposal_rules.json');
  let rules = [];
  try {
    const targetPath = require('fs').existsSync(filePath) ? filePath : altFilePath;
    const data = fs.readFileSync(targetPath, 'utf-8');
    rules = JSON.parse(data);
  } catch (e) {
    console.error("Failed to load disposal_rules.json", e);
    // Return built-in fallback rules so app never fully fails
    rules = [
      { item: "banana peel", category: "Organic", disposal_guidance: "Place in green waste / compost bin.", handling: "Keep covered to avoid pests.", safety_warning: "None.", source: "Built-in fallback", verification: "Prototype knowledge base" },
      { item: "plastic bottle", category: "Plastic", disposal_guidance: "Empty, rinse, place in blue recycling bin.", handling: "Remove caps if required locally.", safety_warning: "None.", source: "Built-in fallback", verification: "Prototype knowledge base" },
      { item: "battery", category: "E-Waste", disposal_guidance: "DO NOT throw in regular trash. Take to a certified e-waste drop-off.", handling: "Tape terminals to prevent short circuits.", safety_warning: "High fire risk if punctured or crushed.", source: "Built-in fallback", verification: "Prototype knowledge base" },
      { item: "glass bottle", category: "Glass", disposal_guidance: "Place in glass recycling bin. Sort by color if required.", handling: "Handle with care — risk of breakage and cuts.", safety_warning: "Do not break glass.", source: "Built-in fallback", verification: "Prototype knowledge base" },
    ];
  }

  const queryTokens = tokenize(query);
  if (queryTokens.size === 0) return [];

  const scores = rules.map((rule: any) => {
    const text = `${rule.item || ''} ${rule.category || ''}`;
    const docTokens = tokenize(text);
    const intersection = new Set([...queryTokens].filter(x => docTokens.has(x)));
    const score = intersection.size / (queryTokens.size + 0.1);
    return { score, rule };
  });

  scores.sort((a: any, b: any) => b.score - a.score);
  return scores.filter((s: any) => s.score > 0).map((s: any) => s.rule).slice(0, 2);
}

// 3. Safety Validator
const DANGEROUS_KEYWORDS = ["burn", "drink", "eat", "flush", "bury", "flush down the toilet", "mix with bleach"];
function validateResponse(text: string): boolean {
  const lower = text.toLowerCase();
  for (const keyword of DANGEROUS_KEYWORDS) {
    if (lower.includes(keyword)) return false;
  }
  return true;
}

// 4. API Route
export async function POST(req: Request) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;
    const manualCategory = formData.get('manualCategory') as string | null;
    
    if (!file && !manualCategory) {
      return NextResponse.json({ error: 'File is required' }, { status: 400 });
    }

    const filename = file ? file.name : "manual_item";
    let category = "";
    let confidence = 0;

    if (manualCategory) {
      category = manualCategory;
      confidence = 1.0;
    } else {
      const prediction = predictCategory(filename);
      category = prediction.category;
      confidence = prediction.confidence;
    }

    // Human in the loop checks
    if (!manualCategory) {
      if (confidence < 0.50) {
        return NextResponse.json({ 
          needsManualSelection: true, 
          message: `Low Confidence (${confidence}). AI is uncertain.`,
          confidence,
          category
        });
      }
      if (confidence < 0.80) {
        return NextResponse.json({ 
          needsConfirmation: true, 
          message: `Moderate Confidence. The AI thinks this is ${category}. Is this correct?`,
          confidence,
          category
        });
      }
    }

    // Process RAG
    let itemName = filename.split(".")[0].replace(/_/g, " ");
    itemName = itemName.charAt(0).toUpperCase() + itemName.slice(1);
    
    const query = `${itemName} ${category}`;
    const retrievedInfo = retrieveRules(query);

    // Process LLM
    let recommendation = "";
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (apiKey) {
      const openai = new OpenAI({ apiKey });
      const systemPrompt = `You are EcoSort AI. Provide waste disposal guidance.
Rules:
1. Use retrieved info as primary basis.
2. If info is insufficient, say EXACTLY: "I don't have enough verified information to provide a definitive disposal recommendation."
3. No dangerous instructions.`;
      
      const userPrompt = `Item: ${itemName}
Category: ${category}
Retrieved Info: ${JSON.stringify(retrievedInfo)}`;
      
      try {
        const response = await openai.chat.completions.create({
          model: "gpt-3.5-turbo",
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt }
          ]
        });
        recommendation = response.choices[0]?.message?.content || "";
      } catch (e) {
        console.error("OpenAI API failed, falling back to mock", e);
        recommendation = ""; // Triggers fallback
      }
    }

    // Mock Fallback if no API key or API failed
    if (!recommendation) {
      if (retrievedInfo.length === 0) {
        recommendation = "I don't have enough verified information to provide a definitive disposal recommendation.";
      } else {
        const bestMatch = retrievedInfo[0];
        recommendation = `Action: ${bestMatch.disposal_guidance}\nWhy: ${bestMatch.handling}\nSafety: ${bestMatch.safety_warning}`;
      }
    }

    if (!validateResponse(recommendation)) {
      recommendation = "ERROR: Generated response violated safety guidelines. Please follow local municipal guidelines.";
    }

    return NextResponse.json({
      success: true,
      category,
      confidence,
      itemName,
      query,
      retrievedInfo,
      recommendation,
      isHazardous: category === "E-Waste" || category === "Hazardous"
    });

  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
