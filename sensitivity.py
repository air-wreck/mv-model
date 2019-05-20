# sensitivity analysis

from model import KharifGangesModel, RabiGangesModel, \
                  KharifRivers, RabiRivers, KharifCrops, RabiCrops

def get_flows(rivers):
    return [(reach.name, reach.flow) for _, reach in vars(rivers).items()]

def sensitivity_analysis(model, rivers, delta=1.1):
    # adjust each pollution index by +/- 10% and see effect on outflows

    # base flow for comparison
    model.get_flow(rivers.OUT)
    flows = {'base': get_flows(rivers)}

    # adjust each pollution by indicated delta
    for _, reach in vars(rivers).items():
        model.clear_all_flows(skip=[rivers.Y1, rivers.Ga0, rivers.Gh0])
        reach.pollution *= delta
        model.get_flow(rivers.OUT)
        flows[reach.name] = get_flows(rivers)
        reach.pollution /= delta

    # compute the pct flow change in a given reach
    def find_change(data):
        old, new = data
        return (new[1] - old[1]) / old[1]

    # return the average percent flow change and max percent flow change
    result = {}
    for key, val in flows.items():
        changes = list(map(find_change, zip(flows['base'], val)))
        avg_change = sum(changes) / len(changes)
        max_change = max(zip(changes, [x[0] for x in flows['base']]),
                         key=lambda x: abs(x[0]))
        result[key] = (avg_change, max_change)
    return result

result = sensitivity_analysis(KharifGangesModel, KharifRivers, delta=1.1)
for key, val in result.items():
    print('%s: %.3f %.3f (%s)' % (key, val[0], val[1][0], val[1][1]))

