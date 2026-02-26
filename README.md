# Accredify – Criterion 4 Dashboard (Django)

A Django-based Accredify project for managing **Criterion 4** data with a modern **Admin Dashboard**, **Edit/Manage pages**, and **PDF report generation** using ReportLab.

---

## 📌 Features

### ✅ Criterion 4 Module
- **4.1 Enrolment Ratio**
  - Add new enrolment ratio records
  - View saved records in table format
  - Auto-calculated total admitted (N1 + N2 + N3)
  - Generate PDF report (Table 4.1)

- **4.2 Success Rate in Stipulated Period**
  - Add success rate records
  - View saved records in table format
  - Generate PDF report (Table 4.2)

### ✅ Dashboard / Admin Panel
- Sidebar navigation
- Cards for quick overview
- Chart preview (Chart.js)
- Clean dark theme UI

### ✅ PDF Generation
- Generates NAAC format tables using **ReportLab**
- Outputs PDF directly in browser (inline view)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 5
- **Backend:** Python, Django
- **Database:** SQLite
- **PDF Reports:** ReportLab
- **Charts:** Chart.js

---

## 📂 Project Structure (Important Files)

# Accredify – Criterion 4 Dashboard (Django)

A Django-based Accredify project for managing **Criterion 4** data with a modern **Admin Dashboard**, **Edit/Manage pages**, and **PDF report generation** using ReportLab.

---

## 📌 Features

### ✅ Criterion 4 Module
- **4.1 Enrolment Ratio**
  - Add new enrolment ratio records
  - View saved records in table format
  - Auto-calculated total admitted (N1 + N2 + N3)
  - Generate PDF report (Table 4.1)

- **4.2 Success Rate in Stipulated Period**
  - Add success rate records
  - View saved records in table format
  - Generate PDF report (Table 4.2)

### ✅ Dashboard / Admin Panel
- Sidebar navigation
- Cards for quick overview
- Chart preview (Chart.js)
- Clean dark theme UI

### ✅ PDF Generation
- Generates NAAC format tables using **ReportLab**
- Outputs PDF directly in browser (inline view)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 5
- **Backend:** Python, Django
- **Database:** SQLite
- **PDF Reports:** ReportLab
- **Charts:** Chart.js

---

## 📂 Project Structure (Important Files)

naac_portal/
│
├── criterion4/
│ ├── templates/
│ │ ├── criterion4_home.html
│ │ ├── enrolment_ratio_manage.html
│ │ ├── success_rate_manage.html
│ │ └── dashboard.html
│ │
│ ├── views.py
│ ├── urls.py
│ ├── models.py
│ ├── forms.py
│ └── migrations/
│
├── static/
│ └── css/
│ └── style.css
│
├── db.sqlite3
└── manage.py


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

#Create Virtual Environment
python -m venv env

#Activate Virtual Environment
env\Scripts\activate

#Install Requirements
pip install django reportlab

#Run Migrations
python manage.py makemigrations
python manage.py migrate

#Start Server
python manage.py runserver

##-----Useful URLs-----##

| Page                         | URL                                                  |
| ---------------------------- | ---------------------------------------------------- |
| Criterion 4 Home             | `http://127.0.0.1:8000/`                             |
| Dashboard                    | `http://127.0.0.1:8000/dashboard/`                   |
| Manage Enrolment Ratio (4.1) | `http://127.0.0.1:8000/manage/enrolment-ratio/`      |
| Manage Success Rate (4.2)    | `http://127.0.0.1:8000/manage/success-rate/`         |
| Enrolment Ratio PDF (4.1)    | `http://127.0.0.1:8000/4-1-enrolment-ratio/`         |
| Success Rate PDF (4.2)       | `http://127.0.0.1:8000/4-2-success-rate-no-backlog/` |


!!!!!!!!!!!!!!!!------------------------ important---------------------!!!!!!!!!!!!!!!!!

#4.1
http://127.0.0.1:8000/enrolment/list/
http://127.0.0.1:8000/enrolment/add/

#4.1.1
http://127.0.0.1:8000/enrolment411/add/
http://127.0.0.1:8000/enrolment411/list/

#4.1.2
http://127.0.0.1:8000/enrolment412/add/
http://127.0.0.1:8000/enrolment412/list/

#4.2
http://127.0.0.1:8000/successrate/add/
http://127.0.0.1:8000/successrate/list/

#4.2.1 and 4.2.2
http://127.0.0.1:8000/success421/add/   → Without backlog
http://127.0.0.1:8000/success422/add/   → With backlog

http://127.0.0.1:8000/success421/list/
http://127.0.0.1:8000/success422/list/

#4.3
http://127.0.0.1:8000/backlog43/add/
http://127.0.0.1:8000/backlog43/list/

#4.3.1
http://127.0.0.1:8000/academic431/add/
http://127.0.0.1:8000/academic431/list/

#4.4.1
http://127.0.0.1:8000/academic44/add/
http://127.0.0.1:8000/academic44/list/

#4.5
http://127.0.0.1:8000/academic451/list/
http://127.0.0.1:8000/academic451/add/

#4.6
http://127.0.0.1:8000/4-6-placement/   #list
http://127.0.0.1:8000/4-6-placement/add/ 

#4.6.a
http://127.0.0.1:8000/placement46a/add/
http://127.0.0.1:8000/placement46a/list/


#4.7.1
http://127.0.0.1:8000/professional/add/
http://127.0.0.1:8000/professional/list/

#4.7.2
http://127.0.0.1:8000/publication472/list/
http://127.0.0.1:8000/publication472/add/

#4.7.3
http://127.0.0.1:8000/participation/add/
http://127.0.0.1:8000/participation/list/

