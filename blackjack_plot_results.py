from blackjack_monte_carlo_ES import optimal_policy 
from blackjack_monte_carlo_prediction import state_value_function 
from blackjack_plotting_functions import plot_policy, plot_state_value


def main() -> None:
    num_episodes: int = 5_000_000

    #Create optimum policy and then state value function for that policy
    optimum_policy: dict[tuple[int, int, bool], int] = optimal_policy(num_episodes)
    optimum_state_value: dict[tuple[int, int, bool], float] = state_value_function(optimum_policy, num_episodes)

    
        
    #plot em
    plot_policy(optimum_policy) 
    plot_state_value(optimum_state_value)

if __name__ == '__main__':
    main()
    