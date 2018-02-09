# MATria
# Language: Python
# Dependencies: Requires modified networkx libraries (included in networkx_mod)
#               Also requires numpy 1.13 or higher
# Input: CSV (network)
# Output: NOA (central nodes and centrality values)
# Tested with: PluMA 1.0, Python 2.7

PluMA plugin to run the Multiple Ablatio Triadum (Cickovski et al, 2017) algorithm for centrality.
The plugin expects an input network in the form of a CSV file, where rows and columns both
represent nodes and entry (i, j) corresponds to the weight of the edge from node i to node j.
The plugin produces centrality values in an output NOde Attribute (NOA) file, which can then
be imported into Cytoscape for downstream analysis or visualization.

Note that this plugin includes some additional libraries:

networkx_mod: A minimally modified version of networkx (http://networkx.github.io), with shortest path
functionality modified to accomodate negative edges and use edge products.  NetworkX is under
the open source 3-clause BSD license (included here), (C) 2004 NetworkX Developers.

PageTrust: Also minimally modified, mainly to remove hardcoded test cases.  Original form hosted
by Github at https://github.com/takahiroanno/pagetrust/blob/master/pagetrust.py. 

PNCentrality: Python library developed by Trevor Cickovski to implement PN-Centrality, validated
against the results of Everett and Borgatti, 2014.
