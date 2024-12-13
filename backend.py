from flask import Flask
from flask_graphql import GraphQLView
import graphene
import mysql.connector
MYSQL_HOST = '123.freemysqlhosting.net'  
MYSQL_USER = '123456' 
MYSQL_PASSWORD = '123456' 
MYSQL_DBNAME = '123456' 
MYSQL_PORT = 3306  

def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DBNAME,
        port=MYSQL_PORT
    )
    return connection

class Bank(graphene.ObjectType):
    name = graphene.String()

class Branch(graphene.ObjectType):
    branch = graphene.String()
    ifsc = graphene.String()
    bank = graphene.Field(Bank)
    id = graphene.Int()

class Query(graphene.ObjectType):
    branches = graphene.List(Branch)

    def resolve_branches(self, info):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT bank_name, branch, ifsc, id FROM branches")
        rows = cursor.fetchall()
        branches_list = []
        for row in rows:
            bank = Bank(name=row.get('bank_name', ''))
            branch = Branch(branch=row.get('branch', ''), ifsc=row.get('ifsc', ''), id=row.get('id', ''), bank=bank)
            branches_list.append(branch)
        cursor.close()
        connection.close()
        return branches_list

schema = graphene.Schema(query=Query)

app = Flask(__name__)
app.add_url_rule(
    "/gql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

if __name__ == "__main__":
    app.run(debug=True)
