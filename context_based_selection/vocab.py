from collections import defaultdict
from os.path import isfile
from scipy.io import savemat
from scipy.stats import spearmanr
from scipy.linalg import orth
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import norm
from math import sqrt
from multiprocessing import cpu_count
import multiprocessing
import cPickle
import threading
import random
import Queue
import scipy 
import numpy as np
import sys
import array
import numpy.random as rn
import cPickle as pickle
import itertools
import os
import logging
import time
import struct
FUNCWORD = 'funcWords.txt'

class Vocab:

	def __init__(self, vecDim, directory, vocabInputFile, vectorInputFile, isFunctional):

		self.vecDim = vecDim
		self.vocabFile = directory + vocabInputFile
		self.vecFile = directory + vectorInputFile

		self.readVocabFromFile()
		self.readVectorFromFile()
		self.readFuncWords(isFunctional)

                #self.sem = multiprocessing.BoundedSemaphore(3)


	def readVocabFromFile(self):

		vocabList = list()
		vocabIndex = dict()
		vocabCount = list()

		f = open(self.vocabFile, "r")
		idx = 0
		for line in f.readlines():
			raw = line.lower().split()
			vocabList.append(raw[0])
			vocabCount.append(int(raw[1]))
			vocabIndex[raw[0]] = idx 
			idx += 1
			#if idx == 200000:
			#	break

		self.vocabList = vocabList
		self.vocabIndex = vocabIndex
		self.vocabSize = len(self.vocabList)
		self.vocabCount = vocabCount

		print >>sys.stdout, "Done loading vocabulary."

	def readVectorFromFile(self):

		vecDim = self.vecDim
		vecMatrix = array.array('f')
		vecMatrix.fromfile(open(self.vecFile, 'rb'), self.vocabSize * vecDim)
		vecMatrix = np.reshape(vecMatrix, (self.vocabSize, vecDim))[:, 0:vecDim]

		#vecMatrixNorm = normalizeMatrix(vecMatrix)
		#self.vecMatrixNorm = vecMatrixNorm
		self.vecMatrix = vecMatrix

		#print vecMatrix[:2]
		print >>sys.stdout, "Done loading vectors."

                def readFuncWords(self, isFunctional):
                        funcWords = set()
                        if isFunctional:
                                f = open(FUNCWORD, 'r')
                                for line in f.readlines():
                                        funcWords.add(line.rstrip())

                        self.funcWords = funcWords

	def getContextIdList(self, contexts):
		contextList = []
		for context in contexts:
                    contextId = []
                    context = context.lower().rstrip().split()
                    for word in context:
                        if word in self.funcWords:
                            continue
                        try:
                            contextId.append(self.vocabIndex[word])
                        except:
                            pass
                    contextList.append(contextId[:])
		#print "contextList:", contextList[0]
                return contextList

                                        
	def getVecFromId(self, contextIdx):
		contextVecs = list()
		for idx in contextIdx:
		    if (idx == []):
			vecs = np.array([[0]*self.vecDim])
		    else:
			vecs = self.vecMatrix[np.array(idx)]
		    contextVecs.append(vecs)
		return contextVecs		

	def getVectors(self, word_list):
		#vecDim = self.vecDim
		idxList = self.getContextIdList(word_list)

		vecList = []
		for i in range(len(idxList)):
		    idx = idxList[i]
		    if (idx == []):
			vecs = np.array([[0]*self.vecDim])
			print "no embedding for context", contexts[i]
		    else:
                        vecs = self.vecMatrix[np.array(idx)]
                    vecList.append(vecs)

                return vecList
        """                           
        def getAvgCxtVec(self, contexts):
                vecList = self.getCxtVec(contexts)
		avgVecList = []
		for vecs in vecList:
                    vecs = np.array(vecs)
                    avgVec = np.sum(vecs, axis = 0)
                    avgVecList.append(avgVec)
                return avgVecList
        """
                                    
                        
