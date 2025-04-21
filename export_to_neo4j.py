
import json
import os
from neo4j import GraphDatabase

class Neo4jExporter:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="test"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def export_insights(self, insight_dir="data/insights"):
        with self.driver.session() as session:
            for fname in os.listdir(insight_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(insight_dir, fname), "r") as f:
                        insight = json.load(f)
                        session.write_transaction(self._create_insight_node, insight, fname.replace(".json", ""))

    @staticmethod
    def _create_insight_node(tx, insight, insight_id):
        tx.run("""
            MERGE (i:Insight {
                id: $id,
                who: $who,
                what: $what,
                when: $when,
                why: $why,
                how: $how,
                outcome: $outcome
            })
        """, id=insight_id, **{k: insight.get(k, "") for k in ["who", "what", "when", "why", "how", "outcome"]})

        for ref in insight.get("references", []):
            tx.run("""
                MERGE (a:Asset {
                    title: $title,
                    url: $url,
                    type: $type
                })
                MERGE (i:Insight {id: $id})
                MERGE (i)-[:REFERENCES]->(a)
            """, id=insight_id, **ref)

        for link in insight.get("links", []):
            tx.run("""
                MATCH (i1:Insight {id: $source_id})
                MATCH (i2:Insight {id: $target_id})
                MERGE (i1)-[r:LINKED_AS {type: $type}]->(i2)
            """, source_id=insight_id, target_id=link["insight_id"], type=link["type"])

if __name__ == "__main__":
    exporter = Neo4jExporter()
    exporter.export_insights()
    exporter.close()
    print("✅ Export to Neo4j complete.")
