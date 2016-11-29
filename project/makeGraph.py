import matplotlib.pyplot as plt
import numpy as np

LNG_MAX = -87.524529378
LNG_MIN = -91.6865656847
LAT_MAX = 42.02291033
LAT_MIN = 36.619446395


def plot():
    with open('hpc/allPositions.txt') as f:
        points = f

        #axis = plt.gca()
        #axis.set_xlim([LNG_MIN, LNG_MAX])
        #axis.set_ylim([LAT_MIN, LAT_MAX])

        x_points = []
        y_points = []
        for point in points:
            if 'Execution time:' not in point:
                point = point.split()
                if float(point[0]) > -91:
                    x_points.append(point[0])
                    y_points.append(point[1])
        x = np.array(x_points, dtype='float32')
        y = np.array(y_points, dtype='float32')

        plt.scatter(x, y)
        plt.grid(True)
        plt.plot()
        plt.show()

    '''x = np.random.randn(8873)
    y = np.random.randn(8873)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()'''

if __name__ == '__main__':
    plot()
