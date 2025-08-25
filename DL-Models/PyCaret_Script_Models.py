# %% [markdown]
# # Turmeric Price Prediction with PyCaret
# 
# This notebook trains and evaluates many regression models using the PyCaret library
# to predict the **Modal Price (Rs./Quintal)** of turmeric based on weather data,
# crop variety, location, and other parameters.
# 
# It includes:
# - Data loading & preprocessing
# - PyCaret regression setup
# - Model comparison across many algorithms
# - Tuning of the best models
# - Ensembling and stacking
# - Final model evaluation and saving
# - Future prediction example

# %%

import pandas as pd
from pycaret.regression import *

# Load dataset
df = pd.read_csv("../Weather_Merged_CSVs/Turmeric.csv")

# Inspect first few rows
df.head()

# %% [markdown]
# ## Data Preprocessing
# Convert `Price Date` to datetime and extract useful features.

# %%
df['Price Date'] = pd.to_datetime(df['Price Date'], errors='coerce')

# Extract year, month, day as separate features
df['Year'] = df['Price Date'].dt.year
df['Month'] = df['Price Date'].dt.month
df['Day'] = df['Price Date'].dt.day

# %% [markdown]
# ## PyCaret Regression Setup

# %%
# Initialize PyCaret regression setup
reg_setup = setup(
    data=df,
    target="Modal Price (Rs./Quintal)",
    session_id=42,
    normalize=True,
    transformation=True,
    polynomial_features=False,
    feature_interaction=True,
    categorical_features=['District Name', 'Market Name', 'Commodity', 'Variety', 'Grade', 'Day Of Week'],
    ignore_features=[],
    numeric_features=['Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 'lookback_temp_mean', 'lookback_precip_sum', 'Year', 'Month', 'Day'],
    silent=True,
    use_gpu=True
)

# %% [markdown]
# ## Compare Many Regression Models

# %%
best_models = compare_models(sort='RMSE', n_select=5)  # Select top 5 models by RMSE

# %% [markdown]
# ## Tune the Top Models

# %%
tuned_models = [tune_model(m) for m in best_models]

# %% [markdown]
# ## Ensemble the Tuned Models

# %%
ensembled_models = [ensemble_model(m) for m in tuned_models]

# %% [markdown]
# ## Stack the Models

# %%
stacked_model = stack_models(ensembled_models)

# %% [markdown]
# ## Evaluate the Stacked Model

# %%
evaluate_model(stacked_model)

# %% [markdown]
# ## Finalize the Best Model

# %%
final_model = finalize_model(stacked_model)

# %% [markdown]
# ## Save the Final Model

# %%
save_model(final_model, "final_turmeric_price_model")

# %% [markdown]
# ## Make Predictions on the Dataset (for RMSE Calculation)

# %%
predictions = predict_model(final_model, data=df)
predictions[['Modal Price (Rs./Quintal)', 'Label']]

# %% [markdown]
# ### RMSE, MAE, R² Scores

# %%
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

rmse = np.sqrt(mean_squared_error(predictions['Modal Price (Rs./Quintal)'], predictions['Label']))
mae = mean_absolute_error(predictions['Modal Price (Rs./Quintal)'], predictions['Label'])
r2 = r2_score(predictions['Modal Price (Rs./Quintal)'], predictions['Label'])

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R²: {r2:.4f}")

# %% [markdown]
# ## Example: Predict Future Prices

# %%
# Example future data (replace with real values)
future_data = df.sample(5).drop(columns=["Modal Price (Rs./Quintal)"])  # Simulated

# Predict future prices
future_predictions = predict_model(final_model, data=future_data)
future_predictions