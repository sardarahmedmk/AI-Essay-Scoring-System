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
    """Score essay using ML algorithms"""
    if len(text.strip()) < 10:
        return 1, "Essay too short", {}
    
    metrics = calculate_metrics(text)
    if not metrics:
        return 1, "Error calculating metrics", {}
    
    # Scoring algorithm
    score = 5.0  # Base score
    
    # Word count scoring (15-25% of total)
    word_count = metrics['word_count']
    if word_count >= 150:
        score += 1.5
    elif word_count >= 100:
        score += 1.0
    elif word_count >= 50:
        score += 0.5
    else:
        score -= 1.0
    
    # Vocabulary diversity (20-30% of total)
    vocab_div = metrics['vocab_diversity']
    if vocab_div >= 0.7:
        score += 2.0
    elif vocab_div >= 0.6:
        score += 1.5
    elif vocab_div >= 0.5:
        score += 1.0
    else:
        score -= 0.5
    
    # Sentence structure (15-20% of total)
    avg_sentence = metrics['avg_sentence_length']
    if 12 <= avg_sentence <= 20:
        score += 1.5
    elif 8 <= avg_sentence <= 25:
        score += 1.0
    else:
        score -= 0.5
    
    # Readability (15-20% of total)
    flesch = metrics['flesch_score']
    if flesch >= 60:
        score += 1.0
    elif flesch >= 30:
        score += 0.5
    
    # Final adjustments
    score = max(1, min(10, score))
    
    # Generate feedback
    feedback = generate_feedback(score, metrics)
    
    return round(score, 1), feedback, metrics

def generate_feedback(score, metrics):
    """Generate personalized feedback"""
    feedback = []
    
    if metrics['word_count'] < 150:
        feedback.append("📝 Consider expanding your essay with more details and examples.")
    
    if metrics['vocab_diversity'] >= 0.7:
        feedback.append("🌟 Excellent vocabulary diversity!")
    elif metrics['vocab_diversity'] < 0.5:
        feedback.append("📚 Try using more varied vocabulary to enhance your writing.")
    
    if metrics['avg_sentence_length'] < 10:
        feedback.append("🔗 Try combining some short sentences for better flow.")
    elif metrics['avg_sentence_length'] > 25:
        feedback.append("✂️ Consider breaking down long sentences for clarity.")
    
    if score >= 8:
        feedback.append("🏆 Outstanding essay! Your writing demonstrates excellent skills.")
    elif score >= 6:
        feedback.append("👍 Good essay! A few improvements could make it even better.")
    elif score >= 4:
        feedback.append("📈 Decent essay with room for improvement.")
    else:
        feedback.append("💪 Keep practicing! Writing improves with regular practice.")
    
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
        
        if st.button("📄 Load Sample Essay"):
            sample = SAMPLE_ESSAYS[0]  # Load first sample
            st.session_state.essay_text = sample['text']
            st.success("Sample essay loaded!")
            st.rerun()
        
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
            - **Length:** Aim for 150+ words
            - **Structure:** Introduction, body, conclusion
            - **Vocabulary:** Use varied and sophisticated words
            - **Transitions:** Connect ideas with linking words
            - **Examples:** Support arguments with specific examples
            - **Grammar:** Check for spelling and grammar errors
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
