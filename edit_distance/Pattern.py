def pattern_match(str1, str2):
    buggy_type = ""
    buggy_count = str1.count('keyword')
    fix_count = str2.count('keyword')
    # ���ж�û�д�Ľڵ������棬�д�ڵ�Ļ��кܴ���������commit�ύ�˺ܶ���룬����������µķ���  Name�����ڵ�
    big_node = ["Call", ""]
    """
        Important!!!
    """
    # if ��ڵ� not in str1 and str2
    if buggy_count != fix_count or ('keyword' not in str1 and 'keyword' in str2):
        buggy_type = 'API misuse'
        return buggy_type
    if 'keyword' in str1 and 'keyword' in str2:
        location_buggy = str1.find('keyword')
        location_fix = str2.find('keyword')
        if location_buggy == location_fix:
            buggy_type = 'API misuse'
            return buggy_type
