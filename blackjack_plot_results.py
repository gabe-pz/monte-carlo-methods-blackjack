from blackjack_monte_carlo_ES import optimal_policy 
from blackjack_monte_carlo_prediction import state_value_function 
from blackjack_plotting_functions import plot_policy, plot_state_value

if __name__ == '__main__':
    num_episodes = 1000000

    optimum_policy = optimal_policy(num_episodes)
    
    #Plot them 
    plot_policy(optimum_policy) 
    