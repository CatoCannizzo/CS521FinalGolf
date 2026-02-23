from GeneralFunctions import promptUser

def start_game():
    print("Welcome to the card game Golf!")
    rulesPrompt = "Would you like a rules overviewfor this game? (y/n)"
    if promptUser(typed=str, userPrompt=rulesPrompt, ynChoice=True) == "y":
        print("The game starts with each player having 6 face down cards in front of them.")
        print("The cards for each player are in 2 rows of 3 columns, this is there hand.")
        print("You take your turn by swapping a card in your hand for a card from the deck or discard pile.")
        print("Any card you swap into your hand become face up.")
        print("The game ends when one player has all 6 cards in their hand face up.")
        print("The goal of the game is to have the lowest number of points.")
        print("All cards are worth their number, with Jacks & Queens worth 10")
        print("Kings are worth 0, as well as getting verital pairs.")

if __name__ == "__main__":
    start_game()