import pickle
import collections
import sys, optparse, json
parser = optparse.OptionParser()

parser.add_option('-r', '--ratio', action='store_true', help='display number of training samples for each class label')
parser.add_option('--duplicates', action='store_true', help='display number of duplicated feature vectors with different labels')
parser.add_option('-d', '--dataset', dest='dataset', help='which dataset to use')

(options, args) = parser.parse_args()


if options.ratio:
	print("Ratio of training samples for each class: \n")

	a = pickle.load(open("{0}_labels.dat".format(options.dataset), "rb"))
	print(collections.Counter(a))

if options.duplicates:
	fv = pickle.load(open("{0}_featureVectors.dat".format(options.dataset), "rb"))
	fl = pickle.load(open("{0}_labels.dat".format(options.dataset), "rb"))
	fv = [tuple(l) for l in fv]
	d = {}
	for i, f in enumerate(fv):
		d[f] = d.get(f, set())
		d[f].add(fl[i])
	duplicates_d = {k:v for k,v in d.items() if len(v) > 1}
	for k,v in duplicates_d.items():
		if k[-9] == 1:
			print(k,v)
	print(len(duplicates_d))


	# fv = pickle.load(open("{0}_featureVectors.dat".format(options.dataset), "rb"))
	# fl = pickle.load(open("{0}_labels.dat".format(options.dataset), "rb"))
	# fv_t = [tuple(l[:-4]) for l in fv]
	# d = {}
	# for i, f in enumerate(fv_t):
	# 	d[f] = d.get(f, set())
	# 	d[f].add((tuple(fv[i][-4:]), fl[i]))
	# duplicates_d = {k:v for k,v in d.items() if len(v) > 1}
	# for k,v in duplicates_d.items():
	# 	print(k,v)
	# print(len(duplicates_d))