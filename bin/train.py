from features import *
from parse import *
import sys, optparse
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import sys, os
import pickle
import random
from sklearn import tree
import json

parser = optparse.OptionParser()
parser.add_option('-p', '--display', action='store_true', help='display the tables as they are parsed')
parser.add_option('-g', '--gen', action='store_true', help='re-generate feature vectors')
parser.add_option('-m', '--method', dest="method", help="classification method")
parser.add_option('-d', '--dataset', dest="dataset", help="us or eu dataset")
parser.add_option('-a', '--all', action='store_true', help="train on all files in the dataset")
parser.add_option('-f', '--fileID', dest = "fileID", help='file index')
parser.add_option('-t', '--tableID', dest = "tableID", help='table index')
parser.add_option('-q', '--quit', action='store_true', help='quit after generating training data')
parser.add_option('-u', '--upsample', action='store_true', help='upsample underrepresented labels')
parser.add_option('--appendSource', action='store_true', help='append the file and tableID for feature vectors')

(options, args) = parser.parse_args()

pairwiseLabels = {"leftSuperior": "L",
				  "rightSuperior": "R",
				  "siblings": "S",
				  "unrelated": "U"}


kernal = "linear"
trainingFilesPtr = open("training_files_" + options.dataset + ".txt")
trainingFiles = []


file_grids_map = {}

counter = 0
#read training files

x = {"L" : [], "R" : [], "S" : [], "U" : []}
X = []
Y = []

def upsample(x, y):
	assert len(x) == len(y), "there should be as many feature vectors as labels"
	import collections, math
	counter = collections.Counter(y)
	mostFrequentLabel = max(counter)
	multipliers = {key: math.floor(counter[mostFrequentLabel] / counter[key]) for key in counter.keys()}
	# print(multipliers)

	X = []
	Y = []
	for i in range(len(x)):
		for _ in range(multipliers[y[i]]):
			X.append(x[i])
			Y.append(y[i])

	return X,Y




if options.gen:
	if options.all:
		line = trainingFilesPtr.readline()
		while line:
			trainingFiles += [line.strip()]
			line = trainingFilesPtr.readline()
	else:
		trainingFiles.append(options.fileID)

	for fileIndex in trainingFiles:
		#parsing the xml file, reading functional and structural tagging
		id_grid_map = parse(fileIndex, dataset = options.dataset, display = options.display)
		file_grids_map[options.dataset + "-" + fileIndex + "-str.xml"] = id_grid_map

		#generate non-header cell pairs with tags
		if options.all:
			tableIDs = id_grid_map.keys()
		else:
			tableIDs = [int(options.tableID)]

		for tableID in tableIDs:
			tableGrid = id_grid_map[tableID]
			featureVectorGenerator = FeatureVectorGenerator(tableGrid)
			
			idCellMap = tableGrid.idCellMap
			for c1_id in range(len(idCellMap.keys())):
				for c2_id in range(c1_id+1, len(idCellMap.keys())):
					c1 = tableGrid.getCellByCellID(c1_id)
					c2 = tableGrid.getCellByCellID(c2_id)

					if (not c1.isData()) and (not c2.isData()):

						featureVector = featureVectorGenerator.generateFeatureVector(c1, c2)

						featureVectorMap = featureVectorGenerator.generateFeatureVectorMap(c1, c2)

						if options.appendSource:
							featureVector.append(c1_id)
							featureVector.append(c2_id)
							featureVector.append(fileIndex)
							featureVector.append(tableID)


						label = tableGrid.classify(c1, c2)

						if not options.all:
							print(c1.cellID, c2.cellID, "\n", json.dumps(featureVectorMap, indent = 4, sort_keys = True), label)

						X += [featureVector]
						Y += [label]

	if options.upsample:
		X, Y = upsample(X,Y)
	
	
	# for label in x:
	# 	X += [random.choice(x[label]) for _ in range(20000)]
	# 	Y += [label] * 20000
	if options.all:
		pickle.dump(X, open(options.dataset + "_featureVectors.dat", "wb"))
		pickle.dump(Y, open(options.dataset + "_labels.dat", "wb"))

	# else:
	# 	for i in range(len(X)):
	# 		print(options.fileID, options.tableID, X[i], Y[i])

if options.quit:
	quit()


# quit()
# X = pickle.load(open("us_featureVectors.dat", "rb"))
# Y = pickle.load(open("us_labels.dat", "rb"))
# C_range = np.logspace(-3, 9, 13)
# gamma_range = np.logspace(-5, 1, 7)
# param_grid = dict(gamma=gamma_range, C=C_range)
# cv = StratifiedShuffleSplit(Y, n_iter=1, test_size=0.2)
# grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv, verbose = 3)
# grid.fit(X, Y)

# print("The best parameters are %s with a score of %0.2f"
#       % (grid.best_params_, grid.best_score_))

# quit()


X = pickle.load(open(options.dataset + "_featureVectors.dat", "rb"))
Y = pickle.load(open(options.dataset + "_labels.dat", "rb"))
# clf = svm.SVC(gamma = float(sys.argv[2]), C = float(sys.argv[3]))
# clf = svm.SVC(kernel = "linear")
print("Fitting")
os.chdir("../data/storage")
if options.method == "svm":
	# gammaVal = 0.001
	# CVal = 10000
	gammaVal = 10
	CVal = 10
	clf = svm.SVC(gamma=gammaVal, C=CVal, probability = True)
	clf.fit(X,Y)
	joblib.dump(clf, options.method + "_" + str(gammaVal) + "_" + str(CVal) + "_" + options.dataset + ".pkl")
elif options.method == "logistic":
	CVal = 10000
	logreg = linear_model.LogisticRegression(C = CVal)
	logreg.fit(X,Y)
	joblib.dump(logreg, options.method + "_" + str(CVal) + "_" + options.dataset + ".pkl")
elif options.method == "tree":
	from sklearn.externals.six import StringIO
	import pydot 
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X, Y)
	joblib.dump(clf, "tree_" + options.dataset + ".pkl")
elif options.method == "randomForest":
	N_ESTIMATORS = 100
	MAX_FEATURES = 10
	clf = RandomForestClassifier(n_estimators = N_ESTIMATORS, max_features = MAX_FEATURES)
	clf = clf.fit(X,Y)
	joblib.dump(clf,  "randomForest_{0}_{1}_{2}.pkl".format(N_ESTIMATORS, MAX_FEATURES, options.dataset))