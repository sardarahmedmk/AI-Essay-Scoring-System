# 🚀 AI-Powered Essay Scoring System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/sardarahmedmk/AI-Essay-Scoring-System?style=social)](https://github.com/sardarahmedmk/AI-Essay-Scoring-System)

> An intelligent essay scoring system built with Streamlit that provides instant feedback, comprehensive analysis, and personalized suggestions to improve writing skills.

## ✨ Features

### 🎯 **Core Functionality**
- **Real-time Essay Scoring** (1-10 scale with detailed breakdown)
- **Comprehensive Metrics Analysis** (word count, vocabulary diversity, readability)
- **AI-Powered Suggestions** (personalized improvement recommendations)
- **Sample Essays Library** (examples with different quality levels)
- **Best Essay Showcase** (high-scoring examples to learn from)

### 🎨 **User Experience**
- **Glass-morphism UI Design** (modern, professional appearance)
- **Responsive Layout** (works perfectly on desktop and mobile)
- **Interactive Sidebar** (quick actions and writing tips)
- **Real-time Statistics** (word/character counters as you type)
- **Color-coded Scoring** (visual feedback with gradient backgrounds)

### 📊 **Advanced Analytics**
- Word count and vocabulary diversity analysis
- Sentence structure and readability assessment  
- Content quality indicators (structure words, examples, advanced vocabulary)
- Flesch readability score approximation
- Detailed feedback with actionable suggestions

## 🚀 Streamlit Deployment

### **One-Click Deployment (Recommended)**

1. **Visit Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click **"New app"**
   - Select **"From existing repo"**
   - Repository: `sardarahmedmk/AI-Essay-Scoring-System`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - Click **"Deploy!"**

3. **Your App Goes Live:**
   - Deployment takes 2-5 minutes
   - URL: `https://ai-essay-scoring-system.streamlit.app/`
   - Automatic updates when you push to GitHub

### **Troubleshooting Deployment Issues**

If you encounter "Error installing requirements":

**Option 1: Use Simplified Requirements**
The app uses minimal dependencies that should work on Streamlit Cloud.

**Option 2: Local Testing First**
```bash
# Test locally before deploying
git clone https://github.com/sardarahmedmk/AI-Essay-Scoring-System.git
cd AI-Essay-Scoring-System
pip install streamlit
streamlit run streamlit_app.py
```

**Option 3: Check Streamlit Cloud Status**
- Visit [status.streamlit.io](https://status.streamlit.io/) for service status
- Try deploying again after a few minutes

### **Alternative Deployment Options**

**Heroku:**
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port \$PORT" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

**Railway:**
- Connect your GitHub repo to [railway.app](https://railway.app/)
- Auto-detects Streamlit and deploys

### Local Installation

```bash
# Clone the repository
git clone https://github.com/sardarahmedmk/AI-Essay-Scoring-System.git
cd AI-Essay-Scoring-System

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📈 Scoring Algorithm

### **Scoring Criteria (10-point scale)**

| Component | Weight | Description |
|-----------|--------|-------------|
| **Word Count** | 25% | Length and content depth (150+ words recommended) |
| **Vocabulary Diversity** | 25% | Variety and sophistication of word usage |
| **Sentence Structure** | 25% | Sentence length, complexity, and flow |
| **Content Quality** | 25% | Structure indicators, examples, advanced vocabulary |

### **Score Ranges**
- **9-10**: Exceptional (A+) - Outstanding writing with excellent structure
- **7.5-8.9**: Excellent (A) - Strong writing with minor improvements needed
- **6-7.4**: Good (B) - Solid writing with room for enhancement
- **4.5-5.9**: Average (C) - Decent foundation, needs development
- **3-4.4**: Below Average (D) - Requires significant improvement
- **1-2.9**: Poor (F) - Major issues with length, structure, or content

## 💡 Writing Tips

### **For High Scores (8-10):**
- Write 200+ words with rich vocabulary
- Use varied sentence structures (15-22 words average)
- Include transition words (firstly, furthermore, however)
- Support arguments with specific examples
- Maintain clear introduction, body, and conclusion

### **Common Mistakes to Avoid:**
- Essays under 100 words (major score penalty)
- Repetitive vocabulary (low diversity score)
- Very short or very long sentences
- Lack of structure and organization
- Missing examples and evidence

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with advanced text analysis
- **Deployment**: Streamlit Community Cloud (primary), Heroku, Railway
- **Version Control**: Git/GitHub
- **Dependencies**: Minimal (streamlit, numpy, pandas)

### **System Requirements**
- **Python**: 3.8 or higher
- **Memory**: ~50MB RAM usage
- **Storage**: ~5MB total
- **Internet**: Required for deployment and updates

## 📊 Performance & Compatibility

- **Response Time**: < 1 second for essay analysis
- **Accuracy**: Comprehensive scoring based on multiple criteria
- **Scalability**: Handles essays from 10 to 1000+ words
- **Browser Support**: Chrome, Firefox, Safari, Edge
- **Mobile**: Fully responsive design
- **Deployment**: ✅ Streamlit Cloud Ready

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the amazing framework
- Inspired by educational technology and AI-powered learning tools
- Designed to help students and writers improve their skills

---

<div align="center">

**[🚀 Deploy Now](https://share.streamlit.io/) | [⭐ Star this repo](https://github.com/sardarahmedmk/AI-Essay-Scoring-System) | [🐛 Report Issues](https://github.com/sardarahmedmk/AI-Essay-Scoring-System/issues)**

*Made with ❤️ for better writing and education*

</div>
