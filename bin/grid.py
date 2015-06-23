import logging
import sys
log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)
# log.disabled = True


class Cell:
	EMPTY_CELL = "E"
	DATA_CELL = "D"
	COL_HEADER_CELL = "CH"
	ROW_HEADER_CELL = "RH"
	STUB_CELL = "S"
	CELL_CHAR_LIMIT = 5
	EMPTY_REPR = " "*CELL_CHAR_LIMIT
	CELL_ID_REPR = False

	def __init__(self, startRow = 0, startCol = 0, rowSpan = 0, colSpan = 0,x1 = 0, x2 = 0, y1 = 0, y2 = 0, content = "", function = DATA_CELL, cellID = 0):
		self.__startRow = startRow
		self.__startCol = startCol
		self.__rowSpan = rowSpan
		self.__colSpan = colSpan
		self.__content = content
		self.__function = function
		self.__cellID = cellID
		self.__parentList = []
		self.__childrenList = []
		self.__x1 = x1
		self.__x2 = x2
		self.__y1 = y1
		self.__y2 = y2

	@property
	def x1(self):
	    return self.__x1

	@property
	def x2(self):
	    return self.__x2

	@property
	def y1(self):
	    return self.__y1

	@property
	def y2(self):
	    return self.__y2

	@property
	def cellID(self):
	    return self.__cellID

	@property
	def startRow(self):
	    return self.__startRow

	@property
	def startCol(self):
	    return self.__startCol
	
	@property
	def rowSpan(self):
	    return self.__rowSpan

	@property
	def colSpan(self):
	    return self.__colSpan
	
	@property
	def content(self):
	    return self.__content
	@content.setter
	def content(self, value):
	    self.__content = value

	@property
	def function(self):
	    return self.__function
	@function.setter
	def function(self, value):
	    self.__function = value

	@property
	def parentList(self):
	    return self.__parentList

	@property
	def childrenList(self):
	    return self.__childrenList
	
	
	def isEmptyCell(cell):
		if type(cell) == type("") or cell.function == Cell.EMPTY_CELL or cell.cellID == -1:
			return True
		return False


	def __repr__(self):
		if Cell.isEmptyCell(self) == True:
			return Cell.CELL_CHAR_LIMIT * " "
		if Cell.CELL_ID_REPR:
			return str(self.cellID) + " " * (Cell.CELL_CHAR_LIMIT - len(str(self.cellID)))
		if len(self.content) > Cell.CELL_CHAR_LIMIT:
			return self.content[:Cell.CELL_CHAR_LIMIT-3] + "..."
		return self.content + " " * (Cell.CELL_CHAR_LIMIT - len(self.content))


	def onLeftCorner(self, row, col):
		return row == self.startRow and col == self.startCol

	def addChild(self, child):
		# print("HIT")
		self.__childrenList.append(child)
		child.addParent(self)

	def addParent(self,parent):
		self.__parentList.append(parent)

	def isStub(self):
		return self.function == Cell.STUB_CELL

	def isRowHeader(self):
		return self.function == Cell.ROW_HEADER_CELL

	def isColHeader(self):
		return self.function == Cell.COL_HEADER_CELL

	def isHeader(self):
		return self.isColHeader() or self.isRowHeader()

	def isData(self):
		return self.function == Cell.DATA_CELL

	def switchToContentRepr():
		Cell.CELL_ID_REPR = False
	def switchToIDRepr():
		Cell.CELL_ID_REPR = True



class Grid:
	VERT_BORDER_SOLID = "-" * (Cell.CELL_CHAR_LIMIT  + 1)
	VERT_BORDER_EMPTY = " " * (Cell.CELL_CHAR_LIMIT  + 1)
	HORI_BORDER_SOLID = "|"
	HORI_BORDER_EMPTY = " "
 



	def __init__(self, numRows = 1, numCols = 1):
		self._grid = [[Cell.EMPTY_CELL] * numCols for _ in range(numRows)]
		self.__idCellMap = dict()
		self.__stubCell = None
		self.__IDRepr = False
		self.__stubRow = 0
		self.__stubCol = 0





	@property
	def idCellMap(self):
	    return self.__idCellMap
	

	@property
	def stubCell(self):
	    return self.__stubCell
	@stubCell.setter
	def stubCell(self, cell):
	    self.__stubCell = cell
	

	@property
	def numRows(self):
	    return len(self._grid)
	@numRows.setter
	def numRows(self, value):
	    if value > self.numRows:
	    	self.insertRow(value)

	@property
	def numCols(self):
	    return len(self._grid[0])
	@numCols.setter
	def numCols(self, value):
	    if value > self.numCols:
	    	self.insertRow(value)

	@property
	def grid(self):
	    return self._grid
	@grid.setter
	def grid(self, value):
	    log.error("YOU CANT SET GRID")
	
	def addCell(self, cell):
		#if cell doesn't fit in current grid, insert extra rows and columns to accomodate
		if cell.startRow + cell.rowSpan > self.numRows:
			self.insertRow(cell.startRow + cell.rowSpan - 1)
		if cell.startCol + cell.colSpan > self.numCols:
			self.insertCol(cell.startCol + cell.colSpan - 1)
		for i in range(cell.startRow, cell.startRow + cell.rowSpan):
			for j in range(cell.startCol, cell.startCol + cell.colSpan):
				self.grid[i][j] = cell;
		self.__idCellMap[cell.cellID] = cell

	def getCellByCellID(self, cellID):
		return self.__idCellMap[cellID]

	#insert a row right at the indicated row number
	def insertRow(self, row):
		# log.info("INSERTING ROW AT %d", row)
		if row < self.numRows:
			self._grid.insert(row, [Cell.EMPTY_CELL for _ in range(self.numCols)])
		else:
			
			for i in range(self.numRows - 1, row):
				self._grid.append([Cell.EMPTY_CELL for _ in range(self.numCols)])

	#insert a row right at the indicated row number
	def insertCol(self, col):
		# log.info("INSERTING COL AT %d", col)
		if col < self.numCols:
			for gridRow in self._grid:
				gridRow.insert(col, Cell.EMPTY_CELL)
		else:
			for gridRow in self._grid:
				gridRow += [Cell.EMPTY_CELL for _ in range(col - len(gridRow) + 1)]


	def getCell(self, row, col):
		assert self.numRows > row and row >= 0, "row number doesn't exist"
		assert self.numCols > col and col >= 0, "col number doesn't exist"
		cell = self.grid[row][col]
		if Cell.isEmptyCell(cell):
	 		return Cell(startRow = row, startCol = col, rowSpan = 1, colSpan = 1, content = "", function = Cell.EMPTY_CELL, cellID = -1)
		return self.grid[row][col]

	def getRow(self, row):
		assert row < self.numRows and row >= 0, "row number doesn't exist"
		cellList = []
		currentCol = 0
		while currentCol < self.numCols:
			cell = self.getCell(row, currentCol)
			cellList += [cell]
			currentCol += cell.colSpan
		return cellList

	def getCol(self, col):
		assert col < self.numCols and col >= 0, "col number doesn't exist"
		cellList = []
		currentRow = 0
		while currentRow < self.numRows:
			cell = self.getCell(currentRow, col)
			cellList += [cell]
			currentRow += cell.rowSpan
		return cellList
	# def deleteRow(self, row):
	# 	assert row < self.numRows and row >= 0, "row number doesn't exist"
	# 	del self.grid[row]

	# def deleteCol(self, col):
	# 	assert col < self.numCols and col >= 0, "col number doesn't exist"
	# 	for i in range(self.numRows):
	# 		del self.grid[row][i]

	def __repr__(self):
		prettyPrint = ""
		for i in range(self.numRows):
			for j in range(self.numCols):
				cell = self.getCell(i,j)
				if Cell.isEmptyCell(cell) or cell.startRow == i:
					prettyPrint += Grid.VERT_BORDER_SOLID
				else:
					prettyPrint += Grid.VERT_BORDER_EMPTY
			prettyPrint += "\n"
			for j in range(self.numCols):
				cell = self.getCell(i,j)
				if Cell.isEmptyCell(cell) or cell.startCol == j:
					prettyPrint += Grid.HORI_BORDER_SOLID
				else:
					prettyPrint += Grid.HORI_BORDER_EMPTY
				if Cell.isEmptyCell(cell) or (not cell.onLeftCorner(i,j)):
					prettyPrint += Cell.EMPTY_REPR
				else:
					prettyPrint += str(cell)

				if j == self.numCols - 1:
					prettyPrint += Grid.HORI_BORDER_SOLID
			prettyPrint += "\n"
			if i == self.numRows - 1:
				prettyPrint += Grid.VERT_BORDER_SOLID * self.numCols
				prettyPrint += "\n"
		return prettyPrint

	def printInOrder(self, root):
		print(root.content)
		if len(root.childrenList) == 0:
			print()
			return
		for child in root.childrenList:
			print(root.content, end = "->")
			self.printInOrder(child) 

	def getNonEmptyCellsCountInRow(self, row):
		r = self.getRow(row)
		return sum([not x.isEmptyCell() for x in r])

	def getNonEmptyCellsCountInCol(self, col):
		c = self.getCol(col)
		return sum([not x.isEmptyCell() for x in c])

	def isSuperior(self, c1, c2):
		if c2 in c1.childrenList:
			return True
		for c in c1.childrenList:
			if self.isSuperior(c, c2):
				return True
		return False

	def isInferior(self, c1, c2):
		return self.isSuperior(c2, c1)

	def isSibling(self, c1, c2):
		if len(set(c1.parentList).intersection(set(c2.parentList))) > 0:
			return True
		elif c1.isRowHeader() and c2.isRowHeader() and len(c1.parentList) == 0 and len(c2.parentList) == 0:
			return True
		elif c1.isColHeader() and c2.isColHeader() and len(c1.parentList) == 0 and len(c2.parentList) == 0:
			return True
		return False

	def isUnrelated(self, c1, c2):
		return not(self.isSuperior(c1, c2) or self.isInferior(c1, c2) or self.isSibling(c1, c2))

	def getStubCell(self):
		if not self.stubCell.isEmptyCell():
			return self.stubCell
		else:
			rowSpan = 1
			colSpan = 1
			c = self.getCell(self.__stubRow + rowSpan, self.__stubCol)
			while c.isEmptyCell():
				rowSpan += 1
				c = self.getCell(rowSpan, colSpan)

			c = self.getCell(self.__stubRow, colSpan)
			while c.isEmptyCell():
				colSpan += 1
				c = self.getCell(1, colSpan)

			return Cell(self.__stubRow, self.__stubCol, rowSpan, colSpan, content = "", function = Cell.EMPTY_CELL)



	def classify(self, c1, c2):
		if self.isSuperior(c1, c2):
			return "L"
		if self.isInferior(c1, c2):
			return "R"
		if self.isSibling(c1, c2):
			return "S"
		return "U"

	def getTrainingData(self, method):
		if method == "Pairwise":
			for c1 in range(len(self.__idCellMap.keys())):
				for c2 in range(c1+1, len(self.__idCellMap.keys())):
					if self.isSuperior(self.getCellByCellID(c1), self.getCellByCellID(c2)):
						print(c1, c2, pairwiseLabels["leftSuperior"])
					elif self.isInferior(self.getCellByCellID(c1), self.getCellByCellID(c2)):
						print(c1, c2, pairwiseLabels["rightSuperior"])
					elif self.isSibling(self.getCellByCellID(c1), self.getCellByCellID(c2)):
						print(c1, c2, pairwiseLabels["siblings"])
					else:
						print(c1, c2, pairwiseLabels["Unrelated"])

pairwiseLabels = {"leftSuperior": "L",
				  "rightSuperior": "C",
				  "siblings": "S",
				  "Unrelated": "U"}





#utils
def printCellList(l):
	return " ".join(map(lambda x: str(x.cellID), l))

def uniqify(l):
	result = []
	seen = {}
	for item in l:
		if item in seen: continue
		seen[item] = 1
		result.append(item)
	return result









