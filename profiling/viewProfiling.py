#This is needed to view the files out put by pressing the y key in game to profile the code.
#Run simply with:
#python viewProfiling.py
import profile
import pstats
import sys

# Read stat file into a single object
stats = pstats.Stats(sys.argv[1])
stats.sort_stats('cumulative')
stats.print_stats()

