---
title: "CF 104782J - Parallelogram"
description: "We are given several test cases. In each test case there is a collection of stick lengths. From this collection we want to know whether we can pick four distinct sticks such that, after freely rotating and rearranging them in the plane, they can form a parallelogram using all…"
date: "2026-06-28T15:04:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104782
codeforces_index: "J"
codeforces_contest_name: "2023 Romanian Collegiate Programming Contest (RCPC)"
rating: 0
weight: 104782
solve_time_s: 56
verified: true
draft: false
---

[CF 104782J - Parallelogram](https://codeforces.com/problemset/problem/104782/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case there is a collection of stick lengths. From this collection we want to know whether we can pick four distinct sticks such that, after freely rotating and rearranging them in the plane, they can form a parallelogram using all four sticks as its sides.

A parallelogram has two pairs of equal opposite sides. So among the four chosen stick lengths, we must be able to pair them into two equal pairs. In other words, if we sort the chosen four values, they must look like $x, x, y, y$ for some positive lengths $x$ and $y$. The order of selection in the input does not matter beyond distinct indices.

The input size is large: the total number of sticks across all test cases can reach $2 \cdot 10^5$, and there are up to $10^4$ test cases. This immediately rules out any solution that tries to check all quadruples explicitly, since even a single test case with $n = 2 \cdot 10^5$ would make $O(n^4)$ or $O(n^3)$ impossible.

The key constraint is that stick lengths are bounded by $n$, which suggests frequency-based reasoning is possible in linear or near-linear time per test case.

A subtle edge case appears when many values are identical. For example, if all sticks are equal like $[1, 1, 1, 1]$, the answer is clearly YES because we can form a parallelogram with all sides equal, which is a special case. Another edge case is when there are exactly two different values but not enough repetitions, like $[1, 1, 2, 3]$, where we might have a pair but cannot form two full pairs.

A naive mistake is to think “any two pairs anywhere in the array are enough,” without ensuring distinct indices. For example, if values are $[1, 1, 2]$, we might mistakenly think we can form two pairs because there is a pair of 1s, but we still need another pair, which does not exist.

## Approaches

A brute-force approach would try all quadruples $i < j < k < p$, check the four values, and test whether they can be partitioned into two equal pairs. This is correct, because it exhaustively tries every possible selection of four sticks. However, the number of quadruples is $\binom{n}{4}$, which grows as $O(n^4)$. Even for $n = 2000$, this is already too slow, and here $n$ is up to $2 \cdot 10^5$, making it completely infeasible.

The structure of the condition is what simplifies the problem. We do not care about which indices form the pairs beyond ensuring distinctness. The only thing that matters is whether there exist at least two distinct values each appearing at least twice. If we have a value appearing four times, that also works because it can form two pairs of equal lengths. If we have two different values each appearing at least twice, we can assign one pair to each value.

So the problem reduces to a frequency question: we need to check whether there exist at least two pairs of equal values, counting multiplicity carefully. One value with frequency at least four already contributes two pairs, and two values with frequency at least two each also suffice.

This reduces the problem to scanning frequencies and counting how many disjoint pairs we can extract.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^4)$ | $O(1)$ | Too slow |
| Frequency counting | $O(n)$ per test | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into counting how many pairs of equal values exist in the multiset of stick lengths.

1. Count the frequency of each stick length using a hash map or array.

This step is necessary because the pairing condition depends only on how many copies of each value exist, not their positions.
2. For each distinct value with frequency $f$, compute how many disjoint pairs it contributes as $f // 2$.

This captures the maximum number of pairs we can form from that value without reusing elements.
3. Sum these pair counts across all values.

The total represents how many equal-length pairs we can form overall.
4. If the total number of pairs is at least 2, print YES. Otherwise, print NO.

We need at least two pairs because a parallelogram requires two opposite sides of one length and two opposite sides of another length.

### Why it works

Any valid selection of four sticks that forms a parallelogram must partition into two equal pairs. Each pair must come from identical values, so every valid solution corresponds to choosing two disjoint pairs from the frequency multiset. Conversely, if we can extract two disjoint pairs from the multiset, we can assign them as opposite sides of a parallelogram. No geometric constraints beyond equality of opposite sides affect feasibility because rotation and rearrangement are allowed.

Thus, the problem is exactly equivalent to checking whether the total number of available equal pairs is at least two.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        pairs = 0
        for v in freq.values():
            pairs += v // 2

        if pairs >= 2:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution is built around a direct frequency aggregation. The dictionary accumulates counts in linear time. The second pass converts each frequency into the number of usable pairs by integer division. This avoids any need to track actual indices or combinations explicitly.

A common implementation pitfall is forgetting that a single value with frequency 4 contributes two pairs, which is why `v // 2` is essential rather than checking only whether `v >= 2`.

## Worked Examples

### Example 1

Input:

```
1
4
1 2 2 3
```

| Step | Frequency Map | Pair Contribution | Total Pairs |
| --- | --- | --- | --- |
| Start | {} | 0 | 0 |
| After scan | {1:1, 2:2, 3:1} | 1 (from 2) | 1 |

We end with only one usable pair (two 2s). Since a parallelogram requires two pairs, the answer is NO.

### Example 2

Input:

```
1
5
1 1 2 2 3
```

| Step | Frequency Map | Pair Contribution | Total Pairs |
| --- | --- | --- | --- |
| Start | {} | 0 | 0 |
| After scan | {1:2, 2:2, 3:1} | 2 | 2 |

We can form one pair from 1s and one pair from 2s, giving two disjoint pairs. This satisfies the condition, so the answer is YES.

These examples show that the condition depends only on aggregated multiplicity, not on how values are interleaved in the array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | One pass to count frequencies and one pass over distinct values |
| Space | $O(n)$ | Frequency map stores counts of distinct stick lengths |

The total $n$ across all test cases is bounded by $2 \cdot 10^5$, so this linear solution fits comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        pairs = sum(v // 2 for v in freq.values())
        out.append("YES" if pairs >= 2 else "NO")
    return "\n".join(out)

# provided samples
assert run("1\n4\n1 2 3 3\n") == "NO"
assert run("1\n4\n1 1 1 1\n") == "YES"

# custom cases
assert run("1\n3\n1 1 2\n") == "NO", "only one pair exists"
assert run("1\n4\n1 2 3 4\n") == "NO", "no pairs at all"
assert run("1\n6\n1 1 1 1 2 2\n") == "YES", "one value gives two pairs"
assert run("1\n6\n1 1 2 2 3 3\n") == "YES", "three pairs available"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 2 | NO | insufficient pairs |
| 1 1 1 1 2 2 | YES | single value can supply two pairs |
| 1 1 2 2 3 3 | YES | multiple pair sources |

## Edge Cases

One edge case is when a single value dominates the array. For input like `1 1 1 1`, the frequency is 4, producing two pairs from the same value. The algorithm computes `4 // 2 = 2`, correctly returning YES.

Another case is when pairs exist but are insufficient in count, such as `1 1 2 3`. Here frequencies produce one pair from `1` and zero from others, totaling one. The algorithm correctly rejects it.

A more deceptive case is `1 1 1 2 2`. Frequencies are `1:3` and `2:2`. This yields `1 + 1 = 2` pairs, so the answer is YES even though it may not be obvious visually that four of the sticks can be arranged appropriately. The pairing abstraction ensures correctness without needing to reason geometrically.
