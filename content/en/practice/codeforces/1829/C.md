---
title: "CF 1829C - Mr. Perfectly Fine"
description: "Victor has two independent skills he wants to acquire, and each book he can read either teaches him skill 1, skill 2, both, or none. Every book also has a time cost."
date: "2026-06-09T07:16:48+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1829
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 871 (Div. 4)"
rating: 800
weight: 1829
solve_time_s: 68
verified: true
draft: false
---

[CF 1829C - Mr. Perfectly Fine](https://codeforces.com/problemset/problem/1829/C)

**Rating:** 800  
**Tags:** bitmasks, greedy, implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Victor has two independent skills he wants to acquire, and each book he can read either teaches him skill 1, skill 2, both, or none. Every book also has a time cost. The task is to choose a set of books whose combined skills cover both required skills while minimizing the total reading time.

Each book is essentially a small “bundle”: it contributes a bitmask over two bits and has a cost. We are allowed to pick any subset of books, but we care only about the union of acquired skills, not the order or repetition. The goal is to reach the full mask `11` with minimum total cost.

The input size is large across test cases, with total number of books up to 200,000. This immediately rules out any solution that tries all subsets or even pairwise combinations for every test case independently. A quadratic or exponential approach will not survive.

A subtle point is that reading multiple books that teach overlapping skills is allowed, but never beneficial if one book strictly dominates another in both skills and cost. Another edge case is when no combination can cover both skills even though each individual skill exists separately.

For example, if we have books:

```
3 10
4 01
```

the answer is `7`, but if both books only give `00`, the answer is `-1` even though books exist.

Another pitfall is assuming a single book might suffice; the correct solution must explicitly handle the case where one book already has `11`.

## Approaches

A direct brute-force approach would try all subsets of books and compute the union of skills for each subset. Each subset check is O(n), and there are 2^n subsets, which is impossible even for n = 30, let alone 2e5.

We can reduce the structure by noticing that there are only four possible skill states: `00`, `01`, `10`, and `11`. This collapses the problem into selecting at most two books that combine to form `11`, or possibly a single book that already equals `11`.

The key observation is that we only ever need:

- the cheapest book that provides `10`
- the cheapest book that provides `01`
- the cheapest book that provides `11`

Any optimal solution must fall into one of two categories. Either we take one `11` book, or we take one `10` book and one `01` book. No other combination improves on this because adding extra books can only increase cost without improving coverage beyond `11`.

Thus the problem reduces to maintaining three minimum values while scanning the input once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n) | O(n) | Too slow |
| Track best candidates | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and reduce all books into a few representative candidates.

1. Initialize three variables: `best_01`, `best_10`, and `best_11` as infinity. These track the minimum cost among books that provide each skill pattern. We only care about the cheapest representative of each type.
2. Iterate over all books. For each book, inspect its binary string and classify it into one of the four types.
3. If the book gives `11`, update `best_11` with its minimum cost. This is important because a single book can already solve the problem.
4. If the book gives `01`, update `best_01`.
5. If the book gives `10`, update `best_10`.
6. Ignore `00` books because they never contribute to the final skill set.
7. After processing all books, compute the best possible answer as the minimum of:

the cost of `best_11`, and the sum `best_01 + best_10`.
8. If both `best_11` is infinite and either `best_01` or `best_10` is infinite, then it is impossible to form `11`, so output `-1`.

### Why it works

The state space is fully captured by the two bits. Any solution that uses more than two books can be compressed: if it uses multiple `10` books, only the cheapest matters; similarly for `01`. If it mixes multiple types, the final combination still reduces to either a single `11` or one `10` plus one `01`. Therefore, tracking only the minimum cost per type preserves all optimal constructions.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

t = int(input())
for _ in range(t):
    n = int(input())

    best_01 = INF
    best_10 = INF
    best_11 = INF

    for _ in range(n):
        parts = input().split()
        cost = int(parts[0])
        s = parts[1]

        if s == "11":
            best_11 = min(best_11, cost)
        elif s == "10":
            best_10 = min(best_10, cost)
        elif s == "01":
            best_01 = min(best_01, cost)

    ans = min(best_11, best_01 + best_10)

    if ans >= INF:
        print(-1)
    else:
        print(ans)
```

The code is a direct implementation of the three-candidate reduction. Each book is classified in constant time. The final decision compares only two structural possibilities.

A common implementation mistake is forgetting to initialize candidates to a large value, which would incorrectly allow missing categories to contribute zero. Another is treating `"00"` as relevant, which is unnecessary and can introduce incorrect minima if mishandled.

## Worked Examples

### Example 1

Input:

```
n = 4
2 00
3 10
4 01
4 00
```

| Book | Cost | Type | best_10 | best_01 | best_11 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 00 | INF | INF | INF |
| 2 | 3 | 10 | 3 | INF | INF |
| 3 | 4 | 01 | 3 | 4 | INF |
| 4 | 4 | 00 | 3 | 4 | INF |

Final computation:

`min(INF, 3 + 4) = 7`

This confirms the algorithm correctly combines one `10` and one `01`.

### Example 2

Input:

```
n = 3
5 11
8 01
7 10
```

| Book | Cost | Type | best_10 | best_01 | best_11 |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 11 | INF | INF | 5 |
| 2 | 8 | 01 | INF | 8 | 5 |
| 3 | 7 | 10 | 7 | 8 | 5 |

Final computation:

`min(5, 7 + 8) = 5`

This shows why direct `11` is always a candidate independent of combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each book is processed once with O(1) classification and updates |
| Space | O(1) | Only three scalar variables are maintained |

The total number of books across test cases is bounded by 2e5, so the linear scan is comfortably within limits. Memory usage remains constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    INF = 10**18
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        best_01 = INF
        best_10 = INF
        best_11 = INF

        for _ in range(n):
            cost, s = input().split()
            cost = int(cost)

            if s == "11":
                best_11 = min(best_11, cost)
            elif s == "10":
                best_10 = min(best_10, cost)
            elif s == "01":
                best_01 = min(best_01, cost)

        ans = min(best_11, best_01 + best_10)
        out.append(str(ans if ans < INF else -1))

    return "\n".join(out)

# provided sample
assert run("""6
4
2 00
3 10
4 01
4 00
5
3 01
3 01
5 01
2 10
9 10
1
5 11
3
9 11
8 01
7 10
6
4 01
6 01
7 01
8 00
9 01
1 00
4
8 00
9 10
9 11
8 11
""") == """7
5
5
9
-1
8"""

# single book direct solve
assert run("""1
1
5 11
""") == "5"

# impossible case
assert run("""1
2
3 10
4 10
""") == "-1"

# must combine
assert run("""1
2
3 10
4 01
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 11 book | 5 | direct solution |
| only one skill type | -1 | impossibility detection |
| 10 + 01 combo | 7 | correct pairing logic |

## Edge Cases

When all books are `00`, the algorithm keeps all candidates at infinity and correctly outputs `-1` because no combination improves the state.

When only one of `01` or `10` exists, the sum becomes impossible since one term remains infinity, preventing a false valid answer.

When multiple optimal candidates exist, the algorithm always retains the minimum cost due to continuous `min` updates, ensuring correctness even under heavy duplication or reordering.
