## Interface ##

Run the MBTA prompt by running 

`python cli.py`

At this point, there will be a persistent prompt in which you can run ? or help 
to see documentation for the available commands. These are:

* Question 1: list\_routes
  * Lists all subway routes
* Question 2: route\_stats
  * Lists various route stats including information about the routes with the most and least stops as well as the stops which connect multiple routes. For conciseness, stops which only connect various Green Line routes are omitted as these are effectively only on one route.
* Question 3: routes\_between\_stops STOP\_1 STOP\_2
  * Lists routes which can be traversed in order to go from STOP\_1 to STOP\_2. This function looks for the shortest route in terms of number of route transfers, not in terms of total stops travelled. Depending on the commuter in question, either of these methods could be considered optimal.
  
Results from API calls are cached for up to a minute after retrieval to minimize API calls. This may lead to slightly stale information if the MBTA route has very recently changed.

## Code Structure ##

Command prompt parsing in cli.py
Main coding functionality in mbta.py
Tests in tests.py
  
## Design Discussion ##

### Question 1 ###
The main design choice here was whether to use the API's filtering method or to fetch all routes and filter locally. I chose to use the API's filtering capability for 3 reasons: 

1. This requires the sending of less total data over a network. This isn't a huge deal here, but network capacity could be a limiting factor if this were to be largely scaled up.
2. I believe it's more likely that MBTA would change the format of data returned than that they would change their API interface. I would hope they wouldn't change either too often, but this seems slightly safer.
3. Using their filtering means we have less code in our code base. Less code means easier maintenance!

### Question 2 ###

Here, the main consideration I had was for how to treat the various Green Line routes. I generally did want to keep these distinct because they do have unique stops, and you would have to transfer if going between unique stops on different Green Line routes. However, I felt like it would be overly verbose to specify stops with mulitple routes if those multiple routes are all Green Line routes, so I chose to omit these from the output. For stops which connect non Green Line routes to the multiple Green Line routes, I do list everything however. This could be easily modified if desired.

### Question 3 ###

For this question, I took the approach of ignoring stops and only really focusing on the routes the stops were part of. This made for a fairly easy implementation as I could convert routes to vertices in a graph data structure and treat connecting stations as edges, then just run BFS to find the shortest path. 

To account for the fact that the start or end could be a connecting station which belongs to multiple routes, I run the BFS for every combination of start and end route and check which is shortest before returning. 

This method optimizes for minimum number of transfers and not mininum number of stops. For example, going from Chinatown to Boyleston could take 3 stops on Orange, Red, Green or 6 stops on Orange, Green, and my system would return the latter. However, given the unpredictability of transfer timing, some commuters may prefer this.

### Caching and Prompt vs Command ###

As I was running this, I noticed the slowest part of the program was waiting for API calls to return. given the fact that the MBTA map changes very infrequently, I wrote a simple cache to hold retrieved API values that we have fetched within the last minute. To maximize the effectiveness of this cache, I decided to set this up as a prompt instead of commands run in a one-off fashion. 
