# -*-coding:GBK -*-
import ast
from collections import Counter
from difflib import unified_diff
from edit_distance.Pattern import pattern_match
from edit_distance.get_update_files_info import get_file_content


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
    :return:
    """
    node_number_list = []
    general_bugs = []
    two_file_content = get_file_content()
    for info in two_file_content:
        # ��ȡ����commit��Ӧ���޸ĵ��ļ�����
        str_pre = info[2]
        str_now = info[3]
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
        print(info[0])
        try:
            print(diff_buggy)
            print(diff_fix)
        except Exception as e:
            print("�����񲻷���")
        # ���ù���ƥ�䷽�����������diff_buggy��diff_fix�����ڹ����ƥ��
        buggy_types = pattern_match(diff_buggy, diff_fix, str_pre_tree)
        repo_name = info[0]
        commit_url = info[4]
        general_bug = [repo_name, commit_url, buggy_types]
        general_bugs.append(general_bug)
    return general_bugs


if __name__ == '__main__':
    # node_numbers = get_two_ast()
    general_bugs = diff_two_ast()
    # print(general_bugs)
    for general_bug in general_bugs:
        if len(general_bug[2]) != 0:
            print(general_bug)
    print("Bug����Ϊ:")
    print(len(general_bugs))
