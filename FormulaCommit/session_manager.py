import datetime
import sqlite3
# https://qna.habr.com/q/1066566
foo = datetime.datetime.now()
sqlite_connection = sqlite3.connect(":memory:")
# sqlite_connection = sqlite3.connect('formula_commit.db')

cursor = sqlite_connection.cursor()

# cursor.execute("drop table test")
# cursor.execute("create table test(name, value)")
# cursor.execute('insert into test(name, value) values ("a_1", 1),  ("a_2", 2)')
# cursor.execute('insert into test(name, value) values ("a_3", (select round(avg(value), 1) from test where name = "a_1" or name = "a_2") )')
# p = cursor.execute('select * from test').fetchall()
# print(p)

cursor.executescript("""
    create table test(name, value);
    insert into test(name, value) values ("a_1", 3),  ("a_2", 2);
    insert into test(name, value) values ("a_3", 
                (select avg(value) from test where name = "a_1" or name = "a_2") 
                                         );
    """)
p = cursor.execute('select * from test').fetchall()
bar = datetime.datetime.now()
print(p)
print(dict(p))
print(bar-foo)

