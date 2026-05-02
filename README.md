# 🚨 Disaster Management AI System
## Complete Project - Setup & Run Guide

---

## 📁 Project Files

```
disaster_project/
├── generate_dataset.py     ← Step 1: Dataset banao
├── train_model.py          ← Step 2: AI model train karo
├── parallel_simulation.py  ← Step 3: Simulation test karo
├── app.py                  ← Step 4: Dashboard run karo
├── disaster_dataset.csv    ← Auto-generated dataset
├── models/                 ← Trained AI models (auto)
│   ├── rf_model.pkl
│   ├── dt_model.pkl
│   ├── encoders.pkl
│   └── model_results.json
├── graphs/                 ← AI graphs (auto)
│   ├── model_accuracy.png
│   ├── feature_importance.png
│   └── confusion_matrix.png
└── simulation_results/     ← Simulation output (auto)
    └── latest_simulation.json
```

---

## ⚙️ Installation

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit scikit-learn psutil
```

---

## 🚀 Step-by-Step Run

### Step 1 – Dataset Generate Karo
```bash
python generate_dataset.py
```
✅ `disaster_dataset.csv` ban jayega (1000 rows)

---

### Step 2 – AI Model Train Karo
```bash
python train_model.py
```
✅ `models/` folder mein models save honge
✅ `graphs/` folder mein 3 graphs save honge

---

### Step 3 – Parallel Simulation Test Karo (Optional)
```bash
python parallel_simulation.py
```
✅ 12 disasters ko 4 parallel nodes pe simulate karega

---

### Step 4 – Dashboard Run Karo
```bash
streamlit run app.py
```
✅ Browser mein automatically open ho jayega
✅ URL: http://localhost:8501

---

## 🎯 Dashboard Features

| Feature | Description |
|---------|-------------|
| 📊 Analytics Tab | 5 interactive graphs |
| 🤖 AI Tab | Priority prediction + confidence |
| ⚡ Simulation Tab | Live parallel disaster simulation |
| 📋 Data Tab | Dataset explorer + download |
| 🌙 Dark Theme | Full black professional UI |
| 🔍 Filters | Sidebar se filter karo |
| 💻 System Monitor | CPU + RAM live |

---

## 📊 Graphs in Dashboard

1. **Disaster Cases Bar Chart** - Har disaster ka count
2. **Priority Pie Chart** - Priority distribution
3. **Top 10 Cities** - Horizontal bar chart
4. **Severity Histogram** - People affected distribution
5. **Response Time Trend** - Scatter plot by severity
6. **Disaster-Location Heatmap** - 2D matrix

---

## 🤖 AI Model Info

- **Algorithm**: Random Forest (100 trees)
- **Task**: Priority Prediction (Low/Medium/High/Critical)
- **Features**: Disaster, Location, Severity, People Affected,
               Ambulances, Resources, Response Time
- **Split**: 80% Train, 20% Test

---

## ⚡ Parallel Processing

- **Library**: `multiprocessing` (Python built-in)
- **Nodes**: 4 parallel processes
- **Tasks**: Resource allocation, ambulance dispatch,
            response time calculation
- **Simulation**: 4-24 disasters simultaneously

---

## 💡 Tips

- Pehle `generate_dataset.py` zaroor run karo
- Phir `train_model.py` run karo (models + graphs banenge)
- Finally `streamlit run app.py` se dashboard open karo
- Sidebar filters use karo data explore karne ke liye

---

*Developed for Academic Disaster Management Project*
