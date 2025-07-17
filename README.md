
# 📊 Real-Time Big Data Analytics with Kafka, PySpark & Grafana  

This project demonstrates **real-time data analytics** using two approaches:  
✔ **Kafka + PySpark + Grafana** – A real-time distributed streaming pipeline (PC1 → PC2).  
✔ **Prometheus + Grafana** – A simulation-based monitoring pipeline.  

It also includes **offline PySpark analytics** in Google Colab for detailed insights.  


## ✅ Table of Contents  
1. [Project Overview](#project-overview)  
2. [Architecture](#architecture)  
3. [Approach 1: Kafka + PySpark + Grafana](#approach-1-kafka--pyspark--grafana)  
4. [Approach 2: Prometheus + Grafana Simulation](#approach-2-prometheus--grafana-simulation)  
5. [Offline Analytics in Google Colab](#offline-analytics-in-google-colab)  
6. [Folder Structure](#folder-structure)  
7. [Setup Instructions](#setup-instructions)  
   - [Approach 1: Kafka + PySpark + Grafana (Distributed Setup)](#approach-1-setup-kafka--pyspark--grafana)  
   - [Approach 2: Prometheus + Grafana Simulation](#approach-2-setup-prometheus--grafana-simulation)  
8. [Screenshots](#screenshots)  
9. [Future Enhancements](#future-enhancements)  


## 📌 Project Overview  
The goal of this project is to **simulate real-time viewership data** from a CSV and analyze it using:  
- **Kafka** for distributed event streaming.  
- **PySpark Structured Streaming** for real-time analytics.  
- **Prometheus & Grafana** for monitoring and visualization.  
- **PostgreSQL or InfluxDB** for optional storage of aggregated results.  

**Dataset Columns**:  
```
Event_ID | Event_Type | User_ID | City | State | User_Type | Timestamp | Channel | Program | Channel_Type | View_Min | Session_Dur | Preferred_Time | Region
```


## 🏗 Architecture  

### ✅ Approach 1: Kafka + PySpark + Grafana  
![Kafka Pipeline Architecture](images/kafka_pipeline.png)

```
PC1 (Producer) → Kafka Broker → PC2 (PySpark Consumer) → Database → Grafana Dashboards
```


### ✅ Approach 2: Prometheus + Grafana Simulation  
![Prometheus Pipeline Architecture](images/prometheus_pipeline.png)

```
CSV Dataset → Prometheus Exporter (Python) → Prometheus → Grafana Dashboards
```


## ✅ Approach 1: Kafka + PySpark + Grafana  

### 🔍 How It Works Across Two PCs  
- **PC 1**: Kafka Producer streams CSV data into **Kafka Topics**.  
- **PC 2**: PySpark Consumer reads Kafka topics in **real-time**, performs aggregations, and writes to DB or console.  
- **Grafana**: Connects to DB or Spark output for visualization.  

### Key Features  
✔ Real-time ingestion & processing  
✔ Distributed setup for scalability  
✔ Visualization in Grafana  


## ✅ Approach 2: Prometheus + Grafana Simulation  
This approach simulates real-time metrics using **Prometheus exporter** when you don’t have a full Kafka cluster setup.  

- Reads CSV rows sequentially with a time delay.  
- Exposes metrics at `http://localhost:8000/metrics`.  
- Grafana pulls data from Prometheus and renders dashboards.  


## ✅ Offline Analytics in Google Colab  
Due to Spark setup constraints locally, detailed analytics were done in **Colab**:  

- **Notebook:** [Analytics & Visualizations](https://colab.research.google.com/drive/1t2X3r2MHtKUaQ4ilkXLT3vJh5Q8eIaTT?usp=sharing)  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1t2X3r2MHtKUaQ4ilkXLT3vJh5Q8eIaTT?usp=sharing)


## 📂 Folder Structure  

```
real-time-bda-pipeline/
 ┣ 📜 README.md
 ┣ 📜 producer.py             # Kafka Producer (simulated streaming)
 ┣ 📜 subscriber.py           # PySpark Consumer with real-time analytics
 ┣ 📜 prometheus_simulator.py # Prometheus metrics exporter
 ┣ 📜 sample_data.csv         # Example dataset
 ┣ 📂 notebooks
 ┃   ┣ pyspark_analytics.ipynb
 ┣ 📜 requirements.txt
 ┗ 📜 docker-compose.yml      # For Kafka + Zookeeper setup
```


## ✅ Setup Instructions  

### 🔹 **Install Dependencies**  
```bash
pip install -r requirements.txt
```

### ✅ Approach 1 Setup: Kafka + PySpark + Grafana  

#### **On PC 1 (Kafka Producer)**  
1. Start Kafka using Docker Compose:  
```bash
docker-compose up -d
```
2. Run the Producer script:  
```bash
python producer.py
```
3. Producer will stream data from `sample_data.csv` to Kafka topics.  

#### **On PC 2 (PySpark Consumer)**  
1. Ensure PC 2 can access PC 1's IP and Kafka port (9092).  
2. Edit `subscriber.py` with PC 1's Kafka IP:  
```python
kafka_bootstrap_servers = "PC1_IP:9092"
```
3. Start PySpark consumer:  
```bash
spark-submit subscriber.py
```
4. Processed data can be viewed on the console or written to DB.  

#### **Grafana**  
- Connect Grafana to **PostgreSQL** or **InfluxDB** where processed results are stored.  
- Import dashboards for visualization.  

### ✅ Approach 2 Setup: Prometheus + Grafana Simulation  

1. Start Prometheus exporter:  
```bash
python prometheus_simulator.py
```
2. Prometheus scrapes metrics from `http://localhost:8000/metrics`.  
3. In Grafana:  
   - Add Prometheus as a data source.  
   - Build dashboards to visualize real-time metrics.  

## 📸 Screenshots  
✔ **Kafka Console Output** – Top Channels, Regional Trends  
✔ **Grafana Dashboard for Kafka Pipeline**  
✔ **Grafana Dashboard for Prometheus Simulation**  
✔ **Colab Visualizations**  


## 🔮 Future Enhancements  
- Integrate **forecasting models** (Prophet, ARIMA) into PySpark streaming.  
- Store real-time processed data in **InfluxDB** for time-series analytics.  
- Deploy pipeline using **Kubernetes** for scalability.  
