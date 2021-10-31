# -*- coding: gbk -*-
import ast
# from collections import Counter

# c = Counter(a=4, b=2, c=0, d=-2)
# d = Counter(a=3, c=2, b=-2)
# c.subtract(d)
# print(c)
from collections import Counter

import astpretty


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


if __name__ == '__main__':
    # fixǰ
    str1 = "d.setdefault(10, []).append(5), p.set(1,2)"
    # fix��
    str2 = "all_toks = all_toks + (list(attr_value) if isinstance(attr_value, (list, tuple)) else [attr_value])"
    # ��ʾԭ��
    print(ast.parse(str1))
    str1_tree = ast.dump(ast.parse(str1))
    print(str1_tree)
    # str2_tree = ast.dump(ast.parse(str2))
    # # ast���ɵ���ͨ��������ʽ
    # print(str1_tree)
    # print(str2_tree)
    # # �ֱ���ù����������
    # node_list_pre = ast_walk(str1_tree)
    # node_list_now = ast_walk(str2_tree)
    # # ��ȡ�����ڵ�����
    # node_tuple_pre = get_node_number(node_list_pre)
    # print(node_tuple_pre)
    # node_tuple_now = get_node_number(node_list_now)
    # print(node_tuple_now)
    # # �������Ľڵ�����
    # node_tuple_now.subtract(node_tuple_pre)
    # print("���Ľڵ�����")
    # print(node_tuple_now)

    # ʹ��astpretty���ߣ����õ���ʾAST�ṹ
    # astpretty.pprint(ast.parse(str1))

    # ʹ�ù�����ȱ���������Ϊÿ���ڵ�����һ��parent���ԣ�����Ѱ�ҽڵ�ĸ��ڵ�
    # for node in ast.walk(ast.parse(str1)):
    #     for child in ast.iter_child_nodes(node):
    #         print(ast.dump(child))
    #         child.parent = node
