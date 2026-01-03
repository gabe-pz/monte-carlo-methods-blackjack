import random 

def average_list(lst: list[int]) -> float: 
    sum = 0
    for element in lst:
        sum += element 
    return sum/len(lst)

def create_and_shuffle_deck() -> list[int]:  
    deck: list[int] = [] 
    
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
                deck.append(1) 

    #Shuffling deck 
    for i in range(len(deck))[::-1]:
        j = random.randint(0, i) 

        temp_card = deck[i] 
        deck[i] = deck[j] 
        deck[j] = temp_card
    
    return deck 

def evaluate_inital_hand(card1: int, card2: int) -> tuple[int, bool]:
    useable_ace: bool = False

    #Checking blackjack
    if((card1 == 1 and card2 == 10) or (card1 == 10 and card2 == 1)): 
        return (21, useable_ace)
    
    #Check if have a usable ace
    if(card1 == 1 or card2 == 1):
        useable_ace = True

        if(card1 == 1 and card2 != 1):
            return (11 + card2, useable_ace)
        elif(card1 != 1 and card2 == 1): 
            return (card1 + 11, useable_ace)
        else:
            return (12, useable_ace) 

    return (card1 + card2, useable_ace)


def evaluate_hand(current_hand: tuple[int, bool], dealt_card: int) -> tuple[int, bool]: 

    if(dealt_card == 1): 
        #If can use ace, then use it
        if(current_hand[0] < 11):
            return (11 + current_hand[0], True)
        
        #If cant use ace, then count it as 1
        return (current_hand[0] + dealt_card, current_hand[1])
                    
    if(current_hand[0] + dealt_card > 21):
        if(current_hand[1]):
            return ((current_hand[0] - 10) + dealt_card, False)
        
        return (current_hand[0] + dealt_card, current_hand[1]) 
    
    return (current_hand[0] + dealt_card, current_hand[1]) 
