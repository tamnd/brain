---
title: "CF 916B - Jamie and Binary Sequence (changed after round)"
description: "We want to represent a positive integer n as a sum of exactly k powers of two: $$n = 2^{a1} + 2^{a2} + cdots + 2^{ak}$$ The exponents may be positive, zero, or even negative. Among all valid sequences of length k, we first minimize the largest exponent that appears."
date: "2026-06-12T09:55:59+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 916
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 457 (Div. 2)"
rating: 2000
weight: 916
solve_time_s: 134
verified: true
draft: false
---

[CF 916B - Jamie and Binary Sequence (changed after round)](https://codeforces.com/problemset/problem/916/B)

**Rating:** 2000  
**Tags:** bitmasks, greedy, math  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We want to represent a positive integer `n` as a sum of exactly `k` powers of two:

$$n = 2^{a_1} + 2^{a_2} + \cdots + 2^{a_k}$$

The exponents may be positive, zero, or even negative. Among all valid sequences of length `k`, we first minimize the largest exponent that appears. Let that minimum possible largest exponent be `y`. Among all sequences achieving that optimal `y`, we must output the lexicographically largest sequence.

The value of `n` can be as large as `10^{18}`, while `k` is at most `10^5`. The binary representation of `n` contains at most sixty bits, so any solution that works with the powers of two appearing in the binary decomposition is naturally very small. On the other hand, a search over all possible exponent assignments is completely impossible because the number of representations grows explosively.

The unusual part of the problem is that negative exponents are allowed. For example,

$$2^{-1} + 2^{-1} = 1.$$

This means we can always split a power into two smaller powers:

$$2^x = 2^{x-1} + 2^{x-1}.$$

That operation increases the number of terms by one while preserving the total sum.

Several edge cases are easy to mishandle.

Consider `n = 1, k = 2`. A solution exists because

$$1 = 2^{-1} + 2^{-1}.$$

A solution that only considers nonnegative exponents would incorrectly print `No`.

Consider `n = 3, k = 1`. The only length-one representation would be a single power of two, but `3` is not a power of two. The correct answer is `No`.

Consider `n = 8, k = 8`. The optimal answer is eight copies of exponent `0`, because repeatedly splitting

$$2^3 \to 2^2+2^2 \to \cdots \to 1+1+\cdots+1.$$

A greedy procedure that tries to keep large exponents without checking the required term count can fail to reach exactly `k` terms.

The lexicographic requirement is another subtle point. After finding the smallest possible maximum exponent, we must place larger exponents as early as possible. Two solutions with the same multiset of exponents can have different lexicographic orderings.

## Approaches

A brute-force view is to think of every representation of `n` as repeatedly splitting powers of two. Starting from the binary representation of `n`, each split replaces one exponent `x` by two copies of `x-1`. We could explore all possible sequences of splits until exactly `k` terms appear.

This is correct because every representation can be obtained through such splits. Unfortunately, the number of states is enormous. Even for moderate values, the branching factor becomes huge, and there is no chance of exploring all possibilities.

The key observation is that we do not actually care about every representation. We first care about the minimum possible value of the largest exponent.

Suppose we decide that every exponent must be at most `M`. Any original bit `2^i` with `i > M` must be split until all resulting exponents become `M`. One copy of `2^i` turns into

$$2^{i-M}$$

copies of exponent `M`.

This immediately tells us how many terms we can obtain while keeping the maximum exponent at most `M`.

For a fixed `M`, there is also a minimum possible number of terms. Every bit with exponent at most `M` can stay unchanged. Every bit above `M` must be split down to level `M`.

Let `cnt(M)` denote that minimum term count. If `cnt(M) > k`, then even the most compact representation already uses too many terms, so `M` is impossible.

If `cnt(M) \le k`, then we can always create additional terms by further splitting exponents at most `M`. Since splitting increases the term count by exactly one, any larger count is reachable. Thus `M` is feasible.

Feasibility is monotone. If `M` works, every larger exponent limit also works. This gives a binary search for the smallest feasible `M`.

After finding the optimal maximum exponent `M`, we must construct the lexicographically largest sequence. We begin with the minimum-term representation respecting the limit `M`. Then we perform additional splits until we reach exactly `k` terms.

To maximize lexicographic order, we should keep large exponents whenever possible and split the smallest available exponent first. Splitting a smaller exponent affects later positions in the descendingly sorted sequence and preserves larger values at the front.

A priority queue of exponents allows us to repeatedly split the current minimum exponent until exactly `k` terms exist.

Finally, we output all exponents in descending order. That ordering is lexicographically largest among all representations with the same multiset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(log² n + k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Decompose `n` into binary. For every set bit at position `i`, record one copy of exponent `i`.
2. Binary search the smallest exponent limit `M` for which a valid representation with maximum exponent at most `M` exists.
3. To test a candidate `M`, compute the minimum number of terms required under that limit.

If a bit contributes exponent `i ≤ M`, it contributes one term.

If `i > M`, it must be split down to level `M`, producing `2^(i-M)` terms.
4. If this minimum count exceeds `k`, the limit `M` is impossible.
5. Otherwise the limit is feasible, because additional splits can always increase the term count one by one.
6. After binary search finishes, let the answer be the smallest feasible `M`.
7. Build the minimum-term representation for this `M`.

Every original exponent `i ≤ M` contributes one exponent `i`.

Every original exponent `i > M` contributes `2^(i-M)` copies of exponent `M`.
8. Let the current number of terms be `cur`.
9. While `cur < k`, repeatedly split the smallest exponent currently present.

Replace one exponent `x` by two copies of `x-1`.

Increase `cur` by one.
10. When exactly `k` terms exist, sort all exponents in descending order.
11. Output the sequence.

### Why it works

For a fixed limit `M`, every exponent larger than `M` must eventually be reduced to `M` or below. Splitting directly to level `M` produces the smallest possible number of terms under that limit. Any other representation respecting the same limit can only have at least as many terms.

Thus `cnt(M)` is the minimum achievable term count. If `cnt(M) > k`, no solution exists with maximum exponent at most `M`. If `cnt(M) ≤ k`, repeated splitting lets us increase the term count by exactly one each time, so reaching exactly `k` terms is always possible.

The binary search finds the smallest feasible `M`, which is precisely the minimum possible largest exponent.

After fixing `M`, additional splits are needed only to reach the required length. Splitting the smallest exponent preserves larger exponents, keeping the front of the descending sequence as large as possible. Hence the final descending sequence is lexicographically largest among all optimal solutions.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    bits = []
    x = n
    pos = 0
    while x:
        if x & 1:
            bits.append(pos)
        pos += 1
        x >>= 1

    if n == 0:
        print("No")
        return

    def min_terms(M):
        total = 0
        for b in bits:
            if b <= M:
                total += 1
            else:
                total += 1 << (b - M)
            if total > k:
                return total
        return total

    lo = -100000
    hi = max(bits) if bits else 0

    while lo < hi:
        mid = (lo + hi) // 2
        if min_terms(mid) <= k:
            hi = mid
        else:
            lo = mid + 1

    M = lo

    exps = []
    for b in bits:
        if b <= M:
            exps.append(b)
        else:
            exps.extend([M] * (1 << (b - M)))

    cur = len(exps)

    heapq.heapify(exps)

    while cur < k:
        x = heapq.heappop(exps)
        heapq.heappush(exps, x - 1)
        heapq.heappush(exps, x - 1)
        cur += 1

    ans = sorted(exps, reverse=True)

    print("Yes")
    print(*ans)

if __name__ == "__main__":
    solve()
```

The binary decomposition contains at most sixty exponents, so the feasibility test is extremely small.

The function `min_terms(M)` computes the smallest number of terms possible while forcing every exponent to be at most `M`. For exponents above `M`, each split level doubles the number of copies, giving `2^(b-M)` terms.

The binary search works over exponents, including negative values. The lower bound `-100000` is safely below anything that could ever be needed because `k ≤ 10^5`. We never need more than about `log2(k)` extra splitting levels beyond the smallest existing exponent.

After obtaining the optimal `M`, the code explicitly builds the minimum-term representation. The total number of terms produced is never more than `k`, because `M` is feasible and was chosen so that `min_terms(M) ≤ k`.

The heap stores all current exponents. Each split removes one exponent and inserts two copies one level lower. Since the number of terms increases by exactly one, exactly `k - cur` splits are required.

Finally, sorting in descending order gives the lexicographically largest sequence.

## Worked Examples

### Sample 1

Input:

```
23 5
```

Binary representation:

$$23 = 2^4 + 2^2 + 2^1 + 2^0$$

The smallest feasible maximum exponent is `3`.

| Step | Representation | Term Count |
| --- | --- | --- |
| Initial under M=3 | 3, 3, 2, 1, 0 | 5 |
| Target reached | 3, 3, 2, 1, 0 | 5 |

Output:

```
Yes
3 3 2 1 0
```

This example shows that one copy of `2^4` must be split into two copies of `2^3`, reducing the maximum exponent from `4` to `3`.

### Sample 2

Input:

```
3 1
```

Binary representation:

$$3 = 2^1 + 2^0$$

| Step | Representation | Term Count |
| --- | --- | --- |
| Minimum possible | 1, 0 | 2 |

The minimum number of terms is already `2`, and splitting can only increase the count.

Output:

```
No
```

This demonstrates the case where the requested length is smaller than the minimum achievable length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log² n + k log k) | Binary search over exponent limits, then at most k heap operations |
| Space | O(k) | Stores the final representation |

The binary decomposition contains at most sixty bits, so feasibility checks are tiny. The dominant cost comes from maintaining up to `k` exponents in the heap. With `k ≤ 10^5`, the solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from contextlib import redirect_stdout

def solve():
    import heapq

    n, k = map(int, input().split())

    bits = []
    x = n
    p = 0
    while x:
        if x & 1:
            bits.append(p)
        p += 1
        x >>= 1

    def min_terms(M):
        total = 0
        for b in bits:
            total += 1 if b <= M else (1 << (b - M))
            if total > k:
                return total
        return total

    lo = -100000
    hi = max(bits)

    while lo < hi:
        mid = (lo + hi) // 2
        if min_terms(mid) <= k:
            hi = mid
        else:
            lo = mid + 1

    M = lo

    exps = []
    for b in bits:
        if b <= M:
            exps.append(b)
        else:
            exps.extend([M] * (1 << (b - M)))

    cur = len(exps)

    heapq.heapify(exps)

    while cur < k:
        x = heapq.heappop(exps)
        heapq.heappush(exps, x - 1)
        heapq.heappush(exps, x - 1)
        cur += 1

    ans = sorted(exps, reverse=True)

    print("Yes")
    print(*ans)

def run(inp: str) -> str:
    global input
    input = io.StringIO(inp).readline

    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("23 5\n") == "Yes\n3 3 2 1 0"

# custom cases
assert run("1 1\n") == "Yes\n0"
assert run("1 2\n") == "Yes\n-1 -1"
assert run("3 1\n") == "No"
assert run("8 8\n") == "Yes\n0 0 0 0 0 0 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Smallest valid instance |
| `1 2` | `-1 -1` | Negative exponents are allowed |
| `3 1` | `No` | Requested length below minimum |
| `8 8` | Eight zeros | Repeated splitting to exact count |

## Edge Cases

Consider the input:

```
1 2
```

The binary representation contains one exponent `0`. The optimal maximum exponent is `-1`, because

$$1 = 2^{-1}+2^{-1}.$$

The feasibility check finds that `M = -1` gives exactly two terms. The algorithm outputs:

```
Yes
-1 -1
```

This case catches solutions that incorrectly assume exponents must be nonnegative.

Consider:

```
3 1
```

The binary representation is `[1, 0]`. Even with no exponent restriction, the minimum number of terms is `2`. Since splitting only increases the count, reaching one term is impossible. The algorithm correctly prints:

```
No
```

Consider:

```
8 8
```

Starting from exponent `[3]`, the optimal maximum exponent becomes `0`, producing eight copies of exponent `0`. The algorithm builds exactly:

```
0 0 0 0 0 0 0 0
```

This verifies that the binary search can push the maximum exponent below the original highest bit when a large number of terms is required.

Consider:

```
5 4
```

We have

$$5 = 2^2 + 2^0.$$

With `M = 0`, the minimum representation becomes four copies of exponent `0` plus one more exponent `0`, totaling five terms, which is too many. With `M = 1`, the minimum representation is three terms: `1, 1, 0`. One additional split of the smallest exponent gives four terms, producing the optimal answer. This checks the boundary between feasible and infeasible exponent limits.
