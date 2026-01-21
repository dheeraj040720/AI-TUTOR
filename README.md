# AI Learning Tutor 🎓

An intelligent, personalized learning platform powered by Google's Gemini AI. Track student progress, generate custom quizzes, and receive AI-driven recommendations to enhance learning outcomes.

## ✨ Features

- **📊 Student Dashboard** - Track progress, accuracy, and performance across subjects
- **🧠 AI Quiz Generator** - Create custom quizzes on any topic using Gemini AI
- **🤖 AI Recommendations** - Get personalized study suggestions based on performance
- **✍️ Progress Tracking** - Submit and monitor quiz results over time
- **🌱 Mental Health Support** - Resources and tools for student well-being
- **🔑 Guest Access** - Easy demo mode for exploring the platform

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (optional, for development)
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Supabase Account ([Sign up here](https://supabase.com))



## 📁 Project Structure

```
AILearningTutor/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── supabase_client.py   # Supabase database connection
│   └── list_models.py       # Utility to list available Gemini models
├── frontend/
│   ├── index.html           # Landing page
│   ├── dashboard.html       # Student progress dashboard
│   ├── add_marks.html       # Submit quiz results
│   ├── quiz.html            # AI quiz generator
│   ├── mental_health.html   # Mental health resources
│   ├── config.js            # Frontend configuration
│   └── style.css            # Styles
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── SECURITY.md              # Security documentation
└── README.md                # This file
```

## 🔐 Security

This project uses environment variables to protect sensitive API keys. See [SECURITY.md](SECURITY.md) for detailed security information and best practices.

**Important:** Never commit your `.env` file to version control!

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini AI** - AI-powered quiz generation and recommendations
- **Supabase** - PostgreSQL database and authentication
- **Python-dotenv** - Environment variable management

### Frontend
- **HTML5/CSS3/JavaScript** - Core web technologies
- **Tailwind CSS** - Utility-first CSS framework
- **Supabase JS** - Client-side database access
- **SweetAlert2** - Beautiful alerts and modals

## 📝 API Endpoints

- `GET /student-progress` - Fetch all student progress data
- `POST /submit-answer` - Submit a quiz answer
- `POST /chat` - Chat with Gemini AI
- `POST /get-recommendation` - Get AI study recommendations
- `POST /generate-quiz` - Generate a custom quiz on any topic

## 🌐 Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Add environment variables in Vercel dashboard:
   - `GEMINI_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

### Other Platforms

The project can be deployed to any platform that supports Python and static file hosting:
- Heroku
- Railway
- Render
- AWS/Google Cloud/Azure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligent features
- Supabase for the database infrastructure
- Tailwind CSS for the beautiful UI components

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for students everywhere**
