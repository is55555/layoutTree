from __future__ import print_function, unicode_literals, division
import sys, os

if sys.version_info < (3,):  # pragma: no cover
    integer_types = (int, long,)
    from itertools import imap
    from builtins import range as range3  # requires package future in Python2 (unfortunate, but there's no better way)
else:  # pragma: no cover
    integer_types = (int,)
    imap = map
    range3 = range
    unicode = str


class Tree(object):
    def __init__(self, node_name=None, children_=None, p_width_is_name_length=True):
        if children_ is None:
            children_ = []
        self.children = children_

        self.node_name = node_name

        if p_width_is_name_length:
            self.width = len(node_name)
        else:
            self.width = 1

    def __str__(self):
        # return "<{%s}(%s)>[%d]" % (self.node, str(self.children), len(self.children)) # print direct children
        return "<name:{%s}>[direct children:%d]" % (self.node_name, len(self.children)) # without printing direct children

    def __repr__(self):
        return "Tree('%s')" % (self.node_name)

    @staticmethod
    def recursive_print_string(tree_, s="", depth_limit=50):
        if tree_.children:
            s += "Tree('%s', [" % tree_.node_name
            for i in tree_.children:
                s += Tree.recursive_print_string(i) + ", "
            s += "])"
        else:
            s += tree_.__repr__()  # "Tree('%s')" % tree_.node_name
        return s

    def __getitem__(self, key):  # tested
        if isinstance(key, int):
            return self.children[key]

        if isinstance(key, unicode):  # unicode defined in the compatibility part at the top, for Py3
            for i in self.children:
                if i.node_name == key:
                    return i

    # def __iter__(self):  # I commented this out because it's not a useful iterator. Maybe provide pre/post-order later
    #     return self.children.__iter__()

    def __len__(self, max_depth=25):  # recursive breadth-first procedure (counts all nodes in the tree)
        adder = 1  # count the node itself
        if max_depth <= 0:  # tested behaviour when the depth limit is reached
            return adder

        for i in self.children:
            adder += i.__len__(max_depth=max_depth-1)  # recursive call

        return adder


def tree_from_os_dir(path, ignore_list=('.DS_Store',), p_width_is_name_length = True):
    basename_ = os.path.basename(path)
    if not basename_:
        basename_ = "./"

    node = Tree(basename_, p_width_is_name_length = p_width_is_name_length)
    if os.path.isdir(path):
        for f in os.listdir(path):
            if f in ignore_list:
                continue
            next_path = os.path.join(path, f)
            new_node = tree_from_os_dir(next_path, p_width_is_name_length = p_width_is_name_length)
            node.children.append(new_node)
    return node

