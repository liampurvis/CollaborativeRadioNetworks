"""
    Created on Thu Feb 28 2019
    
    @author: Sean
    
    Generate gif for position and frequency changing with pause function
    
    """
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import random

pause = False

def gif(Id, pos, freq):
    fig, ax = plt.subplots(1,2)
    fig.set_tight_layout(True)
    
    step = len(pos[Id[0]])
    print (step)

    def onClick(event):
        global pause
        pause ^= True
        
    def frame():
        t_max = step-1
        dt = 1
        t = 0
        while t < t_max:
            if not pause:
                t = t + dt
            yield t

    def update(i):
        
        label = 'timestep {0}'.format(i)
        print(label)

        for j in range(len(Id)):
            (tx, ty, rx, ry) = pos[Id[j]][i]
            ax[0].patches[j*3].center = rx, ry
            ax[0].patches[j*3+1].center = tx, ty
            ax[0].patches[j*3+2].set_xy((min(tx, rx),min(ty, ry)))
            ax[0].patches[j*3+2].set_width(abs(tx-rx))
            ax[0].patches[j*3+2].set_height(abs(ty-ry))
            
            (cf, bw) = freq[Id[j]][i]
            ax[1].patches[j].set_xy((j, cf-(bw/2)))
            ax[1].patches[j].set_height(bw)
        
        ax[0].set_xlabel(label)
        ax[1].set_xlabel(label)

        return ax

    
    ax[0].set_xlim(-1,5)
    ax[0].set_ylim(-1,5)
    ax[1].set_xlim(0,len(Id))
    ax[1].set_ylim(500,2500)

    # Query the figure's on-screen size and DPI. Note that when saving the figure to
    # a file, we need to provide a DPI for that separately.
    print('fig size: {0} DPI, size in inches {1}'.format(
        fig.get_dpi(), fig.get_size_inches()))

    # Init color and legend
    
    # generate same amount of colors as the player number
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(Id))]
    legs = []
    for i in range(len(Id)):
        leg = mpatches.Patch(alpha=0.3, color=colors[i], label='Player ' + str(Id[i]))
        legs.append(leg)
    plt.legend(handles=legs)


    # Init the position patches
    for i in range(len(Id)):
        id = Id[i]
        # position: vertice and range
        (tx, ty, rx, ry) = pos[id][0]
        receiver = plt.Circle((rx, ry), 0.08, color='b', alpha=0.7)
        transmitter = plt.Circle((tx, ty), 0.08, color='y', alpha=0.7)
        rect = plt.Rectangle((min(tx, rx),min(ty, ry)), abs(tx-rx), abs(ty-ry), color=colors[i], alpha=0.3)
        ax[0].add_patch(receiver)
        ax[0].add_patch(transmitter)
        ax[0].add_patch(rect)
        
        # freq
        (cf, bw) = freq[id][0]
        rect = plt.Rectangle((i, cf-(bw/2)), abs(0.5), abs(bw), color=colors[i], alpha=0.3)
        ax[1].add_patch(rect)
    


    # FuncAnimation will call the 'update' function for each frame
    fig.canvas.mpl_connect('button_press_event', onClick)
    anim = FuncAnimation(fig, update, frame(), blit=False, interval=10)
    plt.show()

    return
