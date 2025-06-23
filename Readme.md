# ⚡ Electric Bill Reader Web App

A Flask-based web application that allows users to:

- Upload electric bill PDFs
- Extract data using **regular expressions (re)** from raw text
- Store extracted data securely in MongoDB
- Authenticate users (Login/Register)
- Let users view only their uploaded bills (admin sees all)

---

## 🔍 How It Works

The app works in 3 core steps:

1. **PDF Upload** – Users upload scanned electric bill PDFs.
2. **Text Extraction** – Using `pdfminer.six`, raw text is extracted from the PDF.
3. **Regex Parsing** – Specific fields like name, month, bill number, amount, etc., are pulled using **custom regular expressions**:

   - 👤 Name
   - 🏡 Address
   - 🆔 Consumer ID
   - 🧾 Bill Number
   - 📅 Month and Year
   - 📞 Phone Number
   - 💰 Total Bill
   - ⏰ Due Date

---

## 🛠 Features

- Upload PDF bills
- Extract meaningful data using `re`
- User Authentication (Register/Login)
- User-based access control
- Admin view of all entries
- Download/view uploaded files
- Delete functionality (user and admin-specific)

---

## 🧰 Tech Stack

-**Backend:** Python + Flask

-**PDF Parsing:** pdfminer.six

-**Regex Engine:** Python `re`

-**Database:** MongoDB (Local)

-**Frontend:** HTML + CSS + Bootstrap (Jinja2 templates)

---

## 📂 Folder Structure

```

.
├── app.py                  # Main Flask application
├── match.py
├── pattern.py              # Regex extraction logic
├── templates/              # HTML templates
│   ├── index.html
│   ├── form.html
│   ├── view.html
│   ├── detail_view.html
│   ├── submit_result.html
│   ├── login.html
│   └── register.html
├── uploads/                # Folder for uploaded PDFs
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash

gitclonehttps://github.com/yourusername/electric-bill-reader.git

cdelectric-bill-reader

```

### 2. Create virtual environment

```bash

python -m venv env
#On Windows: env\Scripts\activate
source env/bin/activate
```

### 3. Install dependencies

```bash

pip install -r requirements.txt

```

---

## 🧪 Run Locally

```bash

python app.py

```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 👨‍💻 Author

Made by **Keyur Kolhe**. Inspired by real billing automation needs.
