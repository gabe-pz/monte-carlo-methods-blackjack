import random 

def average_list(lst):
    sum = 0
    for element in lst:
        sum += element 
    return sum/len(lst)

def create_and_shuffle_deck(): 
    deck = [] 

    #Creating deck
    for i in range(2, 15): 
        for j in range(4): 
            #Adding Numerical cards
            if(i < 11):
                deck.append(i)
            #Adding the face cards
            elif(i < 14): 
                deck.append(10)
            #Adding the aces
            else:
                deck.append('A') 

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
    if((card1 == 'A' and card2 == 10) or (card1 == 10 and card2 == 'A')): 
        return [21, useable_ace] 
    
    #Check if have a usable ace
    if(card1 == 'A' or card2 == 'A'):
        useable_ace = True

        if(card1 == 'A' and card2 != 'A'):
            return [11 + card2, useable_ace]
        elif(card1 != 'A' and card2 == 'A'): 
            return [card1 + 11, useable_ace]
        else:
            return [12, useable_ace] 

    return [card1 + card2, useable_ace]


def evaluate_hand(current_hand, dealt_card): 
    
    if(dealt_card == 'A'): 

        if(current_hand[0] < 11):
            current_hand[0] = 11 + current_hand[0]
            current_hand[1] = True 
            return current_hand 

        current_hand[0] = 1 + current_hand[0]
        return current_hand
                
    new_sum = current_hand[0] + dealt_card

    if(new_sum > 21):
        if(current_hand[1]):
            current_hand[0] = (current_hand[0] - 10) + dealt_card
            current_hand[1] = False
            return current_hand 
        
        current_hand[0] = new_sum
        return current_hand
    
    current_hand[0] = new_sum
    return current_hand