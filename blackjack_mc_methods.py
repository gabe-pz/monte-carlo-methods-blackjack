from blackjack_logic_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck 
from random import randint 

def fixed_policy(player_hand, dealer_up_card): 

    if(player_hand[0] > 19):
        return 'S'
    else:
        return 'H'

def run_episode():
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
        return 0
    
    if(player_hand[0] == 21):
        return 1 
    
    if(dealer_hand[0] == 21):
        return -1
        
    #Players Turn
    while True:
        policy_choice = fixed_policy(player_hand, dealer_up_card[0])  
        
        #Always hit between 2-11
        if(player_hand[0] < 12):
            player_card_dealt = create_and_shuffle_deck()[0]  

            player_hand = evaluate_hand(player_hand, player_card_dealt) 

            if(player_hand[0] > 21): 
                player_goes_bust = True
                break 
        #Policy choice for 12-21
        elif(policy_choice == 'H'):
            player_card_dealt = create_and_shuffle_deck()[0]  

            player_hand = evaluate_hand(player_hand, player_card_dealt) 

            if(player_hand[0] > 21): 
                player_goes_bust = True
                break 

        else:
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
        return -1
    if dealer_goes_bust:
        return 1 
    
    #Checking who is close to 21
    if player_hand[0] > dealer_hand[0]:
        return 1
    elif player_hand[0] < dealer_hand[0]:
        return -1
    else:
        return 0
    
def state_value_function(state):
    return 

def first_visit_mc_prediction():
    state_value_functions = [] 
    

if __name__ == '__main__':

    state_space = [] 

    for bool in [True, False]: 
        for i in range(12, 22):
            for j in range(2, 11):
                if(j == 2):
                    state_space.append((i, 'A', bool))
                    state_space.append((i, j, bool))
                else:
                    state_space.append((i, j, bool))
        

    for state in state_space:
        print(state) 
    print(len(state_space)) 
     