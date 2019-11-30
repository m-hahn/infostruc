
#    tamw contains documents annotated on all three annotation layers (morphological, analytical, tectogrammatical, together with all additional annotation and all corrections done after PDT 2.0 has been released),

import gzip

# Of interest: tfa
import os
import sys


import xml.etree.ElementTree as ET

def recursivelyBuildTree(lm, SENT_ID):
 #  print(lm.attrib)
   result = {"id" : lm.attrib["id"], "children" : [], "tfa" : "NULL", "t_lemma" : "NULL"}
   for child in lm:
      if child.tag.endswith("children"):
          for child2 in child:
              result["children"].append(recursivelyBuildTree(child2, SENT_ID))
      elif child.tag.endswith("tfa"):
        result["tfa"] = child.text
      elif child.tag.endswith("t_lemma"):
        result["t_lemma"] = child.text
#      print(child)
   wordsToData[SENT_ID][result["id"][2:]] = result
   return result

wordsToData = {}


for directory in os.listdir("/u/scr/mhahn/CORPORA/czech_pdt/PDT3.5/data/tamw/"):
  BASE_DIR = "/u/scr/mhahn/CORPORA/czech_pdt/PDT3.5/data/tamw/"+directory
  files = sorted(list(set([x[:-5] for x in os.listdir(BASE_DIR)])))
  print(files)
#  quit()
  for fileName in files:
    print(fileName) 
    tree_m = ET.fromstring(gzip.open(BASE_DIR+"/"+fileName+".m.gz", "r").read())
    tree_t = ET.fromstring(gzip.open(BASE_DIR+"/"+fileName+".t.gz", "r").read())
    
#    print(tree_t)
 #   print(tree_t.tag)
  #  print(tree_t.attrib)
    
    
    
    
    for child in tree_t:
       if child.tag.endswith("trees"):
         for sentence in child:
            SENT_ID = sentence.attrib["id"][2:]
            wordsToData[SENT_ID] = {}
            for annotation in sentence:
                #print(annotation)
                if annotation.tag.endswith("children"):
                    for lm in annotation:
                      fullTree = recursivelyBuildTree(lm, SENT_ID) #print("LM", lm.attrib)
                 #     print("TREE")
                  #    print(fullTree)
         #   break
#         break
    
   # print(wordsToData)
    
    # c contrastive & bound
    # f non-bound
    # t non-contrastive bound
    
    for child in tree_m: 
       if child.tag.endswith("s"):
           SENT_ID = child.attrib["id"][2:]
           sentence = []
           wordsToData[SENT_ID]["linearized"] = sentence
           for child2 in child:
               #print(child2.attrib)
               dataHere = wordsToData[SENT_ID].get(child2.attrib["id"][2:], {})
               wordsToData[SENT_ID][child2.attrib["id"][2:]] = dataHere
               #print(dataHere)
               wordForm = None
               for anno in child2:
                   if anno.tag.endswith("form"):
                      dataHere["wordForm"] = anno.text
                      wordForm = anno.text
                #      print("WORD FORM", wordForm)
                      break
               sentence.append((wordForm, dataHere))
#           print(sentence)
           surfaceString = " ".join([x[0] for x in sentence])
#           print(surfaceString)
 #          break
#quit()

#print(wordsToData)

counter = 0
for partition in ["test", "dev", "train"]:
  with open("/u/scr/mhahn/CORPORA/czech_pdt_infostruc/"+partition+".conllu", "w") as outFile:
   with open("/u/scr/corpora/Universal_Dependencies/Universal_Dependencies_2.4/ud-treebanks-v2.4/UD_Czech-PDT/cs_pdt-ud-train.conllu", "r") as inFile:
      sentence = []
      attribs = {}
      for line in inFile:
        line = line.strip()
        if line.startswith("# "):
           print(line, file=outFile)
           try:
              index = line.index("=")
              attribs[line[:index-1]] = line[index+2:]
   #           print((line[:index-1], line[index+1:]))
           except ValueError:
            _ = 0
        elif len(line) <= 1:
          if len(attribs) > 0:
             counter += 1
    #         if counter % 1000 == 0:
   #               print(counter)
             sentenceID = attribs['# sent_id']
             if sentenceID in wordsToData:
                annotated = wordsToData[sentenceID]["linearized"]
                fromAnnotation = [x[0] for x in annotated]
                fromUD = attribs["# text"]
                if "".join(fromAnnotation) != fromUD.replace(" ", ""):
                  print((fromAnnotation, fromUD), file=sys.stderr)
                print(fromAnnotation)
   #             print("\n".join(sentence))
                lastWord = sentence[-1]
                counterInAnnotation = 0
                counterInUD = 0
                while counterInUD < len(sentence):
                   line = sentence[counterInUD]
                   line = line.split("\t")
                   print(line)
                   print(counterInUD, counterInAnnotation)
                   form = line[1]
                   if form != fromAnnotation[counterInAnnotation]:
                     print((form, fromAnnotation[counterInAnnotation]), file=sys.stderr)
                   sentence[counterInUD]+="\t"+annotated[counterInAnnotation][1].get("tfa", "N")
                   if "-" in line[0]:
                      start, end = line[0].split("-")
                      for i in range(counterInUD+1, 2 + int(end) - int(start)):
                         sentence[counterInUD]+="\t"+annotated[counterInAnnotation][1].get("tfa", "N")
                      counterInUD += 2 + int(end) - int(start)
                   else:
                      counterInUD += 1
                   counterInAnnotation += 1
   #             assert len(fromAnnotation) == int(lastWord[:lastWord.index("\t")])
   #             break
             else:
                print(("MISSING SENTENCE", sentenceID), file=sys.stderr)
                for i in range(len(sentence)):
                    sentence[i] += "\tUNK"

             for line in sentence:
                print(line, file=outFile)

          print("\n\n", file=outFile)

          sentence = []
          attribs = {}
        else:
          sentence.append(line)
          
