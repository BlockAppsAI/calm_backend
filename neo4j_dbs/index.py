from neo4j import GraphDatabase
from fastapi import FastAPI

app = FastAPI()

class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

def firstTransaction(tx, name):
    result = tx.run("CREATE (n:NodeExample { name: $name }) RETURN id(n) AS node_id", name=name)
    record = result.single()
    return record["node_id"]


if __name__ == "__main__":
    # greeter = HelloWorldExample("neo4j+s://f1707b8b.databases.neo4j.io", "neo4j", "yENDB86AiKwvV2cZKzr6z9Swis35Pr0cipmYs3K1kTc")
    # greeter.print_greeting("hello, world")
    # greeter.close()

    neo4jSession = GraphDatabase.driver("neo4j+s://f1707b8b.databases.neo4j.io", auth=("neo4j", "yENDB86AiKwvV2cZKzr6z9Swis35Pr0cipmYs3K1kTc"))
    with neo4jSession.session() as session:
        greeting = session.write_transaction(firstTransaction, "example")
        print(greeting)

