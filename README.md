# EasyCRM

A simple desktop-based Customer Relationship Management (CRM) system built with Python, CustomTkinter, and MySQL.

## 💻 Features
- Add new customers
- View existing customers (by ID, Name, or Last Name)
- Delete customers
- Auto-refresh customer list
- Modern UI with `customtkinter`

## 🛠️ Technologies Used
- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- MySQL
- Tkinter & ttk

## 🧩 Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/EasyCRM.git
cd EasyCRM
```

2. Install required libraries:
```bash
pip install customtkinter mysql-connector-python
```

3. Setup MySQL:
```sql
CREATE DATABASE amir;

USE amir;

CREATE TABLE customer (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  last_name VARCHAR(255),
  phone VARCHAR(20)
);
```

4. Run the app:
```bash
python main.py
```

## 📸 UI Preview

*(Add screenshot if you want)*

## 📄 License

MIT License. Free to use and modify.
