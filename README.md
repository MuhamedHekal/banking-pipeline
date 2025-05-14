
# Banking Pipeline

This project implements a data pipeline for banking-related datasets. It automates the extraction, transformation, and loading (ETL) of banking data into a data warehouse using Apache Hive and HDFS. The pipeline is built with Python.

---

## Project Overview

The banking-pipeline project provides a scalable and modular framework to process raw banking datasets, apply necessary transformations, and load them into Hive tables stored on HDFS. This setup enables efficient analytics on financial data using big data technologies.

---

## Repository Structure

```
banking-pipeline/
│
├── src/                          # Source code for the pipeline
│   ├── core/                     # Core base classes 
│   ├── transformers/             # Data transformation classes for different datasets
│   ├── component/                # modules for listen, extract , utilities and writer to HDFS
│   ├── services/                 # error handling module, encryptor, and email notifier , etc ...
│
├── Incoming_data/                # Input raw data files (CSV, Parquet, etc.)
│
├── configs/                      # Configuration files and environment settings
│
├── requirements.txt              # Python dependencies
│
└── README.md                     # Project documentation (this file)

```

---

## Key Components

- **Extractors:** Load raw input files and perform initial validation (in `src/components/extractor/`).
- **Transformers:** Clean, enrich, and transform raw data to structured formats (in `src/transformers/`).
- **writers:** Save transformed data efficiently on HDFS (in `src/components/writers/`).
- **Core:** Base classes and orchestration logic connecting the pipeline stages (in `src/core/`).
- **Main Script:** Coordinates the full ETL workflow (`src/build_pipeline.py`).

---

## Getting Started

### Prerequisites

- Running Hadoop & Hive services (can be containerized or installed locally)
- Python 3.8 or above

### Installation

1. Clone the repository:

```bash
git clone https://github.com/MuhamedHekal/banking-pipeline.git
cd banking-pipeline
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables or settings under `configs/`.

4. Ensure Hadoop cluster are up and accessible.

### Running the Pipeline

Run the main pipeline script to execute the full ETL process:

```bash
python -m src.build_pipeline
```

