import circlify
import matplotlib.pyplot as plt
from matplotlib import font_manager
def test(arrs, lebals, filePath):

  circles = circlify.circlify(arrs, show_enclosure=False,
  target_enclosure=circlify.Circle(x=0,y=0,r=2))


  fig, ax = plt.subplots(figsize=(10,10))
  ax.axis('off')

  lim = max(
    max(
      abs(circle.x) + circle.r,
      abs(circle.y) + circle.r,
    ) for circle in circles
  )
  plt.xlim(-lim, lim)
  plt.ylim(-lim, lim)

  colors = plt.rcParams["axes.prop_cycle"]()
  for circle, label, arr in zip(circles, lebals, arrs):
    print(circle)
    x, y, r = circle
    ax.add_patch(plt.Circle((x,y), r, alpha=0.2, linewidth=2, fill=True, facecolor=next(colors)['color']))
    ax.annotate(f'{label}:{int(arr)}times', (x,y), va='center', ha='center')

  fig.savefig(f'{filePath}/plot.png')

