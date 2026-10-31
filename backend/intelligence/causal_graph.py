class CausalGraph:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node_id, label, category="observation"):

        if not any(node["id"] == node_id for node in self.nodes):
            self.nodes.append({
                "id": node_id,
                "label": label,
                "category": category
            })

    def add_edge(self, source, target, relationship="supports_candidate"):

        edge = {
            "source": source,
            "target": target,
            "relationship": relationship
        }

        if edge not in self.edges:
            self.edges.append(edge)

    def build_from_findings(self, findings):

        self.nodes = []
        self.edges = []

        for index, finding in enumerate(findings):

            cause_id = f"cause_{index}"

            cause = finding.get(
                "cause",
                "Unknown possible cause"
            )

            self.add_node(
                cause_id,
                cause,
                "candidate_root_cause"
            )

            evidence_list = finding.get("evidence", [])

            for evidence_index, evidence in enumerate(evidence_list):

                evidence_id = f"evidence_{index}_{evidence_index}"

                self.add_node(
                    evidence_id,
                    evidence,
                    "observation"
                )

                self.add_edge(
                    evidence_id,
                    cause_id,
                    "supports_candidate"
                )

        return self.to_dict()

    def to_dict(self):

        return {
            "nodes": self.nodes,
            "edges": self.edges,

            "interpretation": (
                "Edges represent supporting evidence, "
                "not scientifically proven causal relationships."
            )
        }