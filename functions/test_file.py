from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from pymorphy3 import MorphAnalyzer
from string import punctuation


def lemmatizer(target_words):
    analyzer = MorphAnalyzer()
    mySet = set()
    for word in target_words:
        normal_form_of_word = analyzer.parse(word)[0].normal_form
        mySet.add(normal_form_of_word)
    return mySet


def target_words_creater(file_name: str):
    mySet = set()
    with open(file_name, encoding='utf-8') as file:
        for line in file:
            mySet.add(line.lower().strip())
    return mySet


def google_links_parse(driver, url):
    driver.get(url)
    links = driver.find_elements(By.CLASS_NAME, 'yuRUbf')
    z = driver.find_elements_by_class_name('yuRUbf')
    pages = set()
    for i in links:
        page = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if page[-3:] != 'pdf':
            pages.add(page)
    return pages


def check_market_or_no(page, normal_forms_target_words):
    driver.get(page)
    all_text = driver.find_element(By.TAG_NAME, 'body').text

    k = 0
    # print(all_text)  # для отладки
    analyzer = MorphAnalyzer()
    sovpadeniya = set()
    for word in all_text.split():
        clear_word = word

        for punct in punctuation:
            if punct in clear_word:
                clear_word = clear_word.replace(punct, '')

        clear_word = analyzer.parse(clear_word)[0].normal_form
        if clear_word in normal_forms_target_words and clear_word not in sovpadeniya:
            k += 1
            sovpadeniya.add(clear_word)

    print(page)
    print(f"{k}/{len(normal_forms_target_words)}")
    print(sovpadeniya)
    print('-' * 10)


urls = [
    'https://www.google.com/search?q=%D0%91%D0%9E%D0%9B%D0%A2%3B+%D0%A1%D0%A2%D0%90%D0%9D%D0%94%D0%90%D0%A0%D0%A2+%D0%93%D0%9E%D0%A1%D0%A27817+DIN609%2C+%D0%9E%D0%91%D0%9E%D0%97%D0%9D%D0%90%D0%A7%D0%95%D0%9D%D0%98%D0%95+M36-6G%D0%A5200%2C+%D0%9A%D0%9B%D0%90%D0%A1%D0%A1+%D0%9F%D0%A0%D0%9E%D0%A7%D0%9D%D0%9E%D0%A1%D0%A2%D0%98+10.9%2C+%D0%9C%D0%90%D0%A2%D0%95%D0%A0%D0%98%D0%90%D0%9B+%D0%A1%D0%A2%D0%90%D0%9B%D0%AC+40%D0%A5',
    'https://www.google.com/search?q=%D0%9C%D0%B0%D0%BD%D0%B6%D0%B5%D1%82%D0%B0+%D0%9C50%D1%8570+%D0%93%D0%9E%D0%A1%D0%A2+22704',
    'https://www.google.com/search?q=%D0%9C%D0%B0%D0%BD%D0%B6%D0%B5%D1%82%D0%B0+%D1%80%D0%B5%D0%B7%D0%B8%D0%BD%D0%BE%D0%B2%D0%B0%D1%8F+%D0%B0%D1%80%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F+%D0%B4%D0%BB%D1%8F+%D0%B2%D0%B0%D0%BB%D0%BE%D0%B2+1.2-120%D1%85150%D1%8512-1+%D0%93%D0%9E%D0%A1%D0%A2+8752'
]

ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)

target_words = target_words_creater('target_words.txt')

normal_forms_target_words = lemmatizer(target_words)

# page = 'https://www.google.com/search?q=%D0%93%D0%9E%D0%A1%D0%A2+22704&oq=%D0%93%D0%9E%D0%A1%D0%A2+22704'  # для отладки
# check_market_or_no(page, normal_forms_target_words)  # для отладки

pages = google_links_parse(driver, 'https://www.google.com/search?q=%D0%93%D0%9E%D0%A1%D0%A2+22704')

for page in pages:
    check_market_or_no(page, normal_forms_target_words)

driver.quit()
