💼 Client Query Management System
📖 About the Project

The Client Query Management System (CQMS) is a Streamlit web application that enables organizations to collect, track, and resolve client queries efficiently.
It is designed to bridge the communication gap between clients and support teams.

🔨 Development Process

Database Setup → Created the database and tables in MySQL.

Connection Setup → Configured database connectivity in VS Code using mysql.connector.connect.

Prototype Testing → Verified database operations in Jupyter Notebook (.ipynb).

Script Conversion → Migrated working prototype into a Python script (.py).

UI Development → Built the Streamlit dashboard for clients & support team.

✨ Key Features

🔐 Login & Register Interface → New users can sign up and log in.

👤 Client Interface → Submit and track queries with details & attachments.

🛠 Support Dashboard → View, filter, and resolve client queries.

⚙️ Tech Stack

Database: MySQL

Frontend/UI: Streamlit

Data Handling: Pandas

Database Connectivity: mysql-connector-python

📋 Project Overview

The Client Query Management System provides a seamless way for organizations to handle client issues.
Clients can submit queries with necessary details, while the support team can manage, track, and resolve them in real time.

🎯 Features
🔐 Login & Register
📝 User Registration

Create an account with Username, Email, Password, and Role (Client/Support).

Prevents duplicate usernames or emails.

Passwords stored securely using SHA256 hashing.

🔑 User Login

Login with username and password.

Password verification with stored hash.

Maintains session state after login.

🎭 Role-Based Access

Client Role → Submit & track own queries.

Support Role → View, manage, and close all queries.

👤 Client Features

📝 Submit queries with email, mobile, heading, description, and file upload.

📂 Track query history by email (with Open/Closed status).

📸 Attach screenshots/documents.

⏱ Real-time status updates for created, updated, and closed queries.

👨‍💻 Support Team Features

📋 View all queries submitted by clients.

🔎 Filter by status → All / Open / Closed.

🛠 Manage & close queries with closing time.

🖼 Preview attachments for better issue understanding.

⚙️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/client-query-management-system.git
cd client-query-management-system

2️⃣ Create a Virtual Environment & Activate
python -m venv venv
# Activate environment
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt


requirements.txt:

streamlit
pandas
mysql-connector-python

3️⃣ Configure MySQL Database
CREATE DATABASE client_query_db;
USE client_query_db;

4️⃣ Run the Application
streamlit run app.py


➡️ The app will launch at 👉 http://localhost:8501

🔑 Sample Users
Username	Password	Role
support_admin	support123	Support
client_user	client123	Client
📊 Dataset

The project includes a sample dataset (sample_queries_250.csv) with 1000 client queries for testing.

Dataset Columns:

email

mobile

query_heading

query_description

query_created_time

status

query_closed_time

🔄 How It Works

User Authentication → Register/Login with role.

Client Side → Submit queries (only with registered email).

Support Side → View & filter queries, update status, close queries.

Database (MySQL) → Ensures real-time updates.

🎯 Use Cases

🏢 IT Companies → Manage support tickets & technical issues.

🎓 Educational Institutions → Handle student queries, complaints, feedback.

🛠 Service-Based Businesses → Track customer complaints & requests.

🏥 Healthcare Sector → Manage patient inquiries & appointments.

🛒 E-commerce Platforms → Resolve order, delivery, or payment issues.

🚀 Future Enhancements

📌 Role-based dashboards (Admins, Clients, Support).

📊 Analytics → Query trends & resolution time tracking.

✉️ Email/SMS notifications for query updates.

📂 Export queries as CSV/Excel for reporting.

✅ Now it’s clean, structured, and GitHub-ready.

Do you also want me to add badges (e.g., Python version, Streamlit, MySQL) at the top for a more professional look?

You said:
