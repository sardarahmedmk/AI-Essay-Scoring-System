from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainpage.html')

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

Individual actions also play a crucial role in addressing climate change. Simple lifestyle changes like using public transportation, reducing energy consumption, and supporting eco-friendly products can collectively make a substantial impact. Education and awareness campaigns help people understand their role in environmental protection."""
        },
        {
            "title": "Social Media Impact",
            "text": """Social media has revolutionized the way we communicate and connect with others. Platforms like Facebook, Twitter, and Instagram have transformed personal relationships, business interactions, and information sharing. While these technologies offer numerous benefits, they also present significant challenges that society must address.

The spread of misinformation, cyberbullying, and privacy concerns have become major issues. Many users experience decreased face-to-face social skills and increased anxiety from constant comparison with others' curated online personas. Society must find ways to harness the positive aspects of social media while addressing its negative impacts through education and responsible usage."""
        }
    ]
    
    return jsonify({'samples': sample_essays})

@app.route('/score', methods=['POST'])
def score_essay():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided', 'score': '0'}), 400
            
        text = data['text']
        
        # Simple scoring
        word_count = len(text.split())
        score = min(10, max(1, word_count / 20))
        
        return jsonify({
            'score': str(round(score, 1)),
            'feedback': f'Quick score based on {word_count} words. ✅ Server is working!',
            'metrics': {
                'word_count': word_count,
                'sentence_count': max(1, len([s for s in text.split('.') if s.strip()])),
                'unique_words': len(set(text.lower().split())),
                'vocab_diversity': round(len(set(text.lower().split())) / max(1, word_count), 2),
                'avg_sentence_length': round(word_count / max(1, len([s for s in text.split('.') if s.strip()])), 1),
                'avg_word_length': round(sum(len(word) for word in text.split()) / max(1, word_count), 1),
                'flesch_score': 60
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'score': '0'}), 500

if __name__ == '__main__':
    print("🚀 Starting Simple Essay Scoring Server...")
    print("📍 Server will be available at: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
