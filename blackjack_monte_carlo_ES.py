from blackjack_helper_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck, average_list
from random import randint 

#Inital policy using for GPI
def policy_0(state): 

    if(state[0] > 19):
        return 'S'
    else:
        return 'H'

def run_episode(policy, inital_state_action):
    #Initalize list to keep track of actions took in each state
    states_actions = [] 

    player_goes_bust = False
    dealer_goes_bust = False

    #Note the inital state and inital action
    inital_state = inital_state_action[0] 
    inital_action = inital_state_action[1] 

    #Initial deal to dealer 
    dealer_down_card = create_and_shuffle_deck()[0]
    dealer_up_card = inital_state[1] 

    #Evaluating initial deal for dealers hand and setting players fixed inital hand
    player_hand = [inital_state[0], inital_state[2]]
    dealer_hand = evaluate_inital_hand(dealer_down_card, dealer_up_card)
    
    #Checking if player or dealer gets BJ
    if(player_hand[0] == 21):
        return [], -2
    
    if(dealer_hand[0] == 21):
        return [], -2
    
    #Taking the inital action from inital state
    if(inital_action == 'H'):
        #Deal card
        player_card_dealt = create_and_shuffle_deck()[0] 

        #Evaluate hand
        player_hand = evaluate_hand(player_hand, player_card_dealt) 
        
        #Check if player goes bust
        if(player_hand[0] > 21): 
            #Note the state were in and action took that lead to busting
            states_actions.append([inital_state, inital_action])
            player_goes_bust = True

        #If dont bust then simply note the new state and add 
        else:
            #If not bust, then simply note the state were in and action took  
            states_actions.append([inital_state, inital_action]) 
            
            #Update to state now in
            state = (player_hand[0], dealer_up_card, player_hand[1])
            

    else:
        #Note the state in when choosing to stand
        states_actions.append([inital_state, inital_action])
        state = inital_state 

    #Run players turn, only if inital state action caused player to not bust and didnt decide to stand
    if(not player_goes_bust and state != inital_state): 
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
                state = (player_hand[0], dealer_up_card, player_hand[1])

            else:
                #Note the state in when choosing to stand
                states_actions.append([(player_hand[0], dealer_up_card, player_hand[1]), 'S'])
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

if __name__ == '__main__':
    #Initalize
    state_actions = []  
    state_space = [] 
    action_space = ['H', 'S'] 
    
    returns = {} 
    action_value = {}
    
    num_episodes = 100 

    #Create the state space
    for bool in [True, False]: 
        for i in range(12, 22):
            for j in range(2, 11):
                if(j == 2):
                    state_space.append((i, 'A', bool))
                    state_space.append((i, j, bool))
                else:
                    state_space.append((i, j, bool))  

    #Creating all possible state action pairs     
    for action in action_space:
        for state in state_space:
            state_actions.append((state, action)) 

    #Create empty list of returns corresponding to each state action as well as initalizing the action value function for each state action
    for state_action in state_actions:
        returns[state_action] = [] 
        action_value[state_action] = 0 
   
    #Monte carlo ES to estimate optimal policy 
    for episode in range(num_episodes):
        inital_state_action = state_actions[randint(0, 399)] 
        #Finish algo tmr, from here
