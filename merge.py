
#    tamw contains documents annotated on all three annotation layers (morphological, analytical, tectogrammatical, together with all additional annotation and all corrections done after PDT 2.0 has been released),

import gzip

# Of interest: tfa



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

tree_m = ET.parse('ln94205_131.m').getroot()
tree_t = ET.parse('ln94205_131.t').getroot()

print(tree_t)
print(tree_t.tag)
print(tree_t.attrib)




for child in tree_t:
   if child.tag.endswith("trees"):
     for sentence in child:
        SENT_ID = sentence.attrib["id"][2:]
        wordsToData[SENT_ID] = {}
        for annotation in sentence:
            print(annotation)
            if annotation.tag.endswith("children"):
                for lm in annotation:
                  fullTree = recursivelyBuildTree(lm, SENT_ID) #print("LM", lm.attrib)
                  print("TREE")
                  print(fullTree)
        break
     break

print(wordsToData)

# c contrastive & bound
# f non-bound
# t non-contrastive bound

for child in tree_m: 
   if child.tag.endswith("s"):
       SENT_ID = child.attrib["id"][2:]
       sentence = []
       for child2 in child:
           print(child2.attrib)
           dataHere = wordsToData.get(child2.attrib["id"][2:], {})
           wordsToData[child2.attrib["id"][2:]] = dataHere
           print(dataHere)
           wordForm = None
           for anno in child2:
               if anno.tag.endswith("form"):
                  dataHere["wordForm"] = anno.text
                  wordForm = anno.text
                  break
           sentence.append((wordForm, dataHere))
       print(sentence)
       surfaceString = " ".join([x[0] for x in sentence])
       print(surfaceString)
       break

print(wordsToData)

counter = 0
with open("/u/scr/corpora/Universal_Dependencies/Universal_Dependencies_2.4/ud-treebanks-v2.4/UD_Czech-PDT/cs_pdt-ud-train.conllu", "r") as inFile:
   sentence = []
   attribs = {}
   for line in inFile:
     line = line.strip()
     if line.startswith("# ") and "=" in line:
       line=line.split(" = ")
       attribs[line[0]] = line[1]
     elif len(line) <= 1:
       if len(attribs) > 0:
          counter += 1
          if counter % 1000 == 0:
               print(counter)
          sentenceID = attribs['# sent_id']
          if sentenceID in wordsToData:
             print(wordsToData[sentenceID])
             print(attribs)
             break
       sentence = []
       attribs = {}
     else:
       sentence.append(line)
       