
"""Queue Object: First In, First Out (FIFO)."""

class Queue:
    def __init__(self, items=None):
        self.items = list(items or [])

    def enqueue(self, value):
        # Add a value to the rear of the queue.
        self.items.append(value)

    def dequeue(self):
        # Remove the front item (first item).
        return self.items.pop(0) if self.items else None

    def peek(self):
        # Return the front item without removing it.
        return self.items[0] if self.items else None

    def is_empty(self):
        return not self.items

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()
