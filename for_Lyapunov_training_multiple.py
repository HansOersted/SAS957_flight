import pandas as pd
import numpy as np

df = pd.read_csv("tracking_error_dynamics_6150s_to_19000s.csv")

for user_input_end_time in range(15900, 16140 + 1, 30):
    closest_end_time = df["Time (s)"].iloc[(df["Time (s)"] - user_input_end_time).abs().argmin()]
    print(f"Selected end time: {closest_end_time} s")

    subset_df = df[(df["Time (s)"] >= 15870) & (df["Time (s)"] <= closest_end_time)].copy()

    e = subset_df[["tracking_error", "tracking_error_derivative"]].to_numpy()
    de = subset_df[["tracking_error_derivative", "tracking_error_second_derivative"]].to_numpy()

    output_filename = f"training_data_15870s_to_{int(closest_end_time)}s.npz"
    np.savez(output_filename, e=e, de=de)
    print(f"Training data saved as: {output_filename}")
