#!/usr/bin/env python
from nose.tools import *
import networkx_mod

class TestBlock:

    def test_path(self):
        G=networkx_mod.path_graph(6)
        partition=[[0,1],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition)
        assert_equal(sorted(M.nodes()),[0,1,2])
        assert_equal(sorted(M.edges()),[(0,1),(1,2)])
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],1)
            assert_equal(M.node[n]['nnodes'],2)
            assert_equal(M.node[n]['density'],1.0)

    def test_multigraph_path(self):
        G=networkx_mod.MultiGraph(networkx_mod.path_graph(6))
        partition=[[0,1],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition,multigraph=True)
        assert_equal(sorted(M.nodes()),[0,1,2])
        assert_equal(sorted(M.edges()),[(0,1),(1,2)])
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],1)
            assert_equal(M.node[n]['nnodes'],2)
            assert_equal(M.node[n]['density'],1.0)

    def test_directed_path(self):
        G = networkx_mod.DiGraph()
        G.add_path(list(range(6)))
        partition=[[0,1],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition)
        assert_equal(sorted(M.nodes()),[0,1,2])
        assert_equal(sorted(M.edges()),[(0,1),(1,2)])
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],1)
            assert_equal(M.node[n]['nnodes'],2)
            assert_equal(M.node[n]['density'],0.5)

    def test_directed_multigraph_path(self):
        G = networkx_mod.MultiDiGraph()
        G.add_path(list(range(6)))
        partition=[[0,1],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition,multigraph=True)
        assert_equal(sorted(M.nodes()),[0,1,2])
        assert_equal(sorted(M.edges()),[(0,1),(1,2)])
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],1)
            assert_equal(M.node[n]['nnodes'],2)
            assert_equal(M.node[n]['density'],0.5)

    @raises(networkx_mod.NetworkXException)
    def test_overlapping(self):
        G=networkx_mod.path_graph(6)
        partition=[[0,1,2],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition)

    def test_weighted_path(self):
        G=networkx_mod.path_graph(6)
        G[0][1]['weight']=1
        G[1][2]['weight']=2
        G[2][3]['weight']=3
        G[3][4]['weight']=4
        G[4][5]['weight']=5
        partition=[[0,1],[2,3],[4,5]]
        M=networkx_mod.blockmodel(G,partition)
        assert_equal(sorted(M.nodes()),[0,1,2])
        assert_equal(sorted(M.edges()),[(0,1),(1,2)])
        assert_equal(M[0][1]['weight'],2)
        assert_equal(M[1][2]['weight'],4)
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],1)
            assert_equal(M.node[n]['nnodes'],2)
            assert_equal(M.node[n]['density'],1.0)


    def test_barbell(self):
        G=networkx_mod.barbell_graph(3,0)
        partition=[[0,1,2],[3,4,5]]
        M=networkx_mod.blockmodel(G,partition)
        assert_equal(sorted(M.nodes()),[0,1])
        assert_equal(sorted(M.edges()),[(0,1)])
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],3)
            assert_equal(M.node[n]['nnodes'],3)
            assert_equal(M.node[n]['density'],1.0)

    def test_barbell_plus(self):
        G=networkx_mod.barbell_graph(3,0)
        G.add_edge(0,5) # add extra edge between bells
        partition=[[0,1,2],[3,4,5]]
        M=networkx_mod.blockmodel(G,partition)
        assert_equal(sorted(M.nodes()),[0,1])
        assert_equal(sorted(M.edges()),[(0,1)])
        assert_equal(M[0][1]['weight'],2)
        for n in M.nodes():
            assert_equal(M.node[n]['nedges'],3)
            assert_equal(M.node[n]['nnodes'],3)
            assert_equal(M.node[n]['density'],1.0)
        


