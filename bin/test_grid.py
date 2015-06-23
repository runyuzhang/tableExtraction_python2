import unittest
from grid import Grid
from grid import Cell
from grid import log

class TestGridMethods(unittest.TestCase):

    def test_constructor(self):
        log.info("TESTING CONSTRUCTOR WITH DIMENSIONS")
        a = Grid(2,3)
        self.assertEqual(a.grid, [[0,0,0], [0,0,0]])
        self.assertEqual(a.numRows,2)
        self.assertEqual(a.numCols,3)

    def test_expandTables(self):
        a = Grid()
        log.info("TESTING INSERTING ROW")
        a.insertRow(5)
        self.assertEqual(a.numRows, 6)
        self.assertEqual(a.grid, [[0], [0], [0], [0], [0], [0]])
        log.info("TESTING INSERTING COL")
        a.insertCol(2)
        self.assertEqual(a.grid, [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0]])

    def test_addCell(self):
        log.info("TESTING ADDING CELL")
        a = Grid(2,3)
        b = Cell(0,0,1,1,"HELLO", Cell.DATA_CELL)
        a.addCell(b)
        self.assertEqual(a.grid, [[b,0,0], [0,0,0]])

    def test_addSpanningCell(self):
        log.info("TESTING ADDING SPANNING CELL")
        a = Grid(3,4)
        b = Cell(1,1,2,2,"YO", Cell.DATA_CELL)
        a.addCell(b)
        self.assertEqual(a.grid, [[0,0,0,0],[0,b,b,0],[0,b,b,0]])
        log.info("TESTING ADDING SPANNING CELL THAT DOESNT FIT")
        a = Grid()
        b = Cell(1,1,2,2,"YO", Cell.DATA_CELL)
        a.addCell(b)
        self.assertEqual(a.grid, [[0,0,0],[0,b,b],[0,b,b]])
        a = Grid()

    def test_gridPrint(self):
        log.info("TESTING CELL PRINT")
        a = Cell(0,0,0,0, "123456789101112", Cell.DATA_CELL)
        self.assertEqual(str(a), "1234567...")
        log.info("TESTING GRID PRINT")
        a = Grid()
        self.assertEqual(str(a), "------------\n|          |\n------------\n")

if __name__ == '__main__':
    unittest.main()