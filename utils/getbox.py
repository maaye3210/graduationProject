def get_box(point1, point2):
    """
    :param point1:点一
    :param point2:点二
    :return:[north, south, east, west]
    """

    east = max(point1[1], point2[1])
    west = min(point1[1], point2[1])
    south = min(point1[0], point2[0])
    north = max(point1[0], point2[0])
    space_h = 0.2 * (north - south)
    space_l = 0.2 * (east - west)
    return north + space_h, south - space_h, east + space_l, west - space_l
