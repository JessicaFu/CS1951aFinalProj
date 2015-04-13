import MySQLdb
import errorcode
        
def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except MySQLdb.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)  

def create_table(cursor, table):
    try:
        print("Creating table {}: ")
        cursor.execute(table)
    except MySQLdb.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

def main():
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="password")

    cursor = conn.cursor()
    DB_NAME = "CS1951a"
    
    try:
        cursor.database = DB_NAME    
    except MySQLdb.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            conn.database = DB_NAME
        else:
            print(err)
            exit(1)

    articleTable = (
    "CREATE TABLE 'articles' ("
    "  'source' VARCHAR(255) NOT NULL,"
    "  'url' VARCHAR(255),"
    "  'dateTime' DATETIME,"
    "  'keywords' date NOT NULL,"
    "  'summary' LONGTEXT,"
    "  'keywords' LONGTEXT NOT NULL"
    ") ENGINE=InnoDB");
    
    create_table(cursor, articleTable)    
    
    redditTable = (
    "CREATE TABLE 'articles' ("
    "  'source' VARCHAR(255) NOT NULL,"
    "  'score' INT NOT NULL,"
    "  'title' VARCHAR(255),"
    "  'headline' VARCHAR(255),"
    "  'dateTime' DATETIME,"
    "  'keywords' date NOT NULL,"
    "  'comments' LONGTEXT,"
    "  'keywords' LONGTEXT NOT NULL"
    ") ENGINE=InnoDB");
    
    create_table(cursor, redditTable)    
    
if __name__ == "__main__":
    main()