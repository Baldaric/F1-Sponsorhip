# Formula 1 Data Analysis

This repository contains the work done for Milestone 3 of the Hacktiv8 Data Science Full-Time Program. The project involves leveraging Formula 1 data to strategically position the Terra brand as a new luxury performance automotive competitor.

---

## 📌 Background
Terra, a luxury performance brand emerging from a historically mass-market automotive manufacturer, aims to establish itself among elite competitors such as Ferrari, Aston Martin, and McLaren. Formula 1, known for its exclusivity, innovation, and high performance, serves as the perfect platform for brand positioning.

---

## 🎯 Objectives
- Automate data processing tasks using Apache Airflow.
- Validate data quality with Great Expectations.
- Utilize NoSQL databases effectively.
- Perform data cleaning and transformation.
- Create informative dashboards and visualizations using Kibana.
- Recommend optimal drivers and circuits for Terra's brand sponsorship.

---

## 📊 Dataset
- **Dataset Used:** [Formula 1 World Championship (1950-2020)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
- Includes diverse categorical and numerical columns suitable for deep analysis.

---

## 🛠️ Project Workflow
1. **Data Ingestion**
   - Import raw data into PostgreSQL via Docker.

2. **Data Cleaning**
   - Remove duplicates.
   - Normalize column names.
   - Handle missing values.

3. **Data Validation**
   - Apply 7+ expectations using Great Expectations (e.g., uniqueness, ranges, categorical checks).

4. **Data Storage**
   - Export clean data to CSV and Elasticsearch.

5. **Automation**
   - Schedule automated tasks using Apache Airflow DAGs.

6. **Visualization & Analysis**
   - Develop dashboards in Kibana including bar plots, pie charts, and other visualizations to deliver insightful analytics.

---

## 🚀 Key Insights & Recommendations
- **Recommended Drivers:** Charles Leclerc (Ferrari) and Lando Norris (McLaren).
- **Strategic Circuits:** Prioritize promotional activities at circuits like Monza and Silverstone.
- **Long-Term Partnerships:** Establish a sustained sponsorship with emerging drivers for increased brand visibility and consumer loyalty.

---

## 📁 Repository Structure
```
Milestone-3/
├── README.md
├── P2M3_<your_name>_ddl.txt
├── P2M3_<your_name>_data_raw.csv
├── P2M3_<your_name>_data_clean.csv
├── P2M3_<your_name>_DAG.py
├── P2M3_<your_name>_DAG_graph.jpg
├── P2M3_<your_name>_GX.ipynb
├── P2M3_<your_name>_conceptual.txt
└── images/
    ├── introduction & objective.png
    ├── plot & insight 01.png
    ├── plot & insight 02.png
    ├── plot & insight 03.png
    ├── plot & insight 04.png
    ├── plot & insight 05.png
    ├── plot & insight 06.png
    └── kesimpulan.png
```

---

## 📝 Usage
To run this project:
- Clone the repository.
- Execute the Airflow DAG script to perform automated data handling.
- Visualize results through Kibana dashboards.

---

Enjoy analyzing the exciting world of Formula 1 and strategically positioning Terra for success!

