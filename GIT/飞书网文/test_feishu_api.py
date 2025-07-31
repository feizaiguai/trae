#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书API连接测试脚本
"""

import requests
import json
from config import config
import os

def test_feishu_connection():
    """测试飞书API连接"""
    
    # 获取配置
    app_config = config['production']
    app_id = app_config.FEISHU_APP_ID
    app_secret = app_config.FEISHU_APP_SECRET
    base_id = app_config.BASE_ID
    table_id = app_config.TABLE_ID
    
    print(f"测试配置:")
    print(f"APP_ID: {app_id}")
    print(f"APP_SECRET: {app_secret[:10]}...")
    print(f"BASE_ID: {base_id}")
    print(f"TABLE_ID: {table_id}")
    print("\n" + "="*50 + "\n")
    
    # 步骤1: 获取访问令牌
    print("步骤1: 获取访问令牌...")
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    token_headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    try:
        token_response = requests.post(token_url, headers=token_headers, json=token_data)
        token_result = token_response.json()
        
        print(f"令牌请求状态码: {token_response.status_code}")
        print(f"令牌响应: {json.dumps(token_result, indent=2, ensure_ascii=False)}")
        
        if token_result.get('code') == 0:
            access_token = token_result['tenant_access_token']
            print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
        else:
            print(f"❌ 访问令牌获取失败: {token_result.get('msg', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 访问令牌请求异常: {e}")
        return False
    
    print("\n" + "-"*30 + "\n")
    
    # 步骤2: 获取表格记录
    print("步骤2: 获取表格记录...")
    records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_id}/tables/{table_id}/records"
    records_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        records_response = requests.get(records_url, headers=records_headers)
        records_result = records_response.json()
        
        print(f"记录请求状态码: {records_response.status_code}")
        print(f"记录响应: {json.dumps(records_result, indent=2, ensure_ascii=False)}")
        
        if records_result.get('code') == 0:
            items = records_result.get('data', {}).get('items', [])
            print(f"✅ 表格记录获取成功，共 {len(items)} 条记录")
            
            # 显示前几条记录的字段信息
            if items:
                print("\n前3条记录的字段信息:")
                for i, item in enumerate(items[:3]):
                    print(f"\n记录 {i+1}:")
                    fields = item.get('fields', {})
                    for key, value in fields.items():
                        if isinstance(value, str) and len(value) > 50:
                            value = value[:50] + "..."
                        print(f"  {key}: {value}")
            else:
                print("⚠️  表格中没有记录")
                
            return True
        else:
            print(f"❌ 表格记录获取失败: {records_result.get('msg', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 表格记录请求异常: {e}")
        return False

if __name__ == '__main__':
    print("🚀 开始测试飞书API连接...\n")
    success = test_feishu_connection()
    
    if success:
        print("\n🎉 飞书API连接测试成功！")
    else:
        print("\n💥 飞书API连接测试失败！")
        print("\n可能的问题:")
        print("1. APP_ID 或 APP_SECRET 配置错误")
        print("2. BASE_ID 或 TABLE_ID 配置错误")
        print("3. 飞书应用权限不足")
        print("4. 网络连接问题")
        print("5. 环境变量未正确设置")