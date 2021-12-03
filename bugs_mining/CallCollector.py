# -*-coding:GBK -*-
import ast

"""
    �����﷨���е�api�����Ӧ�Ĳ���
"""


class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self._current = []
        self.args = []
        self.api_dict = dict()
        self._in_call = False

    # args��Call���¼�
    def visit_Call(self, node):
        self._current = []
        self._in_call = True
        args = []
        for i in node.args:
            args.append(ast.dump(i))
        if self._in_call:
            self.args.append(args)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if self._in_call:
            self._current.append(node.attr)  # node.attr = append �� setdefault  ��Call�е�attr
        self.generic_visit(node)

    def visit_Name(self, node):
        if self._in_call:
            self._current.append(node.id)  # node.id = d  ��Call�е�id
            # �ж�node.id�Ƿ���tf��torch��F��np�ȣ����ǵĻ��ټ��������Ĳ���
            repo_name = ['tf', 'torch', 'np', 'F', 'sess']
            if node.id in repo_name or node.id is None:
                self.calls.append('.'.join(self._current[::-1]))
                # ȡ��call�к�args�����µ�Ԫ�أ���ϳ�dict
                key = self.calls[-1]
                value = self.args[-1]
                self.api_dict[key] = value
            # Reset the state
            self._current = []
            self._in_call = False
        self.generic_visit(node)


# Test
# if __name__ == '__main__':
#     a = "d.setdefault(10, []).append(5), aet(1,2), tf.mean(list(lyk))"
#     tree = ast.parse(a)
#     print(ast.dump(tree))
#     cc = CallCollector()
#     cc.visit(tree)
#     print(cc.api_dict)

