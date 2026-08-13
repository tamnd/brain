---
title: "CF 102284K - \u041f\u0440\u0438\u0448\u0451\u043b \u0414\u0435\u043c\u0438\u0434 \u0438 \u0432\u0441\u0451 \u043f\u0440\u043e\u0432\u0435\u0440\u0438\u043b"
description: "We have a queue of (N) packages. Each package belongs to one of four groups, represented by the digits 6, 7, 8, and 9. Reading the groups from left to right gives the number whose value defines the beauty of the queue."
date: "2026-08-13T08:58:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "K"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 201
verified: true
draft: false
---

[CF 102284K - \u041f\u0440\u0438\u0448\u0451\u043b \u0414\u0435\u043c\u0438\u0434 \u0438 \u0432\u0441\u0451 \u043f\u0440\u043e\u0432\u0435\u0440\u0438\u043b](https://codeforces.com/problemset/problem/102284/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a queue of (N) packages. Each package belongs to one of four groups, represented by the digits 6, 7, 8, and 9. Reading the groups from left to right gives the number whose value defines the beauty of the queue. Since all queues have the same length, maximizing this number is exactly the same as maximizing the string lexicographically.

The only allowed operation is swapping two adjacent packages. Swapping groups (i) and (j) costs (c_{i,j}) seconds, and the total cost cannot exceed (K). The task is to output the lexicographically largest sequence reachable within that budget.

The constraints are (N\le 10^5) and (K\le 10^9). The original Codeforces statement gives a 2 second time limit and 512 MB memory limit. A quadratic algorithm would already perform around (5\cdot10^9) elementary iterations in the worst case, which is far beyond the intended limit. The useful structural fact is that there are only four possible digits, so an algorithm doing constant work per package is realistic.

There are several cases that easily break a careless implementation.

Consider a budget of zero with zero-cost swaps:

```
3 0
678
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```

The correct answer is `876`. A program that interprets (K=0) as "no swaps are allowed" would incorrectly return `678`. A swap can cost zero, so the condition is cost at most (K), not number of swaps at most (K).

A second trap is that moving a package several positions costs the sum of all adjacent swaps on its path. For example:

```
3 1
678
0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0
```

Moving 8 to the front costs (1+1=2), so it is impossible. Moving 7 one position left costs 1, giving the answer `768`. A careless implementation that checks only the cost of swapping 8 with its immediate predecessor could incorrectly choose `867` or `876`.

Large individual costs create another boundary case:

```
3 1000000000
678
0 1000000000 1000000000 1000000000
1000000000 0 1000000000 1000000000
1000000000 1000000000 0 1000000000
1000000000 1000000000 1000000000 0
```

Moving 7 to the front costs exactly (10^9), so it is allowed. Moving 8 costs (2\cdot10^9), so it is not. The answer is `768`. The equality case must use `cost <= K`, and intermediate costs can exceed 32-bit integer range even though (K) itself is at most (10^9).

## Approaches

The most direct approach is to construct the answer from left to right. At every position, inspect the remaining queue and determine which package could be moved to the front within the remaining budget. Among those packages, choose the largest digit. While scanning the remaining queue, we can maintain the cost of moving each encountered package to the front, so one position can be processed in linear time.

This greedy choice is correct because the first digit dominates the value of the whole number. If a 9 can be placed at the current position, choosing anything smaller can never be repaired by later positions. If the chosen digit can be moved to the front within the remaining budget, we can perform exactly those swaps and leave the rest of the queue untouched, so the choice is always feasible.

The problem with this implementation is the repeated scan. There can be (N) candidates for the first output position, (N-1) candidates for the second, and so on. The total number of visited positions can reach

[
N+(N-1)+\cdots+1=\frac{N(N+1)}2,
]

which is about (5\cdot10^9) when (N=10^5).

The key observation is that there are only four possible digits. For each digit (d), we do not need to consider every occurrence of (d). The cheapest occurrence to move to the front is always the first remaining occurrence of (d), because every other occurrence has all of the same preceding packages plus additional nonnegative swap costs.

So at every moment we only need four candidates. For each digit, maintain the position of its first remaining occurrence and the exact cost required to bring that occurrence to the front.

After selecting a package of type (d), its removal affects these four costs in a very structured way. For another digit (x), if the selected package lies before the first remaining (x), removing it decreases the cost for (x) by (c_{d,x}). If it lies after the first (x), that cost does not change.

The only less immediate update concerns the selected digit (d). Its first occurrence disappears, so we have to find the next remaining (d). We keep a doubly linked list of the currently remaining original positions. Starting immediately after the removed position, we walk until the next (d), adding the crossing costs. For a fixed digit, these walks pass through disjoint intervals between consecutive occurrences of that digit, so every original position is visited at most once for that digit. Since there are only four digits, all such walks together take (O(4N)=O(N)) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive greedy scan | (O(N^2)) | (O(N)) | Too slow |
| Optimal four-candidate maintenance | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Convert every character from `6` through `9` to an index from 0 through 3. This makes the cost matrix directly addressable and lets us iterate over the four possible groups in decreasing order.
2. For every digit, find its first remaining occurrence. At the beginning, this is simply its first occurrence in the original string. Alongside it, compute `cost[d]`, the cost of moving this occurrence to the front of the current queue.

For the first occurrence of (d), every package before it must be crossed exactly once. Thus its cost is the sum of (c_{x,d}) over all remaining packages before it.
3. Build a doubly linked list over the original positions. `prev[i]` and `next[i]` tell us the previous and next package that is still in the queue. Removing a package from this list represents moving it into the already constructed answer prefix.
4. At every output position, inspect digits 9, 8, 7, and 6 in that order. Choose the first digit whose first remaining occurrence exists and whose `cost[d]` is at most the remaining budget.

This is the greedy decision. The largest affordable digit must be chosen because the current position has greater significance than every later position combined.
5. Append the chosen digit to the answer and subtract its movement cost from (K). The selected occurrence is the first remaining occurrence of that digit, so moving it to the front costs exactly `cost[d]`.
6. Remove the selected position from the linked list. This changes the relative order of the remaining packages exactly as the adjacent swaps would.
7. Update the cost of every other digit (x). If its first remaining occurrence lies after the removed position, that removed package was one of the packages that had to be crossed, so its cost decreases by (c_{d,x}). If its first occurrence lies before the removed position, the removed package was not part of its crossing path, so its cost stays unchanged.
8. Find the next remaining occurrence of the selected digit. Starting from the next remaining package after the removed position, walk through the linked list until another package of the same digit is found. Add the cost of crossing every visited package to the old cost.

The old first occurrence had some packages before it. Those packages remain before the new first occurrence. The newly visited packages between the two occurrences must also be crossed, so adding exactly their costs gives the new `cost[d]`.
9. Repeat until all (N) packages have been placed in the answer.

### Why it works

The invariant is that before every iteration, `first[d]` is the first remaining occurrence of digit (d), and `cost[d]` is exactly the cost of moving that occurrence to the front of the remaining queue.

Because all swap costs are nonnegative, no later occurrence of the same digit can be cheaper to move to the front than the first one. Thus `cost[d]` represents the minimum possible cost for putting digit (d) at the current position.

If the largest digit with `cost[d] <= K` is (d), there is a valid queue beginning with (d), obtained by moving its first occurrence to the front. Any queue beginning with a smaller digit is lexicographically worse immediately. Hence every greedy choice agrees with the first digit of an optimal answer.

The cost updates preserve the invariant. Removing a package before the first occurrence of another digit removes exactly one required swap from that digit's movement cost. Removing the first occurrence of the selected digit changes its target to the next occurrence, and the linked-list scan adds exactly the costs of the newly crossed remaining packages. Therefore the invariant remains true after every iteration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()
    a = [ord(ch) - ord('6') for ch in s]

    c = [list(map(int, input().split())) for _ in range(4)]

    first = [-1] * 4
    cost = [0] * 4

    # Find the first occurrence of every digit and its initial movement cost.
    for i, x in enumerate(a):
        for d in range(4):
            if first[d] == -1 and d != x:
                cost[d] += c[x][d]
        if first[x] == -1:
            first[x] = i

    # Doubly linked list of currently remaining positions.
    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    nxt[n - 1] = -1

    answer = []

    for _ in range(n):
        chosen = -1

        # Lexicographically largest affordable digit.
        for d in range(3, -1, -1):
            if first[d] != -1 and cost[d] <= k:
                chosen = d
                break

        # The current first remaining package is always affordable:
        # choosing it costs zero.
        if chosen == -1:
            # This branch is unreachable.
            break

        p = first[chosen]
        spent = cost[chosen]
        k -= spent
        answer.append(chr(ord('6') + chosen))

        # Save the next remaining position before unlinking p.
        q = nxt[p]
        left = prev[p]

        if left != -1:
            nxt[left] = q
        if q != -1:
            prev[q] = left

        # Removing p reduces the cost for every first occurrence after p.
        for d in range(4):
            if d != chosen and first[d] != -1 and p < first[d]:
                cost[d] -= c[chosen][d]

        # Find the next remaining occurrence of the chosen digit.
        new_cost = spent
        cur = q

        while cur != -1 and a[cur] != chosen:
            new_cost += c[a[cur]][chosen]
            cur = nxt[cur]

        first[chosen] = cur
        if cur == -1:
            cost[chosen] = 0
        else:
            cost[chosen] = new_cost

    print(''.join(answer))

if __name__ == "__main__":
    solve()
```

The initial `first` and `cost` construction processes the original queue once. When position `i` contains digit `x`, it contributes to the cost of every digit whose first occurrence has not appeared yet, except for `x` itself. The exception matters because the first occurrence of `x` is the target, so it is not crossed.

The linked list represents the queue after previously selected packages have been moved into the answer. We use original indices rather than physically modifying the string, which avoids shifting (O(N)) elements after every selection.

The selection loop checks only four digits. Since it checks from 9 down to 6, the first feasible candidate is exactly the lexicographically best current digit.

The update for the other three digits uses the comparison `p < first[d]`. This comparison is against original positions, but that is also the order in the linked list of all still-remaining packages. Removing packages never changes the relative order of packages that remain.

For the chosen digit, `spent` is the old cost of its first occurrence. After that occurrence is removed, the scan begins at its next remaining package. Every package encountered before the next occurrence of the same digit must be crossed by the new first occurrence. The linked list automatically skips packages that have already been selected.

All costs are stored in Python integers. A movement can cross (10^5) packages, each costing up to (10^9), so intermediate sums can reach (10^{14}), much larger than a 32-bit integer.

The condition is `cost[d] <= k`, not `cost[d] < k`, because spending the entire remaining budget is allowed.

## Worked Examples

For the provided sample, the initial queue is `999789` and the budget is 2. The first three 9s are already at the front, so they cost nothing to select. The first 8 would require crossing 9, 9, 9, and 7, which costs (3+3+3+1=10), so it cannot be selected initially. After the first three 9s are fixed, 8 only needs to cross 7, which costs 1.

| Step | Remaining first candidates | Candidate costs for 6, 7, 8, 9 | Budget | Chosen |
| --- | --- | --- | --- | --- |
| 1 | 7, 8, 9 | unavailable, 3, 10, 0 | 2 | 9 |
| 2 | 7, 8, 9 | unavailable, 3, 10, 0 | 2 | 9 |
| 3 | 7, 8, 9 | unavailable, 3, 10, 0 | 2 | 9 |
| 4 | 7, 8, 9 | unavailable, 1, 1, 1 | 2 | 8 |
| 5 | 7, 9 | unavailable, 0, 0 | 1 | 9 |
| 6 | 7 | unavailable, 0, unavailable | 1 | 7 |

The fourth step demonstrates why costs must be maintained for the current remaining queue rather than calculated only from the original positions. After the first three selections, 8 has only one remaining package before it, namely 7, so its cost is exactly 1. The resulting answer is `999897`.

For a second example, consider

```
3 1
678
0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0
```

Initially, 6 costs 0, 7 costs 1, and 8 costs 2. The largest affordable digit is 7. After moving it to the front, the remaining queue is `68` and the remaining budget is 0.

| Step | Remaining order | Cost of 6 | Cost of 7 | Cost of 8 | Budget | Chosen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 678 | 0 | 1 | 2 | 1 | 7 |
| 2 | 68 | 0 | unavailable | 1 | 0 | 6 |
| 3 | 8 | unavailable | unavailable | 0 | 0 | 8 |

The second step demonstrates the cost update. Removing 7 decreases the cost of bringing 8 forward by exactly (c_{7,8}=1). Since the remaining budget is zero, 8 cannot move before 6, so the final result is `768`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Each iteration checks four digits, and for each digit the linked-list scan crosses each original position at most once. |
| Space | (O(N)) | The string representation, type array, and two linked-list arrays all use linear memory. |

For (N=10^5), the algorithm performs only a constant amount of work per package apart from the four bounded digit checks. The total movement-cost sums can be much larger than (K), but Python integers handle them exactly. The linear complexity is comfortably suited to the stated 2 second and 512 MB limits.

## Test Cases

```python
import io
import sys

def solve_data(inp: str) -> str:
    it = iter(inp.split())

    n = int(next(it))
    k = int(next(it))
    s = next(it)

    c = [[int(next(it)) for _ in range(4)] for _ in range(4)]

    a = [ord(ch) - ord('6') for ch in s]

    first = [-1] * 4
    cost = [0] * 4

    for i, x in enumerate(a):
        for d in range(4):
            if first[d] == -1 and d != x:
                cost[d] += c[x][d]
        if first[x] == -1:
            first[x] = i

    prev = [i - 1 for i in range(n)]
    nxt = [i + 1 for i in range(n)]
    nxt[n - 1] = -1

    ans = []

    for _ in range(n):
        chosen = -1

        for d in range(3, -1, -1):
            if first[d] != -1 and cost[d] <= k:
                chosen = d
                break

        p = first[chosen]
        spent = cost[chosen]
        k -= spent
        ans.append(chr(ord('6') + chosen))

        q = nxt[p]
        left = prev[p]

        if left != -1:
            nxt[left] = q
        if q != -1:
            prev[q] = left

        for d in range(4):
            if d != chosen and first[d] != -1 and p < first[d]:
                cost[d] -= c[chosen][d]

        new_cost = spent
        cur = q

        while cur != -1 and a[cur] != chosen:
            new_cost += c[a[cur]][chosen]
            cur = nxt[cur]

        first[chosen] = cur
        cost[chosen] = 0 if cur == -1 else new_cost

    return ''.join(ans)

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided sample
assert run(
    """\
6 2
999789
1 1 1 1
1 1 1 1
1 1 1 3
1 1 3 1
"""
) == "999897", "sample 1"

# Minimum-size input
assert run(
    """\
1 0
6
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
"""
) == "6", "single package"

# Zero budget, but all swaps are free
assert run(
    """\
3 0
678
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
"""
) == "876", "free swaps must still be allowed"

# Exact budget boundary and multi-swap cost
assert run(
    """\
3 1
678
0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0
"""
) == "768", "8 needs two swaps, 7 needs exactly one"

# Costs near the maximum and exact K boundary
assert run(
    """\
3 1000000000
678
0 1000000000 1000000000 1000000000
1000000000 0 1000000000 1000000000
1000000000 1000000000 0 1000000000
1000000000 1000000000 1000000000 0
"""
) == "768", "large integer costs"

# Maximum-size input, all equal values
n = 100000
s = "6" * n
matrix = "\n".join(["0 0 0 0"] * 4)
large_input = f"{n} 0\n{s}\n{matrix}\n"

assert run(large_input) == s, "maximum N and all equal values"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0`, queue `6` | `6` | Minimum size and no available alternative. |
| `3 0`, queue `678`, all costs zero | `876` | Zero-cost swaps are valid even with zero budget. |
| `3 1`, queue `678`, unit swap costs | `768` | A package may require multiple adjacent swaps, and equality with (K) is allowed. |
| `3 10^9`, queue `678`, off-diagonal costs (10^9) | `768` | Large integer sums and the exact budget boundary. |
| (N=100000), queue of only `6` | The same 100000-character string | Maximum input size and repeated equal values. |

## Edge Cases

The zero-budget case with free swaps is handled by the comparison `cost[d] <= k`. For

```
3 0
678
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```

every candidate has movement cost zero. The algorithm first chooses 9, then 8, then 7, producing `876`. No special treatment for (K=0) is necessary.

The multi-swap case

```
3 1
678
0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0
```

starts with costs 0 for 6, 1 for 7, and 2 for 8. The algorithm selects 7 because it is the largest affordable digit. Removing 7 causes the cost of 8 to decrease from 2 to 1, because 7 was one of the packages that 8 would have crossed. The remaining budget is zero, so 6 is selected before 8. The output is `768`.

The large-cost case

```
3 1000000000
678
0 1000000000 1000000000 1000000000
1000000000 0 1000000000 1000000000
1000000000 1000000000 0 1000000000
1000000000 1000000000 1000000000 0
```

has cost 0 for 6, (10^9) for 7, and (2\cdot10^9) for 8. The algorithm accepts 7 exactly at the budget boundary and rejects 8. After spending (10^9), the remaining budget is zero, giving `768`. Python's arbitrary-precision integers preserve the (2\cdot10^9) comparison without overflow.

Equal values require no artificial swaps. If the queue consists entirely of 6s, the first remaining 6 always has cost zero because it is already at the front of the remaining queue. The algorithm simply selects the next 6 repeatedly. Even if (c_{6,6}) is large, there is no reason to swap equal packages, so that diagonal cost never enters the movement cost of the first occurrence.

The maximum-size case has (N=10^5), so physically modifying the queue after every selection would be dangerous because repeated shifts could become quadratic. The linked-list representation removes a selected position in constant time and changes only the cost data affected by that removal. The total scanning work stays linear because each position is traversed at most once for each of the four possible digits.
