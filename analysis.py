from decouple import config
import urllib3
import json
from zone_info import connect_mysql


def data_analysis(analysis_data):
    open_api_url = "http://aiopen.etri.re.kr:8000/WiseNLU"
    access_key = config('ETRI.KEY')
    analysis_code = "ner"
    titles = analysis_data['title']
    contents = analysis_data['content']
    text_len = len(titles)
    for i in range(text_len):
        text = titles[i] + contents[i]
        request_json = {
            "access_key": access_key,
            "argument": {
                "text": text,
                "analysis_code": analysis_code
            }
        }
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            open_api_url,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json)
        )
        response = json.loads(response.data.decode('utf-8'))
        return_object = response['return_object']
        sentences = return_object['sentence']
        district = District()
        for sentence in sentences:
            recognition_results = sentence['NE']
            for info in recognition_results:
                info_name = info['text']
                print(info_name)
                info_type = str(info['type'])
                print(info_type)
                name_len = len(info_name)
                print(name_len)
                loc_list = ('PROVINCE', 'CAPITALCITY',
                            'ISLAND', 'CITY', 'COUNTY')
                first_name = []
                if info_type.endswith(loc_list):
                    if name_len == 5:
                        info_name = info_name[:2]
                    elif name_len >= 4:
                        info_name = info_name[0] + info_name[2]
                    elif name_len >= 3:
                        info_name = info_name[:2]
                    else:
                        if name_len != 1:
                            first_name.append(info_name[:1])
                    print(info_name)
                    district.name_second = info_name
                    if name_len == 1:
                        for data in first_name:
                            district.name_first = data
                            result_id = insert_zone_check(analysis)
                            if result_id:
                                district.provinces.add(result_id)
                    else:
                        district.name_first = info_name[0:1]
                        district.name_second = info_name[1:2]
                        result_id = insert_zone_check(analysis)
                        if result_id:
                            district.sigungus.add(result_id)
        provinces = district.provinces
        sigungus = district.sigungus
        provinces_len = len(provinces)
        sigungus_len = len(sigungus)
        connect = connect_mysql()
        cursor = connect.cursor()
        sql = 'SELECT id FROM news_lists ORDER BY id DESC LIMIT 1'
        cursor.execute(sql)
        news_id = cursor.fetchone()[0]
        if provinces_len == 0 and sigungus_len == 0:
            insert_news_districts(news_id, 1, 1)
        else:
            if provinces_len != 0:
                for province in provinces:
                    if sigungus_len != 0:
                        for sigungu in sigungus:
                            # 지역정보 가져오기 추가
                            sql = 'SELECT NVL(province, 1) province_id, NVL(sigungu, 1) sigungu_id ' \
                                'FROM provinces p INNER JOIN sigungus s ON p.id=s.province_id WHERE ' \
                                'WHERE p.id=%s AND s.id=%s LIMIT 1'
                            cursor.execute(sql, (province, sigungu))
                            analysis = cursor.fetchone()[0]
                            if analysis != None:
                                insert_news_districts(
                                    news_id, province, sigungu)
                                insert_news_districts(news_id, province, 1)
                            else:
                                insert_news_districts(news_id, province, 0)

                                sql = 'SELECT NVL(province, 1) province_id, NVL(sigungu, 1) sigungu_id ' \
                                    'FROM provinces p INNER JOIN sigungus s ON p.id=s.province_id WHERE ' \
                                    'WHERE s.id=%s LIMIT 1'
                                cursor.execute(sql, (sigungu))
                                analysis = cursor.fetchone()[0]
                                insert_news_districts(
                                    news_id, analysis.['province_id'], analysis.['sigungu_id'])
                            sql = 'SELECT id FROM news_lists ORDER BY id DESC LIMIT 1'
                            cursor.execute(sql)
                            news_id = cursor.fetchone()[0]
                    else:
                        insert_news_districts(news_id, province, 0)
                    sql = 'SELECT id FROM news_lists ORDER BY id DESC LIMIT 1'
                    cursor.execute(sql)
                    news_id = cursor.fetchone()[0]
            else:
                if sigungus_len != 0:
                    for sigungu in sigungus:
                        sql = 'SELECT NVL(province, 1) province_id, NVL(sigungu, 1) sigungu_id ' \
                            'FROM provinces p INNER JOIN sigungus s ON p.id=s.province_id WHERE ' \
                            'WHERE s.id=%s LIMIT 1'
                        cursor.execute(sql, (sigungu))
                        analysis = cursor.fetchone()[0]
                        insert_news_districts(
                            news_id, analysis.['province_id'], analysis.['sigungu_id'])
                        insert_news_districts(news_id, analysis.['province_id'], 1)
    return "Insert District Success"


def insert_news_districts(news_id, province_id, sigungu_id):
    sql = 'INSERT INTO news_districts (news_id, province_id, sigungu_id) ' \
          'SELECT %s, %s, %s FROM DUAL WHERE NOT EXISTS ' \
          '(SELECT * FROM news_districts ' \
          'WHERE news_id=%s AND province_id=%s AND sigungu_id=%s) LIMIT 1'
    cursor.execute(sql, (news_id, province_id, sigungu_id,
                         news_id, province_id, sigungu_id))


def insert_zone_check(district):
    connect = connect_mysql()
    cursor = connect.cursor()
    sql = 'SELECT COUNT(code) FROM provinces WHERE name LIKE "%s"'
    cursor.execute(sql, ('%' + district.name_first +
                         '%' + district.name_second + '%'))
    check = cursor.fetchone()[0]
    result_id = None
    if check > 0:
        sql = 'SELECT p.id FROM provinces p INNER JOIN sigungus s ON p.id=s.province_id ' \
              'WHERE p.name LIKE "%s" LIMIT 1'
        cursor.execute(sql, ('%' + district.name_first +
                             '%' + district.name_second + '%'))
        result_id = cursor.fetchone()[0]
    else:
        sql = 'SELECT COUNT(code) FROM sigungus WHERE name LIKE "%s"'
        cursor.execute(sql, ('%' + district.name_first +
                             '%' + district.name_second + '%'))
        check = cursor.fetchone()[0]
        if check > 0:
            sql = 'SELECT s.id FROM provinces p INNER JOIN sigungus s ON p.id=s.province_id ' \
                  'WHERE s.name LIKE "%s" LIMIT 1'
            cursor.execute(sql, ('%' + district.name_first +
                                 '%' + district.name_second + '%'))
            result_id = cursor.fetchone()[0]
    cursor.close()
    connect.close()
    return result_id


class District:
    name_first = None
    name_second = None
    provinces = set()
    sigungus = set()

    def get_total_count(self):
        return len(self.provinces) + len(self.sigungus)
