---
title: "CF 125C - Hobbits' Party"
description: "We have n hobbits and want to create as many party days as possible. Each day corresponds to a guest list, which is some non-empty subset of the hobbits. The guest lists must satisfy two conditions."
date: "2026-06-02T16:16:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "C"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 1600
weight: 125
solve_time_s: 137
verified: true
draft: false
---

[CF 125C - Hobbits' Party](https://codeforces.com/problemset/problem/125/C)

**Rating:** 1600  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` hobbits and want to create as many party days as possible.

Each day corresponds to a guest list, which is some non-empty subset of the hobbits.

The guest lists must satisfy two conditions.

For every pair of different days, there must be at least one hobbit invited to both days. In set terminology, every two guest lists must intersect.

For every triple of different days, there must not exist a hobbit invited to all three days. A hobbit may appear on one day or two days, but never on three or more days.

The input contains only `n`, the number of available hobbits. We must maximize the number of days `k`, then output one valid guest list for each day.

The constraint `n ≤ 10000` is small enough that output size becomes the real limitation. Any accepted construction must produce at most about ten thousand hobbits in total. A solution with `O(n²)` memory would be impossible because `10000² = 10^8` elements. A solution with roughly `O(n)` work and output is perfectly fine.

The tricky part is that the problem asks for the maximum possible number of days, not merely a valid schedule.

Consider `n = 3`. A careless construction might create only two days:

```
1 2
2 3
```

This satisfies the conditions, but it is not maximal. The correct answer has three days:

```
1 2
1 3
2 3
```

Another easy mistake is allowing one hobbit to appear in three days. For example:

```
Day 1: {1,2}
Day 2: {1,3}
Day 3: {1,4}
```

Every pair of days intersects, but hobbit `1` belongs to all three days, violating the second condition.

A different pitfall is forgetting that every pair of days must intersect. For example:

```
Day 1: {1,2}
Day 2: {2,3}
Day 3: {3,4}
```

Days 1 and 3 are disjoint, so the construction is invalid.

The challenge is to understand the strongest possible upper bound on the number of days and then build a schedule achieving it.

## Approaches

A brute-force mindset starts by viewing each day as an arbitrary subset of hobbits. We could try different collections of subsets and check the two conditions. Verifying one candidate requires examining all pairs and triples of days. Even if we somehow restricted ourselves to only a few hundred days, the search space of subsets is exponential in `n`, making this completely infeasible.

The key observation comes from looking at a single hobbit.

Because no hobbit may attend three different days, each hobbit can belong to at most two days.

Suppose a hobbit belongs to exactly two days, say days `A` and `B`. Then that hobbit can be thought of as representing the pair `(A,B)`.

Now consider the first condition. Every pair of days must have a common hobbit. Since a hobbit cannot belong to three days, one hobbit can witness the intersection of only one pair of days. It cannot simultaneously serve as the common guest for two different pairs.

If there are `k` days, the number of day pairs is

$$\binom{k}{2}.$$

Each pair needs at least one dedicated hobbit. Since there are only `n` hobbits,

$$\binom{k}{2} \le n.$$

This immediately gives an upper bound on `k`.

The next question is whether this bound is achievable.

It is. Take `k` days. For every pair of days `(i,j)`, create one hobbit invited exactly to those two days. Then every pair of days intersects because of that hobbit, and no hobbit belongs to three days because each one was assigned to exactly one pair.

This construction uses exactly

$$\binom{k}{2}$$

hobbits.

If `n` is larger, the remaining hobbits are unused. The statement only requires guest lists to be non-empty subsets of the inhabitants, not that every hobbit must appear.

Thus the entire problem reduces to finding the largest integer `k` satisfying

$$\binom{k}{2} \le n.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Construction | O(k²) | O(k²) | Accepted |

Since `k` is roughly `√(2n)`, for `n = 10000` we get `k ≤ 141`, making `k²` tiny.

## Algorithm Walkthrough

1. Find the largest integer `k` such that `k(k-1)/2 ≤ n`.
2. Create `k` empty guest lists.
3. Number hobbits starting from `1`.
4. For every pair of days `(i,j)` with `i < j`, create a new hobbit and add it to both day `i` and day `j`.

This hobbit becomes the unique witness that those two days intersect.
5. After processing all pairs, exactly `k(k-1)/2` hobbits have been used.
6. Output `k`.
7. Output each guest list.

### Why it works

There are `k(k-1)/2` pairs of days. The construction assigns one distinct hobbit to every pair.

Take any two different days. Their corresponding pair received a hobbit that appears in exactly those two days, so the days intersect.

Take any hobbit. It was created for one specific pair of days and inserted into exactly those two guest lists. Hence no hobbit appears in three different days.

The construction uses exactly `k(k-1)/2` hobbits. Since `k` was chosen as the largest value satisfying `k(k-1)/2 ≤ n`, any schedule with more than `k` days would require more than `n` hobbits, contradicting the counting argument. Thus the number of days is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    k = 1
    while (k + 1) * k // 2 <= n:
        k += 1

    groups = [[] for _ in range(k)]

    cur = 1
    for i in range(k):
        for j in range(i + 1, k):
            groups[i].append(cur)
            groups[j].append(cur)
            cur += 1

    print(k)
    for g in groups:
        print(*g)

solve()
```

The first loop finds the largest feasible number of days. Since `k` never exceeds about 141, even a simple linear search is sufficient.

The array `groups[i]` stores the guest list of day `i`.

The nested loops iterate over every unordered pair of days. For each pair, a fresh hobbit identifier is created and inserted into both corresponding guest lists. No identifier is ever reused.

A common mistake is to continue assigning hobbits until reaching exactly `n`. That is unnecessary. The proof only requires at most `n` hobbits. Unused hobbits are allowed.

Another subtle point is indexing. Days are stored with zero-based indices in the program, but hobbit labels start from `1` because the statement numbers inhabitants from `1` to `n`.

## Worked Examples

### Example 1

Input:

```
4
```

The largest `k` satisfying `k(k-1)/2 ≤ 4` is `3`.

| Pair of days | Assigned hobbit |
| --- | --- |
| (1,2) | 1 |
| (1,3) | 2 |
| (2,3) | 3 |

Resulting guest lists:

| Day | Guests |
| --- | --- |
| 1 | 1 2 |
| 2 | 1 3 |
| 3 | 2 3 |

Output:

```
3
1 2
1 3
2 3
```

Every pair of days shares exactly one hobbit, and no hobbit appears in three days.

### Example 2

Input:

```
6
```

The largest valid value is `k = 4` because:

$$\binom{4}{2}=6.$$

| Pair of days | Assigned hobbit |
| --- | --- |
| (1,2) | 1 |
| (1,3) | 2 |
| (1,4) | 3 |
| (2,3) | 4 |
| (2,4) | 5 |
| (3,4) | 6 |

Guest lists become:

| Day | Guests |
| --- | --- |
| 1 | 1 2 3 |
| 2 | 1 4 5 |
| 3 | 2 4 6 |
| 4 | 3 5 6 |

This trace shows the central invariant: every pair of days receives a unique shared hobbit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k²) | One iteration for every pair of days |
| Space | O(k²) | Stores all assigned hobbits in guest lists |
| Output Size | O(k²) | Exactly `k(k-1)` printed guest appearances |

Since `k` is the largest integer with `k(k-1)/2 ≤ n`, we have `k = O(√n)`. For `n = 10000`, `k ≤ 141`, so fewer than twenty thousand guest appearances are stored and printed. This easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())

    k = 1
    while (k + 1) * k // 2 <= n:
        k += 1

    groups = [[] for _ in range(k)]

    cur = 1
    for i in range(k):
        for j in range(i + 1, k):
            groups[i].append(cur)
            groups[j].append(cur)
            cur += 1

    out = [str(k)]
    for g in groups:
        out.append(" ".join(map(str, g)))

    return "\n".join(out)

# sample
assert run("4\n").splitlines()[0] == "3"

# minimum n
assert run("3\n").splitlines()[0] == "3"

# exact triangular number
assert run("6\n").splitlines()[0] == "4"

# just below next triangular number
assert run("9\n").splitlines()[0] == "4"

# maximum constraint
assert run("10000\n").splitlines()[0] == "141"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | first line `3` | Minimum allowed input |
| `6` | first line `4` | Exact triangular number |
| `9` | first line `4` | Largest feasible `k` chosen correctly |
| `10000` | first line `141` | Upper constraint handling |

## Edge Cases

Consider the minimum input:

```
3
```

The algorithm finds `k = 3` because `3·2/2 = 3`. The three pairs of days receive hobbits `1`, `2`, and `3`. Each day gets exactly two guests. The construction remains valid even at the smallest boundary.

Consider:

```
5
```

We still obtain `k = 3` because `4·3/2 = 6 > 5`. The algorithm uses only three hobbits although five exist. This demonstrates that unused hobbits are harmless. The problem never requires every inhabitant to appear.

Consider a value exactly equal to a triangular number:

```
10
```

The algorithm finds `k = 5` because `5·4/2 = 10`. Every available hobbit is used, one per pair of days. This is the tightest possible case where the counting upper bound is reached exactly.

Consider a value just below the next triangular number:

```
9
```

A common off-by-one bug would incorrectly choose `k = 5`, but that would require ten pair-witness hobbits. The algorithm correctly keeps `k = 4` because `10 > 9`. The maximality proof guarantees that five days are impossible.
