#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from pathlib import Path

def extract_head_words(json_file_path):
    """
    从JSON文件中提取所有headWord
    """
    head_words = []
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # 将每一行当作一个JSON对象处理
            for line in content.strip().split('\n'):
                if line.strip():
                    try:
                        word_data = json.loads(line)
                        head_word = word_data.get('headWord', '')
                        if head_word:
                            head_words.append(head_word.strip().lower())
                    except json.JSONDecodeError:
                        continue
                        
    except Exception as e:
        print(f"错误：读取文件 {json_file_path} 时出错：{e}")
        return []
    
    return head_words

def split_words_into_lists(words, target_size=50):
    """
    将单词列表分成多个子列表，每个子列表大约包含target_size个单词
    避免单个list的单词过少
    """
    if not words:
        return []
    
    total_words = len(words)
    if total_words <= target_size:
        return [words]
    
    # 计算需要的列表数量
    num_lists = max(1, round(total_words / target_size))
    
    # 确保每个列表至少有一定数量的单词
    min_words_per_list = 20
    if total_words / num_lists < min_words_per_list:
        num_lists = max(1, total_words // min_words_per_list)
    
    # 计算每个列表的大小
    words_per_list = total_words // num_lists
    remainder = total_words % num_lists
    
    word_lists = []
    start_idx = 0
    
    for i in range(num_lists):
        # 前面的列表多分配一个单词（如果有余数）
        current_size = words_per_list + (1 if i < remainder else 0)
        end_idx = start_idx + current_size
        
        word_lists.append(words[start_idx:end_idx])
        start_idx = end_idx
    
    return word_lists

def generate_word_list_content(word_lists, title):
    """
    生成单词列表的文本内容
    """
    content = f"# {title}\n\n"
    
    for i, word_list in enumerate(word_lists, 1):
        content += f"List {i}\n"
        content += ", ".join(word_list) + "\n\n"
    
    return content

def process_books_and_generate_lists():
    """
    处理books.json中的每本书，生成单词列表文件
    """
    try:
        # 读取books.json
        with open('books.json', 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        
        books = books_data.get('books', [])
        book_dir = Path('book')
        
        if not book_dir.exists():
            print("错误：book目录不存在")
            return
        
        processed_count = 0
        error_count = 0
        
        for book in books:
            extracted_filename = book.get('extracted_filename', '')
            title = book.get('title', '')
            
            if not extracted_filename:
                print(f"跳过：书籍 '{title}' 没有extracted_filename")
                continue
            
            json_file_path = book_dir / extracted_filename
            
            if not json_file_path.exists():
                print(f"错误：找不到文件 {json_file_path}")
                error_count += 1
                continue
            
            print(f"处理中：{title}")
            
            # 提取headWord
            head_words = extract_head_words(json_file_path)
            
            if not head_words:
                print(f"警告：从 {extracted_filename} 中没有提取到单词")
                error_count += 1
                continue
            
            # 去重并按字母排序
            unique_words = sorted(set(head_words))
            
            # 分成多个列表
            word_lists = split_words_into_lists(unique_words)
            
            # 生成内容
            content = generate_word_list_content(word_lists, title)
            
            # 生成txt文件名（与extracted_filename同名但扩展名为.txt）
            txt_filename = extracted_filename.replace('.json', '.txt')
            txt_file_path = book_dir / txt_filename
            
            # 写入文件
            try:
                with open(txt_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(content)
                
                print(f"✓ 成功生成：{txt_filename}")
                print(f"  提取单词数：{len(head_words)}")
                print(f"  去重后单词数：{len(unique_words)}")
                print(f"  分成 {len(word_lists)} 个列表")
                
                processed_count += 1
                
            except Exception as e:
                print(f"错误：写入文件 {txt_filename} 时出错：{e}")
                error_count += 1
        
        print(f"\n=== 处理完成 ===")
        print(f"成功处理：{processed_count} 本书")
        print(f"处理失败：{error_count} 本书")
        
    except FileNotFoundError:
        print("错误：找不到 books.json 文件")
    except json.JSONDecodeError as e:
        print(f"错误：JSON解析失败 - {e}")
    except Exception as e:
        print(f"错误：{e}")

def show_sample_output():
    """
    显示示例输出
    """
    sample_words = ['abandon', 'ability', 'able', 'about', 'above', 'abroad', 'absent', 'absolute', 'absorb', 'abstract']
    word_lists = split_words_into_lists(sample_words, target_size=4)
    content = generate_word_list_content(word_lists, "示例单词书")
    
    print("=== 示例输出格式 ===")
    print(content)

if __name__ == "__main__":
    print("=== 单词列表生成工具 ===")
    print("1. 生成所有单词列表")
    print("2. 显示示例输出")
    
    choice = input("请选择操作 (1/2): ").strip()
    
    if choice == "1":
        process_books_and_generate_lists()
    elif choice == "2":
        show_sample_output()
    else:
        print("无效选择")
