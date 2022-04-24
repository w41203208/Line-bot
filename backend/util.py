from tkinter import font
import circlify
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager as fm

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.size'] = 13
def test(times, lebals, colors, tag_colors ,filePath):
  circles = circlify.circlify(times, show_enclosure=False,
  target_enclosure=circlify.Circle(x=0,y=0,r=2))

  fig, ax = plt.subplots(figsize=(10,10))

  ax.set_title("食物熱搜圖")
  ax.axis('off')

  lim = max(
    max(
      abs(circle.x) + circle.r,
      abs(circle.y) + circle.r,
    ) for circle in circles
  )
  plt.xlim(-lim, lim)
  plt.ylim(-lim, lim)

  handles = []
  for tc in tag_colors:
    color = tc['color']
    lebal = tc['tag']
    patch = mpatches.Patch(color=f'#{color}', label=f'{lebal}')
    handles.append(patch)

  for circle, label, time, color in zip(circles, lebals, times, colors):
    x, y, r = circle
    ax.add_patch(plt.Circle((x,y), r, alpha=0.2, linewidth=2, fill=True, facecolor=f'#{color}'))
    ax.annotate(f'{label}:{int(time)}times', (x,y), va='center', ha='center')

  ax.legend(handles=handles)
  fig.savefig(f'{filePath}/plot.png')

