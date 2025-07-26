import streamlit as st
import re
import string
import time
from collections import Counter

# Set page configuration
st.set_page_config(
    page_title="🚀 AI Essay Scoring System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glass-morphism design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card {
        background: rgba(102, 126, 234, 0.1);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 5px;
    }
    
    .score-excellent { 
        background: linear-gradient(135deg, #11998e, #38ef7d); 
        color: white; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .score-good { 
        background: linear-gradient(135deg, #4facfe, #00f2fe); 
        color: white; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .score-average { 
        background: linear-gradient(135deg, #fa709a, #fee140); 
        color: white; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .score-poor { 
        background: linear-gradient(135deg, #ff6a6a, #ee0979); 
        color: white; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .suggestion-item {
        background: white;
        padding: 12px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 3px solid #28a745;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .best-essay-section {
        background: rgba(220, 248, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'essay_text' not in st.session_state:
    st.session_state.essay_text = ""
if 'score_result' not in st.session_state:
    st.session_state.score_result = None

# Sample essays data
SAMPLE_ESSAYS = [
    {
        "title": "Technology in Education",
        "text": """Education is one of the most important aspects of human development. It provides us with knowledge, skills, and values that shape our understanding of the world. Through education, we learn to think critically, solve problems, and communicate effectively with others.

In today's rapidly changing world, education must adapt to meet new challenges. Technology has transformed how we learn and access information. Students now have access to vast amounts of knowledge through the internet, online courses, and digital resources.

However, traditional classroom learning remains valuable. The interaction between teachers and students, group discussions, and collaborative projects foster social skills and emotional intelligence. A balanced approach that combines both traditional and modern educational methods would be most effective.

In conclusion, education should continue to evolve while maintaining its core purpose of developing well-rounded individuals who can contribute positively to society."""
    },
    {
        "title": "Climate Change Solutions",
        "text": """Climate change represents one of the most pressing challenges of our time. Rising global temperatures, melting ice caps, and extreme weather events are clear indicators that immediate action is required. However, with proper planning and commitment, we can implement effective solutions to mitigate these effects.

Renewable energy sources such as solar, wind, and hydroelectric power offer promising alternatives to fossil fuels. These technologies have become increasingly efficient and cost-effective, making them viable options for widespread adoption. Governments and businesses worldwide must invest in renewable infrastructure to reduce carbon emissions significantly.

Individual actions also play a crucial role in addressing climate change. Simple lifestyle changes like using public transportation, reducing energy consumption, and supporting eco-friendly products can collectively make a substantial impact. Education and awareness campaigns help people understand their role in environmental protection.

Furthermore, international cooperation is essential for tackling this global issue. Countries must work together to establish and enforce environmental regulations, share clean technologies, and support developing nations in their transition to sustainable practices. Only through coordinated global efforts can we hope to reverse the effects of climate change and preserve our planet for future generations."""
    },
    {
        "title": "Short Essay Test",
        "text": """This is a short essay. It has very few words. The vocabulary is simple. The sentences are short. This should get a low score."""
    }
]

# Best essays for examples
BEST_ESSAYS = [
    {
        "topic": "Education",
        "text": """Education serves as the cornerstone of personal development and societal progress. In today's rapidly evolving world, the importance of quality education cannot be overstated, as it shapes not only individual futures but also the collective destiny of nations.

Firstly, education empowers individuals with critical thinking skills essential for navigating complex challenges. Through rigorous academic training, students learn to analyze information, evaluate evidence, and formulate well-reasoned arguments. For instance, students studying science develop hypothesis-testing abilities that prove invaluable in professional problem-solving scenarios.

Moreover, education fosters innovation and creativity by exposing learners to diverse perspectives and methodologies. Universities and educational institutions serve as incubators for groundbreaking research and technological advancement. The collaboration between students and faculty often leads to discoveries that revolutionize entire industries.

Furthermore, education promotes social mobility and equality by providing opportunities regardless of socioeconomic background. Scholarship programs and accessible learning platforms ensure that talented individuals can pursue their aspirations despite financial constraints. This democratization of knowledge strengthens society's fabric by utilizing human potential more effectively.

In conclusion, education remains humanity's most powerful tool for progress. By investing in comprehensive educational systems, societies ensure sustainable development, innovation, and equality for future generations. The transformative power of education extends far beyond individual achievement, creating ripples of positive change throughout communities worldwide.""",
        "score": 9.5
    }
]

def calculate_metrics(text):
    """Calculate comprehensive essay metrics"""
    try:
        words = text.split()
        word_count = len(words)
        
        # Simple sentence counting
        sentence_count = max(1, len([s for s in text.split('.') if s.strip()]))
        
        # Unique word count
        unique_words = len(set(word.lower().strip(string.punctuation) for word in words))
        
        # Basic averages
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Vocabulary diversity
        vocab_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Quick readability approximation
        flesch_approx = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 4.7))
        flesch_approx = max(0, min(100, flesch_approx))
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'unique_words': unique_words,
            'vocab_diversity': vocab_diversity,
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'flesch_score': flesch_approx
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        return {}

def score_essay(text):
    """Score essay using realistic ML algorithms"""
    if len(text.strip()) < 10:
        return 1, "Essay too short", {}
    
    metrics = calculate_metrics(text)
    if not metrics:
        return 1, "Error calculating metrics", {}
    
    # More realistic scoring algorithm - starts from 0
    score = 0.0
    
    # Word count scoring (25% of total score)
    word_count = metrics['word_count']
    if word_count >= 250:
        score += 2.5  # Excellent length
    elif word_count >= 200:
        score += 2.2  # Very good length
    elif word_count >= 150:
        score += 1.8  # Good length
    elif word_count >= 100:
        score += 1.3  # Adequate length
    elif word_count >= 50:
        score += 0.8  # Short but acceptable
    else:
        score += 0.2  # Too short
    
    # Vocabulary diversity (25% of total score)
    vocab_div = metrics['vocab_diversity']
    if vocab_div >= 0.8:
        score += 2.5  # Exceptional diversity
    elif vocab_div >= 0.7:
        score += 2.0  # Excellent diversity
    elif vocab_div >= 0.6:
        score += 1.5  # Good diversity
    elif vocab_div >= 0.5:
        score += 1.0  # Average diversity
    elif vocab_div >= 0.4:
        score += 0.6  # Below average
    else:
        score += 0.2  # Poor diversity
    
    # Sentence structure (25% of total score)
    avg_sentence = metrics['avg_sentence_length']
    sentence_count = metrics['sentence_count']
    
    # Penalize very short essays heavily
    if sentence_count < 3:
        score += 0.2
    elif sentence_count < 5:
        score += 0.8
    elif 5 <= sentence_count <= 8:
        score += 1.5
    elif 9 <= sentence_count <= 15:
        score += 2.0
    elif 16 <= sentence_count <= 25:
        score += 2.3
    else:
        score += 1.8
    
    # Sentence length quality
    if 15 <= avg_sentence <= 22:
        score += 0.5  # Bonus for ideal sentence length
    elif 10 <= avg_sentence <= 28:
        score += 0.2  # Acceptable sentence length
    elif avg_sentence < 8:
        score -= 0.3  # Too short sentences
    elif avg_sentence > 35:
        score -= 0.3  # Too long sentences
    
    # Content quality indicators (25% of total score)
    content_score = 0.0
    
    # Check for structure indicators
    structure_words = ['firstly', 'secondly', 'thirdly', 'furthermore', 'moreover', 
                      'however', 'therefore', 'in conclusion', 'finally', 'additionally']
    structure_count = sum(1 for word in structure_words if word in text.lower())
    
    if structure_count >= 3:
        content_score += 1.0
    elif structure_count >= 2:
        content_score += 0.7
    elif structure_count >= 1:
        content_score += 0.4
    
    # Check for examples and evidence
    example_words = ['example', 'instance', 'such as', 'for example', 'demonstrate', 
                    'illustrate', 'evidence', 'research', 'study', 'data']
    example_count = sum(1 for word in example_words if word in text.lower())
    
    if example_count >= 3:
        content_score += 0.8
    elif example_count >= 2:
        content_score += 0.5
    elif example_count >= 1:
        content_score += 0.3
    
    # Check for advanced vocabulary
    advanced_words = ['significant', 'substantial', 'comprehensive', 'fundamental', 
                     'essential', 'critical', 'substantial', 'demonstrate', 'establish',
                     'consequently', 'nevertheless', 'furthermore', 'substantial']
    advanced_count = sum(1 for word in advanced_words if word in text.lower())
    
    if advanced_count >= 4:
        content_score += 0.7
    elif advanced_count >= 2:
        content_score += 0.4
    elif advanced_count >= 1:
        content_score += 0.2
    
    score += min(content_score, 2.5)  # Cap content score at 2.5
    
    # Apply penalties for common issues
    if metrics['word_count'] < 100:
        score *= 0.7  # Major penalty for very short essays
    
    if vocab_div < 0.3:
        score *= 0.8  # Penalty for very repetitive writing
    
    # Readability bonus/penalty
    flesch = metrics['flesch_score']
    if 60 <= flesch <= 80:
        score += 0.3  # Good readability
    elif 40 <= flesch <= 90:
        score += 0.1  # Acceptable readability
    elif flesch < 20 or flesch > 95:
        score -= 0.2  # Poor readability
    
    # Final score adjustment and capping
    score = max(1, min(10, score))
    
    # Generate feedback
    feedback = generate_feedback(score, metrics)
    
    return round(score, 1), feedback, metrics

def generate_feedback(score, metrics):
    """Generate realistic personalized feedback"""
    feedback = []
    
    # Word count feedback
    word_count = metrics['word_count']
    if word_count < 100:
        feedback.append("📝 Your essay is quite short. Aim for at least 150-200 words to fully develop your ideas.")
    elif word_count < 150:
        feedback.append("� Consider expanding your essay with more details, examples, and explanations.")
    elif word_count >= 250:
        feedback.append("📚 Excellent essay length! You have sufficient space to develop your arguments.")
    
    # Vocabulary diversity feedback
    vocab_div = metrics['vocab_diversity']
    if vocab_div >= 0.7:
        feedback.append("🌟 Outstanding vocabulary diversity! Your word choice demonstrates strong writing skills.")
    elif vocab_div >= 0.6:
        feedback.append("📖 Good vocabulary diversity. Try incorporating more sophisticated words.")
    elif vocab_div >= 0.5:
        feedback.append("📚 Average vocabulary usage. Work on using more varied and precise word choices.")
    else:
        feedback.append("⚠️ Low vocabulary diversity detected. Avoid repeating the same words frequently.")
    
    # Sentence structure feedback
    avg_sentence = metrics['avg_sentence_length']
    sentence_count = metrics['sentence_count']
    
    if sentence_count < 5:
        feedback.append("📊 Your essay needs more sentences to fully develop ideas. Aim for at least 8-12 sentences.")
    elif avg_sentence < 10:
        feedback.append("🔗 Try combining some short sentences using conjunctions for better flow.")
    elif avg_sentence > 30:
        feedback.append("✂️ Some sentences are quite long. Break them down for better clarity and readability.")
    elif 15 <= avg_sentence <= 22:
        feedback.append("✅ Excellent sentence structure! Your sentences are well-balanced.")
    
    # Overall score feedback
    if score >= 9:
        feedback.append("🏆 Exceptional essay! This demonstrates advanced writing skills and excellent content development.")
    elif score >= 7.5:
        feedback.append("🌟 Excellent work! Your essay shows strong writing abilities with room for minor improvements.")
    elif score >= 6:
        feedback.append("👍 Good essay! With some enhancements, this could be even more compelling.")
    elif score >= 4.5:
        feedback.append("📈 Decent foundation. Focus on expanding content and improving structure.")
    elif score >= 3:
        feedback.append("💪 Keep practicing! Work on essay length, vocabulary, and organization.")
    else:
        feedback.append("📝 This essay needs significant improvement. Focus on length, structure, and content development.")
    
    # Specific improvement suggestions based on score
    if score < 6:
        feedback.append("💡 Suggestions: Add more examples, use transition words, and expand your arguments with evidence.")
    
    return " ".join(feedback)

def generate_suggestions(text):
    """Generate improvement suggestions"""
    words = text.strip().split()
    sentences = text.split('.') if text else []
    suggestions = []
    
    if len(words) < 150:
        suggestions.append({
            'icon': '📏',
            'text': 'Your essay is quite short. Consider adding more detailed examples and explanations to reach at least 150 words for better scoring.'
        })
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    if avg_sentence_length < 10:
        suggestions.append({
            'icon': '🔗',
            'text': 'Try using longer, more complex sentences to show advanced writing skills. Combine related ideas with conjunctions.'
        })
    
    if not any(word in text.lower() for word in ['firstly', 'secondly', 'furthermore', 'conclusion']):
        suggestions.append({
            'icon': '📋',
            'text': 'Use transition words like "Firstly", "Moreover", "Furthermore", "In conclusion" to improve essay structure.'
        })
    
    if not any(word in text.lower() for word in ['example', 'instance']):
        suggestions.append({
            'icon': '💡',
            'text': 'Include specific examples to support your arguments and make them more convincing.'
        })
    
    if not suggestions:
        suggestions.append({
            'icon': '✅',
            'text': 'Great job! Your essay follows good writing practices. Consider adding more sophisticated vocabulary for even better scoring.'
        })
    
    return suggestions

# Main app
def main():
    # Header
    st.markdown("""
    <div class="glass-card">
        <h1 style="text-align: center; color: white; font-size: 2.5rem;">
            🚀 AI-Powered Essay Scoring & Enhancement System
        </h1>
        <p style="text-align: center; color: white; font-size: 1.2rem;">
            Get instant scoring, personalized suggestions, and see examples of excellent essays
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        # Sample essay selector
        sample_choice = st.selectbox(
            "📄 Choose Sample Essay:",
            options=["Select a sample..."] + [essay['title'] for essay in SAMPLE_ESSAYS],
            index=0
        )
        
        if sample_choice != "Select a sample...":
            for essay in SAMPLE_ESSAYS:
                if essay['title'] == sample_choice:
                    if st.button(f"Load: {sample_choice}"):
                        st.session_state.essay_text = essay['text']
                        st.success(f"'{sample_choice}' loaded!")
                        st.rerun()
                    break
        
        if st.button("⭐ Show Best Essay"):
            best_essay = BEST_ESSAYS[0]
            st.markdown(f"""
            <div class="best-essay-section">
                <h4>🌟 Example of Excellent Essay</h4>
                <p><strong>Topic:</strong> {best_essay['topic']} | <strong>Score:</strong> {best_essay['score']}/10</p>
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; max-height: 200px; overflow-y: auto;">
                    {best_essay['text'][:500]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("💡 Writing Tips"):
            st.markdown("""
            ### ✍️ Essay Writing Tips
            - **Length:** Aim for 150+ words (200+ for high scores)
            - **Structure:** Introduction, body, conclusion
            - **Vocabulary:** Use varied and sophisticated words
            - **Transitions:** Connect ideas with linking words
            - **Examples:** Support arguments with specific examples
            - **Grammar:** Check for spelling and grammar errors
            - **Sentences:** Mix short and long sentences (15-22 words avg)
            """)
        
        # Score explanation
        st.markdown("### 📊 Scoring Guide")
        st.markdown("""
        **Score Ranges:**
        - 9-10: Exceptional (A+)
        - 7.5-8.9: Excellent (A)
        - 6-7.4: Good (B)
        - 4.5-5.9: Average (C)
        - 3-4.4: Below Average (D)
        - 1-2.9: Poor (F)
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ✍️ Write Your Essay")
        
        # Essay input
        essay_text = st.text_area(
            "",
            value=st.session_state.essay_text,
            height=300,
            placeholder="""Start writing your essay here...

Tips for better scoring:
• Write at least 150 words
• Use varied vocabulary
• Include clear introduction, body, and conclusion
• Check for grammar and spelling errors
• Use transition words between paragraphs""",
            key="essay_input"
        )
        
        # Update session state
        st.session_state.essay_text = essay_text
        
        # Word counter
        word_count = len(essay_text.split()) if essay_text else 0
        char_count = len(essay_text)
        st.caption(f"Words: {word_count} | Characters: {char_count}")
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🎯 Score & Analyze", type="primary"):
                if essay_text.strip():
                    with st.spinner("Analyzing your essay with AI..."):
                        score, feedback, metrics = score_essay(essay_text)
                        st.session_state.score_result = {
                            'score': score,
                            'feedback': feedback,
                            'metrics': metrics
                        }
                        st.success("Essay analyzed successfully!")
                        st.rerun()
                else:
                    st.error("Please enter some text first!")
        
        with col_btn2:
            if st.button("💡 Get Suggestions"):
                if essay_text.strip():
                    suggestions = generate_suggestions(essay_text)
                    st.markdown("### 🔍 Improvement Suggestions")
                    for suggestion in suggestions:
                        st.markdown(f"""
                        <div class="suggestion-item">
                            {suggestion['icon']} {suggestion['text']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Please enter some text first!")
        
        with col_btn3:
            if st.button("📊 Quick Stats"):
                if essay_text.strip():
                    metrics = calculate_metrics(essay_text)
                    st.markdown("### 📈 Quick Statistics")
                    # Use metrics in a single column to avoid nesting issues
                    st.metric("Words", metrics['word_count'])
                    st.metric("Sentences", metrics['sentence_count'])
                    st.metric("Unique Words", metrics['unique_words'])
                    st.metric("Vocab Diversity", f"{metrics['vocab_diversity']:.2%}")
    
    with col2:
        st.markdown("### 📋 Enhancement Tips")
        st.markdown("""
        <div class="glass-card">
            <p>✅ Use varied sentence structures</p>
            <p>✅ Include specific examples</p>
            <p>✅ Use transition words</p>
            <p>✅ Avoid repetitive vocabulary</p>
            <p>✅ Clear topic sentences</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Results section
    if st.session_state.score_result:
        result = st.session_state.score_result
        
        st.markdown("### 📊 Essay Analysis Results")
        
        # Score display
        score = result['score']
        if score >= 8:
            score_class = "score-excellent"
        elif score >= 6:
            score_class = "score-good"
        elif score >= 4:
            score_class = "score-average"
        else:
            score_class = "score-poor"
        
        st.markdown(f"""
        <div class="{score_class}">
            {score}/10
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        metrics = result['metrics']
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric("Word Count", metrics['word_count'])
        with col_m2:
            st.metric("Sentences", metrics['sentence_count'])
        with col_m3:
            st.metric("Unique Words", metrics['unique_words'])
        with col_m4:
            st.metric("Avg Sentence Length", f"{metrics['avg_sentence_length']:.1f}")
        
        # Feedback
        st.markdown("### 💬 AI Feedback")
        st.info(result['feedback'])

if __name__ == "__main__":
    main()
