from sklearn import svm
X = [[0, 0], [1, 1]]
y = ["a", "b"]
clf = svm.SVC()
clf.fit(X, y)  
