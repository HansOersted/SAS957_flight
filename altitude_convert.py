import pandas as pd
import numpy as np

df = pd.read_csv("SK957_37f9789a.csv")

df["TimeDiff"] = df["Timestamp"].diff()

df["V_vertical"] = df["Altitude"].diff() / df["TimeDiff"]
df["A_vertical"] = df["V_vertical"].diff() / df["TimeDiff"]

df.dropna(subset=["V_vertical", "A_vertical"], inplace=True)

# dt is 30 seconds
start_time = df["Timestamp"].iloc[0]
end_time = df["Timestamp"].iloc[-1]
uniform_timestamps = np.arange(start_time, end_time + 1, 30)

interp_df = pd.DataFrame({"Timestamp": uniform_timestamps})
interp_df["Altitude"] = np.interp(uniform_timestamps, df["Timestamp"], df["Altitude"])
interp_df["V_vertical"] = np.interp(uniform_timestamps, df["Timestamp"], df["V_vertical"])
interp_df["A_vertical"] = np.interp(uniform_timestamps, df["Timestamp"], df["A_vertical"])

interp_df.to_csv("altitude_velocity_acceleration_30s.csv", index=False)
