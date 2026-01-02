from blackjack_helper_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck 

def run_blackjack() -> int:
    player_goes_bust = False
    dealer_goes_bust = False
    
    #Initial deal
    player_card_1 = create_and_shuffle_deck()[0]
    dealer_down_card = create_and_shuffle_deck()[0]
    player_card_2 = create_and_shuffle_deck()[0]
    dealer_up_card = create_and_shuffle_deck()[0]

    player_hand = evaluate_inital_hand(player_card_1, player_card_2) 
    dealer_hand = evaluate_inital_hand(dealer_down_card, dealer_up_card)

    print()
    print('********** BLACKJACK **********') 
    print()

    if(player_hand[0] == 21):
        print('BLACKJACK! You win!')
        return 1
    if(dealer_hand[0] == 21):
        print('Dealer has Blackjack. You lose, womp womp')
        return -1

    print(f'Dealer shows: {dealer_up_card}') 
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
            print(f'You drew: {player_card_dealt}')
            print() 
            if(player_hand[0] > 21): 
                player_goes_bust = True
                break 
        else:
            break 

    if(not player_goes_bust):
        print('*****Dealers Turn*****')
        print()
        print(f'Dealer has: {dealer_hand}', end='')
        if dealer_hand[1]:
            print(' (useable ace)', end='')
        print()
        print() 
        
        while dealer_hand[0] < 17: 
            dealer_card_dealt = create_and_shuffle_deck()[0]
            dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 
            print(f'Dealer drew: {dealer_card_dealt} -> now has {dealer_hand[0]}')
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
        return -1 
    elif dealer_goes_bust:
        print('Dealer busted. You win!')
        return 1
    elif player_hand[0] > dealer_hand[0]:
        print('You win!')
        return 1
    elif player_hand[0] < dealer_hand[0]:
        print('You lose.')
        return -1
    else:
        print('Push.')
        return 0

def main() -> None: 
    print('Welcome to Blackjack!')
    wins: int = 0
    losses: int = 0 
    pushes: int = 0

    user_choice = 'y'
    while user_choice == 'y':
        result = run_blackjack() 
        if(result == 1):
            wins += 1 
        elif(result == -1):
            losses += 1
        else:
            pushes += 1
        print() 
        user_choice = input('Play again? (y/n): ').lower()
        print()
    print(f'Your Stats: Wins = {wins}, Losses = {losses}, Pushes = {pushes}') 

if __name__ == '__main__':
    main()
    