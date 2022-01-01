from utils.connect_to_db import mysql_connect, mysql_disconnect


def create_indices_and_views(conn):
    """
    executes in our DB several create indices and create views
    create index defaults to BTREE index and this is the index organization we chose
    all these are made in order to optimize the queries we run on queries.py
    :param conn: mysql connection to our DB
    :return:
    """
    cursor = conn.cursor()
    create_stmts = ["""CREATE INDEX movie_statuses ON movies (status)""",
                    """CREATE INDEX movie_collections ON movies (belongs_to_collection)""",
                    """CREATE INDEX movie_budget ON movies (budget)""",
                    """CREATE FULLTEXT INDEX taglineIndex ON movies(tagline)""",
                    """CREATE VIEW taglines_as_questions AS
                        (SELECT *
                        FROM movies as m
                        WHERE m.tagline LIKE 'When%?' OR m.tagline LIKE 'Where%?' OR m.tagline LIKE 'What%?' OR m.tagline LIKE 'How%?' OR m.tagline LIKE 'Who%?')""",
                    """CREATE VIEW taglines_not_questions AS
                        (SELECT *   
                        FROM movies as m
                        WHERE m.id NOT IN
                        (SELECT taglines_as_questions.id
                        FROM taglines_as_questions))"""]
    for stmt in create_stmts:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"create statement failed with exception {e}")
            continue
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    conn = mysql_connect()
    create_indices_and_views(conn)  # needed when running on a new DB. the DB we have already has them.
    mysql_disconnect(conn)
