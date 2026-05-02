# 🚨 Disaster Management AI System

### 🔥 AI-Powered Emergency Response & Simulation Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)
![Framework](https://img.shields.io/badge/Frontend-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📌 Overview

The **Disaster Management AI System** is an intelligent platform designed to:

* Predict disaster **priority levels**
* Simulate **emergency response scenarios**
* Provide a **real-time dashboard** for analysis
* Optimize **resource allocation using parallel processing**

This project integrates **Machine Learning + Data Visualization + Parallel Computing** into one complete system.

---

## 🎯 Key Features

✅ AI-based **Priority Prediction** (Low → Critical)
✅ Interactive **Streamlit Dashboard**
✅ **Parallel Disaster Simulation** (multi-process)
✅ Real-time **System Monitoring (CPU & RAM)**
✅ Advanced **Data Visualization (graphs + heatmaps)**
✅ Clean and modern **Dark UI Theme**

---

## 📁 Project Structure

```
disaster_project/
│
├── generate_dataset.py       # Step 1: Generate dataset
├── train_model.py            # Step 2: Train ML models
├── parallel_simulation.py    # Step 3: Run simulation
├── app.py                   # Step 4: Dashboard app
│
├── disaster_dataset.csv     # Generated dataset
│
├── models/                  # Trained models (auto-generated)
├── graphs/                  # Visualization outputs
└── simulation_results/      # Simulation results
```

---

## ⚙️ Installation

Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit scikit-learn psutil
```

---

## 🚀 How to Run the Project

### 🔹 Step 1: Generate Dataset

```bash
python generate_dataset.py
```

---

### 🔹 Step 2: Train AI Model

```bash
python train_model.py
```

✔ Models saved in `models/`
✔ Graphs saved in `graphs/`

---

### 🔹 Step 3: Run Simulation (Optional)

```bash
python parallel_simulation.py
```

✔ Simulates disasters across multiple processes

---

### 🔹 Step 4: Launch Dashboard

```bash
streamlit run app.py
```

🌐 Open in browser:
👉 http://localhost:8501

---

## 📊 Dashboard Features

* 📈 **Analytics Tab** → Interactive graphs
* 🤖 **AI Prediction Tab** → Priority prediction + confidence
* ⚡ **Simulation Tab** → Parallel disaster simulation
* 📋 **Data Explorer** → View & download dataset
* 🌙 **Dark Mode UI** → Clean professional interface
* 🔍 **Filters** → Customize data view
* 💻 **System Monitor** → Live CPU & RAM usage

---

## 📊 Visualizations Included

* Disaster Count (Bar Chart)
* Priority Distribution (Pie Chart)
* Top Cities (Horizontal Bar)
* Severity Distribution (Histogram)
* Response Time Trend (Scatter Plot)
* Disaster vs Location (Heatmap)

---

## 🤖 Machine Learning Details

| Feature          | Description                          |
| ---------------- | ------------------------------------ |
| Algorithm        | Random Forest                        |
| Trees            | 100                                  |
| Task             | Classification (Priority Prediction) |
| Classes          | Low, Medium, High, Critical          |
| Train/Test Split | 80% / 20%                            |

### 📥 Input Features:

* Disaster Type
* Location
* Severity
* People Affected
* Ambulances
* Resources
* Response Time

---

## ⚡ Parallel Processing

* **Technology**: Python `multiprocessing`
* **Execution**: 4 parallel processes
* **Purpose**:

  * Resource allocation
  * Emergency response simulation
  * Performance optimization

---

## 💡 Usage Tips

✔ Always run in this order:

1. `generate_dataset.py`
2. `train_model.py`
3. `app.py`

✔ Use sidebar filters in dashboard
✔ Try different disaster scenarios for testing

---

## 📸 (Optional) Screenshots

> Add screenshots here for better presentation:

```
<img width="1346" height="545" alt="image" src="https://github.com/user-attachments/assets/25c56c21-0913-40ca-93ff-02d9b0be67e1" />

<img width="1200" height="571" alt="image" src="https://github.com/user-attachments/assets/0ae76dc2-bfb7-4447-acff-920c888c17a0" />

<img width="1191" height="567" alt="image" src="https://github.com/user-attachments/assets/5848794e-7076-4cee-b519-82b775ab2d02" />

```

---

## 🧠 Future Improvements

* Deep Learning models (LSTM / Neural Networks)
* Real-time API integration
* GIS-based disaster mapping
* Deployment on cloud (Streamlit Cloud / AWS)

---

## 👩‍💻 Author

**Esha Ali**
  AI / Data Science

---

## ⭐ Support

If you like this project:

👉 Give it a **star ⭐ on GitHub**
👉 Share with others

---

## 📜 License

This project is for **academic and educational purposes**.
