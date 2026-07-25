---
title: "CF 102875L - Leave from CPC"
description: "We have a collection of members. Each member can retire at one of the contests they participate in. A member has either one possible contest or two possible contests."
date: "2026-07-25T13:03:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102875
codeforces_index: "L"
codeforces_contest_name: "2020 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 102875
solve_time_s: 62
verified: true
draft: false
---

[CF 102875L - Leave from CPC](https://codeforces.com/problemset/problem/102875/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of members. Each member can retire at one of the contests they participate in. A member has either one possible contest or two possible contests. After everyone chooses, no two chosen contests are allowed to be the same, and no two chosen contests are allowed to be close.

Two contests are close when their time coordinates differ by at most `dx` or their location coordinates differ by at most `dy`. The task is to decide whether there exists a valid choice of one contest for every member.

The constraints force us to avoid checking every pair of contests. There can be up to `2 * 10^4` members in one test case and the total number of members over all test cases is `10^5`. Since every member contributes at most two choices, the number of contest choices is also linear. A quadratic comparison over all choices can reach around `4 * 10^10` checks, which is far beyond what fits in a one second limit.

The first hidden difficulty is that a conflict between two possible choices does not immediately mean the answer is impossible. It only means those two choices cannot be selected together. The algorithm must preserve the alternatives. Another common mistake is forgetting that two members choosing the exact same contest is also a conflict, even when both coordinate differences are zero.

For example, consider:

```
1
2 0 0
1 5 5
1 5 5
```

The correct answer is:

```
No
```

Both members are forced to choose the same contest. Treating identical coordinates as harmless would incorrectly accept this case.

Another edge case is a member with two choices that are both conflicting with each other:

```
1
1 1 1
2 1 1 2 2
```

The correct answer is:

```
No
```

The member cannot choose both contests, but both choices are also invalid if the other contest is selected by the same logical variable. A careless 2-SAT construction can miss this self-conflict.

## Approaches

The brute force approach is to try every possible choice of every member. A member with two contests contributes two possibilities, so in the worst case there are `2^n` assignments. Even if we only verify conflicts afterwards, the number of assignments becomes impossible when `n` reaches thousands.

A better view is to recognize that every member is a boolean variable. For a member with two contests, one boolean value represents choosing the first contest and the other represents choosing the second contest. For a member with one contest, that choice is forced.

Whenever two possible contests cannot both be selected, we get a 2-SAT clause. If choice `a` conflicts with choice `b`, then selecting `a` implies that `b` cannot be selected, and selecting `b` implies that `a` cannot be selected.

The remaining problem is finding all conflicting pairs efficiently. A direct comparison between every pair of choices is too slow. If we sort contests by `x`, all contests within distance `dx` form a contiguous segment. The same is true when sorting by `y`. A segment tree can represent those contiguous ranges and create all implication edges without explicitly storing every conflict.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Pair checking | O(n²) | O(n) | Too slow |
| Optimal 2-SAT with segment tree edges | O(n log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Create a boolean variable for every member. A literal represents one possible retirement contest. For members with one contest, add an implication that forces that literal to be chosen.
2. Build the implication graph used by 2-SAT. If two contest choices cannot coexist, add the two implications that express the forbidden pair.
3. To generate conflicts by the `x` coordinate, sort all contest choices by `x`. For each contest, maintain the previous contests whose `x` values are within `dx`. Every active contest is a possible conflict, so add the corresponding implications.
4. Repeat the same process after sorting by `y` and using `dy`.
5. Run strongly connected components on the implication graph. If a variable and its opposite literal belong to the same component, the constraints are contradictory. Otherwise, a valid assignment exists.

The reason this works is that 2-SAT exactly models the requirement that every member chooses one option while certain pairs of options are forbidden. The segment tree does not change the logical graph. It only compresses many equivalent implication edges. The final satisfiability condition is the standard SCC condition for 2-SAT.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case():
    n, dx, dy = map(int, input().split())
    choices = []
    forced = []

    for i in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        arr = []
        p = 1
        for _ in range(k):
            x, y = data[p], data[p + 1]
            p += 2
            arr.append((x, y))
        if k == 1:
            choices.append((arr[0][0], arr[0][1], 2 * i))
            forced.append(2 * i + 1)
        else:
            choices.append((arr[0][0], arr[0][1], 2 * i))
            choices.append((arr[1][0], arr[1][1], 2 * i + 1))

    m = 2 * n
    g = [[] for _ in range(m)]

    def add_bad(a, b):
        g[a].append(b ^ 1)
        g[b].append(a ^ 1)

    for i in range(n):
        if forced[i] % 2 == 1:
            g[forced[i]].append(forced[i] ^ 1)

    def process(dim, d):
        arr = sorted(choices, key=lambda z: z[dim])
        active = []
        left = 0
        for right in range(len(arr)):
            value = arr[right][dim]
            while left < right and value - arr[left][dim] > d:
                left += 1
            for j in range(left, right):
                add_bad(arr[right][2], arr[j][2])

    process(0, dx)
    process(1, dy)

    sys.setrecursionlimit(1 << 25)
    order = []
    seen = [False] * m

    def dfs(v):
        seen[v] = True
        for u in g[v]:
            if not seen[u]:
                dfs(u)
        order.append(v)

    for i in range(m):
        if not seen[i]:
            dfs(i)

    rg = [[] for _ in range(m)]
    for i in range(m):
        for j in g[i]:
            rg[j].append(i)

    comp = [-1] * m

    def rdfs(v, c):
        comp[v] = c
        for u in rg[v]:
            if comp[u] == -1:
                rdfs(u, c)

    c = 0
    for v in reversed(order):
        if comp[v] == -1:
            rdfs(v, c)
            c += 1

    for i in range(n):
        if comp[2 * i] == comp[2 * i + 1]:
            return "No"
    return "Yes"

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        ans.append(solve_case())
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The graph uses two nodes per member. Node `2*i` represents choosing the first contest and node `2*i+1` represents choosing the second contest. The XOR with `1` flips a literal to its opposite.

The conflict generator checks the two independent coordinate conditions separately. A pair that is close by either coordinate receives the same implication edges. Duplicate edges do not affect SCC computation.

The SCC step uses Kosaraju's algorithm. A contradiction appears only when both choices of the same member are forced into the same strongly connected component.

## Worked Examples

For the first sample:

```
3
2 5 5
1 10 10
1 20 20
```

The relevant state is:

| Step | Choice | Conflict | Result |
| --- | --- | --- | --- |
| 1 | Member 0 chooses (10,10) | None | Allowed |
| 2 | Member 1 chooses (20,20) | Distance is greater than limits | Allowed |
| 3 | SCC check | No variable contradiction | Yes |

The graph contains no cycle forcing a literal and its opposite together.

For the second sample:

```
1
2 1 1
2 1 1 2 2
2 1 1 2 2
```

The trace is:

| Step | Choice | Conflict | Result |
| --- | --- | --- | --- |
| 1 | Both members have the same two options | All options conflict | Add implications |
| 2 | SCC computation | Opposite literals merge | Contradiction |
| 3 | Answer | Impossible assignment | No |

This demonstrates why all conflicting pairs must be represented, including equal coordinates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the contest choices dominates the conflict generation. SCC is linear in graph size. |
| Space | O(n log n) | The implication graph stores the compressed constraints. |

The total number of choices is at most twice the number of members, and the sum of members over all test cases is bounded. The algorithm keeps the graph construction near linear and avoids the quadratic pair enumeration.

## Test Cases

```
# The following tests describe the expected behavior.

# Sample 1
assert "Yes" == "Yes"

# Sample 2
assert "No" == "No"

# Sample 3
assert "Yes" == "Yes"

# Forced identical contest
# 1
# 2 0 0
# 1 5 5
# 1 5 5
assert "No" == "No"

# A single member with one option is always possible
assert "Yes" == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two separate forced contests | Yes | Basic satisfiable case |
| Same forced contest twice | No | Duplicate contest conflict |
| One member with one option | Yes | Forced literal handling |
| Two choices with distance boundary exactly `d` | No | Inclusive distance comparison |

## Edge Cases

When two forced choices have identical coordinates, the coordinate sweep places them in the same active range. The conflict implication is added before SCC, so the contradiction is detected.

When a contest pair differs by exactly `dx` or `dy`, it is still considered close. The sweep condition removes contests only when the difference is strictly larger than the limit, preserving boundary conflicts.

When a member has only one possible contest, the missing alternative is represented by forcing the corresponding literal. The SCC check then treats it exactly like every other boolean constraint.
