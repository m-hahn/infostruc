#from ud_languages import languages


import subprocess

# ./python27 yStudyTradeoff_Bootstrap_Parallel_OnlyWordForms_BoundedVocab_HistogramsByMem_All.py > ../results/tradeoff/listener-curve-histogram_byMem.tsv

with open("../../results/tradeoff/ngrams/listener-curve-ci-median.tsv", "w") as outFile:
  print >> outFile, "\t".join(["Language", "Type", "Position", "Memory", "MedianEmpirical", "MedianLower", "MedianUpper", "Level"])
  for language in ["Czech-PDT"]:
     print(language)
     print >> outFile, subprocess.check_output(["python2", "yStudyTradeoff_Bootstrap_Parallel_OnlyWordForms_BoundedVocab_BinomialTest_Single_MedianCI_Ngrams.py", language]).strip()


