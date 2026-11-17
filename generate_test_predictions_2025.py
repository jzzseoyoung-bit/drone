import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load enriched test data (has maintenance_date)
test_path = r'cleaned_features/drone_test.csv'
prob_path = r'test_predictions.csv'

test_df = pd.read_csv(test_path)
prob_df = pd.read_csv(prob_path)

# Merge on equipment_id (assuming unique per row). Use left join to keep all rows.
merged = test_df.merge(prob_df, on='equipment_id', how='left')
# Rename probability column
merged.rename(columns={'failure_probability': 'prob'}, inplace=True)
# Ensure maintenance_date format
merged['maintenance_date'] = pd.to_datetime(merged['maintenance_date']).dt.strftime('%Y-%m-%d')
# Select required columns
out_df = merged[['equipment_id', 'maintenance_date', 'prob']]
out_path = r'test_predictions_2025.csv'
out_df.to_csv(out_path, index=False)
print('Saved predictions to', out_path)
