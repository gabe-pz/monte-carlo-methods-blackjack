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

def plot_state_value(state_value_function):
    dealer_showing = np.arange(1, 11)  
    player_sum = np.arange(12, 22)     

    X, Y = np.meshgrid(dealer_showing, player_sum)

    Z_usable = get_z_grid(state_value_function, True, X, Y)
    Z_no_usable = get_z_grid(state_value_function, False, X, Y) 

    create_plots(X, Y, Z_usable, Z_no_usable)  

def plot_policy(policy_dict):
    dealer_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
    player_sums = np.arange(11, 22)
    
    fig, axes = plt.subplots(2, 1, figsize=(5, 7))
    titles = ['Usable\nace', 'No\nusable\nace']
    is_usable_ace = [True, False]
    
    label_coords = [((4.5, 20), (4.5, 13)),((5.0, 20), (7.5, 13))] 

    fig.suptitle(r'$\pi_*$', fontsize=16, y=0.98)
    
    for idx, (ax, ace) in enumerate(zip(axes, is_usable_ace)):
        boundary = []
        for d in dealer_cards:
            found_stick = False
            for p in player_sums:
                if policy_dict.get((p, d, ace)) == 'S':
                    boundary.append(p)
                    found_stick = True
                    break
            if not found_stick:
                boundary.append(22)
        
        x_points = np.arange(len(dealer_cards) + 1) - 0.5
        boundary_extended = boundary + [boundary[-1]]
        ax.step(x_points, boundary_extended, where='post', color='black', linewidth=1.5)
        
        ax.text(-2.5, 16, titles[idx], fontsize=10, ha='center', va='center', multialignment='center')
        ax.set_xticks(np.arange(len(dealer_cards)))
        ax.set_xticklabels(dealer_cards)
        ax.set_yticks(range(11, 22))
        ax.set_ylim(10.5, 21.5)
        ax.set_xlim(-0.5, 9.5)
        
        (s_x, s_y), (h_x, h_y) = label_coords[idx]
        ax.text(s_x,  s_y, 'STICK', fontsize=11, ha='center', va='center')
        ax.text(h_x, h_y, 'HIT', fontsize=11, ha='center', va='center')
    
    fig.text(0.98, 0.5, 'Player sum', fontsize=10, rotation=270, va='center')
    axes[1].set_xlabel('Dealer showing')
    plt.subplots_adjust(left=0.2, right=0.85, hspace=0.3, top=0.92)
    plt.show() 

