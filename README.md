# ✅ TaskFlow // Smart Task Manager

Hey there! This is my project for the Python Development Internship. It's a full-stack task manager that doesn't just list things to do—it actually crunches your productivity stats in real-time.

I wanted to build something that felt snappy, so I integrated WebSockets to handle live updates across different windows without needing a page refresh.

---

## 🛠 What's under the hood?

I tried to keep the tech stack modern but manageable:

*   **Backend:** Python 3.11 with Flask (structured using the App Factory pattern).
*   **Database:** PostgreSQL with SQLAlchemy (SQLAlchemy saved me so much time with queries).
*   **Data Science:** I used **Pandas and NumPy** to calculate completion percentages and task trends. 
*   **Real-time:** Flask-SocketIO (this was the hardest part to get right!).
*   **Frontend:** Vanilla JS and CSS3. I wanted to see how much I could do without a heavy framework like React.

---

## 🚀 Getting Started

If you want to run this locally, here is the quick-start guide:

### 1. Clone & Environment
git clone [https://github.com/] https://github.com/ahmadhomam/TaskFlow-management-app.git
cd smart-task-manager
python -m venv venv
Windows: venv\Scripts\activate | Mac: source venv/bin/activate
pip install -r requirements.txt

2. Database Setup
Make sure you have PostgreSQL installed and running. Create a database named taskmanager:

  CREATE DATABASE taskmanager;

3. Environment Variables
Create a .env file in the root directory and paste this (replace with your actual Postgres password):

  SECRET_KEY={{GENERATE_A_RANDOM_STRING}}
  DATABASE_URL=postgresql://postgres:{{YOUR_PASSWORD}}@localhost:5432/taskmanager

4. Run the App
python run.py

### Screenshots
![Dashboard_01](res/Screenshot%202026-05-11%20223330.png)
![Dashboard_02](res/image.png)
![Loginpage_01](res/Screenshot%202026-05-11%20223347.png)
![Loginpage_02](res/Screenshot%202026-05-11%20223403.png)
![Loginpage_03](res/Screenshot%202026-05-11%20223429.png)




## Author
Homam Ahmad Kazimi | Python Development Internship Assignment













