# Laplacian Centrality

This python script is a part of my project, "LDPC: A Density-Based Clustering Algorithm", and implements Laplacian Centrality [1] which is a network Centrality measure. The main idea behind this measure is to calculate the importance of each node based on the magnitude of the "drop" happening in a quantity called "Laplacian Energy", upon removal of the node from the network. 

[1] Qi, Xingqin, et al. "Laplacian centrality: A new centrality measure for weighted networks." Information Sciences 194 (2012): 240-253

## Usage

```python
python laplacian_centrality.py [input_network_path]
```
