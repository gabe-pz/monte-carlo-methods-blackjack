from blackjack_helper_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck, average_list
from random import randint 
from tqdm import tqdm

def run_episode(policy: dict[tuple[int, int, bool], int], inital_state_action: tuple[tuple[int, int, bool], int]) -> tuple[list, int]: 
    #Initalize things
    states_actions: list[tuple[tuple[int, int, bool], int]] = []   
    state: tuple[int, int, bool] = (0, 0, False)  
    
    player_goes_bust: bool = False
    dealer_goes_bust: bool = False

    player_card_dealt: int = 0 

    #Note the inital state and inital action    
    inital_state: tuple[int, int, bool] = inital_state_action[0] 
    inital_action: int = inital_state_action[1] 

    #Initial deal to dealer  
    dealer_down_card: int = create_and_shuffle_deck()[0]
    dealer_up_card: int = inital_state[1] 

    #Evaluating initial deal for dealers hand and setting players fixed inital hand
    player_hand: tuple[int, bool] = (inital_state[0], inital_state[2])

    dealer_hand: tuple[int, bool] = evaluate_inital_hand(dealer_down_card, dealer_up_card)
    
    #Checking if player or dealer gets a BJ
    if(player_hand[0] == 21):
        return ([], -2)
    
    if(dealer_hand[0] == 21):
        return ([], -2)
    
    #Taking the inital action from inital state
    if(inital_action == 0):
        #Deal card
        player_card_dealt = create_and_shuffle_deck()[0] 
    
        #Evaluate hand
        player_hand = evaluate_hand(player_hand, player_card_dealt) 
        
        #Check if player goes bust
        if(player_hand[0] > 21): 
            #Note the state were in and action took that lead to busting
            states_actions.append((inital_state, inital_action))
            player_goes_bust = True

        #If dont bust then simply note the new state and add 
        else:
            #If not bust, then simply note the state were in and action took  
            states_actions.append((inital_state, inital_action)) 

            #Update to state now 
            state = (player_hand[0], dealer_up_card, player_hand[1]) 
            

    else:
        #Note the state in when choosing to stand
        states_actions.append((inital_state, inital_action))
        state = inital_state 


    #Run players turn, only if inital state action caused player to not bust and didnt decide to stand
    if(not player_goes_bust and state != inital_state): 

        #Players Turn
        while True:
            #Policy choice for sum 12-21
            policy_choice = policy[state]

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
                states_actions.append(((player_hand[0], dealer_up_card, player_hand[1]), 1))
                break 

    #Dealers Turn     
    if(not player_goes_bust):   
        while dealer_hand[0] < 17: 
            dealer_card_dealt = create_and_shuffle_deck()[0]

            dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 

            if(dealer_hand[0] > 21):
                dealer_goes_bust = True
                break 
        
    #Evaluate results
    if player_goes_bust:
        return (states_actions, -1)
    if dealer_goes_bust:
        return (states_actions, 1)
    
    #Checking who is close to 21
    if player_hand[0] > dealer_hand[0]:
        return (states_actions, 1)
    elif player_hand[0] < dealer_hand[0]:
        return (states_actions, -1)
    else:
        return (states_actions, 0)

def optimal_policy(num_episodes: int) -> dict[tuple[int, int, bool], int]:
    #Initalize spaces
    state_space: list[tuple[int, int, bool]] = [] 
    action_space: list[int]= [0, 1]  # Hit is 0, Stick is 1
    state_action_space: list[tuple[tuple[int, int, bool], int]] = []  
    #Initalize dicts
    policy_dict: dict[tuple[int, int, bool], int] = {}    
    returns: dict[tuple[tuple[int, int, bool], int], list[int]] = {} 
    action_value: dict[tuple[tuple[int, int, bool], int], float] = {} 
    
    #Creating the state space
    for usable_ace in [True, False]: 
        for p_sum in range(12, 22):
            for d_card in range(2, 11):
                if(d_card == 2):
                    state_space.append((p_sum, 1, usable_ace))
                    state_space.append((p_sum, d_card, usable_ace))
                else:
                    state_space.append((p_sum, d_card, usable_ace))  
    #Creating all possible actions can take in each state
    for action in action_space:
        for state in state_space:
            state_action_space.append((state, action)) 


    #Create empty list of returns corresponding to each state action pair, as well as initalizing the action value function for each state action pair
    for state_action in state_action_space:
        returns[state_action] = []  
        action_value[state_action] = 0


    #Inital policy for GPI
    for state in state_space:
        if(state[0] > 17):
            policy_dict[state] = action_space[1]
        else: 
            policy_dict[state] = action_space[0] 


    #Monte carlo ES to estimate optimal policy 
    for _ in tqdm(range(num_episodes)):
        inital_state_action = state_action_space[randint(0, len(state_action_space)-1)]  
        (state_actions_ep, return_ep) = run_episode(policy_dict, inital_state_action) 
        
        if(return_ep == -2):
            continue
        
        for t in range(len(state_actions_ep))[::-1]: 
            if(state_actions_ep[t] not in state_actions_ep[:t]):  
                returns[state_actions_ep[t]].append(return_ep) 
                action_value[state_actions_ep[t]] = average_list(returns[state_actions_ep[t]])

                if(action_value[(state_actions_ep[t][0], action_space[0])]  > action_value[(state_actions_ep[t][0], action_space[1])]): 
                    policy_dict[state_actions_ep[t][0]] = action_space[0] 
                else:
                    policy_dict[state_actions_ep[t][0]] = action_space[1]   

    return policy_dict  
