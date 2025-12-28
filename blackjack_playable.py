from blackjack_logic_functions import evaluate_hand, evaluate_inital_hand, create_and_shuffle_deck 

#Ability to run and play the game as a player
def run_blackjack():
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
        print('You and the dealer both have blackjack, push')
    
    if(player_hand[0] == 21):
        print('BLACKJACK!')
    
    if(dealer_hand[0] == 21):
        print('Dealer has blackjack')
        
    #Players Turn
    while True:
        print(f'Your hand is: {player_hand[0]}')
        print(f'Useable Ace: {player_hand[1]}') 
        user_choice = input('Hit or Stick?(H/S)') 
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
        print('Ok Dealers turn')

    #Dealers Turn     
    if(not player_goes_bust):
        print(f'Dealer hand is: {dealer_hand[0]}')
        print(f'Useable Ace: {dealer_hand[1]}') 
        print() 

        while dealer_hand[0] < 17: 
            dealer_card_dealt = create_and_shuffle_deck()[0]

            dealer_hand = evaluate_hand(dealer_hand, dealer_card_dealt) 
            
            print(f'Dealer drew{dealer_card_dealt}')
            print()

            if(dealer_hand[0] > 21):
                dealer_goes_bust = True
                break 
    print('***********RESULTS**********') 

    #Evaluate results
    if player_goes_bust:
        return print('You busted')
         
    
    if dealer_goes_bust:
        return print('Dealer busted')
     
    if player_hand[0] > dealer_hand[0]:
        print(f'Your hand: {player_hand}')
        print(f'Dealer hand: {dealer_hand}')
        print('Thus you win') 

    elif player_hand[0] < dealer_hand[0]:
        print(f'Your hand: {player_hand}')
        print(f'Dealer hand: {dealer_hand}')
        print('Thus you win') 
    else:
        print(f'Your hand: {player_hand}')
        print(f'Dealer hand: {dealer_hand}')
        print('Thus you win') 

if __name__ == '__main__':
    user_choice = 'y'

    while user_choice == 'y':
        run_blackjack() 
        print() 
        user_choice = input('Would you like to play again(y/n)?: ') 