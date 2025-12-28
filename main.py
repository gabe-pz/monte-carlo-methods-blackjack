import random, time


def create_and_shuffle_deck(): 
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
        if(current_hand[0] < 11):
            current_hand[0] = 11 + current_hand[0]
            current_hand[1] = True 
            return current_hand
        else: 
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
            
def player_policy(current_hand, dealer_up_card):
    pass


if __name__ == '__main__':
    player_goes_bust = False
    dealer_goes_bust = False

    inital_deck = create_and_shuffle_deck()

    #Inital Deal
    player_card_1 = inital_deck.pop() 
    dealer_down_card = inital_deck.pop() 
    player_card_2 = inital_deck.pop() 
    dealer_up_card = inital_deck.pop() 

    player_hand = evaluate_inital_hand(player_card_1, player_card_2) 
    dealer_hand = evaluate_inital_hand(dealer_down_card, dealer_up_card)

    #Check blackjack for player
    if(player_hand == 1):
        print('Winner winner chicken dinner') 

    #Check if dealer has blackjack
    if(dealer_hand == 1):
        print('Dealer has blackjack, you lose')
        
    #running game
    while True:
        print(f'Your hand is: {player_hand[0]}')
        print(f'Useable ace: {player_hand[1]}') 
        print(f'Dealer up card: {dealer_up_card[0]}')  

        user_choice = input('Hit or stick?: ')

        if(user_choice == 'H'):
            deck_dealing = create_and_shuffle_deck() 

            player_card_dealt = deck_dealing.pop() 

            player_hand = evaluate_hand(player_hand, player_card_dealt) 

            if(player_hand[0] > 21): 
                player_goes_bust = True
                break 

            #If didn't  bust reask if want to hit or stick 
            print()
            continue
        
        else: 
            print()
            if(dealer_hand[0] > 16): 
                print()
                print(f'Dealer hand is: {dealer_hand[0]}')
                print(f'Useable ace: {dealer_hand[1]}') 
                print('-' * 45) 
                break
            while True:
                print(f'Dealer hand is: {dealer_hand[0]}')
                print(f'Useable ace: {dealer_hand[1]}') 
                print('-' * 45) 

                deck_dealing = create_and_shuffle_deck()

                dealer_card_dealt = deck_dealing.pop() 

                dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 

                if(dealer_hand[0] > 21):
                    dealer_goes_bust = True
                    break 
                
                if(dealer_hand[0] > 16):
                    print(f'Dealer hand is: {dealer_hand[0]}')
                    print(f'Useable ace: {dealer_hand[1]}') 
                    print('-' * 45)  
                    break
            break 
    
    print('**********RESULTS**********')
    #Evaluate results
    if(player_goes_bust or player_hand[0] < dealer_hand[0] and dealer_goes_bust == False):
        print(f'Your hand is: {player_hand[0]}')
        print(f'Useable ace: {player_hand[1]}')
        print()
        print(f'Dealer hand is: {dealer_hand[0]}')
        print(f'Useable ace: {dealer_hand[1]}') 
        print('-' * 45)
        print('Results: You Lost')
    if(dealer_goes_bust or player_hand[0] > dealer_hand[0] and player_goes_bust == False):
        print(f'Your hand is: {player_hand[0]}')
        print(f'Useable ace: {player_hand[1]}')
        print()
        print(f'Dealer hand is: {dealer_hand[0]}')
        print(f'Useable ace: {dealer_hand[1]}') 
        print('-' * 45)
        print('Results: You Won')

    if(player_hand[0] == dealer_hand[0]):
        print(f'Your hand is: {player_hand[0]}')
        print(f'Useable ace: {player_hand[1]}')
        print()
        print(f'Dealer hand is: {dealer_hand[0]}')
        print(f'Useable ace: {dealer_hand[1]}') 
        print('-' * 45)
        print('Results: You Tied')
    