from blackjack_monte_carlo_ES import optimal_policy 
from blackjack_monte_carlo_prediction import state_value_function 
from blackjack_plotting_functions import plot_policy, plot_state_value


def main():
    num_episodes = 1000000

    #Create optimum policy and then state value function for that policy
    optimum_policy = optimal_policy(num_episodes)
    optimum_state_value = state_value_function(optimum_policy, num_episodes)
    
    #plot em
    plot_policy(optimum_policy) 
    plot_state_value(optimum_state_value)

if __name__ == '__main__':
    main() 
    