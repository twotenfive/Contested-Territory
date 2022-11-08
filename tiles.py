import discord

class tile:
    def __init__(self, id, type, relicname, status, owner, score, expiry, memo):
        self.id = id
        self.type = type
        self.relicname = relicname
        self.status = status
        self.score = score
        self.owner = owner
        self.expiry = expiry
        self.memo = memo

    def return_embed(self):
        title = "Viewing details of Tile " + self.id
        typestr = "**Tile Type:** " + self.type
        if (self.type == "Relic"):
            typestr += " (:" + self.relicname + ":)"
        elif (self.type == "Banner"):
            typestr += " :banner:"

        statusstr = "**Tile Status:** "
        if (self.status != "Neutral"):
            statusstr += "Captured by " + self.owner
        else:
            statusstr += "Neutral"
        
        scorestr = "**Current Score:** " + self.score

        expirystr = "**Expires **" + self.expiry

        embed = discord.Embed(title=title, description = typestr + "\n" + statusstr + "\n" + scorestr + "\n" + expirystr)
        return embed

