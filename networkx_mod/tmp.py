
    push = maxheappush
    pop = maxheappop
    dist = {}  # dictionary of final distances
    #seen = {source: 0}
    seen = {source: 0}
    c = count()
    fringe = []  # use heapq with (distance,label) tuples
    #push(fringe, (0, next(c), source))
    push(fringe, (1, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if (v[len(v)-1] == '-'):
           dist[v] = -dist[v]
        # for ignore,w,edgedata in G.edges_iter(v,data=True):
        # is about 30% slower than the following
        if G.is_multigraph():
            edata = []
            for w, keydata in G[v].items():
                #minweight = min((dd.get(weight, 1)
                minweight = max((dd.get(weight, 1)
                                 for k, dd in keydata.items()))
                edata.append((w, {weight: minweight}))
        else:
            edata = iter(G[v].items())

        for w, edgedata in edata:
            #TMC modified
            #vw_dist = dist[v] + -math.log(abs(edgedata.get(weight, 1)))
            vw_dist = dist[v] * edgedata.get(weight, 1)
            if cutoff is not None:
                if vw_dist > cutoff:
                    continue
            if w in dist:
                if w[len(w)-1] == '+' and vw_dist > dist[w]:
                #if vw_dist < dist[w]:
                    print "Vw_dist is: ", vw_dist, " dist[w] is: ", dist[w], " Source: ", source, " v: ", v, " w: ", w
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
                if w[len(w)-1] == '-' and vw_dist < dist[w]:
                    print "Vw_dist is: ", vw_dist, " dist[w] is: ", dist[w], " Source: ", source, " v: ", v, " w: ", w
                    raise ValueError('Contradictory paths found:')
            #elif w not in seen or vw_dist < seen[w]:
            elif w not in seen or (w[len(w)-1] == '+' and vw_dist > seen[w]) or (w[len(w)-1] == '-' and vw_dist < seen[w]):
                seen[w] = vw_dist
                #push(fringe, (vw_dist, next(c), w))
                push(fringe, (abs(vw_dist), next(c), w))
    return dist

