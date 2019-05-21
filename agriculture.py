# simulating different water-savling agricultural things

from model import KharifGangesModel as kgm, \
                  KharifCrops as kc, \
                  KharifRivers as kr

# target groups for study
groups = {
    'base': [],
    'AB': [kc.A, kc.B],
    'LM': [kc.L, kc.M],
    'CDE': [kc.C, kc.D, kc.E],
    'FG': [kc.F, kc.G],
    'INJ': [kc.I, kc.J],
    'HK': [kc.H, kc.K],
    'blanket': list(map(lambda x: x[1],
                        filter(lambda x: x[0] in [c for c in 'ABCDEFGHIJKLMN'],
                               vars(kc).items())))
}

base = 0
for key, val in groups.items():
    kgm.clear_all_flows()
    boni = []
    area = 0
    for district in val:
        # record additional offsets that are difficult to re-compute
        bonus = district.demand - district.compute_demand()

        # re-compute this district's water demand with the coefficient
        district.compute_demand(a=0.776)
        district.demand += bonus
        boni += [bonus]
        area += district.area
    kgm.get_flow(kr.OUT)
    if key == 'base':
        base = kr.OUT.flow
        area = 1
    delta = kr.OUT.flow - base
    print('%s: %s, %f' % (key, kr.OUT.flow, delta / area))

    # restore the original for the next analysis group
    for bonus, district in zip(boni, val):
        district.compute_demand()
        district.demand += bonus

