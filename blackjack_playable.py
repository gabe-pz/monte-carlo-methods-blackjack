from blackjack_logic_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck 

def run_blackjack():
    player_goes_bust = False
    dealer_goes_bust = False
    
    #Initial deal
    inital_deck = create_and_shuffle_deck() 
    player_card_1 = inital_deck.pop()
    dealer_down_card = inital_deck.pop()
    player_card_2 = inital_deck.pop()
    dealer_up_card = inital_deck.pop()

    player_hand = evaluate_inital_hand(player_card_1, player_card_2) 
    dealer_hand = evaluate_inital_hand(dealer_down_card, dealer_up_card)

    print()
    print('********** BLACKJACK **********') 
    print()

    if(player_hand[0] == 21 and dealer_hand[0] == 21): 
        print('Both have 21 - Push!')
        return
    if(player_hand[0] == 21):
        print('BLACKJACK! You win!')
        return
    if(dealer_hand[0] == 21):
        print('Dealer has Blackjack. You lose, womp womp')
        return

    print(f'Dealer shows: {dealer_up_card[0]}')
    print()

    while True:
        print(f'Your hand: {player_hand[0]}', end='')
        if player_hand[1]:
            print(' (useable ace)', end='')
        print()
        
        user_choice = input('Hit or Stand? (H/S): ').upper()
        print() 
        
        if(user_choice == 'H'):
            player_card_dealt = create_and_shuffle_deck()[0]  
            player_hand = evaluate_hand(player_hand, player_card_dealt) 
            print(f'You drew: {player_card_dealt[0]}')
            print() 
            if(player_hand[0] > 21): 
                player_goes_bust = True
                break 
        else:
            break 

    if(not player_goes_bust):
        print('*****Dealers Turn*****')
        print()
        print(f'Dealer has: {dealer_hand[0]}', end='')
        if dealer_hand[1]:
            print(' (useable ace)', end='')
        print()
        print() 
        
        while dealer_hand[0] < 17: 
            dealer_card_dealt = create_and_shuffle_deck()[0]
            dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 
            print(f'Dealer drew: {dealer_card_dealt[0]} -> now has {dealer_hand[0]}')
            if(dealer_hand[0] > 21):
                dealer_goes_bust = True
                break 
        print()

    print('**********RESULTS**********')
    print(f'Your hand: {player_hand[0]}')
    print(f'Dealer hand: {dealer_hand[0]}')
    print()
    
    if player_goes_bust:
        print('You busted. You lose.')
    elif dealer_goes_bust:
        print('Dealer busted. You win!')
    elif player_hand[0] > dealer_hand[0]:
        print('You win!')
    elif player_hand[0] < dealer_hand[0]:
        print('You lose.')
    else:
        print('Push.')

if __name__ == '__main__':
    print()
    print('Welcome to Blackjack!')
    
    user_choice = 'y'
    while user_choice == 'y':
        run_blackjack() 
        print() 
        user_choice = input('Play again? (y/n): ').lower()
        print()
    