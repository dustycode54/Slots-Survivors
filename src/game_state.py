
class SlotGame:
    def __init__(self):
        self.Reset() #Initialize game
        self.State = "Main Menu"

    def Reset(self): #Resets all stats and removes upgrades to start new game
        self.PlayerStats = {
            "Round": 1,
            "Pulls Allowed": 3,
            "Pulls Left": 3,
            "Round Points": 0,
            "Total Points": 0,
            "Target Score": 100
        }

        self.OwnedUpgrades = set() #For upgrades
        self.State = "In Round"

    def SetTarget(self): #Calculates the required target score based off rounds to increase difficulty
        self.PlayerStats["Target Score"] = 100 + (self.PlayerStats["Round"] - 1) * 50

    def PullLever(self, Points): #Handles every level pull turn and deducts # of pulls as each round passes
        if self.State == "In Round":
            if self.PlayerStats["Pulls Left"] > 0:
                self.PlayerStats["Round Points"] += Points
                self.PlayerStats["Total Points"] += Points
                self.PlayerStats["Pulls Left"] -= 1
                self.CheckSurvival()

    def CheckSurvival(self): #Compare earned points with target score and determine if player survived that round
        if self.State == "In Round":
            if self.PlayerStats["Pulls Left"] == 0:
                if self.PlayerStats["Round Points"] >= self.PlayerStats["Target Score"]:
                    self.State = "Pick Upgrade"
                else:
                    self.State = "Run Ended"

    def NextRound(self): #Advance to next round with correct # of pulls left and reset round points
        if self.State == "Pick Upgrade":
            self.PlayerStats["Round"] += 1
            self.PlayerStats["Round Points"] = 0
            self.PlayerStats["Pulls Left"] = self.PlayerStats["Pulls Allowed"]
            self.SetTarget()
            self.State = "In Round"
