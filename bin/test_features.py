import unittest
from grid import Grid
from grid import Cell
from features import FeatureVectorGenerator
from grid import log
import features
from parse import parse


class TestFeaturesMethods(unittest.TestCase):

    def test_spanned_by_same_cell(self):
        Cell.switchToContentRepr()
        log.info("Testing spanned by same cell")
        g = Grid()
        a = Cell(startRow = 1, startCol = 1, rowSpan = 3, colSpan = 5, content = "a")
        b = Cell(startRow = 4, startCol = 1, rowSpan = 1, colSpan = 3, content = "b")
        c = Cell(startRow = 2, startCol = 6, rowSpan = 1, colSpan = 1, content = "c")
        d = Cell(startRow = 4, startCol = 4, rowSpan = 1, colSpan = 1, content = "d")
        e = Cell(startRow = 1, startCol = 6, rowSpan = 2, colSpan = 1, content = "e")
        g.addCell(e)
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        Cell.switchToContentRepr()
        print(g)
        self.assertEqual(features.spannedBySameCell(b,d, g), 1)
        self.assertEqual(features.spannedBySameCell(c,e, g), 1)
        self.assertEqual(features.belowEmptyRow(a,b, g), 0)
        self.assertEqual(features.belowEmptyRow(c,b, g), 0)

    # def test_feature_vector_extraction(self):
    #     g = parse("001", "us")[1]
    #     f = FeatureVectorGenerator(g)
    #     a = f.grid.getCell(0,0)
    #     b = f.grid.getCell(0,2)
    #     c = f.grid.getCell(1,2)
    #     d = f.grid.getCell(2,0)
    #     print(f.grid)
    #     self.assertEqual(f.generateFeatureVector(a,b), [0,0,1,0,1,0,1,0,0,0,0,1,0,0, 0, 0])
    #     self.assertEqual(f.generateFeatureVector(b,c), [0,1,0,1,0,0,0,1,0,0,0,1,0,0, 0, 0])
    #     self.assertEqual(f.generateFeatureVector(a,d), [0.1,1,0,1,0,0,1,0,0,0,0,0,1,0, 0, 0])




    def test_below_empty_row(self):
        Cell.switchToContentRepr()
        log.info("Testing below empty row")
        g = Grid()
        a = Cell(startRow = 1, startCol = 1, rowSpan = 3, colSpan = 5, content = "a")
        b = Cell(startRow = 4, startCol = 1, rowSpan = 1, colSpan = 3, content = "b")
        c = Cell(startRow = 0, startCol = 0, rowSpan = 1, colSpan = 2, content = "c")
        d = Cell(startRow = 4, startCol = 4, rowSpan = 1, colSpan = 1, content = "d")
        e = Cell(startRow = 1, startCol = 0, rowSpan = 2, colSpan = 1, content = "e")
        g.addCell(e)
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        Cell.switchToContentRepr()
        print(g)
        self.assertEqual(features.belowEmptyRow(e,c, g), -1)
        self.assertEqual(features.belowEmptyRow(c,e, g), 1)
        self.assertEqual(features.belowEmptyRow(a,b, g), 0)
        self.assertEqual(features.belowEmptyRow(c,b, g), 1)



    def test_relative_vertical_position(self):
        Cell.switchToContentRepr()
        log.info("Testing relative vertical position")
        g = Grid()
        a = Cell(startRow = 1, startCol = 1, rowSpan = 3, colSpan = 5, content = "a")
        b = Cell(startRow = 4, startCol = 1, rowSpan = 1, colSpan = 3, content = "b")
        c = Cell(startRow = 0, startCol = 0, rowSpan = 1, colSpan = 2, content = "c")
        d = Cell(startRow = 4, startCol = 4, rowSpan = 1, colSpan = 1, content = "d")
        e = Cell(startRow = 1, startCol = 0, rowSpan = 2, colSpan = 1, content = "e")
        g.addCell(e)
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        print(g)
        self.assertEqual(features.relativeVerticalPosition(a,b, None), 1)
        self.assertEqual(features.relativeVerticalPosition(c,a, None), 1)
        self.assertEqual(features.relativeVerticalPosition(d,a, None), -1)
        self.assertEqual(features.relativeVerticalPosition(e,a, None), 0)


    def test_relative_horizontal_position(self):
        Cell.switchToContentRepr()
        log.info("Testing relative horizontal position")
        g = Grid()
        a = Cell(startRow = 1, startCol = 1, rowSpan = 3, colSpan = 3, content = "a")
        b = Cell(startRow = 4, startCol = 1, rowSpan = 1, colSpan = 3, content = "b")
        c = Cell(startRow = 0, startCol = 0, rowSpan = 1, colSpan = 2, content = "c")
        d = Cell(startRow = 4, startCol = 4, rowSpan = 1, colSpan = 1, content = "d")
        e = Cell(startRow = 1, startCol = 0, rowSpan = 2, colSpan = 1, content = "e")
        g.addCell(e)
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        print(g)
        self.assertEqual(features.relativeHorizontalPosition(c,a, None), 0)
        self.assertEqual(features.relativeHorizontalPosition(e,a, None), 1)
        self.assertEqual(features.relativeHorizontalPosition(a,b, None), 0)
        self.assertEqual(features.relativeHorizontalPosition(a,d, None), 1)
    
    def test_vertically_spanning(self):
        Cell.switchToContentRepr()
        log.info("Testing Vertically Spanned")
        g = Grid()
        a = Cell(startRow = 1, startCol = 1, rowSpan = 3, colSpan = 5, content = "a")
        b = Cell(startRow = 4, startCol = 1, rowSpan = 1, colSpan = 3, content = "b")
        c = Cell(startRow = 0, startCol = 0, rowSpan = 1, colSpan = 2, content = "c")
        d = Cell(startRow = 4, startCol = 4, rowSpan = 1, colSpan = 1, content = "d")
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        print(g)
        self.assertEqual(features.verticallySpanned(a,b, None), 1)
        self.assertEqual(features.verticallySpanned(b,a, None), -1)
        self.assertEqual(features.verticallySpanned(c,a, None), 0)
        self.assertEqual(features.verticallySpanned(b,c, None), 0)
        self.assertEqual(features.verticallySpanned(a,c, None), 0)
        self.assertEqual(features.verticallySpanned(a,d, None), 1)
        self.assertEqual(features.verticallySpanned(d,a, None), -1)

    def test_horizontally_spanning(self):
        log.info("Testing Horizontally Spanned")
        g = Grid()
        a = Cell(startRow = 1, startCol = 0, rowSpan = 3, colSpan = 2, content = "a")
        b = Cell(startRow = 3, startCol = 2, rowSpan = 1, colSpan = 1, content = "b")
        c = Cell(startRow = 1, startCol = 2, rowSpan = 2, colSpan = 1, content = "c")
        d = Cell(startRow = 1, startCol = 3, rowSpan = 3, colSpan = 1, content = "d")
        g.addCell(a)
        g.addCell(b)
        g.addCell(c)
        g.addCell(d)
        print(g)
        self.assertEqual(features.horizontallySpanned(a,c, None), 1)
        self.assertEqual(features.horizontallySpanned(a,b, None), 1)
        # self.assertEqual(features.horizontallySpanned(c,d, None), -1)
        self.assertEqual(features.horizontallySpanned(b,c, None), 0)

if __name__ == '__main__':
    # unittest.sortTestMethodsUsing(None)
    unittest.main()