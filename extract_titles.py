#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def extract_book_info_from_booklists():
    """
    从booklists.json文件中提取书籍信息，输出为JSON格式
    包含title、wordNum和introduce三部分信息
    """
    try:
        # 读取JSON文件
        with open('booklists.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取书籍信息
        books_info_list = []
        books_info = data.get('data', {}).get('normalBooksInfo', [])

        for book in books_info:
            book_info = {
                "title": book.get('title', ''),
                "word_num": book.get('wordNum', 0),
                "introduce": book.get('introduce', ''),
                "offlinedata": book.get('offlinedata')
            }
            books_info_list.append(book_info)

        # 输出JSON格式
        output = {
            "total_books": len(books_info_list),
            "books": books_info_list
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except FileNotFoundError:
        print(json.dumps({"error": "找不到 booklists.json 文件"}, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON解析失败 - {e}"}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    extract_book_info_from_booklists()
