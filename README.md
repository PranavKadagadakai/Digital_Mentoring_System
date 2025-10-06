# 🧠 Digital Mentoring System

A Django-based web application designed to facilitate digital academic mentoring. This system enables students, mentors, and administrators to interact through a structured interface that tracks academic performance, manages mentorships, and analyzes student progress.

---

## 📁 Project Structure

```
pranavkadagadakai-digital_mentoring_system/
├── core/                     # Main app logic
│   ├── models.py             # Database models (User, Marks, Course, etc.)
│   ├── views.py              # Core view functions
│   ├── forms.py              # Django forms for registration & profile
│   ├── urls.py               # App-level URL routing
│   └── utils.py              # Helper functions for GPA calculation
├── Digital_Mentoring_System/ # Project configuration folder
│   ├── settings.py           # Django settings file
│   ├── urls.py               # Project URL configuration
│   ├── wsgi.py / asgi.py     # Deployment entry points
├── templates/                # HTML templates for UI
├── static/                   # CSS and JS static assets
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── pyproject.toml            # Alternate dependency specification
└── README.md                 # Documentation (you are here)
```

---

## 🚀 Features

- 👩‍🎓 **Role-based access** for Students, Mentors, and Admins.
- 📈 **Automated SGPA & CGPA calculation** based on entered marks.
- 🧮 **Visual performance analytics** using Matplotlib.
- 💬 **Student–Mentor assignment** and performance tracking.
- 📑 **Grade cards, dashboards, and reports** for students.
- 🧰 Built with **Django 5.1** and **Python 3.12**.

---

## ⚙️ Prerequisites

Before setting up the project, ensure the following are installed:

- 🐍 **Python 3.12+**
- 📦 **pip** (Python package manager)
- 🧱 **Virtual environment tool** (e.g., `venv` or `virtualenv`)

---

## 🛠️ Installation & Setup

Follow the steps below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/pranavkadagadakai/digital_mentoring_system.git
cd pranavkadagadakai-digital_mentoring_system
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies

Using `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or, if you prefer using `pyproject.toml` (with `pip` 23.1+):

```bash
pip install .
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (for Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Collect Static Files (Optional for Deployment)

```bash
python manage.py collectstatic
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## 🧭 Default Roles & Access

| Role        | Access Level    | Key Features                          |
| ----------- | --------------- | ------------------------------------- |
| **Admin**   | Full control    | Assign mentors, view analytics        |
| **Mentor**  | Limited control | Input marks, view student performance |
| **Student** | Restricted      | View grade cards, analytics           |

---

## 📊 Core Models Overview

- **User** → Extends Django’s `AbstractUser` with roles & profile details.
- **Course** → Stores course code, name, and credits.
- **Marks** → Stores marks, grades, and updates SGPA/CGPA automatically.
- **PerformanceAnalytics** → Tracks semester and overall performance.
- **MentorAssignment** → Maps mentors to students.

---

## 🖥️ Project Usage

Once the server is running:

- Visit **`/register/`** to create a user account.
- Visit **`/login/`** to log in as a student, mentor, or admin.
- Admin users can access the Django Admin interface via **`/admin/`**.
- Use the Dashboard to navigate between Grade Cards, Analytics, and Profile.

---

## 🧩 Tech Stack

- **Backend:** Django 5.1 (Python 3.12)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite3 (default)
- **Visualization:** Matplotlib

---

## 🧪 Testing

To run tests:

```bash
python manage.py test
```

---

## 📦 Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`.
2. Configure `ALLOWED_HOSTS` with your domain or IP.
3. Use Gunicorn or uWSGI with Nginx for serving the app.
4. Run migrations and collect static files as shown above.

---

## 🧑‍💻 Author

**Pranav S Kadagadakai**
GitHub: [@pranavkadagadakai](https://github.com/pranavkadagadakai)

---

## 📜 License

This project is licensed under the **MIT License**. See `LICENSE` for more details.

---

**✅ Ready to run:** Clone → Setup → Migrate → Run → Explore!
