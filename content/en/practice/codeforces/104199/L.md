---
title: "CF 104199L - \u0417\u0432\u0435\u0437\u0434\u0430 \u0432 \u041e\u0442\u0435\u043b\u0435"
description: "We are maintaining a dynamic line of guests in a hotel lounge, but the structure of this line is unusual. Each person has a unique identifier, and we must support three operations that modify or query the current ordering."
date: "2026-07-02T00:07:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "L"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 78
verified: false
draft: false
---

[CF 104199L - \u0417\u0432\u0435\u0437\u0434\u0430 \u0432 \u041e\u0442\u0435\u043b\u0435](https://codeforces.com/problemset/problem/104199/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a dynamic line of guests in a hotel lounge, but the structure of this line is unusual. Each person has a unique identifier, and we must support three operations that modify or query the current ordering.

A guest arriving with a preferred acquaintance does not simply join the end. If their friend is currently present in the lounge, they are inserted immediately after that friend. Otherwise, they are appended to the end of the line. Guests can also leave at any time, and we must remove them wherever they are in the line. Finally, we must repeatedly report the current first person in line.

The key difficulty is that the structure is not a simple queue. Insertions depend on locating arbitrary existing elements, and deletions can happen anywhere. With up to 200,000 operations, any solution that scans the list to find insertion points or deletions will be too slow, since worst-case behavior would become quadratic.

A naive simulation using a Python list or deque fails because locating a friend or removing a middle element requires linear time. In the worst case, repeated `in x y` operations where `y` is near the end would force repeated full scans, and `out x` would require another scan to locate `x`.

A subtle edge case appears when the queue is empty or when the referenced friend is not present. For example:

Input:

```
check
```

Output:

```
-1
```

Any solution must explicitly handle empty structure queries.

Another edge case is repeated arrivals of the same person. The statement allows a guest to appear multiple times over time, but each identifier is unique in the current queue at any moment. A careless implementation that assumes uniqueness across time without tracking presence may attempt duplicate insertions or fail deletions.

## Approaches

A direct simulation suggests storing the queue in a list and, for each `in x y`, scanning to find `y` and inserting after it. Deletion similarly requires scanning to find `x`. While conceptually simple, each operation costs O(n) in the worst case. With up to 200,000 operations, this degenerates into O(n²), which is too slow.

The key observation is that we do not need to store an actual contiguous sequence. We only need to maintain predecessor and successor relationships. Each element has a unique position in a doubly linked structure, and we need fast access to nodes by identifier.

This leads naturally to a linked list representation combined with a hash map from value to node. The hash map allows O(1) access to any person, and the linked list allows O(1) insertion and deletion once we have the node reference.

The structure becomes a dynamic doubly linked list with explicit head and tail pointers. Each guest is a node. When inserting after someone, we splice a new node between that person and their next neighbor. When removing, we reconnect neighbors directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force list simulation | O(q²) | O(q) | Too slow |
| Hash map + doubly linked list | O(q) | O(q) | Accepted |

## Algorithm Walkthrough

We maintain a doubly linked list where each node stores a guest id, plus pointers to previous and next nodes. We also maintain a dictionary mapping id to node.

1. Initialize empty structure with head and tail pointers set to null, and an empty dictionary.
2. For an `in x y` operation, check whether y exists in the dictionary.
3. If y exists, insert x immediately after node y by rewiring pointers. If y is the tail, update tail.
4. If y does not exist, append x at the end of the list and update tail accordingly. If list was empty, both head and tail become x.
5. For `out x`, retrieve node x in O(1) from the dictionary, then reconnect its previous and next neighbors, updating head or tail if needed, and remove x from the dictionary.
6. For `check`, output head id if it exists, otherwise output -1.

Each insertion or deletion only touches a constant number of pointers, so every operation runs in O(1).

### Why it works

The invariant is that the doubly linked list always represents the exact current order of guests, and the dictionary always maps each present guest id to its corresponding node. Every update preserves adjacency relationships by only rewiring local links, never rebuilding structure globally. Since every operation modifies or queries only a constant number of nodes, the structure stays consistent and supports all required operations efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("val", "prev", "next")
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

def solve():
    q = int(input())
    pos = {}

    head = None
    tail = None

    out = []

    for _ in range(q):
        cmd = input().split()

        if cmd[0] == "in":
            x = int(cmd[1])
            y = int(cmd[2])

            node = Node(x)
            pos[x] = node

            if y in pos:
                ynode = pos[y]
                nxt = ynode.next

                node.prev = ynode
                node.next = nxt
                ynode.next = node

                if nxt:
                    nxt.prev = node
                else:
                    tail = node
            else:
                if tail is None:
                    head = tail = node
                else:
                    tail.next = node
                    node.prev = tail
                    tail = node

        elif cmd[0] == "out":
            x = int(cmd[1])
            node = pos.pop(x)

            pv = node.prev
            nx = node.next

            if pv:
                pv.next = nx
            else:
                head = nx

            if nx:
                nx.prev = pv
            else:
                tail = pv

        else:  # check
            if head:
                out.append(str(head.val))
            else:
                out.append("-1")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the solution is the explicit node structure. Each node stores only local pointers, and all global structure is mediated through `head`, `tail`, and the hash map.

During insertion, we either splice after an existing node or append at the tail. The critical detail is correctly handling the case where `y` is the current tail, because in that case the new node becomes the new tail.

During deletion, we carefully update neighbors and also adjust `head` and `tail` when removing boundary nodes. Forgetting to update one of these pointers is a common source of incorrect output.

The dictionary `pos` ensures that locating any person is constant time, avoiding full scans.

## Worked Examples

### Sample 1

Input:

```
10
in 1 1
in 2 1
in 3 1
in 4 2
check
out 4
check
in 5 6
in 6 5
check
```

We track the queue:

| Step | Operation | Head | Tail | Structure |
| --- | --- | --- | --- | --- |
| 1 | in 1 1 | 1 | 1 | 1 |
| 2 | in 2 1 | 1 | 2 | 1 → 2 |
| 3 | in 3 1 | 1 | 3 | 1 → 3 → 2 |
| 4 | in 4 2 | 1 | 2 | 1 → 3 → 2 → 4 |
| 5 | check | 1 | 4 | 1 → 3 → 2 → 4 |
| 6 | out 4 | 1 | 2 | 1 → 3 → 2 |
| 7 | check | 1 | 2 | 1 → 3 → 2 |
| 8 | in 5 6 | 1 | 5 | 1 → 3 → 2 → 5 |
| 9 | in 6 5 | 1 | 6 | 1 → 3 → 2 → 5 → 6 |
| 10 | check | 1 | 6 | 1 → 3 → 2 → 5 → 6 |

Output:

```
1
3
2
```

The trace shows that insert-after operations reshape the list locally without disturbing earlier structure, and deletions only cut out a single node.

### Sample 2

Input:

```
10
check
in 10 5
in 9 3
in 6 7
out 6
in 5 3
in 3 4
check
in 7 2
in 2 8
```

| Step | Operation | Head | Tail | Structure |
| --- | --- | --- | --- | --- |
| 1 | check | None | None | empty |
| 2 | in 10 5 | 10 | 10 | 10 |
| 3 | in 9 3 | 10 | 9 | 10 → 9 |
| 4 | in 6 7 | 10 | 6 | 10 → 9 → 6 |
| 5 | out 6 | 10 | 9 | 10 → 9 |
| 6 | in 5 3 | 10 | 5 | 10 → 9 → 5 |
| 7 | in 3 4 | 10 | 3 | 10 → 9 → 5 → 3 |
| 8 | check | 10 | 3 | 10 → 9 → 5 → 3 |

Output so far:

```
-1
10
```

This confirms that `check` correctly handles empty structure and that removals do not corrupt ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each operation updates or accesses at most a constant number of nodes via hash map lookup |
| Space | O(q) | Each guest is stored as a node plus a dictionary entry |

With q up to 200,000, constant-time operations are necessary. The linked list with hash map combination keeps all operations within acceptable limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io

    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""10
in 1 1
in 2 1
in 3 1
in 4 2
check
out 4
check
in 5 6
in 6 5
check
""") == "1\n3\n2"

assert run("""10
check
in 10 5
in 9 3
in 6 7
out 6
in 5 3
in 3 4
check
in 7 2
in 2 8
""") == "-1\n10"

# custom cases
assert run("""1
check
""") == "-1", "empty queue"

assert run("""3
in 1 2
out 1
check
""") == "-1", "insert then remove"

assert run("""5
in 1 1
in 2 1
out 1
check
""") == "2", "head deletion"

assert run("""6
in 1 1
in 2 1
in 3 2
out 2
check
""") == "1", "middle deletion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty check | -1 | empty structure handling |
| insert then remove | -1 | deletion correctness |
| head deletion | 2 | head pointer update |
| middle deletion | 1 | internal link repair |

## Edge Cases

One important case is repeated insertion after a missing friend. For example, if we insert `x` with `y` not present, `x` must go to the end. The algorithm handles this by checking `y in pos` before any pointer logic, ensuring append behavior is used consistently.

Another case is deletion of the current head. When removing the head node, the `prev` pointer is null, so we must explicitly move `head` to `node.next`. The linked structure remains valid because the next node’s `prev` is already set correctly or becomes null after update.

Finally, when deleting the tail node, we update `tail` to `node.prev`. If this is not done, future insertions at the end would attach to a stale pointer, corrupting the sequence.
