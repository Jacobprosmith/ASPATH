"""
Name: Jacob Proenza-Smith
Date: 9/30/2024
Due date: 9/30/2024
About this project: This projects goal was to take in a BPG routing trace file
We would then find the 7th field also called the ASPATH and extract information 
from the file about its neighbors. The information is fed into one of two output 
files which display total number of neighbors something has or the list
of neighbors.
Assumptions: We are assuming the user is giving a valid BPG routing trace file
All work below was performed solely by Jacob Proenza-Smith
I used ChatGPT for:
 for i in range(len(as_list)):
        if i == 0 or as_list[i] != as_list[i - 1]:
            clean_as_list.append(as_list[i]) 
and:
neighbor_counts = {as_num: len(neighbors) for as_num, neighbors in graph.items()}

"""

import re
import argparse

def process_aspath(aspath):
    aspath = re.sub(r'\[.*?\]', '', aspath)
    as_list = aspath.split()
    clean_as_list = []
    for i in range(len(as_list)):
        if i == 0 or as_list[i] != as_list[i - 1]:
            clean_as_list.append(as_list[i])
    
    return clean_as_list

def build_graph_from_file(file_path):
    graph = {}
    
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.split('|')
            if len(fields) > 7:
                aspath = fields[6]  
                clean_as_list = process_aspath(aspath)
                for i in range(len(clean_as_list) - 1):
                    as1 = clean_as_list[i]
                    as2 = clean_as_list[i + 1]
                    
                    if as1 not in graph:
                        graph[as1] = set()
                    if as2 not in graph:
                        graph[as2] = set()
                    
                    graph[as1].add(as2)
                    graph[as2].add(as1) 
    
    return graph

def neighbor_sort_key(item):
    as_num, count = item
    return (-count, int(as_num)) 

def write_top10_file(graph, file_path):
    neighbor_counts = {as_num: len(neighbors) for as_num, neighbors in graph.items()}
    sorted_as = sorted(neighbor_counts.items(), key=neighbor_sort_key)
    with open(file_path, 'w') as f:
        for as_num, count in sorted_as[:10]:  
            neighbors = sorted(graph[as_num], key=int)  
            f.write(f"{as_num}: {count} {'|'.join(neighbors)}\n")

def write_neighbor_count_file(graph, file_path):
    neighbor_counts = {as_num: len(neighbors) for as_num, neighbors in graph.items()}
    sorted_as = sorted(neighbor_counts.items(), key=neighbor_sort_key)
    with open(file_path, 'w') as f:
        for as_num, count in sorted_as:
            f.write(f"{as_num}: {count}\n")

def main():
    parser = argparse.ArgumentParser(description='Process BGP AS path trace file')
    parser.add_argument('file', help='The file containing the BGP AS path trace data')
    args = parser.parse_args()

    as_graph = build_graph_from_file(args.file)

    write_top10_file(as_graph, 'top10.txt')
    write_neighbor_count_file(as_graph, 'neighbor_count.txt')

if __name__ == '__main__':
    main()
