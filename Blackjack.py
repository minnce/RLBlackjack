import random

# Initializes the decks for blackjack
blackjack = []


def cardRefill():
    for i in range(1, 9):
        for j in range(0, 4):
            for z in range(2, 11):
                blackjack.append(z)
            blackjack.extend(["A", "J", "Q", "K"])
    random.shuffle(blackjack)


def cardDeal(handValue):
    if len(blackjack) > 0:
        try:
            selected = blackjack.pop()
            if selected in ["J", "Q", "K"]:
                cardValue = 10
            elif selected == "A":
                if handValue >= 11:
                    cardValue = 1
                else:
                    cardValue = 11
            else:
                cardValue = selected
            return selected, cardValue
        except IndexError:
            print("No more cards, reshuffling")
            cardRefill()
            return cardDeal(handValue)
    else:
        print("No more cards, reshuffling")
        cardRefill()
        return cardDeal(handValue)

# RL implementation
Q = {} 
epsilon = 0.1 
alpha = 0.5  
gamma = 1.0  

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(["hit", "stay"])
    else:
        if state not in Q:
            Q[state] = {"hit": 0, "stay": 0}
        return max(Q[state], key=Q[state].get)


def update_Q(state, action, reward, next_state):
    if state not in Q:
        Q[state] = {"hit": 0, "stay": 0}
    if next_state not in Q:
        Q[next_state] = {"hit": 0, "stay": 0}

    Q[state][action] += alpha * (reward + gamma * max(Q[next_state].values()) - Q[state][action])


def train(num_episodes):
    for episode in range(num_episodes):
        print("Episode:", episode + 1)
        playerHand = []
        playerHandVal = 0
        playerSoft = False

        for i in range(0, 2):
            selectedCard = cardDeal(playerHandVal)
            playerHand.append(selectedCard[0])
            playerHandVal += int(selectedCard[1])
            if selectedCard[0] == "A":
                playerSoft = True

        state = (playerHandVal, playerSoft)
        action = choose_action(state)

        while action == "hit":
            selectedCard = cardDeal(playerHandVal)
            playerHand.append(selectedCard[0])
            playerHandVal += int(selectedCard[1])

            if playerHandVal > 21 and playerSoft:
                playerHandVal -= 10
                playerSoft = False

            if playerHandVal > 21:
                reward = -1
                next_state = "bust"
                update_Q(state, action, reward, next_state)
                break
            else:
                state = (playerHandVal, playerSoft)
                action = choose_action(state)

        if action == "stay":
            computerHand = []
            computerHandVal = 0
            computerSoft = False

            for i in range(0, 2):
                selectedCard = cardDeal(computerHandVal)
                computerHand.append(selectedCard[0])
                computerHandVal += int(selectedCard[1])
                if selectedCard[0] == "A":
                    computerSoft = True

            while computerHandVal < 17:
                selectedCard = cardDeal(computerHandVal)
                computerHand.append(selectedCard[0])
                computerHandVal += int(selectedCard[1])

                if computerHandVal > 21 and computerSoft:
                    computerHandVal -= 10
                    computerSoft = False

            if computerHandVal > 21:
                reward = 1
                next_state = "win"
            elif playerHandVal > computerHandVal:
                reward = 1
                next_state = "win"
            elif playerHandVal < computerHandVal:
                reward = -1
                next_state = "lose"
            else:
                reward = 0
                next_state = "draw"

            update_Q(state, action, reward, next_state)


num_episodes = 10000

Q = {}

cardRefill()
train(num_episodes)
