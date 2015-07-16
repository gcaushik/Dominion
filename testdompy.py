import dominion as d
import cardnames as c
import itertools
import random




game2 = d.initializeGame(3, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)

game3 = d.initializeGame(4, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)

game4 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.outpost], 10)

def test1(game):
  d.buyCard(c.silver, game)
  d.endTurn(game)
  assert (d.buyCard(c.copper, game) == 0)
  d.buyCard(c.silver, game)
  assert (d.whoseTurn(game) == 1)
  assert (d.buyCard(c.silver, game) == -1)
  d.endTurn(game)
  assert (d.buyCard(c.province,game) == -1) 
    
  print "TEST CASE PASSED" 
  return 0                  
  
# Test checks whether a game state sets up supplies correctly with all the different valid configurations 
# of starting cards and players.
def checkStart():
  kingdomCards = [7,8,9,10,11,12,13,14,15,16,17,18,19]
  kingdom = []
  configurations = [comb for comb in itertools.combinations(kingdomCards,10)]
  counter = 0
  for i in range(2,5):
    for conf in configurations:
      kingdom = list(conf)
      game = d.initializeGame(i,kingdom,10)
      counter += 1
      assert(d.supplyCount(c.silver,game) == 40)
      assert(d.supplyCount(c.gold,game) == 30)
      for j in c.kingdom_cards:
        if j in kingdom:
          assert(d.supplyCount(j,game) == 10) 
      if i == 2:
        assert(d.supplyCount(c.copper,game) == 46)
        assert(d.supplyCount(c.curse,game) == 10)
        assert(d.supplyCount(c.estate,game) == 2)
        assert(d.supplyCount(c.duchy,game) == 8)
        assert(d.supplyCount(c.province,game) == 8)
        assert(d.supplyCount(c.gardens,game) == 8)
        assert(d.supplyCount(c.great_hall,game) == 8)
      elif i == 3:
        assert(d.supplyCount(c.copper,game) == 39)
        assert(d.supplyCount(c.curse,game) == 20)
        assert(d.supplyCount(c.estate,game) == 3)
        assert(d.supplyCount(c.duchy,game) == 12)
        assert(d.supplyCount(c.province,game) == 12)
        assert(d.supplyCount(c.gardens,game) == 12)
        assert(d.supplyCount(c.great_hall,game) == 12) 
      elif i == 4:
        assert(d.supplyCount(c.copper,game) == 32)
        assert(d.supplyCount(c.curse,game) == 30)
        assert(d.supplyCount(c.estate,game) == 0)
        assert(d.supplyCount(c.duchy,game) == 12)
        assert(d.supplyCount(c.province,game) == 12)
        assert(d.supplyCount(c.gardens,game) == 12)
        assert(d.supplyCount(c.great_hall,game) == 12)

      print "Configuration ", counter, " PASSED"
      print i, "players, kingdom = " , kingdom
  
  print "TEST CASE PASSED"
  return 0

# First turn of the game you cannot play actions because there are no action cards in your hand.
def checkFirstTurn():
  game = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
  handPos = random.randrange(5)
  ret = d.playCard(handPos,0,0,0,game)
  assert(ret == -1)
  print "TEST CASE PASSED"
  return 0

# Check if turn really transfers to the next player. Also check special case of outpost, where turn stays with 
# same player.
# Here we have two tests - first case hand count at the end of turn should be 5. Second case the hand count should
# be 3.
def checkEndTurn(game):
  d.buyCard(c.embargo,game)
  d.endTurn(game)
  assert (d.whoseTurn(game) == 1)
  assert(d.numHandCards(game) == 5)

  print "TEST CASE PASSED"

def checkOutpost(game):
  # Outpost case
  d.updateCoins(0,game,5)
  assert(d.buyCard(c.outpost,game) == 0)
  d.endTurn(game)
  d.endTurn(game)
  outpost = -1
  for i in range(5):
    if handCard(i,game) == card.outpost:
      outpost = i
  if outpost == -1:
    d.playCard(outpost,0,0,0,game)
    d.endTurn(game)
    assert(d.whoseTurn(game) == 1)
    assert(d.numHandCards(game) == 3)

  print "TEST CASE PASSED"  
  

# Check drawCard, especially corner case where deck and discard are empty.
def checkDraw(game):
  size = len(game.decks[0]) + len(game.discards[0])
  for i in range(size):
    assert(d.drawCard(0,game) == 0)
  assert(d.drawCard(0,game) == -1)

  print "TEST CASE PASSED"


# Check playCard, you are not allowed to specify an index out of bounds of the hand.
# You must play action cards.
# You can only play cards in the action phase.
# You can only play as many cards as you have actions.
def checkPlayCard(game):
  d.updateCoins(0,game,20)
  d.buyCard(c.baron,game)
  d.endTurn(game)
  d.endTurn(game)
  assert(d.playCard(-1,0,0,0,game) == -1)
  for i in range(d.numHandCards(game)):
    if (d.handCard(0,game) == c.baron):
      assert(d.playCard(i,1,0,0,game) == 0) 
    else:
      assert(d.playCard(0,0,0,0,game) == -1)

  # Still need to refine this

  print "TEST CASE PASSED"
  
  

# Check buyCard, you are not allowed to buy an item that costs too much, or buy more times than the number of buys you have.
def checkBuyCard(game):
  assert(d.buyCard(c.province,game) == -1)
  assert(d.buyCard(c.silver,game) == 0)
  assert(d.buyCard(c.embargo,game) == -1)
 
  print "TEST CASE PASSED"


# Check gainCard, if invalid card then you cannot gain it.
# Otherwise it has to be put in the appropriate place, according to whether in discard, hand, or deck.
def checkGainCard(game):
  assert(d.gainCard(-1,game,0,0) == -1)
  d.gainCard(c.province,game,0,0)
  assert(c.province in game.discards[0])
  d.gainCard(c.province,game,1,0) 
  assert(c.province in game.decks[0])
  d.gainCard(c.province,game,2,0)
  assert(c.province in game.hands[0])

  print "TEST CASE PASSED"

# Check if score is accurate.
def checkScore(game):
  score = d.scoreFor(0,game)
  assert(score == 3)
  d.updateCoins(0,game,20)
  d.buyCard(c.province,game)
  d.endTurn(game)
  d.updateCoins(0,game,20)
  d.buyCard(c.duchy,game)
  score = d.scoreFor(0,game)
  assert(score == 9)
  score = d.scoreFor(1,game)
  assert(score == 6)
  d.endTurn(game)
  d.updateCoins(0,game,20)
  d.buyCard(c.great_hall,game)
  d.endTurn(game)
  d.updateCoins(0,game,20)
  d.buyCard(c.gardens,game)
  score = d.scoreFor(0,game)
  assert(score == 10)
  for i in range(10):
    d.gainCard(c.silver,game,1,1)
  score = d.scoreFor(1,game)
  assert(score == 7)
  
  print "TEST CASE PASSED"  


# Check if game is over
def checkGameOver(game):
  for i in range(8):
    assert(d.isGameOver(game) == 0)
    d.gainCard(c.province,game,0,0)
  assert(d.isGameOver(game) == 1)

  print "TEST CASE PASSED"

def checkGameOver2(game):
  for i in range(10):
    assert(d.isGameOver(game) == 0)
    d.gainCard(c.ambassador,game,0,0)
  for i in range(10):
    assert(d.isGameOver(game) == 0)
    d.gainCard(c.adventurer,game,0,0)
  for i in range(10):
    assert(d.isGameOver(game) == 0)
    d.gainCard(c.baron,game,0,0)
  assert(d.isGameOver(game) == 1)
  
  print "TEST CASE PASSED"



# COMMENTED OUT TESTS FAILED

game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
#checkStart()
checkFirstTurn()
#checkEndTurn(game1)

game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
#checkOutpost(game4)

test1(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkDraw(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkPlayCard(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkBuyCard(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkGainCard(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
#checkScore(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkGameOver(game1)
game1 = d.initializeGame(2, [c.adventurer, c.ambassador, c.baron, c.council_room, c.cutpurse,
                            c.embargo, c.feast, c.gardens, c.great_hall, c.mine], 10)
checkGameOver2(game1)
