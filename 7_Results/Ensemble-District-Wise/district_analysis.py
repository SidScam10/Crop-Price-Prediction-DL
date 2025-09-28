import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def calculate_mape(actual, predicted):
    actual, predicted = np.array(actual), np.array(predicted)
    nonzero_mask = actual != 0
    if not np.any(nonzero_mask):
        return float('inf')
    mape = np.mean(np.abs((actual[nonzero_mask] - predicted[nonzero_mask]) / actual[nonzero_mask])) * 100
    return mape

def analyze_district_performance(df):
    district_groups = df.groupby('District_Name')
    district_results = []
    for district_name, group in district_groups:
        actual = group['Actual_Price']
        predicted_col = 'ENSEMBLE_(Average)_Pred' if 'ENSEMBLE_(Average)_Pred' in group.columns else 'Ensemble_Pred'
        predicted = group[predicted_col]
        mape = calculate_mape(actual, predicted)
        accuracy = 100 - mape
        rmse = np.sqrt(np.mean((actual - predicted)**2))
        district_results.append({
            'District': district_name,
            'Accuracy (%)': accuracy,
            'MAPE (%)': mape,
            'RMSE': rmse,
            'Prediction_Count': len(group)
        })
    summary_df = pd.DataFrame(district_results)
    summary_df = summary_df.sort_values(by='Accuracy (%)', ascending=False).reset_index(drop=True)
    return summary_df

# --- Main Execution ---
district_wise_folder = r'c:\Users\siddh\OneDrive\Documents\Agricultural Datasets\7_Results\Ensemble-District-Wise'
output_folder = r'c:\Users\siddh\OneDrive\Documents\Agricultural Datasets\7_Results\District-Wise-Crop-Graphs'

csv_files = glob.glob(os.path.join(district_wise_folder, '*.csv'))

for csv_file in csv_files:
    crop_name = os.path.basename(csv_file).replace('_district_level_predictions.csv', '').replace('.csv', '')
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        continue

    district_summary = analyze_district_performance(df)
    if district_summary.empty:
        print(f"No data for {crop_name}")
        continue

    print(f"\n--- District-Level Performance Summary for {crop_name} ---")
    print(district_summary.to_string())

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(district_summary['District'], district_summary['Accuracy (%)'], color='skyblue')
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title(f'Ensemble Model Accuracy by District for {crop_name}', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval:.2f}%', ha='center', va='bottom')
    plt.tight_layout()
    output_filename = os.path.join(output_folder, f'{crop_name}_accuracy_bar_chart.png')
    plt.savefig(output_filename, dpi=300)
    print(f"Bar graph saved to '{output_filename}'")
    plt.close(fig)