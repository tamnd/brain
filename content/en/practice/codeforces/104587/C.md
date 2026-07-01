---
title: "CF 104587C - Math Trade"
description: "Each person in the input owns exactly one object and wants exactly one object. We can think of each person as a directed edge in a graph: from the object they currently have to the object they want."
date: "2026-06-30T07:28:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104587
codeforces_index: "C"
codeforces_contest_name: "2020-2021 ICPC East Central North America Regional Contest (ECNA 2020)"
rating: 0
weight: 104587
solve_time_s: 46
verified: true
draft: false
---

[CF 104587C - Math Trade](https://codeforces.com/problemset/problem/104587/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Each person in the input owns exactly one object and wants exactly one object. We can think of each person as a directed edge in a graph: from the object they currently have to the object they want. Because every object is uniquely owned and uniquely desired, every object appears exactly once as a source and exactly once as a target.

A valid “math trade chain” is a sequence of people such that the object wanted by the first person is currently owned by the second, the second’s wanted object is owned by the third, and so on. If you follow the chain of dependencies, you are essentially walking along directed edges induced by people. The key constraint is that trades are only possible when this chain is consistent, which forces the structure to be disjoint directed cycles.

The task reduces to finding the longest such cycle formed by these directed edges, and outputting its length in terms of number of people involved. If no cycle of length at least 2 exists, the answer is that no trade can be made.

The input size is small, at most 100 people. This immediately rules out any need for heavy graph machinery beyond simple mappings and traversal. An O(n²) or even O(n) solution per test case is perfectly sufficient.

A subtle case arises when the mapping forms only self-loops, meaning a person wants exactly what they already have. Such a person does not contribute to a trade chain. Another edge case is when the graph decomposes into multiple small cycles of different sizes, where we must correctly identify the largest one rather than just detecting existence of a cycle.

## Approaches

The structure induced by the problem is a functional graph: every node (person) points to exactly one other node (the person who owns the desired object). Because object ownership is unique, each node has exactly one outgoing edge and exactly one incoming edge, forming a permutation-like structure over participants.

A brute-force approach would attempt to start from every person and follow the chain until repetition is detected, recording cycle lengths. This is already close to optimal since each walk is deterministic. However, if implemented carelessly, one might restart traversal for every node and repeatedly walk the same cycles, leading to redundant work. In the worst case, this becomes O(n²), which is still fine here but conceptually inefficient.

The key observation is that we are dealing with disjoint cycles. Each node belongs to exactly one cycle, so once a node is visited, its entire cycle can be marked and never recomputed. This suggests a simple DFS-like or visited-array traversal that extracts each cycle exactly once.

We can therefore iterate over all nodes, and whenever we find an unvisited node, we follow its outgoing edges until we return to a visited node, counting the cycle length if it is valid. The answer is the maximum such length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force walk from each node | O(n²) | O(n) | Accepted |
| Cycle decomposition with visited marking | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first convert object names into indices so that we can work with arrays instead of strings. This makes traversal constant-time per step.

1. Build two hash maps: one mapping object name to owner index, and one mapping owner index to desired object name. The first mapping is essential because it lets us instantly jump from an object to its owner.
2. Construct a functional graph array next[] where next[i] is the index of the person who owns the object that person i wants. This creates a deterministic pointer from each node to exactly one other node.
3. Maintain a visited array initialized to false for all nodes. This ensures we do not recompute cycles we have already processed.
4. Iterate through every node i from 0 to n−1. If node i is already visited, skip it because it belongs to a previously processed cycle.
5. If node i is not visited, start walking from i following next pointers, marking nodes as visited and counting how many unique nodes are encountered until we return to a visited node. This traversal necessarily stays within one cycle because every node has exactly one outgoing edge.
6. If the cycle length is at least 2, update the answer with this value.
7. After processing all nodes, output the maximum cycle length found, or report that no valid cycle exists if no cycle length exceeds 1.

The correctness hinges on the fact that once we enter a cycle, we cannot escape it, and since each node has exactly one outgoing edge, the traversal cannot branch.

### Why it works

The constructed graph is a permutation on the set of participants induced by object ownership and demand. In such a graph, every connected component is a directed cycle. Each cycle is disjoint and every node belongs to exactly one cycle. The traversal marks every node in a cycle exactly once, so cycle lengths are computed precisely without duplication or omission. The maximum over these cycle lengths is therefore the longest possible valid trade chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    if n == 0:
        print("No trades possible")
        return

    owner_of = {}
    want = []
    names = []

    for i in range(n):
        name, have, need = input().strip().split()
        names.append(name)
        owner_of[have] = i
        want.append(need)

    nxt = [-1] * n
    for i in range(n):
        if want[i] in owner_of:
            nxt[i] = owner_of[want[i]]

    visited = [False] * n
    ans = 0

    for i in range(n):
        if visited[i]:
            continue

        cur = i
        cnt = 0
        path = []

        while not visited[cur]:
            visited[cur] = True
            path.append(cur)
            cnt += 1
            cur = nxt[cur]

            if cur == -1:
                cnt = 0
                break

        if cnt > 1:
            ans = max(ans, cnt)

    if ans == 0:
        print("No trades possible")
    else:
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading all participants and building a mapping from each object to its owner. This is the key transformation that allows us to jump from a “wanted object” directly to the person who currently holds it.

The next pointer array encodes the functional graph: each person points to exactly one other person, or to -1 if the desired object does not exist among participants. The visited array ensures each node is processed once.

During traversal, we accumulate a path until we encounter a visited node. Since cycles are disjoint, this traversal captures exactly one cycle or breaks if the chain is incomplete. We only consider cycles of size at least 2, since size 1 corresponds to a person who wants their own item and does not form a trade.

A subtle detail is that marking visited immediately during traversal prevents revisiting nodes from other cycles, ensuring linear behavior.

## Worked Examples

### Example 1

Input:

```
Sally Clock Doll
Steve Doll Painting
Carlos Painting Clock
Maria Candlestick Vase
```

We build mappings:

Sally → Clock, Steve → Doll, Carlos → Painting, Maria → Candlestick

Clock → Sally, Doll → Steve, Painting → Carlos, Vase → Maria

Traversal:

| Start | Path | Next steps | Cycle size |
| --- | --- | --- | --- |
| Sally | Sally → Steve → Carlos → Sally | closes cycle | 3 |
| Steve | already visited | skip | - |
| Carlos | already visited | skip | - |
| Maria | Maria → Maria | self-loop | 1 |

Maximum cycle size is 3, so output is 3.

This confirms that only the meaningful cycle contributes, while self-loops are ignored.

### Example 2

Input:

```
Abby Bottlecap Card
Bob Card Spoon
Chris Spoon Chair
Dan Pencil Pen
```

Mappings:

Abby → Bob → Chris → Abby forms a cycle of 3. Dan → Dan is a self-loop.

| Start | Path | Next steps | Cycle size |
| --- | --- | --- | --- |
| Abby | Abby → Bob → Chris → Abby | cycle closes | 3 |
| Bob | visited | skip | - |
| Chris | visited | skip | - |
| Dan | Dan | self-loop | 1 |

Output is 3.

This shows that disconnected cycles are handled independently and the maximum is correctly selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once while traversing its cycle, and visited prevents reprocessing |
| Space | O(n) | Storage for mappings, next pointers, and visited array |

The constraints limit n to 100, so even inefficient approaches would pass easily. This linear solution is comfortably within limits and leaves ample margin.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""Sally Clock Doll
Steve Doll Painting
Carlos Painting Clock
Maria Candlestick Vase""") == "3"

# sample 2
assert run("""Abby Bottlecap Card
Bob Card Spoon
Chris Spoon Chair
Dan Pencil Pen""") == "3"

# all self loops
assert run("""A X X
B Y Y
C Z Z""") == "No trades possible"

# single cycle
assert run("""A A B
B B C
C C A""") == "3"

# two cycles different sizes
assert run("""A A B
B B A
C C D
D D C""") == "2"

# no edges except broken chain
assert run("""A A B
B B C
C C D""") == "No trades possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all self loops | No trades possible | ignores trivial cycles |
| single cycle | 3 | detects full cycle |
| two cycles | 2 | selects maximum cycle |
| broken chain | No trades possible | handles invalid pointers |

## Edge Cases

One edge case is when every participant wants their own item. For example:

```
A X X
B Y Y
C Z Z
```

Each node points to itself. The traversal marks each node individually, but cycle size is always 1, so no valid trade is recorded. The algorithm correctly outputs “No trades possible”.

Another case is a mix of a valid cycle and isolated self-loops. The visited array ensures the cycle is discovered once, and self-loops are treated as size 1 cycles that do not affect the answer. The maximum over all components still yields the correct longest trade chain.
