from decouple import config
import pandas as pd
import pymysql

def connect_mysql():
    connect = pymysql.connect(host=config('DB.URL'), port=int(config('DB.PORT')), user=config('DB.USER'),
                             passwd=config('DB.PASSWORD'), db=config('DB.NAME'), charset='utf8', autocommit=True)
    return connect


def add_zone_info():
    connect = connect_mysql()
    cursor = connect.cursor()

    zone_name = ['PROVINCES', 'SIGUNGUS']
    try:
        for name in zone_name:
            data = pd.read_csv(config(name + '.URL'), encoding='utf8').fillna(0)
            data_len = 4 if name == 'PROVINCES' else 5
            data_row = data.iloc[:, :data_len]
            for i in range(len(data_row)):
                if data_len == 4:
                    code = int(data_row.loc[i][0])
                    name = data_row.loc[i][1]
                    longitude = float(data_row.loc[i][2])
                    latitude = float(data_row.loc[i][3])
                    sql = 'INSERT INTO provinces (code, name, latitude, longitude) SELECT %s, %s, %s, %s ' \
                          'FROM DUAL WHERE NOT EXISTS' \
                          '(SELECT code, name, latitude, longitude FROM provinces WHERE code = %s AND name = %s)'
                    cursor.execute(sql, (code, name, latitude, longitude, code, name))
                else:
                    province_code = int(data_row.loc[i][0])
                    code = int(data_row.loc[i][1])
                    name = data_row.loc[i][2]
                    longitude = float(data_row.loc[i][3])
                    latitude = float(data_row.loc[i][4])
                    cursor.execute('SELECT id FROM provinces WHERE code = %s', province_code)
                    province_id = cursor.fetchone()[0]
                    sql = 'INSERT INTO sigungus (province_id, code, name, latitude, longitude) ' \
                          'SELECT %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS' \
                          '(SELECT province_id, code, name, latitude, longitude ' \
                          'FROM sigungus ' \
                          'WHERE code = %s AND name = %s)'
                    cursor.execute(sql, (province_id, code, name, latitude, longitude, code, name))
    except Exception as e:
        return e
    finally:
        cursor.close()
        connect.commit()
        connect.close()
    return 1


def exist_zone_info():
    connect = connect_mysql()
    cursor = connect.cursor()

    sql = 'SELECT count(id) FROM provinces'
    cursor.execute(sql)
    check_province = cursor.fetchone()[0]
    sql = 'SELECT count(id) FROM sigungus'
    cursor.execute(sql)
    check_sigungu = cursor.fetchone()[0]

    result = None
    if check_province < 18 or check_sigungu < 263:
        result = 'Zone is inconsistent or not exists'
    else:
        result = 'Zone is exists'
    cursor.close()
    connect.close()
    return result
