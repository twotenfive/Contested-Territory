from tiles import tile

def upload(wks, tile, row):
    row = str(row)
    wks.update_value("B"+row, tile.id)
    wks.update_value("C"+row, tile.type)
    wks.update_value("D"+row, tile.relicname)
    wks.update_value("E"+row, tile.status)
    wks.update_value("F"+row, tile.score)
    wks.update_value("G"+row, tile.expiry)
    wks.update_value("I"+row, tile.owner)

def download(wks, row):
    row = str(row)
    fetchedTile = tile(wks.get_value('B'+row), wks.get_value('C'+row), wks.get_value('D'+row), wks.get_value('E'+row), wks.get_value('I'+row), wks.get_value('F'+row), wks.get_value('G'+row),"")
    return fetchedTile