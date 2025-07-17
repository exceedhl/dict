#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def add_tags_to_books():
    """
    从booklists.json中读取tag信息，并添加到books.json中
    """
    try:
        # 读取booklists.json文件
        with open('booklists.json', 'r', encoding='utf-8') as file:
            booklists_data = json.load(file)
        
        # 读取books.json文件
        with open('books.json', 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        
        # 从booklists.json中创建offlinedata到tags的映射
        offlinedata_to_tags = {}
        
        books_info = booklists_data.get('data', {}).get('normalBooksInfo', [])
        
        for book in books_info:
            offlinedata = book.get('offlinedata', '')
            tags = book.get('tags', [])
            
            # 提取tagName作为数组
            tag_names = [tag.get('tagName', '') for tag in tags if tag.get('tagName')]
            
            if offlinedata:
                offlinedata_to_tags[offlinedata] = tag_names
        
        # 为books.json中的每一本书添加tags
        books = books_data.get('books', [])
        updated_count = 0
        
        for book in books:
            offlinedata = book.get('offlinedata', '')
            
            if offlinedata in offlinedata_to_tags:
                book['tags'] = offlinedata_to_tags[offlinedata]
                updated_count += 1
            else:
                # 如果找不到对应的tags，设置为空数组
                book['tags'] = []
                print(f"警告：找不到 '{offlinedata}' 对应的tags信息")
        
        # 将更新后的数据写回books.json
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(books_data, file, ensure_ascii=False, indent=2)
        
        print(f"✓ 成功为 {updated_count} 本书添加了tags信息")
        print(f"✓ 更新后的数据已写入 books.json")
        
        # 显示一些统计信息
        print("\n标签统计：")
        tag_count = {}
        for book in books:
            for tag in book.get('tags', []):
                tag_count[tag] = tag_count.get(tag, 0) + 1
        
        for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {tag}: {count} 本书")
        
    except FileNotFoundError as e:
        print(f"错误：找不到文件 {e}")
    except json.JSONDecodeError as e:
        print(f"错误：JSON解析失败 - {e}")
    except Exception as e:
        print(f"错误：{e}")

def check_tag_status():
    """
    检查books.json中的tags添加状态
    """
    try:
        with open('books.json', 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        
        books = books_data.get('books', [])
        
        print(f"总共有 {len(books)} 本书")
        print("\nTags状态:")
        print("-" * 80)
        
        books_with_tags = 0
        for i, book in enumerate(books):
            title = book.get('title', f'Book {i+1}')
            tags = book.get('tags', [])
            
            if tags:
                books_with_tags += 1
                tags_str = ', '.join(tags)
                print(f"{i+1:2d}. {title:<50} [{tags_str}]")
            else:
                print(f"{i+1:2d}. {title:<50} [无标签]")
        
        print(f"\n统计: {books_with_tags}/{len(books)} 本书有标签")
        
    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    print("=== 标签添加工具 ===")
    print("1. 添加标签到books.json")
    print("2. 查看标签状态")
    
    choice = input("请选择操作 (1/2): ").strip()
    
    if choice == "1":
        add_tags_to_books()
    elif choice == "2":
        check_tag_status()
    else:
        print("无效选择")
