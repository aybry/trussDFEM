import testModels, json

i = 1
while i <= 5:
    next_func = 'truss' + str(i)
    [nodes, elements, bearings, loads, nodeTable, elemTable, A, E, poiss] = getattr(testModels, next_func)()
    nodes_json = '{"nodes": {'
    elements_json = '{"elements": {'
    bearings_json = '{"bearings": {'
    loads_json = '{"loads": {'
    i_running = 1
    for node in nodes:
        current_node = ('"' + str(int(node[0])) + '": [' + str(node[1]) + ',' + str(node[2]) + ']')
        if i_running < len(nodes):
            current_node += ', '
        nodes_json += current_node
        i_running += 1
    i_running = 1
    for elem in elements:
        current_elem = ('"' + str(int(elem[0])) + '": [' + str(elem[1]) + ',' + str(elem[2]) + ']')
        if i_running < len(elements):
            current_elem += ', '
        elements_json += current_elem
        i_running += 1
    i_running = 1
    for bear in bearings:
        current_bear = ('"' + str(int(bear[0])) + '": [' + str(bear[1]) + ',' + str(bear[2]) + ']')
        if i_running < len(bearings):
            current_bear += ', '
        bearings_json += current_bear
        i_running += 1
    i_running = 1
    for load in loads:
        current_load = ('"' + str(int(load[0])) + '": [' + str(load[1]) + ',' + str(load[2]) + ']')
        if i_running < len(loads):
            current_load += ', '
        loads_json += current_load
        i_running += 1
    nodes_json += '}}'
    elements_json += '}}'
    print(nodes_json, '\n', 
        elements_json, '\n',
        bearings_json, '\n',
        loads_json)
    with open('test_models.json', 'w') as f:
        f.write(json.dumps())
    print(getattr(next_func, ))
    i += 1