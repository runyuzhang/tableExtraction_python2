import json

lishaTaggingPtr = open("lisha_tagging_eu.json")
fileToTagging = json.load(lishaTaggingPtr)

for fileName in fileToTagging:
	tableIDToTagging = fileToTagging[fileName] 

	wf = open("../data/eu_function/" + fileName.split("-str")[0] + "_function.txt", "w")
	wf.write(str(len(tableIDToTagging)))
	wf.write("\n")
	for tableID in range(1, len(tableIDToTagging) + 1):
		wf.write(str(tableID))
		wf.write("\n")
		tagging = tableIDToTagging[str(tableID)]
		rowInc = tagging["rowInc"]
		colInc = tagging["colInc"]
		endRow = tagging["endRow"]
		endCol = tagging["endCol"]
		wf.write("S " + str(-rowInc) + " " + str(-colInc))
		wf.write("\n")
		wf.write("C " + " ".join(map(str, list(range(endCol + 1)))))
		wf.write("\n")
		wf.write("R " + " ".join(map(str, list(range(endRow + 1)))))
		wf.write("\n")
		wf.write("*")
		wf.write("\n")
