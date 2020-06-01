import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_specimen(specimen,test_data, master_width, master_height, offset=100):
    fig,ax = plt.subplots(1)
    ax.set_xlim(0, master_width + 2*offset)
    ax.set_ylim(0, master_width + 2*offset)
    rect = patches.Rectangle((offset,offset),master_width,master_height,linewidth=3,edgecolor='r',facecolor='none')
    ax.add_patch(rect)

    for key, value in specimen.decode().items():
        if not value["exist"]:
            continue

        matching_rect = test_data[key]
        x_pos = value['x']
        y_pos = value['y']
        w = matching_rect.width
        h = matching_rect.height

        if value['flip']:
            w = matching_rect.height
            h = matching_rect.width

        rect = patches.Rectangle((offset + x_pos,offset + y_pos),w,h,linewidth=2,edgecolor='b',facecolor='none')
        ax.add_patch(rect)


    plt.show()