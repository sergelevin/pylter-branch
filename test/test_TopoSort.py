# -*- coding: utf-8 -*-

from pylter_branch.TopoSort import TopoSort
import unittest


class TopoSortTest(unittest.TestCase):
    def setUp(self):
        self.graph = TopoSort()

    def test_one_way_dag(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.assertEqual([0, 1, 2, 3], self.graph.sort())

    def test_multi_roots(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(2, 4)
        self.assertIn(self.graph.sort(), ([0, 1, 2, 3, 4], [0, 1, 2, 4, 3]))

    def test_multi_paths(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(3, 4)
        self.assertIn(self.graph.sort(), ([0, 1, 2, 3, 4], [0, 1, 3, 2, 4]))

    def test_cycle(self):
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 1)
        self.assertRaises(RuntimeError, self.graph.sort)

    def test_single_node(self):
        self.graph.add_vertex(0)
        self.assertEqual([0], self.graph.sort())


if __name__ == '__main__':
    unittest.main()
