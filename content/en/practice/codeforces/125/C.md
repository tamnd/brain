---
title: "CF 125C - Hobbits' Party"
description: "We need to construct as many party days as possible using exactly n hobbits. Every day has a guest list. The construction must satisfy two conditions. First, every pair of different days must share at least one hobbit."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "C"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 1600
weight: 125
solve_time_s: 125
verified: false
draft: false
---

[CF 125C - Hobbits' Party](https://codeforces.com/problemset/problem/125/C)

**Rating:** 1600  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct as many party days as possible using exactly `n` hobbits. Every day has a guest list.

The construction must satisfy two conditions.

First, every pair of different days must share at least one hobbit. If day A and day B exist, there must be some hobbit invited to both.

Second, no hobbit may appear on three different days. A hobbit can belong to one day or two days, but never three.

The input only gives the number of hobbits. We must output the maximum possible number of days, followed by one guest list for each day.

The limit is only `n ≤ 10000`, so performance is not difficult. Even an `O(n²)` construction is completely safe because `10000² = 10^8` is only near the upper edge in Python, and our actual solution is much smaller. The real challenge is not speed but understanding the combinatorial structure of the constraints.

The key observation comes from interpreting each hobbit by the pair of days they attend.

Because a hobbit cannot appear in three days, every hobbit can connect at most one pair of days. If a hobbit attends days `i` and `j`, then that hobbit is responsible for satisfying the intersection requirement for that pair.

Suppose there are `k` days. There are exactly

$\frac{k(k-1)}{2}$

pairs of days.

Each pair must share at least one hobbit, and one hobbit cannot cover two different pairs because that would require attending at least three days. So we need at least one distinct hobbit per pair of days.

That means:

$\frac{k(k-1)}{2} \le n$

This already gives the upper bound.

A common mistake is trying to reuse the same hobbit for many intersections. For example, with 4 days, someone might try:

```
Day 1: 1
Day 2: 1
Day 3: 1
Day 4: 1
```

Every pair intersects, but hobbit `1` appears in four days, violating the second rule.

Another subtle case happens when `n` is not exactly triangular. For example:

```
n = 5
```

We can make only 3 days, because:

```
3 * 2 / 2 = 3
4 * 3 / 2 = 6
```

We do not have enough hobbits for 4 days. A careless implementation may try to greedily continue constructing days and accidentally exceed the available hobbits.

The minimum input is also interesting:

```
n = 3
```

We can form exactly 3 days:

```
1 2
1 3
2 3
```

Every pair intersects once, and every hobbit appears in exactly two days.

## Approaches

The brute-force way to think about the problem is to search over all possible guest lists and test whether the constraints hold. For every construction, we would verify that every pair of days intersects and that no hobbit belongs to three days.

This becomes hopeless almost immediately because the number of possible subsets grows exponentially. Even for small `n`, the search space explodes.

A more structured brute-force idea is to decide the number of days `k`, then assign hobbits to pairs of days. Since every valid hobbit can belong to at most two days, each hobbit effectively represents either a single day or an edge between two days.

At that point, the problem becomes much clearer.

If there are `k` days, every pair of days must intersect. Since one hobbit can cover only one pair, we need at least one unique hobbit for every pair of days. The minimum number of hobbits needed is exactly the number of edges in a complete graph on `k` vertices:

$\frac{k(k-1)}{2}$

Now the problem reduces to finding the largest `k` satisfying:

$\frac{k(k-1)}{2} \le n$

Once we know `k`, the construction is straightforward.

Treat each day as a vertex. For every pair of days `(i, j)`, create one unique hobbit assigned to exactly those two days. Then every pair intersects, and no hobbit appears in more than two days.

This construction is optimal because we already proved that any valid arrangement with `k` days requires at least `k(k-1)/2` hobbits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(k²) | O(k²) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the number of hobbits.
2. Find the largest integer `k` such that:

$\frac{k(k-1)}{2} \le n$

This is the maximum possible number of days because every pair of days needs its own hobbit.
3. Create `k` empty guest lists.
4. Number the hobbits starting from `1`.
5. For every pair of days `(i, j)` with `i < j`, assign one new hobbit to both days.

This guarantees that day `i` and day `j` intersect.
6. Continue until every pair of days has received a unique hobbit.
7. Output `k`, followed by the guest list for each day.

### Why it works

Each pair of days receives exactly one shared hobbit, so every pair intersects.

Each hobbit is assigned to exactly one pair of days, meaning every hobbit appears in exactly two days and never three.

The construction uses exactly one hobbit per pair of days, so the total number used is:

$\frac{k(k-1)}{2}$

Since `k` was chosen as the largest value satisfying this bound, no larger number of days is possible. The construction is both valid and optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    k = 1
    while (k + 1) * k // 2 <= n:
        k += 1

    days = [[] for _ in range(k)]

    hobbit = 1

    for i in range(k):
        for j in range(i + 1, k):
            days[i].append(hobbit)
            days[j].append(hobbit)
            hobbit += 1

    print(k)
    for guests in days:
        print(*guests)

solve()
```

The first part computes the maximum feasible number of days. The loop keeps increasing `k` while the complete graph requirement still fits within `n`.

The nested loops implement the pair construction directly. Every pair of days gets one unique hobbit. Because the hobbit counter increases after every assignment, no hobbit is reused for another pair.

One subtle detail is the indexing. The days are stored as zero-based lists internally, but the hobbit numbers start from `1` because the output format expects positive integers.

Another easy mistake is forgetting that unused hobbits are allowed. If `n = 5`, the construction for `k = 3` uses only 3 hobbits. The remaining two are irrelevant and do not need to appear anywhere.

## Worked Examples

### Example 1

Input:

```
4
```

We search for the largest `k` such that:

```
k(k-1)/2 ≤ 4
```

`k = 3` works because `3`, but `k = 4` requires `6`.

| Pair of days | Hobbit assigned | Day 1 | Day 2 | Day 3 |
| --- | --- | --- | --- | --- |
| (1,2) | 1 | 1 | 1 |  |
| (1,3) | 2 | 1 2 | 1 | 2 |
| (2,3) | 3 | 1 2 | 1 3 | 2 3 |

Final output:

```
3
1 2
1 3
2 3
```

This trace shows the core invariant. Every pair of days shares exactly one hobbit, and every hobbit appears in exactly two days.

### Example 2

Input:

```
6
```

Now:

```
4 * 3 / 2 = 6
```

So we can build 4 days exactly.

| Pair of days | Hobbit | Day 1 | Day 2 | Day 3 | Day 4 |
| --- | --- | --- | --- | --- | --- |
| (1,2) | 1 | 1 | 1 |  |  |
| (1,3) | 2 | 1 2 | 1 | 2 |  |
| (1,4) | 3 | 1 2 3 | 1 | 2 | 3 |
| (2,3) | 4 | 1 2 3 | 1 4 | 2 4 | 3 |
| (2,4) | 5 | 1 2 3 | 1 4 5 | 2 4 | 3 5 |
| (3,4) | 6 | 1 2 3 | 1 4 5 | 2 4 6 | 3 5 6 |

Output:

```
4
1 2 3
1 4 5
2 4 6
3 5 6
```

This example demonstrates the complete graph interpretation directly. Every edge becomes one hobbit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k²) | We process every pair of days once |
| Space | O(k²) | Total stored hobbit assignments equals the number of pairs |

Since:

$\frac{k(k-1)}{2} \le n$

we have `k = O(sqrt(n))`. With `n ≤ 10000`, the total work is tiny and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    k = 1
    while (k + 1) * k // 2 <= n:
        k += 1

    days = [[] for _ in range(k)]

    hobbit = 1

    for i in range(k):
        for j in range(i + 1, k):
            days[i].append(hobbit)
            days[j].append(hobbit)
            hobbit += 1

    out = [str(k)]
    for guests in days:
        out.append(" ".join(map(str, guests)))

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    solve()

    sys.stdout = old_stdout
    return buf.getvalue().strip()

# provided sample
assert run("4\n") == "3\n1 2\n1 3\n2 3", "sample 1"

# minimum valid input
assert run("3\n") == "3\n1 2\n1 3\n2 3", "minimum case"

# exact triangular number
assert run("6\n") == "4\n1 2 3\n1 4 5\n2 4 6\n3 5 6", "exact complete graph"

# non-triangular number
assert run("5\n") == "3\n1 2\n1 3\n2 3", "unused hobbits allowed"

# larger boundary-style case
res = run("10000\n")
first_line = int(res.splitlines()[0])
assert first_line == 141, "largest k for n=10000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | 3 days | Minimum valid construction |
| `4` | 3 days | Basic pair construction |
| `5` | 3 days | Extra hobbits may remain unused |
| `6` | 4 days | Exact triangular boundary |
| `10000` | 141 days | Large input and upper-bound logic |

## Edge Cases

Consider:

```
5
```

A greedy approach might incorrectly try to construct 4 days because there are still unused hobbits available after creating some intersections. Our algorithm prevents this by checking the theoretical lower bound first.

We compute:

```
4 * 3 / 2 = 6 > 5
```

So 4 days are impossible. The algorithm settles on 3 days and constructs:

```
1 2
1 3
2 3
```

Only 3 hobbits are used, which is completely valid.

Another important edge case is the minimum input:

```
3
```

The algorithm computes:

```
3 * 2 / 2 = 3
```

So exactly 3 days are possible.

The nested loops generate one hobbit for each pair:

```
(1,2) -> hobbit 1
(1,3) -> hobbit 2
(2,3) -> hobbit 3
```

Every pair intersects once, and no hobbit appears three times.

Finally, consider a large triangular number such as:

```
n = 6
```

The algorithm finds:

```
4 * 3 / 2 = 6
```

So the construction uses all hobbits exactly once as pair-connectors. This verifies that the implementation handles the equality boundary correctly and does not stop one step too early.
