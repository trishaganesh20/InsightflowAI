**InsightFlow — AI-Powered Business Analytics Assistant**

InsightFlow is an end-to-end analytics application that transforms natural language business questions into SQL queries, executes them safely on a MySQL database, and visualizes results through interactive dashboards.
This project was designed to simulate a real-world business analytics environment — combining data engineering, analytics, and AI to support faster, data-driven decision making.

Why I Built This:
  As a Management Information Systems graduate, I wanted to build something that reflects how modern analytics teams actually operate.

Instead of relying on dashboards, InsightFlow allows users to simply ask:
  “What is the monthly revenue by region?”  
  “Show order cancellation trends.”  

and instantly receive SQL queries and visual insights.

The goal was to bridge the gap between business questions and technical execution.

**What This Project Demonstrates**

This project highlights my ability to:

- Design relational database schemas  
- Generate large-scale synthetic datasets  
- Build secure database connections  
- Validate SQL for safety  
- Integrate OpenAI-based LLMs into an analytics workflow  
- Develop interactive data apps using Streamlit  
- Translate business needs into technical solutions  

**Languages and Tools**
- Python  
- MySQL  
- Streamlit  
- OpenAI API  
- Plotly  
- Pandas  
- Faker (synthetic data generation)  

**Environment**
- MySQL Workbench  
- VS Code  
- GitHub  
- macOS  

**Key Features**
- Natural Language → SQL
Users can ask business questions, and the app generates optimized SQL queries using an OpenAI-powered model.

- SQL Safety Layer
Before execution, queries pass through a validation system that blocks destructive commands such as:
- DROP  
- DELETE  
- UPDATE  
- ALTER  
This ensures a secure analytics environment.

- Automated Data Generation
A custom data generator simulates a production-scale business database including:
- 5,000 customers  
- 60,000 orders  
- 120,000 order items  
- subscriptions  
- support tickets  
This allowed me to test realistic analytics scenarios.

- Interactive Dashboards
Query results are automatically visualized using Plotly, enabling faster interpretation of trends and performance metrics.



**Architecture Overview**
User Question  
↓  
OpenAI SQL Generator  
↓  
SQL Validation Layer  
↓  
MySQL Database  
↓  
Streamlit Interface  
↓  
Interactive Visualization  


**Example Business Questions**
- Monthly revenue by region  
- Customer segment performance  
- Order cancellation rate  
- Subscription trends  
- Support ticket volume  


## 🚀 How to Run This Project

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/insightflow-ai.git
cd insightflow-ai




