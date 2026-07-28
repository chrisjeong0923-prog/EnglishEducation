#!/usr/bin/env python3
import os
import json
import re
import random

def clean_word(w):
    return re.sub(r'[^a-z]+', '', w.lower())

def is_option_valid(blank_sentence, option):
    s = blank_sentence.lower()
    o = option.lower()
    
    adjectives = {
        "good", "bad", "tired", "sleepy", "sick", "mad", "pretty", "scary", 
        "big", "small", "sunny", "windy", "rainy", "snowy", "yellow", "red", "blue", "green", "orange", "purple"
    }
    
    singular_nouns = {
        "boy", "girl", "dog", "cat", "horse", "fish", "shark", "coral", "key", 
        "phone", "lamp", "head", "sofa", "car", "rainbow", "weather", "sun", "cloud", "rain", "snow", "wind"
    }
    
    plural_nouns = {"glasses", "clouds", "sharks"}
    prepositions = {"on", "under", "in", "at", "next to", "beside"}
    
    if "i am _____" in s or "he is _____" in s or "she is _____" in s or "feels _____" in s or "is _____ and needs" in s:
        return o in adjectives
        
    if "see a _____" in s or "see a small _____" in s or "see a big _____" in s or "look! i see a _____" in s:
        return o in singular_nouns and o not in plural_nouns
        
    if "see a yellow _____" in s or "see a red _____" in s or "see a blue _____" in s or "see a green _____" in s:
        return o in singular_nouns and o not in plural_nouns

    if "where is my _____" in s or "where is your _____" in s or "is this your _____" in s:
        return o in singular_nouns and o not in plural_nouns

    if "where are my _____" in s:
        return o in plural_nouns

    if "this is my _____" in s:
        return o in singular_nouns and o not in plural_nouns

    if "is _____ the sofa" in s or "is _____ the car" in s or "is _____ the table" in s or "is _____ the bed" in s:
        return o in prepositions

    if "it is _____ outside" in s or "it's a _____ day" in s or "a _____ afternoon" in s:
        return o in {"sunny", "windy", "rainy", "snowy"}

    if "i see _____ clouds" in s:
        return o in {"the", "some"}

    return False

def main():
    print("Generating aligned quizzes...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vocab_path = os.path.join(project_root, 'src', 'data', 'vocabulary.json')
    quizzes_path = os.path.join(project_root, 'src', 'data', 'quizzes.json')

    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)

    # Word-to-lesson mapping for vocabulary quizzes
    lesson_mappings = [
        {
            "id": "hello",
            "pdfUrl": "/lessons/pdf/grade3/hello.pdf",
            "grade": 3,
            "words": ["hello", "boy", "girl", "dog", "he", "she"]
        },
        {
            "id": "how-are-you",
            "pdfUrl": "/lessons/pdf/grade3/how-are-you.pdf",
            "grade": 3,
            "words": ["good", "bad", "tired", "sleepy", "sick", "mad"]
        },
        {
            "id": "look",
            "pdfUrl": "/lessons/pdf/grade3/look.pdf",
            "grade": 3,
            "words": ["look", "dog", "cat", "horse", "big", "small", "see"]
        },
        {
            "id": "what-i-see",
            "pdfUrl": "/lessons/pdf/grade4/what-i-see.pdf",
            "grade": 4,
            "words": ["see", "fish", "sea", "shark", "coral", "scary", "red", "yellow", "blue", "green", "rainbow", "orange", "purple", "dog", "small", "big", "pretty"]
        },
        {
            "id": "where-is-it",
            "pdfUrl": "/lessons/pdf/grade4/where-is-it.pdf",
            "grade": 4,
            "words": ["key", "phone", "glasses", "lamp", "head", "sofa", "car", "on", "under", "my", "your"]
        },
        {
            "id": "how-is-the-weather",
            "pdfUrl": "/lessons/pdf/grade5/how-is-the-weather.pdf",
            "grade": 5,
            "words": ["weather", "sun", "sunny", "cloud", "rain", "rainy", "wind", "windy", "snow", "snowy", "outside"]
        }
    ]

    new_quizzes = []
    
    # 1. Define pre-defined simple grammar quizzes (word-for-word sentence completion)
    grammar_quizzes = [
        # hello
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/hello.pdf",
            "questionText": 'Complete the sentence: "My name _____ Alice."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "My name _____ Alice."',
            "options": ["is", "am", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'In the lesson, we say: "My name is Alice."',
            "explanationKh": 'នៅក្នុងមេរៀន យើងនិយាយថា៖ "My name is Alice."'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/hello.pdf",
            "questionText": 'Complete the sentence: "_____ is a boy."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "_____ is a boy."',
            "options": ["He", "She", "It", "They"],
            "correctAnswer": 0,
            "explanation": 'We use "He" for a boy.',
            "explanationKh": 'យើងប្រើ "He" សម្រាប់ក្មេងប្រុស។'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/hello.pdf",
            "questionText": 'Complete the sentence: "_____ is a girl."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "_____ is a girl."',
            "options": ["She", "He", "It", "They"],
            "correctAnswer": 0,
            "explanation": 'We use "She" for a girl.',
            "explanationKh": 'យើងប្រើ "She" សម្រាប់ក្មេងស្រី។'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/hello.pdf",
            "questionText": 'Complete the sentence: "I _____ a boy."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I _____ a boy."',
            "options": ["am", "is", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'We use "am" with "I".',
            "explanationKh": 'យើងប្រើ "am" ជាមួយ "I"។'
        },
        # how-are-you
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/how-are-you.pdf",
            "questionText": 'Complete the sentence: "I _____ good."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I _____ good."',
            "options": ["am", "is", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'We use "am" with "I".',
            "explanationKh": 'យើងប្រើ "am" ជាមួយ "I"។'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/how-are-you.pdf",
            "questionText": 'Complete the sentence: "He _____ bad."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "He _____ bad."',
            "options": ["is", "am", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'We use "is" for singular third-person.',
            "explanationKh": 'យើងប្រើ "is" សម្រាប់ឯកវចនៈបុរសទីបី។'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/how-are-you.pdf",
            "questionText": 'Complete the sentence: "She _____ tired."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "She _____ tired."',
            "options": ["is", "am", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'We use "is" with "She".',
            "explanationKh": 'យើងប្រើ "is" ជាមួយ "She"។'
        },
        # look
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/look.pdf",
            "questionText": 'Complete the sentence: "I _____ a small cat."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I _____ a small cat."',
            "options": ["see", "sees", "seeing", "is see"],
            "correctAnswer": 0,
            "explanation": 'We use "see" with "I".',
            "explanationKh": 'យើងប្រើ "see" ជាមួយ "I"។'
        },
        {
            "grade": 3,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade3/look.pdf",
            "questionText": 'Complete the sentence: "The horse _____ big."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "The horse _____ big."',
            "options": ["is", "am", "are", "be"],
            "correctAnswer": 0,
            "explanation": 'We use "is" for a singular animal.',
            "explanationKh": 'យើងប្រើ "is" សម្រាប់សត្វឯកវចនៈ។'
        },
        # what-i-see
        {
            "grade": 4,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade4/what-i-see.pdf",
            "questionText": 'Complete the sentence: "I see _____ big sharks."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I see _____ big sharks."',
            "options": ["two", "a two", "two a", "a"],
            "correctAnswer": 0,
            "explanation": 'When plural, we do not use the article "a". The correct phrase is "two big sharks".',
            "explanationKh": 'នៅពេលនាមជាពហុវចនៈ យើងមិនប្រើ "a" ទេ។ ឃ្លាត្រឹមត្រូវគឺ "two big sharks"។'
        },
        {
            "grade": 4,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade4/what-i-see.pdf",
            "questionText": 'Complete the sentence: "I see _____ yellow fish."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I see _____ yellow fish."',
            "options": ["a", "an", "two a", "a two"],
            "correctAnswer": 0,
            "explanation": 'For a singular noun starting with a consonant sound, we use "a".',
            "explanationKh": 'សម្រាប់នាមឯកវចនៈដែលចាប់ផ្តើមដោយព្យញ្ជនៈ យើងប្រើ "a"។'
        },
        # where-is-it
        {
            "grade": 4,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade4/where-is-it.pdf",
            "questionText": 'Complete the sentence: "Where _____ my glasses?"',
            "questionTextKh": 'បំពេញប្រយោគ៖ "Where _____ my glasses?"',
            "options": ["are", "is", "am", "be"],
            "correctAnswer": 0,
            "explanation": '"Glasses" is plural, so we use "are".',
            "explanationKh": '"Glasses" ជានាមពហុវចនៈ ដូច្នេះយើងប្រើ "are"។'
        },
        {
            "grade": 4,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade4/where-is-it.pdf",
            "questionText": 'Complete the sentence: "My phone is _____ the sofa."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "My phone is _____ the sofa."',
            "options": ["on", "under", "in", "at"],
            "correctAnswer": [0, 1],
            "explanation": 'The phone is resting on top of the sofa.',
            "explanationKh": 'ទូរស័ព្ទស្ថិតនៅលើសាឡុង។'
        },
        {
            "grade": 4,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade4/where-is-it.pdf",
            "questionText": 'Complete the sentence: "The key is _____ the car."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "The key is _____ the car."',
            "options": ["under", "on", "in", "at"],
            "correctAnswer": [0, 1],
            "explanation": 'The key is underneath the car.',
            "explanationKh": 'កូនសោស្ថិតនៅក្រោមឡាន។'
        },
        # how-is-the-weather
        {
            "grade": 5,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade5/how-is-the-weather.pdf",
            "questionText": 'Complete the sentence: "It is _____ outside."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "It is _____ outside."',
            "options": ["sunny", "sun", "sun\'s", "sunny a"],
            "correctAnswer": 0,
            "explanation": 'We use the adjective "sunny" to describe the weather.',
            "explanationKh": 'យើងប្រើគុណនាម "sunny" ដើម្បីពិពណ៌នាអំពីអាកាសធាតុ។'
        },
        {
            "grade": 5,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade5/how-is-the-weather.pdf",
            "questionText": 'Complete the sentence: "I see _____ clouds."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I see _____ clouds."',
            "options": ["the", "a", "an", "some"],
            "correctAnswer": [0, 3],
            "explanation": 'We say "the clouds" when referring to clouds.',
            "explanationKh": 'យើងនិយាយថា "the clouds" នៅពេលសំដៅលើពពក។'
        },
        {
            "grade": 5,
            "type": "grammar",
            "pdfUrl": "/lessons/pdf/grade5/how-is-the-weather.pdf",
            "questionText": 'Complete the sentence: "I see _____."',
            "questionTextKh": 'បំពេញប្រយោគ៖ "I see _____."',
            "options": ["rain", "the rain", "rains", "a rain"],
            "correctAnswer": 0,
            "explanation": 'We say "I see rain" without using "the" or adding "s".',
            "explanationKh": 'យើងនិយាយថា "I see rain" ដោយមិនប្រើ "the" ឬបន្ថែម "s" ទេ។'
        }
    ]

    new_quizzes.extend(grammar_quizzes)

    # 2. Generate simple vocabulary quizzes by blanking out the vocabulary words themselves
    for mapping in lesson_mappings:
        pdf_url = mapping["pdfUrl"]
        grade = mapping["grade"]
        target_words = mapping["words"]

        # Filter vocabulary entries belonging to this lesson
        matched_vocab = []
        for word_name in target_words:
            entries = [v for v in vocab_data if v['grade'] == grade and clean_word(v['word']) == clean_word(word_name)]
            if entries:
                matched_vocab.append(entries[0])
            
        random.seed(42)
        random.shuffle(matched_vocab)

        # Generate vocabulary quizzes (up to 5 per lesson)
        quizzes_count = 0
        for vocab in matched_vocab:
            if quizzes_count >= 5:
                break

            word = vocab['word']
            example = vocab['example']
            example_kh = vocab['exampleKh']

            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            if not pattern.search(example):
                pattern = re.compile(re.escape(word), re.IGNORECASE)

            if not pattern.search(example):
                continue

            blank_sentence = pattern.sub("_____", example)

            # Select distractors from the same lesson only (don't go past words outlined in the PDF)
            lesson_vocab = [w for w in target_words if clean_word(w) != clean_word(word)]
            lesson_vocab = list(set(lesson_vocab))
            
            if len(lesson_vocab) < 3:
                # Fallback to same grade if not enough words in this lesson
                lesson_vocab = [v['word'] for v in vocab_data if v['grade'] == grade and clean_word(v['word']) != clean_word(word)]
                lesson_vocab = list(set(lesson_vocab))

            distractors = random.sample(lesson_vocab, 3)
            options = [word] + distractors
            random.shuffle(options)
            
            # Find all correct answers (either matching the target word, or is another grammatically valid choice)
            correct_answers = [idx for idx, opt in enumerate(options) if clean_word(opt) == clean_word(word) or is_option_valid(blank_sentence, opt)]

            new_quiz = {
                "grade": grade,
                "type": "vocabulary",
                "pdfUrl": pdf_url,
                "questionText": f'Complete the sentence: "{blank_sentence}"',
                "questionTextKh": f'បំពេញប្រយោគ៖ "{blank_sentence}"',
                "options": options,
                "correctAnswer": correct_answers,
                "explanation": f'In the lesson, we read: "{example}"',
                "explanationKh": f'នៅក្នុងមេរៀន យើងបានអាន៖ "{example}" ({example_kh})'
            }

            new_quizzes.append(new_quiz)
            quizzes_count += 1

        print(f"  -> Generated {quizzes_count} vocabulary quizzes for {mapping['id']}")

    # Write new quizzes to quizzes.json
    with open(quizzes_path, 'w', encoding='utf-8') as f:
        json.dump(new_quizzes, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully regenerated {len(new_quizzes)} quizzes and saved to src/data/quizzes.json")

if __name__ == "__main__":
    main()
