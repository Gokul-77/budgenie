# 💰 BudGenie - Smart Expense Tracker

## 📋 Overview

BudGenie is a modern, full-featured expense tracking application built with Django. It helps you take control of your finances with real-time insights, beautiful visualizations, and multi-user support. Track expenses and income, manage categories, and visualize your spending patterns with an intuitive, responsive dashboard.

## ✨ Key Features

### 💳 Expense & Income Management
- **Full CRUD Operations**: Create, read, update, and delete transactions effortlessly
- **Dual Transaction Types**: Track both expenses and income separately
- **Custom Categories**: Organize transactions with color-coded categories
- **Date Filtering**: View transactions by date range with powerful filtering options

### 📊 Analytics & Visualization
- **Interactive Dashboard**: Real-time financial overview with beautiful charts
- **Spend vs. Credit Trends**: Line charts showing spending and income patterns over time
- **Category Breakdown**: Pie charts displaying expense distribution by category
- **Summary Statistics**: Quick glance at total expenses, income, and balance

### 🎨 Modern User Experience
- **Responsive Design**: Seamless experience across desktop, tablet, and mobile devices
- **Dark/Light Theme Toggle**: Choose your preferred viewing mode
- **Real-time Updates**: WebSocket integration for instant data synchronization
- **Intuitive Navigation**: Clean, user-friendly interface with hamburger menu for mobile

### 🔐 Security & Multi-User Support
- **User Authentication**: Secure login and registration system
- **Custom User Backend**: Email or username authentication support
- **User Isolation**: Each user's data is completely separate and secure
- **Session Management**: Secure session handling with Django's built-in security

### 🚀 Production Ready
- **Docker Support**: Full containerization with Docker Compose
- **PostgreSQL Database**: Production-grade database support
- **Redis Integration**: High-performance caching and WebSocket backend
- **Static File Management**: WhiteNoise for efficient static file serving

---

## 🛠️ Technology Stack

### Backend
- **Django 5.0**: High-level Python web framework
- **Django Channels 4.0**: WebSocket support for real-time features
- **Daphne**: ASGI server for Django Channels
- **Redis 5.0**: In-memory data store for caching and channels layer

### Frontend
- **HTML5/CSS3**: Modern, semantic markup and styling
- **Vanilla JavaScript**: No heavy frameworks, just clean, efficient code
- **Chart.js**: Beautiful, responsive charts and graphs
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

### Database
- **PostgreSQL 15**: Production database (via Docker)
- **SQLite**: Development database (default)

### DevOps
- **Docker & Docker Compose**: Containerization and orchestration
- **WhiteNoise**: Static file serving
- **Python-dotenv**: Environment variable management

---


## 📸 Screenshots

<img width="1897" height="888" alt="image" src="https://github.com/user-attachments/assets/9c0f0cb5-137f-44da-b67a-66f4611586b1" />
<br>
<img width="1895" height="882" alt="image" src="https://github.com/user-attachments/assets/bfda63dc-7ddf-49dd-a51f-f8f786be0a98" />
<br>
<img width="1896" height="859" alt="image" src="https://github.com/user-attachments/assets/ad71512b-2ccb-4764-8d4e-c6ed4062d58b" />

<br>


---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gokul-77/budgenie.git
   cd budgenie
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Run migrations (first time only)**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create a superuser (first time only)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the application**
   - Navigate to `http://localhost:8000`

---

## 📖 Usage Guide

### Getting Started

1. **Register an Account**
   - Click "Sign Up" on the landing page
   - Fill in your details (username, email, password)
   - Log in with your credentials

2. **Create Categories**
   - Navigate to Categories page
   - Click "Add Category"
   - Set a name and choose a color for visual identification

3. **Add Transactions**
   - Go to Expenses page
   - Click "Add Expense" or "Add Income"
   - Fill in the details: title, amount, category, date, and description
   - Save to add the transaction

4. **View Dashboard**
   - The dashboard provides an overview of your finances
   - See total expenses, income, and balance
   - View interactive charts for spending trends and category breakdowns
   - Filter by date range to focus on specific periods

5. **Manage Transactions**
   - Edit or delete transactions from the Expenses page
   - Use the search and filter options to find specific transactions
   - Export data for further analysis (coming soon)

### Key Pages

- **🏠 Home/Landing**: Welcome page with app overview
- **📊 Dashboard**: Financial overview with charts and statistics
- **💸 Expenses**: List and manage all transactions
- **🏷️ Categories**: Create and manage expense categories
- **👤 Profile**: View and edit user information
- **🔐 Login/Register**: Authentication pages

---

## 🗂️ Project Structure

```
budgenie/
├── accounts/              # User authentication & management
│   ├── backends.py        # Custom authentication backend
│   ├── forms.py           # Registration & login forms
│   ├── models.py          # Custom User model
│   ├── views.py           # Auth views
│   └── templates/         # Auth templates
├── expenses/              # Expense tracking core features
│   ├── models.py          # Category & Expense models
│   ├── views.py           # Expense CRUD views
│   ├── forms.py           # Expense forms
│   └── templates/         # Expense templates
├── core/                  # Core functionality & dashboard
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   ├── views.py           # Dashboard views
│   ├── static/            # CSS, JS, images
│   └── templates/         # Core templates
├── budgenie/              # Project settings & configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Multi-container orchestration
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/budgenie
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

**For local development:**
- SQLite is used by default (no configuration needed)

**For production (Docker):**
- PostgreSQL is configured in `docker-compose.yml`
- Connection URL: `postgres://postgres:postgres@db:5432/budgenie`

---

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Run tests with coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up Redis for production
- [ ] Configure static file serving (WhiteNoise is included)
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure backup strategy for database
- [ ] Use environment variables for sensitive data


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@Gokul-77](https://github.com/Gokul-77/)
- LinkedIn: [Gokul](https://www.linkedin.com/in/gokul-selvaraj-a3b65a213/)
- Email: gokul142003@gmail.com

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- Chart.js for beautiful visualizations
- Redis for high-performance caching
- Docker for simplified deployment
- All contributors and users of BudGenie

---




