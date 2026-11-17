import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve, auc
from sklearn.model_selection import train_test_split
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Load data
train_path = r'cleaned_features/drone_train.csv'
valid_path = r'cleaned_features/drone_this_month.csv'

df_train = pd.read_csv(train_path)
df_valid = pd.read_csv(valid_path)

# Ensure date column exists
if 'maintenance_date' not in df_train.columns:
    raise ValueError('maintenance_date column missing')

df_train['date'] = pd.to_datetime(df_train['maintenance_date'])
df_valid['date'] = pd.to_datetime(df_valid['maintenance_date'])

# Period split for validation within train data (as per guidelines)
# Use training part before 2024-07-01, validation part between 2024-07-01 and 2024-12-31
train_data = df_train[df_train['date'] < '2024-07-01']
valid_data = df_train[(df_train['date'] >= '2024-07-01') & (df_train['date'] <= '2024-12-31')]

# Feature columns (selected usable columns)
usable = [
    'equipment_type', 'unit_code', 'equipment_age_years', 'maintenance_type',
    'fault_category', 'severity', 'fault_count_last_30d', 'days_since_last_fault',
    'flight_hours_since_last_preventive', 'availability_rate'
]
# Ensure columns exist, drop missing
usable = [col for col in usable if col in train_data.columns]

# One-hot encode categorical features
cat_cols = ['equipment_type', 'unit_code', 'maintenance_type', 'fault_category']
train_enc = pd.get_dummies(train_data[usable], columns=[c for c in cat_cols if c in usable])
valid_enc = pd.get_dummies(valid_data[usable], columns=[c for c in cat_cols if c in usable])
# Align columns
train_enc, valid_enc = train_enc.align(valid_enc, join='left', axis=1, fill_value=0)

X_train = train_enc
y_train = train_data['failure_within_30days']
X_valid = valid_enc
y_valid = valid_data['failure_within_30days']

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# Predictions
proba_valid = model.predict_proba(X_valid)[:,1]
precision, recall, _ = precision_recall_curve(y_valid, proba_valid)
pr_auc = auc(recall, precision)

# Monthly top-20 failures
valid_data = valid_data.copy()
valid_data['score'] = proba_valid
valid_data['month'] = valid_data['date'].dt.to_period('M')
monthly_top20 = valid_data.groupby('month').apply(lambda g: g.nlargest(20, 'score')['failure_within_30days'].sum())
monthly_top20 = monthly_top20.reset_index(name='top20_failures')

# Baseline: random 20 selection
np.random.seed(0)

def baseline_random(df_month):
    return df_month.sample(min(20, len(df_month)))['failure_within_30days'].sum()

def baseline_oldest(df_month):
    sort_col = 'equipment_age_years' if 'equipment_age_years' in df_month.columns else None
    if sort_col:
        return df_month.nlargest(min(20, len(df_month)), sort_col)['failure_within_30days'].sum()
    else:
        return np.nan

baseline = valid_data.groupby('month').apply(lambda g: pd.Series({
    'random': baseline_random(g),
    'oldest': baseline_oldest(g)
})).reset_index()

# Save results
out_path = r'model_results.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# 모델 학습 및 검증 결과\n\n')
    f.write(f'**PR-AUC**: {pr_auc:.4f}\n\n')
    f.write('## 월별 Top‑20 실제 재고장 수\n')
    f.write(monthly_top20.to_markdown(index=False))
    f.write('\n\n')
    f.write('## 기준선 비교 (무작위 vs 오래된 순)\n')
    f.write(baseline.to_markdown(index=False))
    f.write('\n')
print('Results written to', out_path)
