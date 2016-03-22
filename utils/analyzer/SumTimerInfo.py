#!/usr/bin/env python

"""
Script to Summarize statistics in the scan-build output.

Statistics are enabled by passing '-internal-stats' option to scan-build
(or '-analyzer-stats' to the analyzer).

"""

import string
from operator import itemgetter
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: ', sys.argv[0],\
                             'scan_build_output_file'
        sys.exit(-1)

    f = open(sys.argv[1], 'r')
    Time = 0.0
    TotalTime = 0.0
    MaxTime = 0.0
    Warnings = 0
    Count = 0
    FunctionsAnalyzed = 0
    ReachableBlocks = 0
    ReachedMaxSteps = 0
    NumSteps = 0
    NumInlinedCallSites = 0
    NumBifurcatedCallSites = 0
    MaxCFGSize = 0
    Mode = 1
    for line in f:
        if ("Miscellaneous Ungrouped Timers" in line) :
          Mode = 1
        if (("Analyzer Total Time" in line) and (Mode == 1)) :
          s = line.split()
          Time = Time + float(s[6])
          Count = Count + 1
          if (float(s[6]) > MaxTime) :
            MaxTime = float(s[6])
        if ((("warning generated." in line) or ("warnings generated" in line)) and Mode == 1) :
          s = line.split()
          Warnings = Warnings + int(s[0])
        if (("The # of functions analysed (as top level)" in line) and (Mode == 1)) :
          s = line.split()
          FunctionsAnalyzed = FunctionsAnalyzed + int(s[0])
        if (("The % of reachable basic blocks" in line) and (Mode == 1)) :
          s = line.split()
          ReachableBlocks = ReachableBlocks + int(s[0])
        if (("The # of times we reached the max number of steps" in line) and (Mode == 1)) :
          s = line.split()
          ReachedMaxSteps = ReachedMaxSteps + int(s[0])
        if (("The maximum number of basic blocks in a function" in line) and (Mode == 1)) :
          s = line.split()
          if (MaxCFGSize < int(s[0])) :
            MaxCFGSize = int(s[0])
        if (("The # of steps executed" in line) and (Mode == 1)) :
          s = line.split()
          NumSteps = NumSteps + int(s[0])
        if (("The # of times we inlined a call" in line) and (Mode == 1)) :
          s = line.split()
          NumInlinedCallSites = NumInlinedCallSites + int(s[0])
        if (("The # of times we split the path due to imprecise dynamic dispatch info" in line) and (Mode == 1)) :
          s = line.split()
          NumBifurcatedCallSites = NumBifurcatedCallSites + int(s[0])
        if ((")  Total" in line) and (Mode == 1)) :
          s = line.split()
          TotalTime = TotalTime + float(s[6])

    print "TU Count {0:d}".format((Count))
    print "Time {0:f}".format((Time))
    print "Warnings {0:d}".format((Warnings))
    print "Functions Analyzed {0:d}".format((FunctionsAnalyzed))
    print "Reachable Blocks {0:d}".format((ReachableBlocks))
    print "Reached Max Steps {0:d}".format((ReachedMaxSteps))
    print "Number of Steps {0:d}".format((NumSteps))
    print "Number of Inlined calls {0:d} (bifurcated {1:d})".format(NumInlinedCallSites, NumBifurcatedCallSites)
    print "MaxTime {0:f}".format((MaxTime))
    print "TotalTime {0:f}".format((TotalTime))
    print "Max CFG Size {0:d}".format((MaxCFGSize))
