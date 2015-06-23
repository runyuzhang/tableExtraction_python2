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

parser = optparse.OptionParser()
parser.add_option('-f', '--fileID', dest = "fileID", help='file index')
parser.add_option('-t', '--tableID', dest = "tableID", help='table index')
parser.add_option('-d', '--dataset', dest = "dataset", help='eu or us dataset')
parser.add_option('-g', '--persistedModel', dest = "persistedModel", help='persisted model')
(options, args) = parser.parse_args()

Cell.switchToIDRepr()

clf = joblib.load(options.persistedModel)


tableGrid = parse(options.fileID, options.dataset,readFunction = True, readStructure = False)[int(options.tableID)]

fvg = FeatureVectorGenerator(tableGrid)

stubCell = tableGrid.getStubCell()

explored = set()


def predict(c1, c2):
	global fvg
	print(clf.predict_proba(fvg.generateFeatureVector(c1, c2)))
	return clf.predict(fvg.generateFeatureVector(c1, c2))[0]


def explore(tableGrid, c1, direction, x1, x2, y1, y2, parent):
	print(c1.cellID, x1, x2, y1, y2, direction, parent)
	global exploredWindow
	global explored
	global stubCell



	exploredWindow[c1] = (x1, x2, y1, y2)

	# print(exploredWindow)	

	if direction == "v" and x1 < x2:
		j = y1
		i = x1
		while j < y2:
			c2 = tableGrid.getCell(i,j)
			j += c2.colSpan
			if not c2 in exploredWindow:
				if not c1.isEmptyCell():
					l = predict(c1, c2)
					print(c1, c2, l)
					if l == "L":
						c1.addChild(c2)
					elif l == "R" or l == "U":
						print("wtf")
						ct = c1.parentList[0] if c2.parentList else None
						while ct != None and predict(ct, c2) != "S":
							ct = ct.parentList[0]
						if ct and len(ct.parentList) != 0:
							ct.parentList[0].addChild(c2)
						elif not stubCell.isEmptyCell() and c2.function == Cell.COL_HEADER_CELL:
							print(c2.function, c2)
							stubCell.addChild(c2)
					elif l == "S":
						if len(c1.parentList) != 0:
							c1.parentList[0].addChild(c2)
				explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c1.startCol + c1.colSpan, exploredWindow[c2.parentList[0] if c2.parentList else None][3], c1)
				explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, exploredWindow[c2.parentList[0] if c2.parentList else None][1], c2.startCol, c2.startCol + c2.colSpan, c1)

			else:
				print("visited", c2)

	elif direction == "h" and y1 < y2:

		j = y1
		i = x1


		while i < x2:
			c2 = tableGrid.getCell(i,j)
			i += c2.rowSpan
			if not c2 in exploredWindow:
				# explored.add(c2)
				if not c1.isEmptyCell():

					l = predict(c1, c2)
					print(c1, c2, l)
					if l == "L":
						c1.addChild(c2)
					elif l == "R" or l == "U":
						print("wtf")
						ct = c1.parentList[0] if c2.parentList else None
						while ct != None and predict(ct, c2) != "S":
							ct = ct.parentList[0]
						if ct and len(ct.parentList) != 0:
							ct.parentList[0].addChild(c2)
						elif not stubCell.isEmptyCell() and c2.function == Cell.COL_HEADER_CELL:
							print(c2.function, c2)
							stubCell.addChild(c2)
					elif l == "S":
						if len(c1.parentList) != 0:
							c1.parentList[0].addChild(c2)
				explore(tableGrid, c2, "v", c2.startRow + c2.rowSpan, exploredWindow[c2.parentList[0] if c2.parentList else None][1], c2.startCol, c2.startCol + c2.colSpan, c1)
				explore(tableGrid, c2, "h", c2.startRow, c2.startRow + c2.rowSpan, c2.startCol + c2.colSpan, exploredWindow[c2.parentList[0] if c2.parentList else None][3], c1)
			else:
				print("visited", c2)


exploredWindow = dict()
exploredWindow[None] = (stubCell.startRow + stubCell.rowSpan, tableGrid.numRows, stubCell.startCol, stubCell.startCol + stubCell.colSpan)

explore(tableGrid, stubCell, "v", stubCell.startRow + stubCell.rowSpan, tableGrid.numRows, stubCell.startCol, stubCell.startCol + stubCell.colSpan, None)

exploredWindow = dict()
exploredWindow[None] = (stubCell.startRow, stubCell.startRow + stubCell.rowSpan, stubCell.startCol + stubCell.colSpan, tableGrid.numCols)

explore(tableGrid, stubCell, "h", stubCell.startRow, stubCell.startRow + stubCell.rowSpan, stubCell.startCol + stubCell.colSpan, tableGrid.numCols, None)



	






#find stub area