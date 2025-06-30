import pandas as pd

df = pd.read_csv("altitude_velocity_acceleration_30s.csv")
df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

# Selected time 6150s ~ 19000s
df_range = df[(df["Time (s)"] >= 6150) & (df["Time (s)"] <= 19000)].copy()

df_range["tracking_error"] = 36000 - df_range["Altitude"]
df_range["tracking_error_derivative"] = -df_range["V_vertical"]
df_range["tracking_error_second_derivative"] = -df_range["A_vertical"]

result = df_range[["Time (s)", "tracking_error", "tracking_error_derivative", "tracking_error_second_derivative"]]

result.to_csv("tracking_error_dynamics_6150s_to_19000s.csv", index=False)
