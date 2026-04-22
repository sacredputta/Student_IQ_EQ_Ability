# Student IQ/EQ Ability Assessment Tool

An AI-powered communication and self-introduction analyzer that evaluates student transcripts on multiple dimensions including vocabulary, emotional intelligence, speech pacing, and overall communication quality.

---

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [How It Works](#how-it-works)
5. [API Endpoints](#api-endpoints)
6. [Scoring Criteria](#scoring-criteria)
7. [Running the Application](#running-the-application)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Basic understanding of Flask and REST APIs

### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask app: `python app.py`
4. Open your browser to `http://localhost:5000`

---

## 📦 Installation

### Step 1: Install Python Dependencies

```bash
pip install flask
pip install language-tool-python
pip install vaderSentiment
```

### Step 2: Verify Installation

Test that all modules are properly installed:

```bash
python -c "import flask; import language_tool_python; from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer; print('All dependencies installed successfully!')"
```

---

## 🏗️ Project Structure

```
Student_IQ_EQ_Ability/
├── app.py              # Flask application & API endpoints
├── logic.py            # Core analysis logic & scoring functions
├── index.html          # Frontend UI for user input
└── README.md           # Documentation (this file)
```

### File Descriptions

#### `app.py` - Flask Backend
- Serves the HTML frontend
- Defines the `/analyze` endpoint that accepts transcript data
- Calls the `calculate_total_score()` function from `logic.py`
- Returns structured JSON responses

#### `logic.py` - Analysis Engine
Contains the core logic with these analysis functions:

| Function | Purpose |
|----------|---------|
| `analyze_salutation()` | Evaluates greeting quality and warmth |
| `analyze_keywords()` | Identifies essential and bonus information (name, age, school, family, hobbies, goals) |
| `analyze_flow()` | Checks logical flow: salutation → name → closing |
| `analyze_speech_rate()` | Calculates words per minute and optimal pacing |
| `analyze_sentiment()` | Uses VADER sentiment analysis for emotional tone |
| `analyze_grammar()` | Identifies grammar and spelling errors |
| `calculate_total_score()` | Combines all analyses into final score |

#### `index.html` - Frontend UI
- Responsive web interface for transcript input
- Duration input field
- Real-time result display with visual feedback
- Category-wise score breakdown

---

## 🔍 How It Works

### User Journey

```
Select Transcript
      ↓
Enter Duration (seconds)
      ↓
Click "Analyze Score"
      ↓
Frontend sends POST request to /analyze
      ↓
Backend processes with logic.py functions
      ↓
Returns JSON response with scores
      ↓
Results displayed in frontend
```

### Analysis Pipeline

The system evaluates transcripts across 6 dimensions:

1. **Salutation Quality** (up to 5 points)
   - Looks for warm greetings
   - Examples: "excited to introduce", "good morning"

2. **Keyword Coverage** (up to 30 points)
   - **Must-haves** (20 points max): Name, Age, School, Family, Hobbies
   - **Good-to-haves** (10 points max): Origin, Ambition, Unique facts, Strengths

3. **Speech Flow** (up to 5 points)
   - Checks proper sequencing: Greeting → Introduction → Closing

4. **Speech Rate** (up to 15 points)
   - Optimal: 130-150 words/minute
   - Evaluated against duration input

5. **Sentiment Analysis** (up to 15 points)
   - VADER sentiment scores translated to point scale
   - Positive sentiment rewarded

6. **Grammar & Spelling** (up to 15 points)
   - LanguageTool identifies errors
   - Fewer errors = higher score

**Total Possible Score: 100 points**

---

## 🔌 API Endpoints

### POST `/analyze`
Analyzes a transcript and returns detailed scores.

**Request Format:**
```json
{
  "transcript": "Hello everyone, my name is John...",
  "duration": 52
}
```

**Response Format:**
```json
{
  "total_score": 78,
  "salutation": {
    "score": 4,
    "feedback": "Good salutation"
  },
  "keywords": {
    "score": 24,
    "feedback": "Found keywords: Name, Age, School, Family, Hobbies, Ambition"
  },
  "flow": {
    "score": 5,
    "feedback": "Perfect flow Followed"
  },
  "speech_rate": {
    "score": 12,
    "feedback": "83 words/min - Good pace"
  },
  "sentiment": {
    "score": 14,
    "feedback": "Overall positive sentiment detected"
  },
  "grammar": {
    "score": 9,
    "feedback": "3 grammar/spelling errors found"
  }
}
```

**Error Responses:**
```json
{ "error": "No transcript provided" }  // 400
{ "error": "Invalid duration format" }  // 400
{ "error": "Internal server error" }    // 500
```

---

## 📊 Scoring Criteria

### Detailed Scoring Breakdown

#### Salutation (5 points max)
| Input | Score | Category |
|-------|-------|----------|
| "excited to introduce", "feeling great" | 5 | Excellent |
| "good morning", "good afternoon" | 4 | Good |
| "hi", "hello" | 2 | Basic |
| None | 0 | Missing |

#### Keywords (30 points max)
**Must-Have Categories** (4 points each, max 20):
- Personal name
- Age
- School/Class/College
- Family
- Hobbies

**Good-to-Have Categories** (2 points each, max 10):
- Place of origin
- Career ambitions/goals
- Unique personal facts
- Personal strengths

#### Flow (5 points)
- Perfect order: Greeting → Name → Closing = 5 points
- Suboptimal order or missing sections = 0 points

#### Speech Rate (15 points)
- Optimal range: 130-150 words/minute
- Score decreases with deviation from optimal range

#### Sentiment (15 points)
- VADER compound score converted to 0-15 scale
- Positive sentiment: higher scores
- Negative sentiment: lower scores

#### Grammar & Spelling (15 points)
- Starts at 15, deducts for each error found
- Uses LanguageTool for detection

---

## ▶️ Running the Application

### Step 1: Start the Flask Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 2: Open in Browser
Navigate to: `http://localhost:5000`

### Step 3: Test with Sample Input
```
Transcript: "Good morning everyone! My name is Sarah and I'm 16 years old. I study in class 10 at XYZ School. I live with my family including my parents and younger brother. My hobbies include reading and playing badminton. I dream of becoming a software engineer. Thank you!"

Duration: 30 seconds
```

### Step 4: View Results
The interface will display:
- Total score (0-100)
- Individual category scores
- Specific feedback for improvement

---

## 🔧 Troubleshooting

### ModuleNotFoundError: No module named 'language_tool_python'
**Solution:** Install the missing dependency
```bash
pip install language-tool-python
```

### ModuleNotFoundError: No module named 'vaderSentiment'
**Solution:** Install VADER sentiment analyzer
```bash
pip install vaderSentiment
```

### Port 5000 already in use
**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### LanguageTool taking time on first run
**Solution:** LanguageTool downloads Java libraries on first use. This may take 1-2 minutes. Subsequent runs will be faster.

---

## 📈 Future Enhancements

- [ ] Add confidence scores to each category
- [ ] Implement user progress tracking
- [ ] Add audio file support for real speech analysis
- [ ] Create comparative analytics dashboard
- [ ] Add multi-language support
- [ ] Implement ML-based category detection

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

Created for student communication assessment and improvement.
