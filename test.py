from __future__ import print_function, unicode_literals, division

from tree import Tree, tree_from_os_dir

import layoutTree
from graph import Canvas, draw
from copy import deepcopy

new_sample_trees = \
    {
    # smallest binary tree
    'binary'    :   Tree("binary_root", [
                        Tree("left"),
                        Tree("right")]),
    # n-ary simple tree (3-ary)
    '3-ary'     :   Tree("3-ary_root", [
                        Tree("left"),
                        Tree("centre"),
                        Tree("right")]),
    # n-ary simple tree (4-ary)
    '4-ary'    :   Tree("4-ary_root", [
                        Tree("leftmost"),
                        Tree("second"),
                        Tree("third"),
                        Tree("fourth"),
                        Tree("rightmost")]),
    # n-ary simple tree (5-ary)
    '5-ary'    :   Tree("5-ary_root", [
                        Tree("leftmost"),
                        Tree("second"),
                        Tree("third"),
                        Tree("fourth"),
                        Tree("rightmost")]),
    # 1-ary
    '1-ary'    :    Tree("1-ary_root", [Tree('one')]),
    # 1-ary-2
    '1-ary-2'  :    Tree("1-ary-2_root", [Tree('one', [Tree('two')])]),
    # 1-ary-5
    '1-ary-5'  :    Tree("1-ary-5_root", [Tree('one', [Tree('two', [Tree('three', [Tree('four')])])])]),
    # binary-to-right
    'bin2right':    Tree("bin2right_root", [Tree('only-left'), Tree('right-binary', [Tree('L'), Tree('R')])]),
    # binary-to-left
    'bin2left' :    Tree("bi2left_root", [Tree('left-binary', [Tree('L'), Tree('R')]), Tree('only-right')]),
    }

new_sample_trees['composite-one'] = deepcopy(new_sample_trees['binary'])
a = deepcopy(new_sample_trees['binary'])
b = deepcopy(a)
new_sample_trees['composite-one'].children[0] = a
new_sample_trees['composite-one'].children[1] = b

new_sample_trees['composite-two-balanced'] = deepcopy(new_sample_trees['4-ary'])
a = deepcopy(new_sample_trees['5-ary'])
b = deepcopy(new_sample_trees['1-ary-5'])
c = deepcopy(new_sample_trees['bin2right'])
d = deepcopy(new_sample_trees['1-ary-2'])
e = deepcopy(new_sample_trees['4-ary'])
new_sample_trees['composite-two-balanced'].children[0] = a
new_sample_trees['composite-two-balanced'].children[1] = b
new_sample_trees['composite-two-balanced'].children[2] = c
new_sample_trees['composite-two-balanced'].children[4] = d
new_sample_trees['composite-two-balanced'].children[4].children[0].children[0] = e

new_sample_trees['composite-three'] = deepcopy(new_sample_trees['composite-two-balanced'])
a = deepcopy(new_sample_trees['bin2right'])
b = deepcopy(new_sample_trees['bin2left'])
c = deepcopy(new_sample_trees['composite-two-balanced'])
d = deepcopy(new_sample_trees['composite-one'])
new_sample_trees['composite-three'].children[0].children[1] = a
new_sample_trees['composite-three'].children[0].children[3] = b
new_sample_trees['composite-three'].children[1].children[0].children[0].children[0] = c
new_sample_trees['composite-three'].children[4].children[0].children[0].children[2] = d

new_sample_trees['composite-four'] = deepcopy(new_sample_trees['composite-three'])
a = deepcopy(new_sample_trees['composite-three'])
b = deepcopy(new_sample_trees['composite-two-balanced'])
new_sample_trees['composite-four'].children[1].children[0].children[0].children[0].children[0].children[1] = a
new_sample_trees['composite-four'].children[4].children[0].children[0].children[2].children[1].children[1] = b

new_sample_trees['composite-five'] = deepcopy(new_sample_trees['composite-four'])
a = deepcopy(new_sample_trees['composite-four'])
b = deepcopy(new_sample_trees['1-ary-5'])
c = deepcopy(new_sample_trees['composite-four'])

new_sample_trees['composite-five'].\
    children[1].children[0].children[0].children[0].children[4].\
    children[0].children[0].children[4] = a
new_sample_trees['composite-five']. \
    children[1].children[0].children[0].children[0].children[4]. \
    children[0].children[0].children[4]. \
    children[1].children[0].children[0].children[0].children[4]. \
    children[0].children[0].children[4] = b
new_sample_trees['composite-five']. \
    children[1].children[0].children[0].children[0].children[4]. \
    children[0].children[0].children[4]. \
    children[1].children[0].children[0].children[0].children[4]. \
    children[0].children[0].children[4]. \
    children[0].children[0].children[0].children[0] = c   # this makes it exceed the maximum depth of 25 - for test
# so not all this tree is rendered, only up to the maximum defined depth (by default, it can be expanded by parameter)

new_sample_trees['alignment-problem'] = \
    Tree("top", [
            Tree("", [
                Tree("", [
                    Tree("", [
                        Tree(""), Tree("")]),
                    Tree("", [
                        Tree("", [
                            Tree("", [
                                Tree("", [
                                    Tree("", [
                                        Tree(""),
                                        Tree("", [
                                            Tree("", [
                                                Tree("", [
                                                    Tree("")])])])])]),
                                Tree("", [Tree("")])]),
                            Tree("", [
                                Tree("", [
                                    Tree(""),
                                    Tree("", [
                                        Tree(""),
                                        Tree("")])])]),
                            Tree("", [
                                Tree("", [
                                    Tree("", [
                                        Tree("", [
                                            Tree("", [
                                                Tree("", [
                                                    Tree(""), Tree("")]),
                                                Tree("")]),
                                            Tree("")])])])])])]), ])])])


def draw_tree(tree, canvasx = 800, canvasy = 600, marginx = 20., marginy = 10., filename="tree.png"):
    algorithm = layoutTree.buchheim
    c = Canvas(canvasx, canvasy)
    context = c.ctx()
    context.translate(marginx, marginy)
    layout_tree = layoutTree.LayoutTree(tree)
    draw(context, algorithm, layout_tree, p_draw_threads=False)
    c.save(filename)


if __name__ == "__main__":
    # example on generating a Tree with a string:
    # t = sample_trees[0]
    # t_s = Tree.recursive_print_string(t)
    # t2 = eval(t_s)

    # this bit generates a tree with the directory structure under the folder /structure_test
    # this is an easy way to create tree structures, simply using your OS interface.
    os_dir = tree_from_os_dir('./structure_test/', p_width_is_name_length=False)
    print(Tree.recursive_print_string(os_dir))
    draw_tree(os_dir, filename="./sample_output/osdir_test_tree.png")

    print(Tree.recursive_print_string(os_dir[1]))
    print(Tree.recursive_print_string(os_dir['c']))  # covers test case for string accessor (only looks at 1st depth)
    print(Tree.recursive_print_string(tree_from_os_dir('')))  # covers a test case for tree_from_os_dir

    print("-----")

    algorithm = layoutTree.buchheim

    for i in new_sample_trees.keys():
        c = Canvas(2200, 800)
        context = c.ctx()
        context.translate(800., 10.)  # leave some margin
        tree_i = new_sample_trees[i]
        layout_tree = layoutTree.LayoutTree(tree_i)
        draw(context, algorithm, layout_tree)
        c.save("./sample_output/saved_new_sample_tree_%s.png" % i)
        print(i, layout_tree, len(tree_i), Tree.recursive_print_string(tree_i))

