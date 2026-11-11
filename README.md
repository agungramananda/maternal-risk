# Maternal Health Risk Classification System

A web-based application that classifies the health risk level of pregnant women using machine learning algorithms (Decision Tree and Random Forest).

**Tech Stack:** Python, Streamlit, PostgreSQL, Docker
**Date:** December 2025

---

## Project Goals

1. Build a maternal health risk prediction system using medical data
2. Provide an easy-to-use interface for medical professionals
3. Store patient history and prediction results in a database
4. Compare the performance of Decision Tree and Random Forest models
5. Simplify deployment using Docker

---

## Key Features

### 1. Patient Data Input
- Patient full name
- Phone number
- Email
- Full address

### 2. Medical Data Input
- Patient age
- Systolic blood pressure
- Diastolic blood pressure
- Blood sugar (BS)
- Body temperature
- Heart rate

### 3. Risk Prediction
- Uses a Decision Tree model
- Uses a Random Forest model
- Displays the risk level: Low Risk, Mid Risk, or High Risk

### 4. Database Management
- Patient data storage
- Medical record history storage
- Table relationships using foreign keys

### 5. Data History
- View all patient data
- View medical record history
- Filter and search data

---

## Project Structure

```
maternal-risk/
├── app.py                          # Main Streamlit application
├── start.py                        # Script to run migrations & the app
├── database.py                     # Database connection configuration
├── models.py                       # SQLAlchemy database models
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Docker Compose configuration
├── alembic.ini                     # Alembic configuration
│
├── alembic/                        # Database migration folder
│   ├── env.py                      # Migration environment
│   ├── script.py.mako              # Migration script template
│   └── versions/                   # Migration versions
│       └── 001_initial_migration.py
│
└── model/                          # Machine learning model folder
    ├── maternal_health_dt_model.pkl
    ├── maternal_health_dt_model_fix.pkl
    ├── maternal_health_rf_model.pkl
    └── maternal_health_rf_fix.pkl
```

---

## Technologies Used

### Frameworks and Libraries
| Library | Version | Purpose |
|---|---|---|
| Streamlit | 1.29.0 | Web interface framework |
| Pandas | 2.1.4 | Data manipulation and analysis |
| Scikit-learn | 1.3.2 | Machine learning algorithms |
| NumPy | - | Numerical computing |

### Database
| Tool | Version | Purpose |
|---|---|---|
| PostgreSQL | - | Relational database |
| SQLAlchemy | 2.0.23 | ORM (Object-Relational Mapping) |
| Alembic | 1.13.1 | Database migration tool |
| psycopg2-binary | 2.9.9 | PostgreSQL adapter |

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

### Utilities
- **python-dotenv** 1.0.0 - Environment variable management
- **joblib** 1.3.2 - Model serialization

---

## Machine Learning Algorithms

### 1. Decision Tree
- Implemented from scratch
- Supports parameters: `max_depth`, `min_samples_split`, `min_samples_leaf`
- Used for maternal risk classification

### 2. Random Forest
- Implemented from scratch
- Ensemble of multiple decision trees
- Parameters: `n_estimators`, `max_depth`, `min_samples_split`, `bootstrap`
- Provides more robust predictions

---

## Database Models

### Table: `patients`
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Primary key |
| name | String | Patient name |
| phone_number | String | Phone number |
| email | String | Email |
| address | String | Address |
| created_at | DateTime | Creation date |

### Table: `maternal_records`
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Primary key |
| patient_id | Integer (FK) | Foreign key to `patients` |
| age | Integer | Patient age |
| systolic_bp | Integer | Systolic blood pressure |
| diastolic_bp | Integer | Diastolic blood pressure |
| bs | Float | Blood sugar |
| body_temp | Float | Body temperature |
| heart_rate | Integer | Heart rate |
| risk_level | String | Predicted risk level |
| model_used | String | Model used for prediction |
| created_at | DateTime | Creation date |

**Relationship:** One-to-many between `patients` and `maternal_records`.

---

## Installation and Usage

### A. Running with Python

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=maternal_risk
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

3. Run the application:
   ```bash
   python start.py
   ```
   Or run it directly:
   ```bash
   streamlit run app.py
   ```

### B. Running with Docker

1. Make sure Docker and Docker Compose are installed.
2. Set up the `.env` file.
3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
4. Open the app in your browser at http://localhost:8501

---

## Database Configuration

- PostgreSQL as the database
- Connection through the SQLAlchemy ORM
- Migrations managed with Alembic
- Environment variables:

| Variable | Description |
|---|---|
| `DB_HOST` | Database server host |
| `DB_PORT` | Database port (default: 5432) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |

### Database Migrations

Alembic provides version control for the database schema, including auto-generated migration scripts.

```bash
alembic upgrade head     # Run all migrations
alembic downgrade -1     # Roll back one version
alembic current          # Check the current version
alembic history          # View migration history
```

---

## Application Workflow

1. Open the Streamlit application.
2. Choose a menu option:
   - Input New Patient Data
   - View Patient Data History
   - View Medical Record History

**Entering new data:**
1. Fill in the patient identity data
2. Fill in the medical data (vital signs)
3. Choose a prediction model (Decision Tree / Random Forest)
4. Click the predict button
5. The system displays the risk classification result
6. The data is saved to the database

**Viewing history:**
1. Data is displayed in table form
2. Filter and search are available
3. Export data when needed

---

## Prediction Results

The system classifies maternal health risk into three categories:

| Level | Meaning |
|---|---|
| **Low Risk** | Normal health condition; no special attention required |
| **Mid Risk** | Requires more intensive monitoring and regular doctor consultations |
| **High Risk** | Requires immediate medical attention, close monitoring, and special care |

---

## Strengths

1. User-friendly interface built with Streamlit
2. Real-time predictions using ML models
3. Structured data storage in a database
4. Multiple ML algorithms supported for comparison
5. Containerized with Docker for easy deployment
6. Database migration management with Alembic
7. Scalable and easy to extend

---

## Development Notes

- ML models are trained on a maternal health dataset
- Decision Tree and Random Forest are implemented from scratch
- Models are saved in pickle format (`.pkl`)
- Each model has a "fix" version (improved version)
- The database schema can be migrated and rolled back easily
- Environment variables are used for secure configuration

---

## Future Improvements

1. Add other ML algorithms (SVM, Neural Network)
2. Feature engineering to improve accuracy
3. Analytics dashboard for data visualization
4. API endpoints for integration with other systems
5. PDF report export
6. Automatic notifications for high-risk cases
7. User authentication and authorization
8. Automated database backup and restore

---

## About

This is a personal project built to help medical professionals identify maternal health risk.

For questions, bug reports, or contributions, please open an issue or reach out to the project maintainer.
