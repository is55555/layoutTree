
class LayoutTree(object):
    def __init__(self, tree, parent=None, depth=0, sibling_order_number=1, depth_limit=25):
        self.x = -1.
        self.y = depth
        self.tree = tree
        self.ancestor = self

        if depth < depth_limit:  # depth limit (never had any problems with this, but I limit it by default because...
            # ... such super-tall trees are not practical to visualise anyway.
            self.children = [LayoutTree(child, self, depth + 1, i + 1, depth_limit=depth_limit)
                             for i, child
                             in enumerate(tree.children)]
        else:
            self.children = []  # already tested: generate trees larger than depth_limit to test behaviour
        self.parent = parent
        self.thread = None
        self.offset_modifier = 0
        self.change = self.shift = 0
        self.sibling_order_number = sibling_order_number
        self._leftmost_sibling = None  # through a descriptor

    def left(self):
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

    def left_brother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

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

def buchheim(tree):
    dt = first_walk(tree)
    second_walk(dt)
    return dt


def first_walk(v, distance=1.):
    if len(v.children) == 0:
        if v.leftmost_sibling:
            v.x = v.left_brother().x + distance
        else:
            v.x = 0.
    else:
        default_ancestor = v.children[0]
        for w in v.children:
            first_walk(w)
            default_ancestor = apportion(w, default_ancestor,
                                         distance)
        execute_shifts(v)

        midpoint = (v.children[0].x + v.children[-1].x) / 2

        w = v.left_brother()
        if w:
            v.x = w.x + distance
            v.offset_modifier = v.x - midpoint
        else:
            v.x = midpoint
    return v


def second_walk(v, m=0, depth=0):
    v.x += m
    v.y = depth

    for w in v.children:
        second_walk(w, m + v.offset_modifier, depth+1)


def apportion(v, default_ancestor, distance):
    w = v.left_brother()
    if w is not None:
        vir = vor = v
        vil = w
        vol = v.leftmost_sibling
        sir = sor = v.offset_modifier
        sil = vil.offset_modifier
        sol = vol.offset_modifier
        while vil.right() and vir.left():
            vil = vil.right()
            vir = vir.left()
            vol = vol.left()
            vor = vor.right()
            vor.ancestor = v
            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                a = ancestor(vil, v, default_ancestor)
                move_subtree(a, v, shift)
                sir = sir + shift
                sor = sor + shift
            sil += vil.offset_modifier
            sir += vir.offset_modifier
            sol += vol.offset_modifier
            sor += vor.offset_modifier
        if vil.right() and not vor.right():
            vor.thread = vil.right()
            vor.offset_modifier += sil - sor
        else:
            if vir.left() and not vol.left():
                vol.thread = vir.left()
                vol.offset_modifier += sir - sol
            default_ancestor = v
    return default_ancestor


def move_subtree(wl, wr, shift):
    subtrees = wr.sibling_order_number - wl.sibling_order_number
    wr.change -= shift / subtrees
    wr.shift += shift
    wl.change += shift / subtrees
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
    if vil.ancestor in v.children:
        return vil.ancestor  # TODO: generate a test where this happens
    else:
        return default_ancestor


