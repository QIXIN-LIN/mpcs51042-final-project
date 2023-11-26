from collections.abc import MutableMapping


class Node:
    def __init__(self, key, value):
        '''
        Initiate a Node instance with key and value
        '''
        self.key = key
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        '''
        Initiate a LinkedList instance
        '''
        self.head = None
        self.tail = None

    def add(self, key, value):
        '''
        Add one node at the end of this list
        Inputs:
            key: the key of node
            value: the value of node
        '''
        if self.head is None:
            self.head = self.tail = Node(key, value)

        current_node = self.head
        while current_node:
            if current_node.key == key:
                current_node.value = value
                return
            current_node = current_node.next

        self.tail.next = Node(key, value)
        self.tail = self.tail.next

    def remove(self, key):
        '''
        Remove one node with a specific key in this list
        Inputs:
            key: the key of the specific node
        '''
        current_node = self.head
        previous_node = None
        while current_node:
            if current_node.key == key:
                if previous_node:
                    previous_node.next = current_node.next
                else:
                    self.head = current_node.next
                return True
            previous_node = current_node
            current_node = current_node.next
        return False

    def find(self, key):
        '''
        Find one node in the list with a specific key
        Inputs:
            key: the key of the specific node
        Returns:
            the value of the specific node, None if cannot find
        '''
        current_node = self.head
        while current_node:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        '''
        Initiate a Hashtable instance
        '''
        self.capacity = capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self._size = 0
        self._items = [LinkedList() for i in range(capacity)]

    def _hash(self, key):
        """
        This method takes in a string and returns an integer value.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf

        DO NOT CHANGE THIS FUNCTION
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val

    def __setitem__(self, key, val):
        index = self._hash(key) % self.capacity
        if self._items[index].find(key) is None:
            self._size += 1
        self._items[index].add(key, val)

        if (len(self) / self.capacity) > self.load_factor:
            self._resize()

    def _resize(self):
        '''
        Resize the Hashtable and place all nodes based on new capacity
        '''
        new_capacity = self.growth_factor * self.capacity
        new_items = [LinkedList() for i in range(new_capacity)]
        for linked_list in self._items:
            current_node = linked_list.head
            while current_node:
                index = self._hash(current_node.key) % new_capacity
                new_items[index].add(current_node.key, current_node.value)
                current_node = current_node.next

        self.capacity = new_capacity
        self._items = new_items

    def __getitem__(self, key):
        return_value = self._items[self._hash(key) % self.capacity].find(key)
        if return_value is not None:
            return return_value
        else:
            return self.default_value

    def __delitem__(self, key):
        removed = self._items[self._hash(key) % self.capacity].remove(key)
        if removed:
            self._size -= 1
        else:
            raise KeyError(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
