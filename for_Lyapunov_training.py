import pandas as pd

user_input_end_time = 15450  # select the end time in seconds, e.g., 15450 seconds

df = pd.read_csv("tracking_error_dynamics_6150s_to_19000s.csv")

closest_end_time = df["Time (s)"].iloc[(df["Time (s)"] - user_input_end_time).abs().argmin()]
print(f"Selected end time: {closest_end_time} s")

subset_df = df[(df["Time (s)"] >= 6150) & (df["Time (s)"] <= closest_end_time)].copy()

packed_df = pd.DataFrame({
    "e[0]": subset_df["tracking_error"],
    "e[1]": subset_df["tracking_error_derivative"],
    "de[0]": subset_df["tracking_error_derivative"],
    "de[1]": subset_df["tracking_error_second_derivative"]
})

output_csv = f"packed_lyapunov_input_6150s_to_{int(closest_end_time)}s.csv"
packed_df.to_csv(output_csv, index=False)
print(f"Output file saved as: {output_csv}")
