def parse_carto(file_name):
    file = open(file_name).readlines()
    edges = []
    nb_nodes = int(file[0].split(" ")[-2])
    for line in file[1:]:
        line_split = line.split("\n")[0].split(" ")
        edges.append((int(line_split[1]), int(line_split[2])))
    return nb_nodes, edges
