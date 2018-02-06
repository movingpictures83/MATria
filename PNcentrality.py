import numpy

# Change as necessary
#myfile = "examples/mixedtie.csv"
#myfile = "examples/triad.csv"
#myfile = "examples/mostextreme.csv"
#myfile = "examples/mostextreme_rivals.csv"
#myfile = "examples/Level1Clusters_Active_Size_2_1_Inf_2_2_P_0.01_InnerSortedCorrelations.csv"
#myfile = "examples/COPD.pvalued.csv"
#myfile = "examples/Never/Never_9A/Never.pvalued.csv"
#myfile = "examples/Social_networks/Karate/karate.csv"

#f = open(myfile, 'r')

# Get the first line (names)
#firstline = f.readline()
#bacteria = firstline.split(',')
#bacteria.remove('\"\"')

def pncentrality(bacteria, G):
 n = len(bacteria)
 m = numpy.zeros([n, n])
 bacteria[len(bacteria)-1] = bacteria[len(bacteria)-1].strip()
 for key in G.adj:
    for key2 in G.adj[key]:
       # TMC need to fix this, breaks for either CSV or GML
       if (bacteria[0].count("\"") == 0):
          index1 = bacteria.index(key)
          index2 = bacteria.index(key2)
       else:
          index1 = bacteria.index("\""+key+"\"")
          index2 = bacteria.index("\""+key2+"\"")
       w = G.adj[key][key2]['weight']
       m[index1][index2] = w
       m[index2][index1] = w
 # Make the identity matrix I
 # and the adjacency matrix A
 # and the positive matrix P
 # and the negative matrix N
 #m = []
 p = []
 nv = []
 z = []
 for i in range(n):
   #mc = []
   zc = []
   pc = []
   nc = []
   #contents = line.split(',')
   for j in range(n):
      value = float(m[i][j])
      #mc.append(value)
      zc.append(0)
      if (value > 0):
         pc.append(value)
         nc.append(0)
      else:
         pc.append(0)
         nc.append(-value)
   #m.append(mc)
   z.append(zc)
   p.append(pc)
   nv.append(nc)

 # Check to make sure all entries (i, i) are 0
 for i in range(n):
   m[i][i] = 0
   p[i][i] = 0
   nv[i][i] = 0

 # Added TMC December 23, 2014
 onemat = []
 for i in range(n):
   omc = []
   for j in range(n):
      omc.append(1)
   onemat.append(omc)
 OneMatrix = numpy.matrix(onemat)     


 ADJ = numpy.matrix(m)
 P = numpy.matrix(p)
 N = numpy.matrix(nv)
 #A = P - 2*N

 A = P - 2*N

 for i in range(n):
   z[i][i] = 1
 I = numpy.matrix(z)

 # Make the vector of ones
 Ones = []
 for i in range(n):
   Ones.append([1])
 O = numpy.matrix(Ones)

 # Compute hStar (traditional centrality)
 print A
 print I - (1.0/(2*n-2))*A
 PN = ((I - (1.0/(2*n-2))*A).getI()) * O

 arr = PN.getA()
 retval = []
 for i in range(n):
    retval.append(arr[i][0])
 return retval
 #tuples = []
 #for i in range(n):
 #  tuples.append([arr[i][0], bacteria[i].strip()])

 #tuples.sort()
 #tuples.reverse()
 #from tabulate import tabulate
 #print tabulate(tuples, headers=["OTU","PN Centrality"])
#for i in range(n):
#   print tuples[i][1], "\t\t", tuples[i][0]
