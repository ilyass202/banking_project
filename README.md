# 🚀 Real-Time Data Engineering Pipeline
### End-to-End CDC, Streaming, Lakehouse & Data Orchestration

<p align="center">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Debezium-FF6B35?style=for-the-badge&logo=debezium&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" />
</p>

---

## 📌 Overview

This project aims to design and implement a scalable end-to-end data engineering pipeline that captures database changes in near real time, processes and transforms incoming data, and delivers reliable business-ready datasets for analytical purposes.

The architecture combines **Change Data Capture (CDC)**, distributed event streaming, cloud-based data processing, Medallion Architecture, and workflow orchestration.

The objective is to build a modern data platform capable of continuously synchronizing operational data with an analytical environment while ensuring data quality, consistency, scalability, and traceability.

## 🏗️ Architecture & Data Flow

The pipeline follows a distributed architecture composed of interconnected components:

```text
                OPERATIONAL DATABASE
                     PostgreSQL
                         |
                         |
                  Debezium CDC
                         |
                         |
                   Kafka Connect
                         |
                         |
                   Apache Kafka
                  (Event Streaming)
                         |
                         |
                  Databricks
                         |
                         |
                MEDALLION ARCHITECTURE
                         |
           +-------------+-------------+
           |             |             |
        BRONZE         SILVER         GOLD
           |             |             |
       Raw Events    Clean Data    Business Data
           |             |             |
           +-------------+-------------+
                         |
                         |
                   DATA WAREHOUSE
                         |
                         |
                BI & Business Analytics

              Apache Airflow
          (Workflow Orchestration)
```

### 🔄 Pipeline Components

| Stage | Component | Description |
|---|---|---|
| 01 | PostgreSQL | Stores operational business data. |
| 02 | Debezium | Captures database changes through transaction logs. |
| 03 | Kafka Connect | Manages CDC connectors and publishes change events. |
| 04 | Apache Kafka | Provides distributed event streaming and message delivery. |
| 05 | Databricks | Processes and transforms incoming data using Apache Spark. |
| 06 | Medallion Architecture | Organizes data into Bronze, Silver, and Gold layers. |
| 07 | Data Warehouse | Stores curated business-ready datasets for analytical consumption. |
| 08 | Apache Airflow | Orchestrates pipeline execution, dependencies, and monitoring. |

## 🥉 Medallion Architecture

The project implements a three-layer data architecture to progressively improve data quality and usability.

### 🥉 Bronze Layer — Raw Data
- Ingest raw CDC events from Kafka.
- Preserve original event payloads and metadata.
- Maintain source information and ingestion timestamps.
- Provide traceability and data lineage.

### 🥈 Silver Layer — Cleaned & Validated Data
- Parse and normalize incoming records.
- Handle INSERT, UPDATE, and DELETE operations.
- Remove duplicates and manage inconsistent records.
- Apply data quality and validation rules.
- Produce structured and reliable datasets.

### 🥇 Gold Layer — Business-Ready Data
- Aggregate and transform validated datasets.
- Build analytical tables and business indicators.
- Optimize datasets for reporting and analytical queries.
- Prepare curated data for BI dashboards and business intelligence.

## 🛠️ Technology Stack



A modular and scalable data platform demonstrating the integration of distributed systems, real-time data ingestion, data lakehouse engineering, and analytical data management.

The architecture is designed to provide a foundation for extending the pipeline to geospatial datasets and spatial analytics.
