import random 

#Logic functions for evaluating hands and creating deck

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

        current_hand[0] = 1 + current_hand[0]
        return current_hand
                
    new_sum = current_hand[0] + dealt_card[0]

    if(new_sum > 21):
        if(current_hand[1]):
            current_hand[0] = (current_hand[0] - 10) + dealt_card[0]
            current_hand[1] = False
            return current_hand 
        
        current_hand[0] = new_sum
        return current_hand
    
    current_hand[0] = new_sum
    return current_hand
