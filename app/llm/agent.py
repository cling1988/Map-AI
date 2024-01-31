import os

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI


def query(question):
    db = SQLDatabase.from_uri(os.getenv('SQLALCHEMY_DATABASE_URL'))
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM outlet;")
    llm = ChatOpenAI()
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    result = agent_executor.invoke(question)
    print(result)
    return result
