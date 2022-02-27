from selenium.webdriver.common.by import By
from pymorphy3 import MorphAnalyzer
from string import punctuation


# Создание множества market_words
def market_words_creater(file_name: str):
    # Лемматизация слов
    def lemmatizer(words, analyzer):
        market_words_lemma = set()
        for word in words:
            normal_form_of_word = analyzer.parse(word)[0].normal_form
            market_words_lemma.add(normal_form_of_word)
        return market_words_lemma

    market_words = set()
    with open(file_name, encoding='utf-8') as file:
        for line in file:
            market_words.add(line.lower().strip())
    return lemmatizer(market_words, MorphAnalyzer())


# Проверка наличия пунктуации в словах
def check_punctuation(word):
    for punct in punctuation:
        if punct in word:
            word = word.replace(punct, '')
    return word


# Парсинг ссылок из поискового запроса в Google
def google_links_parse(google, url):
    google.get(url)
    classes_with_urls = google.find_elements(By.CLASS_NAME, 'yuRUbf')
    markets_urls = set()
    for i in classes_with_urls:
        market_url = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
        if market_url[-3:] != 'pdf':
            markets_urls.add(market_url)
    return markets_urls


# Проверка является ли сайт магазином
def check_market_or_no(google, url, target_words_lemma, analyzer):
    try:
        google.get(url)
    except Exception:
        print(f"{url} - какая то гачибасня")

    all_text = google.find_element(By.TAG_NAME, 'body').text

    matches = set()
    # k = 0
    check = False
    for word in all_text.split():
        clear_word = check_punctuation(word)
        clear_word = analyzer.parse(clear_word)[0].normal_form
        if clear_word in target_words_lemma and clear_word not in matches:
            # k += 1
            check = True
            matches.add(clear_word)
            break

    # print(url)
    # print(f"{k}/{len(target_words_lemma)}")
    # print(matches)
    # print('-' * 10)

    return check
