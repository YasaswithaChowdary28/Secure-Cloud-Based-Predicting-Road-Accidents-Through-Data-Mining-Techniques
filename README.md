# 🚦 Accident Detection System (Django + Machine Learning)

This is a *Django-based web application* for predicting and analyzing road accident positioning.  
It integrates *machine learning (SVM)* with a Django web dashboard to assist service providers in understanding accident trends and positioning.

---

## 🚀 Features
- Service provider login
- Upload and analyze *Datasets.csv*
- Train & test ML model (Support Vector Machine)
- View accuracy, classification report, and confusion matrix
- Ratio analysis: "In Position" vs "Not In Position"
- Data visualization with charts
- Export predictions to Excel (WIP)

---

## 📂 Dataset
- Example dataset: [Kenya Road Accidents Database](https://data.humdata.org/dataset/kenya-road-accidents-database)  
- For this project, place the cleaned dataset as **Datasets.csv** in the project root.  
- Required columns:  
  - Fid → Feature column (accident details text)  
  - Label → Target column (0 = In Positioning, 1 = Not In Positioning)  

---

## ⚙ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/accident-detection-django.git
cd accident-detection-django

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py makemigrations
python manage.py migrate

5. Start server
python manage.py runserver

▶ Usage

Place Datasets.csv in project root.

Start the Django server.

Login as Admin → Username: Admin, Password: Admin.

Navigate to:

Train/Test Dataset → Run ML model training & view results.

Charts → View accident ratios and accuracy charts.

Download → Export predictions to Excel.
