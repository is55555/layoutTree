from __future__ import print_function, unicode_literals, division

import cairo
import math

default_proportions = (1.5, 1.15)
default_node_radius = 25


class Canvas:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.background(1, 1, 1)

    def ctx(self):
        return cairo.Context(self.surface)

    def background(self, r, g, b):
        c = self.ctx()
        c.set_source_rgba(r, g, b, 0)
        c.rectangle(0, 0, self.width, self.height)
        c.fill()
        c.stroke()

    def save(self, filename):
        self.surface.write_to_png(filename)


def line(ctx, x0, y0, x1, y1):
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.stroke()


def dotted_line(ctx, x0, y0, x1, y1, segment=3):
    if x0 == x1:
        theta = math.pi / 2.
    else:
        slope = float(y1 - y0) / float(x1 - x0)
        if x1 - x0 > 0:
            theta = math.atan(slope)
        else:
            theta = math.pi + math.atan(slope)

    dx = math.cos(theta) * segment
    dy = math.sin(theta) * segment
    x_inbounds = x0 < x1
    y_inbounds = y0 < y1

    while x_inbounds == (x0 < x1) and y_inbounds == (y0 < y1):
        line(ctx, x0, y0, x0 + dx, y0 + dy)
        x0, y0 = x0 + 2 * dx, y0 + 2 * dy


def draw_tree_nodes(ctx, node, depth, r, prop):
    width_prop = r * prop[0]
    height_prop = r * prop[1]
    ctx.save()
    ctx.translate(node.x * width_prop + r/2., depth * height_prop + r/2.)
    ctx.scale(r/2., r/2.)
    ctx.arc(0., 0., 1., 0.0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    ctx.stroke()
    for child in node.children:
        draw_tree_nodes(ctx, child, depth + 1, r, prop)


def draw_connections(ctx, node, depth, r, prop):
    width_prop = r * prop[0]
    height_prop = r * prop[1]
    for child in node.children:
        line(ctx, node.x * width_prop + (r / 2), depth * height_prop + (r / 2),
             child.x * width_prop + (r / 2), (depth + 1) * height_prop + (r / 2))
        draw_connections(ctx, child, depth + 1, r, prop)


def draw_threads(ctx, node, depth, r, prop):  # prop: proportions tuple (x, y)
    width_prop = r * prop[0]
    height_prop = r * prop[1]
    for child in node.children:
        c = child.thread
        if c:
            dotted_line(ctx, child.x * width_prop + (r / 2), (depth + 1) * height_prop + (r / 2),
                       c.x * width_prop + (r / 2), (depth + 2) * height_prop + (r / 2))
        draw_threads(ctx, child, depth + 1, r, prop)


def draw(context, tree, node_radius=default_node_radius, proportions=default_proportions,
         p_draw_connections=True, p_draw_threads=True):
    if p_draw_connections:
        draw_connections(context, tree, 0, node_radius, proportions)

    if p_draw_threads:
        draw_threads(context, tree, 0, node_radius, proportions)

    context.fill()
    draw_tree_nodes(context, tree, 0, node_radius, proportions)
