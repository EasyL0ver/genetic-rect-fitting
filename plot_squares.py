import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy


def plot_outcome(parent_rect, rectangles, offset=100):
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
        rect = patches.Rectangle((offset + x_pos,offset + y_pos),w,h,linewidth=2,edgecolor=numpy.random.rand(3,),facecolor='none')
        ax.add_patch(rect)

    plt.show()

