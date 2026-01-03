from blackjack_helper_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck, average_list
from random import randint 
from tqdm import tqdm 

def run_episode(policy: dict[tuple[int, int, bool], int]) -> tuple[list, int]:
    #Initalize things
    states_actions: list[tuple[tuple[int, int, bool], int]] = [] 
    player_goes_bust: bool = False
    dealer_goes_bust: bool = False
    state: tuple[int, int, bool] = (0, 0, False) 

    #Initial deal
    player_card_1: int = create_and_shuffle_deck()[0]
    dealer_down_card: int = create_and_shuffle_deck()[0]
    player_card_2: int = create_and_shuffle_deck()[0]
    dealer_up_card: int = create_and_shuffle_deck()[0]

    #Evaluating initial deal
    player_hand: tuple[int, bool] = evaluate_inital_hand(player_card_1, player_card_2) 
    dealer_hand: tuple[int, bool] = evaluate_inital_hand(dealer_down_card, dealer_up_card)
    
    #Checking if player or dealer gets BJ
    if(player_hand[0] == 21):
        return ([], -2)
    
    if(dealer_hand[0] == 21):
        return ([], -2)
    
    #Always hit between 2-11 
    while player_hand[0] < 12:
        player_card_dealt: int = create_and_shuffle_deck()[0]  

        player_hand = evaluate_hand(player_hand, player_card_dealt) 
    
    #Note the inital playable state
    state = (player_hand[0], dealer_up_card, player_hand[1])

    #Players Turn
    while True:
        #Policy choice for sum 12-21
        policy_choice: int = policy[state]

        if(policy_choice == 0):
            #Deal card
            player_card_dealt = create_and_shuffle_deck()[0] 

            #Evaluate hand
            player_hand = evaluate_hand(player_hand, player_card_dealt) 
            
            #Check if player goes bust
            if(player_hand[0] > 21): 
                #Note the state were in and action took that lead to busting
                states_actions.append((state, 0))
                player_goes_bust = True
                break
            
            #If not bust, then simply note the state now in and action took 
            states_actions.append((state, 0))

            #Update new state
            state = (player_hand[0], dealer_up_card, player_hand[1])

        else:
            #Note the state in when choosing to stand
            states_actions.append((state, 1))
            break 

    #Dealers Turn     
    if(not player_goes_bust):   
        while dealer_hand[0] < 17: 
            dealer_card_dealt: int = create_and_shuffle_deck()[0]

            dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 

            if(dealer_hand[0] > 21):
                dealer_goes_bust = True
                break 
        
    #Evaluate results
    if(player_goes_bust):
        return (states_actions, -1)
    if(dealer_goes_bust):
        return (states_actions, 1)
    
    #Checking who is close to 21
    if(player_hand[0] > dealer_hand[0]):
        return (states_actions, 1)
    elif (player_hand[0] < dealer_hand[0]):
        return (states_actions, -1)
    else:
        return (states_actions, 0) 

def state_value_function(policy, num_episodes) -> dict[tuple[int, int, bool], float]:
    state_space: list[tuple[int, int, bool]] = [] 
    
    state_values: dict[tuple[int, int, bool], float] = {}
    returns: dict[tuple[int, int, bool], list[int]] = {} 

    #Create the state space
    for usable_ace in [True, False]: 
        for p_sum in range(12, 22):
            for d_card in range(2, 11):
                if(d_card == 2):
                    state_space.append((p_sum, 1, usable_ace))
                    state_space.append((p_sum, d_card, usable_ace))
                else:
                    state_space.append((p_sum, d_card, usable_ace))
     
    #Initalize state value functions and creating empty list to store returns corresponding to each state
    for state in state_space:
        state_values[state] = randint(-1, 1) 
        returns[state] = [] 

    #Policy Evaulation
    for _ in tqdm(range(num_episodes)): 
        states_actions_ep, return_ep = run_episode(policy)
        
        if(return_ep == -2):
            continue

        for t in range(len(states_actions_ep))[::-1]: 
            if(states_actions_ep[t][0] not in states_actions_ep[:t]):
                returns[states_actions_ep[t][0]].append(return_ep) 
                state_values[states_actions_ep[t][0]] = average_list(returns[states_actions_ep[t][0]])  

    return state_values 