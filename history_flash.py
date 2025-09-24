import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from math import ceil

# ---------- CLI ----------
p = argparse.ArgumentParser(description="Animated Altitude vs Reference")
p.add_argument("--input", default="altitude_velocity_acceleration_30s.csv")
p.add_argument("--t-start", type=int, default=6150, help="range start (s)")
p.add_argument("--t-end", type=int, default=19000, help="range end (s)")
p.add_argument("--ref", type=float, default=36000, help="reference altitude (ft)")
p.add_argument("--interval-ms", type=int, default=60, help="frame interval (ms)")
p.add_argument("--ppf", type=int, default=1, help="points per frame")
p.add_argument("--start-at", type=int, default=None,
               help="playback start time within [t-start, t-end] (s). Default=t-start")
p.add_argument("--out", default="altitude_vs_reference_animated.gif")
args = p.parse_args()

# ---------- LaTeX (with graceful fallback) ----------
try:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 12,
    })
    _latex_ok = True
except Exception as e:
    print("[warn] LaTeX not available, falling back to Matplotlib's default fonts.")
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "serif",
        "font.size": 12,
    })
    _latex_ok = False

# ---------- Load & slice ----------
df = pd.read_csv(args.input)
df["Time (s)"] = df["Timestamp"] - df["Timestamp"].iloc[0]

T_START = args.t_start
T_END = args.t_end
REF_ALT_FT = args.ref
FRAME_INTERVAL_MS = args.interval_ms
POINTS_PER_FRAME = max(1, args.ppf)

mask = (df["Time (s)"] >= T_START) & (df["Time (s)"] <= T_END)
df_range = df.loc[mask, ["Time (s)", "Altitude"]].copy()
if df_range.empty or len(df_range) < 2:
    raise ValueError("所选时间段数据不足。")

df_range["Reference"] = REF_ALT_FT
times = df_range["Time (s)"].to_numpy()
alt = df_range["Altitude"].to_numpy()
ref = df_range["Reference"].to_numpy()
n = len(times)

# 播放起点（不改变导出的区间，只决定动画从哪里开始揭示）
start_at = T_START if args.start_at is None else args.start_at
if not (T_START <= start_at <= T_END):
    raise ValueError("--start-at 必须在 [t-start, t-end] 内")
start_idx = int(np.searchsorted(times, start_at, side="left"))

# 帧数（从 start_idx 开始往后揭示）
num_frames = ceil((n - start_idx) / POINTS_PER_FRAME)
num_frames = max(1, num_frames)

# ---------- Figure ----------
fig, ax = plt.subplots(figsize=(10, 4))
(line_alt,) = ax.plot([], [], label="Altitude")
(line_ref,) = ax.plot([], [], linestyle="--", label="Reference")
(point_now,) = ax.plot([], [], marker="o", linestyle="", alpha=0.9)

title_text = f"Altitude vs Reference ({T_START}s–{T_END}s)"
ax.set_title(title_text)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Altitude (feet)")
ax.grid(True, linewidth=0.5, alpha=0.6)
ax.legend(loc="best")
ax.margins(x=0.02, y=0.05)  # 适度留白

def init():
    # 不预设范围，不画空白固定框，完全由数据推动
    line_alt.set_data([], [])
    line_ref.set_data([], [])
    point_now.set_data([], [])
    return (line_alt, line_ref, point_now)

def update(i):
    # 每帧新增 POINTS_PER_FRAME 个点（从 start_idx 起）
    end_idx = min(start_idx + (i + 1) * POINTS_PER_FRAME, n)
    if end_idx <= start_idx:
        # 还没到起始点，保持空
        return (line_alt, line_ref, point_now)

    x = times[start_idx:end_idx]
    y_alt = alt[start_idx:end_idx]
    y_ref = ref[start_idx:end_idx]

    line_alt.set_data(x, y_alt)
    line_ref.set_data(x, y_ref)
    point_now.set_data([x[-1]], [y_alt[-1]])

    # 动态自适应坐标（不固定空白）
    ax.relim()
    ax.autoscale_view()

    return (line_alt, line_ref, point_now)

anim = FuncAnimation(
    fig, update, init_func=init,
    frames=num_frames, interval=FRAME_INTERVAL_MS,
    blit=False  # 自适应缩放需关闭 blit
)

fps = 1000 / FRAME_INTERVAL_MS if FRAME_INTERVAL_MS > 0 else 30
anim.save(args.out, writer=PillowWriter(fps=fps))
plt.close(fig)
print(f"Saved: {args.out}")
