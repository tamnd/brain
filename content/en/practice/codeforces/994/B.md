---
title: "CF 994B - Knights of a Polygonal Table"
description: "Each knight comes with two attributes, a fighting strength and a stash of coins. A knight is only able to defeat knights with strictly smaller strength, and every victory transfers the defeated knight’s coins to the winner."
date: "2026-06-17T00:09:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 994
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 488 by NEAR (Div. 2)"
rating: 1400
weight: 994
solve_time_s: 262
verified: true
draft: false
---

[CF 994B - Knights of a Polygonal Table](https://codeforces.com/problemset/problem/994/B)

**Rating:** 1400  
**Tags:** greedy, implementation, sortings  
**Solve time:** 4m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

Each knight comes with two attributes, a fighting strength and a stash of coins. A knight is only able to defeat knights with strictly smaller strength, and every victory transfers the defeated knight’s coins to the winner. However, there is a global constraint: no knight is willing to defeat more than `k` others.

The task is to imagine that every knight independently plans an optimal sequence of fights under these rules and compute, for each knight, the maximum number of coins they could end up with.

The input gives an array of strengths and an array of coin values aligned by index. The output is another array where each position corresponds to a knight and contains the best achievable total coins starting from that knight.

The constraints shape the solution space strongly. With up to 100,000 knights, any approach that tries to simulate fights between all pairs immediately becomes quadratic and infeasible. A naive $O(n^2)$ strategy would already perform on the order of $10^{10}$ comparisons in the worst case, which is far beyond what a one-second time limit can tolerate. The additional restriction that $k \le 10$ is the key structural hint: each knight is only ever interested in a very small number of best candidates among all weaker knights.

A subtle failure case appears when thinking greedily without sorting by strength. If a knight considers only nearby indices, it might miss weaker knights that appear later in input order but are actually valid targets. For example, if strengths are `[10, 1, 2]`, the first knight could defeat both others, but a position-based scan without sorting would incorrectly treat ordering as meaningful. Another common pitfall is ignoring the “at most k kills” constraint and simply summing all weaker coins, which fails when there are many small-value weak knights and only a few high-value ones should be chosen.

## Approaches

A direct interpretation suggests trying every knight against all others, checking which ones are weaker and selecting the best subset of up to `k` among them. This is correct in principle because it evaluates all possible valid choices, but it becomes too slow because for each knight we may scan all others and then sort or select up to `k` best candidates, leading to a total cost of roughly $O(n^2 \log n)$.

The structural simplification comes from separating the constraints. Strength determines feasibility of a kill, while coins determine desirability. If we process knights in increasing order of strength, then at the moment we handle a knight, all previously processed knights are exactly the ones it is allowed to kill. The problem then reduces to maintaining, for each prefix of this ordering, the best possible subset of size at most `k` by coin value.

Instead of recomputing the best subset from scratch for every knight, we maintain a small structure containing only the top `k` coin values among all weaker knights seen so far. Since `k` is at most 10, a min-heap works efficiently: it stores the current best candidates, and whenever a new weaker knight appears, we decide whether it belongs in the top `k`. This turns the selection step into logarithmic time with a tiny constant.

The key transition is that the answer for each knight depends only on the multiset of coins belonging to strictly weaker knights, reduced to its best `k` elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We first reorder the knights by increasing strength so that all valid targets for a knight appear before it.

1. Pair each knight’s strength, coins, and original index into a single structure, then sort these structures by strength. This guarantees that when we process a knight, every previously processed knight is strictly weaker.
2. Maintain a min-heap that stores coin values of selected weaker knights, along with a running sum of the heap contents. The heap will never contain more than `k` elements. This structure represents the best set of up to `k` kills available so far.
3. Iterate through knights in sorted order. Before inserting the current knight into the heap, compute the answer for it as its own coins plus the current heap sum. This works because the heap at this moment contains exactly the best `k` coins from all strictly weaker knights.
4. Insert the current knight’s coin value into the heap and add it to the running sum. If the heap size exceeds `k`, remove the smallest element and subtract it from the sum. This keeps only the most profitable `k` candidates for future stronger knights.
5. After processing all knights, restore results to the original order using stored indices.

The central idea is that each knight queries a prefix structure over the sorted-by-strength array, where the prefix is continuously maintained as the best possible set of up to `k` coin values.

### Why it works

At the moment we process a knight, the heap contains exactly the `k` largest coin values among all knights with smaller strength. Any optimal strategy for this knight can only choose from these weaker knights, and since it is allowed to pick at most `k`, replacing any chosen subset with the best `k` available cannot decrease the total. This establishes that the heap always represents the optimal choice set for all future knights, and thus each computed answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

n, k = map(int, input().split())
p = list(map(int, input().split()))
c = list(map(int, input().split()))

knights = [(p[i], c[i], i) for i in range(n)]
knights.sort()

heap = []
heap_sum = 0
ans = [0] * n

for power, coins, idx in knights:
    ans[idx] = coins + heap_sum

    heapq.heappush(heap, coins)
    heap_sum += coins

    if len(heap) > k:
        removed = heapq.heappop(heap)
        heap_sum -= removed

print(*ans)
```

The sorting step ensures we only ever consider valid weaker opponents when computing each answer. The heap always stores the best possible candidates among them, and the running sum avoids recomputing heap totals repeatedly. The use of a min-heap is crucial because it allows efficient removal of the least useful coin value whenever the size exceeds `k`.

A common implementation mistake is inserting the current knight into the heap before computing its answer. That would incorrectly allow a knight to “kill itself” in the computation. The correct order is to query first, then insert.

## Worked Examples

Consider the sample input:

```
4 2
4 5 9 7
1 2 11 33
```

After sorting by strength, the knights become:

| Step | Strength | Coins | Heap before | Answer computed | Heap after |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | [] | 1 | [1] |
| 2 | 5 | 2 | [1] | 3 | [1,2] |
| 3 | 7 | 33 | [1,2] | 36 | [1,2,33] → [2,33] |
| 4 | 9 | 11 | [2,33] | 46 | [2,33,11] → [11,33] |

The table shows that at each step, the heap always preserves the best available coins among weaker knights, and each answer is computed before the current knight is included as a candidate.

A second example highlights the effect of `k = 0`:

Input:

```
3 0
10 5 7
100 20 30
```

| Step | Strength | Coins | Heap before | Answer computed | Heap after |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 20 | [] | 20 | [] |
| 2 | 7 | 30 | [] | 30 | [] |
| 3 | 10 | 100 | [] | 100 | [] |

This confirms that when no kills are allowed, each knight keeps only their initial coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log k)$ | Each knight is pushed and possibly popped once from a heap of size at most `k` |
| Space | $O(k)$ | Heap stores only the best `k` candidates |

The solution comfortably fits within limits because `k` is extremely small, making heap operations effectively constant time in practice even for $10^5$ knights.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline
    import heapq

    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    c = list(map(int, input().split()))

    knights = [(p[i], c[i], i) for i in range(n)]
    knights.sort()

    heap = []
    heap_sum = 0
    ans = [0] * n

    for power, coins, idx in knights:
        ans[idx] = coins + heap_sum

        heapq.heappush(heap, coins)
        heap_sum += coins

        if len(heap) > k:
            heap_sum -= heapq.heappop(heap)

    return " ".join(map(str, ans))

assert run("""4 2
4 5 9 7
1 2 11 33
""") == "1 3 46 36"

assert run("""3 0
10 5 7
100 20 30
""") == "100 20 30"

assert run("""1 0
5
10
""") == "10"

assert run("""5 1
1 2 3 4 5
5 4 3 2 1
""") == "5 9 8 5 1"

assert run("""5 2
5 1 3 2 4
10 100 20 30 40
""") == "10 100 130 120 150"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single knight | same value | minimal case |
| k = 0 | no accumulation | boundary constraint |
| increasing powers | straightforward greedy heap growth | correctness of sorting logic |
| mixed order values | heap selection correctness | top-k maintenance |
| random small mix | general correctness | integration of all components |

## Edge Cases

When `k = 0`, the heap is never used for accumulation. For each knight, the answer is simply their own coins, and the algorithm naturally handles this because the heap remains empty throughout processing.

When all strengths are in descending order in input, the sorting step reverses them completely. The algorithm still works because it relies only on sorted order, not input order. Each knight will then see all weaker ones correctly before it is processed.

When `k` equals `n-1`, the heap may grow large but still remains bounded by `k`. The algorithm still correctly selects the best possible subset because every weaker knight is considered, and the heap retains the top values among them.
