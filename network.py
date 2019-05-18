# classes relating to the networked model

class Node(object):
    # a Node object represents a hydrologic demand node
    # it combines agricultural and urban water use cases

    # crop water demands, in meters per growing cycle
    crop_needs = {
        'none':      0.00,
        'rice':      1.25,
        'sugarcane': 2.00,
        'pulses':    0.35,
        'wheat':     0.55,
        'maize':     0.65
    }

    # water scarcity theshold, in cubic meters per annum per capita
    scarcity_threshold = 1700.0

    # constructor takes:
    #   identifying name (string)
    #   crop type (string)
    #   irrigated area, in sq km (float)
    #   population (int)
    def __init__(self, name, crop, area, population):
        self.name = name
        self.crop = crop
        self.area = area
        self.population = population

        # compute water demand, in MCM / year
        # note that India uses half-year growing cycles, Kharif and Rabi
        agricultural_demand = crop_needs[crop] * area * 2
        urban_demand = population * scarcity_threshold / 1000000
        self.demand = agricultural_demand + urban_demand

class IrrDistrict(Node):
    # an IrrDistrict is a pure irrigation district
    # i.e. it is modeled with no people

    def __init__(self, name, crop, area):
        super().__init__(name, crop, area, 0)

class UrbArea(Node):
    # an UrbArea is a pure urban area
    # i.e. it is modeled with no crops

    def __init__(self, name, population):
        super().__init__(name, 'none', 0, population)

class Edge(object):
    # an Edge object represents a river reach

    # constructor takes:
    #   identifying name (string)
    #   volume flow rate (MCM / year)
    #   pollution index, fraction of water that is usable (float)
    # flow can be -1 if unknown
    def __init__(self, name, flow, pollution):
        self.name = name
        self.flow = flow
        self.pollution = pollution

class Graph(object):
    # a Graph represents a river basin network

    def __init__(self):
        self.nodes = []  # list of all node objects
        self.edges = {}  # dictionary of [(Edge, dst_name)] indexed by src_name
                         # TODO: add a weight for the water distribution?

    # add a Node object to this Graph
    def add_node(self, node):
        self.nodes += [node]
        self.edges[node] = []

    def add_nodes_from_list(self, node_list):
        for node in node_list:
            self.add_node(node)

    # add an Edge object to this Graph
    def add_edge(self, edge, src_name, dst_name):
        self.edges[src_name] += [(edge, dst_name)]

    def add_edges_from_list(self, edge_list):
        for edge, src_name, dst_name in edge_list:
            self.add_edge(edge, src_name, dst_name)

    # find a node object by name
    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    # find a Node's parent Nodes
    def get_parents(self, node):
        parents = []
        for key, val in self.edges.items():
            _, dst_name = val
            if dst_name == node.name:
                parents += self.get_node(key)
        return parents

    # find a Node's child Nodes
    def get_children(self, node):
        children_names = [dst_name for _, dst_name in self.edges[node.name]]
        return [self.get_node(name for name in children_names)]

    # apply a constant demand offset to each Node in this Graph
    # this can be used to, for instance, simulate drawing from an aquifer
    # if distributed, the offset is proportionally handed out to the nodes
    #   by default, it is handed out as a constant to all nodes
    def apply_constant_offset(self, offset, distributed=False):
        net_demand = sum([node.demand for node in self.nodes])
        for node in self.nodes:
            if distributed:
                node.demand += (node.demand / net_demand) * offset
            else:
                node.demand += offset

    # apply a demand offset for each node per irrigated area
    # this can be used to, for instance, simulate precipitation
    def apply_area_offset(self, offset_per_area):
        for node in self.nodes:
            node.demand += node.area * offset_per_area_

    # solve for the flow through a given Edge
    # if the flow is unknown, we recursively back-trace, solving as we go
    def get_flow(self, edge):

        # if flow is known a priori, return that
        # this may cause an infinite loop if demand exceeds supply
        # we will avoid that with a check later
        if edge.flow > 0:
            return edge.flow

        # find this edge's source Node
        source = None
        for key, val in self.edges.items():
            e, _ = val
            if e.name == edge.name:
                source = self.get_node(key)
                break
        if source is None:
            raise('Edge not found in graph')

        # find all outflow Edges of that source Node
        # this should include the original argument 'edge'
        outflows = [e for e, _ in self.edges[source.name]]

        # find all inflow Edges of that source Node
        inflows = []
        for key, val in self.edges.items():
            e, d = val
            if d == source.name:
                inflows += [e]

        # recursively get all volume inflows of this node
        vol_inflows = [self.get_flow(f) for f in inflows]

        # pollution indices of all inflows
        pol_inflows = [f.pollution for f in inflows]

        # sort inflow data by pollution index and compute net outflow
        # the methodology is presented in Section 5 of our paper
        inflow_data = sorted(zip(vol_inflows, pol_inflows), key=lambda x: x[1])
        D = source.demand
        total_draw = 0
        for vol, pol in inflow_data:
            draw = min(vol, D / pol)
            D = D - draw * pol
            total_draw += draw
        net_outflow = sum(vol_inflows) - total_draw

        if net_outflow < 0:
            raise('Water supply could not be solved at node [%s]' % source.name)

        # since we do not have historical data, divide the outflows evenly
        for o in outflows:
            o.flow = net_outflow / len(outflows)
        return edge.flow

    # clear all the flows after solving
    # this resets all Edge flows to -1
    # this should be doable from the outside, since Edges are just references,
    # but it's more convenient to do here
    def clear_all_flows(self):
        for _, val in self.edges.items():
            edge, _ = val
            edge.flow = -1
