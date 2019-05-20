# cropping data for Ganges River Basin, split by season

from network import Node, IrrDistrict

# Kharif (summer monsoon) season cropping patterns
class KharifCrops(object):
    # seasonal rainfall, in m / year
    # this assumes that the season is half a year
    rainfall = 0.84 * 2

    # Delhi urban area and Lower Ganges, Delhi irrigation district
    A = Node('A', 'sugarcane', 21842.448, 11034555)

    # Lower Ganges, Gomti
    B = IrrDistrict('B', 'rice', 27137.137)

    # Chambal-Sindh
    C = IrrDistrict('C', 'pulses', 2981.668)

    # Yamuna
    D = IrrDistrict('D', 'pulses', 7657.239)

    # Ken
    E = IrrDistrict('E', 'rice', 4076.266)

    # Kanpur, North
    F = IrrDistrict('F', 'rice', 14987.585)

    # Faizabad
    G = IrrDistrict('G', 'rice', 13754.304)

    # Son
    H = IrrDistrict('H', 'rice', 9435.343)

    # Gundak-Ghaghara
    I = IrrDistrict('I', 'rice', 13779.068)

    # Kosi
    J = IrrDistrict('J', 'rice maize', 15507.643)

    # Bengal Basin
    K = IrrDistrict('K', 'rice', 21105.402)

    # Lower Ganges, Aligarh
    L = IrrDistrict('L', 'sugarcane', 12922.21)

    # Lower Ganges, Ganga
    M = IrrDistrict('M', 'maize pulses', 21515.554)

    # Patna urban area and Patna irrigation district
    N = Node('N', 'sugarcane', 10822.165, 1684222)

# Rabi (winter) season cropping patterns
class RabiCrops(object):
    # seasonal rainfall, in m / year
    # this assumes that the season is half a year
    rainfall = 0.16 * 2

    # Delhi urban area and Lower Ganges, Delhi irrigation district
    A = Node('A', 'sugarcane', 21842.448, 11034555)

    # Lower Ganges, Gomti
    B = IrrDistrict('B', 'wheat', 27137.137)

    # Chambal-Sindh
    C = IrrDistrict('C', 'pulses', 2981.668)

    # Yamuna
    D = IrrDistrict('D', 'pulses', 7657.239)

    # Ken
    E = IrrDistrict('E', 'pulses', 4076.266)

    # Kanpur, North
    F = IrrDistrict('F', 'wheat pulses', 14987.585)

    # Faizabad
    G = IrrDistrict('G', 'wheat pulses', 13754.304)

    # Son
    H = IrrDistrict('H', 'wheat sugarcane pulses', 9435.343)

    # Gundak-Ghaghara
    I = IrrDistrict('I', 'sugarcane', 13779.068)

    # Kosi
    J = IrrDistrict('J', 'wheat', 15507.643)

    # Bengal Basin
    K = IrrDistrict('K', 'wheat', 21105.402)

    # Lower Ganges, Aligarh
    L = IrrDistrict('L', 'wheat', 12922.21)

    # Lower Ganges, Ganga
    M = IrrDistrict('M', 'wheat pulses', 21515.554)

    # Patna urban area and Patna irrigation district
    N = Node('N', 'sugarcane pulses', 10822.165, 1684222)

