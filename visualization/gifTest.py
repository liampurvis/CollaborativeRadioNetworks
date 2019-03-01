import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import matplotlib.animation as animation

pause = False

def gif(Id, pos, freq):
    fig, ax = plt.subplots(1,2)
    fig.set_tight_layout(True)
    
    step = len(pos[Id[0]])

    def onClick(event):
        global pause
        pause ^= True
        
    def frame():
        t_max = step 
        dt = 1
        t = 0
        while t < t_max:
            if not pause:
                t = t + dt
            yield t

    def update(i):
        
        label = 'timestep {0}'.format(i)
        print(label)

        # Update the pos
        for id in Id:
            (tx, ty, rx, ry) = pos[id][i]
            ax[0].patches[0].set_xy((min(tx, rx),min(ty, ry)))
            ax[0].patches[0].set_width(abs(tx-rx))
            ax[0].patches[0].set_height(abs(ty-ry))
        ax[0].set_xlabel(label)
        return ax

    
    ax[0].set_xlim(0,20)
    ax[0].set_ylim(0,20)
    ax[1].set_xlim(0,20)
    ax[1].set_ylim(0,20)

    # Query the figure's on-screen size and DPI. Note that when saving the figure to
    # a file, we need to provide a DPI for that separately.
    print('fig size: {0} DPI, size in inches {1}'.format(
        fig.get_dpi(), fig.get_size_inches()))

    # Init the position patches
    for id in Id:
        (tx, ty, rx, ry) = pos[id][0]
        rect = plt.Rectangle((min(tx, rx),min(ty, ry)), abs(tx-rx), abs(ty-ry), color='r', alpha=0.3)
        ax[0].add_patch(rect)

    # FuncAnimation will call the 'update' function for each frame
    fig.canvas.mpl_connect('button_press_event', onClick)
    anim = FuncAnimation(fig, update, frame(), blit=False, interval=500, repeat=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('map.gif', dpi=80, writer='imagemagick')
    else:
        # plt.show() will just loop the animation forever.
        plt.show()

