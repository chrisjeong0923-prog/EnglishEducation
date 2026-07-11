#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "python-dotenv",
# ]
# ///
import os
import re
import sys
import json
import shutil
import base64
import urllib.request

# Try to load python-dotenv, fallback to manual parsing of .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual parser for .env
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()


def main():
    print("=" * 60)
    print("🧠 Kids English Academy - AI PDF Material Generator 🧠")
    print("=" * 60)

    # 1. Load Gemini API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ Error: GEMINI_API_KEY not found in environment or .env file.")
        print("Please check that your project root contains a '.env' file with:")
        print("GEMINI_API_KEY=your_gemini_api_key_here\n")
        sys.exit(1)

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    data_dir = os.path.join(project_root, 'src', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    lessons_json = os.path.join(data_dir, 'lessons.json')
    vocab_json = os.path.join(data_dir, 'vocabulary.json')
    quizzes_json = os.path.join(data_dir, 'quizzes.json')
    listening_json = os.path.join(data_dir, 'listening.json')

    # Helper to check/initialize empty JSON arrays
    for path in [lessons_json, vocab_json, quizzes_json, listening_json]:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    # 2. Get User Inputs
    pdf_path = input("📂 Enter the path to your PDF lesson file: ").strip()
    # Handle terminal drag-and-drop escaping (e.g. spaces, parentheses escaped with backslashes or wrapped in quotes)
    pdf_path = pdf_path.strip("'\"")
    pdf_path = re.sub(r'\\(.)', r'\1', pdf_path)

    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at '{pdf_path}'")
        sys.exit(1)

    try:
        grade = int(input("🏫 Enter the grade level (3, 4, 5, or 6): ").strip())
        if grade not in [3, 4, 5, 6]:
            raise ValueError
    except ValueError:
        print("❌ Error: Grade level must be 3, 4, 5, or 6.")
        sys.exit(1)

    title = input("📝 Enter the lesson title in English: ").strip()
    if not title:
        print("❌ Error: Lesson title cannot be empty.")
        sys.exit(1)

    title_kh = input("📝 Enter the lesson title in Khmer [Leave blank for AI translation]: ").strip()
    desc = input("💬 Enter a short description in English: ").strip()
    desc_kh = input("💬 Enter a short description in Khmer [Leave blank for AI translation]: ").strip()

    # Generate slug from English title
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    custom_slug = input(f"🔖 Enter unique lesson slug ID [default: {slug}]: ").strip()
    if custom_slug:
        slug = custom_slug

    # 3. Read PDF file binary data
    print("\n📖 Reading PDF file binary data...")
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        print(f"✅ Loaded PDF file ({len(pdf_bytes)} bytes) and encoded in Base64.")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        sys.exit(1)

    # 4. Generate Materials using Gemini REST API
    print("🤖 Contacting Gemini AI to generate flashcards, quizzes, and translations...")
    
    prompt = f"""You are a professional ESL (English as a Second Language) curriculum developer.
Analyze the attached lesson PDF visually and contextually.
Based on this lesson, generate the following learning materials and translations:
1. Translate the English lesson title '{title}' and description '{desc}' into natural, grade-appropriate Khmer.
2. "vocabulary": A list of 5 to 10 vocabulary words found in the text. Provide word, ipa phonetic transcription, type (must be "noun", "verb", "adjective", or "adverb"), fitting emoji, English definition, Khmer translation definition, English example sentence, and Khmer translation example.
3. "quizzes": A list of 3 to 5 multiple-choice questions (grammar or vocabulary type). Provide questionText, questionTextKh, options (exactly 4 strings), correctAnswer (0-indexed integer choice), explanation in English, and explanationKh in Khmer.
4. "listening": A list of 1 to 3 listening exercise sentences. Provide title, titleKh, text (the actual spelling sentence read aloud), clue hint, and clueKh hint translation.

You MUST conform to the JSON schema specified in responseSchema. Return only valid JSON."""

    # Schema configuration matching data files
    body = {
        "contents": [{
            "parts": [
                { "text": prompt },
                {
                    "inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_b64
                    }
                }
            ]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "titleKh": { "type": "STRING", "description": "Grade-appropriate Khmer translation of the English lesson title" },
                    "descriptionKh": { "type": "STRING", "description": "Grade-appropriate Khmer translation of the English description" },
                    "vocabulary": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "word": { "type": "STRING" },
                                "ipa": { "type": "STRING" },
                                "type": { "type": "STRING", "enum": ["noun", "verb", "adjective", "adverb"] },
                                "emoji": { "type": "STRING", "description": "Single emoji character" },
                                "definition": { "type": "STRING" },
                                "definitionKh": { "type": "STRING" },
                                "example": { "type": "STRING" },
                                "exampleKh": { "type": "STRING" }
                            },
                            "required": ["word", "type", "emoji", "definition", "definitionKh", "example", "exampleKh"]
                        }
                    },
                    "quizzes": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "type": { "type": "STRING", "enum": ["grammar", "vocabulary"] },
                                "questionText": { "type": "STRING" },
                                "questionTextKh": { "type": "STRING" },
                                "options": { "type": "ARRAY", "items": { "type": "STRING" } },
                                "correctAnswer": { "type": "INTEGER" },
                                "explanation": { "type": "STRING" },
                                "explanationKh": { "type": "STRING" }
                            },
                            "required": ["type", "questionText", "questionTextKh", "options", "correctAnswer", "explanation", "explanationKh"]
                        }
                    },
                    "listening": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "title": { "type": "STRING" },
                                "titleKh": { "type": "STRING" },
                                "text": { "type": "STRING" },
                                "clue": { "type": "STRING" },
                                "clueKh": { "type": "STRING" }
                            },
                            "required": ["title", "titleKh", "text", "clue", "clueKh"]
                        }
                    }
                },
                "required": ["titleKh", "descriptionKh", "vocabulary", "quizzes", "listening"]
            }
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    # Handle SSL verification context (workaround for macOS python cert issue)
    import ssl
    ssl_context = None
    try:
        ssl_context = ssl.create_default_context()
    except AttributeError:
        pass

    try:
        try:
            response = urllib.request.urlopen(req, context=ssl_context)
        except Exception as ssl_err:
            if "CERTIFICATE_VERIFY_FAILED" in str(ssl_err):
                unverified_context = ssl._create_unverified_context()
                response = urllib.request.urlopen(req, context=unverified_context)
            else:
                raise ssl_err

        with response:
            res_body = json.loads(response.read().decode('utf-8'))
            json_text = res_body['candidates'][0]['content']['parts'][0]['text']
            generated = json.loads(json_text)
            print("✅ Successfully generated learning content and translations from AI!")
    except Exception as e:
        print(f"❌ Error communicating with Gemini API: {e}")
        if hasattr(e, 'read'):
            try:
                print(f"API Response: {e.read().decode('utf-8')}")
            except Exception:
                pass
        sys.exit(1)

    # 5. File Operations
    print("\n📂 Staging and writing files locally...")

    # Copy PDF
    dest_dir = os.path.join(project_root, 'public', 'lessons', 'pdf', f'grade{grade}')
    os.makedirs(dest_dir, exist_ok=True)
    pdf_dest_path = os.path.join(dest_dir, f"{slug}.pdf")
    shutil.copy(pdf_path, pdf_dest_path)
    print(f"  -> Copied PDF to: public/lessons/pdf/grade{grade}/{slug}.pdf")

    # Resolve Khmer translations if left blank
    actual_title_kh = title_kh if title_kh else generated.get('titleKh', title)
    actual_desc_kh = desc_kh if desc_kh else generated.get('descriptionKh', desc)

    # Update lessons.json
    try:
        with open(lessons_json, 'r', encoding='utf-8') as f:
            lessons_data = json.load(f)
        
        new_lesson = {
            "id": slug,
            "grade": grade,
            "title": title,
            "titleKh": actual_title_kh,
            "description": desc,
            "descriptionKh": actual_desc_kh,
            "content": f"Study materials generated from PDF lesson \"{title}\". Download the attached PDF to review full reading materials.",
            "contentKh": f"ឯកសារសិក្សាត្រូវបានបង្កើតចេញពីមេរៀន PDF \"{title}\"។ សូមទាញយកឯកសារ PDF ដែលភ្ជាប់មកជាមួយដើម្បីពិនិត្យឡើងវិញនូវខ្លឹមសារពេញលេញ។",
            "pdfUrl": f"/lessons/pdf/grade{grade}/{slug}.pdf"
        }
        
        # Deduplicate
        lessons_data = [l for l in lessons_data if l['id'] != slug]
        lessons_data.append(new_lesson)
        
        with open(lessons_json, 'w', encoding='utf-8') as f:
            json.dump(lessons_data, f, indent=2, ensure_ascii=False)
        print("  -> Updated lessons.json")
    except Exception as e:
        print(f"❌ Error writing lessons.json: {e}")

    # Update vocabulary.json
    try:
        with open(vocab_json, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
        
        new_words = []
        for w in generated.get('vocabulary', []):
            new_words.append({
                "grade": grade,
                "word": w['word'],
                "ipa": w.get('ipa', ''),
                "type": w['type'],
                "emoji": w.get('emoji', '📖'),
                "definition": w['definition'],
                "definitionKh": w['definitionKh'],
                "example": w['example'],
                "exampleKh": w['exampleKh']
            })
            
        # Deduplicate based on word name and grade
        new_word_names = [w['word'].lower() for w in new_words]
        vocab_data = [w for w in vocab_data if not (w['grade'] == grade and w['word'].lower() in new_word_names)]
        vocab_data.extend(new_words)

        with open(vocab_json, 'w', encoding='utf-8') as f:
            json.dump(vocab_data, f, indent=2, ensure_ascii=False)
        print(f"  -> Added {len(new_words)} words to vocabulary.json")
    except Exception as e:
        print(f"❌ Error writing vocabulary.json: {e}")

    # Update quizzes.json
    try:
        with open(quizzes_json, 'r', encoding='utf-8') as f:
            quizzes_data = json.load(f)

        new_quizzes = []
        for q in generated.get('quizzes', []):
            new_quizzes.append({
                "grade": grade,
                "type": q['type'],
                "questionText": q['questionText'],
                "questionTextKh": q['questionTextKh'],
                "options": q['options'],
                "correctAnswer": q['correctAnswer'],
                "explanation": q['explanation'],
                "explanationKh": q['explanationKh']
            })

        # Deduplicate based on questionText and grade
        new_questions_list = [q['questionText'].lower() for q in new_quizzes]
        quizzes_data = [q for q in quizzes_data if not (q['grade'] == grade and q['questionText'].lower() in new_questions_list)]
        quizzes_data.extend(new_quizzes)

        with open(quizzes_json, 'w', encoding='utf-8') as f:
            json.dump(quizzes_data, f, indent=2, ensure_ascii=False)
        print(f"  -> Added {len(new_quizzes)} quizzes to quizzes.json")
    except Exception as e:
        print(f"❌ Error writing quizzes.json: {e}")

    # Update listening.json
    try:
        with open(listening_json, 'r', encoding='utf-8') as f:
            listening_data = json.load(f)

        next_id = max([item.get('id', 0) for item in listening_data] + [0]) + 1
        level_label = f"Level {grade - 2}"
        level_kh_label = {3: 'កម្រិត ១', 4: 'កម្រិត ២', 5: 'កម្រិត ៣', 6: 'កម្រិត ៤'}.get(grade, 'កម្រិត ១')

        new_listening = []
        for l in generated.get('listening', []):
            new_listening.append({
                "id": next_id,
                "title": l['title'],
                "titleKh": l['titleKh'],
                "difficulty": level_label,
                "difficultyKh": level_kh_label,
                "text": l['text'],
                "clue": l['clue'],
                "clueKh": l['clueKh']
            })
            next_id += 1

        listening_data.extend(new_listening)

        with open(listening_json, 'w', encoding='utf-8') as f:
            json.dump(listening_data, f, indent=2, ensure_ascii=False)
        print(f"  -> Added {len(new_listening)} dictations to listening.json")
    except Exception as e:
        print(f"❌ Error writing listening.json: {e}")

    print("=" * 60)
    print("🎉 SUCCESS! Local files updated successfully.")
    if title_kh == "" or desc_kh == "":
        print(f"🤖 AI Khmer Title generated: \"{actual_title_kh}\"")
        print(f"🤖 AI Khmer Desc generated: \"{actual_desc_kh}\"")
    print("You can verify changes by checking the local dev server at:")
    print("👉 http://localhost:4321/EnglishEducation")
    print("=" * 60)

    # Optional Git Push Automation
    publish = input("\n🚀 Do you want to publish these changes to the live site now? (y/n) [default: n]: ").strip().lower()
    if publish == 'y':
        print("\n⚙️ Running Git publish commands...")
        try:
            import subprocess
            # Stage changes
            subprocess.run(["git", "add", "."], check=True, cwd=project_root)
            # Commit changes
            commit_msg = f"CMS Update: Added lesson \"{title}\" and generated materials"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd=project_root)
            # Push changes
            subprocess.run(["git", "push"], check=True, cwd=project_root)
            print("\n✅ Successfully committed and pushed to GitHub!")
            print("GitHub Actions is now rebuilding and deploying your site live.")
            print("It will be online in 1-2 minutes.")
        except Exception as e:
            print(f"\n❌ Error during Git publish: {e}")
            print("You may need to run 'git push' manually.")


if __name__ == "__main__":
    main()
