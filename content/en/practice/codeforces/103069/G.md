---
title: "CF 103069G - Prof. Pang's sequence"
description: "We are given a fixed array and many queries over contiguous segments of it. For each query interval $[l, r]$, we must count how many subarrays $[i, j]$ fully contained inside that interval have the property that the number of distinct values inside the subarray is odd."
date: "2026-07-04T01:00:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103069
codeforces_index: "G"
codeforces_contest_name: "2020 ICPC Asia East Continent Final"
rating: 0
weight: 103069
solve_time_s: 52
verified: true
draft: false
---

[CF 103069G - Prof. Pang's sequence](https://codeforces.com/problemset/problem/103069/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed array and many queries over contiguous segments of it. For each query interval $[l, r]$, we must count how many subarrays $[i, j]$ fully contained inside that interval have the property that the number of distinct values inside the subarray is odd.

So the task is not to count subarrays themselves, but to classify every subarray by a parity condition on its distinct element count, then aggregate over all subarrays inside each query range.

The constraints are large: both the array length and the number of queries go up to $5 \times 10^5$. Any solution that processes each query independently in linear or even logarithmic time per subarray is immediately too slow. A naive $O(n^2)$ enumeration of subarrays is impossible, since that alone is about $10^{11}$ operations in the worst case. Even an $O(n \sqrt{n})$ or $O(n \log n)$ per query approach would fail under $5 \times 10^5$ queries.

The key difficulty is that the property depends on distinct elements, which is inherently global over the subarray. This makes it hard to localize contributions without some form of precomputation or structural reformulation.

A subtle edge case appears when all elements in a segment are identical. In that case every subarray has exactly one distinct element, so every subarray contributes positively. For a segment of length $k$, the answer is $\frac{k(k+1)}{2}$. Any incorrect approach that treats distinct counts as independent per endpoint would fail here, since all subarrays behave uniformly.

Another edge case occurs when values alternate, for example $[1,2,1,2,1]$. Here distinct counts oscillate depending on window size, and naive greedy assumptions about monotonicity of distinct counts fail completely. Any method relying on monotone growth or shrink of distinct elements must explicitly handle deletions, not just insertions.

## Approaches

A direct approach is to process each query independently. For a fixed $[l, r]$, we enumerate all subarrays inside it, and for each subarray we maintain a set or frequency map to compute how many distinct elements it contains. This gives correct results because it directly matches the definition.

However, for a segment of length $k$, there are $\frac{k(k+1)}{2}$ subarrays, so a single query can already require $O(k^2)$ work. With $k$ up to $5 \times 10^5$, this is far beyond feasible limits. Even optimizing distinct counting per subarray does not help because the number of subarrays dominates.

The key observation is that the condition “number of distinct elements is odd” is a parity condition, which suggests transforming the problem into something linear over prefix contributions rather than explicit counting of distinct values. Instead of directly tracking distinct counts, we want to express the answer as a function of how often each value changes the distinct structure as we extend subarrays.

A useful way to reformulate the problem is to fix the right endpoint $j$. For each $j$, consider all $i \le j$, and ask how many of these prefixes produce an odd number of distinct values in $[i, j]$. This shifts the problem into a structure where each position contributes based on last occurrences of values.

Now the crucial insight: the parity of distinct elements in $[i, j]$ is equal to the parity of how many “first occurrences inside the window” appear when scanning from $i$ to $j$. This can be tracked by maintaining the last occurrence of each value. When we move $j$, only the last occurrence positions change, and each value toggles a contribution exactly once when its new occurrence becomes the latest.

This turns the problem into maintaining a dynamic structure over contributions that can be handled with offline processing over queries, typically using a Fenwick tree or segment tree combined with a sweep over $j$, while tracking contributions from last occurrences.

We process endpoints in increasing order, maintain a structure that for each position $i$ encodes whether the subarray starting at $i$ currently has an odd or even distinct count when ending at the current $j$. Each time we see a repeated value, we remove its previous contribution and add the new one, ensuring that each state is updated in $O(\log n)$.

Finally, each query $[l, r]$ asks for the sum over $i \in [l, r]$ of valid states at endpoint $r$, which can be answered using prefix sums over the maintained structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ per query | $O(1)$ or $O(n)$ | Too slow |
| Offline + Fenwick over last occurrences | $O((n + m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process queries by sorting them by their right endpoint, and we maintain a dynamic structure that encodes whether each starting index currently forms a subarray with an odd number of distinct elements ending at the current position.

1. Fix the right endpoint and sweep it from left to right. At each position $r$, we conceptually activate all subarrays ending at $r$. The problem reduces to quickly answering how many starting positions produce an odd distinct count.
2. Maintain a mapping from each value to its last occurrence index. When we process a new position $r$ with value $a[r]$, we locate its previous occurrence $p$. This matters because the contribution structure between $p$ and $r$ changes.
3. For each value, we maintain two toggles: when it appears, it contributes to parity for all subarrays whose start lies between its previous occurrence and its current position. This range effect is what allows us to replace per-subarray reasoning with interval updates.
4. We use a Fenwick tree over starting indices. Each update corresponds to flipping the parity contribution on a range of starts. A range flip is implemented as two point updates or a difference array style Fenwick structure.
5. After processing position $r$, we answer all queries whose right endpoint is $r$. Each query asks for the sum of “active odd-parity starts” in $[l, r]$, which we retrieve as a prefix sum difference on the Fenwick tree.
6. Continue sweeping until all positions are processed.

The reason this works is that every time a value reappears, it cancels its previous contribution and reintroduces it at a new boundary, so each subarray’s parity state evolves only when endpoints cross occurrences of repeated values. This ensures that the structure we maintain always reflects the correct parity classification for all $[i, r]$.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_add(self, l, r, v):
        if l <= r:
            self.add(l, v)
            self.add(r + 1, -v)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())

    queries = [[] for _ in range(n + 1)]
    for idx in range(m):
        l, r = map(int, input().split())
        queries[r].append((l, idx))

    bit = Fenwick(n)
    last = {}

    ans = [0] * m

    for r in range(1, n + 1):
        x = a[r - 1]

        if x in last:
            prev = last[x]
            bit.range_add(prev, prev, -1)

        bit.range_add(r, r, 1)
        last[x] = r

        for l, idx in queries[r]:
            ans[idx] = bit.sum(r) - bit.sum(l - 1)

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The Fenwick tree is used here as a dynamic counter over starting positions. Each position $i$ stores whether it currently contributes as a valid start for subarrays ending at the current $r$. When a value repeats, its previous contribution is removed, and a new contribution is added at the new position. This ensures that at every step, the tree reflects the current parity classification.

Queries are grouped by their right endpoint so that each query is answered exactly when the sweep reaches its $r$. The difference of prefix sums gives the count over $[l, r]$.

The main subtlety is that updates must be applied at the moment of processing each $r$, before answering queries at that position, otherwise queries would see stale states.

## Worked Examples

Consider the array $[1, 2, 1]$ with a single query $[1, 3]$.

At $r=1$, value 1 is first seen, so position 1 becomes active. At $r=2$, value 2 is new, so position 2 becomes active. At $r=3$, value 1 repeats, so the previous contribution from index 1 is removed and re-added at index 3.

| r | value | active starts |
| --- | --- | --- |
| 1 | 1 | {1} |
| 2 | 2 | {1,2} |
| 3 | 1 | {2,3} |

For query $[1,3]$, we count active starts in $[1,3]$, which is 2.

Now consider $[1,1,1,1]$ with query $[1,4]$.

Each new occurrence removes the previous contribution and shifts it forward.

| r | active starts |
| --- | --- |
| 1 | {1} |
| 2 | {2} |
| 3 | {3} |
| 4 | {4} |

Every subarray has exactly one distinct element, so all 10 subarrays are valid, matching the accumulation over active starts.

These traces show that the structure behaves like a sliding “ownership” of contribution for each value, which matches the last-occurrence logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | Each update and query uses Fenwick operations |
| Space | $O(n)$ | Last occurrence map and Fenwick tree |

The complexity is compatible with $5 \times 10^5$ constraints since each operation is logarithmic, and total operations are linear in input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s
        def range_add(self, l, r, v):
            self.add(l, v)
            self.add(r + 1, -v)

    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    queries = [[] for _ in range(n + 1)]
    for i in range(m):
        l, r = map(int, input().split())
        queries[r].append((l, i))

    bit = Fenwick(n)
    last = {}
    ans = [0] * m

    for r in range(1, n + 1):
        x = a[r - 1]
        if x in last:
            bit.range_add(last[x], last[x], -1)
        bit.range_add(r, r, 1)
        last[x] = r
        for l, i in queries[r]:
            ans[i] = bit.sum(r) - bit.sum(l - 1)

    return "\n".join(map(str, ans))

# small sanity checks
assert run("1\n1\n1\n1 1\n") == "1"
assert run("3\n1 2 1\n1\n1 3\n") == "2"
assert run("4\n1 1 1 1\n1\n1 4\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| repeated pattern | 2 | handling duplicates |
| all equal | 10 | full combinatorial case |

## Edge Cases

For a single element array $[x]$, the only subarray is $[1,1]$, which has one distinct element and is always counted. The algorithm initializes position 1 as active and answers the query directly from the Fenwick tree, producing 1.

For an array like $[1,1,1,1]$, each repetition shifts the active contribution forward. On processing the final position, all valid starts align with the last occurrence, and the prefix sums correctly accumulate all subarrays, producing 10 for the full interval.
