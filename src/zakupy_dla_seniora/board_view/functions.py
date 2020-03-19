def get_min_max_coordinates(radius, coord_value):
    km_in_degrees = 0.009
    min_coord_value = coord_value - (radius * km_in_degrees)
    max_coord_value = coord_value + (radius * km_in_degrees)
    return min_coord_value, max_coord_value



