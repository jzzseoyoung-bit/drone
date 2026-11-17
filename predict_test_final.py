import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import xgboost as xgb

# Paths
train_path = r'cleaned_features/drone_train.csv'
test_path = r'cleaned_features/drone_test.csv'

# Load data
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Feature columns (consistent with training)
usable = [
    'equipment_type', 'unit_code', 'equipment_age_years', 'maintenance_type',
    'fault_category', 'severity', 'fault_count_last_30d', 'days_since_last_fault',
    'flight_hours_since_last_preventive', 'availability_rate'
]
usable = [c for c in usable if c in train_df.columns]

cat_cols = ['equipment_type', 'unit_code', 'maintenance_type', 'fault_category']

# One‑hot encode
train_enc = pd.get_dummies(train_df[usable], columns=[c for c in cat_cols if c in usable])
test_enc = pd.get_dummies(test_df[usable], columns=[c for c in cat_cols if c in usable])
# Align columns
train_enc, test_enc = train_enc.align(test_enc, join='left', axis=1, fill_value=0)

X_train = train_enc
y_train = train_df['failure_within_30days']
X_test = test_enc

# Train model (same hyper‑params as earlier)
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# Predict probabilities
proba = model.predict_proba(X_test)[:, 1]

test_df = test_df.copy()
test_df['failure_probability'] = proba

# Output identifiers + probability
if 'equipment_id' in test_df.columns:
    out = test_df[['equipment_id', 'failure_probability']]
else:
    out = test_df[['failure_probability']]

out_path = r'test_predictions.csv'
out.to_csv(out_path, index=False)
print('Predictions saved to', out_path)
