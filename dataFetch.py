import requests
from bs4 import BeautifulSoup

def get_book_data_from_douban(query, max_results=10):
    url = "https://search.douban.com/book/subject_search"
    params = {
        'search_text': query,
        'cat': '1001'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('div', class_='item-root', limit=max_results)
        book_data = []
        for book in books:
            title_tag = book.find('a', class_='title-text')
            title = title_tag.text.strip() if title_tag else 'N/A'
            
            pub_info_tag = book.find('div', class_='meta abstract')
            pub_info = pub_info_tag.text.strip() if pub_info_tag else 'N/A'
            pub_info_parts = pub_info.split('/')
            author = pub_info_parts[0].strip() if len(pub_info_parts) > 0 else 'N/A'
            publisher = pub_info_parts[-2].strip() if len(pub_info_parts) > 1 else 'N/A'
            published_date = pub_info_parts[-1].strip() if len(pub_info_parts) > 2 else 'N/A'
            
            book_info = {
                'title': title,
                'category': 'N/A',  # 豆瓣搜索结果页面不直接提供类别信息
                'author': author,
                'publisher': publisher,
                'published_date': published_date
            }
            book_data.append(book_info)
        return book_data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return []

query = "计算机科学"
book_data = get_book_data_from_douban(query, max_results=20)
for book in book_data:
    print(book)

