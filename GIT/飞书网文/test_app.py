#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改后的应用数据处理
"""

from app import get_blog_data
import json

def test_blog_data():
    """测试博客数据获取和处理"""
    print("🚀 测试博客数据处理...\n")
    
    try:
        articles = get_blog_data()
        
        print(f"✅ 成功获取 {len(articles)} 篇文章\n")
        
        if articles:
            print("文章列表:")
            print("=" * 60)
            
            for i, article in enumerate(articles, 1):
                print(f"\n文章 {i}:")
                print(f"ID: {article['id']}")
                print(f"标题: {article['title']}")
                print(f"金句: {article['quote'][:100]}..." if len(article['quote']) > 100 else f"金句: {article['quote']}")
                print(f"点评: {article['review'][:100]}..." if len(article['review']) > 100 else f"点评: {article['review']}")
                print(f"内容: {article['content'][:100]}..." if len(article['content']) > 100 else f"内容: {article['content']}")
                print(f"预览: {article['preview']}")
                print("-" * 40)
        else:
            print("⚠️  没有获取到文章数据")
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_blog_data()
    
    if success:
        print("\n🎉 博客数据处理测试成功！")
    else:
        print("\n💥 博客数据处理测试失败！")