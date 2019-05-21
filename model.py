# the actual math model

from network import UrbArea, Node, Edge, Graph
from crops import CropPattern, KharifCrops, RabiCrops

# cities --- exist for both models
U2 = UrbArea('U-2', 2765348)  # Kanpur
U3 = UrbArea('U-3', 1112544)  # Allahabad
U4 = UrbArea('U-4', 2817105)  # Lucknow
U5 = UrbArea('U-5', 1198461)  # Varanasi

# dummy source/destination node for external flow
EXTERN = Node('EXTERN', 'none', 0, 0)

# base river reaches --- exist for both models
class BaseRivers(object):
    def __init__(self):
        self.Y1 = Edge('Y-1', -1, 0.9)    # Yamuna
        self.Y2 = Edge('Y-2', -1, 0.44)
        self.Y3 = Edge('Y-3', -1, 0.44)
        self.Y4 = Edge('Y-4', -1, 0.44)
        self.Y5 = Edge('Y-5', -1, 0.44)
        self.Y6 = Edge('Y-6', -1, 0.44)
        self.Y7 = Edge('Y-7', -1, 0.44)
        self.Ga1 = Edge('Ga-1', -1, 0.53)  # Ganges
        self.Ga2 = Edge('Ga-2', -1, 0.53)
        self.Ga3 = Edge('Ga-3', -1, 0.53)
        self.Ga4 = Edge('Ga-4', -1, 0.53)
        self.Ga5 = Edge('Ga-5', -1, 0.53)
        self.Ga6 = Edge('Ga-6', -1, 0.53)
        self.Ga7 = Edge('Ga-7', -1, 0.53)
        self.Ga8 = Edge('Ga-8', -1, 0.53)
        self.Go1 = Edge('Go-1', -1, 0.53)  # Gomti
        self.Go2 = Edge('Go-2', -1, 0.53)
        self.Go3 = Edge('Go-3', -1, 0.53)
        self.Gh1 = Edge('Gh-1', -1, 0.67)  # Ghaghara
        self.Ag1 = Edge('Ag-1', -1, 0.44)  # Agra
        self.C1 = Edge('C-1', -1, 0.44)    # Chambal
        self.C2 = Edge('C-2', -1, 0.44)
        self.B1 = Edge('B-1', -1, 0.44)    # Betwa
        self.B2 = Edge('B-2', -1, 0.44)
        self.K1 = Edge('K-1', -1, 0.53)    # Ken
        self.K2 = Edge('K-2', -1, 0.53)
        self.H1 = Edge('H-1', -1, 0.54)    # Hoghly
        self.S1 = Edge('S-1', -1, 0.54)    # Son

        # pseudo-reaches for computations
        self.Ga0 = Edge('Ga-0', -1, 0.53)
        self.Gh0 = Edge('Gh-0', -1, 0.53)
        self.OUT = Edge('OUT', -1, 1)

# generate a generic Ganges basin network topology
# accepts a cropping season as the input
def populate_network(model, Crops, Rivers):
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
        (Rivers.Y1, EXTERN, Crops.A),
        (Rivers.Y2, Crops.A, Crops.L),
        (Rivers.Y3, Crops.L, Crops.M),
        (Rivers.Y4, Crops.M, U2),
        (Rivers.Y5, Crops.C, Crops.D),
        (Rivers.Y6, Crops.D, Crops.E),
        (Rivers.Y7, Crops.E, U3),
        (Rivers.Ga0, EXTERN, Crops.L),
        (Rivers.Ga1, Crops.B, U2),
        (Rivers.Ga2, Crops.F, U3),
        (Rivers.Ga3, Crops.H, Crops.N),
        (Rivers.Ga4, Crops.N, Crops.J),
        (Rivers.Ga5, U2, Crops.F),
        (Rivers.Ga6, U3, U5),
        (Rivers.Ga7, U5, Crops.H),
        (Rivers.Ga8, Crops.L, Crops.B),
        (Rivers.Go1, Crops.G, Crops.H),
        (Rivers.Go2, U4, Crops.G),
        (Rivers.Go3, U2, U4),
        (Rivers.Gh0, EXTERN, Crops.I),
        (Rivers.Gh1, Crops.I, Crops.N),
        (Rivers.Ag1, EXTERN, Crops.L),
        (Rivers.C1, Crops.M, Crops.C),
        (Rivers.C2, EXTERN, Crops.C),
        (Rivers.B1, Crops.M, Crops.D),
        (Rivers.B2, EXTERN, Crops.D),
        (Rivers.K1, Crops.F, Crops.E),
        (Rivers.K2, EXTERN, Crops.E),
        (Rivers.H1, Crops.J, Crops.K),
        (Rivers.S1, EXTERN, Crops.H),
        (Rivers.OUT, Crops.K, EXTERN)
    ])

    # apply the aquifer offset
    model.apply_constant_offset(-20480.61103, distributed=True)

    # apply rainfall offset
    model.apply_area_offset(-Crops.rainfall)

    # apply rest of population to fields
    districts = filter(lambda x: issubclass(x.__class__, Node),
                       [k for _, k in vars(Crops).items()])
    total_area = sum([d.area for d in districts])
    pop_density = 66308416.96 / total_area
    model.apply_area_offset(pop_density * Node.scarcity_threshold / 1000000)

# Kharif season model
KharifRivers = BaseRivers()
KharifRivers.Y1.flow = 93094.92
KharifRivers.Ga0.flow = 525370.9248
KharifRivers.Gh0.flow = 946728
KharifRivers.K2.flow = 9800
KharifRivers.B2.flow = 21000
KharifRivers.S1.flow = 5000
KharifRivers.C2.flow = 5000
KharifRivers.Ag1.flow = 5000

KharifGangesModel = Graph()
populate_network(KharifGangesModel, KharifCrops, KharifRivers)
KharifGangesModel.set_root()

# Rabi season model
RabiRivers = BaseRivers()
RabiRivers.Y1.flow = 93094.92
RabiRivers.Ga0.flow = 525370
RabiRivers.Gh0.flow = 24357.224
RabiRivers.K2.flow = 9800
RabiRivers.B2.flow = 21000
RabiRivers.S1.flow = 5000
RabiRivers.C2.flow = 5000
RabiRivers.Ag1.flow = 5000

RabiGangesModel = Graph()
populate_network(RabiGangesModel, RabiCrops, RabiRivers)
RabiGangesModel.set_root()

if __name__ == '__main__':
    print('=== Kharif Season Simulation ===')
    KharifGangesModel.get_flow(KharifRivers.OUT)
    print(KharifGangesModel.report())
    # print()
    # print('=== Rabi Season Simulation ===')
    # RabiGangesModel.get_flow(RabiRivers.OUT)
    # print(RabiGangesModel.report())

