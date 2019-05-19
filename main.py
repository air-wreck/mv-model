# the actual math model

from network import UrbArea, Node, Edge, Graph
from crops import KharifCrops, RabiCrops

# cities --- exist for both models
U2 = UrbArea('U-2', 2765348)  # Kanpur
U3 = UrbArea('U-3', 1112544)  # Allahabad
U4 = UrbArea('U-4', 2817105)  # Lucknow
U5 = UrbArea('U-5', 1198461)  # Varanasi

# river reaches --- exist for both models
Y1 = Edge('Y-1', 50500, 0.8)    # Yamuna
Y2 = Edge('Y-2', -1, 0.8)
Y3 = Edge('Y-3', -1, 0.8)
Y4 = Edge('Y-4', -1, 0.8)
Y5 = Edge('Y-5', -1, 0.8)
Y6 = Edge('Y-6', -1, 0.8)
Y7 = Edge('Y-7', -1, 0.8)
Ga1 = Edge('Ga-1', -1, 0.8)  # Ganges
Ga2 = Edge('Ga-2', -1, 0.8)
Ga3 = Edge('Ga-3', -1, 0.8)
Ga4 = Edge('Ga-4', -1, 0.8)
Ga5 = Edge('Ga-5', -1, 0.8)
Ga6 = Edge('Ga-6', -1, 0.8)
Ga7 = Edge('Ga-7', -1, 0.8)
Go1 = Edge('Go-1', -1, 0.8)  # Gomti
Go2 = Edge('Go-2', -1, 0.8)
Go3 = Edge('Go-3', -1, 0.8)
Gh1 = Edge('Gh-1', -1, 0.8)  # Ghaghara
C1 = Edge('C-1', -1, 0.8)    # Chambal
B1 = Edge('B-1', -1, 0.8)    # Betwa
K1 = Edge('K-1', -1, 0.8)    # Ken
H1 = Edge('H-1', -1, 0.8)    # Hoghly

# pseudo-reaches for computations
Ga0 = Edge('Ga-0', 2209032, 0.8)
Gh0 = Edge('Gh-0', 946728, 0.8)
OUT = Edge('OUT', -1, 1)

# dummy source/destination node for external flow
EXTERN = Node('EXTERN', 'none', 0, 0)

# generate a generic Ganges basin network topology
# accepts a cropping season as the input
def populate_network(model, Crops):
    # add the irrigation districts and urban areas as nodes
    model.add_nodes_from_list([
        Crops.A, Crops.B, Crops.C, Crops.D, Crops.E, Crops.F, Crops.G,
        Crops.H, Crops.I, Crops.J, Crops.K, Crops.L, Crops.M, Crops.N
    ])
    model.add_nodes_from_list([U2, U3, U4, U5])

    # add the "special" node
    model.add_node(EXTERN)

    # add all the river reach segments
    model.add_edges_from_list([
        (Y1, EXTERN, Crops.A),
        (Y2, Crops.A, Crops.L),
        (Y3, Crops.L, Crops.M),
        (Y4, Crops.M, U2),
        (Y5, Crops.C, Crops.D),
        (Y6, Crops.D, Crops.E),
        (Y7, Crops.E, U3),
        (Ga0, EXTERN, Crops.B),
        (Ga1, Crops.B, U2),
        (Ga2, Crops.F, U3),
        (Ga3, Crops.H, Crops.N),
        (Ga4, Crops.N, Crops.J),
        (Ga5, U2, Crops.F),
        (Ga6, U3, U5),
        (Ga7, U5, Crops.H),
        (Go1, Crops.G, Crops.H),
        (Go2, U4, Crops.G),
        (Go3, U2, U4),
        (Gh0, EXTERN, Crops.I),
        (Gh1, Crops.I, Crops.N),
        (C1, Crops.M, Crops.C),
        (B1, Crops.M, Crops.D),
        (K1, Crops.F, Crops.E),
        (H1, Crops.J, Crops.K),
        (OUT, Crops.K, EXTERN)
    ])

    # apply the aquifer offset
    model.apply_constant_offset(-20480.61103, distributed=True)

    # apply rainfall offset
    model.apply_area_offset(-Crops.rainfall)

# Kharif season model
KharifGangesModel = Graph()
populate_network(KharifGangesModel, KharifCrops)
KharifGangesModel.get_flow(OUT)
for node in KharifGangesModel.nodes:
    node_type = 'Irrigation District' if node.area > 0 else 'Urban Area'
    print('%s: %s' % (node.name, node_type))
    for reach, _ in KharifGangesModel.edges[node.name]:
        print('  %s: [%.3f] %f MCM / year' % (reach.name,
                                              reach.pollution, reach.flow))

