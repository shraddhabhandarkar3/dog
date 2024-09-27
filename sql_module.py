import os
import pyodbc
from dotenv import load_dotenv
import json
import datetime


def get_metadata_from_sql():
    # Load .env file
    load_dotenv()

    # SQL Server connection settings
    ##server = os.getenv('SQL_SERVER')
    database = os.getenv('SQL_DATABASE')
    ##username = os.getenv('SQL_USER')
    localhost = 'localhost,1433'
    ##password = os.getenv('SQL_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'

    # Establish connection
    connection = pyodbc.connect(
        f"DRIVER={driver};SERVER={localhost};DATABASE={database};UID=sa;PWD=Shraddha123;"
    )
    
    cursor = connection.cursor()
    
    # Execute query to fetch necessary fields
    cursor.execute('''
        SELECT task_id, Question, Final_answer, Steps, Number_of_steps, 
               How_long_did_this_take, Tools, Number_of_tools 
        FROM Tasks
    ''')
    rows = cursor.fetchall()
    
    # Organize the fetched data into a list of dictionaries
    metadata = []
    for row in rows:
        metadata.append({
            'task_id': row.task_id,
            'Question': row.Question,
            'Final answer': row.Final_answer,
            'Steps': row.Steps,
            'Number of steps': row.Number_of_steps,
            'How long did this take?': row.How_long_did_this_take,
            'Tools': row.Tools,
            'Number of tools': row.Number_of_tools
        })

    # Close the database connection
    cursor.close()
    connection.close()

    return metadata

def update_metadata_steps(task_id, new_steps):
    """
    Updates the 'Steps' field for a given task_id.

    Parameters:
    - task_id (str): The unique identifier for the task.
    - new_steps (str): The updated steps to replace the existing ones.

    Returns:
    - bool: True if the update was successful, False otherwise.
    """
    load_dotenv()

    # Read SQL Server connection settings from environment variables
    database = os.getenv('SQL_DATABASE')
    ##username = os.getenv('SQL_USER')
    localhost = 'localhost,1433'
    ##password = os.getenv('SQL_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        # Establish connection
        connection = pyodbc.connect(
            f"DRIVER={driver};SERVER={localhost};DATABASE={database};UID=sa;PWD=Shraddha123;"
        )
        cursor = connection.cursor()

        # Update the 'Steps' column for the given task_id
        cursor.execute(
            '''
            UPDATE Tasks 
            SET Steps = ? 
            WHERE task_id = ?
            ''',
            new_steps,
            task_id
        )
        connection.commit()
        success = True

    except Exception as e:
        print(f"Error updating Steps: {e}")
        success = False
    finally:
        # Ensure the connection is closed
        cursor.close()
        connection.close()

    return success

def insert_evaluation(task_id, is_correct, user_feedback=None):
    """
    Inserts a new evaluation record into the Evaluations table.

    Parameters:
    - task_id (str): The unique identifier for the task.
    - is_correct (bool): Whether the OpenAI response was correct.
    - user_feedback (str, optional): Additional feedback from the user.

    Returns:
    - bool: True if insertion was successful, False otherwise.
    """
    load_dotenv()

    # Read SQL Server connection settings from environment variables
    database = os.getenv('SQL_DATABASE')
    ##username = os.getenv('SQL_USER')
    localhost = 'localhost,1433'
    ##password = os.getenv('SQL_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        # Establish connection
        connection = pyodbc.connect(
            f"DRIVER={driver};SERVER={localhost};DATABASE={database};UID=sa;PWD=Shraddha123;"
        )
        cursor = connection.cursor()

        # Insert into Evaluations
        cursor.execute(
            '''
            INSERT INTO Evaluations (task_id, is_correct, user_feedback, evaluation_timestamp)
            VALUES (?, ?, ?, ?)
            ''',
            task_id,
            int(is_correct),  # Convert boolean to integer (1 or 0)
            user_feedback,
            datetime.datetime.now()
        )

        connection.commit()
        success = True

    except Exception as e:
        print(f"Error inserting evaluation: {e}")
        success = False
    finally:
        # Ensure the connection is closed
        cursor.close()
        connection.close()

    return success

def get_evaluations():
    """
    Retrieves all evaluation records from the Evaluations table.

    Returns:
    - list of dict: Each dictionary represents an evaluation record.
    """
    load_dotenv()

    # Read SQL Server connection settings from environment variables
    database = os.getenv('SQL_DATABASE')
    ##username = os.getenv('SQL_USER')
    localhost = 'localhost,1433'
    ##password = os.getenv('SQL_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'  

    try:
        # Establish connection
        connection = pyodbc.connect(
            f"DRIVER={driver};SERVER={localhost};DATABASE={database};UID=sa;PWD=Shraddha123;"
        )
        cursor = connection.cursor()

        # Fetch all evaluations
        cursor.execute('SELECT evaluation_id, task_id, is_correct, user_feedback, evaluation_timestamp FROM Evaluations')
        rows = cursor.fetchall()

        # Organize into list of dictionaries
        evaluations = []
        for row in rows:
            evaluations.append({
                'evaluation_id': row.evaluation_id,
                'task_id': row.task_id,
                'is_correct': bool(row.is_correct),
                'user_feedback': row.user_feedback,
                'evaluation_timestamp': row.evaluation_timestamp
            })

    except Exception as e:
        print(f"Error retrieving evaluations: {e}")
        evaluations = []
    finally:
        # Ensure the connection is closed
        cursor.close()
        connection.close()

    return evaluations
