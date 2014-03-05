#######################################################
##
## hw6 Condor command file
## Ahmad Elshenawy
## Ling 571
## Mar 6, 2014
##
#######################################################

executable      = resnik_similarity.sh
getenv		= true
output		= results
error		= hw6.err
log		= hw6.log
arguments 	= "data/wsd_contexts.txt ic-brown-resnik-add1.dat"
transfer_executable = false
Queue
