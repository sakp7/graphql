
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

### step 3:I have created two objects using graphene(GraphQl library for python)
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
Project Screenshots:
![image](https://github.com/user-attachments/assets/cc0bace5-dd79-4bed-888a-902a31296c47)

![image](https://github.com/user-attachments/assets/270b140e-7471-460c-83a2-5ea19858c555)

![image](https://github.com/user-attachments/assets/6e2993ed-1e8e-4df5-88d6-936285379409)


![image](https://github.com/user-attachments/assets/399e2179-46af-4d44-abe5-aefa28f0d948)

![image](https://github.com/user-attachments/assets/caf2e778-44ce-424c-8042-1d53d156f012)

![image](https://github.com/user-attachments/assets/f4114401-796e-487f-9702-77638c2ac237)

![image](https://github.com/user-attachments/assets/40a91ff4-b084-47a8-922b-09754c78a890)



