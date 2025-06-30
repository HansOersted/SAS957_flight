import pandas as pd

user_input_end_time = 15390  # select the end time for the subset, 

input_csv = "tracking_error_dynamics_6150s_to_19000s.csv"
df = pd.read_csv(input_csv)

closest_end_time = df["Time (s)"].iloc[(df["Time (s)"] - user_input_end_time).abs().argmin()]
print(f"The closest end time is: {closest_end_time} s")

subset_df = df[(df["Time (s)"] >= 6150) & (df["Time (s)"] <= closest_end_time)].copy()

converted_df = subset_df.rename(columns={
    "tracking_error": "e",
    "tracking_error_derivative": "de",
    "tracking_error_second_derivative": "dde"
})[["Time (s)", "e", "de", "dde"]]

output_csv = f"lyapunov_training_data_6150s_to_{int(closest_end_time)}s.csv"
converted_df.to_csv(output_csv, index=False)
print(f"Output file saved as: {output_csv}")
