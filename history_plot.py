import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === 可调参数 ===
INPUT_CSV = "altitude_velocity_acceleration_30s.csv"
T_START = 6150     # s
T_END = 19000      # s
REF_ALT_FT = 36000 # 参考高度（英尺）
OUT_CSV = "altitude_and_reference_6150_19000.csv"
OUT_FIG = "altitude_vs_reference_6150_19000.png"

# 1) 读取与构造时间轴（从0开始的秒）
df = pd.read_csv(INPUT_CSV)
df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

# 2) 选定分析区间
mask = (df["Time (s)"] >= T_START) & (df["Time (s)"] <= T_END)
df_range = df.loc[mask, ["Time (s)", "Altitude"]].copy()

# 3) 构造参考高度曲线（恒定）
df_range["Reference"] = REF_ALT_FT

# 4) 保存数据表（可选）
df_range.to_csv(OUT_CSV, index=False)

# 5) 画图：同一张图两条曲线
plt.figure(figsize=(10, 4))  # 宽一些、扁一些
plt.plot(df_range["Time (s)"], df_range["Altitude"], label="Altitude")
plt.plot(df_range["Time (s)"], df_range["Reference"], label="Reference", linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (feet)")
plt.title(f"Altitude vs Reference ({T_START}s–{T_END}s)")
plt.grid(True, linewidth=0.5, alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=200)
plt.show()
