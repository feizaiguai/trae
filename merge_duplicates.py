#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from difflib import SequenceMatcher

def extract_key_words(text):
    """提取文本中的关键词"""
    # 简化版本：提取主要的技术词汇和公司名称
    key_patterns = [
        r'\b[A-Z][a-zA-Z]*AI\b',  # AI相关
        r'\bOpenAI\b', r'\bGoogle\b', r'\bMicrosoft\b', r'\bAnthropic\b',
        r'\bGPT-?\d+\b', r'\bClaude\b', r'\bGemini\b', r'\bGrok\b',
        r'\b[A-Z][a-zA-Z]*\s?模型\b', r'\b[A-Z][a-zA-Z]*\s?平台\b'
    ]
    
    keywords = []
    for pattern in key_patterns:
        matches = re.findall(pattern, text)
        keywords.extend(matches)
    
    return set(keywords)

def calculate_similarity(text1, text2):
    """计算两个文本的相似度"""
    # 使用SequenceMatcher计算相似度
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def merge_duplicate_news():
    # 读取AI新闻分类整理版文件
    with open('D:/trae/AI新闻分类整理版.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # 分析现有内容，查找重复项
    lines = content.split('\n')
    news_items = {}
    duplicate_items = []
    
    # 提取所有新闻条目
    for line in lines:
        if line.strip() == '' or line.startswith('#') or line.startswith('##') or line.startswith('---') or line.startswith('新闻日期范围') or line.startswith('小白解读'):
            continue
        
        match = re.match(r'^(\d+)\. (.+)', line.strip())
        if match:
            num = int(match.group(1))
            content_text = match.group(2)
            news_items[num] = content_text
    
    print(f'原始文件包含{len(news_items)}条新闻')
    
    # 查找相似内容
    duplicates_found = []
    processed = set()
    
    for num1, content1 in news_items.items():
        if num1 in processed:
            continue
            
        similar_items = [num1]
        for num2, content2 in news_items.items():
            if num2 != num1 and num2 not in processed:
                similarity = calculate_similarity(content1, content2)
                if similarity > 0.6:  # 60%相似度阈值
                    similar_items.append(num2)
                    processed.add(num2)
        
        if len(similar_items) > 1:
            duplicates_found.append(similar_items)
        processed.add(num1)
    
    print(f'发现{len(duplicates_found)}组重复新闻')
    
    # 显示重复项详情
    for i, group in enumerate(duplicates_found):
        print(f'\n重复组 {i+1}: 新闻编号 {group}')
        for num in group[:2]:  # 只显示前两条
            print(f'  {num}: {news_items[num][:100]}...')
    
    
    # 如果发现重复项，询问用户是否要生成去重版本
    if duplicates_found:
        print(f'\n是否要生成去重后的文件？发现了{len(duplicates_found)}组重复内容')
        return duplicates_found, news_items
    else:
        print('\n未发现明显的重复内容')
        return [], news_items

def create_deduplicated_file(duplicates_found, news_items):
    """创建去重后的文件"""
    # 读取原始文件
    with open('D:/trae/AI新闻分类整理版.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 确定要移除的新闻编号（每组保留第一个）
    items_to_remove = set()
    for group in duplicates_found:
        # 保留每组的第一个，移除其他的
        for item in group[1:]:
            items_to_remove.add(item)
    
    print(f'将移除{len(items_to_remove)}条重复新闻：{sorted(items_to_remove)}')
    
    # 生成新的内容
    lines = content.split('\n')
    new_lines = []
    skip_next_explanation = False
    
    for line in lines:
        # 检查是否是要移除的新闻
        match = re.match(r'^(\d+)\. (.+)', line.strip())
        if match:
            num = int(match.group(1))
            if num in items_to_remove:
                skip_next_explanation = True
                continue  # 跳过这条新闻
            else:
                skip_next_explanation = False
        elif line.startswith('小白解读') and skip_next_explanation:
            continue  # 跳过被移除新闻的解读
        else:
            skip_next_explanation = False
            
        new_lines.append(line)
    
    # 重新编号
    final_lines = []
    current_num = 1
    
    for line in new_lines:
        match = re.match(r'^(\d+)\. (.+)', line.strip())
        if match:
            old_num = int(match.group(1))
            content_text = match.group(2)
            final_lines.append(f'{current_num}. {content_text}')
            current_num += 1
        else:
            final_lines.append(line)
    
    # 保存去重后的文件
    output_content = '\n'.join(final_lines)
    with open('D:/trae/AI新闻分类整理版_去重.txt', 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f'\n去重完成！')
    print(f'原始新闻：{len(news_items)}条')
    print(f'移除重复：{len(items_to_remove)}条')
    print(f'最终新闻：{len(news_items) - len(items_to_remove)}条')
    print(f'去重后的文件已保存为：AI新闻分类整理版_去重.txt')
    
    return len(news_items) - len(items_to_remove)

if __name__ == "__main__":
    duplicates, news = merge_duplicate_news()
    
    if duplicates:
        print(f"\n发现{len(duplicates)}组重复内容，正在生成去重文件...")
        final_count = create_deduplicated_file(duplicates, news)
        print(f"\n去重处理完成！最终保留{final_count}条新闻")
    else:
        print("\n未发现重复内容，无需去重处理")