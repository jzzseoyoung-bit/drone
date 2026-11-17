import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Load data
train_path = r'cleaned_features/drone_train.csv'
df = pd.read_csv(train_path)

# Ensure date column
if 'maintenance_date' not in df.columns:
    raise ValueError('maintenance_date missing')
df['date'] = pd.to_datetime(df['maintenance_date'])

# Validation period within train (2024-07 to 2024-12)
valid = df[(df['date'] >= '2024-07-01') & (df['date'] <= '2024-12-31')].copy()

# Feature columns (same as earlier)
usable = [
    'equipment_type', 'unit_code', 'equipment_age_years', 'maintenance_type',
    'fault_category', 'severity', 'fault_count_last_30d', 'days_since_last_fault',
    'flight_hours_since_last_preventive', 'availability_rate'
]
usable = [c for c in usable if c in df.columns]

cat_cols = ['equipment_type', 'unit_code', 'maintenance_type', 'fault_category']
train = df[df['date'] < '2024-07-01']
train_enc = pd.get_dummies(train[usable], columns=[c for c in cat_cols if c in usable])
valid_enc = pd.get_dummies(valid[usable], columns=[c for c in cat_cols if c in usable])
train_enc, valid_enc = train_enc.align(valid_enc, join='left', axis=1, fill_value=0)

X_train = train_enc
y_train = train['failure_within_30days']
X_valid = valid_enc
y_valid = valid['failure_within_30days']

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)
proba = model.predict_proba(X_valid)[:,1]
valid['score'] = proba

# Evaluate thresholds
costs = []
thresholds = np.arange(0, 1.001, 0.01)
for thr in thresholds:
    missed = ((y_valid == 1) & (proba < thr)).sum()
    flagged = (proba >= thr).sum()
    cost = missed * 300 + flagged * 60
    costs.append((thr, missed, flagged, cost))

best = min(costs, key=lambda x: x[3])
# Recompute with missed cost 600
costs2 = []
for thr in thresholds:
    missed = ((y_valid == 1) & (proba < thr)).sum()
    flagged = (proba >= thr).sum()
    cost = missed * 600 + flagged * 60
    costs2.append((thr, missed, flagged, cost))
best2 = min(costs2, key=lambda x: x[3])

out_path = r'risk_threshold.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# 위험 표시 기준 (Validation Period)\n\n')
    f.write('## 원래 비용 가정 (missed=300만원, flagged=60만원)\n')
    f.write(f"- 최적 임계값: {best[0]:.2f}\n")
    f.write(f"- 놓친 재고장 수: {best[1]}\n")
    f.write(f"- 기준 이상 건수 (예측 양성): {best[2]}\n")
    f.write(f"- 총 비용: {best[3]}만원\n\n")
    f.write('## 놓친 재고장 비용을 600만원으로 변경\n')
    f.write(f"- 최적 임계값: {best2[0]:.2f}\n")
    f.write(f"- 놓친 재고장 수: {best2[1]}\n")
    f.write(f"- 기준 이상 건수: {best2[2]}\n")
    f.write(f"- 총 비용: {best2[3]}만원\n")
    f.write('\n---\n')
    f.write('**참고**: 검증 기간은 2024‑07~2024‑12이며, 2025 시험 데이터는 사용하지 않았습니다.\n')
print('Results written to', out_path)
