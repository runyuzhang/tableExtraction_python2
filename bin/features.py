from grid import Grid
from grid import Cell
import parse
import collections
import json
from difflib import SequenceMatcher
from sklearn import svm
import sys

class FeatureVectorGenerator:
	def __init__(self, tableGrid, featureListFileName = "../data/feature_list.json"):

		with open(featureListFileName) as data_file:
			self.featuresMap = json.load(data_file, object_pairs_hook=collections.OrderedDict)
		self.grid = tableGrid

	def generateFeatureVector(self, c1, c2):
		featureVector = self.generateFeatureVectorMap(c1, c2).values()
		ret = []
		for f in featureVector:
			if type(f) == type([]):
				ret += f
			else:
				ret += [f]
		return ret

	def generateFeatureVectorMap(self, c1, c2):
		featuresVectorMap = collections.OrderedDict()
		for feature in self.featuresMap:
			if self.featuresMap[feature] == 1:
				featuresVectorMap[feature] = globals()[feature](c1,c2,self.grid)
		return featuresVectorMap



def contentSimilarityCase(c1, c2, grid):
    return SequenceMatcher(None, c1.content, c2.content).ratio()

# def contentSimilarityCaseIn(c1, c2, grid):
#     return SequenceMatcher(None, c1.content.lower(), c2.content.lower()).ratio()

def get_bigrams(string):
    '''
    Takes a string and returns a list of bigrams
    '''
    s = string.lower()
    return [s[i:i+2] for i in range(len(s) - 1)]

def contentSimilarityCaseIn(c1, c2, g):
    '''
    Perform bigram comparison between two strings
    and return a percentage match in decimal form
    '''
    
    # str1 = c1.content.decode('utf8')
    # str2 = c2.content.decode('utf8')
    str1 = c1.content
    str2 = c2.content
    if str1 == "" and str2 == "":
    	return 1
    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    union  = len(pairs1) + len(pairs2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    try:
    	return (2.0 * hit_count) / union
    except:
    	return SequenceMatcher(None, c1.content, c2.content).ratio()


"""
c1 spans vertically over c2 if c2 is one row below c2 and c2 is contained in c1 horizontally
return 1 if c1 spans over c2, -1 if c2 spans over c1, 0 otherwise

"""
def verticallySpanned(c1, c2, g):
	c2_one_row_below = (c1.startRow + c1.rowSpan == c2.startRow)
	c1_one_row_below = (c2.startRow + c2.rowSpan == c1.startRow)
	# c1_contains_c2 = (c1.startCol <= c2.startCol and c1.startCol + c1.colSpan > c2.startCol + c2.colSpan)
	# c2_contains_c1 = (c2.startCol <= c1.startCol and c2.startCol + c2.colSpan > c1.startCol + c1.colSpan)
	c1_contains_c2 = c1.startCol <= c2.startCol < c2.startCol + c2.colSpan <= c1.startCol + c1.colSpan and c1.colSpan > c2.colSpan
	c2_contains_c1 = c2.startCol <= c1.startCol < c1.startCol + c1.colSpan <= c2.startCol + c2.colSpan and c2.colSpan > c1.colSpan

	if c2_one_row_below and c1_contains_c2:
		return 1
	if c1_one_row_below and c2_contains_c1:
		return -1
	return 0

"""
c1 spans horizontally over c2 if c2 is one column right to c1, and c2 is contained in c2 vertically
return 1 if c1 spans over c2, -1 if c2 spans over c1, 0 otherwise
"""
def horizontallySpanned(c1, c2, g):
	c2_one_col_right = (c1.startCol + c1.colSpan == c2.startCol)
	c1_one_col_right = (c2.startCol + c2.colSpan == c1.startCol)
	# c1_contains_c2 = (c1.startRow <= c2.startRow and c1.startRow + c1.rowSpan >= c2.startRow + c2.rowSpan)
	# c2_contains_c1 = (c2.startRow <= c1.startRow and c2.startRow + c2.rowSpan >= c1.startRow + c1.rowSpan)
	c1_contains_c2 = c1.startRow <= c2.startRow < c2.startRow + c2.rowSpan <= c1.startRow + c1.rowSpan and c1.rowSpan > c2.rowSpan
	c2_contains_c1 = c2.startRow <= c1.startRow < c1.startRow + c1.rowSpan <= c2.startRow + c2.rowSpan and c2.rowSpan > c1.rowSpan
	if c2_one_col_right and c1_contains_c2:
		return 1
	if c1_one_col_right and c2_contains_c1:
		return -1
	return 0

"""
return 1 if c2 is below c1, -1 if c1 is below c2, 0 if they overlap vertically
"""
def relativeVerticalPosition(c1, c2, g):
	if c2.startRow >= c1.startRow + c1.rowSpan:
		return 1
	if c1.startRow >= c2.startRow + c2.rowSpan:
		return -1
	return 0

"""
return 1 if c2 is right to c1, -1 if c1 is right to c2, 0 if they overlap 
"""
def relativeHorizontalPosition(c1, c2, g):
	if c2.startCol >= c1.startCol + c1.colSpan:
		return 1
	if c1.startCol >= c2.startCol + c2.colSpan:
		return -1
	return 0



"""
return 0 if c1 and c2 are not column headers
returns 1 if c2 is below c1 and the row which contains c1 excluding c1 is empty,
0 if both rows are non-empty, -1 if c1 is below c2 and the row which contains c2 excluding e2 is empty
"""
def belowEmptyRow(c1, c2, g):
	if c1.function == Cell.COL_HEADER_CELL and c2.function == Cell.COL_HEADER_CELL:
		relativePosition = relativeVerticalPosition(c1,c2, g)
		if relativePosition == 1:
			flag, i = True, 0
			c1Row = g.getRow(c1.startRow)
			while flag and i < c1.rowSpan:
				flag = g.getNonEmptyCellsCountInRow(c1.startRow + i) == 1
				i += 1

			if flag: 
				return 1
		elif relativePosition == -1:
			flag, i = True, 0
			c2Row = g.getRow(c2.startRow)
			while flag and i < c2.rowSpan:
				flag = g.getNonEmptyCellsCountInRow(c2.startRow + i) == 1
				i += 1
			if flag: 
				return -1
	return 0

"""
returns 1 if c1 is above c2 and the row which contains c2 excluding c2 is empty,
0 if both rows are non-empty, -1 if c2 is above c1 and the row which contains c1 excluding e1 is empty
"""
def aboveEmptyRow(c1, c2, g):
	if c1.function == Cell.COL_HEADER_CELL and c2.function == Cell.COL_HEADER_CELL:
		relativePosition = relativeVerticalPosition(c1,c2, g)
		if relativePosition == 1:
			flag, i = True, 0
			c2Row = g.getRow(c2.startRow)
			while flag and i < c2.rowSpan:
				flag = g.getNonEmptyCellsCountInRow(c2.startRow + i) == 1
				i += 1

			if flag: 
				return 1
		elif relativePosition == -1:
			flag, i = True, 0
			c1Row = g.getRow(c1.startRow)
			while flag and i < c1.rowSpan:
				flag = g.getNonEmptyCellsCountInRow(c1.startRow + i) == 1
				i += 1
			if flag: 
				return -1
	return 0



"""
return a vector of binary values indicating c1 and c2's functions
"""
def injectFunctions(c1, c2, g):
	functionVector = [0] * 8
	functionVector[0] = 1 if c1.isStub() else 0
	functionVector[1] = 1 if c1.isRowHeader() else 0
	functionVector[2] = 1 if c1.isColHeader() else 0
	functionVector[3] = 1 if c1.isData() else 0
	functionVector[4] = 1 if c2.isStub() else 0
	functionVector[5] = 1 if c2.isRowHeader() else 0
	functionVector[6] = 1 if c2.isColHeader() else 0
	functionVector[7] = 1 if c2.isData() else 0
	return functionVector

"""
return 1 if c1 and c2 are spanned by the same cell, 0 if not
"""
def spannedBySameCell(c1, c2, g):
	#check vertical spanning
	if c1.startRow == 0 and c2.startRow == 0 and c1.function != Cell.STUB_CELL and c2.function != Cell.STUB_CELL:
		return 1
	if c1.startRow > 0 and c1.startRow == c2.startRow:
		c3 = g.getCell(c1.startRow - 1, c1.startCol)
		c4 = g.getCell(c2.startRow - 1, c2.startCol)
		if verticallySpanned(c3, c1, g) == 1 and verticallySpanned(c4, c2, g) == 1 and c3 == c4:
			return 1
	#check horizontal spanning
	if c1.startCol == 0 and c2.startCol == 0 and c1.function != Cell.STUB_CELL and c2.function != Cell.STUB_CELL:
		return 1
	if c1.startCol > 0 and c1.startCol == c2.startCol:
		c3 = g.getCell(c1.startRow, c1.startCol - 1)
		c4 = g.getCell(c2.startRow, c2.startCol - 1)
		if horizontallySpanned(c3, c1, g) == 1 and horizontallySpanned(c4, c2, g) == 1 and c3 == c4:
			return 1
	return 0

"""
return 1 if stub cell is empty, 0 otherwise
"""
def emptyStubCell(c1, c2, g):
	return 1 if g.stubCell.isEmptyCell() else 0

"""
return 1 if c1 and c2 are spanning over the same column(s), 0 otherwise
"""
def sameColumn(c1, c2, g):
	if c1.startCol == c2.startCol and c1.colSpan == c2.colSpan:
		return 1
	return 0

"""
return 1 if c1 and c2 are spanning over the same row(s), 0 otherwise
"""
def sameRow(c1, c2, g):
	if c1.startRow == c2.startRow and c1.rowSpan == c2.rowSpan:
		return 1
	return 0



"""
return 1 if c1's content repeats in another cell in the same row/column, -1 if c2's content repeats in another cell in the same row/column, 0 otherwise
"""
def recurringCell(c1, c2, g):
	def helper(c, g):
		for i in range(g.numRows):
			d = g.getCell(i, c.startCol)
			if d != c and d.content == c.content:
				return 1
		for j in range(g.numCols):
			d = g.getCell(c.startRow, j)
			if d != c and d.content == c.content:
				return 1
		return 0
	if helper(c1, g): 
		return 1
	elif helper(c2, g):
		return -1
	return 0

"""
return a length 4 binary vector that represenst the relative indentation of c1 and c2
"""

def indentation(c1, c2, g):
	if sameColumn(c1, c2, g) != 1:
		return [0,0,0,1]
	else:
		if c1.content.lower() == "total" or c2.content.lower() == "total":
			return [0,0,1,0]

		if c1.x1 < c2.x1:
			return [1,0,0,0]
		elif c1.x1 > c2.x1:
			return [0,1,0,0]
		else:
			return [0,0,1,0]

"""
return 1 if two cells have the same dimension, 0 otherwise
"""
def sameDimension(c1, c2, g):
	if c1.colSpan == c2.colSpan and c1.rowSpan == c2.rowSpan:
		return 1
	return 0

def contextualStructure(c1, c2, g):
	def helper(c1, c2, g):
		up_l = 0
		up_r = 0
		up_s = 0
		up_u = 0
		down_l = 0
		down_r = 0
		down_s = 0
		down_u = 0
		left_l = 0
		left_r = 0
		left_s = 0
		left_u = 0
		right_l = 0
		right_r = 0
		right_s = 0
		right_u = 0	

		if c1.startRow > 0:
			for i in range(c1.startCol, c1.startCol + c1.colSpan):
				seen = set()
				seen.add(c2)
				c_up = g.getCell(c1.startRow - 1, i)
				if not c_up in seen:
					if g.isSuperior(c1, c_up):
						up_l = 1
					elif g.isInferior(c1, c_up):
						up_r = 1
					elif g.isSibling(c1, c_up):
						up_s = 1
					else:
						up_u = 1
				seen.add(c_up)

		if c1.startRow + c1.rowSpan <= g.numRows:
			for i in range(c1.startCol, c1.startCol + c1.colSpan):
				seen = set()
				seen.add(c2)				
				c_down = g.getCell(c1.startRow + c1.rowSpan, i)
				if not c_down in seen:
					if g.isSuperior(c1, c_down):
						down_l = 1
					elif g.isInferior(c1, c_down):
						down_r = 1
					elif g.isSibling(c1, c_down):
						down_s = 1
					else:
						down_u = 1
				seen.add(c_down)

		if c1.startCol > 0:
			for i in range(c1.startRow, c1.startRow + c1.rowSpan):
				seen = set()
				seen.add(c2)
				c_left = g.getCell(i, c1.startCol - 1)
				if not c_left in seen:
					if g.isSuperior(c1, c_left):
						left_l = 1
					elif g.isInferior(c1, c_left):
						left_r = 1
					elif g.isSibling(c1, c_left):
						left_s = 1
					else:
						left_u = 1
				seen.add(c_left)
		if c1.startCol + c1.colSpan <= g.numCols:
			for i in range(c1.startRow, c1.startRow + c1.rowSpan):
				seen = set()
				seen.add(c2)
				c_right = g.getCell(i, c1.startCol + c1.colSpan)
				if not c_right in seen:
					if g.isSuperior(c1, c_right):
						left_l = 1
					elif g.isInferior(c1, c_right):
						left_r = 1
					elif g.isSibling(c1, c_right):
						left_s = 1
					else:
						left_u = 1
		print([up_l, up_r, up_s, up_u,down_l, down_r, down_s, down_u,left_l, left_r, left_s, left_u, right_l, right_r, right_s, right_u])
		return [up_l, up_r, up_s, up_u,down_l, down_r, down_s, down_u,left_l, left_r, left_s, left_u, right_l, right_r, right_s, right_u]

	return helper(c1, c2, g) + helper(c2, c1, g)






