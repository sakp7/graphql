import streamlit as st
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd

api_url = "http://127.0.0.1:5000/gql"
transport = RequestsHTTPTransport(url=api_url)
client = Client(transport=transport, fetch_schema_from_transport=True)

query_all_data = gql('''
query {
    branches {
        bank {
            name
        }
        branch
        ifsc
        id
    }
}
''')

query_all_bank_names = gql('''
query {
    branches {
        bank {
            name
        }
        branch
    }
}
''')

query_bank_names_with_branch_ifsc = gql('''
query {
    branches {
        bank {
            name
        }
        branch
        ifsc
    }
}
''')

query_bank_names_with_id = gql('''
query {
    branches {
        bank {
            name
        }
        branch
        id
    }
}
''')

def execute_query(query, fields):
    try:
        response = client.execute(query)
        if 'branches' in response and response['branches']:
            branches = response['branches'][:50]
            data = []

            for branch in branches:
                row = {}
                for field in fields:
                    if field == "bank":
                        row["Bank"] = branch.get("bank", {}).get("name", "Unknown")
                    else:
                        row[field.capitalize()] = branch.get(field, "N/A")
                data.append(row)

            df = pd.DataFrame(data)
            st.table(df)
            return response
        else:
            st.write("No branches found.")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

menu = ["Home", "Test Cases", "Documentation"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.title("Bank Branches - GraphQL API")

    if st.button('Get All Data (Top 50)'):
        st.subheader('Query')
        st.code("""query {
    branches {
        bank {
            name
        }
        branch
        ifsc
        id
    }
}""")
        st.header('Output')
        execute_query(query_all_data, ["branch", "bank", "ifsc", "id"])

    if st.button('Get All Bank Names Only'):
        st.subheader('Query')
        st.code("""query {
    branches {
        bank {
            name
        }
        branch
    }
}
''')""")
        st.subheader('Output')
        execute_query(query_all_bank_names, ["branch", "bank"])

    if st.button('Get Bank Names with Branch and IFSC Codes'):
        st.subheader('Query')
        st.code("""query {
    branches {
        bank {
            name
        }
        branch
        ifsc
    }
}""")
        st.subheader('Output')
        execute_query(query_bank_names_with_branch_ifsc, ["branch", "bank", "ifsc"])

    if st.button('Get Bank Name with ID'):
        st.subheader('Query')
        st.code("""query {
    branches {
        bank {
            name
        }
        branch
        id
    }
}""")
        st.subheader('Output')
        execute_query(query_bank_names_with_id, ["branch", "bank", "id"])

elif choice == "Test Cases":
    st.title("Test Cases")

    test_cases = [
        {"input": "ABHY0065002", "expected": "ABHYUDAYA NAGAR"},
        {"input": "ABHY0065003", "expected": "BAIL BAZAR"},
        {"input": "ABHY0065006", "expected": "FORT"},
        {"input": "ABHY0065012", "expected": "WADALA"},
    ]

    def run_test_cases():
        results = []
        passed = 0

        fields = ["branch", "ifsc"]

        query = gql('''
        query {
            branches {
                branch
                ifsc
            }
        }
        ''')

        response = execute_query(query, fields)

        if response and "branches" in response and response["branches"]:
            branches = response['branches']

            for test in test_cases:
                output = next((branch['branch'] for branch in branches if branch['ifsc'] == test['input']), 'N/A')
                results.append({"Expected Result": test['expected'], "Output Result": output})
                if output == test['expected']:
                    passed += 1
        else:
            results.append({"Expected Result": "N/A", "Output Result": "Error fetching data"})

        return results, passed

    if st.button("Run Test Cases"):
        test_results, passed_count = run_test_cases()
        df = pd.DataFrame(test_results)
        st.table(df)

        total_cases = len(test_cases)
        passed_percentage = (passed_count / total_cases) * 100
        st.success(f"Test Cases Passed: {passed_percentage:.2f}%")

elif choice == "Documentation":
    st.title("Documentation")

    st.write("""Welcome to the Bank Branches API documentation.""")
    st.subheader('Frontend - Streamlit')

    st.subheader('Backend - Flask,GraphQL,Php admin for live sql database')
