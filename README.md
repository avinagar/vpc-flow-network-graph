
# vpc-flow-network-graph

A python program that creates the network graph from VPC flow logs for the analysis.
It uses awswrangler for performing the Athena Query to get the VPC Flow logs.
Pandas is used to deal with large data. For graph generation pyvis python module is used.
KnownIPs list can be passed for the easy analysis.



## Prerequisite
- pip installed
- aws cli configured with proper permissions


## Installation

Clone the Github repo and install the requirements.

```
  git clone https://github.com/avinagar/vpc-flow-network-graph.git
  cd vpc-flow-network-graph
  pip install -r requirements.txt
```

## Documentation

[pyvis](https://pyvis.readthedocs.io/en/latest/index.html)
[AWS-Data-Wrangler](https://aws-sdk-pandas.readthedocs.io/en/stable/api.html)


You can also modify the program according to your need using above documentation.
