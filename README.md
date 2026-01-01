# Monte Carlo Methods Applied To Blackjack
#### Introduction
The goal of this project is to apply the methods of **Monte Carlo control with exploring starts** to determine the optimal policy and visualize the resulting state-value function, for the card game **Blackjack**. The Methods used in this project are those presented in chapter 5 of Sutton and Barto's Reinforcement learning
## The Environment

### Game overview  
The objective of **blackjack** is to obtain cards whose numerical values, sum to a integer as large as possible **without** exceeding the integer 21. 

All face cards are counted as 10, and an ace can be counted as either 1 or 11. The version of blackjack considered in this project, is the one where each player plays against the dealer independently. The game begins with the player being dealt a card and the dealer dealt one faced down, then the player is dealt his final card and the dealer dealt his last card, of which is face up for the player to be able to know the value of. If the player has an immediate 21, i.e an ace and 10 card, then it is called a natural and he automatically wins the game, unless the dealer also has a natural, in which it will just be a tie. If he does not and the dealer has a natural then the dealer wins the game and player loses. 

Then if the player does not have a natural and neither does the dealer, he then can request additional cards, one at a time(which are called 'Hits') until he either stops at his current sum(sticks) or exceeds 21(goes bust). If he goes bust he automatically loses the game but if he does not bust and decides to stick, then it becomes the dealers turn. The dealer plays by a fixed strategy, he sticks on any sum of 17 or greater, and hits otherwise. If the dealer goes bust, then the player automatically wins but if he does not then the outcome is determined by whose sum is closer to 21, if they both have the same sum then its a tie(push). 

### Formulating as an MDP
Blackjack can be quite easily formulated into a finite episodic MDP. Its done by letting each game of blackjack be an episode, and rewards of +1, -1, and 0 and given for winning, losing and drawing, respectively. All rewards within the game are zero, and $\gamma=1$, i.e do not discount. Since the rewards within the game are zero, then the terminal rewards are also the returns.  

The players actions are to either hit or stick. And the states depend upon the players hand and the dealers showing card. Where the players hand consists of his sum and whether or not he holds an ace he could could count as 11 without busting, if he can then the ace is said to be usable.  

In this case that he does have an ace that's usable, it is always counted as 11, for if he counted it as 1 then his sum would be 11 or less, of which there would then be no decision to be made for the action would always be to hit. Therefore the player makes decisions on the basis of three variables, his current sum(12-21), the dealers up card(A-10), and whether or not he holds a usable ace. These three variables make up the players state. Which ends up making a total of 200. 

The cards are dealt from an infinite deck, that is with replacement, thus there is no benefit of keeping track of the cards that have already been dealt

 ## Monte Carlo Prediction 
 ### An overview of Monte Carlo methods
 Monte Carlo methods only require experience from either actual or simulated interaction with the environment, and they do not assume complete knowledge of the environment. Thus with no prior knowledge of the environment, optimal behavior can still be obtained. 
 
They are ways to solve the Reinforcement Learning problem, based on averaging sample returns. And thus to ensure that returns are well defined, episodic tasks are used. Which then means assuming that experience is divided into episodes and that all episodes will eventually terminate. So only after a completion of an episode are value estimated and polices updated. Thus the returns averaging are complete returns.
 ### Prediction
 Recall that the value of a state is the expected return, starting from that state and thereafter following $\pi$, and the expected return is the cumulative discounted reward get along the way of doing so.  Then an obvious way to estimate the value of a state from experience only, is to simply average the returns observed, after visits to that state. And then as more returns are observed from visits to each state, the average should converge to the expected value of the state value function.

In the code, the method of first visit Monte Carlo prediction was used. Where first visit methods simply means to estimate the state value function for a state, as the average of the returns following first visits to that particular state. It goes like,
````
for  i  in  range(num_episodes):

	states_actions_ep, return_ep  =  run_episode(policy)
	
	if(return_ep  ==  -2):

		continue

	for  t  in  range(len(states_actions_ep))[::-1]:

		if(states_actions_ep[t][0] not  in  states_actions_ep[:t]):
	
			returns[states_actions_ep[t][0]].append(return_ep)

			state_values[states_actions_ep[t][0]] =  average_list(returns[states_actions_ep[t][0]])
````
This is the implementation of the algorthim for first visit MC prediction presented in chapter 5 of Sutton and Barto's Reinforcement learning. The break down of the code is as such,
- For each episode in the number of episodes simulating, a list of states, actions, and rewards are generated. But recall for blackjack the only reward is the terminal one, thus that is the complete return for the episode. 
- Check if actually play a game of blackjack where the player can make a choice, that is if don't automatically win or lose.  
- For each time step in the list of state action pairs, since applying the first visits method, check if the current state at particular time step occurs in the episode already, then if it does do nothing, and loop until get to the first instance of its occurrence
- Of which will save the return got from the state at time step $t$, to the list of returns corresponding to that particular state
- Then with that list of returns corresponding to that particular state,the list of returns  is averaged and that value is the new estimate for the state value function, for that state

As this is done for more and more episodes, eventually every state possible that can be visited, will be visited enough times, such that the average of the returns, will converge to the true value of the value of a state. 
 ## Monte Carlo Control 
 
 

