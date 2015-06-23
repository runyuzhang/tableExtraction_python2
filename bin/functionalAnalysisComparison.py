import glob, os, json
with open("lisha_tagging_us.json") as json_file:
    file_functionalInfo_lisha = json.load(json_file)
os.chdir("../data/us_function")
file_functionalInfo = {}




for file in glob.glob("*.txt"):
	file = open(str(file), "r")

	try:
		numTables = int(file.readline().strip())
	except:
		# print("SKIPPED" + str(file))
		continue
	table_functionalInfo = {}
	for tableID in range(numTables):
		file.readline()
		functionalInfo = {}
		stubCorner = file.readline().strip().split()[1:]
		stubCornerRow, stubCornerCol = int(stubCorner[0]), int(stubCorner[1])
		columnHeaders = file.readline().strip().split()[1:]
		rowHeaders = file.readline().strip().split()[1:]

	 	#converting to Lisha's format
		rowInc = -stubCornerRow
		colInc = -stubCornerCol
		end_row = rowInc + int(max(rowHeaders))
		end_col = colInc + int(max(columnHeaders))

		functionalInfo["rowInc"] = rowInc
		functionalInfo["colInc"] = colInc
		functionalInfo["endRow"] = end_row
		functionalInfo["endCol"] = end_col
		table_functionalInfo[tableID+1] = functionalInfo
		file.readline()
	file_functionalInfo[file.name.split("_function.txt")[0] + "-str.xml"] = table_functionalInfo

# for file in file_functionalInfo.keys():
# 	functionalInfo = file_functionalInfo[file]
# 	if file_functionalInfo_lisha[file] != file_functionalInfo[file]:
# 		print(file)
# 		print("***************LISHA***************")
# 		print(json.dumps(file_functionalInfo_lisha[file], indent = 4, sort_keys = True))
# 		print("***************JASON***************")
# 		print(json.dumps(file_functionalInfo[file], indent = 4, sort_keys = True))


print(json.dumps(file_functionalInfo, indent = 4, sort_keys = True))


