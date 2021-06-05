from cmd import Cmd
from mbta import list_routes, route_stats, routes_between_stops

class MbtaPrompt(Cmd):
    prompt = 'mbta> '
    intro = "Type ? to list commands"

    def do_list_routes(self, inp):
        '''
        This function lists all MBTA routes which have type "Light Rail" or
        "Heavy Rail", both of which we consider "subways"
        '''
        print("List of all subway routes:")
        print(list_routes())

    def do_route_stats(self, inp):
        '''
        This function lists some route statistics including:
        - route with fewest stops
        - route with most stops
        - all stops which are part of multiple routes (and what those are)
        '''
        print(route_stats())

    def do_routes_between_stops(self, inp):
        '''
        Given a start and end stop, this function provides a route between them
        as specified by the series of routes that would need to be taken.

        Provide the two stops space separated after the command name as follows:
        routes_between_stops Ashmont Arlington
        '''
        args = inp.split()
        if len(args) != 2:
            print("please provide exactly 2 stops")
        else:
            print(routes_between_stops(args[0], args[1]))


    def do_exit(self, inp):
        '''exit the application'''
        return True

MbtaPrompt().cmdloop()
