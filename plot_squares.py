import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy
from datetime import datetime


def print_coverage_data(parent_rect, rectangles):
    covered_area = sum(map(lambda x: x.area, rectangles))

    print(f"Covered: {covered_area} out of {parent_rect.area}")
    print(f"Cover percentage is: {covered_area/parent_rect.area * 100} %" )


def plot_outcome(parent_rect, rectangles, save_path, offset=100, show=True):
    fig,ax = plt.subplots(1)
    ax.set_xlim(0, parent_rect.width + 2*offset)
    ax.set_ylim(0, parent_rect.height + 2*offset)
    rect = patches.Rectangle((offset,offset),parent_rect.width,parent_rect.height,linewidth=3,edgecolor='r',facecolor='none')
    ax.add_patch(rect)

    for rectangle in rectangles:
        x_pos = rectangle.x_pos
        y_pos = rectangle.y_pos
        w = rectangle.width
        h = rectangle.height
        random_color = numpy.random.rand(3,)
        rect = patches.Rectangle((offset + x_pos,offset + y_pos),w,h,linewidth=0,edgecolor=random_color,facecolor=random_color)
        ax.add_patch(rect)

    if show:
        plt.show()

    now = str(datetime.now().strftime("%d%m%Y%H%M"))
    save_path = f"{save_path}{now}.png"

    plt.savefig(save_path)

def plot_convergence(conv_vec, mean_conv_vec):
    fig,ax = plt.subplots(1)
    plt.plot(conv_vec)
    plt.plot(mean_conv_vec)

    plt.show()

