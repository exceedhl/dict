#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from pathlib import Path

def sanitize_filename(filename):
    """
    清理文件名，移除或替换不适合作为文件名的字符
    """
    # 替换或删除不适合的字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # 删除Windows不允许的字符
    filename = re.sub(r'[（）]', '', filename)  # 删除中文括号
    filename = re.sub(r'[\(\)]', '', filename)  # 删除英文括号
    filename = filename.replace('—', '-')  # 替换长横线
    filename = filename.replace('–', '-')  # 替换中横线
    filename = filename.strip()  # 去除首尾空格
    
    # 如果文件名过长，截取前100个字符
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def create_filename_mapping():
    """
    创建extracted_filename到title的映射
    """
    try:
        with open('books.json', 'r', encoding='utf-8') as file:
            books_data = json.load(file)
        
        books = books_data.get('books', [])
        filename_mapping = {}
        
        for book in books:
            extracted_filename = book.get('extracted_filename', '')
            title = book.get('title', '')
            
            if extracted_filename and title:
                # 生成对应的txt文件名
                txt_filename = extracted_filename.replace('.json', '.txt')
                # 清理标题作为新文件名
                clean_title = sanitize_filename(title)
                new_filename = f"{clean_title}.txt"
                
                filename_mapping[txt_filename] = new_filename
        
        return filename_mapping
    
    except Exception as e:
        print(f"错误：创建文件名映射时出错：{e}")
        return {}

def rename_txt_files():
    """
    重命名book目录下的txt文件
    """
    book_dir = Path('book')
    
    if not book_dir.exists():
        print("错误：book目录不存在")
        return
    
    # 获取文件名映射
    filename_mapping = create_filename_mapping()
    
    if not filename_mapping:
        print("错误：无法创建文件名映射")
        return
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    print("=== 开始重命名文件 ===")
    
    for old_filename, new_filename in filename_mapping.items():
        old_path = book_dir / old_filename
        new_path = book_dir / new_filename
        
        if not old_path.exists():
            print(f"跳过：文件 {old_filename} 不存在")
            skipped_count += 1
            continue
        
        # 检查新文件名是否已存在
        if new_path.exists() and old_path != new_path:
            print(f"警告：目标文件 {new_filename} 已存在，跳过重命名")
            skipped_count += 1
            continue
        
        try:
            # 重命名文件
            old_path.rename(new_path)
            print(f"✓ 重命名：{old_filename} -> {new_filename}")
            success_count += 1
            
        except Exception as e:
            print(f"错误：重命名 {old_filename} 时出错：{e}")
            error_count += 1
    
    print(f"\n=== 重命名完成 ===")
    print(f"成功重命名：{success_count} 个文件")
    print(f"跳过文件：{skipped_count} 个文件")
    print(f"重命名失败：{error_count} 个文件")

def preview_rename():
    """
    预览重命名操作，不实际执行
    """
    book_dir = Path('book')
    
    if not book_dir.exists():
        print("错误：book目录不存在")
        return
    
    # 获取文件名映射
    filename_mapping = create_filename_mapping()
    
    if not filename_mapping:
        print("错误：无法创建文件名映射")
        return
    
    print("=== 重命名预览 ===")
    print("以下文件将被重命名：")
    print("-" * 100)
    
    existing_count = 0
    
    for old_filename, new_filename in filename_mapping.items():
        old_path = book_dir / old_filename
        new_path = book_dir / new_filename
        
        if old_path.exists():
            status = "✓ 存在"
            existing_count += 1
        else:
            status = "✗ 不存在"
        
        # 检查是否会覆盖现有文件
        conflict = ""
        if new_path.exists() and old_path != new_path:
            conflict = " [警告：目标文件已存在]"
        
        print(f"{status:<8} {old_filename:<35} -> {new_filename}{conflict}")
    
    print("-" * 100)
    print(f"总计：{len(filename_mapping)} 个映射，{existing_count} 个文件存在")

def show_current_files():
    """
    显示当前book目录下的txt文件
    """
    book_dir = Path('book')
    
    if not book_dir.exists():
        print("错误：book目录不存在")
        return
    
    txt_files = list(book_dir.glob('*.txt'))
    
    if not txt_files:
        print("book目录下没有找到txt文件")
        return
    
    print("=== 当前txt文件列表 ===")
    for i, file_path in enumerate(sorted(txt_files), 1):
        print(f"{i:2d}. {file_path.name}")
    
    print(f"\n总计：{len(txt_files)} 个txt文件")

def main():
    """
    主函数
    """
    print("=== 文件重命名工具 ===")
    print("1. 预览重命名操作")
    print("2. 执行重命名")
    print("3. 显示当前txt文件")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == "1":
            preview_rename()
        elif choice == "2":
            confirm = input("确定要执行重命名操作吗？(y/N): ").strip().lower()
            if confirm == 'y':
                rename_txt_files()
            else:
                print("操作已取消")
        elif choice == "3":
            show_current_files()
        elif choice == "4":
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()
