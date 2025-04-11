/backend
├── app.py                # Main Flask application
├── routes.py             # API endpoints for story generation, saving, downloading, etc.
├── models.py             # Database models for users, stories, and quizzes
├── utils/
│   ├── story_generator.py # Logic to generate stories using Gemini models
│   ├── image_generator.py # Logic to generate illustrations using Gemini models
│   └── pdf_generator.py   # Functionality to create PDF files
├── templates/            # HTML templates (if needed for testing)
└── static/               # Static files like images or stylesheets


frontend/
├── public/
│   ├── index.html
│   └── assets/
├── src/
│   ├── components/
│   │   ├── Navbar.js
│   │   ├── Dashboard.js
│   │   ├── StoryCard.js
│   │   ├── CreateStory.js
│   │   ├── ExploreStories.js
│   │   ├── StoryViewer.js
│   │   ├── Quiz.js               # Interactive quiz component
│   │   └── Footer.js
│   ├── styles/
│   │   ├── App.css
│   │   ├── Quiz.css              # Styles for Quiz component
│   │   └── other styles...
│   ├── utils/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── context/
└── package.json
