# !/usr/bin/env python3
import psycopg2

# query titles
query_title1 = ("1.What are the most popular three articles of all time?")
query_title2 = ("2.Who are the most popular article authors of all time?")
query_title3 = ("3.On which days did more than 1% of requests lead to errors?")

# query 1
query1 = "select title,views from v1 limit 3"

# query 2
query2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') where "
    "log.status like '%200%' group "
    "by authors.name order by views desc"
    )

# query 3
query3 = (
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1"
    )


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.OperationalError as db_except:
        print('Unable to connect!\n{0}').format(db_except)
        sys.exit(1)

def get__query(query):
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
	return results


def print_query(q):
    print(q[1])
    for index, results in enumerate(q[0]):
        print(
            "\t", index+1, "---", results[0],
            "\t - ", str(results[1]), "views")


def print_er(q):
    print(q[1])
    for results in q[0]:
        print("\t", results[0], "---", str(results[1]) + "%")


# MAIN PROGRAM
if __name__ == '__main__':
    q1 = get_query(query1), query_title1
    q2 = get_query(query2), query_title2
    q3 = get_query(query3), query_title3
    print("Most Popular Articles: ")
    print_query(q1)
    print("Most Popular Authors: ")
    print_query(q2)
    print("Days with more than 1% errors: ")
    print_er(q3)
