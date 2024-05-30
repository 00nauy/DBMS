import requests

def get_book_data_from_douban(query, max_results=10):
    url = "https://api.douban.com/v2/book/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    params = {
        'q': query,
        'count': max_results,
        'apikey': '0ac44ae016490db2204ce0a042db2916'
    }
    try:
        response = requests.get(url, headers=headers, params=params, proxies={'http': None, 'https': None})
        response.raise_for_status()  # 检查请求是否成功
        books = response.json().get('books', [])
        book_data = []
        for book in books:
            book_info = {
                'title': book.get('title', 'N/A'),
                'category': ', '.join(tag['name'] for tag in book.get('tags', [])) if 'tags' in book else 'N/A',
                'author': ', '.join(book.get('author', [])) if 'author' in book else 'N/A',
                'publisher': book.get('publisher', 'N/A'),
                'published_date': book.get('pubdate', 'N/A')
            }
            book_data.append(book_info)
        return book_data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return []

query = "计算机科学"
book_data = get_book_data_from_douban(query, max_results=10)
for book in book_data:
    print(book)
