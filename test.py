import circlify
import matplotlib.pyplot as plt

circles = circlify.circlify([19, 17, 13, 11, 7, 5, 3, 2, 1], show_enclosure=False,
target_enclosure=circlify.Circle(x=0,y=0,r=1))
# circlify.bubbles(circles)

fig, ax = plt.subplots(figsize=(10,10))
ax.set_title('test')
ax.axis('off')

lim = max(
  max(
    abs(circle.x) + circle.r,
    abs(circle.y) + circle.r,
  ) for circle in circles
)

plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

for circle in circles:
  x, y, r = circle
  ax.add_patch(plt.Circle((x,y), r, alpha=0.2, linewidth=2, fill=False))

plt.show()