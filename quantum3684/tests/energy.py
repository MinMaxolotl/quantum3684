def energy(bs: BitString, G: nx.Graph):
    """Compute energy of configuration, `bs`

        .. math::
            E = \\left<\\hat{H}\\right>

    Parameters
    ----------
    bs   : Bitstring
        input configuration
    G    : Graph
        input graph defining the Hamiltonian
    Returns
    -------
    energy  : float
        Energy of the input configuration
    """
    Energy = 0
    bs.string = list(map(int, bs.string))

    # 0 = -1, 1 = 1
    for i in bs.string:
        if i == 0:
            bs.string[bs.string.index(i)] = -1

    #print(bs.string)

    
    
    orientation = bs.string  #Says whether it is up or down, list of node values

    #for x in G.edges:
    #    print(x)
    
    #size = bs.__len__

    # We want to multiply the interacting nodes together
    for e in G.edges:
        i_idx = e[0]
        j_idx = e[1]
        si = orientation[i_idx]
        sj = orientation[j_idx]

        sisj = si*sj
        Energy += sisj*(G.edges[e]['weight']) 

    # Converts -1 back to 0
    for i in bs.string:
        if i == -1:
            bs.string[bs.string.index(i)] = 0

    return Energy


