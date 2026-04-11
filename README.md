# Alfred University Admission Checker 🎓

A professional full-stack web application designed for students and administrators to check university admission eligibility in Ghana based on WASSCE results. This system supports OCR result extraction, intelligent grade validation, and social authentication with Firebase.

![Dashboard Preview](https://via.placeholder.com/1200x630.png?text=Alfred+University+Admission+Checker)

## ✨ Features

- **Double Entry System**: Upload a result slip (PDF/JPG/PNG) for automatic OCR extraction or use the manual entry form.
- **Firebase Authentication**: Secure registration and login using Email/Password or **Sign in with Google**.
- **Real-time Eligibility Matching**: Checks results against 16+ universities and 50+ programs instantly.
- **My Admission History**: Persistent tracking of all previous admission checks for authenticated users.
- **Premium Aesthetics**: Modern, responsive UI with sleek animations and professional design.
- **Intelligent Aggregate Calculation**: Automatically selects the best subjects to calculate final aggregates based on course category.

## 🚀 Quick Start (Windows)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ghana-admission-checker.git
   cd ghana-admission-checker
   ```

2. **Run the setup script**:
   Double-click `setup.bat`. This will:
   - Create a virtual environment.
   - Install all Python dependencies.
   - Initialize the database.

3. **Configure Environment**:
   Copy `.env.example` to `.env` and add your `SECRET_KEY`.

4. **Launch the app**:
   Double-click `run.bat` and open `http://localhost:5000` in your browser.

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-Login, Flask-SQLAlchemy (SQLite)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+), Bootstrap 5
- **Auth**: Firebase Authentication (Email/Password, Google OAuth)
- **OCR**: EasyOCR / Tesseract
- **Database**: SQLite (Production-ready migrations structure)

## 📁 Repository Structure

```
├── app.py           # Application Factory
├── models.py        # Database Models
├── routes.py        # Web & API Routes
├── utils.py         # Grade & Admission Logic
├── static/          # CSS & JS Assets
├── templates/       # HTML Pages
├── data/            # University & Program JSON Data
└── run.py           # Production Server Entry
```

## 🔒 Firebase Configuration

This project is pre-integrated with Firebase. Replace the config in `templates/base.html` with your own project credentials to enable authentication:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  // ... and other fields
};
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ for student success in Ghana.
