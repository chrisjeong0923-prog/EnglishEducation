import fs from 'fs';
import path from 'path';

// 1. Simple parser for local .env file (so we don't depend on npm dotenv package)
function loadEnv() {
  try {
    const envPath = path.resolve(process.cwd(), '.env');
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, 'utf8');
      envContent.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;
        const eqIdx = trimmed.indexOf('=');
        if (eqIdx > 0) {
          const key = trimmed.substring(0, eqIdx).trim();
          let val = trimmed.substring(eqIdx + 1).trim();
          if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
            val = val.slice(1, -1);
          }
          process.env[key] = val;
        }
      });
    }
  } catch (error) {
    console.error('Error loading .env file:', error);
  }
}

loadEnv();

const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
if (!ELEVENLABS_API_KEY) {
  console.error('❌ Error: ELEVENLABS_API_KEY not found in environment or .env file!');
  process.exit(1);
}

// 2. Data definition for vocabulary words
const vocabWords = [
  // Grade 3
  "Happy", "Apple", "Jump", "Sun", "Read", "Clean", "Water", "Run", "Green",
  // Grade 4
  "Explore", "Courage", "Curious", "Journey", "Protect", "Brave", "Discover", "Library", "Gentle",
  // Grade 5
  "Gather", "Scribble", "Peculiar", "Sweet", "Travel", "Forest", "Healthy", "Build", "Island",
  // Grade 6
  "Generous", "Predict", "Obstacle", "Neighbor", "Search", "Famous", "Whisper", "Shadow", "Pleasant"
];

// 3. Data definition for listening exercises
const listeningExercises = [
  { id: 1, text: "The little cat chased the ball across the floor." },
  { id: 2, text: "Please remember to wash your hands before eating lunch." },
  { id: 3, text: "We saw a colorful rainbow in the sky after the rain stopped." },
  { id: 4, text: "The students worked together to build a magnificent sandcastle on the beach." }
];

// ElevenLabs Configuration
const VOICE_ID = 'pNInz6obpgDQGcFmaJgB'; // Adam - deep male narrator (free tier compatible)
const API_URL = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`;

// Helper to make API request and save file
async function generateSpeech(text, outputPath) {
  console.log(`Generating audio for: "${text}" -> ${path.basename(outputPath)}`);
  
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': ELEVENLABS_API_KEY,
    },
    body: JSON.stringify({
      text: text,
      model_id: 'eleven_multilingual_v2',
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75
      }
    })
  });

  if (!response.ok) {
    const errorDetails = await response.text();
    throw new Error(`API call failed (${response.status}): ${errorDetails}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  fs.writeFileSync(outputPath, buffer);
}

async function main() {
  const publicDir = path.resolve(process.cwd(), 'public');
  const vocabDir = path.join(publicDir, 'audio', 'vocab');
  const listeningDir = path.join(publicDir, 'audio', 'listening');

  // Create directories if they don't exist
  fs.mkdirSync(vocabDir, { recursive: true });
  fs.mkdirSync(listeningDir, { recursive: true });

  console.log('🎙️ Starting ElevenLabs audio pre-generation...\n');

  // Generate Vocabulary Pronunciations
  console.log('--- Step 1: Generating Vocabulary Audio ---');
  for (const word of vocabWords) {
    const filename = `${word.toLowerCase()}.mp3`;
    const destPath = path.join(vocabDir, filename);

    if (fs.existsSync(destPath)) {
      console.log(`✓ Vocab audio for "${word}" already exists. Skipping.`);
      continue;
    }

    try {
      await generateSpeech(word, destPath);
      // Brief pause to respect rate limits
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`❌ Failed to generate audio for "${word}":`, error.message);
    }
  }

  console.log('\n--- Step 2: Generating Listening Exercises Audio ---');
  for (const ex of listeningExercises) {
    const filename = `${ex.id}.mp3`;
    const destPath = path.join(listeningDir, filename);

    if (fs.existsSync(destPath)) {
      console.log(`✓ Listening audio for exercise ${ex.id} already exists. Skipping.`);
      continue;
    }

    try {
      await generateSpeech(ex.text, destPath);
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`❌ Failed to generate audio for exercise ${ex.id}:`, error.message);
    }
  }

  console.log('\n🎉 Audio generation completed!');
}

main().catch(err => {
  console.error('Fatal error running script:', err);
  process.exit(1);
});
