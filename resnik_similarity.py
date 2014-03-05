'''
#==============================================================================
resnik_similarity
Created on Mar 6, 2014
@author: aelshen
#==============================================================================
'''

from __future__ import print_function
import os
import sys
import math
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content
from collections import defaultdict
#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True

#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    context_file = sys.argv[1]
    ic_file = sys.argv[2]
    print(ic_file)
    
    context = LoadContextFile(context_file)
    brown_ic = wordnet_ic.ic(ic_file)
    
    results = Process(context, brown_ic)
    
    
    ######
    #EXAMPLES
    ######
    #dog = wn.synset('dog.n.01')
    #cat = wn.synset('cat.n.01')
    #Calculate resnik similarity
    #dog.res_similarity(cat, brown_ic)
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## LoadContextFile()
##-------------------------------------------------------------------------
##    Description:        description
##
##    Arguments:        arguments
##
##    Calls:                calls
##
##        Returns:            returns
##-------------------------------------------------------------------------
def LoadContextFile(context_file):
    context = []
    
    for line in open(context_file, 'r'):
        line = line.strip().split()
        probe_word = line[0]
        word_grouping = line[1].split(",")
        
        context.append((probe_word, word_grouping))
            
    return context


##-------------------------------------------------------------------------
## Process()
##-------------------------------------------------------------------------
##    Description:        description
##
##    Arguments:        arguments
##
##    Calls:                calls
##
##        Returns:            returns
##-------------------------------------------------------------------------
def Process(context, ic):
    best_senses = []
    results = []
    for i in xrange( len(context) ):
        normalization_factor = 0.0
        scores = defaultdict(float)
        probe_word = context[i][0]
        for context_word in context[i][1]:            
            resnik = ResnikSimilarity(probe_word, context_word, ic)
            
            if resnik:
                mis,similarity = resnik
                print( (probe_word, context_word, similarity), end="" )

                normalization_factor += similarity
                
                for sense in wn.synsets(probe_word):
                    if mis in mis.common_hypernyms(sense):
                        scores[sense] += similarity
                    
            else:
                print( (probe_word, context_word, 'None'), end="" )
    
        
        for s in scores:
            scores[s] = scores[s] / normalization_factor
    
        print(os.linesep + max(scores.iterkeys(), key=lambda x: scores[x]).name )
    
    return results
        
##-------------------------------------------------------------------------
## Resnik_Similarity()
##-------------------------------------------------------------------------
##    Description:        description
##
##    Arguments:        arguments
##
##    Calls:                calls
##
##        Returns:            returns
##-------------------------------------------------------------------------
def ResnikSimilarity(probe_word, context_word, ic):
    probe_senses = wn.synsets(probe_word)
    context_senses = wn.synsets(context_word)
    
    if not context_senses:
        return None
    
    most_informative_subsumers = set() 
    
    for p in probe_senses:
        for c in context_senses:
            common_hypernyms = p.common_hypernyms(c)
            if common_hypernyms:
                temp =  max(common_hypernyms, key=lambda x: information_content(x, ic) )
                score = information_content(temp, ic)

                
                most_informative_subsumers.add( (temp, score) )
            
    
    mis = max(most_informative_subsumers, key=lambda x: x[1])
    
    return mis

    
#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )
