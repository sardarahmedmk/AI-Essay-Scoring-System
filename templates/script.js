// 🚀 Advanced Essay Scoring & Enhancement System - JavaScript

let sampleEssays = [];
let bestEssays = [
    {
        topic: "Education",
        text: `Education serves as the cornerstone of personal development and societal progress. In today's rapidly evolving world, the importance of quality education cannot be overstated, as it shapes not only individual futures but also the collective destiny of nations.

Firstly, education empowers individuals with critical thinking skills essential for navigating complex challenges. Through rigorous academic training, students learn to analyze information, evaluate evidence, and formulate well-reasoned arguments. For instance, students studying science develop hypothesis-testing abilities that prove invaluable in professional problem-solving scenarios.

Moreover, education fosters innovation and creativity by exposing learners to diverse perspectives and methodologies. Universities and educational institutions serve as incubators for groundbreaking research and technological advancement. The collaboration between students and faculty often leads to discoveries that revolutionize entire industries.

Furthermore, education promotes social mobility and equality by providing opportunities regardless of socioeconomic background. Scholarship programs and accessible learning platforms ensure that talented individuals can pursue their aspirations despite financial constraints. This democratization of knowledge strengthens society's fabric by utilizing human potential more effectively.

In conclusion, education remains humanity's most powerful tool for progress. By investing in comprehensive educational systems, societies ensure sustainable development, innovation, and equality for future generations. The transformative power of education extends far beyond individual achievement, creating ripples of positive change throughout communities worldwide.`,
        score: 9.5
    },
    {
        topic: "Technology",
        text: `The digital revolution has fundamentally transformed human civilization, reshaping how we communicate, work, and perceive reality. As we stand at the threshold of unprecedented technological advancement, it becomes crucial to examine both the profound benefits and potential challenges that technology presents to society.

Technology has democratized access to information and education on an unprecedented scale. Online learning platforms, digital libraries, and educational applications have made knowledge accessible to millions who previously lacked such opportunities. Students in remote areas can now attend virtual lectures from world-renowned institutions, breaking down geographical barriers to quality education.

Additionally, technological innovations have revolutionized healthcare delivery and outcomes. Telemedicine enables doctors to diagnose and treat patients across vast distances, while artificial intelligence assists in early disease detection and personalized treatment plans. Medical devices and digital health monitoring systems have empowered individuals to take proactive control of their well-being.

However, the rapid pace of technological change also presents significant challenges. Privacy concerns, digital addiction, and the potential displacement of traditional employment require careful consideration and proactive solutions. Society must develop frameworks that harness technology's benefits while mitigating its risks.

In conclusion, technology represents both humanity's greatest opportunity and its most complex challenge. By fostering responsible innovation, promoting digital literacy, and maintaining human-centered values, we can ensure that technological progress serves the greater good while preserving the qualities that make us fundamentally human.`,
        score: 9.8
    }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Essay Scoring System Initialized');
    
    // Load samples from server
    loadSamplesFromServer();
    
    // Initialize word counter
    initializeWordCounter();
    
    // Initialize auto-hide functionality
    initializeAutoHide();
});

// Load samples from server
function loadSamplesFromServer() {
    fetch('/samples')
        .then(response => response.json())
        .then(data => {
            sampleEssays = data.samples;
            console.log('✅ Loaded samples:', sampleEssays.length);
        })
        .catch(error => {
            console.error('❌ Error loading samples:', error);
        });
}

// Initialize word counter functionality
function initializeWordCounter() {
    const essayTextarea = document.getElementById('essay');
    if (essayTextarea) {
        essayTextarea.addEventListener('input', updateWordCounter);
        // Trigger initial count
        essayTextarea.dispatchEvent(new Event('input'));
    }
}

// Update word counter
function updateWordCounter() {
    const text = document.getElementById('essay').value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    
    const counter = document.getElementById('word-counter');
    if (counter) {
        counter.textContent = `Words: ${words} | Characters: ${chars}`;
    }
}

// Initialize auto-hide functionality
function initializeAutoHide() {
    const essayTextarea = document.getElementById('essay');
    if (essayTextarea) {
        essayTextarea.addEventListener('input', function() {
            if (this.value.trim() === '') {
                hideAllResults();
            }
        });
    }
}

// Hide all result sections
function hideAllResults() {
    const sections = ['results', 'suggestions', 'best-essay'];
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'none';
        }
    });
}

// Load sample essay
function loadSample() {
    if (sampleEssays.length > 0) {
        const randomIndex = Math.floor(Math.random() * sampleEssays.length);
        const essay = sampleEssays[randomIndex].text;
        
        document.getElementById('essay').value = essay;
        document.getElementById('essay').dispatchEvent(new Event('input'));
        
        console.log('✅ Sample essay loaded');
        
        // Show success message
        showToast('Sample essay loaded successfully!', 'success');
    } else {
        showToast('No samples available. Please make sure the server is running.', 'error');
    }
}

// Score essay function
function scoreEssay() {
    const text = document.getElementById('essay').value;
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    
    if (!text.trim()) {
        showToast('Please enter some text', 'warning');
        return;
    }
    
    // Show loading
    if (loadingDiv) loadingDiv.style.display = 'block';
    if (resultsDiv) resultsDiv.style.display = 'none';
    
    console.log('🔄 Scoring essay with', text.length, 'characters');
    
    fetch('/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        console.log('📡 Response status:', response.status);
        return response.json();
    })
    .then(result => {
        console.log('📊 Full result:', result);
        
        // Hide loading
        if (loadingDiv) loadingDiv.style.display = 'none';
        
        if (result.error) {
            showToast('Error: ' + result.error, 'error');
            return;
        }
        
        // Display results
        displayResults(result, text);
        
        console.log('✅ Results displayed successfully');
        showToast('Essay scored successfully!', 'success');
    })
    .catch(error => {
        if (loadingDiv) loadingDiv.style.display = 'none';
        console.error('❌ Scoring error:', error);
        showToast('Scoring failed: ' + error.message, 'error');
    });
}

// Display scoring results
function displayResults(result, text) {
    const resultsDiv = document.getElementById('results');
    if (!resultsDiv) return;
    
    // Calculate enhanced metrics
    const words = text.trim().split(/\s+/);
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const uniqueWords = new Set(words.map(w => w.toLowerCase().replace(/[^\w]/g, ''))).size;
    const vocabularyDiversity = Math.round((uniqueWords / words.length) * 100);
    const avgSentenceLength = Math.round(words.length / sentences.length);
    const readabilityScore = Math.min(10, Math.max(1, Math.round(10 - (avgSentenceLength - 15) * 0.2)));
    
    // Display score with styling
    const scoreDisplay = document.getElementById('score-display');
    const scoreValue = result.score;
    
    if (scoreDisplay) {
        scoreDisplay.innerHTML = `<div class="score-value">${scoreValue}/10</div>`;
        
        // Apply score-based styling
        scoreDisplay.className = 'score-display ';
        if (scoreValue >= 8) scoreDisplay.className += 'score-excellent';
        else if (scoreValue >= 6) scoreDisplay.className += 'score-good';
        else if (scoreValue >= 4) scoreDisplay.className += 'score-average';
        else scoreDisplay.className += 'score-poor';
    }
    
    // Update metrics
    updateElement('word-count', result.metrics.word_count);
    updateElement('sentences', result.metrics.sentence_count);
    updateElement('unique-words', uniqueWords);
    updateElement('vocab-diversity', vocabularyDiversity + '%');
    updateElement('avg-sentence', avgSentenceLength);
    updateElement('readability', readabilityScore + '/10');
    updateElement('feedback', result.feedback);
    
    resultsDiv.style.display = 'block';
}

// Update element content safely
function updateElement(id, content) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = content;
    }
}

// Get personalized suggestions
function getSuggestions() {
    const text = document.getElementById('essay').value;
    const suggestionsDiv = document.getElementById('suggestions');
    const suggestionsList = document.getElementById('suggestions-list');
    
    if (!text.trim()) {
        showToast('Please enter some text first', 'warning');
        return;
    }

    // Analyze text and generate suggestions
    const suggestions = generateSuggestions(text);
    
    if (suggestionsList) {
        suggestionsList.innerHTML = suggestions.map(suggestion => `
            <div class="suggestion-item">
                <i class="${suggestion.icon}" style="color: #28a745; margin-right: 10px;"></i>
                ${suggestion.text}
            </div>
        `).join('');
    }

    if (suggestionsDiv) {
        suggestionsDiv.style.display = 'block';
    }
    
    showToast('Suggestions generated!', 'success');
}

// Generate suggestions based on text analysis
function generateSuggestions(text) {
    const words = text.trim().split(/\s+/);
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const suggestions = [];

    // Word count suggestions
    if (words.length < 150) {
        suggestions.push({
            icon: 'fas fa-expand-arrows-alt',
            text: 'Your essay is quite short. Consider adding more detailed examples and explanations to reach at least 150 words for better scoring.'
        });
    } else if (words.length > 500) {
        suggestions.push({
            icon: 'fas fa-compress-arrows-alt',
            text: 'Your essay is quite long. Consider being more concise and focused on your main arguments.'
        });
    }

    // Sentence variety
    const avgSentenceLength = words.length / sentences.length;
    if (avgSentenceLength < 10) {
        suggestions.push({
            icon: 'fas fa-text-width',
            text: 'Try using longer, more complex sentences to show advanced writing skills. Combine related ideas with conjunctions.'
        });
    } else if (avgSentenceLength > 25) {
        suggestions.push({
            icon: 'fas fa-cut',
            text: 'Some sentences are very long. Break them into shorter ones for better readability.'
        });
    }

    // Vocabulary diversity
    const uniqueWords = new Set(words.map(w => w.toLowerCase().replace(/[^\w]/g, ''))).size;
    const diversity = uniqueWords / words.length;
    if (diversity < 0.6) {
        suggestions.push({
            icon: 'fas fa-book',
            text: 'Try using more varied vocabulary. Replace repeated words with synonyms to show language sophistication.'
        });
    }

    // Structure suggestions
    if (!text.toLowerCase().includes('firstly') && !text.toLowerCase().includes('first') && 
        !text.toLowerCase().includes('secondly') && !text.toLowerCase().includes('finally')) {
        suggestions.push({
            icon: 'fas fa-list-ol',
            text: 'Use transition words like "Firstly", "Moreover", "Furthermore", "In conclusion" to improve essay structure.'
        });
    }

    // Introduction/conclusion check
    if (!text.toLowerCase().includes('conclusion') && !text.toLowerCase().includes('in summary')) {
        suggestions.push({
            icon: 'fas fa-flag-checkered',
            text: 'Consider adding a clear conclusion that summarizes your main points.'
        });
    }

    // Examples suggestion
    if (!text.toLowerCase().includes('example') && !text.toLowerCase().includes('instance')) {
        suggestions.push({
            icon: 'fas fa-lightbulb',
            text: 'Include specific examples to support your arguments and make them more convincing.'
        });
    }

    // Default positive feedback if no suggestions
    if (suggestions.length === 0) {
        suggestions.push({
            icon: 'fas fa-check-circle',
            text: 'Great job! Your essay follows good writing practices. Consider adding more sophisticated vocabulary for even better scoring.'
        });
    }

    return suggestions;
}

// Show best essay example
function showBestEssay() {
    const bestEssayDiv = document.getElementById('best-essay');
    const bestEssayContent = document.getElementById('best-essay-content');
    
    // Select a random best essay
    const randomBestEssay = bestEssays[Math.floor(Math.random() * bestEssays.length)];
    
    if (bestEssayContent) {
        bestEssayContent.innerHTML = `
            <div style="margin-bottom: 10px;">
                <strong>Topic:</strong> ${randomBestEssay.topic} | 
                <strong>Score:</strong> ${randomBestEssay.score}/10
            </div>
            <div style="line-height: 1.6;">
                ${randomBestEssay.text.split('\n\n').map(paragraph => 
                    `<p style="margin-bottom: 15px;">${paragraph}</p>`
                ).join('')}
            </div>
        `;
    }
    
    if (bestEssayDiv) {
        bestEssayDiv.style.display = 'block';
    }
    
    showToast('Best essay example loaded!', 'success');
}

// Copy best essay to editor
function copyBestEssay() {
    const randomBestEssay = bestEssays[Math.floor(Math.random() * bestEssays.length)];
    const essayTextarea = document.getElementById('essay');
    
    if (essayTextarea) {
        essayTextarea.value = randomBestEssay.text;
        essayTextarea.dispatchEvent(new Event('input'));
        
        // Scroll to essay textarea
        essayTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        showToast('Best essay copied to editor! You can now modify it or analyze it.', 'success');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element if it doesn't exist
    let toast = document.getElementById('toast-notification');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast-notification';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        document.body.appendChild(toast);
    }
    
    // Set colors based on type
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    
    toast.style.backgroundColor = colors[type] || colors.info;
    toast.textContent = message;
    
    // Show toast
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
    }, 3000);
}

// Utility function to safely log
function log(message, type = 'info') {
    const prefix = {
        info: 'ℹ️',
        success: '✅',
        error: '❌',
        warning: '⚠️'
    };
    console.log(`${prefix[type]} ${message}`);
}
