#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 chatlog.txt 文件，整理成指定格式
"""

import re

def parse_chatlog(input_file, output_file):
    """解析对话日志文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    conversations = []
    current_conversation = []
    current_role = None
    current_content = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检测新对话开始
        if '【内测】' in line:
            # 保存之前的对话
            if current_conversation:
                conversations.append(current_conversation)
            current_conversation = []
            current_role = None
            current_content = []
            
            # 跳过标题、错误信息、对话ID等行，找到第一条用户消息
            i += 1
            while i < len(lines):
                test_line = lines[i].strip()
                # 跳过空行和元数据
                if (not test_line or 
                    test_line == '对话 ID' or 
                    'age_match' in test_line or
                    len(test_line) == 36 and '-' in test_line):  # UUID格式
                    i += 1
                    continue
                # 找到第一条用户消息（不是🤖，不是时间戳，不是元数据）
                if (test_line and 
                    test_line != '🤖' and 
                    not test_line.startswith('耗时') and
                    not test_line.startswith('花费 Token') and
                    test_line != '·' and
                    not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', test_line)):
                    current_conversation.append(('用户', test_line))
                    current_role = '用户'
                    i += 1
                    break
                i += 1
            continue
        
        # 检测AI回复标记
        if line == '🤖':
            # 保存之前的消息
            if current_role == '用户' and current_content:
                content = '\n'.join(current_content).strip()
                if content:
                    current_conversation.append((current_role, content))
                current_content = []
            
            # 开始收集AI回复
            current_role = 'AI助理'
            current_content = []
            i += 1
            continue
        
        # 检测时间戳行（格式：2025-11-30 16:39:24）
        if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', line):
            # 保存之前的AI回复
            if current_role == 'AI助理' and current_content:
                content = '\n'.join(current_content).strip()
                if content:
                    current_conversation.append(('AI助理', content))
                current_content = []
            
            # 下一行应该是用户消息
            i += 1
            if i < len(lines):
                user_msg = lines[i].strip()
                # 跳过空行和特殊标记
                if (user_msg and 
                    user_msg != '🤖' and 
                    user_msg != '对话 ID' and
                    not user_msg.startswith('【') and
                    not user_msg.startswith('耗时') and
                    not user_msg.startswith('花费 Token') and
                    user_msg != '·' and
                    not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', user_msg)):
                    current_role = '用户'
                    current_content = [user_msg]
                    i += 1
                    continue
            else:
                # 文件末尾，没有更多用户消息
                break
        
        # 跳过元数据行
        if (line.startswith('耗时') or 
            line.startswith('花费 Token') or 
            line == '·' or 
            line == '' or 
            'age_match' in line or
            line == '对话 ID' or
            (len(line) == 36 and '-' in line and line.count('-') == 4)):  # UUID
            i += 1
            continue
        
        # 收集内容（跳过时间戳）
        if current_role and line and not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', line):
            current_content.append(line)
        
        i += 1
    
    # 保存最后一个对话
    if current_role and current_content:
        content = '\n'.join(current_content).strip()
        if content:
            current_conversation.append((current_role, content))
    if current_conversation:
        conversations.append(current_conversation)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, conv in enumerate(conversations, 1):
            f.write(f'对话{idx}:\n\n')
            for role, content in conv:
                # 清理内容中的多余空行
                content = re.sub(r'\n{3,}', '\n\n', content)
                f.write(f'{role}: {content}\n\n')
            f.write('\n' + '='*80 + '\n\n')
    
    print(f'成功解析 {len(conversations)} 个对话，已保存到 {output_file}')

if __name__ == '__main__':
    parse_chatlog('chatlog.txt', 'chatlog_formatted.txt')
