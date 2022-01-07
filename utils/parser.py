def parse_carto(file_name):
    file = open(file_name)
    edges = []
    nb_nodes = file.readlines()[0].split(" ")[-2]
    for line in file.readlines()[1:]:
        line_split = line.split(" ")
        edges.append((line_split[1], line_split[2]))
    return nb_nodes, edges
