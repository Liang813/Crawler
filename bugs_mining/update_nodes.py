# -*-coding:GBK -*-
import ast
from collections import Counter
from difflib import unified_diff

import pandas as pd

from bugs_mining.CallCollector import CallCollector
from bugs_mining.Pattern import pattern_match
from bugs_mining.get_update_files_info import read_csv, get_file_content


class ASTVisitor(ast.NodeVisitor):
    """
    ������ȱ���������
    """

    # ������Ҫ��ֻ��"ģ��"�е�һ�����ƣ����Բ��ø���generic_visit���˴�ʹ��generic_visit��ȡȫ���Ľڵ�
    def generic_visit(self, node):
        # �洢���нڵ�
        tree_nodes = [type(node).__name__]
        ast.NodeVisitor.generic_visit(self, node)
        return tree_nodes

        # def visit_FunctionDef(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

        # ���費��ҪLoad�ڵ�
        # def visit_Load(self, node): pass

        # def visit_Load(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    # ��ʾName�ڵ��ʵ������
    def visit_Name(self, node):
        print('Name: ', node.id)


def ast_walk(str1):
    """
    ������ȱ������ڵ㣬Ȼ�󽫽ڵ�洢��һ�������з���
    :param str1:
    :return: nums[]
    """
    # �洢���ڵ�ļ���
    tree_nodes = []
    for node in ast.walk(ast.parse(str1)):
        tree_nodes.append(type(node).__name__)
    # print(tree_nodes)
    return tree_nodes


def get_node_number(node_list):
    """
    ʹ��python collections�Դ���Counter��������ÿ���ڵ���ֵĴ���
    :param node_list:
    :return: node_tuple
    """
    cnt = Counter()
    for word in node_list:
        cnt[word] += 1
    node_tuple = cnt
    # print(node_tuple)
    return node_tuple


def two_ast_nodes():
    """

    :return: fixǰ���﷨���ڵ�Ĳ�ֵ
    """
    node_number_list = []
    two_file_content = get_file_content()
    for info in two_file_content:
        # ��ȡ����commit��Ӧ���޸ĵ��ļ�����
        str_pre = info[2]
        str_now = info[3]
        # �������ݹ����﷨��
        str_pre_tree = ast.dump(ast.parse(str_pre))
        str_now_tree = ast.dump(ast.parse(str_now))

        # �ֱ���ù�����ȱ�������Ȼ��ֱ��ȡ�ڵ�ֵ
        node_list_pre = ast_walk(str_pre_tree)
        node_list_now = ast_walk(str_now_tree)
        # ��ȡ�����ڵ�����
        node_tuple_pre = get_node_number(node_list_pre)
        print(node_tuple_pre)
        node_tuple_now = get_node_number(node_list_now)
        print(node_tuple_now)
        # �������Ľڵ�����
        node_tuple_now.subtract(node_tuple_pre)
        print(node_tuple_now)
        node_number_list.append(node_tuple_now)
    return node_number_list


def diff_two_ast():
    """
        ��ȡfixǰ�������﷨��str����Ĳ��죬�����û��ڹ���ƥ�亯���ж� Bug �����
    :return: List[List[Union[str, List[str]]]]
    """
    repo_info_list = read_csv()
    general_bugs = []
    for repo_info in repo_info_list:
        # �ֱ��ȡrepo������commitId
        repo_name = repo_info[0]
        repo_name_str = ''.join(repo_name)  # repo��
        fix_commit = repo_info[1]
        print(fix_commit)  # ������fix_commitΪ��
        fix_commit_str = ''.join(fix_commit)  # fix commitId
        commit_url = repo_info[2]
        commit_url_str = ''.join(commit_url)  # fix commit url
        two_file_content = get_file_content(repo_name_str, fix_commit_str, commit_url_str)
        # ��ȡ����commit��Ӧ���޸ĵ��ļ�����
        str_pre = two_file_content[2]
        str_now = two_file_content[3]
        # �������ݹ����﷨��
        str_pre_tree = ""
        str_now_tree = ""
        try:
            str_pre_tree = ast.dump(ast.parse(str_pre))
            str_now_tree = ast.dump(ast.parse(str_now))
        except Exception as e:
            print(e)
        # ���������﷨�����ַ������첢��ȡ����
        diff = unified_diff(str_pre_tree, str_now_tree, lineterm='', )
        diff_buggy = ""
        diff_fix = ""
        for i in diff:
            if len(i) <= 2:
                if i.startswith("-"):
                    a = i.replace("-", "")
                    diff_buggy += a
                elif i.startswith("+"):
                    a = i.replace("+", "")
                    diff_fix += a
                else:
                    a = i.replace(" ", "")
                    diff_buggy += a
                    diff_fix += a
        print(two_file_content[0])
        # try:
        #     print(diff_buggy)
        #     print(len(diff_buggy))
        #     print(diff_fix)
        #     print(len(diff_fix))
        #     print(len(diff_fix) / len(diff_buggy))
        # except Exception as e:
        #     print("�����񲻷���")
        # ���ù���ƥ�䷽�����������diff_buggy��diff_fix�����ڹ����ƥ��
        if len(diff_buggy) != 0:
            # if len(diff_fix) < 0.0172 or len(diff_fix) > 785:   �׳�31��Bug��׼ȷ�ʴ�93.55%
            if (len(diff_fix) / len(diff_buggy)) < 0.0172 or (len(diff_fix) / len(diff_buggy)) > 785:
                continue
        try:
            buggy_types = pattern_match(diff_buggy, diff_fix, str_pre_tree, str_pre, str_now)
            repo_name = two_file_content[0]
            commit_url = commit_url_str
            if len(buggy_types) >= 3:
                del buggy_types[1: len(buggy_types)]
            general_bug = [repo_name, commit_url, buggy_types]
            general_bugs.append(general_bug)
        except Exception as e:
            print("����ƥ�����")
            continue
    return general_bugs


if __name__ == '__main__':
    general_bugs = diff_two_ast()
    for general_bug in general_bugs:
        if len(general_bug[2]) != 0:
            print(general_bug)
            # ��API misuse���Bug�����csv�ļ���
            bug_type = general_bug[2]
            if 'API' in bug_type[0]:
                # ���������csv��
                fileName = 'API_misuse' + '.csv'
                api_info = [general_bug[1], bug_type[0]]
                data = [api_info]
                df = pd.DataFrame(data)
                try:
                    df.to_csv(fileName, header=False, index=False,
                                mode='a+', encoding='utf-8-sig')

                except UnicodeEncodeError:
                    print('Encode error drop the data')

    print("Bug����Ϊ:")
    print(len(general_bugs))
