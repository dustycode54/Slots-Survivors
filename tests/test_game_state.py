
from src.game_state import SlotGame


def testPlayerStats(): #Test all statistics are properly initialized at beginning of game. 
    Game = SlotGame()
    Game.Reset()

    assert Game.PlayerStats["Round"] == 1
    assert Game.PlayerStats["Pulls Allowed"] == 3
    assert Game.PlayerStats["Pulls Left"] == 3
    assert Game.PlayerStats["Round Points"] == 0
    assert Game.PlayerStats["Total Points"] == 0
    assert Game.PlayerStats["Target Score"] == 100
    assert Game.State == "In Round"


def testPullLever(): #Test if it deducts a pull and updates score
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(40)

    assert Game.PlayerStats["Round Points"] == 40
    assert Game.PlayerStats["Total Points"] == 40
    assert Game.PlayerStats["Pulls Left"] == 2
    assert Game.State == "In Round"


def testSurvivedRound(): #Test if player survives a round after reaching target score. 
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(40)
    Game.PullLever(30)
    Game.PullLever(30)

    assert Game.PlayerStats["Round Points"] == 100
    assert Game.PlayerStats["Pulls Left"] == 0
    assert Game.State == "Pick Upgrade"


def testFailedRound(): #Test if game ends when player uses all available pulls. 
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(10)
    Game.PullLever(20)
    Game.PullLever(30)

    assert Game.PlayerStats["Round Points"] == 60
    assert Game.PlayerStats["Pulls Left"] == 0
    assert Game.State == "Run Ended"


def testNextRound(): #Test if advancing to next round increases difficulty while preserving accumulated score.
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(50)
    Game.PullLever(50)
    Game.PullLever(50)

    Game.NextRound()

    assert Game.PlayerStats["Round"] == 2
    assert Game.PlayerStats["Target Score"] == 150
    assert Game.PlayerStats["Round Points"] == 0
    assert Game.PlayerStats["Total Points"] == 150
    assert Game.PlayerStats["Pulls Left"] == 3
    assert Game.State == "In Round"


def testExtraPull(): #Test if acquiring extra pull increases the number of available pulls
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(50)
    Game.PullLever(50)
    Game.PullLever(50)

    Game.OwnedUpgrades.add("Extra Pull")
    Game.PlayerStats["Pulls Allowed"] += 1

    Game.NextRound()

    assert Game.PlayerStats["Pulls Allowed"] == 4
    assert Game.PlayerStats["Pulls Left"] == 4
    assert "Extra Pull" in Game.OwnedUpgrades


def testGameProgression(): #Test over5all progression
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(50)
    Game.PullLever(50)
    Game.PullLever(50)

    assert Game.State == "Pick Upgrade"

    Game.NextRound()

    Game.PullLever(20)
    Game.PullLever(20)
    Game.PullLever(20)

    assert Game.PlayerStats["Round"] == 2
    assert Game.PlayerStats["Total Points"] == 210
    assert Game.State == "Run Ended"


def testReset(): #Test whether restarting a game restores all original stats and removes upgrades.
    Game = SlotGame()
    Game.Reset()

    Game.PullLever(50)
    Game.OwnedUpgrades.add("Extra Pull")
    Game.PlayerStats["Pulls Allowed"] += 1

    Game.Reset()

    assert Game.PlayerStats["Round"] == 1
    assert Game.PlayerStats["Round Points"] == 0
    assert Game.PlayerStats["Total Points"] == 0
    assert Game.PlayerStats["Pulls Allowed"] == 3
    assert Game.PlayerStats["Pulls Left"] == 3
    assert Game.PlayerStats["Target Score"] == 100
    assert Game.OwnedUpgrades == set()
    assert Game.State == "In Round"
