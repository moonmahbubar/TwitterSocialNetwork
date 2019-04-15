#Put all the cookbook functions in a seperate file.
import cookbook 
#Import graph and plotting tools.
import networkx as nx 
import matplotlib.pyplot as plt

#Initialize graph
graph = nx.Graph()

#Authenticate with twitter api.
twitter_api = cookbook.oauth_login()

#Screen name of user, and convert it to their user_id.
screen_name = "ItzJustKat"
user_id = str(twitter_api.users.show(screen_name=screen_name)['id'])
#Function that returns the list of users reciprocal friends sorted by most popular friend.
#Modify to allow option between screen_name and user_id.
def get_reciprocal_ids(twitter_api, user_id, friends_limit = 5000, followers_limit = 5000):
    #Get friend IDs, and follower IDs.
    friends_ids, followers_ids = cookbook.get_friends_followers_ids(twitter_api, 
                                                        user_id=user_id, 
                                                        friends_limit=friends_limit, 
                                                        followers_limit=followers_limit)

    #Find reciprocal friends (list of ids not screen names)
    reciprocal_friends = list(set(friends_ids) & set(followers_ids))

    #Store user profile information of reciprocal friends.
    reciprocal_info = cookbook.get_user_profile(twitter_api, user_ids=reciprocal_friends)

    #Create a dictionary of reciprocal friends id and follower count. key = id and val = follower count.
    reciprocal_dict = {reciprocal_id:reciprocal_info[reciprocal_id]['followers_count'] for reciprocal_id in reciprocal_info.keys()}

    #Sort the dictionary by follower count in descending order.
    reciprocal_dict = {k:v for k,v in sorted(reciprocal_dict.items(), key=lambda val: val[1], reverse=True)}

    #Return the reciprocal friends ids as a list.
    return list(reciprocal_dict.keys())

#Main
if __name__== "__main__":
    #Add initial user as a node.
    graph.add_node(user_id)

    #Get five most popular reciprocal friends.
    reciprocal_popular_ids = get_reciprocal_ids(twitter_api, user_id)[0:5]

    #Add reciprocal friends as nodes.
    graph.add_nodes_from(reciprocal_popular_ids)

    #Create a list of edges from user to their reciprocal friends.
    edges = [(user_id, reciprocal) for reciprocal in reciprocal_popular_ids]
    graph.add_edges_from(edges)

    #List of reciprocal ids.
    ids = next_queue = reciprocal_popular_ids
    num_nodes = len(reciprocal_popular_ids) + 1
    max_nodes = 100

    #Ensure there are at least a 100 nodes. Modified the basic crawler provided in lecture (CIS400)
    while num_nodes <= max_nodes:
        (queue, next_queue) = (next_queue, [])
        for id in queue:
            ##Add id as a node.
            graph.add_node(id)
            #Get five most popular reciprocal friends for id in the queue.
            response = get_reciprocal_ids(twitter_api, id)
            #Cut down to five most popular reciprocal friends. (Added case if less than 5).
            response = response[0:min(5,len(response))]
            #Add the reciprocal friends as nodes.
            graph.add_nodes_from(response)
            #Create pairs of edges.
            edges = [(id, reciprocal) for reciprocal in response]
            #Add edges.
            graph.add_edges_from(edges)
            #Keep count of number of nodes.
            num_nodes += len(response)
            #Set the response as the next in queue.
            next_queue += response
        #add next queue to list of ids.
        ids += next_queue

    #Draw graph and save it as an adjacency list.
    nx.draw(graph)
    nx.write_adjlist(graph,"out.adjlist")
    plt.show()
    #Calculations are done in calculations.py based on 'out.adjlist'. 
    #Doing the calculation seperately helps lower computation time.


