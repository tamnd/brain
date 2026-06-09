---
title: "CF 1807D - Odd Queries"
description: "We are given an array of integers and a sequence of queries. Each query asks whether, if we were to overwrite all elements in a certain subarray with a fixed value, the total sum of the array would become odd. The queries do not modify the array permanently."
date: "2026-06-09T09:03:45+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1807
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 859 (Div. 4)"
rating: 900
weight: 1807
solve_time_s: 89
verified: true
draft: false
---

[CF 1807D - Odd Queries](https://codeforces.com/problemset/problem/1807/D)

**Rating:** 900  
**Tags:** data structures, implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a sequence of queries. Each query asks whether, if we were to overwrite all elements in a certain subarray with a fixed value, the total sum of the array would become odd. The queries do not modify the array permanently. For each query, we simply need a "YES" if the sum is odd after the hypothetical overwrite and "NO" if it is even.

The array size $n$ can reach up to 200,000, and the number of queries $q$ can also be 200,000, but the sum of all $n$ and all $q$ across test cases stays under 200,000. This implies we can afford linear work per test case but not per query. An $O(n \cdot q)$ approach is immediately too slow because, in the worst case, it could require $4 \cdot 10^{10}$ operations.

Edge cases to consider include very small arrays, queries that cover the entire array, and queries where the replacement value is very large. For example, if the array is `[2]` and the query asks to set the only element to `1`, the sum becomes `1` which is odd, and the answer is "YES". A naive approach that recalculates the sum of the whole array for every query will work on small arrays but fail on large ones.

Another subtlety is that we only care about **parity**. Large numbers themselves do not need full arithmetic; knowing if they are odd or even is sufficient. A common mistake is to compute the full sum with large numbers, risking overflow or unnecessary computation.

## Approaches

The brute-force approach iterates over the query range, replaces the elements, computes the sum, and checks parity. This works because it exactly simulates the problem. For each query, we could do up to $r - l + 1$ operations, and with 200,000 queries on arrays of size 200,000, this gives a worst-case $O(n \cdot q) = O(4 \cdot 10^{10})$, which is far too slow.

The key insight is that we only need **parity**, not the full sum. Instead of replacing elements, we can calculate the new sum as the old sum minus the sum of the replaced elements plus the sum of the new values. Let the length of the replaced range be $m = r - l + 1$. The parity of the new sum is:

```
new_sum_parity = (old_sum - sum_of_range + m * k) % 2
```

Because only parity matters, subtraction and addition can be done modulo 2. Each element modulo 2 is either 0 or 1. The sum of the original range modulo 2 can be precomputed with a prefix sum array modulo 2. Multiplying the replacement value $k$ by the range length $m$ modulo 2 is simply $0$ if $k$ is even or $m % 2$ if $k$ is odd.

This observation reduces the query processing to $O(1)$ per query after computing the prefix sum of the original array. This works efficiently for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the entire array modulo 2. This represents the current parity of the array. We only need 0 for even, 1 for odd.
2. Compute a prefix sum array modulo 2. Let `prefix[i]` be the sum modulo 2 of the first `i` elements. This allows O(1) queries for the sum parity of any subarray `[l, r]` using `prefix[r] - prefix[l-1]` modulo 2.
3. For each query `(l, r, k)`, compute the length `m = r - l + 1`. Compute the parity of the range sum modulo 2 from the prefix sum array.
4. Compute the parity of `m * k`. This is `0` if `k` is even, or `m % 2` if `k` is odd.
5. Compute the new array parity as `(total_parity - range_parity + replacement_parity) % 2`.
6. If the result is 1, print "YES". Otherwise, print "NO".

Why it works: all arithmetic is modulo 2. The invariant is that any sequence of additions and subtractions modulo 2 gives the correct parity. Since each query is independent, we never modify the actual array, and we only rely on the precomputed prefix sum and array total sum parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        prefix = [0] * (n + 1)
        total_parity = 0
        for i in range(n):
            prefix[i + 1] = (prefix[i] + a[i]) % 2
            total_parity = (total_parity + a[i]) % 2

        for _ in range(q):
            l, r, k = map(int, input().split())
            m = r - l + 1
            range_parity = (prefix[r] - prefix[l - 1]) % 2
            replacement_parity = (m % 2) if (k % 2 == 1) else 0
            new_parity = (total_parity - range_parity + replacement_parity) % 2
            print("YES" if new_parity == 1 else "NO")

if __name__ == "__main__":
    solve()
```

The code first computes the prefix sum modulo 2 to allow quick subarray parity queries. Each query is then processed in O(1), computing the effect of replacing the range on the overall parity. Subtle points include using `l-1` in the prefix array for 1-based indices and reducing all arithmetic modulo 2 to avoid large numbers.

## Worked Examples

### Example 1

Input:

```
5 5
2 2 1 3 2
2 3 3
```

| Query | l | r | k | m | range_parity | replacement_parity | total_parity | new_parity | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 3 | 2 | 1 | 0 | 0 | 1 | YES |

Explanation: original sum = 10 (even), replacing indices 2-3 with 3, length 2, replacement parity 0, subtract range parity 1 → 10-1+0 = 9 → odd.

### Example 2

Input:

```
1 1
1
1 1 2
```

| Query | l | r | k | m | range_parity | replacement_parity | total_parity | new_parity | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 1 | 1 | 0 | 1 | 0 | NO |

This tests the smallest array. Replacing `1` with even `2` changes the sum from odd to even.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Prefix sum computation is O(n), each query is O(1) |
| Space | O(n) | Store prefix sum modulo 2 |

The total `n` and `q` across test cases do not exceed 200,000, so O(n + q) is acceptable within the 2-second limit. Modulo arithmetic avoids large integer sums.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""2
5 5
2 2 1 3 2
2 3 3
2 3 4
1 5 5
1 4 9
2 4 3
10 5
1 1 1 1 1 1 1 1 1 1
3 8 13
2 5 10
3 8 10
1 10 2
1 9 100""") == """YES
YES
YES
NO
YES
NO
NO
NO
NO
YES"""

# Custom cases
assert run("""1
1 1
1
1 1 1""") == "NO", "single element replaced with same parity"
assert run("""1
2 2
1 2
1 1 2
2 2 3""") == "NO\nYES", "two elements, mixed parity"
assert run("""1
3 3
2 2 2
1 3 1
1 2
```
