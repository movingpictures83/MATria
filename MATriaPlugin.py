import copy
import sys
import operator
import random
import PageTrust
import networkx_mod
import os
import PyPluMA

#import PNcentrality
from PNcentrality import *
from scipy.stats import spearmanr

# Return a list of fully connected components of size i
def fullyConnected(ADJ, n, i, bacteria):
   FULLY_CONNECTED = []
   # Start with single edgese
   components = []
   for k in range(n):
      for j in range(k+1, n):
         if (ADJ[k][j] != 0):
            components.append((k, j))
   
   if (i > 2):
    for j in range(i-1):
      tmp = []
      toremove = []
      for component in components:
         takeout = False
         # Component nodes are in ascending oroder
         for k in range(component[len(component)-1]+1, n):
            connected = True
            for j in range(len(component)):
               if (ADJ[k][component[j]] == 0):
                  connected = False
                  break
            if (connected):
               tmp.append(component+(k,))
               takeout = True
         if (takeout):
            toremove.append(component)
      for component in toremove:
         components.remove(component)
      FULLY_CONNECTED += components
      components = tmp
    toremove = []
    for k in range(len(FULLY_CONNECTED)):
      if (len(FULLY_CONNECTED[k]) != i):
         toremove.append(FULLY_CONNECTED[k])
    for component in toremove:
      FULLY_CONNECTED.remove(component)
   else:
     FULLY_CONNECTED += components
   for k in range(len(FULLY_CONNECTED)):
      bacs = []
      for j in range(len(FULLY_CONNECTED[k])):
        bacs.append(bacteria[FULLY_CONNECTED[k][j]])
      FULLY_CONNECTED[k] = tuple(bacs)
   return FULLY_CONNECTED


# Can be taken out later, for analysis purposes
ADJ = []


def buildATriaNetworkXGraph(myfile):
 ADJ.__delitem__(slice(0, len(ADJ)))
 if (myfile[len(myfile)-3:] == "csv"):
  PyPluMA.log("*************************************************************************************************")
  PyPluMA.log("Reading CSV File: "+myfile)
  G=networkx_mod.Graph()
  ###########################################################
  # Read the file
  # Put results in filestuff
  filestuff = open(myfile, 'r')
  firstline = filestuff.readline()
  bacteria = firstline.split(',')
  if ('\"\"' in bacteria):
     bacteria.remove('\"\"')
  n = len(bacteria)
  inf = float("infinity")
  ###########################################################

  for i in range(n):
    bac = bacteria[i].strip()
    bac = bac[1:len(bac)-1]
    G.add_node(bac+"+")
    G.add_node(bac+"-")
  eps = 0.01
  ###########################################################
  # Populate the adjacency matrix, ADJ
  i = 0
  for line in filestuff:
   contents = line.split(',')
   values = numpy.zeros([n])
   ADJ.append([])
   for j in range(n):
      value = float(contents[j+1])
      if (i == j):
         value = 0
      ADJ[i].append(value)
      # Anything other than pagerank, we can read as we go
      if (i != j and value != 0):
           bac1 = bacteria[i].strip()
           bac2 = bacteria[j].strip()
           bac1 = bac1[1:len(bac1)-1]
           bac2 = bac2[1:len(bac2)-1]
           if (value < 0):
              G.add_edge(bac1+'+', bac2+'-', weight=value)
              G.add_edge(bac1+'-', bac2+'+', weight=value)
           elif (value > 0):
              G.add_edge(bac1+'+', bac2+'+', weight=value)
              G.add_edge(bac1+'-', bac2+'-', weight=value)
   # Pagerank cannot handle a weighted sum of zero
   # for all edges of a node.  Adding eps if that's the case
   i = i + 1
  ############################################################

 else:
  PyPluMA.log("Reading GML File...")
  G = networkx_mod.read_gml(myfile)
  bacteria = G.nodes()
  PyPluMA.log("Done.")

 return bacteria, G

############################################################

def buildNetworkXGraph(myfile, clusters=[]):
 ADJ.__delitem__(slice(0, len(ADJ)))
 if (myfile[len(myfile)-3:] == "csv"):
  PyPluMA.log("*************************************************************************************************")
  PyPluMA.log("Reading CSV File: "+myfile)
  G=networkx_mod.Graph()
  ###########################################################
  # Read the file
  # Put results in filestuff
  filestuff = open(myfile, 'r')
  firstline = filestuff.readline()
  bacteria = firstline.split(',')
  if ('\"\"' in bacteria):
     bacteria.remove('\"\"')
  n = len(bacteria)
  inf = float("infinity")
  ###########################################################

  for i in range(n):
    bac = bacteria[i].strip()
    bac = bac[1:len(bac)-1]
    G.add_node(bac)

  eps = random.random()*0.000001
  ###########################################################
  # Populate the adjacency matrix, ADJ
  i = 0
  for line in filestuff:
   ADJ.append([])
   contents = line.split(',')
   values = numpy.zeros([n])
   for j in range(n):
      value = float(contents[j+1])
      if (i == j):
         value = 0
      ADJ[i].append(value)
      # Anything other than pagerank, we can read as we go
      if (i != j and value != 0):
           bac1 = bacteria[i].strip()
           bac2 = bacteria[j].strip()
           bac1 = bac1[1:len(bac1)-1]
           bac2 = bac2[1:len(bac2)-1]
           G.add_edge(bac1, bac2, weight=value)
   i = i + 1
  ############################################################

 else:
  PyPluMA.log("Reading GML File...")
  G = networkx_mod.read_gml(myfile)
  bacteria = G.nodes()
  PyPluMA.log("Done.")

 return bacteria, G

############################################################


class MATriaPlugin:
 def input(self, filename):
  self.myfile = filename

 def run(self):
   myalg=""
   self.results = {}
   self.iter_results = {}
   self.sorted_iter_results = {}
   algs = ["betweenness", "closeness", "degree", "PN"]#"pagetrust", "PN"]
   numalg = len(algs)
   for alg in algs:
      self.iter_results[alg] = {}
      self.sorted_iter_results[alg] = {}
   #results = {}
   for myalg in self.iter_results.keys():
    count = 1
    if (myalg == "pagetrust" or myalg == "PN"):
       self.bacteria, G = buildNetworkXGraph(self.myfile)
       bacteria2 = copy.deepcopy(self.bacteria)
    else:
       self.bacteria, G = buildATriaNetworkXGraph(self.myfile)
    n = len(G.nodes())
    mynodes=[]
    for bac in self.bacteria:
      mynodes.append(bac.strip()[1:len(bac.strip())-1]+"+")
    PyPluMA.log("RUNNING: "+myalg)
    for i in range(len(mynodes)):
      if (myalg == "betweenness"):
         tmp = networkx_mod.betweenness_centrality(G, weight='weight', normalized=False, mynodes=mynodes)
      elif (myalg == "closeness"):
         tmp = networkx_mod.closeness_centrality(G, distance='weight', normalized=False, mynodes=mynodes)
      elif (myalg == "degree"):
         tmp = networkx_mod.degree_centrality(G, normalized=False)
      elif (myalg == "pagetrust"):
         tmp2 = PageTrust.pagetrust(G)
         tmp = dict()
         for i in range(len(self.bacteria)):
            if (sum(ADJ[i]) == 0): 
               benchmark = tmp2[G.nodes().index(self.bacteria[i].strip()[1:len(self.bacteria[i].strip())-1])]
         for i in range(len(tmp2)):
            tmp[G.nodes()[i]] = tmp2[i] - benchmark
      elif (myalg == "PN"):
         #tmp2 = PNcentrality.pncentrality(bacteria2, G)
         tmp2 = pncentrality(bacteria2, G)
         tmp = dict()
         for i in range(len(tmp2)):
            tmp[bacteria2[i]] = tmp2[i] - 1  # 1 is neutral
      maxcent = -1
      maxcent = -1
      maxkey = ''
      for key in tmp:
         if (abs(tmp[key]) > maxcent or (key < maxkey and abs(tmp[key]) == maxcent)):
            maxcent = abs(tmp[key])
            maxkey = key
      if (myalg == "pagetrust"):
        bac = maxkey
      elif (myalg != "PN"):
        bac = maxkey[0:len(maxkey)-1]
      else:
        bac = maxkey[1:len(maxkey)-1]
      PyPluMA.log("Maxkey: "+bac+" Payoff: "+str(tmp[maxkey]))
      if (tmp[maxkey] != 0):
       self.iter_results[myalg][bac] = count #tmp[maxkey]
       count += 1
       # Triads
       marks = set()
       if (myalg != "pagetrust" and myalg != "PN"):
        for node1 in G.adj[bac+"+"]:
         for node2 in G.adj[bac+"+"]:
           if (node1 != node2 and G.has_edge(node1, node2)):
              marks.add(tuple(sorted((node1, node2))))
        for node1 in G.adj[bac+"-"]:
         for node2 in G.adj[bac+"-"]:
           if (node1 != node2 and G.has_edge(node1, node2)):
              marks.add(tuple(sorted((node1, node2))))
        for edge in marks:
         G.remove_edge(edge[0], edge[1])
        G.remove_node(bac+"+")
        G.remove_node(bac+"-")
        mynodes.remove(bac+"+")
       else:
        for node1 in G.adj[bac]:
         for node2 in G.adj[bac]:
           if (node1 != node2 and G.has_edge(node1, node2)):
              marks.add(tuple(sorted((node1, node2))))
        for edge in marks:
           G.remove_edge(edge[0], edge[1])        
        G.remove_node(bac)
        if (myalg == "PN"):
          bacteria2.remove('\"'+bac+'\"')

      done = True
      for v in G:
         if len(G.neighbors(v)) > 1:
            done = False
            break
      if (tmp[maxkey] == 0 or done):
         self.sorted_iter_results[myalg] = sorted(self.iter_results[myalg].items(), key=operator.itemgetter(1))
         break
   bacteria2 = []
   for bac in self.bacteria:
      bacteria2.append(bac.strip()[1:len(bac.strip())-1])
   self.S = []
   # Agreements
   agreements = set(bacteria2)
   for alg in self.iter_results:
      agreements = agreements.intersection(set(self.iter_results[alg].keys()))
   for bac in agreements:
      self.S.append([bac])

   # Resolving Disagreements
   components = []
   littleS = []
   for c in range(numalg, 1, -1):
      # Get all components first
      for component in fullyConnected(ADJ, len(self.bacteria), c, bacteria2):
         # Here, we check if each node covers at least one algorithm AND
         # all algorithms are covered exactly once
         counts = {}
         for alg in self.iter_results:
            counts[alg] = 0
         allAtLeastOne = True
         for bac in component:
            if ([bac] not in self.S):
               atleastOne = False
               for alg in self.iter_results:
                  if bac in self.iter_results[alg]:
                     counts[alg] += 1
                     atleastOne = True
               allAtLeastOne = allAtLeastOne and atleastOne
            else:
               allAtLeastOne = False
               break
         algsExactlyOne = True
         for alg in self.iter_results:
            if (counts[alg] != 1):
               algsExactlyOne = False
         if (allAtLeastOne and algsExactlyOne):
            # Now, we have to check to make sure that this component
            # is not completely engulfed by a larger one
            element = []
            for alg in self.iter_results:
               element.append([])
               for bac in component:
                  if bac in self.iter_results[alg]:
                     element[len(element)-1].append(bac)
            littleS.append(element)

   # Now, tricky.  We have to merge components
   merges = True
   while (merges):
      merges = False
      i = 0
      while (not merges and i < len(littleS)):
         j = i+1
         while (not merges and j < len(littleS)): 
            component1 = littleS[i]
            component2 = littleS[j]
            newcomponent = []
            for bac in range(numalg):
               if (len(set(component1[bac]).intersection(component2[bac])) != 0):
                  newcomponent.append(list(set(component1[bac]).union(component2[bac])))
                  merges = True
               else:
                  newcomponent.append(list(set(component1[bac]).union(set(component2[bac]))))
            if (merges):
               littleS.remove(component1)
               littleS.remove(component2)
               littleS.append(newcomponent)
            j += 1
         i += 1
   for element in littleS:
      for i in range(numalg):
         j = i+1
         while (j < len(element)):
            if (element[j] == element[i]):
               element.remove(element[j])
            else:
               j += 1 

   for element in littleS:
      self.S.append(element)



   if (myalg != ""):
      myalg = '.' + myalg

 def output(self, filename):
   UG2s = dict()
   # Print other three iteration files
   for alg in self.sorted_iter_results: #'betweenness', 'closeness', 'degree', 'PN']:
      results = self.sorted_iter_results[alg]
      UG2 = []
      for tup in results:
         UG2.append((abs(tup[1]), tup[0]))
      UG2.sort()
      UG2.reverse()
      UG2s[alg] = UG2
      cytofile2 = filename + "." + alg + ".noa"
      outfile = open(cytofile2, 'w')
      outfile.write("Name\tCentrality\tRank\n")
      # Just top 20%
      numberselected = len(UG2)
      for i in range(numberselected):
         bac = UG2[i][1]
         if (bac[0] == '\"'):
            bac = bac[1:len(bac)-1]
         if (UG2[i][0] != UG2[len(UG2)-1][0]):
            outfile.write(bac+"\t"+str(abs(UG2[i][0]))+"\t"+str(len(UG2)-i)+"\n")
         else:
            outfile.write(bac+"\t"+str(abs(UG2[i][0]))+"\t"+"0\n")
      for bac in self.bacteria:
         bac = bac.strip()
         bac = bac[1:len(bac)-1]
         flag = False
         for tup in results:
            if (tup[0] == bac):
               flag = True
         if (not flag):
            outfile.write(bac+"\t0\t0\n")         

   cor = dict()
   for alg in self.iter_results:
      cor[alg] = []
   PyPluMA.log("*************************************************************************************************")
   PyPluMA.log("FINAL S: "+str(self.S))
   PyPluMA.log("*************************************************************************************************")

   totallength = 0
   for myset in self.S:
      # Universal agreement, simply add it to the result vectors
      if (len(myset) == 1):
         for alg in self.iter_results: #['betweenness', 'closeness', 'degree']:
            cor[alg].append(abs(self.iter_results[alg][myset[0]]))
         totallength += 1
      # Primary triad, give it the average of the scores of its algorithm
      else:
            myunion = set()
            for alg in self.iter_results:
               minr = len(self.bacteria)+1
               for element in myset: 
                  for bac in element: 
                     if (bac in self.iter_results[alg]):      
                        rank = self.iter_results[alg][bac]
                        if (rank < minr):
                           minr = rank
               cor[alg].append(minr)
               myunion = myunion.union(set(element))
            totallength += len(myunion)       


   # Unresolved disagreements
   for bac in self.bacteria:
      bac = bac.strip()
      bac = bac[1:len(bac)-1]
      flag = False
      for aset in self.S:
         for element in aset:
            if bac in element:
               flag = True
      if (not flag):
         for alg in self.iter_results:
            if (bac in self.iter_results[alg]):
               cor[alg].append(abs(self.iter_results[alg][bac]))
            else:
               cor[alg].append(len(self.bacteria))

   maxes = dict()
   # Agreed unimportance    
   for alg in cor:
         maxes[alg] = -1
         for val in cor[alg]: 
            if (val > maxes[alg] and val != len(self.bacteria)):
               maxes[alg] = val

   
   # Smooth out ranks
   for alg in cor:
      # Find missing values
      missing = []
      for i in range(1, maxes[alg]+1):
         if (not i in cor[alg]):
            missing.append(i)
      # For each value, go until you hit a value in missing that is higher
      # Count how many values have passed
      # Subtract this amount
      for i in range(len(cor[alg])):
         val = cor[alg][i]
         count = 0
         while (count < len(missing) and missing[count] < val):
            count += 1
         if (cor[alg][i] != len(self.bacteria)):
           cor[alg][i] -= count


   for alg in cor:
      for alg2 in cor:
         results = spearmanr(cor[alg], cor[alg2])

   # Now compute average correlations
   # A bit tricky...
   meancor = []
   numalg = len(cor)
   #numnodes = len(cor[cor.keys()[0]])
   numnodes = len(cor[list(cor)[0]])
   for i in range(numnodes):
      sum = 0.0
      for alg in cor:
         sum += cor[alg][i]
      meancor.append(sum / numalg)
   
   # Now assemble a dictionary, consisting of elements of S and their average cor.
   meandict = []
   index = 0
   for myset in self.S:
      if (len(myset) == 1):
         meandict.append((meancor[index], [myset]))
      else:
         meandict.append((meancor[index], myset))
      index += 1
   for bac in self.bacteria:
      bac = bac.strip()
      bac = bac[1:len(bac)-1]
      flag = False
      for sset in self.S:
         for element in sset:
            if bac in element:
               flag = True
      if (not flag):
         meandict.append((meancor[index], [bac]))
         index += 1
   
   #for element in meandict:
   #   for element2 in meandict:
   #      print(str(element[0])+"\t"+str(element[1])+"\t"+str(element2[0])+"\t"+str(element2[1]))
   #      print(element < element2)
   meandict.sort()
   for element in meandict:
      print(str(element[0])+"\t"+str(element[1]))

   overall = dict()
   overall['average'] = []
   for alg in cor:
      overall[alg] = []

   for bac in self.bacteria:
      bac = bac.strip()
      bac = bac[1:len(bac)-1]
      spot = 0
      while (spot < len(meandict)):
         flag = False
         if (len(meandict[spot][1]) > 1):
            for element in meandict[spot][1]:
               if bac in element:
                  flag = True      
         if flag or (len(meandict[spot][1]) == 1 and bac in meandict[spot][1]):
            if (meandict[spot][0] != len(self.bacteria)):
               overall['average'].append(len(self.bacteria)-(spot+1))
            else:
               overall['average'].append(0)
         spot += 1
      for alg in cor:
            if bac in self.iter_results[alg]:
               overall[alg].append(len(self.bacteria)-self.iter_results[alg][bac])
            else:
               overall[alg].append(0) 

   #for alg in cor:
   #   results = spearmanr(overall['average'], overall[alg])
   #   PyPluMA.log("Correlation between MATria and "+alg+": "+str(results[0]))

   PyPluMA.log("*************************************************************************************************")


