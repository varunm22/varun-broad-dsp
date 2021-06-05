import unittest
from mbta import list_routes, route_stats, routes_between_stops

class TestMbtaMethods(unittest.TestCase):
    def test_list_routes(self):
        self.assertEqual(list_routes(), "Red Line, Mattapan Trolley, Orange Line, Green Line B, Green Line C, Green Line D, Green Line E, Blue Line")

    def test_route_stats(self):
        self.assertEqual(route_stats(), '''Fewest stops: Mattapan Trolley with 8 stops
Most stops: Green Line B with 23 stops

Stops with mulitple routes:
Park Street: Red Line, Green Line B, Green Line C, Green Line D, Green Line E
Downtown Crossing: Red Line, Orange Line
Ashmont: Red Line, Mattapan Trolley
State: Orange Line, Blue Line
Haymarket: Orange Line, Green Line C, Green Line E
North Station: Orange Line, Green Line C, Green Line E
Government Center: Green Line C, Green Line D, Green Line E, Blue Line''')

    def test_route_path_single_route(self):
        self.assertEqual(routes_between_stops("Broadway", "Ashmont"), "Red Line")

    def test_route_path_two_routes(self):
        self.assertEqual(routes_between_stops("Arlington", "Ashmont"), "Green Line B, Red Line")

    def test_route_path_three_routes(self):
        self.assertEqual(routes_between_stops("Broadway", "Airport"), "Red Line, Green Line C, Blue Line")

    def test_route_path_connecting_stations(self):
        self.assertEqual(routes_between_stops("State", "Park Street"), "Orange Line, Red Line")

if __name__ == '__main__':
    unittest.main()
