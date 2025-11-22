# 🎯 AI Career & Skills Advisor

A comprehensive AI-powered career guidance platform built with Gradio and Google's Gemini AI.

## ✨ Features

### 🔐 User Authentication
- **Secure Login/Signup** system
- **Session Management** with persistent chat history
- **Guest Mode** for quick access

### 💬 AI Chat Interface
- **Real-time Career Guidance** powered by Gemini AI
- **Chat History** - Save and load previous conversations
- **Loading Animations** for better user experience
- **Multi-line Input** with keyboard shortcuts

### 🎯 Career Tools
- **📋 Career Assessment** - Personalized career path recommendations
- **🎯 Skills Gap Analysis** - Identify missing skills for target roles
- **📄 Resume Tips** - Professional resume enhancement guidance
- **📊 Market Insights** - Job market trends and salary information
- **📚 Learning Resources** - Personalized learning path recommendations

### 🎨 Modern UI/UX
- **Emoji-Enhanced Interface** for visual appeal
- **Responsive Design** works on all devices
- **Status Notifications** for user feedback
- **Professional Layout** with organized tabs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/arpit-sharma-budaun/nxt-wave.git
cd nxt-wave
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. **Run the application**
```bash
cd career_chatbot
python simple_app.py
```

5. **Access the app**
Open your browser and go to the URL shown in the terminal (usually `http://localhost:7860`)

## 📁 Project Structure

```
nxt-wave/
├── career_chatbot/
│   ├── simple_app.py          # Main application file
│   └── .env                   # Environment variables (create this)
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

## 🛠️ Technology Stack

- **Frontend**: Gradio (Python web framework)
- **AI Model**: Google Gemini 2.5 Flash Lite
- **Backend**: Python
- **Authentication**: Custom session management
- **Storage**: In-memory (for demo purposes)

## 🎯 Use Cases

### For Job Seekers
- Get personalized career recommendations
- Identify skill gaps for target roles
- Receive professional resume tips
- Access market insights and salary data
- Find relevant learning resources

### For Career Counselors
- Use as a supplementary tool for client guidance
- Access comprehensive career assessment framework
- Provide data-driven career advice

### For Students
- Explore career options based on interests
- Understand skill requirements for different roles
- Get guidance on learning paths

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Customization
- Modify prompts in `simple_app.py` to adjust AI responses
- Update career assessment questions as needed
- Customize UI elements and styling

## 📊 Features in Detail

### Career Assessment
- **5-Question Framework** covering work environment, style, tasks, work-life balance, and routine preferences
- **AI-Powered Analysis** providing 3 personalized career path recommendations
- **Detailed Explanations** for each suggested career

### Skills Analysis
- **Gap Identification** between current skills and target role requirements
- **Learning Path Suggestions** with prioritized skill development
- **Industry-Specific Guidance** tailored to different fields

### Resume Enhancement
- **Level-Specific Tips** for entry, mid, and senior level positions
- **Industry Best Practices** for different job roles
- **Actionable Recommendations** for immediate improvement

### Market Intelligence
- **Industry Trends** and growth projections
- **Location-Based Insights** for different markets
- **Salary Information** and compensation trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powering the intelligent career guidance
- **Gradio** for the excellent web framework
- **Open Source Community** for inspiration and tools

## 📞 Support

For support, email [your-email@example.com] or create an issue in this repository.

---

**Made with ❤️ by [Arpit Sharma](https://github.com/arpit-sharma-budaun)**