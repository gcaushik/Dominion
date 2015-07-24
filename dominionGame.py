# Dominion Module
# -*- coding: utf-8 -*-

import cardnames1
import random

numCards = len(cardnames1.curse_cards) + len(cardnames1.victory_cards) + len(cardnames1.treasure_cards) + len(cardnames1.victory_kingdom_cards) + len(cardnames1.kingdom_cards)

supply = [0] * numCards

embargo = list()


class GameState(object):
  action = 'action'
  buy = 'buy'
  clean = 'cleanup'
  def __init__(self):
    self.decks = []
    self.hands = []
    self.discards = []
    self.money = []
    self.phase = GameState.action
    self.actions = 1
    self.whoseTurn = 0
    self.numBuys = 1
    self.outpost = False
    self.played = []



# Shuffle decks
def shuffle(player, gameState): 
  randobj = random.Random(1)
  playerdeck = gameState.decks[player]

  if not playerdeck:
    return -1

  playerdeck.sort()
  randobj.shuffle(playerdeck)

  return 0


# Draw card
def drawCard(player,gameState):
  playerdeck = gameState.decks[player]
  playerdcard = gameState.discards[player]
  playerhand = gameState.hands[player]

  if not playerdeck:
    if not playerdcard:
      return -1
    r = len(playerdcard)
    for i in range(r):
      playerdeck.append(playerdcard.pop(-1))
    shuffle(player,gameState)

  playerhand.append(playerdeck.pop(-1))

  return 0

    
# Update coins
def updateCoins(player,gameState,bonus):
  playerhand = gameState.hands[player]
  playercoins = 0
  for i in playerhand:
    if i == cardnames1.copper:
      playercoins += 1
    elif i == cardnames1.silver:
      playercoins += 2
    elif i == cardnames1.gold:
      playercoins += 3
  playercoins += bonus 
  gameState.money[player] = playercoins
  return 0



# Initializes the game
def initializeGame(numPlayers, kingdomCards, randomSeed):
  # Set up random number generator
  random.seed(randomSeed)
  
  max_players = 4
  # Check players  
  assert ((numPlayers >= 2 and numPlayers <= max_players))
  
  assert (len(list(set(kingdomCards))) == len(kingdomCards)) 

  # Initialize Supply

  numCurse = [10,20,30]
  numVictory = [8,12,12]
  numCopper = 60
  numSilver = 40
  numGold = 30
  numTreasure = [numGold, numSilver, numCopper]
  numVKingdom = [8,12,12]
  numKingdom = 10 
  
  # Set up curse cards
  for i in cardnames1.curse_cards:
    supply[i] = numCurse[numPlayers-2] 
  
  # Set up victory cards
  for i in cardnames1.victory_cards: 
    supply[i] = numVictory[numPlayers-2]

  # Set up treasure cards
  for i in cardnames1.treasure_cards: 
    supply[i] = numTreasure.pop()

  # Set up victory kingdom cards
  # A value of -1 means that particular card was not one of the 10 chosen for this game
  for i in cardnames1.victory_kingdom_cards:
    if i in kingdomCards:
      supply[i] = numVKingdom[numPlayers-2]
    else: 
      supply[i] = -1

  # Set up regular kingdom cards
  # A value of -1 means that particular card was not one of the 10 chosen for this game
  for i in cardnames1.kingdom_cards:
    if i in kingdomCards:
      supply[i] = numKingdom
    else:
      supply[i] = -1

  game = GameState()

  # Set up decks
  for i in range(numPlayers):
    game.decks.append([cardnames1.estate] * 3 + [cardnames1.copper] * 7)
    supply[1] -= 3
    supply[4] -= 7  

  # Shuffle decks 
  for i in range(numPlayers):
    shuffle(i, game)

  # Set embargo tokens for each supply pile to zero (if Embargo is in game)
  if supply[12] != -1:
    embargo.extend([0] * len(supply)) 

  # Set up discards and hands
  for i in range(numPlayers):
    game.discards.append([])
    game.hands.append([])  
  
  # First player draw initial hand
  for j in range(5):
    drawCard(0, game)

  # Initialize first turn 
  for i in range(numPlayers):
     game.money.append(0)

  updateCoins(0,game,0)

  return game  


def whoseTurn(gameState):
  return gameState.whoseTurn

def numHandCards(gameState):
  player = gameState.whoseTurn
  num = len(gameState.hands[player])
  return num

def handCard(handNum, gameState):
  player = gameState.whoseTurn
  return gameState.hands[player][handNum]

def supplyCount(card, gameState):
  return supply[card]


# End turn. Discard hand and played cards. Check if outpost has been played, and set up new turn.
def endTurn(gameState):
  currentPlayer = gameState.whoseTurn
  numPlayers = len(gameState.hands)
  numh = len(gameState.hands[currentPlayer])
  nump = len(gameState.played)
  for i in range(numh):
    gameState.discards[currentPlayer].append(gameState.hands[currentPlayer].pop(0))
  for i in range(nump):
    gameState.discards[currentPlayer].append(gameState.played.pop())
  gameState.phase = GameState.action
  gameState.numBuys = 1
  gameState.actions = 1
  draw = 5
  if gameState.outpost == True:
    draw = 3
  else:
    gameState.whoseTurn = (currentPlayer + 1) % numPlayers
  for i in range(draw):
    drawCard(gameState.whoseTurn, gameState)
  updateCoins(gameState.whoseTurn, gameState, 0)
  return 0



# Is the game over
def isGameOver(gameState):
  if supply[cardnames1.province] == 0:
    return 1
  empty = [i for i in supply if i == 0]
  if len(empty) >= 3:
    return 1
  return 0




# Calculate score for player
def scoreFor(player, gameState):
  score = 0
  deckSize = len(gameState.decks[player])

  for i in gameState.decks[player]:
    if i == cardnames1.curse:
      score += -1
    elif i == cardnames1.estate:
      score += 1
    elif i == cardnames1.duchy:
      score += 3
    elif i == cardnames1.province:
      score += 6
    elif i == cardnames1.great_hall:
      score += 1
    elif i == cardnames1.gardens:
      score += (deckSize/10)

  for i in gameState.discards[player]:
    if i == cardnames1.curse:
      score += -1
    elif i == cardnames1.estate:
      score += 1
    elif i == cardnames1.duchy:
      score += 3
    elif i == cardnames1.province:
      score += 6
    elif i == cardnames1.great_hall:
      score += 1
    elif i == cardnames1.gardens:
      score += (deckSize/10)

  for i in gameState.hands[player]:
    if i == cardnames1.curse:
      score += -1
    elif i == cardnames1.estate:
      score += 1
    elif i == cardnames1.duchy:
      score += 3
    elif i == cardnames1.province:
      score += 6
    elif i == cardnames1.great_hall:
      score += 1
    elif i == cardnames1.gardens:
      score += (deckSize/10)

  return score



# Decide the winner - Highest score wins if there is a tie then player with fewer turns wins, 
# if there is still a tie the win is shared.
# player matrix shows winner, winner = 1, everyone else = 0, unless there is a tie then multiple
# players will have a 1 in the matrix.
def getWinners(players, gameState):
  for i in range(len(players)):
    players[i] = scoreFor(i,gameState)  
  highScore = max(players)
  winners = []
  
  for i in range(len(players)):
    if players[i] == max:
      winners.append(i)

  # If there is a tie
  if len(winners) > 1:
    turns = [i for i in winners if i > gameState.whoseTurn]
    # If turn tiebreaker fails
    if len(turns) > 1:
      for i in range(len(players)):
        if i in turns:
          players[i] = 1
        else:
          players[i] = 0
    # If turn tiebreaker fails
    elif len(turns) == 0:
      for i in range(len(players)):
        if i in winners:
          players[i] = 1
        else:
          players[i] = 0
    # Winner is determined
    else:
      for i in range(len(players)):
        if i in turns:
          players[i] = 1
        else:
          players[i] = 0
  # If no tie, winner is determined                
  else:
    for i in range(len(players)):
        if i in winners:
          players[i] = 1
        else:
          players[i] = 0
  return 0



def cardEffect(card, choice1, choice2, choice3, gameState, handPos, bonus):
  currentPlayer = gameState.whoseTurn
  
  # Reveal cards from your deck until you reveal 2 Treasure cards. 
  # Put those Treasure cards in your hand and discard the other revealed cards.
  if card == cardnames1.adventurer:
    treasure = 0
    draw = 0
    reveal = []
    while treasure < 2:
      if not gameState.decks[currentPlayer]:
        if draw == 1:
          break
        else:
          draw += 1
      drawCard(currentPlayer,gameState)
      reveal.append(gameState.hands[currentPlayer].pop())  
      if reveal[-1] in cardnames1.treasure_cards:
        treasure += 1
        gameState.hands[currentPlayer].append(reveal[-1])
        del reveal[-1]
    gameState.discards[currentPlayer].extend(reveal)


  # Reveal a card from your hand. 
  # Return up to 2 copies of it from your hand to the Supply. 
  # Then each other player gains a copy of it.
  # choice1 is the card to reveal, and choice2 is the number of copies.
  elif card == cardnames1.ambassador:
    numCards = len(gameState.hands[currentPlayer])
    if choice2 < 0 or choice2 > 2:
      return -1
    if choice1 == handPos or choice1 < 0 or choice1 >= numCards:
      return -1
    if numCards == 0:
      return -1
    returned = 0
    ret = gameState.hands[currentPlayer][choice1]
    for r in range(choice2):
      if ret in gameState.hands[currentPlayer]:
        returned += 1
        gameState.hands[currentPlayer].remove(ret)
    supply[ret] += returned
    numPlayers = len(gameState.hands)
    others = [i for i in range(numPlayers) if i != currentPlayer]
    for i in reversed(others):
      gameState.hands[i].append(ret)
   

  # +1 Buy
  # You may discard an Estate card. If you do, +$4. Otherwise, gain an Estate card.
  # choice1 > 0 means 1st option, otherwise 2nd option
  elif card == cardnames1.baron:
    gameState.numBuys += 1   
    if choice1 > 0:
      discarded = False
      if cardnames1.estate in gameState.hands[currentPlayer]:
        gameState.hands[currentPlayer].remove(cardnames1.estate)
        discarded = True
      if discarded == True:
        bonus += 4         
      else:
        gainCard(cardnames1.estate,gameState,0,currentPlayer)
        if supply[cardnames1.estate] == 0:
          isGameOver(gameState)
    else:
      gainCard(cardnames1.estate,gameState,0,currentPlayer)
      if supply[cardnames1.estate] == 0:
        isGameOver(gameState)
    
  
  # +4 Cards; +1 Buy
  # Each other player draws a card.
  elif card == cardnames1.council_room:
    gameState.numBuys += 1
    for i in range(4):
      drawCard(currentPlayer,gameState)        
    numPlayers = len(gameState.hands)
    others = [i for i in range(numPlayers) if i != currentPlayer]
    for i in others:
      drawCard(i,gameState)  
    

  # +$2
  # Each other player discards a Copper card (or reveals a hand with no Copper).
  elif card == cardnames1.cutpurse:
    bonus += 2
    numPlayers = len(gameState.hands)
    others = [i for i in range(numPlayers) if i != currentPlayer]
    for i in others:
      if cardnames1.copper in gameState.hands[i]:
        gameState.hands[i].remove(cardnames1.copper)
        gameState.discards[i].append(cardnames1.copper)
    

  # Trash this card. Put an Embargo token on top of a Supply pile.
  # When a player buys a card, he gains a Curse card per Embargo token on that pile.
  # choice1 is the supply pile.
  elif card == cardnames1.embargo:
    gameState.hands[currentPlayer].remove(card)
    if supply[choice1] > 0:
      embargo[choice1] += 1
    else:
      return -1
    return 0

  # Trash this card. Gain a card costing up to $5.
  # choice1 is the card.
  elif card == cardnames1.feast:
    gameState.hands[currentPlayer].remove(card)
    if getCost(choice1) > 5:
      return -1
    elif supply[choice1] <= 0:
      return -1
    else:
      gainCard(choice1, gameState, 0, currentPlayer)
    return 0

  # Worth 1 Victory for every 10 cards in your deck (rounded down).
  elif card == cardnames1.gardens:
    return -1

  # 1 Victory Point
  # +1 Card; +1 Action.
  elif card == cardnames1.great_hall:
    drawCard(currentPlayer, gameState)
    gameState.actions += 1   
    

  # Trash a Treasure card from your hand. 
  # Gain a Treasure card costing up to $3 more; put it into your hand.
  # choice1 is the card to trash, choice2 is the card to gain.
  elif card == cardnames1.mine:
    if getCost(choice2) > (getCost(choice1) + 3):
      return -1
    if choice1 not in [cardnames1.copper,cardnames1.gold,cardnames1.silver]:
      return -1
    if choice2 > len(supply) or choice2 < 0:
      return -1
    if choice1 not in gameState.hands[currentPlayer]:
      return -1
    else:
      gameState.hands[currentPlayer].remove(choice1)
      gainCard(choice2, gameState, 2, currentPlayer)
    

  # You only draw 3 cards (instead of 5) in this turn’s Clean-up phase. 
  # Take an extra turn after this one. 
  # This can’t cause you to take more than two consecutive turns.
  elif card == cardnames1.outpost:
    gameState.outpost = True
    
  
  # +3 cards
  elif card == cardnames1.smithy:
    for i in range(3):
      drawCard(currentPlayer, gameState)
                               
 
  # +1 Card; +2 Actions. 
  elif card == cardnames1.village:
    drawCard(currentPlayer, gameState)
    gameState.actions += 2
    
  gameState.played.append(card)
  updateCoins(currentPlayer, gameState, bonus)
  return 0   


  
# Play card
def playCard (handPos, choice1, choice2, choice3, gameState):
  coinBonus = 0

  if gameState.phase != GameState.action:
    return -1

  if gameState.actions < 1:
    return -1
  
  currentPlayer = gameState.whoseTurn

  if handPos < 0 or handPos >= len(gameState.hands[currentPlayer]):
    return -1

  card = gameState.hands[currentPlayer][handPos]
  
  action_cards = [cardnames1.adventurer, cardnames1.ambassador, cardnames1.baron, cardnames1.council_room, cardnames1.cutpurse,
                 cardnames1.embargo, cardnames1.feast, cardnames1.great_hall, cardnames1.mine, cardnames1.outpost, cardnames1.smithy,
                 cardnames1.village]

  if card not in action_cards:
    return -1

  if cardEffect(card, choice1, choice2, choice3, gameState, handPos, coinBonus) < 0:
    return -1

  gameState.actions -= 1
  updateCoins(currentPlayer, gameState, coinBonus)
    
  return 0


# Get cost of card
def getCost(supplyPos):
  cost = 0
  if supplyPos in [cardnames1.curse,cardnames1.copper]:
    return cost
  elif supplyPos in [cardnames1.estate, cardnames1.embargo]:
    cost = 2
  elif supplyPos in [cardnames1.silver,cardnames1.ambassador,cardnames1.great_hall,cardnames1.village]:
    cost = 3
  elif supplyPos in [cardnames1.baron, cardnames1.cutpurse, cardnames1.feast, cardnames1.gardens, cardnames1.smithy]:
    cost = 4
  elif supplyPos in [cardnames1.duchy, cardnames1.council_room, cardnames1.mine, cardnames1.outpost]:
    cost = 5
  elif supplyPos in [cardnames1.gold, cardnames1.adventurer]:
    cost = 6
  elif supplyPos == cardnames1.province:
    cost = 8
  else:
    return -1
  
  return cost
  


# Gain a card from supply
def gainCard(supplyPos, gameState, toFlag, player):
  if supply[supplyPos] < 1:
    return -1

  # toFlag = 0 : add to discard
  # toFlag = 1 : add to deck
  # toFlag = 2 : add to hand
  if toFlag == 0:
    gameState.discards[player].append(supplyPos)
  elif toFlag == 1:
    gameState.decks[player].append(supplyPos)
  elif toFlag == 2:
    gameState.hands[player].append(supplyPos)

  supply[supplyPos] -= 1
  return 0


# Buy a card from supply
def buyCard (supplyPos, gameState):
  currentPlayer = gameState.whoseTurn

  if gameState.numBuys < 1:
    return -1

  if supply[supplyPos] < 1:
    return -1

  if gameState.money[currentPlayer] < getCost(supplyPos):
    return -1

  cost = getCost(supplyPos)
  gameState.phase = GameState.buy
  
  updateCoins(currentPlayer, gameState, -cost)    
  gainCard(supplyPos, gameState, 0, currentPlayer)
  if embargo[supplyPos] > 0:
    for i in range(embargo[supplyPos]):
      gainCard(cardnames1.curse, gameState, 0, currentPlayer)
  gameState.numBuys -= 1 
  return 0

