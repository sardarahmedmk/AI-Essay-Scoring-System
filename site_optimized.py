from flask import Flask, request, render_template, jsonify, send_from_directory
import re
import string
import time
import os
from collections import Counter

# Simple cache for recent results
scoring_cache = {}
CACHE_DURATION = 300  # 5 minutes cache

app = Flask(__name__)

def fast_calculate_metrics(text):
    """Fast and simple metric calculation"""
    try:
        # Use simple string operations for speed
        words = text.split()
        word_count = len(words)
        
        # Simple sentence counting
        sentence_count = max(1, len([s for s in text.split('.') if s.strip()]))
        
        # Quick unique word count
        unique_words = len(set(word.lower().strip(string.punctuation) for word in words))
        
        # Basic averages
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Simple vocabulary diversity
        vocab_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Quick readability approximation (simplified Flesch score)
        asl = avg_sentence_length
        asw = avg_word_length
        flesch_approx = 206.835 - (1.015 * asl) - (84.6 * (asw / 4.7))
        flesch_approx = max(0, min(100, flesch_approx))  # Clamp between 0-100
        
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
        print(f"Error in fast_calculate_metrics: {e}")
        # Return safe defaults
        word_count = len(text.split())
        return {
            'word_count': word_count,
            'sentence_count': max(1, word_count // 15),
            'unique_words': max(1, word_count // 2),
            'vocab_diversity': 0.6,
            'avg_sentence_length': 15,
            'avg_word_length': 5,
            'flesch_score': 60
        }

def fast_score_essay(text):
    """Fast essay scoring algorithm - optimized for speed"""
    start_time = time.time()
    
    # Check cache first
    text_hash = hash(text.strip())
    if text_hash in scoring_cache:
        cache_entry = scoring_cache[text_hash]
        if time.time() - cache_entry['timestamp'] < CACHE_DURATION:
            print(f"Cache hit! Scoring took {time.time() - start_time:.3f} seconds")
            return cache_entry['result']
    
    try:
        if len(text.strip()) < 10:
            return 1, "Essay too short", {}
        
        # Get metrics quickly
        metrics = fast_calculate_metrics(text)
        
        # Fast scoring calculation (simplified)
        word_count = metrics['word_count']
        vocab_diversity = metrics['vocab_diversity']
        avg_sentence_length = metrics['avg_sentence_length']
        flesch_score = metrics['flesch_score']
        
        # Quick scoring components
        # Length score (0-10)
        if word_count < 50:
            length_score = 2
        elif word_count < 150:
            length_score = 6
        elif word_count < 300:
            length_score = 9
        else:
            length_score = 10
        
        # Vocabulary score (0-10)
        vocab_score = min(10, vocab_diversity * 15)
        
        # Structure score (0-10)
        if 10 <= avg_sentence_length <= 25:
            structure_score = 8
        elif 5 <= avg_sentence_length <= 35:
            structure_score = 6
        else:
            structure_score = 4
        
        # Readability score (0-10)
        if 60 <= flesch_score <= 100:
            readability_score = 9
        elif 30 <= flesch_score < 60:
            readability_score = 7
        else:
            readability_score = 5
        
        # Content score (simplified based on word count and diversity)
        content_score = min(10, (word_count / 50) + (vocab_diversity * 10))
        
        # Calculate final score (weighted average)
        final_score = (
            length_score * 0.2 +
            vocab_score * 0.25 + 
            structure_score * 0.2 +
            readability_score * 0.2 +
            content_score * 0.15
        )
        
        final_score = max(1, min(10, round(final_score, 1)))
        
        # Quick feedback generation
        feedback = generate_quick_feedback(final_score, metrics)
        
        result = (final_score, feedback, metrics)
        
        # Cache the result
        scoring_cache[text_hash] = {
            'result': result,
            'timestamp': time.time()
        }
        
        print(f"Fast scoring completed in {time.time() - start_time:.3f} seconds")
        return result
        
    except Exception as e:
        print(f"Error in fast scoring: {e}")
        return 5, "Unable to score essay properly", {}

def generate_quick_feedback(score, metrics):
    """Generate quick feedback based on score and metrics"""
    feedback = []
    
    word_count = metrics.get('word_count', 0)
    vocab_diversity = metrics.get('vocab_diversity', 0)
    avg_sentence_length = metrics.get('avg_sentence_length', 0)
    flesch_score = metrics.get('flesch_score', 0)
    
    # Length feedback
    if word_count < 100:
        feedback.append("📝 Consider expanding your essay with more details and examples.")
    elif word_count > 500:
        feedback.append("✂️ Your essay is quite long. Consider being more concise.")
    else:
        feedback.append("✅ Good essay length!")
    
    # Vocabulary feedback
    if vocab_diversity < 0.4:
        feedback.append("📚 Try using more varied vocabulary to enhance your writing.")
    elif vocab_diversity > 0.7:
        feedback.append("🌟 Excellent vocabulary diversity!")
    else:
        feedback.append("👍 Good vocabulary usage!")
    
    # Sentence structure feedback
    if avg_sentence_length < 8:
        feedback.append("🔗 Try combining some short sentences for better flow.")
    elif avg_sentence_length > 30:
        feedback.append("✂️ Some sentences are quite long. Consider breaking them down.")
    else:
        feedback.append("📐 Good sentence length variety!")
    
    # Overall feedback
    if score >= 8:
        feedback.append("🎉 Excellent work! Your essay demonstrates strong writing skills.")
    elif score >= 6:
        feedback.append("👏 Good essay! A few improvements could make it even better.")
    elif score >= 4:
        feedback.append("📈 Decent effort. Focus on the suggestions above to improve.")
    else:
        feedback.append("💪 Keep practicing! Writing improves with regular practice.")
    
    return " ".join(feedback)

@app.route('/')
def index():
    return render_template('mainpage.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS) from templates directory"""
    if filename.endswith('.css') or filename.endswith('.js'):
        return send_from_directory('templates', filename)
    return "File not found", 404

@app.route('/samples')
def get_samples():
    """Return sample essays for testing"""
    sample_essays = [
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
            "title": "Social Media Impact",
            "text": """Social media has revolutionized the way we communicate and connect with others. Platforms like Facebook, Twitter, and Instagram have transformed personal relationships, business interactions, and information sharing. While these technologies offer numerous benefits, they also present significant challenges that society must address.

On the positive side, social media enables people to maintain relationships across vast distances and connect with like-minded individuals worldwide. It has democratized information sharing, allowing anyone to broadcast news, opinions, and creative content to a global audience. Small businesses can reach customers more effectively, and social movements can organize and spread awareness rapidly.

However, social media also has negative consequences. The spread of misinformation, cyberbullying, and privacy concerns have become major issues. Many users experience decreased face-to-face social skills and increased anxiety from constant comparison with others' curated online personas. The addictive nature of these platforms can lead to decreased productivity and mental health problems.

To maximize benefits while minimizing harm, users must develop digital literacy skills and practice mindful consumption of social media content. Platforms should implement better content moderation and privacy protection measures. Society as a whole must find ways to harness the positive aspects of social media while addressing its negative impacts through education, regulation, and responsible usage."""
        }
    ]
    
    return jsonify({'samples': sample_essays})

@app.route('/score', methods=['POST'])
def score_essay():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No essay text provided',
                'score': '0'
            }), 400
            
        text = data['text']
        print(f"Processing essay with {len(text)} characters")
        
        if not text or len(text.strip()) < 5:
            return jsonify({
                'error': 'Please enter a valid essay (at least 5 characters)',
                'score': '0'
            }), 400
        
        # Use fast scoring function
        score, feedback, metrics = fast_score_essay(text)
        
        result = {
            'score': str(score),
            'feedback': feedback,
            'metrics': {
                'word_count': metrics.get('word_count', 0),
                'sentence_count': metrics.get('sentence_count', 0),
                'unique_words': metrics.get('unique_words', 0),
                'vocab_diversity': round(metrics.get('vocab_diversity', 0), 2),
                'avg_sentence_length': round(metrics.get('avg_sentence_length', 0), 1),
                'avg_word_length': round(metrics.get('avg_word_length', 0), 1),
                'flesch_score': round(metrics.get('flesch_score', 0), 1)
            }
        }
        
        print(f"Fast scoring successful: {score}/10")
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in score_essay: {e}")
        
        return jsonify({
            'error': f'Scoring error: {str(e)}',
            'score': '5',
            'feedback': 'System error occurred. Please try again.',
            'metrics': {
                'word_count': 0,
                'sentence_count': 0,
                'unique_words': 0,
                'vocab_diversity': 0,
                'avg_sentence_length': 0,
                'avg_word_length': 0,
                'flesch_score': 0
            }
        }), 500

if __name__ == '__main__':
    print("Starting Fast Essay Scoring Server...")
    print("Cache enabled: Results cached for 5 minutes")
    app.run(debug=True, host='0.0.0.0', port=5000)
