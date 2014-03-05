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
    if len(sys.argv) < 3:
        print("resnik_similarity.py requires 2 arguments:" + os.linesep +
              "\t(1) context file" + os.linesep +
              "\t(2) information content file")
        sys.exit()
    
    context_file = sys.argv[1]
    ic_file = sys.argv[2]
    
    
    context = LoadContextFile(context_file)
    brown_ic = wordnet_ic.ic(ic_file)
    
    Process(context, brown_ic)

#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## LoadContextFile()
##-------------------------------------------------------------------------
##    Description:      Read in a context file, given in the format:
##                      probe_word context_word_1,context_word_2,context_word_n
##
##    Arguments:        context_file; file containing probe words and the 
##                          specified noun contexts
##
##    Returns:          context; list(), list of tuples of the format:
##                          (probe_word,context_list), where context_list
##                          is a list of nouns
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
##    Description:      From a given context file, run through each probe
##                      word, calculating resnik similiarity between that
##                      probe word and each context word given in the 
##                      context list. Print the results of said calculations
##                      and select the best word sense.
##
##    Arguments:        context; list(), list of tuples of the format:
##                          (probe_word,context_list), where context_list
##                          is a list of nouns
##                      ic; wordnet_ic.ic(); information content created
##                          by wordnet_ic.ic(), from an ic file.
##
##    Calls:            ResnikSimilarity()
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
        
##-------------------------------------------------------------------------
## Resnik_Similarity()
##-------------------------------------------------------------------------
##    Description:      Calculate resnik similarity score for two words
##
##    Arguments:        probe_word; the probe word
##                      context_word; the contextual comparision word
##                      ic; wordnet_ic.ic() 
##
##    Returns:          mis; tuple(), a tuple of the format:
##                          (synset, score), where synset is the most
##                          informative subsumer of the probe and context 
##                          words, and score is the resnik similarity score
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