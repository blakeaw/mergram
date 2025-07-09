"""
This module provides classes for constructing Mermaid flowchart diagrams in Python.

Classes:
    Flowchart: Represents a Mermaid flowchart diagram with nodes, links, and optional subgraphs.
    Subgraph: Represents a subgraph within a Mermaid flowchart.
    Node: Represents a node in a Mermaid flowchart.
    Link: Represents a link (edge) between two nodes in a Mermaid flowchart.

All string representations are returned in Mermaid syntax.
"""

import warnings


class Flowchart:
    """
    Represents a flowchart diagram with nodes, links, and optional subgraphs.

    Attributes:
        title (str): The title of the flowchart.
        orientation (str): The orientation of the flowchart ("TB", "BT", "LR", "RL").
        _nodes (set): A set of Node objects in the flowchart.
        edges (list): A list of Link objects representing edges between nodes.
        subgraphs (dict): A dictionary of subgraph title to Subgraph objects.
    """

    _orientations = ["TB", "BT", "LR", "RL"]

    _type = "flowchart"

    def __init__(self, title: str, orientation: str = "TB"):
        """
        Initialize a Flowchart instance.

        Args:
            title (str): The title of the flowchart.
            orientation (str, optional): The orientation of the flowchart. Defaults to "TB".

        Raises:
            ValueError: If the orientation is not valid.
        """
        self.title = title
        if orientation not in self._orientations:
            raise ValueError(
                f"Invalid orientation: {orientation}. Must be one of {self._orientations}."
            )
        self.orientation = orientation
        self._nodes = set()
        self.edges = []
        self.subgraphs = {}

    @property
    def nodes(self):
        """
        Get the list of nodes in the flowchart.

        Returns:
            list: List of Node objects.
        """
        return list(self._nodes)

    def add_node(self, node: "Node"):
        """
        Add a node to the flowchart.

        Args:
            node (Node): The node to add.

        Raises:
            TypeError: If the argument is not a Node instance.
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        self._nodes.add(node)

    def add_link(self, link: "Link"):
        """
        Add a link (edge) to the flowchart.

        Args:
            link (Link): The link to add.

        Raises:
            TypeError: If the argument is not a Link instance.
        """
        if not isinstance(link, Link):
            raise TypeError("link must be an instance of Link.")
        self.edges.append(link)

    def add_subgraph(self, subgraph: "Subgraph"):
        """
        Add a subgraph to the flowchart.

        Args:
            subgraph (Subgraph): The subgraph to add.

        Raises:
            TypeError: If the argument is not a Subgraph instance.
        """
        if not isinstance(subgraph, Subgraph):
            raise TypeError("subgraph must be an instance of Subgraph.")
        self.subgraphs[subgraph.title] = subgraph

    def __iadd__(self, other):
        """
        Add a Node, Link, or Subgraph to the flowchart using the += operator.

        Args:
            other (Node, Link, or Subgraph): The object to add.

        Returns:
            Flowchart: The updated flowchart.

        Raises:
            TypeError: If the argument is not a supported type.
        """
        if isinstance(other, Node):
            self.add_node(other)
        elif isinstance(other, Link):
            self.add_link(other)
        elif isinstance(other, Subgraph):
            self.add_subgraph(other)
        else:
            raise TypeError("Can only add Node, Link, or Subgraph instances.")
        return self

    def __str__(self):
        """
        Return a string representation of the flowchart.

        Returns:
            str: The string representation.
        """
        flowchart_str = f"---\n title: {self.title}\n---\n"
        flowchart_str += f"{self._type} {self.orientation} \n"
        for node in self.nodes:
            flowchart_str += f"    {node.node}\n"
        for link in self.edges:
            flowchart_str += f"    {link}\n"
        for subgraph in self.subgraphs.values():
            sg_str = str(subgraph)
            for line in sg_str.splitlines():
                flowchart_str += f"    {line}\n"
        return flowchart_str

    def write(self, file_path: str):
        """
        Write the flowchart to a file.

        Args:
            file_path (str): The path to the file where the flowchart will be written.
        """
        if not file_path.endswith(".mmd") or not file_path.endswith(".mermaid"):
            warnings.warn("Recommended file extensions are '.mmd' or '.mermaid'.")
        with open(file_path, "w") as f:
            f.write(str(self))

    def from_networkx(self, graph, subgraph_using: str = None) -> "Flowchart":
        """
        Convert a NetworkX graph to a Flowchart.

        Args:
            graph: A NetworkX graph instance.
            subgraph_using (str, optional): Edge attribute to use for subgraph grouping.

        Returns:
            Flowchart: The updated flowchart.

        Raises:
            TypeError: If the input is not a NetworkX graph.
        """
        if not hasattr(graph, "nodes") or not hasattr(graph, "edges"):
            raise TypeError("graph must be a NetworkX graph instance.")

        for node_id in graph.nodes:
            node = Node(id=node_id)
            self.add_node(node)

        for source, target, data in graph.edges(data=True):
            if subgraph_using and subgraph_using in data:
                subgraph_title = data[subgraph_using]
                if subgraph_title not in self.subgraphs:
                    self.add_subgraph(Subgraph(title=subgraph_title))
                subgraph = self.subgraphs[subgraph_title]
                link = Link(
                    source=Node(id=source),
                    target=Node(id=target),
                    text=data.get("label"),
                )
                subgraph.add_link(link)
            else:
                link = Link(
                    source=Node(id=source),
                    target=Node(id=target),
                    text=data.get("label"),
                )
                self.add_link(link)

        return

    def to_markdown(self) -> str:
        """
        Convert the flowchart to a Markdown string with the flowchart in a mermaid code block.

        Returns:
            str: The Markdown representation of the flowchart.
        """
        markdown_str = f"```mermaid\n{str(self)}\n```\n"
        return markdown_str

    def to_html(self) -> str:
        """
        Convert the flowchart to an HTML string with mermaid.js scritp via ESM import.

        Adated from: https://mermaid.js.org/config/usage.html

        Returns:
            str: The HTML representation of the flowchart.
        """
        html_str = f"""
<html lang='en'>
<body>
<pre class=\"mermaid\">
{str(self)}
</pre>
<script type=\"module\">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
</script>
</body>
</html>"""
        return html_str


class Subgraph(Flowchart):
    """
    Represents a subgraph within a flowchart.

    Attributes:
        title (str): The title of the subgraph.
        orientation (str): The orientation of the subgraph.
    """

    _type = "subgraph"

    def __init__(self, title: str, direction: str = "TB"):
        """
        Initialize a Subgraph instance.

        Args:
            title (str): The title of the subgraph.
            direction (str, optional): The orientation of the subgraph. Defaults to "TB".
        """
        super().__init__(title, orientation=direction)

    def __str__(self):
        """
        Return a string representation of the subgraph.

        Returns:
            str: The string representation.
        """
        subgraph_str = f"subgraph {self.title}\n"
        subgraph_str += f"    direction {self.orientation} \n"
        for node in self.nodes:
            subgraph_str += f"    {node.node}\n"
        for link in self.edges:
            subgraph_str += f"    {link}\n"
        for subgraph in self.subgraphs.values():
            sg_str = str(subgraph)
            for line in sg_str.splitlines():
                subgraph_str += f"    {line}\n"
        subgraph_str += "end\n"
        return subgraph_str


class Node:
    """
    Represents a node in a flowchart.

    Attributes:
        id (str): The unique identifier for the node.
        attributes (dict): Node attributes such as shape, label, fill, stroke, and stroke-width.
    """

    _shapes = [
        "notch-rect",
        "hourglass",
        "bolt",
        "brace",
        "brace-r",
        "braces",
        "lean-r",
        "lean-l",
        "cyl",
        "diam",
        "delay",
        "h-cyl",
        "lin-cyl",
        "curv-trap",
        "div-rect",
        "doc",
        "rounded",
        "tri",
        "fork",
        "win-pane",
        "f-circ",
        "lin-doc",
        "lin-rect",
        "notch-pent",
        "flip-tri",
        "sl-rect",
        "odd",
        "flag",
        "hex",
        "trap-b",
        "rect",
        "circle",
        "sm-circ",
        "dbl-circ",
        "fr-circ",
        "bow-rect",
        "fr-rect",
        "cross-circ",
        "tag-doc",
        "tag-rect",
        "stadium",
        "text",
    ]

    def __init__(
        self,
        id: str,
        label: str = None,
        shape: str = "rect",
        fill: str = "#fff",
        stroke: str = "#000",
        stroke_width: str = "2px",
    ):
        """
        Initialize a Node instance.

        Args:
            id (str): The unique identifier for the node.
            label (str, optional): The label for the node. Defaults to id.
            shape (str, optional): The shape of the node. Defaults to "rect".
            fill (str, optional): The fill color of the node. Defaults to "#fff".
            stroke (str, optional): The stroke color of the node. Defaults to "#000".
            stroke_width (str, optional): The stroke width of the node. Defaults to "2px".

        Raises:
            ValueError: If the shape is not valid.
        """
        self.id = id
        if shape not in self._shapes:
            raise ValueError(f"Invalid shape: {shape}. Must be one of {self._shapes}.")
        label = label if label is not None else id
        self.attributes = {
            "shape": shape,
            "label": label,
            "fill": fill,
            "stroke": stroke,
            "stroke-width": stroke_width,
        }

    def set_attribute(self, key: str, value: str):
        """
        Set an attribute for the node.

        Args:
            key (str): The attribute key.
            value (str): The attribute value.

        Raises:
            ValueError: If setting an invalid shape.
            KeyError: If the attribute key does not exist.
        """
        if key == "shape" and value not in self._shapes:
            raise ValueError(f"Invalid shape: {value}. Must be one of {self._shapes}.")
        if key not in self.attributes:
            raise KeyError(f"Attribute {key} does not exist in Node attributes.")
        self.attributes[key] = value

    def __str__(self):
        """
        Return a string representation of the node in Mermaid syntax.

        Returns:
            str: The string representation in Mermaid syntax.
        """
        return self.node

    @property
    def node(self) -> str:
        """
        Get the string representation of the node with its attributes in Mermaid syntax.

        Returns:
            str: The node string in Mermaid syntax.
        """
        node_str = f"{self.id}@{{ shape: {self.attributes['shape']}, label: {self.attributes['label']}, fill: {self.attributes['fill']}, stroke: {self.attributes['stroke']}, stroke-width: {self.attributes['stroke-width']} }}"
        return node_str


class Link:
    """
    Represents a link (edge) between two nodes in a flowchart.

    Attributes:
        source (Node): The source node.
        target (Node): The target node.
        link_type (str): The type of link.
        text (str): Optional label for the link.
    """

    _link_types = ["-->", "---", "-.-", "==>", "~~~"]

    def __init__(
        self, source: Node, target: Node, link_type: str = "-->", text: str = None
    ):
        """
        Initialize a Link instance.

        Args:
            source (Node): The source node.
            target (Node): The target node.
            link_type (str, optional): The type of link. Defaults to "-->".
            text (str, optional): The label for the link. Defaults to None.

        Raises:
            ValueError: If the link type is not valid.
        """
        self.source = source
        self.target = target
        if link_type not in self._link_types:
            raise ValueError(
                f"Invalid link type: {link_type}. Must be one of {self._link_types}."
            )
        self.link_type = link_type
        self.text = text

    @property
    def link(self) -> str:
        """
        Get the string representation of the link in Mermaid syntax.

        Returns:
            str: The link string in Mermaid syntax.
        """
        if self.text is not None:
            link_ = f"{self.source.id}{self.link_type}|{self.text}|{self.target.id}"
        else:
            link_ = f"{self.source.id} {self.link_type} {self.target.id}"
        return link_

    def __str__(self):
        """
        Return a string representation of the link in Mermaid syntax.

        Returns:
            str: The string representation in Mermaid syntax.
        """
        return self.link
