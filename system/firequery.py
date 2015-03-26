__author__ = 'rigel'
import sqlite3


def execquery_onload(dbpath1):
    data_structure1 = dict()
    list_of_tables1 = dict()
    list_of_schemas1 = dict()

    conn = sqlite3.connect(dbpath1)
    c = conn.cursor()
    #print("execute" + dbpath1 + "  " + query)
    i=0;
# Create table

    print("tables \n")
    for row in c.execute("select name from sqlite_master  where type='table'"):
        list_of_tables1[str(i)] = row
        i = i+1
        print(row)
        print("\n")

    print("schemas \n")
    i=0
    for row in c.execute(" select sql from sqlite_master where type = 'table' " ):
        print(row)
        list_of_schemas1[str(i)] = row
        i = i+1

        print("\n")

    print("ttttttttttttttt")


    data_structure1["tables"] = list_of_tables1
    data_structure1["schema"] = list_of_schemas1

    conn.close()

    return data_structure1


def execQuery( dbpath1, query):
    list_of_records = dict()
    data_structure = dict()
    list_of_tables = dict()
    list_of_schemas = dict()
    conn = sqlite3.connect(dbpath1)
    c = conn.cursor()
    print("execute" + dbpath1 + "  " + query)


# Create table

    if(query.find("select")!=-1):
         #c.execute("select * from  empsam;")
         #i =0
         #for row in  c.execute(query):
            #list_of_records[str(i)] = row
            #i = i+1

         i=1
         co = c.execute(query)
         names = list(map(lambda x: x[0], co.description))
         print(names)
         list_of_records[str(0)] = names
         for row in  co:
            list_of_records[str(i)] = row
            i = i+1
    else:
        #c.execute(query)
        #conn.commit()
        #i =0
        #for row in  c.execute("select * from  empsam;"):
             #list_of_records[str(i)] = row
             #i = i+1


        c.execute(query)
        conn.commit()

        tablename = query.split(" ")





        #for row in  c.execute("select * from  empsam;"):
        if(query.find("create")== -1):
            if(query.find("update")!=-1):
                co = c.execute("select * from " + tablename[1] + ";")
            else:

                co = c.execute("select * from " + tablename[2] + ";")

            i =1
            names = list(map(lambda x: x[0], co.description))
            print(names)
            list_of_records[str(0)] = names
            for row in  co:


                list_of_records[str(i)] = row
                i = i+1

    i=0;
# Create table
    print("tables \n")

    for row in c.execute("select name from sqlite_master  where type='table'"):
        list_of_tables[str(i)] = row
        i = i+1
        print(row)
        print("\n")

    print("schemas \n")
    i=0
    for row in c.execute(" select sql from sqlite_master where type = 'table'" ):
        print(row)
        list_of_schemas[str(i)] = row
        i = i+1

        print("\n")

    print("ttttttttttttttt")

    data_structure["tables"] = list_of_tables
    data_structure["schema"] = list_of_schemas
    data_structure["records"] = list_of_records









# Insert a row of data
#    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
    #conn.commit()
    #c.execute("select * from  empsam;")
    #i =0
    #for row in  c.execute("select * from  empsam;"):
        #list_of_records[str(i)] = row
        #i = i+1
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
    conn.close()
    return data_structure