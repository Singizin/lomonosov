from bs4 import BeautifulSoup
import os
import requests

# путь к предварительно сохраненной полной версии сайта
root_path = r'E:\YandexDisc\YandexDisk\НГТУ\НТИ'
downloaded_page = root_path + '/web/Список заявок - Ломоносов.html'
event_id = '6339/'
lomonosov_download_url = 'https://lomonosov-msu.ru/file/uploaded/' + event_id
save_files_path = ''

level_1 = ['Thesis']
level_2 = ['5.1', '5.2', '5.3', '5.4']
level_3 = ['NSTU', 'Other']

save_files_path = level_1[0]


def create_dir():
    for i in level_1:
        os.mkdir(root_path + '/' + i)
        for j in level_2:
            os.mkdir(root_path + '/' + i + '/' + j)
            for k in level_3:
                os.mkdir(root_path + '/' + i + '/' + j + '/' + k)


def download(url=None, section=None, from_place=None, fio=None, file_format='docx', save_files_path=save_files_path):
    r = requests.get(url=url)
    if section[:3] == '5.1':
        save_files_path += '5.1/'
    elif section[:3] == '5.2':
        save_files_path += '5.2/'
    elif section[:3] == '5.3':
        save_files_path += '5.3/'
    elif section[:3] == '5.4':
        save_files_path += '5.4/'
    if 'Новосибирск' in from_place:
        save_files_path += 'NSTU'
    else:
        save_files_path += 'Other'
    file = open('{}/{}.{}'.format(save_files_path, fio, file_format), "wb")
    file.write(r.content)
    file.close()


def parse_t(path):
    site = open(path, 'r', encoding='utf-8')
    soup = BeautifulSoup(site.read(), 'lxml')

    table = soup.find('table', attrs={'class': 'table table-bordered request-list-table'})
    table_body = table.find('tbody')
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    for i in data:
        # i[2] - FIO
        # i[3] - section
        # i[9] - thesis name
        # i[10] - file name
        fio = i[2]
        section = i[3][:3]
        thesis_name = i[9]
        file_name = i[10]
        file_format = file_name.split('.')[-1]
        from_place = i[6]
        download(url=lomonosov_download_url + file_name, fio=fio, from_place=from_place, section=section,
                 file_format=file_format)


create_dir()
parse_t(downloaded_page)
