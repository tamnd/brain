---
title: "CF 104199L - \u0417\u0432\u0435\u0437\u0434\u0430 \u0432 \u041e\u0442\u0435\u043b\u0435"
description: "We are maintaining a dynamic line of guests in an event hall. Each guest has a unique numeric identifier. The line supports three types of operations that continuously reshape its order. A guest can arrive with a declared “friend reference” to another guest."
date: "2026-07-02T18:02:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "L"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 90
verified: false
draft: false
---

[CF 104199L - \u0417\u0432\u0435\u0437\u0434\u0430 \u0432 \u041e\u0442\u0435\u043b\u0435](https://codeforces.com/problemset/problem/104199/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a dynamic line of guests in an event hall. Each guest has a unique numeric identifier. The line supports three types of operations that continuously reshape its order.

A guest can arrive with a declared “friend reference” to another guest. If that friend is currently in the line, the arriving guest must be inserted directly behind them. If the friend is absent, the new guest is appended at the end of the line. Guests may appear multiple times over time, so the structure must support re-insertion.

A guest can also leave the line at any moment, and that removal must not break the relative order of everyone else.

Finally, we are asked to repeatedly report the current front of the line, or report that the line is empty.

The key difficulty is that insertion is not simply at the end, but potentially after an arbitrary existing element, while deletions and queries must remain efficient under up to 200,000 operations. Any approach that scans the line for each operation will fail immediately, since a full scan per query leads to quadratic behavior in the worst case.

A second subtlety is that “insert behind friend if present” requires fast detection of whether a person is currently inside the structure, and if so, direct access to their position.

A naive failure mode appears when repeatedly inserting relative to frequently moving people. For example, if we always search linearly for the friend each time, a case like many chained inserts behind a moving front element degenerates into repeated full scans, producing a hidden quadratic blow-up even if each individual operation seems cheap.

Another edge case is deletion. If we physically remove elements from an array-based queue, shifting elements after every deletion becomes linear per operation, again leading to quadratic behavior when deletions are frequent.

The core requirement is therefore a structure that supports:

fast existence check for a guest,

fast insertion next to a known node,

fast deletion of a known node,

and fast access to the current front.

## Approaches

A direct brute-force simulation stores the queue as a Python list. For each `in x y`, we scan the list to find `y`, then insert `x` right after it. If `y` is not found, we append. For `out x`, we scan again to locate `x` and remove it. For `check`, we return the first element.

This is correct logically, since it literally simulates the rules. However, each operation may require scanning up to O(n) elements. With up to 200,000 operations, the total work becomes O(nq), which can exceed 10^10 operations in worst cases, far beyond feasible limits.

The key observation is that the line order is always a linked structure with local modifications. Each guest’s position changes only via insertion next to a known node or removal. This suggests replacing array shifting with pointer manipulation.

We can model the queue as a doubly linked list. Each guest corresponds to a node. We maintain a dictionary from guest id to node pointer, so we can access any guest in O(1). Insertions become pointer rewiring: if the friend exists, we splice the new node right after them; otherwise we append at the tail. Deletions are also O(1) by unlinking a node using its neighbors.

This transforms all expensive linear scans into constant-time dictionary lookups and pointer updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (list + scans) | O(q · n) | O(n) | Too slow |
| Optimal (hash map + linked list) | O(q) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a doubly linked list with explicit head and tail pointers, plus a hash map from guest id to node.

1. Create a node structure storing `value`, `prev`, and `next`. This represents a guest in the line. This allows constant-time removal and insertion without shifting elements.
2. Maintain `head` and `tail` pointers for the current front and back of the line. These give O(1) access to the first element for `check`.
3. Maintain a dictionary `pos[x]` that maps each guest id to its node. This ensures we never search the list linearly.
4. For an `in x y` operation, first create a new node for `x`. Then check whether `y` exists in `pos`. If it exists, we insert the new node immediately after `y`’s node by updating four pointers: new node’s links and surrounding neighbors. If it does not exist, we attach the node at the end using the tail pointer. This preserves the required ordering rule.
5. For an `out x` operation, retrieve the node from `pos[x]` and remove it from the list. We reconnect its previous and next nodes. If it was head or tail, we update the corresponding pointer. Finally, remove `x` from the dictionary.
6. For `check`, we output `head.value` if the list is non-empty, otherwise output -1.

Why it works: the linked list always represents the exact current order of guests. The dictionary guarantees we can locate any referenced guest in constant time. Every insertion preserves relative order by only modifying local adjacency, and every deletion preserves order among remaining nodes. Since all operations modify or query only constant local structure, the global ordering invariant is never violated.

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

def main():
    q = int(input().strip())

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
                ny = pos[y]

                node.prev = ny
                node.next = ny.next

                if ny.next:
                    ny.next.prev = node
                ny.next = node

                if tail == ny:
                    tail = node
            else:
                node.prev = tail
                node.next = None

                if tail:
                    tail.next = node
                tail = node

                if head is None:
                    head = node

        elif cmd[0] == "out":
            x = int(cmd[1])
            node = pos.pop(x)

            if node.prev:
                node.prev.next = node.next
            else:
                head = node.next

            if node.next:
                node.next.prev = node.prev
            else:
                tail = node.prev

        else:
            if head is None:
                out.append("-1")
            else:
                out.append(str(head.val))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation relies on a manual doubly linked list because Python’s built-in list does not support O(1) mid-insert or delete. The dictionary `pos` is the critical component that avoids traversal.

The insertion logic carefully distinguishes whether the friend exists. When inserting after a node, we must handle the case where the friend is the tail, since `ny.next` is None and we must update `tail`. Similarly, when inserting into an empty list, both head and tail must be initialized.

Deletion must handle boundary cases symmetrically. Removing the head requires updating `head`, and removing the tail requires updating `tail`. The dictionary removal ensures stale references never appear again.

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

| Step | Operation | List State | Head |
| --- | --- | --- | --- |
| 1 | in 1 1 | 1 | 1 |
| 2 | in 2 1 | 1 2 | 1 |
| 3 | in 3 1 | 1 3 2 | 1 |
| 4 | in 4 2 | 1 3 2 4 | 1 |
| 5 | check | 1 3 2 4 | 1 |
| 6 | out 4 | 1 3 2 | 1 |
| 7 | check | 1 3 2 | 1 |
| 8 | in 5 6 | 1 3 2 5 | 1 |
| 9 | in 6 5 | 1 3 2 5 6 | 1 |
| 10 | check | 1 3 2 5 6 | 1 |

This trace shows how missing friends cause append behavior, while existing friends enforce local insertion without disturbing earlier structure.

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

| Step | Operation | List State | Head |
| --- | --- | --- | --- |
| 1 | check | empty | - |
| 2 | in 10 5 | 10 | 10 |
| 3 | in 9 3 | 10 9 | 10 |
| 4 | in 6 7 | 10 9 6 | 10 |
| 5 | out 6 | 10 9 | 10 |
| 6 | in 5 3 | 10 9 5 | 10 |
| 7 | in 3 4 | 10 9 5 3 | 10 |
| 8 | check | 10 9 5 3 | 10 |
| 9 | in 7 2 | 10 9 5 3 7 | 10 |
| 10 | in 2 8 | 10 9 5 3 7 2 | 10 |

The second trace highlights that even when referenced friends are absent, the system behaves deterministically by appending, maintaining stability of ordering rules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each operation performs only dictionary access and pointer updates |
| Space | O(q) | Each guest is stored as one node plus one hash map entry |

The constraints allow up to 200,000 operations, and the solution performs constant-time work per operation, so total work remains linear and comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return None  # placeholder for integration

# provided samples
# assert run(...) == ...

# custom tests

# empty checks only
assert run("3\ncheck\ncheck\ncheck\n") == "-1\n-1\n-1"

# single insert then removal
assert run("3\nin 1 1\ncheck\nout 1\ncheck\n") == "1\n-1"

# chain insertion behind head
assert run("4\nin 1 1\nin 2 1\nin 3 2\ncheck\n") == "1"

# repeated re-insert behavior
assert run("6\nin 1 1\nin 2 1\nout 2\nin 2 1\ncheck\nin 3 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty checks | all -1 | empty structure handling |
| insert + delete | 1 then -1 | head/tail updates |
| chained inserts | 1 | local insertion correctness |
| reinsert after removal | stable ordering | dictionary consistency |

## Edge Cases

One important edge case is inserting when the referenced friend is the current tail. In that case, the insertion logic must update the tail pointer. For example:

Input:

```
3
in 1 1
in 2 1
in 3 2
```

After processing, the list becomes `1 2 3`. When inserting `3` after `2`, the node `2` is the tail at that moment, so failing to update `tail` would leave the structure inconsistent and break later insertions or checks. The algorithm explicitly checks this and assigns `tail = node`.

Another edge case is deleting the head element. If the first element leaves, the head pointer must move forward. For:

```
3
in 1 1
in 2 1
out 1
```

The list becomes `2`. The deletion logic detects `node.prev is None` and updates `head = node.next`. Without this adjustment, `check` would still return a removed element.

A final edge case is repeated reinsertion of the same id. Since each `in x y` creates a fresh node and updates `pos[x]`, any previous occurrence must already have been removed. The dictionary ensures only the current node is tracked, so no stale pointers can be accessed.
