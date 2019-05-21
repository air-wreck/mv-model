# sensitivity analysis

from model import KharifGangesModel as kgm, \
                  KharifCrops as kc, \
                  KharifRivers as kr

# establish base case
def change_none(delta):
    pass

# change the input flows
def change_inflows(delta):
    for _, reach in vars(kr).items():
        if reach.root:
            reach.flow *= delta

# change the cropping area
def change_areas(delta):
    for district in kgm.nodes:
        bonus = district.demand - district.compute_demand()
        district.area *= delta
        district.demand = district.compute_demand() + bonus

# change the pollution indices
def change_pollution(delta):
    for _, reach in vars(kr).items():
        reach.pollution *= delta

# change populations
def change_population(delta):
    for node in kgm.nodes:
        bonus = node.demand - node.compute_demand()
        node.population *= delta
        node.demand = node.compute_demand() + bonus

# change rainfall
def change_rainfall(delta):
    kgm.apply_area_offset(+kc.rainfall)
    kc.rainfall *= delta
    kgm.apply_area_offset(-kc.rainfall)

# run a sensitivity analysis, given a change function
def sensitivity_analysis(delta_f, level):
    kgm.get_flow(kr.OUT)
    old = kr.OUT.flow
    kgm.clear_all_flows()
    delta_f(level)
    kgm.get_flow(kr.OUT)
    print((kr.OUT.flow - old) / old)

# do analysis by changing this line and running script
# it isn't pretty, but this project is due tomorrow
sensitivity_analysis(change_rainfall, 0.95)

