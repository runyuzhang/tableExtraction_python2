from features import FeatureVectorGenerator
from grid import Grid
from grid import Cell
from grid import log
from parse import parse
from sklearn.externals import joblib
from sklearn import svm
from sklearn import linear_model
import pickle
import sys, optparse
from pprint import pprint

parser = optparse.OptionParser()
parser.add_option('-f', '--fileID', dest = "fileID", help='file index')
parser.add_option('-t', '--tableID', dest = "tableID", help='table index')
parser.add_option('-d', '--dataset', dest = "dataset", help='eu or us dataset')
parser.add_option('-g', '--persistedModel', dest = "persistedModel", help='persisted model')
parser.add_option('-a', '--all', action = "store_true", help='construct all')
(options, args) = parser.parse_args()

Cell.switchToIDRepr()

clf = joblib.load(options.persistedModel)


def construct(tableGrid):

	fvg = FeatureVectorGenerator(tableGrid)

	stubCell = tableGrid.getStubCell()

	pprint(vars(stubCell))

	explored = set()


	def predict(c1, c2):
		nonlocal fvg
		print(clf.predict_proba(fvg.generateFeatureVector(c1, c2)))
		return clf.predict(fvg.generateFeatureVector(c1, c2))[0]

	def explore(tableGrid, c1, direction, x1, x2, y1, y2, parent, mode):
		nonlocal exploredWindow
		nonlocal stubCell

		print(c1, direction, x1, x2, y1, y2, parent, mode)
		exploredWindow[c1] = (x1, x2, y1, y2)

		# # print(exploredWindow)	

		if direction == "v" and x1 < x2:
			j = y1
			i = x1
			while j < y2:
				print(i,j)
				c2 = tableGrid.getCell(i,j)
				if c2.isEmptyCell() and i < x2:
					i += 1
					continue
				j += c2.colSpan
				if not c2 in exploredWindow:
					if not c1.isEmptyCell():
						l = predict(c1, c2)
						print(c1, c2, l)
						if l == "L":
							c1.addChild(c2)
						elif l == "U":
							ct = c1.parentList[0]
							while ct and predict(ct, c2) != "S":
								# print("CT", ct)
								ct = ct.parentList[0]
							# print("CT", ct)
							if ct and ct.parentList[0]:
								ct.parentList[0].addChild(c2)
							elif not stubCell.isEmptyCell() and c2.function == Cell.COL_HEADER_CELL:
								# print(c2.function, c2)
								stubCell.addChild(c2)
						elif l == "S":
							print(c1.parentList)
							if c1.parentList[0]:
								c1.parentList[0].addChild(c2)

					if mode == "column":			
						explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c2.startCol + c2.colSpan, min(exploredWindow[c2.parentList[0]][3], exploredWindow[stubCell if not stubCell.isEmptyCell() else None][3]), c1, mode)
						explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, min(exploredWindow[c1.parentList[0]][1],exploredWindow[stubCell if not stubCell.isEmptyCell() else None][1]), c2.startCol, min(c2.startCol + c2.colSpan, exploredWindow[stubCell if not stubCell.isEmptyCell() else None][3]), c1, mode)

					elif mode == "row":
						explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c2.startCol + c2.colSpan, exploredWindow[c2.parentList[0]][3], c1, mode)
						explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, exploredWindow[stubCell if not stubCell.isEmptyCell() else None][1], c2.startCol, c2.startCol + c2.colSpan, c1, mode)

				# else:
					# print("visited", c2)

		elif direction == "h" and y1 < y2:

			j = y1
			i = x1

			while i < x2:
				c2 = tableGrid.getCell(i,j)
				i += c2.rowSpan
				if c2.isEmptyCell():
					j += 1
					continue
				if not c2 in exploredWindow:
					if not c1.isEmptyCell():
						l = predict(c1, c2)
						print(c1, c2, l)
						if l == "L":
							c1.addChild(c2)
						elif l == "U":
							ct = c1.parentList[0]
							while ct and predict(ct, c2) != "S":
								# print("CT", ct)
								ct = ct.parentList[0]
							# print("CT", ct)
							if ct and ct.parentList[0]:
								ct.parentList[0].addChild(c2)
							elif not stubCell.isEmptyCell() and c2.function == Cell.COL_HEADER_CELL:
								# print(c2.function, c2)
								stubCell.addChild(c2)
						elif l == "S":
							print(c1.parentList)
							if c1.parentList[0]:
								c1.parentList[0].addChild(c2)
					if mode == "column":
						explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, min(exploredWindow[c1.parentList[0]][1],exploredWindow[stubCell if not stubCell.isEmptyCell() else None][1]), c2.startCol, min(c2.startCol + c2.colSpan, exploredWindow[stubCell if not stubCell.isEmptyCell() else None][3]), c1, mode)
						explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c2.startCol + c2.colSpan, min(exploredWindow[c2.parentList[0]][3], exploredWindow[stubCell if not stubCell.isEmptyCell() else None][3]), c1, mode)
				
					elif mode == "row":
						explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, exploredWindow[stubCell if not stubCell.isEmptyCell() else None][1], c2.startCol, c2.startCol + c2.colSpan, c1, mode)
						explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c2.startCol + c2.colSpan, exploredWindow[c2.parentList[0]][3], c1, mode)


				# else:
					# print("visited", c2)


	exploredWindow = dict()
	exploredWindow[None] = (stubCell.startRow + stubCell.rowSpan, tableGrid.numRows, stubCell.startCol, stubCell.startCol + stubCell.colSpan)

	explore(tableGrid, stubCell, "v", stubCell.startRow + stubCell.rowSpan, tableGrid.numRows, stubCell.startCol, stubCell.startCol + stubCell.colSpan, None, "column")

	# return tableGrid

	exploredWindow = dict()
	exploredWindow[None] = (stubCell.startRow, stubCell.startRow + stubCell.rowSpan, stubCell.startCol + stubCell.colSpan, tableGrid.numCols)

	explore(tableGrid, stubCell, "h", stubCell.startRow, stubCell.startRow + stubCell.rowSpan, stubCell.startCol + stubCell.colSpan, tableGrid.numCols, None, "row")


	return tableGrid
#validate





def validate(tableGrid, tableGrid_truth, fileID, tableGridID):
	global options
	global total
	global correct
	global wrongTables

	idCellMap = tableGrid.idCellMap
	for c1_id in range(len(idCellMap.keys())):
			for c2_id in range(c1_id+1, len(idCellMap.keys())):
				c1 = tableGrid.getCellByCellID(c1_id)
				c2 = tableGrid.getCellByCellID(c2_id)

				c1_truth = tableGrid_truth.getCellByCellID(c1_id)
				c2_truth = tableGrid_truth.getCellByCellID(c2_id)

				if (not c1.isData()) and (not c2.isData()):
					total += 1

					prediction = tableGrid.classify(c1,c2)
					groundTruth = tableGrid_truth.classify(c1_truth, c2_truth)

					if prediction == groundTruth:
						correct += 1
					else:
						# wrongTables += [(fileID, tableGridID)]
						# return
						print(fileID, tableGridID, c1.cellID, c2.cellID, groundTruth, prediction)


total = 0
correct = 0
wrongTables = []



fileList = []
filesListPtr = open("training_files_" + options.dataset + ".txt")
line = filesListPtr.readline()
while line:
	fileList += [line.strip()]
	line = filesListPtr.readline()

if options.all:
	for file in fileList:
		grids = parse(file, dataset = options.dataset, readFunction = True, readStructure = False)
		grids_truth = parse(file, dataset = options.dataset, readFunction = True, readStructure = True)
		for tableGridID in grids.keys():
			validate(construct(grids[tableGridID]), grids_truth[tableGridID], file, tableGridID)

else:
	grid_test = construct(parse(options.fileID, dataset = options.dataset, readFunction = True, readStructure = False)[int(options.tableID)])
	grid_truth = parse(options.fileID, dataset = options.dataset, readFunction = True, readStructure = True)[int(options.tableID)]
	
	validate(grid_test, grid_truth, options.fileID, options.tableID)


print(correct / total)
# print(len(wrongTables))
# print(wrongTables)





#find stub area