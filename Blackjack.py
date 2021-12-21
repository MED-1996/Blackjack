import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self, suit, rank):
        
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def set_value(self, value):
        self.value = value
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    
    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

class Player:
    
    def __init__(self, name, amount_of_money):
        self.name = name
        self.amount_of_money = amount_of_money
        self.cards = []
    
    def __str__(self):
        return f'{self.name} has ${self.amount_of_money}.'
    
    # Player can "hit". The opposite of hitting is "staying".
    def hit(self):
        return True
    
    # Player can bet an amount.
    def bet(self, amount):
        self.amount_of_money -= amount
    
    # Player can collect winnings.
    def collect(self, amount):
        self.amount_of_money += amount


###################################################


# Opening Statement
print('Welcome to BlackJack, Let\'s have some fun!')


# Ask player for name/amount, then initiate player.
name = input('Please enter your name: ')
amount = int(input('Please enter how much money you\'d like to play with: '))
player  = Player(name, amount)


# We will treat the dealer as a "Player".
dealer = Player('Dealer', 0)


game_on = True
round_number = 0

# Blackjack game loop.
while game_on and (player.amount_of_money > 0):
    
    # Start a new round of Blackjack.
    deck = Deck()
    deck.shuffle()
    player.cards = []
    dealer.cards = []
    round_number += 1
    print(f'\n---------------Round {round_number}---------------\n')
    
    
    # Ask the player to place a bet.
    bet_placed = False
    bet_amount = 0
    while not bet_placed:
        bet_amount = int(input('Place your bet: '))
        
        # Ensure that the bet does not exeed the amount of money they have available to bet.
        if (bet_amount > player.amount_of_money):
            print(f'Can\'t bet ${bet_amount}, bet must be less than or equal to ${player.amount_of_money}')
        else:
            player.bet(bet_amount)
            print(f'${bet_amount} bet has been placed!\n')
            bet_placed = True
    
    
    # Deal 2 cards to both the player & the dealer & calculate their starting sums.
    player.cards.append(deck.deal_one())
    dealer.cards.append(deck.deal_one())
    player.cards.append(deck.deal_one())
    dealer.cards.append(deck.deal_one())
    
    player_sum = player.cards[0].value + player.cards[1].value
    dealer_sum = dealer.cards[0].value + dealer.cards[1].value
    
    # Incase 2 Aces are dealt to the player/dealer, this automatically sets their sum to 12 instead of 22. 
    if player_sum == 22:
        player.cards[0].set_value(1)
        player_sum = 12
    
    if dealer_sum == 22:
        dealer.cards[0].set_value(1)
        dealer_sum = 12
    
    # Show what cards were dealt
    print(f'***Dealers Cards***\n{dealer.cards[1]}')
    print(f'\n***{player.name}\'s Cards***\n{player.cards[0]}\n{player.cards[1]}')
    
    
    # Begin asking the player if they would like to "hit" or "stay".
    bust = False
    
    while not bust:
    
        hit = input('\nWould you like to hit or stay [h/s]: ')
        
        # If the player hits, we add a card to their hand & calculate the new sum.
        if hit.lower() == 'h':
            player.cards.append(deck.deal_one())
            player_sum += player.cards[-1].value
            card_slot = 0
            
            
            while player_sum > 21:
                
                # If the players sum is greater than 21, this algorithm searches the cards to see if any Aces can be devauled from 11 to 1.
                if (player.cards[card_slot].rank == 'Ace') and (player.cards[card_slot].value == 11):
                    player.cards[card_slot].set_value(1)
                    player_sum -= 10
                
                # If we've gone through all the cards & all the Aces are 1's and the player is still above 21, then they have busted.
                if (card_slot == (len(player.cards) - 1)) and (player_sum > 21):
                    bust = True
                    break
                    
                card_slot += 1
            
            
            # Print the new cards the player has, 1 has been added
            print(f'*_*{player.name}\'s New Cards*_*')
            for card in player.cards:
                print(card)
        
        
        # The player stays and we stop asking them if they'd like to hit.
        elif hit.lower() == 's':
            break
        
        
        # The player gives an invalid text entry.
        else:
            print('Not a valid entry, please enter [h or s]!')
    
    
    # If the player busted, then they lost.
    if bust == True:
        print(f'You busted! Your remaining balance is ${player.amount_of_money}.')
     
    
    # If the player didn't bust, then we need to see if the dealer beats the player.      
    else:
        # Print the 2 cards the dealer has.
        print('***Dealers Cards***')
        
        for card in dealer.cards:
            print(card)     
            
        dealer_bust = False
        
        
        while not dealer_bust:
            
            # Check to see if both the dealer & player have BlackJack.
            if dealer_sum == player_sum == 21:
                print(f'Draw, you both have BlackJack! Your remaining balance is ${player.amount_of_money}.')
                break
            
            
            # If the dealer has a greater sum than the player, the dealer has won.
            elif dealer_sum > player_sum:
                print(f'The dealer has beaten you! Your remaining balance is ${player.amount_of_money}.')
                dealer.collect(bet_amount)
                break
            
            
            # The dealer must hit, inorder to get a sum higher than the players.
            else:
                dealer.cards.append(deck.deal_one())
                dealer_sum += dealer.cards[-1].value
                
                print('\n*_*Dealers New Cards*_*')
                for card in dealer.cards:
                    print(card)
            
                card_slot = 0
                while dealer_sum > 21:
                
                    # If the dealers sum is greater than 21, this algorithm searches the cards to see if any Aces can be devauled from 11 to 1.
                    if (dealer.cards[card_slot].rank == 'Ace') and (dealer.cards[card_slot].value == 11):
                        dealer.cards[card_slot].set_value(1)
                        dealer_sum -= 10
                    
                    # If we've gone through all the cards & all the Aces are 1's and the dealer is still above 21, then they have busted.
                    if (card_slot == (len(dealer.cards) - 1)) and (dealer_sum > 21):
                        dealer_bust = True
                        player.collect(2*bet_amount)
                        print(f'\nThe dealer has busted, you win ${bet_amount}! your balance is now ${player.amount_of_money}!')
                        break
                    
                    card_slot += 1
        
        
    # Ask the player if they'd like to play another round of Blackjack.   
    while True:
        play_another_round = input('Would you like to play another round [y,n]: ')
        if play_another_round.lower()  == 'n':
            game_on = False
            break
        elif play_another_round.lower()  == 'y':
            break
        else:
            print('Invalid entry, please enter [y or n].')     

            
# End the game with a thanks & some statistics.
print(f'\nThanks for playing {player.name}!')

if player.amount_of_money == 0:
    print('You can\'t play, you have $0.')
    print(f'You lost ${amount - player.amount_of_money}! Next Time!')
elif player.amount_of_money == amount:
    print('You didn\'t win or lose any money.')
elif player.amount_of_money > amount:
    print(f'You won ${player.amount_of_money - amount}! Congrats!')
else:
    print(f'You lost ${amount - player.amount_of_money}! Next Time!')   