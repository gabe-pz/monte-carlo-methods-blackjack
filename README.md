# Monte Carlo Methods Applied To Blackjack
#### Introduction
The goal of this project is to apply the methods of **Monte Carlo control with exploring starts** to determine the optimal policy and visualize the resulting state-value function, for the card game **Blackjack**. The Methods used in this project are those presented in chapter 5 of Sutton and Barto's Reinforcement learning
## The Environment

### Game overview  
The objective of **blackjack** is to obtain cards whose numerical values, sum to a integer as large as possible **without** exceeding the integer 21. 

All face cards are counted as 10, and an ace can be counted as either 1 or 11. The version of blackjack considered in this project, is the one where each player plays against the dealer independently. The game begins with the player being dealt a card and the dealer dealt one faced down, then the player is dealt his final card and the dealer dealt his last card, of which is face up for the player to be able to know the value of. If the player has an immediate 21, i.e an ace and 10 card, then it is called a natural and he automatically wins the game, unless the dealer also has a natural, in which it will just be a tie. If he does not and the dealer has a natural then the dealer wins the game and player loses. \

Then if the player does not have a natural and neither does the dealer, he then can request additional cards, one at a time(which are called 'Hits') until he either stops at his current sum(sticks) or exceeds 21(goes bust). If he goes bust he automatically loses the game but if he does not bust and decides to stick, then it becomes the dealers turn. The dealer plays by a fixed strategy, he sticks on any sum of 17 or greater, and hits otherwise. If the dealer goes bust, then the player automatically wins but if he does not then the outcome is determined by whose sum is closer to 21, if they both have the same sum then its a tie(push). 

### Formulating as an MDP
Blackjack can be quite easily formulated into a finite episodic MDP. Its done by letting each game of blackjack be an episode, and rewards of +1, -1, and 0 and given for winning, losing and drawing, respectively. All rewards within the game are zero, and $\gamma=1$, i.e do not discount. Since the rewards within the game are zero, then the terminal rewards are also the returns.  

The players actions are to either hit or stick. And the states depend upon the players hand and the dealers showing card. Where the players hand consists of his sum and whether or not he holds an ace he could could count as 11 without bussin.  

