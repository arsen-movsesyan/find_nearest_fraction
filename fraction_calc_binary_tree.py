class BFNode:

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.right_child = None
        self.left_child = None

    def format_result(self):
        return f"{self.data['numerator']} / {self.data['denominator']}"


class BinaryFractionBTree:

    def __init__(self, height):
        self.root = None
        self.height = height
        self._populate()

    def insert(self, data):
        if self.root is None:
            self.root = BFNode(data, None)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, node):
        if data['value'] > node.data['value']:
            if node.left_child:
                self._insert_node(data, node.left_child)
            else:
                node.left_child = BFNode(data, node)
        elif data['value'] < node.data['value']:
            if node.right_child:
                self._insert_node(data, node.right_child)
            else:
                node.right_child = BFNode(data, node)

    def traverse(self):
        if self.root:
            self._traverse_in_order(self.root)
        else:
            print("BTre is empty")

    def _traverse_in_order(self, node):
        if node.left_child:
            self._traverse_in_order(node.left_child)
        print(node.data)

        if node.right_child:
            self._traverse_in_order(node.right_child)

    def _populate(self):
        level = 1
        denominator = 2
        while level <= self.height:
            numerator = 1
            while numerator < denominator:
                data = {
                    "numerator": numerator,
                    "denominator": denominator,
                    "value": numerator / denominator
                }
                self.insert(data)
                # print(data, level)
                numerator += 2
            level += 1
            denominator = 2 ** level

    def find_nearest(self, num):
        if num < self.root.data['value']:
            return self._find_traverse(num, self.root.right_child)
        elif num > self.root.data['value']:
            return self._find_traverse(num, self.root.left_child)
        else:
            return self.root.format_result()

    def _find_traverse(self, num, node):
        if node.data['value'] > num:
            if node.right_child:
                return self._find_traverse(num, node.right_child)
        elif node.data['value'] < num:
            if node.left_child:
                return self._find_traverse(num, node.left_child)
        return node.format_result()


def find_nearest_fraction(num, precision_level=5):
    if isinstance(num, int):
        return num
    if num.is_integer():
        return int(num)
    whole = int(num)
    frac_str = str(num).split('.')[1]
    decimal_factor = 10 ** len(frac_str)
    fraction = int(frac_str)
    ff = BinaryFractionBTree(precision_level)
    nearest = ff.find_nearest(fraction / decimal_factor)
    return f"{whole} {nearest}"


print(find_nearest_fraction(17.29))
