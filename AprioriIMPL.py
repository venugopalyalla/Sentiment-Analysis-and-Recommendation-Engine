import MySQLdb
from MySQLdb import Error
import time


def open_db_connection(host, user, password):
    start = time.time()
    conn = MySQLdb.connect(host, user, password, port=3307)
    print "Connection to the database has been established successfully! Time taken: " + str(time.time() - start)
    return conn


def create_database_with_schema(conn):
    start = time.time()
    cursor_instance = conn.cursor()
    sql = 'CREATE DATABASE TRANSACTIONS_DATABASE'
    cursor_instance.execute(sql)
    sql = '''CREATE TABLE TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE
             (TRANSACTION_ID VARCHAR(100) NOT NULL, TRANSACTION_LIST VARCHAR(100) NOT NULL,
             PRIMARY KEY (TRANSACTION_ID));'''
    cursor_instance.execute(sql)
    print "Database along with the table has been created! Time taken: " + str(time.time() - start)


def read_input_and_insert_data(conn, file_name):
    start = time.time()
    cursor_instance = conn.cursor()
    file_pointer = open(file_name, 'rb')
    row = file_pointer.readline()
    while row:
        row_arr = row.split(',')
        first = row_arr[0]
        last = '_'.join(row_arr[1:])
        last_strip = ''.join(last.split())
        last_updated = '_' + last_strip + '_'
        try:
            args = (first, last_updated)
            cursor_instance.execute(
                '''INSERT INTO TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE(TRANSACTION_ID,TRANSACTION_LIST)
                   VALUES (%s,%s)''', args)
            conn.commit()
        except Error as error:
            print "Unexpected error:", error
            conn.rollback()
        row = file_pointer.readline()
    file_pointer.close()
    print "Data inserted Successfully! Time taken: " + str(time.time() - start)


def calculate_support(conn, support):
    print "Calculating Support... "
    start = time.time()
    cursor_instance = conn.cursor()
    support_dict = {}
    try:
        query = '''SELECT TRANSACTION_ID FROM TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE'''
        cursor_instance.execute(query)
        transactions = cursor_instance.fetchall()
    except Error as error:
        print "Unexpected error:", error
    total_num_transactions = float(len(transactions))
    # Max product Id is 49 in the sample data set
    for each_transaction in range(1, 50):
        args = ("%_" + str(each_transaction) + "_%")
        cursor_instance.execute(
            '''SELECT * FROM TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE WHERE TRANSACTION_LIST LIKE %s''', args)
        each_transaction_count = cursor_instance.fetchall()
        support_each_transaction = len(each_transaction_count) / total_num_transactions
        if support_each_transaction >= support:
            support_dict[each_transaction] = support_each_transaction
    print "Calculated Support! Time taken: " + str(time.time() - start)
    return support_dict, total_num_transactions


def calculate_confidence(conn, support_dict, confidence, total_num_transactions):
    print "Calculating Confidence and writing the values to a file... "
    start = time.time()
    cursor_instance = conn.cursor()
    support_list = list(support_dict.keys())
    for i in range(len(support_list)):
        final_rules = {}
        for j in range(len(support_list)):
            if i == j:
                continue
            else:
                args = ("%_" + str(support_list[i]) + "_%", "%_" + str(support_list[j]) + "_%")
                cursor_instance.execute(
                    '''SELECT * FROM TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE WHERE TRANSACTION_LIST IN
                      (SELECT TRANSACTION_LIST FROM TRANSACTIONS_DATABASE.TRANSACTIONS_TABLE
                       where TRANSACTION_LIST LIKE %s) and (TRANSACTION_LIST LIKE %s)''', args)
                each_transaction_count = cursor_instance.fetchall()
                confidence_each_transaction = len(each_transaction_count) / (
                    support_dict[support_list[i]] * total_num_transactions)
                if confidence_each_transaction >= confidence:
                    final_rules[support_list[i], support_list[j]] = confidence_each_transaction
        final_confidence_list = sorted(((v, k) for k, v in final_rules.iteritems()), reverse=True)[0:6]
        # print final_confidence_list
        flag = False
        output_recommendation = ""
        with open("GeneratedRecommendations.txt", "a") as text_file:
            for each_list in final_confidence_list:
                if not flag:
                    output_recommendation += str(each_list[1][0]) + '->'
                    flag = True
                output_recommendation += str(each_list[1][1]) + ','
            text_file.write(output_recommendation[:-1] + "\n")
    print "Calculated Confidence! Time taken: " + str(time.time() - start)
    print "Check the output in the file - GeneratedRecommendations.txt!"


def main():
    print "This Program is used to generate Recommendations."
    support = 0.02
    confidence = 0.01
    input_file = '75000-out1.csv'
    # input_file = 'sample.csv'
    connection = open_db_connection(host="localhost", user="root", password="root")
    create_database_with_schema(connection)
    read_input_and_insert_data(connection, input_file)
    support_map, no_of_transactions = calculate_support(connection, support)
    calculate_confidence(connection, support_map, confidence, no_of_transactions)

    print "Completed generating Recommendations."


if __name__ == "__main__":
    main()
