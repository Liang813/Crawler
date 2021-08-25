import ast
from collections import Counter
from difflib import unified_diff
# import astpretty
from edit_distance.Pattern import pattern_match
from edit_distance.get_update_files_info import get_file_content


class ASTVisitor(ast.NodeVisitor):
    """
    深度优先遍历树函数
    """
    # 若是想要的只是"模块"中的一组名称，可以不用覆盖generic_visit，此处使用generic_visit获取全部的节点
    def generic_visit(self, node):
        # 存储所有节点
        tree_nodes = [type(node).__name__]
        ast.NodeVisitor.generic_visit(self, node)
        return tree_nodes

    # def visit_FunctionDef(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    # 假设不需要Load节点
    # def visit_Load(self, node): pass

    # def visit_Load(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    # 显示Name节点的实际名称
    def visit_Name(self, node):
        print('Name: ', node.id)


def ast_walk(str1):
    """
    广度优先遍历树节点，然后将节点存储到一个数组中返回
    :param str1:
    :return: nums[]
    """
    # 存储树节点的集合
    tree_nodes = []
    for node in ast.walk(ast.parse(str1)):
        tree_nodes.append(type(node).__name__)
    # print(tree_nodes)
    return tree_nodes


def get_node_number(node_list):
    """
    使用python collections自带的Counter函数计算每个节点出现的次数
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

    :return: fix前后语法树节点的差值
    """
    node_number_list = []
    two_file_content = get_file_content()
    for info in two_file_content:
        # 获取两个commit对应的修改的文件内容
        str_pre = info[2]
        str_now = info[3]
        # 根据内容构建语法树
        str_pre_tree = ast.dump(ast.parse(str_pre))
        str_now_tree = ast.dump(ast.parse(str_now))

        # 分别调用广度优先遍历树，然后分别获取节点值
        node_list_pre = ast_walk(str_pre_tree)
        node_list_now = ast_walk(str_now_tree)
        # 获取各个节点数量
        node_tuple_pre = get_node_number(node_list_pre)
        print(node_tuple_pre)
        node_tuple_now = get_node_number(node_list_now)
        print(node_tuple_now)
        # 计算相差的节点数量
        node_tuple_now.subtract(node_tuple_pre)
        print(node_tuple_now)
        node_number_list.append(node_tuple_now)
    return node_number_list


def diff_two_ast():
    """
        fix前后两颗语法树str级别的差异
    :return:
    """
    node_number_list = []
    two_file_content = get_file_content()
    for info in two_file_content:
        # 获取两个commit对应的修改的文件内容
        str_pre = info[2]
        str_now = info[3]
        # 根据内容构建语法树
        str_pre_tree = ast.dump(ast.parse(str_pre))
        str_now_tree = ast.dump(ast.parse(str_now))
        # 计算两颗语法树的字符串差异并获取差异
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
        # print(diff_buggy)
        # print(diff_fix)
        # 调用规则匹配方法，传入参数diff_buggy与diff_fix，基于规则的匹配
        buggy_type = pattern_match(diff_buggy, diff_fix)
        if buggy_type == 'API misuse':
            print("True!")


if __name__ == '__main__':
    # node_numbers = get_two_ast()
    diff_two_ast()

