# Tree Traversals


```c
preorder  |  root -> left  -> right
inorder   |  left -> root  -> right
postorder |  left -> right -> root
```

## Traversals

```python
class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def pre_order(tree):
    if not tree:
        return
    print tree.value, '->',
    pre_order(tree.left)
    pre_order(tree.right)


def in_order(tree):
    if not tree:
        return None
    in_order(tree.left)
    print tree.value, '->',
    in_order(tree.right)


def post_order(tree):
    if not tree:
        return None
    post_order(tree.left)
    post_order(tree.right)
    print tree.value, '->',



nodes = {}
for char in 'abcdefghijklmnopqrstuvwxyz':
    nodes[char] = Node(char)

nodes['a'].left = nodes['b']
nodes['a'].right = nodes['c']
nodes['b'].left = nodes['d']
nodes['b'].right = nodes['e']
nodes['c'].left = nodes['f']
nodes['c'].right = nodes['g']
nodes['d'].left = nodes['h']
nodes['d'].right = nodes['i']
nodes['e'].left = nodes['j']
nodes['e'].right = nodes['k']
nodes['f'].left = nodes['l']
nodes['f'].right = nodes['m']
nodes['g'].left = nodes['n']
nodes['g'].right = nodes['o']


pre_order(nodes['a'])
print
in_order(nodes['a'])
print
post_order(nodes['a'])

# a -> b -> d -> h -> i -> e -> j -> k -> c -> f -> l -> m -> g -> n -> o ->
# h -> d -> i -> b -> j -> e -> k -> a -> l -> f -> m -> c -> n -> g -> o ->
# h -> i -> d -> j -> k -> e -> b -> l -> m -> f -> n -> o -> g -> c -> a ->

```

## get tree from preorder and inorder

```python
def build_tree(inorder, preorder):
    """
    :type preorder: List[int]
    :type inorder: List[int]
    :rtype: Node
    """
    if inorder:
        root = Node(preorder.pop(0))
        inorder_index = inorder.index(root.val)
        root.left = build_tree(preorder, inorder[:inorder_index])
        root.right = build_tree(preorder, inorder[inorder_index+1:])
        return root
```

## get tree from inorder and postorder
```python
def build_tree(inorder, postorder):
    """
    :type inorder: List[int]
    :type postorder: List[int]
    :rtype: Node
    """
    if inorder and postorder:
        root = Node(postorder.pop())
        inorder_index = inorder.index(root.val)
        root.right = build_tree(inorder[inorder_index + 1:], postorder)
        root.left = build_tree(inorder[:inorder_index], postorder)
        return root
```

> **Refer:**

> [1].http://interactivepython.org/courselib/static/pythonds/Trees/TreeTraversals.html

> [2].https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

> [3].https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
