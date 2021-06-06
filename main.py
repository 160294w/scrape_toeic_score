import requests
from bs4 import BeautifulSoup


# def extract_nth_data(average_score_link, distribution_score_link):


def structed_nth_lists_data(nth_toeic_contests) -> list:
    result = []    
    for contest in nth_toeic_contests:
        kaisaibi = contest.find_all('td')[0].text
        examinee_count = contest.find_all('td')[1].text
        average_score_href = contest.find_all('td')[2].a.get('href')
        distribution_score_href = contest.find_all('td')[3].a.get('href')
        URL_DOMAIN = "https://www.iibc-global.org"
        average_score_link = URL_DOMAIN + average_score_href
        distribution_score_link = URL_DOMAIN + distribution_score_href
        result.append([kaisaibi,examinee_count,average_score_link,distribution_score_link])
        #(f'{kaisaibi}\n{examinee_count}\n {average_score_link} \n{distribution_score_link}')
        #print()
    return(result)

def extract_average_score_data_from_tr(score):
    header_name = score.find('th').text
    listening_section = score.find_all('td')[0].text
    reading_section = score.find_all('td')[1].text
    total = score.find_all('td')[2].text
    # print(f'{header_name} {listening_section} {reading_section} {total}')
    return([header_name, listening_section, reading_section, total])

def extract_average_score_from_href(average_score_link):
    """     res = requests.get(average_score_link)
        soup = BeautifulSoup(res.text, "html.parser")
    """
    soup = BeautifulSoup(requests.get(average_score_link).text, "html.parser")

    data_table = soup.find_all('tbody')[0]
    """ maximum_score = data_table.find_all('tr')[0]
    minimum_score = data_table.find_all('tr')[1]
    average_score = data_table.find_all('tr')[2]
    gauss_distribution = data_table.find_all('tr')[3]
 """
    # 行毎のデータ
    # [0]:最高スコア,[1]:最低スコア,[2]:平均スコア,[3]:スコア分布
    maximum_score, minimum_score, average_score, gauss_distribution = data_table.find_all('tr')

    result = []
    result.append(extract_average_score_data_from_tr(maximum_score))
    result.append(extract_average_score_data_from_tr(minimum_score))
    result.append(extract_average_score_data_from_tr(average_score))
    result.append(extract_average_score_data_from_tr(gauss_distribution))
    return(result)



def extract_distribution_score_data_from_tr(score):
    header_name = score.find('th').text
    listening_section = score.find_all('td')[0].text
    reading_section = score.find_all('td')[1].text
    total = score.find_all('td')[2].text
    # print(f'{header_name} {listening_section} {reading_section} {total}')
    return([header_name, listening_section, reading_section, total])


def extract_distribution_score_from_href(distribution_score_link):
    soup = BeautifulSoup(requests.get(distribution_score_link).text, "html.parser")
    data_table = soup.find_all('tbody')[1]
    print(data_table)
    data_table_row = data_table.find_all('tr')
    [extract_distribution_score_data_from_tr(row) for row in data_table]
    return()


if __name__ == "__main__":
    URL = "https://www.iibc-global.org/toeic/official_data/lr/data_avelist.html"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    # 第N回の行を取得
    nth_toeic_contests = soup.find('tbody').find_all('tr')
    # 各回の[第N回, 受験者数, 平均スコアへのリンク, 分布スコアへのリンク]をリスト化
    nth_toeic_contests_list = structed_nth_lists_data(nth_toeic_contests)
    for test in nth_toeic_contests_list:
        # test[2] is url of average score
        print(extract_average_score_from_href(test[2]))
        # test[3] is url of distribution score
        #extract_distribution_score_from_href(test[3])
        #break
    #extract_nth_data(average_score_link=)