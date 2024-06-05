
from sqlalchemy import  text
import json
import pandas as pd

def get_user_role(engine, email):
    """
    Ger user role
    """ 
    query = "SELECT * FROM clients WHERE email = :email"
    df = pd.read_sql_query(text(query), engine, params={"email": email})
    
    # Convertir el resultado a JSON
    if not df.empty:
        result_json = df.to_json(orient="records")
        return json.loads(result_json)[0]
    else:
        return json.dumps({"error": "No se encontró ningún cliente con ese correo electrónico."})
    

def get_user_by_id_db(engine, user_id):
    """
    Perform a SQL query to obtain the client by email
    """ 

    query = "SELECT * FROM clients WHERE id = :user_id"
    df = pd.read_sql_query(text(query), engine, params={"user_id": user_id})
    

    if not df.empty:
        result_json = df.to_json(orient="records", lines=True)
        return json.loads(result_json)
    else:
        return json.dumps({"error": "No user with that ID"})
    

def get_user_by_username_db(engine, username):
    """
    Perform a SQL query to obtain the client by username
    """ 

    query = "SELECT * FROM clients WHERE name = :username"
    df = pd.read_sql_query(text(query), engine, params={"username": username})
    

    if not df.empty:
        result_json = df.to_json(orient="records", lines=True)
        return json.loads(result_json)
    else:
        return json.dumps({"error": "No user with that username"})
    

def get_policies_by_username_db(engine, username):
    """
    Perform a SQL query to obtain the policies by username
    """ 
       
    query = """
    SELECT policies.*
    FROM policies
    JOIN clients ON policies.clientId = clients.id
    WHERE clients.name = :username
    """

    df = pd.read_sql_query(text(query), engine, params={"username": username})

    if not df.empty:
        result_json = df.to_json(orient="records")
        return json.loads(result_json)
    else:
        return json.dumps({"error": "No policies with that username"})



def get_usere_by_policie_id_db(engine, policy_id):
    """
    Perform a SQL query to obtain the user by policy
    """ 

    query = """
    SELECT clients.*
    FROM clients
    JOIN policies ON clients.id = policies.clientId
    WHERE policies.id = :policy_id
    """

    df = pd.read_sql_query(text(query), engine, params={"policy_id": policy_id})


    if not df.empty:
        result_json = df.to_json(orient="records", lines=True)
        return json.loads(result_json)
    else:
        return json.dumps({"error": "No user with that policie id"})