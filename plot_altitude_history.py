import pandas as pd
import matplotlib.pyplot as plt

# 启用 LaTeX 字体
plt.rcParams["text.usetex"] = True
plt.rcParams["font.size"] = 14  

# 读取原始数据
df = pd.read_csv("SK957_37f9789a.csv")

# 绘图
plt.figure(figsize=(12, 3.5))  # 长长扁扁
plt.plot(df["Timestamp"], df["Altitude"], 
         color="#1E90FF", linewidth=2.0)  # 换成亮蓝色

plt.xlabel(r"\textbf{Timestamp (s)}")
plt.ylabel(r"\textbf{Altitude (feet)}")
plt.title(r"\textbf{Altitude History}")
plt.grid(True)

# 禁止科学计数法 offset
ax = plt.gca()
ax.ticklabel_format(style='plain', axis='x', useOffset=False)

plt.tight_layout()
plt.show()
