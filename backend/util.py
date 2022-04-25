import circlify
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

matplotlib.rcParams['font.size'] = 17
def plotHeatMap(times, lebals,colors,tag_colors ,filePath):
  circles = circlify.circlify(times, show_enclosure=False,
  target_enclosure=circlify.Circle(x=0,y=0,r=2))


  fig, ax = plt.subplots(figsize=(10,10))
  ax.set_title("食物熱搜圖", fontsize=48)
  ax.axis('off')

  lim = max(
    max(
      abs(circle.x) + circle.r,
      abs(circle.y) + circle.r,
    ) for circle in circles
  )
  plt.xlim(-lim-0.5, lim+0.5)
  plt.ylim(-lim, lim+1)

  handles = []
  for tc in tag_colors:
    color = tc['color']
    lebal = tc['tag']
    patch = mpatches.Patch(color=f'#{color}', label=f'{lebal}')
    handles.append(patch)

  for circle, label, time, color in zip(circles, lebals, times, colors):
    x, y, r = circle
    ax.add_patch(plt.Circle((x,y), r, alpha=0.2, linewidth=2, fill=True, facecolor=f'#{color}'))
    ax.annotate(f'{label}\n{int(time)}次', (x,y), va='center', ha='center', fontsize=time*3)

  ax.legend(handles=handles, prop={'size': 24}, loc='upper right')
  fig.savefig(f'{filePath}/plot.png')

