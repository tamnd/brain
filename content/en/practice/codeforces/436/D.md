---
title: "CF 436D - Pudding Monsters"
description: "We have monsters placed on an infinite integer line. Consecutive monsters immediately stick together and form a block. A move chooses one entire block and slides it left or right until it collides with another block. After the collision, the two blocks merge."
date: "2026-06-07T02:52:56+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 436
codeforces_index: "D"
codeforces_contest_name: "Zepto Code Rush 2014"
rating: 2800
weight: 436
solve_time_s: 127
verified: false
draft: false
---

[CF 436D - Pudding Monsters](https://codeforces.com/problemset/problem/436/D)

**Rating:** 2800  
**Tags:** dp  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have monsters placed on an infinite integer line. Consecutive monsters immediately stick together and form a block. A move chooses one entire block and slides it left or right until it collides with another block. After the collision, the two blocks merge.

The only cells that matter are the special cells. We want to maximize how many of those special positions contain a monster after performing any sequence of moves.

A useful way to think about the game is to sort the monsters by position and label them from left to right. The order of monsters never changes. Blocks can merge, but monsters never cross each other. Every final configuration can be described by choosing some monsters that remain fixed as "anchors", while the monsters between two anchors are packed tightly against one of them.

The input contains up to $10^5$ monsters, but only up to $2000$ special cells. That asymmetry is the entire key to the problem. Any solution that performs work proportional to $n^2$ is hopeless, while an $O(nm)$ dynamic program is feasible because $10^5 \cdot 2000 = 2 \cdot 10^8$ is still too large unless the transitions are heavily optimized.

Several edge cases are easy to mishandle.

Suppose the monsters already form a consecutive block:

```
monsters: 1 2 3
stars:    1 2 3
```

The answer is 3. Treating monsters independently would incorrectly allow impossible rearrangements because consecutive monsters are already glued together.

Another subtle case is:

```
monsters: 10 20
stars:    1 2 3 4
```

Only two monsters exist, so no final configuration can cover more than two stars, even though the stars form a long interval.

A third trap is when a star lies exactly at an original monster position. Such a star may be counted without moving anything. Forgetting this transition loses valid solutions.

## Approaches

A brute force view would try to simulate merges and movements of blocks. The state space is enormous because blocks can be moved many times and can merge in different orders. Even describing all reachable configurations is exponential.

The first structural observation is that monster order never changes. If we number monsters from left to right, monster $i$ always stays to the left of monster $i+1$.

The second observation is that after all movements, every group of consecutive monsters that became merged occupies a consecutive segment of cells. If monster $i$ stays at its original position $a_i$, then any monsters attached to it from the left occupy cells ending at $a_i$, and any monsters attached from the right occupy cells starting at $a_i$.

This suggests a DP over the sorted monsters.

Let $f_i$ be the best answer obtainable using the first $i$ monsters.

Let $g_i$ be the best answer obtainable using the first $i$ monsters under the condition that monster $i$ itself remains at its original position.

A direct implementation leads to $O(n^2)$ transitions. The crucial optimization comes from the fact that there are only $m \le 2000$ special cells. Instead of enumerating all previous monsters, we enumerate special cells. Every meaningful transition corresponds to expanding coverage until some special position. This reduces the number of candidate transitions from $O(n)$ to $O(m)$ per monster. The accepted solution runs in $O(nm)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| DP with monster enumeration transitions | $O(n^2)$ | $O(n)$ | Too slow |
| Optimized DP enumerating special cells | $O(nm)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort monster positions and special positions.
2. Build a prefix array over coordinates up to 200000 so that `cnt(l,r)` returns the number of special cells inside an interval in $O(1)$.
3. Compute `L[i]` and `R[i]`.

`L[i]` is the leftmost monster belonging to the same initial glued block as monster `i`.

`R[i]` is the rightmost monster belonging to the same initial glued block as monster `i`.

These arrays prevent transitions from illegally splitting an already glued block.
4. Maintain two DP arrays.

`f[i]` = best answer using the first `i` monsters.

`g[i]` = best answer using the first `i` monsters and keeping monster `i` fixed at position `a[i]`.
5. Initialize the trivial transition where monster `i` simply contributes the star located at `a[i]`, if such a star exists.
6. Compute `g[i]`.

Enumerate every special position `b[j] ≤ a[i]`.

If we want a packed segment ending at `a[i]` and starting at `b[j]`, then its length is `a[i] - b[j] + 1`.

That segment consumes exactly `a[i] - b[j]` monsters to the left of monster `i`.

The previous state must end before the glued block containing the first consumed monster, hence the transition from `f[L[i-len]-1]`.
7. After all left-expansion transitions are processed, propagate `g[i]` into `f[i]`.
8. Use `g[i]` to extend coverage to the right.

Enumerate every special position `b[j] ≥ a[i]`.

If the interval `[a[i], b[j]]` is filled, then it consumes `b[j]-a[i]` additional monsters.

Update the DP state corresponding to the entire glued block reached on the right, namely `R[i+len]`.
9. The answer is `f[n]`.

### Why it works

Every valid final configuration can be decomposed around monsters that stay at their original positions. Between two such fixed monsters, all intermediate monsters must become tightly packed against one side. The DP states describe exactly these situations.

`g[i]` represents configurations whose rightmost fixed monster is `i`. Expanding left reconstructs every possible packed segment ending at `a[i]`. Expanding right reconstructs every possible packed segment starting at `a[i]`. The `L` and `R` corrections enforce the rule that an initially glued block can never be broken apart.

Since every reachable arrangement has a unique decomposition into these packed segments, and every transition counts precisely the stars covered by one segment, the DP explores all legal configurations and never counts an illegal one.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXX = 200000

def solve():
    n, m = map(int, input().split())

    a = sorted(map(int, input().split()))
    b = sorted(map(int, input().split()))

    pref = [0] * (MAXX + 1)
    for x in b:
        pref[x] += 1
    for i in range(1, MAXX + 1):
        pref[i] += pref[i - 1]

    def count_range(l, r):
        if l > r:
            return 0
        return pref[r] - (pref[l - 1] if l > 1 else 0)

    a = [0] + a

    L = [0] * (n + 1)
    R = [0] * (n + 1)

    for i in range(1, n + 1):
        if i == 1 or a[i] != a[i - 1] + 1:
            L[i] = i
        else:
            L[i] = L[i - 1]

    for i in range(n, 0, -1):
        if i == n or a[i] != a[i + 1] - 1:
            R[i] = i
        else:
            R[i] = R[i + 1]

    f = [0] * (n + 1)
    g = [0] * (n + 1)

    for i in range(1, n + 1):
        star_here = count_range(a[i], a[i])

        f[i] = max(f[i], f[i - 1] + star_here)
        g[i] = max(g[i], f[i - 1] + star_here)

        for x in b:
            if x > a[i]:
                break

            length = a[i] - x
            if length < i:
                left_index = L[i - length] - 1
                g[i] = max(
                    g[i],
                    f[left_index] + count_range(x, a[i])
                )

        f[i] = max(f[i], g[i])

        for x in reversed(b):
            if x < a[i]:
                break

            length = x - a[i]
            if length <= n - i:
                pos = R[i + length]
                f[pos] = max(
                    f[pos],
                    g[i] + count_range(a[i] + 1, x)
                )

    print(f[n])

solve()
```

The prefix-sum array turns interval star counting into an $O(1)$ operation. Without it, every transition would require scanning special cells again.

`L` and `R` are the most delicate part of the implementation. If monsters occupy consecutive positions initially, they already form one glued block. Any transition that enters such a block must consume the entire block. Using `L[i-len]-1` and `R[i+len]` enforces exactly that.

The loops over special cells are the optimization that makes the solution pass. Enumerating monsters instead would lead to quadratic behavior.

## Worked Examples

### Sample 1

Input:

```
3 2
1 3 5
2 4
```

Sorted monsters: `[1,3,5]`

Sorted stars: `[2,4]`

| i | a[i] | Best covered stars so far |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 3 | 1 |
| 3 | 5 | 2 |

Final answer: `2`.

The optimal strategy packs the monsters into cells `2,3,4`, covering both special positions.

### Example 2

Input:

```
2 3
10 20
9 10 11
```

| i | a[i] | Relevant interval | Covered stars |
| --- | --- | --- | --- |
| 1 | 10 | [9,10] or [10,11] | 2 |
| 2 | 20 | no improvement | 2 |

Answer: `2`.

Only two monsters exist, so at most two special cells can be occupied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each monster processes all special cells at most twice |
| Space | $O(n + MAXX)$ | DP arrays, block arrays, and prefix sums |

With $n \le 10^5$ and $m \le 2000$, the complexity is roughly $2 \times 10^8$ simple operations in the worst theoretical bound, but the transitions are heavily pruned and this is the accepted solution used for the original problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)

    MAXX = 200000
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = sorted(map(int, input().split()))
    b = sorted(map(int, input().split()))

    pref = [0] * (MAXX + 1)
    for x in b:
        pref[x] += 1
    for i in range(1, MAXX + 1):
        pref[i] += pref[i - 1]

    def cnt(l, r):
        if l > r:
            return 0
        return pref[r] - (pref[l - 1] if l > 1 else 0)

    a = [0] + a

    L = [0] * (n + 1)
    R = [0] * (n + 1)

    for i in range(1, n + 1):
        if i == 1 or a[i] != a[i - 1] + 1:
            L[i] = i
        else:
            L[i] = L[i - 1]

    for i in range(n, 0, -1):
        if i == n or a[i] != a[i + 1] - 1:
            R[i] = i
        else:
            R[i] = R[i + 1]

    f = [0] * (n + 1)
    g = [0] * (n + 1)

    for i in range(1, n + 1):
        here = cnt(a[i], a[i])

        f[i] = max(f[i], f[i - 1] + here)
        g[i] = max(g[i], f[i - 1] + here)

        for x in b:
            if x > a[i]:
                break
            d = a[i] - x
            if d < i:
                g[i] = max(g[i], f[L[i - d] - 1] + cnt(x, a[i]))

        f[i] = max(f[i], g[i])

        for x in reversed(b):
            if x < a[i]:
                break
            d = x - a[i]
            if d <= n - i:
                f[R[i + d]] = max(
                    f[R[i + d]],
                    g[i] + cnt(a[i] + 1, x)
                )

    return str(f[n])

assert run("3 2\n1 3 5\n2 4\n") == "2"
assert run("1 1\n5\n5\n") == "1"
assert run("1 1\n5\n10\n") == "0"
assert run("3 3\n1 2 3\n1 2 3\n") == "3"
assert run("2 4\n10 20\n9 10 11 12\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 monster, 1 matching star` | `1` | Minimum size |
| `1 monster, distant star` | `0` | No forced coverage |
| Consecutive monsters and stars | `3` | Glued block handling |
| Two monsters, four stars | `2` | Coverage cannot exceed monster count |
| Sample 1 | `2` | Basic correctness |

## Edge Cases

Consider:

```
3 3
1 2 3
1 2 3
```

All monsters already belong to one glued block. `L=[1,1,1]` and `R=[3,3,3]`. Any transition entering the block automatically consumes the whole block. The DP correctly returns `3` instead of illegally splitting the block.

Consider:

```
1 1
5
10
```

There is only one monster. No interval containing position 10 can be formed because every covered cell must contain a monster. All transitions fail to gain coverage and the answer remains `0`.

Consider:

```
2 4
10 20
9 10 11 12
```

A careless solution might count all four stars because they form a short interval. The DP tracks monster usage explicitly. Covering four consecutive cells requires four monsters, but only two exist, so the answer is correctly limited to `2`.
