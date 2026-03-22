#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浙大导师信息爬取脚本
从主页面获取导师链接，访问个人页面提取详细信息
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from datetime import datetime

# 主页面内容（已获取）
MAIN_PAGE_CONTENT = """
序号	姓名	所在学院	专业学位类别
1	蔡云龙	信息与电子工程学院	电子信息
https://person.zju.edu.cn/ylcai
2	曹臻	信息与电子工程学院	电子信息
https://person.zju.edu.cn/eezcao
3	车录锋	信息与电子工程学院	电子信息
https://person.zju.edu.cn/mems
4	陈红胜	信息与电子工程学院	电子信息
https://person.zju.edu.cn/chenhongsheng
5	陈惠芳	信息与电子工程学院	电子信息
https://person.zju.edu.cn/chenhuifang
6	陈晓明	信息与电子工程学院	电子信息
https://person.zju.edu.cn/chenxiaoming
7	单杭冠	信息与电子工程学院	电子信息
https://person.zju.edu.cn/hshan
8	董树荣	信息与电子工程学院	电子信息
https://person.zju.edu.cn/sean
9	杜歆	信息与电子工程学院	电子信息
https://person.zju.edu.cn/duxin
10	杜阳	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0004142
11	高飞	信息与电子工程学院	电子信息
https://person.zju.edu.cn/feigao
12	龚小谨	信息与电子工程学院	电子信息
https://person.zju.edu.cn/gongxj
13	郝寅雷	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0005147
14	胡浩基	信息与电子工程学院	电子信息
https://person.zju.edu.cn/huhaoji
15	皇甫江涛	信息与电子工程学院	电子信息
https://person.zju.edu.cn/huangfujt
16	黄崇文	信息与电子工程学院	电子信息
https://person.zju.edu.cn/chongwenhuang
17	黄科杰	信息与电子工程学院	电子信息
https://person.zju.edu.cn/huangkejie
18	金浩	信息与电子工程学院	电子信息
https://person.zju.edu.cn/hjin
19	金韬	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0096016
20	金晓峰	信息与电子工程学院	电子信息
https://person.zju.edu.cn/jxf
21	雷鸣	信息与电子工程学院	电子信息
https://person.zju.edu.cn/lm1029
22	李东晓	信息与电子工程学院	电子信息
https://person.zju.edu.cn/lidx
23	李建龙	信息与电子工程学院	电子信息
https://person.zju.edu.cn/JLLi
24	李军伟	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0020196
25	李旻	信息与电子工程学院	电子信息
https://person.zju.edu.cn/limin
26	李荣鹏	信息与电子工程学院	电子信息
https://person.zju.edu.cn/rongpeng
27	李英明	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yingming
28	李鹰	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yingli
29	李宇波	信息与电子工程学院	电子信息
https://person.zju.edu.cn/leelinear
30	廖依伊	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yiyiliao
31	林宏焘	信息与电子工程学院	电子信息
https://person.zju.edu.cn/hometown
32	林时胜	信息与电子工程学院	电子信息
https://person.zju.edu.cn/shishenglin
33	林晓	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xiaolinGroup
34	林星	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0618098
35	刘安	信息与电子工程学院	电子信息
https://person.zju.edu.cn/anliu
36	刘而云	信息与电子工程学院	电子信息
https://person.zju.edu.cn/eryunliu
37	刘鹏	信息与电子工程学院	电子信息
https://person.zju.edu.cn/liupeng
38	刘英	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yliu
39	骆季奎	信息与电子工程学院	电子信息
https://person.zju.edu.cn/LuoJikui
40	潘赟	信息与电子工程学院	电子信息
https://person.zju.edu.cn/panyun
41	钱浩亮	信息与电子工程学院	电子信息
https://person.zju.edu.cn/haoliangqian
42	沙威	信息与电子工程学院	电子信息
https://person.zju.edu.cn/weisha
43	沈海斌	信息与电子工程学院	电子信息
https://person.zju.edu.cn/345890fjdasjoidf
44	沈会良	信息与电子工程学院	电子信息
https://person.zju.edu.cn/shenhl
45	史峥	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0000280
46	史治国	信息与电子工程学院	电子信息
https://person.zju.edu.cn/shizg
47	宋牟平	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0098163
48	孙斌	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0095070
49	汪小知	信息与电子工程学院	电子信息
https://person.zju.edu.cn/wxz
50	王浩刚	信息与电子工程学院	电子信息
https://person.zju.edu.cn/cemwang
51	王匡	信息与电子工程学院	电子信息
https://person.zju.edu.cn/wangkuang
52	王维东	信息与电子工程学院	电子信息
https://person.zju.edu.cn/wdwd
53	王玮	信息与电子工程学院	电子信息
https://person.zju.edu.cn/wangw
54	王勇	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0002259
55	王曰海	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0099184
56	王作佳	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zuojiawang
57	魏准	信息与电子工程学院	电子信息
https://person.zju.edu.cn/Zhun
58	吴锡东	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xwu
59	夏明俊	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xiamingjun
60	项志宇	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xiangzy
61	谢磊	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xielei
62	徐元欣	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xuyuanxin
63	杨建义	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yjy
64	杨倩倩	信息与电子工程学院	电子信息
https://person.zju.edu.cn/qianqianyang
65	杨怡豪	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yangyihao
66	叶德信	信息与电子工程学院	电子信息
https://person.zju.edu.cn/dexinye
67	叶志	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yezhi
68	尹文言	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0008089
69	尹勋钊	信息与电子工程学院	电子信息
https://person.zju.edu.cn/xunzhaoyin
70	于云龙	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yunlong
71	余官定	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yuguanding
72	虞露	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yul
73	詹启伟	信息与电子工程学院	电子信息
https://person.zju.edu.cn/qiweizhan
74	张朝阳	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhaoyangzhang
75	章献民	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhangxm
76	赵航芳	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhf_zju
77	赵亮	信息与电子工程学院	电子信息
https://person.zju.edu.cn/liangzhao
78	赵民建	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0003171
79	赵明敏	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhaomingmin
80	郑斌	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhengbin
81	郑史烈	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhengsl
82	钟杰	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhongjie
83	周成伟	信息与电子工程学院	电子信息
https://person.zju.edu.cn/zhouchw
84	李达	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0021359
85	李凯	信息与电子工程学院	电子信息
https://person.zju.edu.cn/Likai
86	冉立新	信息与电子工程学院	电子信息
https://person.zju.edu.cn/ranlx
87	魏兴昌	信息与电子工程学院	电子信息
https://person.zju.edu.cn/weixc
88	余显斌	信息与电子工程学院	电子信息
无链接
89	刘峰	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0019025
90	马蔚	信息与电子工程学院	电子信息
https://person.zju.edu.cn/weima
91	程磊	信息与电子工程学院	电子信息
https://person.zju.edu.cn/leicheng
92	张婷	信息与电子工程学院	电子信息
https://person.zju.edu.cn/tzhang
93	刘雷	信息与电子工程学院	电子信息
https://person.zju.edu.cn/leiliu_cn
94	金日成	信息与电子工程学院	电子信息
https://person.zju.edu.cn/richengjin
95	回晓楠	信息与电子工程学院	电子信息
https://person.zju.edu.cn/huixn
96	李世龙	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0023171
97	杨宗银	信息与电子工程学院	电子信息
https://person.zju.edu.cn/0020059/0.html
98	张鹿	信息与电子工程学院	电子信息
https://person.zju.edu.cn/luzhang
99	杨照辉	信息与电子工程学院	电子信息
https://person.zju.edu.cn/yangzhaohui
100	吴汉明	集成电路学院	电子信息
https://person.zju.edu.cn/0019828
101	程志渊	集成电路学院	电子信息
https://person.zju.edu.cn/zcheng
102	高大为	集成电路学院	电子信息
https://person.zju.edu.cn/0021056
103	汪涛	集成电路学院	电子信息
https://person.zju.edu.cn/wangtao
104	张睿	集成电路学院	电子信息
https://person.zju.edu.cn/0012183
105	程然	集成电路学院	电子信息
https://person.zju.edu.cn/chengran
106	卓成	集成电路学院	电子信息
https://person.zju.edu.cn/chengzhuo
107	陈一宁	集成电路学院	电子信息
https://person.zju.edu.cn/yiningchen/
108	倪东	集成电路学院	电子信息
https://person.zju.edu.cn/nidong
109	丁勇	集成电路学院	电子信息
https://person.zju.edu.cn/DVIE
110	黄凯	集成电路学院	电子信息
https://person.zju.edu.cn/kai_huang
111	虞小鹏	集成电路学院	电子信息
https://person.zju.edu.cn/yu
112	谭年熊	集成电路学院	电子信息
https://person.zju.edu.cn/0005012
113	赵博	集成电路学院	电子信息
https://person.zju.edu.cn/zhaobo
114	高翔	集成电路学院	电子信息
https://person.zju.edu.cn/xianggao
115	罗宇轩	集成电路学院	电子信息
https://person.zju.edu.cn/luoyx
116	张培勇	集成电路学院	电子信息
https://person.zju.edu.cn/zhangpy
117	屈万园	集成电路学院	电子信息
https://person.zju.edu.cn/wanyuanqu
118	朱晓雷	集成电路学院	电子信息
https://person.zju.edu.cn/zhuxl
119	俞滨	集成电路学院	电子信息
https://person.zju.edu.cn/0019029
120	徐明生	集成电路学院	电子信息
https://person.zju.edu.cn/graphene
121	赵昱达	集成电路学院	电子信息
https://person.zju.edu.cn/yudazhao
122	任堃	集成电路学院	电子信息
https://person.zju.edu.cn/0021379
123	郑飞君	集成电路学院	电子信息
https://person.zju.edu.cn/frank_zheng
124	宋爽	集成电路学院	电子信息
https://person.zju.edu.cn/shuangsong
125	李云龙	集成电路学院	电子信息
https://person.zju.edu.cn/0022217
126	张运炎	集成电路学院	电子信息
https://person.zju.edu.cn/123321
127	孙奇	集成电路学院	电子信息
https://person.zju.edu.cn/qisunchn
128	张亦舒	集成电路学院	电子信息
https://ic.zju.edu.cn/2024/0604/c81879a2928352/page.htm
129	方文章	集成电路学院	电子信息
https://ic.zju.edu.cn/2024/0529/c81879a2924989/page.htm
130	徐杨	集成电路学院	电子信息
https://person.zju.edu.cn/yangxu
131	崔强	集成电路学院	电子信息
https://person.zju.edu.cn/qiangcui
132	赵梦恋	集成电路学院	电子信息
https://person.zju.edu.cn/zhaomenglian
133	谭志超	集成电路学院	电子信息
https://person.zju.edu.cn/zctan
"""

# 解析导师数据
def parse_professors():
    """从主页面内容解析导师列表"""
    professors = []
    lines = MAIN_PAGE_CONTENT.strip().split('\n')
    
    # 匹配模式: 数字 姓名 学院 类别 + URL
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # 尝试匹配序号开头的行
        match = re.match(r'^(\d+)\s+(.+?)\s+(信息与电子工程学院|集成电路学院)\s+(.+)$', line)
        if match:
            idx = int(match.group(1))
            name = match.group(2).strip()
            college = match.group(3).strip()
            category = match.group(4).strip()
            
            # 下一行应该是链接
            url = None
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('http'):
                    url = next_line
                    i += 1
            
            professors.append({
                '序号': idx,
                '姓名': name,
                '学院': college,
                '专业学位类别': category,
                '个人页面链接': url if url and url.startswith('http') else ''
            })
        i += 1
    
    return professors

# 获取导师个人页面信息
def fetch_professor_info(url, name, session):
    """访问导师个人页面，提取研究方向等信息"""
    if not url:
        return {
            '姓名': name,
            '职称': '',
            '研究方向大类': '',
            '研究方向小类': '',
            '邮箱': '',
            '电话': '',
            '错误': '无个人页面链接'
        }
    
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        response = session.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return {
                '姓名': name,
                '职称': '',
                '研究方向大类': '',
                '研究方向小类': '',
                '邮箱': '',
                '电话': '',
                '错误': f'HTTP状态码: {response.status_code}'
            }
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        info = {
            '姓名': name,
            '职称': '',
            '研究方向大类': '',
            '研究方向小类': '',
            '邮箱': '',
            '电话': '',
            '错误': ''
        }
        
        # 尝试多种方式提取信息
        # 方式1: 查找常见的个人主页结构
        text = soup.get_text(separator='\n', strip=True)
        
        # 提取职称
        title_patterns = [
            r'职\s*称[：:]\s*([^\n]+)',
            r'(教授|副教授|研究员|副研究员|讲师|高级工程师|正高级工程师)',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, text)
            if match:
                info['职称'] = match.group(1).strip()
                break
        
        # 提取研究方向
        research_patterns = [
            r'研究方向[：:]\s*([^\n]+)',
            r'研究领域[：:]\s*([^\n]+)',
            r'研究兴趣[：:]\s*([^\n]+)',
        ]
        for pattern in research_patterns:
            match = re.search(pattern, text)
            if match:
                research = match.group(1).strip()
                # 尝试分割研究方向
                if '、' in research or '，' in research or ',' in research:
                    parts = re.split(r'[、，,]', research, maxsplit=1)
                    if len(parts) > 1:
                        info['研究方向大类'] = parts[0].strip()
                        info['研究方向小类'] = parts[1].strip()
                    else:
                        info['研究方向大类'] = research
                else:
                    info['研究方向大类'] = research
                break
        
        # 提取邮箱
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        if emails:
            info['邮箱'] = emails[0]
        
        # 提取电话
        phone_pattern = r'(?:电话|Tel|Phone)[：:]\s*([0-9\-+()\s]+)'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            info['电话'] = phone_match.group(1).strip()
        
        # 尝试从特定元素提取
        # 查找包含个人信息的div或table
        for tag in soup.find_all(['div', 'td', 'span', 'p']):
            tag_text = tag.get_text(strip=True)
            
            # 职称
            if '职称' in tag_text and not info['职称']:
                parent = tag.find_parent()
                if parent:
                    parent_text = parent.get_text(strip=True)
                    match = re.search(r'职\s*称[：:]\s*([^\n]+)', parent_text)
                    if match:
                        info['职称'] = match.group(1).strip()
            
            # 研究方向
            if '研究方向' in tag_text and not info['研究方向大类']:
                parent = tag.find_parent()
                if parent:
                    parent_text = parent.get_text(strip=True)
                    match = re.search(r'研究方向[：:]\s*([^\n]+)', parent_text)
                    if match:
                        research = match.group(1).strip()
                        if '、' in research or '，' in research:
                            parts = re.split(r'[、，]', research, maxsplit=1)
                            if len(parts) > 1:
                                info['研究方向大类'] = parts[0].strip()
                                info['研究方向小类'] = parts[1].strip()
                            else:
                                info['研究方向大类'] = research
                        else:
                            info['研究方向大类'] = research
        
        # 清理研究方向中的HTML标签
        for key in ['研究方向大类', '研究方向小类']:
            if info[key]:
                info[key] = re.sub(r'<[^>]+>', '', info[key]).strip()
        
        return info
        
    except Exception as e:
        return {
            '姓名': name,
            '职称': '',
            '研究方向大类': '',
            '研究方向小类': '',
            '邮箱': '',
            '电话': '',
            '错误': str(e)[:100]
        }

# 定义研究方向分类映射
RESEARCH_CATEGORIES = {
    '集成电路与半导体': ['集成电路', '半导体', '芯片', 'VLSI', 'SOC', '微电子', 'MEMS', '传感器', '工艺', '封装', '测试'],
    '通信与网络': ['通信', '5G', '6G', '网络', '无线', '移动通信', '物联网', 'IoT', '卫星通信', '信号处理'],
    '电磁与微波': ['电磁', '微波', '天线', '射频', 'RF', '电磁兼容', '电磁场', '微波电路'],
    '信息处理与人工智能': ['人工智能', 'AI', '机器学习', '深度学习', '信号处理', '图像处理', '语音处理', '模式识别', '计算机视觉'],
    '光电与显示': ['光电', '显示', 'LED', '激光', '光通信', '光电子', '显示技术', 'AR', 'VR'],
    '电子系统与器件': ['嵌入式', 'FPGA', '电路', '电子系统', '智能硬件', '传感器网络', '电源管理'],
    '计算机体系结构': ['计算机体系', '处理器', '架构', 'GPU', '高性能计算', '并行计算'],
    '其他': []
}

def categorize_research(research_text):
    """根据研究方向文本进行分类"""
    if not research_text:
        return '未分类'
    
    research_lower = research_text.lower()
    
    for category, keywords in RESEARCH_CATEGORIES.items():
        if category == '其他':
            continue
        for keyword in keywords:
            if keyword.lower() in research_lower:
                return category
    
    return '其他'

def main():
    print("=" * 60)
    print("浙大导师信息爬取脚本")
    print("=" * 60)
    
    # 解析导师列表
    professors = parse_professors()
    print(f"\n共解析到 {len(professors)} 位导师信息")
    
    # 创建会话
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # 爬取每位导师的详细信息
    detailed_info = []
    total = len(professors)
    
    print(f"\n开始爬取导师个人页面信息...")
    print("-" * 60)
    
    for i, prof in enumerate(professors, 1):
        print(f"[{i}/{total}] 正在获取: {prof['姓名']}", end='')
        
        info = fetch_professor_info(prof['个人页面链接'], prof['姓名'], session)
        
        # 合并信息
        merged = {
            '序号': prof['序号'],
            '姓名': prof['姓名'],
            '学院': prof['学院'],
            '专业学位类别': prof['专业学位类别'],
            '职称': info.get('职称', ''),
            '研究方向大类': info.get('研究方向大类', ''),
            '研究方向小类': info.get('研究方向小类', ''),
            '研究方向分类': categorize_research(info.get('研究方向大类', '') + ' ' + info.get('研究方向小类', '')),
            '邮箱': info.get('邮箱', ''),
            '电话': info.get('电话', ''),
            '个人页面链接': prof['个人页面链接'],
            '错误信息': info.get('错误', '')
        }
        detailed_info.append(merged)
        
        status = "✓" if not info.get('错误') else f"✗ ({info.get('错误', '')[:30]})"
        print(f" {status}")
        
        # 控制请求频率，避免给服务器造成压力
        if i < total:
            time.sleep(random.uniform(0.5, 1.5))
    
    print("-" * 60)
    print(f"信息爬取完成！成功: {sum(1 for d in detailed_info if not d['错误信息'])}, 失败: {sum(1 for d in detailed_info if d['错误信息'])}")
    
    # 创建DataFrame
    df = pd.DataFrame(detailed_info)
    
    # 保存到Excel
    output_path = '/home/admin/.openclaw/workspace/导师信息.xlsx'
    
    # 使用ExcelWriter创建带格式的Excel文件
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 主表 - 全部导师
        df.to_excel(writer, sheet_name='全部导师', index=False)
        
        # 按学院分表
        for college in df['学院'].unique():
            college_df = df[df['学院'] == college]
            sheet_name = college[:10]  # Excel sheet名称限制
            college_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # 按研究方向分类分表
        for category in df['研究方向分类'].unique():
            if category and category != '未分类':
                cat_df = df[df['研究方向分类'] == category]
                sheet_name = category[:10]
                cat_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"\n数据已保存到: {output_path}")
    
    # 生成统计信息
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)
    
    print(f"\n【学院分布】")
    for college, count in df['学院'].value_counts().items():
        print(f"  {college}: {count} 人")
    
    print(f"\n【研究方向分类】")
    for cat, count in df['研究方向分类'].value_counts().items():
        if cat:
            print(f"  {cat}: {count} 人")
    
    print(f"\n【职称分布】")
    title_counts = df['职称'].value_counts()
    for title, count in title_counts.items():
        if title:
            print(f"  {title}: {count} 人")
    
    # 保存统计信息用于报告
    stats = {
        'total': total,
        'success': sum(1 for d in detailed_info if not d['错误信息']),
        'failed': sum(1 for d in detailed_info if d['错误信息']),
        'college_distribution': df['学院'].value_counts().to_dict(),
        'research_categories': df['研究方向分类'].value_counts().to_dict(),
        'title_distribution': df['职称'].value_counts().to_dict(),
    }
    
    return df, stats

if __name__ == '__main__':
    df, stats = main()
    print("\n爬取完成！")