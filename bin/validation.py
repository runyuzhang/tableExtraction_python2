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
parser.add_option('-a', '--all', action ="store_true", help='validate all files')
parser.add_option('-f', '--fileID', dest = "fileID", help='file index')
parser.add_option('-t', '--tableID', dest = "tableID", help='table index')
parser.add_option('-d', '--dataset', dest = "dataset", help='eu or us dataset')
parser.add_option('-g', '--persistedModel', dest = "persistedModel", help='persisted model')
(options, args) = parser.parse_args()


#use persisted model
clf = joblib.load(options.persistedModel)
total = 0
correct = 0

fileList = []
filesListPtr = open("training_files_" + options.dataset + ".txt")
line = filesListPtr.readline()
while line:
	fileList += [line.strip()]
	line = filesListPtr.readline()
# fileList= ["001", "002", "003", "005", "006", "007", "008", '010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027']

def validate(file, tableGridID, tableGrid):
	global total
	global correct
	fvg = FeatureVectorGenerator(tableGrid)
	idCellMap = tableGrid.idCellMap

	for c1_id in range(len(idCellMap.keys())):
		for c2_id in range(c1_id+1, len(idCellMap.keys())):
			c1 = tableGrid.getCellByCellID(c1_id)
			c2 = tableGrid.getCellByCellID(c2_id)

			if (not c1.isData()) and (not c2.isData()):
				total += 1

				featureVector = fvg.generateFeatureVector(c1, c2)
				prediction = clf.predict(fvg.generateFeatureVector(c1, c2))[0]
				groundTruth = tableGrid.classify(c1, c2)

				if prediction == groundTruth:
					correct += 1
				else:
					print(file, tableGridID, c1.cellID, c2.cellID, groundTruth, prediction, clf.predict_proba(featureVector))



if options.all:
	for file in fileList:
		grids = parse(file, dataset = options.dataset)
		for tableGridID in grids.keys():
			validate(file, tableGridID, grids[tableGridID])
else:
	grids = parse(options.fileID, dataset = options.dataset)
	validate(options.fileID, int(options.tableID), grids[int(options.tableID)])
	

	

print(correct / total)
