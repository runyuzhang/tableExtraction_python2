import grid
from grid import log
from xml.dom import minidom

FILE_DIRECTORIES = {'us': {"xml" : "../data/us/",
"structure" : "../data/us_structure/",
"function" : "../data/us_function/"}, 'eu' :  {"xml" : "../data/eu/",
"structure" : "../data/eu_structure/",
"function" : "../data/eu_function/"}
}


def parse(fileIndex, dataset = 'us', cell_char_limit = 5, readFunction = True, readStructure = True, display = False):
	grid.log.disabled = True
	fileName = FILE_DIRECTORIES[dataset]['xml'] + dataset + '-' + fileIndex + "-str.xml"
	grid.log.info("Parsing " + fileName)

	grid.Cell.CELL_CHAR_LIMIT = cell_char_limit

	xmldoc = minidom.parse(fileName)

	tableList = xmldoc.getElementsByTagName("table")

	id_grid_map = {}

	for table in tableList:

		xmlGrid = grid.Grid()
		region = table.getElementsByTagName('region')[0]

		cellList = table.getElementsByTagName('cell')
	
		for i, cellElem in enumerate(cellList):
			startRow = int(cellElem.attributes.get('start-row', 0).value) 
			startCol = int(cellElem.attributes.get('start-col', 0).value) 
			rowSpan = cellElem.attributes.get('end-row', -1)
			if rowSpan == -1:
				rowSpan = 1
			else:
				rowSpan = int(rowSpan.value) - startRow + 1
			colSpan = cellElem.attributes.get('end-col', -1)
			if colSpan == -1:
				colSpan = 1
			else:
				colSpan = int(colSpan.value) - startCol + 1

			x1 = int(cellElem.getElementsByTagName("bounding-box")[0].attributes.get('x1').value)
			y1 = int(cellElem.getElementsByTagName("bounding-box")[0].attributes.get('y1').value)
			x2 = int(cellElem.getElementsByTagName("bounding-box")[0].attributes.get('x2').value)
			y2 = int(cellElem.getElementsByTagName("bounding-box")[0].attributes.get('y2').value)

			content = cellElem.getElementsByTagName("content")[0].firstChild.data.replace("\n", " ")

			function = grid.Cell.DATA_CELL
			xmlGrid.addCell(grid.Cell(startRow, startCol, rowSpan, colSpan, x1, x2, y1, y2, content, function, i))

		id_grid_map[int(table.attributes.get("id").value)] = xmlGrid

		if display:
			grid.Cell.switchToContentRepr()
			print(xmlGrid)
			grid.Cell.switchToIDRepr()
			print(xmlGrid)


	
	if (readFunction):
		functionFileName = FILE_DIRECTORIES[dataset]['function'] + dataset + '-' + fileIndex + "_function.txt"
		
		#read functional tagging

		log.info("READING FUNCTIONAL TAGGING FROM" + functionFileName)

		functionalFilePtr = open(functionFileName)
		numGrids = int(functionalFilePtr.readline())

		for i in range(1, numGrids+1):
			functionalFilePtr.readline()
			stubCorner = functionalFilePtr.readline().strip().split()[1:]
			stubCornerRow, stubCornerCol = int(stubCorner[0]), int(stubCorner[1])
			stubCell = id_grid_map[i].getCell(stubCornerRow, stubCornerCol)
			stubCell.function = grid.Cell.STUB_CELL

			id_grid_map[i].stubCell = stubCell

			id_grid_map[i].stubRow = stubCornerRow
			id_grid_map[i].stubCol = stubCornerCol

			columnHeaders = functionalFilePtr.readline().strip().split()[1:]
			for column in columnHeaders:
				column = int(column)
				for j in range(stubCornerRow + 1, id_grid_map[i].numRows):
					cell = id_grid_map[i].getCell(j, column)
					if cell != grid.Cell.EMPTY_CELL and cell != stubCell:
						cell.function = grid.Cell.COL_HEADER_CELL
			rowHeaders = functionalFilePtr.readline().strip().split()[1:]
			for row in rowHeaders:
				row = int(row)
				for k in range(stubCornerCol + 1, id_grid_map[i].numCols):
					cell = id_grid_map[i].getCell(row, k)
					if cell != grid.Cell.EMPTY_CELL and cell != stubCell:	
						cell.function = grid.Cell.ROW_HEADER_CELL
			functionalFilePtr.readline()

		functionalFilePtr.close()

	if (readStructure):

		structureFileName = FILE_DIRECTORIES[dataset]['structure'] + dataset + '-' + fileIndex + "_structure.txt"
		#read structural tagging
		
		log.info("READING STRUCTURAL TAGGING FROM" + structureFileName)

		structuralFilePtr = open(structureFileName)
		numGrids = int(structuralFilePtr.readline())
		for i in range(1, numGrids+1):
			line = structuralFilePtr.readline().strip()
			while (line[0] != "*"):
				parentID, childrenIDList = line[0], line[1:]
				parent = id_grid_map[i].getCellByCellID(int(parentID))
				for childID in childrenIDList:
					child = id_grid_map[i].getCellByCellID(int(childID))
					parent.addChild(child)
					child.addParent(parent)
				line = structuralFilePtr.readline().strip().split()

		structuralFilePtr.close()

	return id_grid_map





