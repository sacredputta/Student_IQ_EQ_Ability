import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Initialize tools
# Note: On first run, LanguageTool might take a moment to download java files
tool = language_tool_python.LanguageTool('en-US')
sentiment_analyser = SentimentIntensityAnalyzer()

def count_words(text):
    return len(text.split())

def analyze_salutation(text):
    text_lower = text.lower()
    
    if any(x in text_lower for x in ["excited to introduce", "feeling great"]):
        return 5, "Excellent salutation"
    elif any(x in text_lower for x in ["good morning", "good afternoon", "good evening"]):
        return 4, "Good salutation"
    elif any(x in text_lower for x in ["hi", "hello"]):
        return 2, "Basic salutation"
    
    return 0, "No salutation"

def analyze_keywords(text):
    text_lower = text.lower()
    score = 0
    found_keywords = []
    
    must_haves = {
        "Name": ["myself", "my name is", "i am"],
        "Age": ["years old", "age is"],
        "School/Class": ["studying in", "class", "school", "grade", "college", "university"],
        "Family": ["family", "mother", "father", "parents", "sister", "brother"],
        "Hobbies": ["hobby", "hobbies", "interest", "enjoy", "like to", "playing"]
    }
    
    for category, keywords in must_haves.items():
        if any(k in text_lower for k in keywords):
            score += 4  # FIXED: was 'scire'
            found_keywords.append(category)
            
    # Cap basic score at 20
    score = min(score, 20)
    
    good_to_haves = {
        "Origin": ["i am from", "come from", "native", "born in"],
        "Ambition": ["goal", "dream", "ambition", "became a", "aspire"],
        "Unique Fact": ["fun fact", "special thing", "unique", "secret", "don't know about me"],
        "Strengths": ["strength", "good at", "confident", "skill"]
    }        
    
    good_score = 0
    for category, keywords in good_to_haves.items():
        if any(k in text_lower for k in keywords): # FIXED: was 'andy'
            good_score += 2
            found_keywords.append(category)
            
    # Add bonus score
    score += min(good_score, 10) # FIXED: was '=+'
    
    return score, f"Found keywords: {', '.join(found_keywords)}"

def analyze_flow(text):
    text_lower = text.lower()
    
    salutation_markers = ["hi", "hello", "good morning", "good afternoon"]
    name_markers = ["my name", "myself", "i am"]
    closing_markers = ["thank you", "thanks", "that's all"] # FIXED: was 'thankes'
    
    # Finding Positions
    salutation_idx = -1
    for m in salutation_markers:
        idx = text_lower.find(m)
        if idx != -1:
            salutation_idx = idx
            break
        
    name_idx = -1  
    for m in name_markers:
        idx = text_lower.find(m)
        if idx != -1:
            name_idx = idx
            break          
        
    closing_idx = -1
    for m in closing_markers:
        idx = text_lower.find(m)
        if idx != -1:
            closing_idx = idx
            break
        
    if salutation_idx != -1 and name_idx != -1 and closing_idx != -1:
        if salutation_idx < name_idx < closing_idx:
            return 5, "Perfect flow Followed"
    
    return 0, "Flow order not optimal or missing sections"

def analyze_speech_rate(text, duration_seconds):
    if not duration_seconds or duration_seconds <= 0:
        return 0, "Invalid duration"
    
    word_count = count_words(text)
    wpm = (word_count / duration_seconds) * 60
    wpm = round(wpm)
    
    if 111 <= wpm <= 140:
        return 10, f"Ideal pace ({wpm} WPM)"
    elif 141 <= wpm <= 160:
        return 6, f"Fast pace ({wpm} WPM)"
    elif 81 <= wpm <= 110:
        return 6, f"Slow pace ({wpm} WPM)"
    elif wpm > 160:
        return 2, f"Too fast ({wpm} WPM)"
    else:
        return 2, f"Too slow ({wpm} WPM)"
    
def analyze_grammar(text): # FIXED: spelling of 'grammar'
    matches = tool.check(text)
    error_count = len(matches)
    word_count = count_words(text) 
    
    if word_count == 0: return 0, "No text"    
    
    errors_per_100 = (error_count * 100) / word_count
    grammar_metric = 1 - min(errors_per_100 / 10, 1)    
    
    if grammar_metric > 0.9:
        score = 10
    elif 0.7 <= grammar_metric <= 0.89:
        score = 8
    elif 0.5 <= grammar_metric <= 0.69:
        score = 6
    elif 0.3 <= grammar_metric <= 0.49:
        score = 4
    else:
        score = 2    
        
    return score, f"Grammar Score: {round(grammar_metric, 2)} (Errors: {error_count})"

def analyze_vocabulary(text):
    words = text.lower().split()
    if not words: return 0, "No text"
    
    unique_words = set(words)
    ttr = len(unique_words) / len(words) 
    
    if 0.9 <= ttr <= 1.0:
        score = 10
    elif 0.7 <= ttr <= 0.89:
        score = 8
    elif 0.5 <= ttr <= 0.69:
        score = 6
    elif 0.3 <= ttr <= 0.49:
        score = 4
    else:
        score = 2
        
    return score, f"TTR Score: {round(ttr, 2)}"

def analyze_clarity(text):
    # FIXED: Defined as 'fillers' to match the variable used below
    fillers = ["um", "uh", "like", "you know", "so", "actually", "basically", "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]           
    words = text.lower().split()
    if not words: return 0, "No text"
    
    filler_count = sum(1 for w in words if w in fillers)
    filler_rate = (filler_count / len(words)) * 100
    
    if 0 <= filler_rate <= 3:
        score = 15
    elif 4 <= filler_rate <= 6:
        score = 12
    elif 7 <= filler_rate <= 9:
        score = 9
    elif 10 <= filler_rate <= 12:
        score = 6
    else:
        score = 3
        
    return score, f"Filler Rate: {round(filler_rate, 1)}% ({filler_count} fillers)" 

def analyze_engagement(text):
    scores = sentiment_analyser.polarity_scores(text)
    positivity = scores['compound']
    metric = positivity
      
    if metric >= 0.5:
        score = 15
    elif 0.3 <= metric < 0.5:
        score = 12
    elif 0.1 <= metric < 0.3:
        score = 9
    elif -0.1 <= metric < 0.1:
        score = 6
    else:
        score = 3  
        
    return score, f"Sentiment Score: {round(metric, 2)}"

def calculate_total_score(text, duration_seconds):
    salutation_score, sal_msg = analyze_salutation(text)
    keyword_score, key_msg = analyze_keywords(text)
    flow_score, flow_msg = analyze_flow(text)
    speech_score, speech_msg = analyze_speech_rate(text, duration_seconds)
    grammar_score, gram_msg = analyze_grammar(text)
    vocab_score, vocab_msg = analyze_vocabulary(text)
    clarity_score, clarity_msg = analyze_clarity(text)
    engage_score, engage_msg = analyze_engagement(text)

    total_score = (
        salutation_score + keyword_score + flow_score + speech_score + grammar_score + vocab_score + clarity_score + engage_score
    )
        
    return {
        "total_score": total_score,
        "Salutation_Score": salutation_score,
        "Keyword_Score": keyword_score,
        "Flow_Score": flow_score,
        "Speech_Score": speech_score,
        "Grammar_Score": grammar_score,
        "Vocabolary_Score": vocab_score,
        "Clarity_Score": clarity_score,
        "Engagement_Score": engage_score
    }    


if __name__ == "__main__":
    
    sample_text = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
    I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father. 
    One special thing about my family is that they are very kind hearted to everyone and soft spoken. 
    One thing I really enjoy is playing cricket and taking wickets.
    A fun fact about me is that I see in mirror and talk by myself. 
    One thing people don't know about me is that I once stole a toy from one of my cousin.
    My favorite subject is science because it is very interesting. 
    Through science I can explore the whole world and make the discoveries and improve the lives of others.
    Thank you for listening."""
    
    duration = 53 
    
    
    result = calculate_total_score(sample_text, duration)
    
    
    print(json.dumps(result, indent=4))