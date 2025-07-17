#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import zipfile
from pathlib import Path

def process_books_and_extract():
    """
    读取books.json文件，解压缩对应的zip文件，并将解压出的文件名写回JSON
    """
    try:
        # 读取books.json文件
        with open('books.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        books = data.get('books', [])
        book_dir = Path('book')

        # 确保book目录存在
        if not book_dir.exists():
            print("错误：book目录不存在")
            return

        processed_count = 0
        error_count = 0

        for i, book in enumerate(books):
            offlinedata = book.get('offlinedata', '')
            title = book.get('title', f'Book {i+1}')

            if not offlinedata:
                print(f"警告：书籍 '{title}' 没有offlinedata字段")
                continue

            zip_path = book_dir / offlinedata

            # 检查zip文件是否存在
            if not zip_path.exists():
                print(f"错误：找不到文件 {zip_path}")
                error_count += 1
                continue

            try:
                # 解压缩zip文件
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    # 获取zip文件内的所有文件名
                    file_names = zip_file.namelist()

                    if len(file_names) != 1:
                        print(f"警告：'{offlinedata}' 包含 {len(file_names)} 个文件，预期只有1个")

                    # 取第一个文件名（通常只有一个文件）
                    extracted_filename = file_names[0]

                    # 解压到book目录
                    zip_file.extractall(book_dir)

                    # 将解压出的文件名添加到JSON数据中
                    book['extracted_filename'] = extracted_filename

                    print(f"✓ 处理完成：{title}")
                    print(f"  ZIP文件: {offlinedata}")
                    print(f"  解压文件: {extracted_filename}")

                    processed_count += 1

            except zipfile.BadZipFile:
                print(f"错误：'{zip_path}' 不是有效的zip文件")
                error_count += 1
            except Exception as e:
                print(f"错误：处理 '{zip_path}' 时发生错误：{e}")
                error_count += 1

        # 将更新后的数据写回books.json
        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        print(f"\n处理完成！")
        print(f"成功处理：{processed_count} 个文件")
        print(f"处理失败：{error_count} 个文件")
        print(f"已更新 books.json 文件")

    except FileNotFoundError:
        print("错误：找不到 books.json 文件")
    except json.JSONDecodeError as e:
        print(f"错误：JSON解析失败 - {e}")
    except Exception as e:
        print(f"错误：{e}")

def list_extraction_status():
    """
    列出所有书籍的解压状态
    """
    try:
        with open('books.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        books = data.get('books', [])

        print(f"总共有 {len(books)} 本书籍")
        print("\n解压状态:")
        print("-" * 80)

        extracted_count = 0
        for i, book in enumerate(books):
            title = book.get('title', f'Book {i+1}')
            offlinedata = book.get('offlinedata', 'N/A')
            extracted_filename = book.get('extracted_filename', '')

            status = "✓ 已解压" if extracted_filename else "✗ 未解压"
            extracted_count += 1 if extracted_filename else 0

            print(f"{i+1:2d}. {title:<40} {status}")
            if extracted_filename:
                print(f"    解压文件: {extracted_filename}")
            print()

        print(f"\n统计: {extracted_count}/{len(books)} 本书已解压")

    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    print("=== 书籍解压处理工具 ===")
    print("1. 解压所有书籍")
    print("2. 查看解压状态")

    choice = input("请选择操作 (1/2): ").strip()

    if choice == "1":
        process_books_and_extract()
    elif choice == "2":
        list_extraction_status()
    else:
        print("无效选择")
