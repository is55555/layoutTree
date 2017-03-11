from __future__ import print_function, unicode_literals, division


class LayoutTree(object):
    def __init__(self, tree, parent=None, depth=0, sibling_order_number=1, depth_limit=25):
        self.x = -1000.
        self.y = depth
        self.tree = tree
        self.ancestor = self

        if depth < depth_limit:  # depth limit (never had any problems with this, but I limit it by default because...
            # ... such super-tall trees are not practical to visualise anyway.
            self.children = [LayoutTree(child, self, depth + 1, sibling_order_number=i + 1, depth_limit=depth_limit)
                             for i, child
                             in enumerate(tree.children)]
        else:
            self.children = []  # already tested: generate trees larger than depth_limit to test behaviour
        self.parent = parent
        self.thread = None
        self.offset_modifier = 0  # "mod" in buchheim
        self.change = self.shift = 0
        self.sibling_order_number = sibling_order_number
        self._leftmost_sibling = None  # through a descriptor

    def __iter__(self):
        return next(self)

    def next(self):
        yield self  # pre-order

        for i in self.children:
            for j in i:
                yield j

    def is_leaf(self):
        return len(self.children) == 0

    def boundaries(self):
        minx = maxx = self.x
        miny = maxy = self.y
        for i in self.children:
            (minx_, maxx_, miny_, maxy_) = i.boundaries_(minx, maxx, miny, maxy)
            minx = min(minx, minx_)
            miny = min(miny, miny_)
            maxx = max(maxx, maxx_)
            maxy = max(maxy, maxy_)
        return (minx, maxx, miny, maxy)

    def boundaries_(self, minx, maxx, miny, maxy):  # returns the boundaries of the tree (to use after rearrangements)
        if self.is_leaf():
            minx = min(minx, self.x)
            miny = min(miny, self.y)
            maxx = max(maxx, self.x)
            maxy = max(maxy, self.y)
        else:
            for i in self.children:
                (minx_, maxx_, miny_, maxy_) = i.boundaries_(minx, maxx, miny, maxy)
                minx = min(minx, minx_)
                miny = min(miny, miny_)
                maxx = max(maxx, maxx_)
                maxy = max(maxy, maxy_)
        return (minx, maxx, miny, maxy)

    def next_left(self):  # as described in Buchheim
        if not self.is_leaf():
            return self.children[0]
        else:
            return self.thread

    def next_right(self):  # as described in Buchheim
        if not self.is_leaf():
            return self.children[-1]
        else:
            return self.thread

    def left_brother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

    def is_leftmost_sibling(self):
        if self.parent:
            if self == self.parent.child[0]:
                return True
        return False

    def get_leftmost_sibling(self):
        if not self._leftmost_sibling and self.parent and self != \
                self.parent.children[0]:
            self._leftmost_sibling = self.parent.children[0]
        return self._leftmost_sibling

    leftmost_sibling = property(get_leftmost_sibling)

    def __repr__(self):
        return "{LayoutTree %s [coords (%s,%s)] [offset=%s]}" % (self.tree, self.x, self.y, self.offset_modifier)


# below, variables follow the convention in Buchheim. Using v for nodes, i for inner, o for outer, l for left,
# and r for right.

distance = 1.  # default horizontal unit distance


def buchheim(tree):  # alters the tree in place (both first_walk(*) and second_walk(*) do)
    first_walk(tree)
    assert tree.offset_modifier == 0
    second_walk(tree, 0 - tree.offset_modifier)
    return tree.boundaries()


def first_walk(v):
    if v.is_leaf():
        if v.leftmost_sibling:
            v.x = v.left_brother().x + distance
        else:
            v.x = 0.
    else:
        default_ancestor = v.children[0]
        for w in v.children:
            first_walk(w)
            default_ancestor = apportion(w, default_ancestor)

        execute_shifts(v)

        midpoint = (v.children[0].x + v.children[-1].x) / 2.

        w = v.left_brother()
        if w:
            v.x = w.x + distance
            # wut = v.leftmost_sibling.x + ((v.sibling_order_number - 1 )* distance)
            # assert v.x >= wut, "should at least be the distance to leftmost_sibling + the x of leftmost_sibling"
            v.offset_modifier = v.x - midpoint
        else:
            v.x = midpoint


def apportion(v, default_ancestor):
    w = v.left_brother()
    if w is not None:
        vir = vor = v
        vil = w
        vol = v.leftmost_sibling
        sir = sor = v.offset_modifier
        sil = vil.offset_modifier
        sol = vol.offset_modifier
        while vil.next_right() and vir.next_left():
            vil = vil.next_right()
            vir = vir.next_left()
            vol = vol.next_left()
            vor = vor.next_right()
            vor.ancestor = v
            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                a = ancestor(vil, v, default_ancestor)
                move_subtree(a, v, shift)
                sir += shift
                sor += shift
            sil += vil.offset_modifier
            sir += vir.offset_modifier
            sol += vol.offset_modifier
            sor += vor.offset_modifier
        if vil.next_right() and not vor.next_right():
            vor.thread = vil.next_right()
            vor.offset_modifier += sil - sor
        else:
            if vir.next_left() and not vol.next_left():
                vol.thread = vir.next_left()
                vol.offset_modifier += sir - sol
            default_ancestor = v
    return default_ancestor


def move_subtree(wl, wr, shift):
    subtrees = wr.sibling_order_number - wl.sibling_order_number
    shift_by_subtrees = float(shift) / subtrees
    wr.change -= shift_by_subtrees
    wl.change += shift_by_subtrees
    wr.shift += shift
    wr.x += shift
    wr.offset_modifier += shift


def execute_shifts(v):
    shift = change = 0
    for w in v.children[::-1]:
        w.x += shift
        w.offset_modifier += shift
        change += w.change
        shift += w.shift + change


def ancestor(vil, v, default_ancestor):
    if vil.ancestor in v.parent.children:
        return vil.ancestor
    else:
        return default_ancestor


def second_walk(v, m=0):
    for w in v.children:
        second_walk(w, m + v.offset_modifier)
    v.x += m

