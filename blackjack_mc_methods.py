from blackjack_logic_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck
from blackjack_plotting_results import plot 
from random import randint 


def average_list(lst):
    sum = 0
    for element in lst:
        sum += element 
    return sum/len(lst)

def policy_0(state): 

    if(state[0] > 16):
        return 'S'
    else:
        return 'H'

def run_episode(policy):
    states_actions = [] 
    player_goes_bust = False
    dealer_goes_bust = False
        
    #Initial deal
    player_card_1 = create_and_shuffle_deck()[0]
    dealer_down_card = create_and_shuffle_deck()[0]
    player_card_2 = create_and_shuffle_deck()[0]
    dealer_up_card = create_and_shuffle_deck()[0]

    #Evaluating initial deal
    player_hand = evaluate_inital_hand(player_card_1, player_card_2) 
    dealer_hand = evaluate_inital_hand(dealer_down_card, dealer_up_card)
    
    #Checking if dealer, player, or both get bj
    if(player_hand[0] == 21 and dealer_hand[0] == 21):  
        return [], -2
    
    if(player_hand[0] == 21):
        return [], -2
    
    if(dealer_hand[0] == 21):
        return [], -2
    
    #Always hit between 2-11 
    while player_hand[0] < 12:
        player_card_dealt = create_and_shuffle_deck()[0]  

        player_hand = evaluate_hand(player_hand, player_card_dealt) 
    
    #Note the inital playable state
    state = (player_hand[0], dealer_up_card[0], player_hand[1])

    #Players Turn
    while True:
        #Policy choice for sum 12-21
        policy_choice = policy(state) 

        if(policy_choice == 'H'):
            #Deal card
            player_card_dealt = create_and_shuffle_deck()[0] 

            #Evaluate hand
            player_hand = evaluate_hand(player_hand, player_card_dealt) 
            
            #Check if player goes bust
            if(player_hand[0] > 21): 
                #Note the state were in and action took that lead to busting
                states_actions.append([state, 'H'])
                player_goes_bust = True
                break
            
            #If not bust, then simply note the state now in and action took 
            states_actions.append([state, 'H'])

            #Update new state
            state = (player_hand[0], dealer_up_card[0], player_hand[1])

        else:
            #Note the state in when choosing to stand
            states_actions.append([(player_hand[0], dealer_up_card[0], player_hand[1]), 'S'])
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
        return states_actions, -1
    if dealer_goes_bust:
        return states_actions, 1
    
    #Checking who is close to 21
    if player_hand[0] > dealer_hand[0]:
        return states_actions, 1
    elif player_hand[0] < dealer_hand[0]:
        return states_actions, -1
    else:
        return states_actions, 0 

def state_value_function(policy):
    num_episodes = 100000

    state_space = [] 
    state_values = {}
    returns = {} 
    
    #Create the state space
    for bool in [True, False]: 
        for i in range(12, 22):
            for j in range(2, 11):
                if(j == 2):
                    state_space.append((i, 'A', bool))
                    state_space.append((i, j, bool))
                else:
                    state_space.append((i, j, bool))
    
    #Initalize state value functions and creating empty list to store returns corresponding to each state
    for state in state_space:
        state_values[state] = randint(-1, 1) 
        returns[state] = [] 

    #Policy Evaulation
    for i in range(num_episodes): 
        states_actions_ep, return_ep = run_episode(policy)
        count = 1                       
        
        if(return_ep == -2):
            continue
        
        for t in range(len(states_actions_ep))[::-1]: 
            if(not(states_actions_ep[t][0] in states_actions_ep[:-count])):
                returns[states_actions_ep[t][0]].append(return_ep) 
                state_values[states_actions_ep[t][0]] = average_list(returns[states_actions_ep[t][0]]) 
                count += 1      
    
    return state_values 

if __name__ == '__main__':
    state_value = state_value_function(policy_0) 

    plot(state_value) 