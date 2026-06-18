---
title: "CF 106263B - \u5c0f\u6a58\u7684\u9b54\u6cd5\u5b9d\u77f3"
description: "We are given several independent test cases. In each one, we receive a list of integers representing the “magic power” of a collection of stones. For every unordered pair of distinct stones, we compute the bitwise AND of their values and then sum these results over all pairs."
date: "2026-06-18T23:18:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106263
codeforces_index: "B"
codeforces_contest_name: "2025 \u534e\u5357\u5e08\u8303\u5927\u5b66\u201c\u5353\u8d8a\u6559\u80b2\u676f\u201d\u7b97\u6cd5\u4e0e\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u65b0\u751f\u8d5b\uff09"
rating: 0
weight: 106263
solve_time_s: 52
verified: true
draft: false
---

[CF 106263B - \u5c0f\u6a58\u7684\u9b54\u6cd5\u5b9d\u77f3](https://codeforces.com/problemset/problem/106263/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, we receive a list of integers representing the “magic power” of a collection of stones. For every unordered pair of distinct stones, we compute the bitwise AND of their values and then sum these results over all pairs.

So the task is purely combinational: every pair contributes a value determined by shared set bits between the two numbers. The output for each test case is the total sum over all pairs.

The key structural challenge is that the number of pairs grows quadratically with n. When n reaches 200,000 in a test, the number of pairs is on the order of 2×10^10, which immediately rules out any direct pair enumeration. Even with multiple test cases, the total n can reach 400,000, so any solution must be close to linear or linear-logarithmic.

A subtle failure case for naive reasoning is assuming that pairwise AND behaves like arithmetic averages or can be aggregated without considering bit independence. For example, if all numbers are identical, say `[7, 7, 7]`, every pair contributes `7 & 7 = 7`, so the answer is `3 * 7 = 21`. A naive attempt that mistakenly counts contributions per element instead of per pair can easily overcount or undercount by mixing ordered and unordered pairs.

Another pitfall is forgetting that bitwise operations decompose cleanly per bit, but only if each bit is treated independently. Any approach that tries to reconstruct AND values without per-bit reasoning tends to collapse under large constraints.

## Approaches

A brute-force solution would iterate over all pairs `(i, j)` with `i < j` and compute `(a[i] & a[j])`, accumulating the result. This is correct because it directly follows the definition of the problem. However, its cost is proportional to the number of pairs, which in the worst case is `n(n-1)/2`. With `n = 2 × 10^5`, this becomes completely infeasible.

The structure of bitwise AND suggests a decomposition: instead of computing full values per pair, we can look at each bit position independently. A bit contributes `2^k` to the final AND sum of a pair if and only if both numbers in the pair have that bit set. This transforms the problem from reasoning about values to reasoning about bit counts.

For a fixed bit `k`, suppose `cnt_k` numbers have this bit set. Any pair formed from these `cnt_k` numbers contributes `2^k` to the answer. The number of such pairs is `cnt_k * (cnt_k - 1) / 2`. Summing this over all bits gives the final result.

This works because bitwise AND is additive over independent bit positions, and no carry or interaction exists between bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Bit Counting | O(n · 31) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and compute the answer using per-bit counting.

1. Initialize an array or loop structure to count how many numbers contain each bit. Since `a[i] ≤ 10^8`, we only need bits up to 30.
2. For each number in the array, inspect each bit position. If the bit is set, increment the corresponding counter. This builds a frequency table of how many numbers contain each bit.
3. For each bit position `k`, compute how many pairs can be formed from numbers having that bit set. If `cnt_k` numbers contain bit `k`, the number of valid pairs is `cnt_k * (cnt_k - 1) // 2`.
4. Each such pair contributes `2^k` to the final sum. Multiply and add this contribution to the answer.
5. Output the accumulated result for the test case.

The reason we count pairs after counting frequencies is that pair formation depends only on membership in the set of numbers with a bit, not on ordering or interaction with other bits.

### Why it works

Each pair contributes to the final sum independently for each bit where both numbers share a 1. If we fix a bit position, the contribution of all pairs is determined entirely by how many numbers include that bit. Because different bit positions never interfere, summing contributions across bits reconstructs the full AND sum over all pairs exactly once per pair-bit combination.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * 31  # enough for values up to 1e9

        for x in a:
            b = 0
            while x:
                if x & 1:
                    cnt[b] += 1
                x >>= 1
                b += 1

        ans = 0
        for k in range(31):
            c = cnt[k]
            if c > 1:
                ans += (c * (c - 1) // 2) * (1 << k)

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution uses a per-bit frequency array `cnt`. For each number, we decompose it using bit shifts rather than repeatedly masking each bit index, which keeps implementation simple and avoids extra overhead.

A common implementation mistake is iterating bits incorrectly and shifting the original number destructively without care. Here, we rebuild bit positions using a loop that shifts `x`, so each number is consumed safely without affecting others.

The combination formula `c * (c - 1) // 2` must be computed in 64-bit-safe arithmetic. Python naturally handles large integers, so overflow is not a concern.

## Worked Examples

Consider input:

```
1
3
1 2 3
```

We track bit counts:

| Step | Number | Bit 0 count | Bit 1 count | Partial state |
| --- | --- | --- | --- | --- |
| 1 | 1 (01) | 1 | 0 | [1,0] |
| 2 | 2 (10) | 1 | 1 | [1,1] |
| 3 | 3 (11) | 2 | 2 | [2,2] |

Now compute contributions:

For bit 0: `cnt = 2`, pairs = 1, contribution = `1 * 1 = 1`

For bit 1: `cnt = 2`, pairs = 1, contribution = `2 * 1 = 2`

Final answer = 3.

This trace shows that each bit contributes independently, and overlaps across numbers accumulate correctly.

Now consider:

```
1
4
5 5 5 5
```

Binary 5 = `101`.

| Step | Number | Bit 0 | Bit 2 | State |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 1 | [1,1] |
| 2 | 5 | 2 | 2 | [2,2] |
| 3 | 5 | 3 | 3 | [3,3] |
| 4 | 5 | 4 | 4 | [4,4] |

Each bit has `cnt = 4`, so pairs = 6.

Bit 0 contribution = 6 * 1 = 6

Bit 2 contribution = 6 * 4 = 24

Total = 30

This matches the fact that all 6 pairs produce `(5 & 5) = 5`, so total is `6 * 5 = 30`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n · B) | Each number is processed across at most B = 31 bits |
| Space | O(B) | Only frequency array for bits |

The constraints allow up to 4×10^5 total elements across all test cases. With about 31 operations per element, the total work is roughly 1.2×10^7 operations, which fits easily within time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout

    data = inp.strip().split()
    it = iter(data)
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]

        cnt = [0] * 31
        for x in arr:
            b = 0
            while x:
                if x & 1:
                    cnt[b] += 1
                x >>= 1
                b += 1

        ans = 0
        for k in range(31):
            c = cnt[k]
            ans += (c * (c - 1) // 2) * (1 << k)

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("1\n3\n1 2 3") == "3"

# minimum size
assert run("1\n1\n7") == "0"

# all equal
assert run("1\n4\n5 5 5 5") == "30"

# no shared bits
assert run("1\n3\n1 2 4") == "0"

# mixed
assert run("2\n2\n1 3\n3\n7 7 7") == "1\n21"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | no pairs exist |
| all equal | 30 | combinational pair counting correctness |
| disjoint bits | 0 | AND zero propagation |
| mixed cases | varied | multi-test handling and correctness |

## Edge Cases

A single-element test like `n = 1` exposes whether the implementation incorrectly assumes at least one pair exists. In this case, the bit counts may be non-zero, but the pair formula correctly yields zero because `cnt * (cnt - 1) / 2` is zero.

For an input like `3 1 2 4`, each number has disjoint bits, so every AND is zero. The bit counting approach sets each bit count to exactly one, producing zero contribution per bit, matching the expected result.

For a uniform array such as `5 5 5 5`, each bit appears four times, and the algorithm counts `6` pairs per bit, correctly reproducing the fact that all pairs have identical AND equal to 5.
