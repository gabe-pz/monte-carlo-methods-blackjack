import matplotlib.pyplot as plt # type: ignore
from matplotlib import cm
import numpy as np 
from matplotlib.colors import ListedColormap # type: ignore
from matplotlib.colors import LightSource 

def get_z_grid(state_dict, useable_ace, X_grid, Y_grid):
    def lookup_val(d, p):
        dealer_key = 1 if d == 1 else d
        return state_dict.get((p, dealer_key, useable_ace), 0)
    
    lookup = np.vectorize(lookup_val)
    return lookup(X_grid, Y_grid)

def create_plots(X, Y, Z_usable, Z_no_usable):
    fig = plt.figure(figsize=(16, 8))
    ls = LightSource(azdeg=315, altdeg=45) 
    
    def setup_ax(pos, Z_data, title):
        ax = fig.add_subplot(1, 2, pos, projection='3d')

        #Plot surface
        rgb = ls.shade(Z_data, cmap=cm.coolwarm, vert_exag=0.1, blend_mode='soft') # type: ignore
        surf = ax.plot_surface(X, Y, Z_data, facecolors=rgb, 
                            antialiased=True, shade=False)
        
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


def plot_state_value(state_value_function):
    dealer_showing = np.arange(1, 11)  
    player_sum = np.arange(12, 22)     

    X, Y = np.meshgrid(dealer_showing, player_sum)

    Z_usable = get_z_grid(state_value_function, True, X, Y)
    Z_no_usable = get_z_grid(state_value_function, False, X, Y) 

    create_plots(X, Y, Z_usable, Z_no_usable)  

#Plotting policy
def plot_policy(policy_dict) -> None:
    dealer_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    player_sums = np.arange(12, 22)
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    titles = ['Usable Ace', 'No Usable Ace']
    is_usable_ace = [True, False]
    
    #colors, Red for HIT , Blue for STICK 
    cmap = ListedColormap(['#ff9999', '#9999ff']) 

    for idx, (ax, ace) in enumerate(zip(axes, is_usable_ace)):
        #Create a grid for the heatmap
        grid = np.zeros((len(player_sums), len(dealer_cards)))
        
        for i, p in enumerate(player_sums):
            for j, d in enumerate(dealer_cards):
                action = policy_dict.get((p, d, ace))
                grid[i, j] = 1 if action == 1 else 0
        
        #Plot heatmap
        im = ax.imshow(grid, origin='lower', cmap=cmap, aspect='auto', extent=[-0.5, 9.5, 11.5, 21.5])
        
        #Formatting
        ax.set_title(titles[idx], fontsize=12, pad=10)

        ax.set_xticks(range(len(dealer_cards)))
        ax.set_xticklabels(['A', 2, 3, 4, 5, 6, 7, 8, 9, 10])

        ax.set_yticks(player_sums)
        
        ax.set_xlabel('Dealer Showing')
        if idx == 0: ax.set_ylabel('Player Sum')
        
        ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
        ax.set_yticks(np.arange(11.5, 22, 1), minor=True)
        
        ax.grid(which='minor', color='white', linestyle='-', linewidth=1)
        ax.tick_params(which="minor", bottom=False, left=False)
    
    plt.tight_layout()
    plt.show()                 