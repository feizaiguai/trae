#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def add_numbers_to_news():
    # 读取文件
    with open('D:/trae/AI新闻分类整理版.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    output_lines = []
    news_counter = 1
    
    for i, line in enumerate(lines):
        # 如果这一行看起来像是新闻内容的开始（非空行，非小白解读，非标题，非其他格式化内容）
        if (line.strip() and 
            not line.startswith('小白解读：') and 
            not line.startswith('#') and 
            not line.startswith('---') and
            not line.startswith('本次处理统计') and
            not line.startswith('说明：') and
            not line.startswith('新闻日期范围') and
            not line.startswith('##') and
            not line.startswith('**') and
            not line.startswith('- ') and
            not line.startswith('*') and
            not line.startswith('包括：') and
            not line.startswith('✅') and
            not line.startswith('📊') and
            not line.startswith('🎯') and
            not '完成状态' in line and
            not '最终统计' in line and
            not '质量保证' in line and
            not '分类统计' in line):
            
            # 检查这不是一个已经有数字的行
            if not re.match(r'^\d+\.', line.strip()):
                # 检查下一行是否是小白解读（确认这是新闻内容）
                next_line_idx = i + 1
                while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                    next_line_idx += 1
                
                if (next_line_idx < len(lines) and 
                    lines[next_line_idx].startswith('小白解读：')):
                    # 添加序号
                    numbered_line = f"{news_counter}. {line.strip()}"
                    output_lines.append(numbered_line)
                    news_counter += 1
                else:
                    output_lines.append(line)
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)
    
    # 写回文件
    with open('D:/trae/AI新闻分类整理版.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"已为 {news_counter - 1} 条新闻添加序号")

if __name__ == "__main__":
    add_numbers_to_news()