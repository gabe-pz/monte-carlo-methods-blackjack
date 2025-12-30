import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def get_z_grid(state_dict, useable_ace, X_grid, Y_grid):
    def lookup_val(d, p):
        dealer_key = 'A' if d == 1 else d
        return state_dict.get((p, dealer_key, useable_ace), 0)
    
    lookup = np.vectorize(lookup_val)
    return lookup(X_grid, Y_grid)

def create_plots(X, Y, Z_usable, Z_no_usable):
    fig = plt.figure(figsize=(16, 8))
    
    def setup_ax(pos, Z_data, title):
        ax = fig.add_subplot(1, 2, pos, projection='3d')

        #Plot surface
        surf = ax.plot_surface(X, Y, Z_data, cmap=cm.coolwarm, antialiased=False)
        
        #Set labels
        ax.set_title(title, fontsize=17)
        ax.set_xlabel('Dealer Showing')
        ax.set_ylabel('Player Sum')
        ax.set_zlabel('State Value')
        
        #Set ticks
        ax.set_xticks(range(1, 11))
        ax.set_xticklabels(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        ax.set_yticks(range(12, 22)) 

        
        return ax

    setup_ax(1, Z_usable, 'Value Function (Usable Ace)')
    setup_ax(2, Z_no_usable, 'Value Function (No Usable Ace)')

    fig.subplots_adjust(wspace=0.45, top=0.85)     
    plt.show()

def plot(state_value_function):
    dealer_showing = np.arange(1, 11)  
    player_sum = np.arange(12, 22)     

    X, Y = np.meshgrid(dealer_showing, player_sum)

    Z_usable = get_z_grid(state_value_function, True, X, Y)
    Z_no_usable = get_z_grid(state_value_function, False, X, Y) 

    create_plots(X, Y, Z_usable, Z_no_usable) 