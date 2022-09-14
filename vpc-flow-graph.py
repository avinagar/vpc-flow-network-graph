import pandas as pd
import networkx as nx
from pyvis.network import Network
from datetime import datetime
import awswrangler as wr


# Get the current time
starttime = datetime.now()

# Path for known IPs file
knownips = "knownips.csv"

# Athena query to perform
query = "SELECT srcaddr, dstaddr, srcport, dstport, COUNT(*) AS Requests FROM vpcflowlogs \
WHERE action = 'ACCEPT' AND log_status = 'OK' and start > 1659312000 \
GROUP BY srcaddr, dstaddr, srcport, dstport \
ORDER BY Requests DESC \
LIMIT 10000"

print(f"Performing the following athena query:\n{query}")

# Save query result to a dataframe
# This will create temp files in Athena Query result bucket. If you want to delete those files add parameter keep_file=False
athena_results_df = wr.athena.read_sql_query(sql=query, database="default")

# Load knownips to a dataframe
iplist_df = pd.read_csv(knownips)

# Merge both the dataframes
joined = athena_results_df.merge(iplist_df, how='left', left_on='srcaddr', right_on='IP')
joined = joined.merge(iplist_df, how='left', left_on='dstaddr', right_on='IP')

# Drop unwanted columns
joined = joined.drop(columns=['IP_x', 'IP_y'])

# Fill all the blank values with the actual IP address
namex = joined.Name_x.fillna(joined.srcaddr)
namey = joined.Name_y.fillna(joined.dstaddr)

# Concat both the dataframes
joined = pd.concat([namey, joined], axis = 1)
joined = pd.concat([namex, joined], axis = 1)

# Drop unwanted columns
joined = joined.drop(columns=['srcaddr', 'dstaddr'])

# Rename the column names according to need
joined.columns = ['srcaddr', 'dstaddr', 'srcport', 'dstport', 'Requests', 'Name_x', 'Name_y']

# Drop unwanted columns
joined = joined.drop(columns=['Name_x', 'Name_y'])

# Create the network graph
net = Network(height=600, width=1350)

# Change the node distance and spring lenght
net.repulsion(node_distance=150, spring_length=300)

# Combine all the required fields
edge_data = zip(joined['srcaddr'], joined['dstaddr'], joined['Requests'], joined['srcport'], joined['dstport'])

# Create node and edges
for edge in edge_data:
    src = edge[0]
    dst = edge[1]
    weight = int(edge[2])
    srcprt = int(edge[3])
    dstprt = int(edge[4])
    net.add_node(src, src, title=f'({src}:{srcprt})\n Neighbours:\n')
    net.add_node(dst, dst, title=f'({dst}:{dstprt})\n Neighbours:\n')
    net.add_edge(src, dst, value=weight)

# Get the neighbours of the node
neighbor_map = net.get_adj_list()
for node in net.nodes:
    node['title'] += ('\n').join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])

# Save the graph with your desired name and location
net.save_graph("graph.html")

# Get current time
endtime = datetime.now()

# Print the total time taken for execution
timedifference = (endtime - starttime).total_seconds()
print(f'Total time taken: {timedifference} seconds')
