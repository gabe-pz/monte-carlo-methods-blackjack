import random


def create_and_shuffle_deck(): 
    deck = [] 
    suits = ['H', 'D', 'C', 'S']

    #Creating deck
    for i in range(2, 15): 
        for j in suits: 
            #Adding Numerical cards
            if(i < 11):
                deck.append((i, j))
            #Adding the face cards
            elif(i < 14): 
                deck.append((10, j))
            #Adding the aces
            else:
                deck.append(('A', j)) 

    #Shuffling deck 
    for i in range(len(deck))[::-1]:
        j = random.randint(0, i) 

        temp_card = deck[i] 
        deck[i] = deck[j] 
        deck[j] = temp_card
    
    return deck 


def evaluate_inital_hand(card1, card2):
    useable_ace = False

    #Checking blackjack
    if((card1[0] == 'A' and card2[0] == 10) or (card1[0] == 10 and card2[0] == 'A')): 
        return [21, useable_ace] 
    
    #Check if have a usable ace
    if(card1[0] == 'A' or card2[0] == 'A'):
        useable_ace = True

        if(card1[0] == 'A' and card2[0] != 'A'):
            return [11 + card2[0], useable_ace]
        elif(card1[0] != 'A' and card2[0] == 'A'): 
            return [card1[0] + 11, useable_ace]
        else:
            return [12, useable_ace] 

    return [card1[0] + card2[0], useable_ace]


def evaluate_hand(current_hand, dealt_card): 
    
    if(dealt_card[0] == 'A'):
        if(current_hand[0] < 11):
            current_hand[0] = 11 + current_hand[0]
            current_hand[1] = True 
            return current_hand
        else:
            
            #Fix useable ace bug, that is if have card and useable ace and get another ace and then get card that would bust, set both aces to 1 and then take sum there then add on the card got for new sum
            if(current_hand[1]):
                current_hand[0] = 1 + current_hand[0]
                current_hand[1] = True
                return current_hand            

            current_hand[0] = 1 + current_hand[0]
            current_hand[1] = False
            return current_hand
        
    current_hand[0] = current_hand[0] + dealt_card[0]

    if(current_hand[0] > 21):
        if(current_hand[1]):
            current_hand[0] = current_hand[0] - 10
            current_hand[1] = False
            return current_hand 
        
        return current_hand
        
    return current_hand

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

        if(policy_choice == 'H'):
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
        
        
    if player_goes_bust:
        return -1

    if dealer_goes_bust:
        return 1

    if player_hand[0] > dealer_hand[0]:
        return 1
    elif player_hand[0] < dealer_hand[0]:
        return -1
    else:
        return 0
    
if __name__ == '__main__':
    i = 0
    check_win = 0
    games_played = 100000

