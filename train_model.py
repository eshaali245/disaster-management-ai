"""
=================================================
DISASTER MANAGEMENT SYSTEM - AI Model Training
=================================================
Random Forest se Priority Prediction karo.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json
import os

print("=" * 55)
print("🤖 AI MODEL TRAINING - DISASTER PRIORITY PREDICTION")
print("=" * 55)

# ─── Step 1: Data Load ───────────────────────────────────
df = pd.read_csv('disaster_dataset.csv')
print(f"\n✅ Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ─── Step 2: Label Encoding ──────────────────────────────
le_disaster  = LabelEncoder()
le_location  = LabelEncoder()
le_severity  = LabelEncoder()
le_priority  = LabelEncoder()

df['Disaster_enc']  = le_disaster.fit_transform(df['Disaster'])
df['Location_enc']  = le_location.fit_transform(df['Location'])
df['Severity_enc']  = le_severity.fit_transform(df['Severity'])
df['Priority_enc']  = le_priority.fit_transform(df['Priority'])

print("\n✅ Label Encoding Complete!")
print(f"   Priority Classes: {list(le_priority.classes_)}")

# ─── Step 3: Features & Target ───────────────────────────
features = ['Disaster_enc', 'Location_enc', 'Severity_enc',
            'People_Affected', 'Ambulance_Needed',
            'Resources_Needed', 'Response_Time']
target = 'Priority_enc'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n✅ Train/Test Split: {len(X_train)} train, {len(X_test)} test")

# ─── Step 4: Random Forest Model ─────────────────────────
print("\n🌲 Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=100, max_depth=10,
    random_state=42, n_jobs=-1
)
rf_model.fit(X_train, y_train)
rf_pred   = rf_model.predict(X_test)
rf_acc    = accuracy_score(y_test, rf_pred)
print(f"   ✅ Random Forest Accuracy: {rf_acc*100:.2f}%")

# ─── Step 5: Decision Tree Model ─────────────────────────
print("\n🌳 Training Decision Tree...")
dt_model = DecisionTreeClassifier(max_depth=8, random_state=42)
dt_model.fit(X_train, y_train)
dt_pred  = dt_model.predict(X_test)
dt_acc   = accuracy_score(y_test, dt_pred)
print(f"   ✅ Decision Tree Accuracy: {dt_acc*100:.2f}%")

# ─── Step 6: Save Models & Encoders ──────────────────────
os.makedirs('models', exist_ok=True)

with open('models/rf_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
with open('models/dt_model.pkl', 'wb') as f:
    pickle.dump(dt_model, f)
with open('models/encoders.pkl', 'wb') as f:
    pickle.dump({
        'disaster': le_disaster,
        'location': le_location,
        'severity': le_severity,
        'priority': le_priority,
    }, f)

# Save accuracy results
results = {
    'random_forest_accuracy': round(rf_acc * 100, 2),
    'decision_tree_accuracy': round(dt_acc * 100, 2),
    'best_model': 'Random Forest' if rf_acc >= dt_acc else 'Decision Tree',
    'features': features,
    'classes': list(le_priority.classes_)
}
with open('models/model_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Models saved to 'models/' folder!")

# ─── Step 7: Generate Graphs ─────────────────────────────
os.makedirs('graphs', exist_ok=True)
plt.style.use('dark_background')
colors = ['#00d4ff', '#ff6b6b', '#ffd700', '#00ff88']

# Graph 1: Model Accuracy Comparison
fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0d1117')
models_names = ['Random Forest', 'Decision Tree']
accuracies   = [rf_acc * 100, dt_acc * 100]
bars = ax.bar(models_names, accuracies, color=['#00d4ff', '#ff6b6b'],
              width=0.5, edgecolor='white', linewidth=0.5)
for bar, acc in zip(bars, accuracies):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5, f'{acc:.1f}%',
            ha='center', color='white', fontsize=12, fontweight='bold')
ax.set_ylim(0, 115)
ax.set_title('🤖 AI Model Accuracy Comparison', color='white', fontsize=14, pad=15)
ax.set_ylabel('Accuracy (%)', color='white')
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_edgecolor('#333355')
ax.yaxis.grid(True, color='#333355', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('graphs/model_accuracy.png', dpi=120, bbox_inches='tight',
            facecolor='#0a0a1a')
plt.close()

# Graph 2: Feature Importance
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0d1117')
importances = rf_model.feature_importances_
feat_labels = ['Disaster', 'Location', 'Severity',
               'People\nAffected', 'Ambulance\nNeeded',
               'Resources\nNeeded', 'Response\nTime']
sorted_idx  = np.argsort(importances)[::-1]
bar_colors  = ['#00d4ff', '#ff6b6b', '#ffd700', '#00ff88',
               '#ff9f43', '#a29bfe', '#fd79a8']
bars = ax.bar(range(len(feat_labels)),
              importances[sorted_idx],
              color=[bar_colors[i] for i in sorted_idx],
              edgecolor='white', linewidth=0.3)
ax.set_xticks(range(len(feat_labels)))
ax.set_xticklabels([feat_labels[i] for i in sorted_idx], color='white', fontsize=9)
ax.set_title('🔍 Feature Importance (Random Forest)', color='white', fontsize=14, pad=15)
ax.set_ylabel('Importance Score', color='white')
ax.tick_params(colors='white')
ax.yaxis.grid(True, color='#333355', linestyle='--', alpha=0.5)
for spine in ax.spines.values():
    spine.set_edgecolor('#333355')
plt.tight_layout()
plt.savefig('graphs/feature_importance.png', dpi=120, bbox_inches='tight',
            facecolor='#0a0a1a')
plt.close()

# Graph 3: Confusion Matrix
fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0d1117')
cm = confusion_matrix(y_test, rf_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le_priority.classes_,
            yticklabels=le_priority.classes_,
            ax=ax, linewidths=0.5, linecolor='#333355',
            annot_kws={'color': 'white', 'fontsize': 11})
ax.set_title('📊 Confusion Matrix - Random Forest', color='white', fontsize=13, pad=15)
ax.set_xlabel('Predicted Label', color='white')
ax.set_ylabel('True Label', color='white')
ax.tick_params(colors='white')
plt.tight_layout()
plt.savefig('graphs/confusion_matrix.png', dpi=120, bbox_inches='tight',
            facecolor='#0a0a1a')
plt.close()

print("✅ All graphs saved to 'graphs/' folder!")
print("\n" + "=" * 55)
print(f"🏆 BEST MODEL : {results['best_model']}")
print(f"🎯 RF Accuracy: {rf_acc*100:.2f}%")
print(f"🌳 DT Accuracy: {dt_acc*100:.2f}%")
print("=" * 55)
print("\n✅ Training Complete! Ab app.py run karo.")
