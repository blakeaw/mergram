# MerGram

**Programmatically generate [Mermaid](https://mermaid.jd.org) diagrams and charts using Python.**

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![Python version badge](https://img.shields.io/badge/python->=3.8-blue.svg)
[![license](https://img.shields.io/github/license/blakeaw/mergram.svg)](LICENSE)
[![release](https://img.shields.io/github/release/blakeaw/mergram.svg)](https://github.com/blakeaw/mergram/releases)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

MerGram currently supports constructing Mermaid flowcharts, with plans to expand support for additional diagram and chart types in future releases.
 

## Features

- Build Mermaid flowcharts using Python classes
- Support for nodes, links, and subgraphs
- Export diagrams to Mermaid `.mmd` or `.mermaid` files
- Optional integration with [networkx](https://networkx.org/) for graph conversion

### What's New in 

#### v0.2.0

* `Flowchart.to_markdown` function to get a string representation of the flowchart embedded in a Markdown Mermaid code block.
* `Flowchart.to_html` function to get a string representation of the flowchart embedded in HTML. 

## Installation

```bash
pip install mergram
```

To enable networkx integration:

```bash
pip install mergram[networkx]
```

## Usage

### Basic Flowchart

```python
from mergram.flowchart import Flowchart, Node, Link

fc = Flowchart("Example Flowchart")
a = Node("A", label="Start")
b = Node("B", label="End", shape='circle')
fc += a
fc += b
fc += Link(a, b, text="to end")

print(fc)
```
Generates the following mermaid diagram code:

    ---
    title: Example Flowchart
    ---
    flowchart TB
        A@{ shape: rect, label: Start, fill: #fff, stroke: #000, stroke-width: 2px }
        B@{ shape: circle, label: End, fill: #fff, stroke: #000, stroke-width: 2px }
        A-->|to end|B

That looks like: 
```mermaid
---
 title: Example Flowchart
---
flowchart TB
    A@{ shape: rect, label: Start, fill: #fff, stroke: #000, stroke-width: 4px }
    B@{ shape: circle, label: End, fill: #fff, stroke: #000, stroke-width: 2px }
    A-->|to end|B
```

### From NetworkX

```python
import networkx as nx
from mergram.flowchart import Flowchart

G = nx.DiGraph()
G.add_edge("A", "B", label="to B")
G.add_edge("B", "A", label="to A")
fc = Flowchart("From NetworkX", orientation='LR')
fc.from_networkx(G)
print(fc)
```
    ---
    title: From NetworkX
    ---
    flowchart LR
        A@{ shape: rect, label: A, fill: #fff, stroke: #000, stroke-width: 2px }
        B@{ shape: rect, label: B, fill: #fff, stroke: #000, stroke-width: 2px }
        A-->|to B|B
        B-->|to A|A

```mermaid
---
 title: From NetworkX
---
flowchart LR
    A@{ shape: rect, label: A, fill: #fff, stroke: #000, stroke-width: 2px }
    B@{ shape: rect, label: B, fill: #fff, stroke: #000, stroke-width: 2px }
    A-->|to B|B
    B-->|to A|A
```


### Export to File

```python
fc.write("diagram.mmd")
```

## Optional Dependencies

- `networkx`: For converting existing graphs to Mermaid flowcharts.

## License

MIT License

## Contributing

Contributions are welcome! Please open issues or pull requests.
