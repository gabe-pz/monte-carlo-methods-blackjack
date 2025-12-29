from blackjack_logic_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck 
from random import randint 

def fixed_policy(state): 

    if(state[0] > 19):
        return 'S'
    else:
        return 'H'

def run_episode():
    states = [] 
    actions = [] 
    
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


    if(player_hand[0] == 21 and dealer_hand[0] == 21):  
        states.append((player_hand[0], dealer_up_card[0], player_hand[1])) 
        actions.append(' ')   
        return states, actions, 0
    
    if(player_hand[0] == 21):
        states.append((player_hand[0], dealer_up_card[0], player_hand[1])) 
        actions.append(' ')   
        return states, actions, 1
    
    if(dealer_hand[0] == 21):
        states.append((player_hand[0], dealer_up_card[0], player_hand[1])) 
        actions.append(' ')   
        return states, actions, -1
    
    #Always hit between 2-11 
    while player_hand[0] < 12:
        player_card_dealt = create_and_shuffle_deck()[0]  

        player_hand = evaluate_hand(player_hand, player_card_dealt) 
    
    #Note the inital playable state
    states.append((player_hand[0], dealer_up_card[0], player_hand[1])) 
    i = 0

    #Players Turn
    while True:
        policy_choice = fixed_policy(states[i])   

        #Policy choice for 12-21
        if(policy_choice == 'H'):
            player_card_dealt = create_and_shuffle_deck()[0]  

            player_hand = evaluate_hand(player_hand, player_card_dealt) 

            states.append((player_hand[0], dealer_up_card[0], player_hand[1]))   
            actions.append('H') 
            #Gone to next state
            i += 1
            if(player_hand[0] > 21): 
                player_goes_bust = True
                #Over 21 and states are only, 12-21 
                states.pop()
                break 

        else:
            actions.append('S')  
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
        return states, actions, -1
    if dealer_goes_bust:
        return states, actions, 1
    
    #Checking who is close to 21
    if player_hand[0] > dealer_hand[0]:
        return states, actions, 1
    elif player_hand[0] < dealer_hand[0]:
        return states, actions, -1
    else:
        return states, actions, 0 
def average_list(lst):
    sum = 0
    for element in lst:
        sum += element 
    return (sum/len(lst)) 

if __name__ == '__main__':
    state_space = [] 
    state_values = {}
    returns = {} 

    episodes = 1000

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
    for i in range(episodes): 
        states_ep, actions_ep, return_ep = run_episode()

        print(actions_ep)
        print(return_ep)
        print() 




