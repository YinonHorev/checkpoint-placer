# Control Flow Graph Analyzer

## Overview

The Control Flow Graph Analyzer is an open-source project that provides an HTTP server with a REST API to analyze control flow graphs (CFGs). It implements a specific algorithm to identify "must-go-through" nodes in a single-entry, single-exit CFG. This project is designed to assist developers, researchers, and enthusiasts in understanding and analyzing the flow of control in software programs.

## Features

Analyze Control Flow Graphs: Input a graph in DOT format and identify key nodes that must be traversed for specific control flow paths.
## REST API
Interact with the analyzer through a simple and intuitive REST API.
Docker Support: Easily deployable using Docker for consistent and isolated environments.
Getting Started

## Prerequisites
Docker installed on your system. You can download it from Docker.
## Installation
Pull the Docker Image. Take `tagname` as the version you want to use (refer to the Release section).
```
docker pull temp427/checkpoint-placer:tagname
```

## Run the Docker Container
```
docker run -p 10000:10000 temp427/checkpoint-placer:tagname
```
This command starts the server on port 10000.
Usage
Send a POST request to the server with the CFG data:
```
curl -X POST http://localhost:10000/server \
     -H "Content-Type:application/json" \
     -d '{"e1": "1","h": "5","graph": "digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}"}'
 ```

The server will return a JSON object containing the set of "must-go-through" nodes.

## Example
Request:
```
curl -X POST http://localhost:10000/server \
     -H "Content-Type:application/json" \
     -d '{"e1": "1","h": "5","graph": "digraph graphname{\n1->2\n2->3\n2->5\n5->2\n3->5}"}'
```
Response:
```
{
  "must_go_through_nodes": [1, 2]
}
```
## API Reference

`POST /server`

Payload:

`e1`: String - The entry node in the CFG.

`h`: String - The target node in the CFG.

`graph`: String - The CFG in DOT format.

Response:

JSON object containing the set of "must-go-through" nodes.

## Credits
This project is based on the paper "A simplified algorithm computing all s-t bridges and articulation points" by Massimo Cairo, Shahbaz Khan, Romeo Rizzi, Sebastian Schmidt, Alexandru I. Tomescu, Elia C. Zirondelli.
The original paper can be found here. https://doi.org/10.1016/j.dam.2021.08.026
