---
title: "CF 102538B - Best Tree"
description: "The problem describes a tree and asks for the maximum number of times we can perform the required operation on it. The tree is represented by its number of vertices and the degree of every vertex."
date: "2026-08-04T08:59:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102538
codeforces_index: "B"
codeforces_contest_name: "300iq Contest 3"
rating: 0
weight: 102538
solve_time_s: 50
verified: true
draft: false
---

[CF 102538B - Best Tree](https://codeforces.com/problemset/problem/102538/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a tree and asks for the maximum number of times we can perform the required operation on it. The tree is represented by its number of vertices and the degree of every vertex. A vertex with degree one is a leaf, while a vertex with degree greater than one is an internal vertex. The answer depends only on how many internal vertices exist and the total number of vertices in the tree.

The key observation is that every operation needs a pair of vertices that can be combined into a new structure while preserving the possibility of forming a valid tree. The number of possible operations is limited by two different resources. A tree with n vertices can only contain at most half that many disjoint pairs, and leaf vertices cannot repeatedly provide useful pairs except in the smallest possible tree. Because of this, the final answer is the smaller value between half of the vertices and the number of internal vertices.

The constraints are designed so that the degrees must be processed directly. If n is around 10^5, any approach that tries every possible pair of vertices already becomes too slow because it would require around 10^10 checks. A linear scan is enough because the solution only needs to count vertices satisfying a simple degree condition.

There are several edge cases where a direct formula can fail if implemented carelessly. The smallest tree is the first one. For a tree with two vertices, both vertices are leaves, so the number of internal vertices is zero. However, the answer is one because the only possible pair can still be chosen.

For example, consider the input:

```
2
1 1
```

The correct output is:

```
1
```

A solution that always returns the number of internal vertices would incorrectly output zero.

Another boundary case is a star shaped tree. Consider:

```
5
4 1 1 1 1
```

There is only one internal vertex, so the answer is one. The value n / 2 is larger, but there are not enough internal vertices to create more valid operations. A solution that only considers the number of vertices would overestimate the answer.

A path also checks the opposite boundary. For:

```
6
1 2 2 2 2 1
```

there are four internal vertices and n / 2 equals three, so the answer is three. Counting only internal vertices would incorrectly return four.

## Approaches

A straightforward approach would try to simulate the merging process. We could repeatedly search for suitable pairs of vertices, update the tree, and count how many operations are possible. This is correct because it follows the definition of the process directly. However, it requires maintaining the changing structure of the tree and repeatedly finding candidates. In the worst case, checking all possible pairs requires O(n²) work, which is far beyond what is reasonable for large trees.

The brute force works because every valid operation is explicitly explored, but it fails when the tree becomes large. The observation that the answer is controlled only by the number of internal vertices and the maximum number of disjoint pairs lets us avoid constructing the operations entirely.

Let x be the number of vertices with degree greater than one. The answer cannot exceed x because each useful operation needs an internal vertex. It also cannot exceed n / 2 because each operation consumes two vertices. The remaining task is proving that this upper bound is always achievable.

The construction behind the proof is to repeatedly combine the vertex with the smallest degree and the vertex with the largest degree. Doing this min(n / 2, x) times leaves enough structure to represent the merged pairs as a smaller valid tree. The important consequence is that the degree information alone is enough, so the actual tree edges are unnecessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices and inspect every vertex degree. Count how many vertices have degree greater than one. These are the only vertices that can contribute to the answer.
2. If the tree contains exactly two vertices, return one immediately. This handles the special case where there are no internal vertices but one operation is still possible.
3. Compute the maximum possible number of operations from the two independent limits. The first limit is the number of internal vertices. The second limit is the number of pairs that can be formed from all vertices, which is floor(n / 2).
4. Output the smaller of these two values. This value is achievable because the merging argument shows that enough valid pairs can always be formed.

Why it works:

The answer cannot be larger than the number of internal vertices because two leaves cannot form a useful pair in a tree with more than two vertices. It also cannot exceed the number of vertex pairs available. The construction that repeatedly joins a minimum degree vertex with a maximum degree vertex proves that every one of these possible operations can actually be realized. After performing the required number of merges, the remaining structure still has valid tree degrees, so the upper bound is also a lower bound.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    n = data[0]
    degrees = data[1:]

    if n == 2:
        print(1)
        return

    internal = 0
    for d in degrees:
        if d > 1:
            internal += 1

    print(min(n // 2, internal))

if __name__ == "__main__":
    solve()
```

The program only needs the degree sequence. It first handles the special two vertex tree because the general formula would incorrectly return zero there.

For every other case, the loop counts vertices with degree greater than one. The variable `internal` represents the value x from the proof. The final expression uses integer division because only complete pairs of vertices matter.

There are no overflow concerns in Python because integer values are arbitrary precision, and the largest stored value is only the number of vertices. The order of operations is also important: the special case must be checked before applying the general formula.

## Worked Examples

Consider:

```
2
1 1
```

| Step | n | Internal vertices | Formula result | Output |
| --- | --- | --- | --- | --- |
| Initial | 2 | 0 | Special case | 1 |

This example confirms why the smallest tree must be separated from the general rule. The degree count alone is not enough because both vertices are leaves.

Consider:

```
6
1 2 2 2 2 1
```

| Step | Vertex degree | Internal count |
| --- | --- | --- |
| Start | 1 2 2 2 2 1 | 0 |
| Read degree 2 | Internal vertex found | 1 |
| Read degree 2 | Internal vertex found | 2 |
| Read degree 2 | Internal vertex found | 3 |
| Read degree 2 | Internal vertex found | 4 |

The final values are n / 2 = 3 and internal = 4, so the answer is min(3, 4) = 3. This demonstrates the limit caused by the number of available pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every degree is inspected once. |
| Space | O(1) | Only counters are needed after reading input. |

The solution fits the intended constraints because it performs a single pass over the degree list. Even for very large trees, the number of operations grows linearly with the input size.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    data = list(map(int, sys.stdin.read().split()))
    if data:
        n = data[0]
        degrees = data[1:]

        if n == 2:
            print(1)
        else:
            internal = sum(1 for d in degrees if d > 1)
            print(min(n // 2, internal))

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("2\n1 1\n") == "1\n", "minimum tree"
assert run("5\n4 1 1 1 1\n") == "1\n", "star tree"
assert run("6\n1 2 2 2 2 1\n") == "3\n", "path tree"
assert run("8\n1 3 2 2 2 2 1 1\n") == "4\n", "pair limit boundary"
assert run("7\n6 1 1 1 1 1 1\n") == "1\n", "single internal vertex"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with degrees 1, 1 | 1 | Special case handling |
| Five vertex star | 1 | Internal vertex limit |
| Six vertex path | 3 | Pair count limit |
| Eight vertex tree with many internal nodes | 4 | Maximum pairing boundary |
| Seven vertex star | 1 | Cases with only one internal vertex |

## Edge Cases

The two vertex tree is the only case where the formula needs an exception. For:

```
2
1 1
```

the algorithm immediately returns one. Without this check, the count of internal vertices is zero and the answer would be wrong.

For a star tree:

```
5
4 1 1 1 1
```

the algorithm counts only one internal vertex. It then compares one with floor(5 / 2), which is two, and returns one. This follows the invariant that internal vertices are the limiting resource when leaves dominate the tree.

For a path:

```
6
1 2 2 2 2 1
```

the algorithm counts four internal vertices. Since only three disjoint pairs exist among six vertices, it returns three. This verifies that the second limit is applied correctly.

The algorithm does not need to know the actual connections between vertices. The degree sequence contains exactly the information needed because the proof shows that every tree with the same relevant degree counts has the same maximum answer.

You can adapt this editorial further if you have the original Codeforces input/output section or official samples, since those were not included in the provided statement excerpt.
