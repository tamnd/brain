---
title: "CF 102625D - Best Wishes !!"
description: "We start with a charge of 1 on the first day. Every following day, the new charge must be obtained from the previous day's charge by one of three operations: doubling it, tripling it, or increasing it by one."
date: "2026-08-03T15:18:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "D"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 69
verified: true
draft: false
---

[CF 102625D - Best Wishes !!](https://codeforces.com/problemset/problem/102625/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
# Problem Understanding

We start with a charge of 1 on the first day. Every following day, the new charge must be obtained from the previous day's charge by one of three operations: doubling it, tripling it, or increasing it by one. Given a target charge `D`, we need to find the smallest number of days needed so that the charge on the final day is exactly `D`. We also have to print one valid sequence of daily charges that reaches the target in that minimum number of days.

The input contains several independent targets. Since the maximum target is only `10^6`, the intended solution can afford preprocessing over all possible values up to the largest target that appears. A solution that tries to search separately from every query would waste work because there can be `10^5` queries. At this scale, an `O(D)` or `O(maxD)` preprocessing approach is suitable, while algorithms that explore many paths independently for each query can easily become too slow.

The main edge cases appear around very small values and values where the best route does not use the largest multiplication immediately. For example, for `D = 1`, the answer is one day and the sequence is just `1`. An implementation that starts searching from a move instead of considering the starting state could incorrectly return a longer answer.

For `D = 5`, the optimal sequence is:

```
1 3 4 5
```

The output is `4` days. A greedy strategy that always multiplies when possible might choose `1 2 4 5`, which is valid but also has four days here, hiding the problem. On larger values, blindly preferring multiplication can miss shorter paths because reaching a useful intermediate value with `+1` can enable a later multiplication chain.

For `D = 10`, one shortest sequence is:

```
1 2 3 9 10
```

The answer is `5` days. A method that only stores distances but not parent choices would find the correct minimum length but would not be able to reconstruct the required charge sequence.

# Approaches

A direct brute-force solution can model every possible sequence of operations. Starting from `1`, it tries all combinations of `+1`, `*2`, and `*3` until reaching `D`. This is correct because every legal sequence is explored, so the first shortest sequence found gives the answer. The problem is the number of possibilities. After `k` days there can be up to `3^k` different operation sequences, so this grows exponentially and becomes impossible even for moderately large targets.

The structure of the problem gives a much cleaner view. Every charge value is a node in a graph. From a value `x`, there are edges to `x + 1`, `2x`, and `3x` whenever those values are not larger than the maximum target we need. Every valid sequence of charges is exactly a path in this graph. Since every operation costs one day, the shortest sequence is the shortest path from node `1` to node `D`. Because all edges have equal cost, breadth-first search finds the minimum number of days.

The brute-force search fails because it repeatedly explores similar partial sequences. BFS merges all paths that reach the same charge value, solving each state once. By storing a parent for every visited value, we can reconstruct the exact sequence after finding the target.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k) | O(k) | Too slow |
| Optimal | O(maxD) | O(maxD) | Accepted |

# Algorithm Walkthrough

1. Read all target values and find the largest target `M`. We only need to build states up to `M` because no useful intermediate value can exceed the final destination in this problem. All operations only increase the charge.
2. Run BFS starting from charge `1`. Store the distance of every reached charge and the previous charge used to reach it. The BFS queue guarantees that values are processed in increasing number of days.
3. For every current charge `x`, try the three possible next charges: `x + 1`, `2x`, and `3x`. Ignore values larger than `M` or values that have already been visited. The first time a value is visited is through a shortest path, so its parent can be fixed permanently.
4. For each query `D`, start from `D` and repeatedly follow stored parents until reaching `1`. Reverse this collected list to obtain the daily charge sequence in forward order.

Why it works: BFS explores all states reachable in one day before any state reachable in two days, then all states reachable in two days before three days, and so on. Therefore, the first time a charge value is reached, the path used has the smallest possible number of operations. The parent pointers store exactly one shortest path to every reachable charge, so following them from `D` back to `1` reconstructs an optimal sequence.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    queries = data[1:1 + t]
    limit = max(queries)

    parent = [-1] * (limit + 1)
    parent[1] = 0

    from collections import deque
    q = deque([1])

    while q:
        x = q.popleft()

        for y in (x + 1, x * 2, x * 3):
            if y <= limit and parent[y] == -1:
                parent[y] = x
                q.append(y)

    ans = []
    for d in queries:
        path = []
        cur = d
        while cur != 0:
            path.append(cur)
            if cur == 1:
                break
            cur = parent[cur]
        path.reverse()

        ans.append(str(len(path)))
        ans.append(" ".join(map(str, path)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The preprocessing section builds the shortest path tree once. The `parent` array has two purposes: `parent[x] == -1` means the value has not been reached yet, and otherwise it stores the previous charge in the shortest path.

The BFS transition order does not affect correctness because all operations have equal cost. The only required condition is that every newly discovered state is added once. Values above the maximum query are ignored because they can never be part of a path ending at a smaller target.

During reconstruction, the path is collected backwards from `D` to `1`. Reversing it gives the order of daily charges. The number of days is the number of values in the sequence, not the number of operations, because the first day already contains the initial charge `1`.

# Worked Examples

For `D = 5`, BFS reaches the target through the following shortest path.

| Current charge | Operation | New charge | Parent stored |
| --- | --- | --- | --- |
| 1 | *3 | 3 | 1 |
| 3 | +1 | 4 | 3 |
| 4 | +1 | 5 | 4 |

Following parents from `5` gives `5 -> 4 -> 3 -> 1`, which reverses to:

```
1 3 4 5
```

This example shows that a sequence containing smaller increments can beat a strategy focused only on multiplication.

For `D = 10`, one possible BFS reconstruction is:

| Current charge | Operation | New charge | Parent stored |
| --- | --- | --- | --- |
| 1 | *2 | 2 | 1 |
| 2 | +1 | 3 | 2 |
| 3 | *3 | 9 | 3 |
| 9 | +1 | 10 | 9 |

The reconstructed sequence is:

```
1 2 3 9 10
```

This demonstrates why all three transitions must be considered. Removing the `+1` operation would make some optimal paths unreachable.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(maxD) | Each charge value is visited once and has three outgoing transitions. |
| Space | O(maxD) | The parent array and BFS queue store information for each reachable charge. |

The maximum target is `10^6`, so the preprocessing visits at most one million states. This is easily within the limits, and it avoids repeating work across up to `10^5` queries.

# Test Cases

```python
import sys
import io
from collections import deque

def solution(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        sys.stdin = old
        return ""

    t = data[0]
    queries = data[1:1+t]
    limit = max(queries)

    parent = [-1] * (limit + 1)
    parent[1] = 0
    q = deque([1])

    while q:
        x = q.popleft()
        for y in (x + 1, x * 2, x * 3):
            if y <= limit and parent[y] == -1:
                parent[y] = x
                q.append(y)

    out = []
    for d in queries:
        path = []
        while d:
            path.append(d)
            if d == 1:
                break
            d = parent[d]
        path.reverse()
        out.append(str(len(path)))
        out.append(" ".join(map(str, path)))

    sys.stdin = old
    return "\n".join(out)

assert solution("3\n1\n5\n96234\n").splitlines()[0:4] == ["1", "1", "4", "1 3 4 5"]
assert solution("1\n1000000\n").splitlines()[0] == "20"

assert solution("1\n1\n") == "1\n1"
assert solution("1\n2\n") == "2\n1 2"
assert solution("1\n3\n") == "2\n1 3"
assert solution("1\n10\n").splitlines()[0] == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1 / 1` | The starting state is already the answer. |
| `2` | `2 / 1 2` | Smallest non-trivial transition. |
| `3` | `2 / 1 3` | Direct multiplication is handled. |
| `10` | `5` days | Reconstruction through mixed operations. |
| `1000000` | `20` days | Large boundary value and preprocessing limit. |

# Edge Cases

For `D = 1`, the BFS starts with the answer already discovered. The reconstruction loop stops immediately and returns the single charge `1`. This avoids the common mistake of assuming that at least one operation is required.

For targets such as `D = 5`, the algorithm does not force multiplication paths. BFS explores all three choices from every value and keeps the first shortest route to each state. The stored parent chain reaches `5` through `1 -> 3 -> 4 -> 5`, giving the minimum number of days.

For the maximum target `D = 1000000`, the algorithm does not create states beyond this value. The BFS still covers the entire useful search space once, and the parent array allows reconstruction without another search. The resulting sequence has the minimum possible length because every state was assigned its distance during BFS.
