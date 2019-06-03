import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

import numpy as np

def makeWheelImg(angle, show=False):
	center = np.array([0.5, 0.5])
	radius = 0.2
	shlefsize = np.array([0.2, 0.06])
	imgFileName = "wheel.png"

	def pol2cart(rho, phi):
	    phi = phi/360.0*2*3.1415
	    x = rho * np.cos(phi)
	    y = rho * np.sin(phi)
	    return np.array([x, y])


	fig, ax = plt.subplots()

	def drawShelf(name, color, angle, active=False):
		if active :
			edgecolor = "red"
			linewidth = 4
		else : 
			edgecolor = "black"
			linewidth = 2
		pos = center + pol2cart(radius, angle)
		shelf = mpatches.Rectangle(pos - shlefsize/2, shlefsize[0], shlefsize[1], ec=edgecolor, fc=color, alpha=1, lw=linewidth)
		plt.text(pos[0], pos[1], name, va="center", ha="center", family='sans-serif', size=14, color=edgecolor)
		ax.add_patch(shelf)

	circle = mpatches.Circle(center, radius, fill=False, ec="black", lw=2)
	ax.add_patch(circle)

	circle = mpatches.Circle(center, radius/10, fill=True, ec="black", fc="black")
	ax.add_patch(circle)

	plt.text(0.15, 0.7, "Angle : " + str(angle) + " [deg]", va="center", ha="left", family='sans-serif', size=14)

	drawShelf("Salad", "plum", angle, False)
	drawShelf("Radish", "bisque", angle + 90, True)
	drawShelf("Lunar Soil 1", "greenyellow", angle + 180, False)
	drawShelf("Lunar Soil 2", "cornflowerblue", angle + 270, False)



	plt.axis('equal')
	plt.axis('off')
	plt.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	return imgFileName


makeWheelImg(180, True)

#patches = []
#patches.append(circle)
#collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=1)
#collection.set_array(np.array(colors))
#ax.add_collection(collection)
