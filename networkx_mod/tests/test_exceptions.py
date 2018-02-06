from nose.tools import raises
import networkx_mod as nx

# smoke tests for exceptions

@raises(nx.NetworkXException)
def test_raises_networkx_mod_exception():
    raise nx.NetworkXException

@raises(nx.NetworkXError)
def test_raises_networkx_mod_error():
    raise nx.NetworkXError

@raises(nx.NetworkXPointlessConcept)
def test_raises_networkx_mod_pointless_concept():
    raise nx.NetworkXPointlessConcept

@raises(nx.NetworkXAlgorithmError)
def test_raises_networkx_mod_algorithm_error():
    raise nx.NetworkXAlgorithmError

@raises(nx.NetworkXUnfeasible)
def test_raises_networkx_mod_unfeasible():
    raise nx.NetworkXUnfeasible

@raises(nx.NetworkXNoPath)
def test_raises_networkx_mod_no_path():
    raise nx.NetworkXNoPath

@raises(nx.NetworkXUnbounded)
def test_raises_networkx_mod_unbounded():
    raise nx.NetworkXUnbounded

