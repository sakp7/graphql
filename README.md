
### Project Title
Backend Functionality

### Project Description
This project contains functionality related to the backend.py file, which provides GraphQl implementation.
### Required Libraries
* Python 3.8+
* Flask 2.0+
* numpy 1.20+
* pandas 1.3+
* graphene

### Detailed Explanation
This project provides a single endpoint for data retriving.

Front-end :Streamlit
Backend: Flask,GraphQL,sql

### Step 1 : I have created an api endpoint with the name 'gql'.
app.add_url_rule(
    "/gql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

### step 2: I have converted the .csv file to sql file and deployed it in freesqlhosting.com
    def get_db_connection():
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DBNAME,
            port=MYSQL_PORT
        )
        return connection

### step 3:I have created to objects using graphene(GraphQl library for python)
    class Bank(graphene.ObjectType):
        name = graphene.String()
    
    class Branch(graphene.ObjectType):
        branch = graphene.String()
        ifsc = graphene.String()
        bank = graphene.Field(Bank)
        id = graphene.Int()
### step 4:Created multiple queries and tested the code
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

I have tested for mutiple test cases.
