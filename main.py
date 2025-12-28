import random, time


def create_deck(): 
    deck = [] 
    suits = ['H', 'D', 'C', 'S']
    graphical_cards = ['K', 'Q', 'J', 'A'] 

    #Add numerical cards
    for i in range(2, 11): 
        for j in suits: 
            deck.append((i, j))

    #Add graphical cards
    for i in graphical_cards: 
        for j in suits:
            if(i != 'A'):
                deck.append((10, j)) 
            else:
                deck.append(('A', j))
 
    return deck 

def shuffle_deck(deck): 
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
        return 1 
    
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
        if current_hand[0] < 11:
            current_hand[0] = 11 + current_hand[0]
            current_hand[1] = True 
            return current_hand
        else: 
            current_hand[0] = 1 + current_hand[0]
            current_hand[1] = False
            return current_hand
        
    current_hand[0] = current_hand[0] + dealt_card[0]

    if current_hand[0] > 21:
        if current_hand[1]:
            current_hand[0] = current_hand[0] - 10
            current_hand[1] = False
            return current_hand 
        else:
            return -1
        
    return current_hand
            

if __name__ == '__main__':

    deck_1 = create_deck()
    shuffled_deck_1 = shuffle_deck(deck_1)     

    #Inital Deal
    player_card_1 = shuffled_deck_1.pop() 
    dealer_card_1 = shuffled_deck_1.pop() 
    player_card_2 = shuffled_deck_1.pop() 
    dealer_card_2 = shuffled_deck_1.pop() 
    
    intial_hand = evaluate_inital_hand(player_card_1, player_card_2) 

    if(intial_hand != 1):
        print(f'Hand value: {intial_hand[0]}')  
        print(f'Useable Ace: {intial_hand[1]}')
    else:
        print('Winner Winner chicken Dinner') 

    print(player_card_1)
    print(player_card_2) 

    print('*' * 150)