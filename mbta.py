import requests
from requests.auth import HTTPBasicAuth
import time
from collections import defaultdict
import itertools

cache = defaultdict(lambda:{"time":time.time(), "data": None})
headers = {'api_key': '4150ca5a315a4ed49e810ded5f96af08'}

def get_routes():
    cache_entry = cache["routes"]
    if cache_entry["data"] == None or (time.time() - cache_entry["time"] > 60):
        routes = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1", headers)
        cache["routes"] = {"time": time.time(), "data": routes}
    else:
        routes = cache_entry["data"]
    return routes

def get_stop_and_route_info():
    cache_entry = cache["stop_and_route_info"]
    if cache_entry["data"] == None or (time.time() - cache_entry["time"] > 60):
        routes = get_routes()
        ids_and_names = [(route['id'], route['attributes']['long_name'] ) for route in routes.json()['data']]
        stop_counts = []
        stops_to_routes = defaultdict(list)
        for (id, name) in ids_and_names:
            stops = requests.get("https://api-v3.mbta.com/stops?filter[route]=%s" %id, headers)
            stop_names = [stop['attributes']["name"] for stop in stops.json()['data']]
            stop_counts.append((len(stop_names), name))
            for stop in stop_names:
                stops_to_routes[stop].append(name)

        cache["stop_and_route_info"] = {
            "time": time.time(),
            "data": (stop_counts, stops_to_routes)
        }
    else:
        stop_counts, stops_to_routes = cache_entry["data"]
    return stop_counts, stops_to_routes

'''
Code for question 1
This function lists all MBTA routes which have type "Light Rail" or "Heavy Rail",
both of which we consider "subways"

'''
def list_routes():
    routes = get_routes()
    names = [route['attributes']['long_name'] for route in routes.json()['data']]
    return ", ".join(names)

'''
Code for question 2
This function lists some route statistics including:
- route with fewest stops
- route with most stops
- all stops which are part of multiple routes (and what those are)
'''
def route_stats():
    def all_green(stops):
        return all(s[:5] == "Green" for s in stops)
    stop_counts, stops_to_routes = get_stop_and_route_info()
    sorted_stop_counts = sorted(stop_counts)
    fewest_num_stops, fewest_stops_route = sorted_stop_counts[0]
    most_num_stops, most_stops_route = sorted_stop_counts[-1]
    stops_on_multiple_routes = {
        k:(', '.join(v))
        for (k,v) in stops_to_routes.items()
        if len(v) > 1 and any(s[:5] != "Green" for s in v)
    }

    return "\n".join([
        "Fewest stops: %s with %i stops"%(fewest_stops_route, fewest_num_stops),
        "Most stops: %s with %i stops"%(most_stops_route, most_num_stops),
        "\nStops with mulitple routes:\n%s"%("\n".join(
            ["%s: %s"%(route,stops) for (route, stops) in stops_on_multiple_routes.items()]
        ))
    ])

def list_to_pairs(s):
    return [(a,b) for idx, a in enumerate(s) for b in s[idx+1:]]

def bfs(start, end, vertices):
    q = [start]
    parents = {start: None}
    found = False
    while len(q)>0 and found == False:
        cur = q.pop(0)
        children = sorted(list(vertices[cur]))
        for child in children:
            if child == end:
                found = True
            if child not in parents:
                q.append(child)
                parents[child] = cur
    path = [end]
    cur = end
    while cur != start:
        cur = parents[cur]
        path.insert(0, cur)
    return path

'''
Code for question 3
Given a start and end stop, this function provides a route between them as
specified by the series of routes that would need to be taken.
'''
def routes_between_stops(stop_1, stop_2):
    stop_counts, stops_to_routes = get_stop_and_route_info()
    stops_on_multiple_routes = {k:v for (k,v) in stops_to_routes.items() if len(v) > 1}
    edge_set = set().union(*[set(list_to_pairs(s)) for s in stops_on_multiple_routes.values()])
    connected_lines = defaultdict(set)
    for v1, v2 in edge_set:
        connected_lines[v1].add(v2)
        connected_lines[v2].add(v1)

    assert(stop_1 in stops_to_routes)
    assert(stop_2 in stops_to_routes)
    stop_1_routes = stops_to_routes[stop_1]
    stop_2_routes = stops_to_routes[stop_2]
    start_end_route_combos = itertools.product(*[stop_1_routes, stop_2_routes])
    path_options = [bfs(r1, r2, connected_lines) for (r1, r2) in start_end_route_combos]
    path = min(path_options, key=len)

    return ", ".join(path)

