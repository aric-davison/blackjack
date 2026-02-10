import random

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
    }
    deck = [(rank, suit, value) for suit in suits for rank, value in ranks.items()]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)  

def dealing_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    value = sum(card[2] for card in hand)
    # Adjust for Aces if value exceeds 21
    aces = [card for card in hand if card[0] == 'Ace']
    while value > 21 and aces:
        value -= 10
        aces.pop()
    return value

def display_hand(hand, owner, hide_hole_card=False):
    if hide_hole_card:
        visible = hand[:1]
        print(f"{owner}'s Hand: {hand[0][0]} of {hand[0][1]}, [Hidden] (Value: {calculate_hand_value(visible)})")
    else:
        print(f"{owner}'s Hand: " + ", ".join(f"{card[0]} of {card[1]}" for card in hand) + f" (Value: {calculate_hand_value(hand)})")

def check_winner(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return "Dealer wins! Player busts."
    elif dealer_value > 21:
        return "Player wins! Dealer busts."
    elif player_value > dealer_value:
        return "Player wins!"
    elif dealer_value > player_value:
        return "Dealer wins!"
    else:
        return "It's a tie!"

def player_choice():
    while True:
        choice = input("Do you want to hit (h) or stand (s)? ").lower()
        if choice == 'h':
            return False
        elif choice == 's':
            return True
        else:
            print("Invalid choice. Please enter 'h' to hit or 's' to stand.")


def main():
    deck = create_deck()
    shuffle_deck(deck)

    print("Welcome to Blackjack!")
    print("The goal is to get as close to 21 as possible without going over.")
    print("Face cards are worth 10, and Aces can be worth 1 or 11.")
    print(" press 'h' to hit or 's' to stand.")
    #dealing logic 
    player_hand = [dealing_card(deck)]
    dealer_hand = [dealing_card(deck)]
    player_hand.append(dealing_card(deck))
    dealer_hand.append(dealing_card(deck))

    display_hand(player_hand, "Player")
    display_hand(dealer_hand, "Dealer", hide_hole_card=True)

    if calculate_hand_value(player_hand) == 21:
        print("Blackjack!")
        display_hand(dealer_hand, "Dealer")
        print(check_winner(player_hand, dealer_hand))
        return

    while player_choice() == False:
        player_hand.append(dealing_card(deck))
        display_hand(player_hand, "Player")
        if calculate_hand_value(player_hand) > 21:
            break

    display_hand(dealer_hand, "Dealer")
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(dealing_card(deck))
        display_hand(dealer_hand, "Dealer") 
    print(check_winner(player_hand, dealer_hand))
if __name__ == "__main__":
    main()


        
