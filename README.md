# 📚 Savash – The All-in-One Digital School Platform

Savash is a next-generation educational platform designed to unify and streamline the digital school experience. It combines essential classroom features—such as assignments, class management, interactive learning, and intelligent assistance—into a single, modern interface tailored for both students and teachers.

## 🚀 Live Demo

- 🌐 Frontend: [https://savash.rohanjain.xyz](https://savash.rohanjain.xyz)
- 📡 API Docs: [https://api.codewasabi.xyz/docs](https://api.codewasabi.xyz/docs)

---

## ✨ Features

- 🔐 **Authentication** – Secure login for students and teachers
- 🏫 **Classroom Management** – Create, join, and manage digital classrooms
- 📝 **Assignments System (Work in progress)** – Teachers can post assignments; students can submit work
- 🧠 **AI Integration (Upcoming)** – Tools to rewrite prompts, suggest content, or give feedback using LLMs
- 🎮 **Gamified Learning (Planned)** – Host and play educational games inspired by Kahoot, Gimkit, and Blooket
- 📊 **Analytics Dashboard (Planned)** – See student performance and class insights in real-time

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** – High-performance Python web framework
- **Postgres** – Relational database
- **Uvicorn** – ASGI server for FastAPI
- **Swagger/OpenAPI** – Built-in documentation at `/docs`

### Frontend
- **React.js** – Built by [@RanMC-9918](https://github.com/RanMC-9918)
- **Vite** – Fast frontend build tool

---

## 📦 Getting Started

### Clone the Repository
```bash
git clone https://github.com/pyGuy152/savash.git
cd savash
```
### Backend 
```bash
cd back-end
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app
```
### Frontend Setup
```bash
cd front-end
cd Savash
npm i
npm run build
npm run dev
```

