from bs4 import BeautifulSoup
import requests

# page = requests.get('https://otkritkiok.ru/ejednevnie/dobroe-utro')

# путь к предварительно сохраненной полной версии сайта
otkritki_ok = r'E:\YandexDisc\YandexDisk\НГТУ\НТИ\web/Список заявок - Ломоносов.html'
id_sobitia = '6339/'
lmnsv_link = 'https://lomonosov-msu.ru/file/uploaded/'+id_sobitia

def crop_name(path):
    """
    Нужна для того чтобы из пути достать название сайта после *html_txt/*
    :param path: path string
    :return: string name
    """
    pos_from = path.find('html_txt/') + 9
    name = otkritki_ok[pos_from:].split('/')[0]
    return name


def gen_txt_path(path):
    txt_path = path.replace('.html', '.txt')
    return txt_path


def parse(path):
    site = open(path, 'r', encoding='utf-8')
    soup = BeautifulSoup(site.read(), 'lxml')
    website = crop_name(path)
    if website == 'otkritkiok.ru':
        urls = soup.find_all('img', {'class': 'postcard-snippet__image'})
        amount = len(urls)
        new_text = open(gen_txt_path(path), 'a', encoding='utf-8')
        for i in urls:
            file_name = str(i['alt'])
            url_end = str(i['src']).split('/')[-1]
            new_text.write(url_end + ';' + file_name + '\n')
        new_text.close()
        print("Файл готов: " + gen_txt_path(path))
    else:
        print("Нет шаблона для сайта: " + website)


def download(url=None, section=None, from_place=None, fio=None,file_format='docx'):
    r = requests.get(url=url)
    path = 'E:\YandexDisc\YandexDisk\НГТУ\НТИ\web\доклады/'
    if section[:3] == '5.1':
        path += '5.1/'
    elif section[:3] == '5.2':
        path += '5.2/'
    elif section[:3] == '5.3':
        path += '5.3/'
    elif section[:3] == '5.4':
        path += '5.4/'
    if 'Новосибирск' in from_place:
        path += 'НГТУ/'
    else:
        path += 'ИНОГОРОДНИЕ/'
    file = open('{}{}.{}'.format(path, fio,file_format), "wb")
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
        download(url=lmnsv_link+file_name, fio=fio, from_place=from_place,section=section, file_format=file_format)

parse_t(otkritki_ok)