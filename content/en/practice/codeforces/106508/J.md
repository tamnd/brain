---
title: "CF 106508J - GCD and LCM Subsequences"
description: "We are given a sequence of integers and we are asked to consider all its non-empty subsequences. For each subsequence, we compute two values: the greatest common divisor of all elements in it and the least common multiple of all elements in it."
date: "2026-06-18T19:12:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106508
codeforces_index: "J"
codeforces_contest_name: "2026 SCUT Programming Contest\uff082026 \u534e\u5357\u7406\u5de5\u5927\u5b66\u7a0b\u5e8f\u8bbe\u8ba1\u6821\u8d5b\uff09"
rating: 0
weight: 106508
solve_time_s: 45
verified: true
draft: false
---

[CF 106508J - GCD and LCM Subsequences](https://codeforces.com/problemset/problem/106508/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and we are asked to consider all its non-empty subsequences. For each subsequence, we compute two values: the greatest common divisor of all elements in it and the least common multiple of all elements in it. The task is to count how many subsequences have the property that these two values are equal.

A useful way to interpret this condition is to think about what it means for a set of numbers to have identical gcd and lcm. The gcd of a set is always less than or equal to every element in the set, while the lcm is always greater than or equal to every element. For both to coincide, every element must sit exactly at the same value, because otherwise the lcm would strictly exceed the smallest element or the gcd would drop below the largest element. This observation turns the problem from something that looks number-theoretically heavy into a structural counting problem over equal values.

The input is simply one array of integers, and the output is the number of valid subsequences under this condition.

From a constraints perspective, the key implication is whether we can afford anything that iterates over all subsequences. A sequence of size up to around 10^5 immediately rules out any exponential exploration. Even quadratic counting over pairs becomes too slow in the worst case if repeated across multiple test cases. This pushes us toward a solution that compresses the array into frequency counts and works in linear or near-linear time.

A subtle failure case appears when trying to reason locally about gcd or lcm instead of globally. For example, in an array like `[2, 3, 4]`, a naive attempt might think some mixed subsequences could work if gcd and lcm “happen to meet”, but checking reveals:

subsequence `[2, 4]` has gcd 2 and lcm 4, which are not equal, and `[2, 3, 4]` has gcd 1 and lcm 12. Only single-element subsequences work. This reinforces that any mixture of distinct values breaks the equality condition immediately.

Another edge case is when all elements are identical, for example `[5, 5, 5]`. Every non-empty subsequence works, so the answer should be $2^3 - 1 = 7$. Any solution that forgets to count multiplicities would incorrectly return 1.

## Approaches

The brute-force approach is straightforward to describe. We iterate over every non-empty subsequence, compute its gcd and lcm by folding over its elements, and check whether they match. This is correct because it directly follows the definition of the problem. The issue is the number of subsequences: an array of size $n$ has $2^n - 1$ subsequences, and even for $n = 40$ this already becomes infeasible, while $n = 10^5$ makes it completely impossible.

The key structural insight is that equality of gcd and lcm forces all elements in the subsequence to be identical. Once this is recognized, the problem stops depending on gcd or lcm computations at all and reduces to counting how many ways we can pick a non-empty subset from each group of equal values. If a value appears $f$ times, any subset of those occurrences forms a valid subsequence, giving $2^f - 1$ choices.

We reduce the problem from enumerating subsequences to counting frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Frequency Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and count how many times each distinct number appears. This step compresses the sequence into equivalence classes of identical values, which are the only candidates that can form valid subsequences.
2. For each distinct value with frequency $f$, compute how many non-empty subsequences can be formed using only that value. This is $2^f - 1$, since each occurrence can be either included or excluded, except the empty choice.
3. Sum these contributions across all distinct values.
4. Return the final sum as the answer.

The reasoning behind summing independently per value is that any subsequence containing two different values immediately violates the condition, so valid subsequences are partitioned cleanly by value.

### Why it works

A subsequence satisfies gcd equals lcm only if all its elements are identical. If two elements differ, say $a < b$, then the lcm is at least $b$ while the gcd is at most $a$, so equality is impossible unless $a = b$. This forces every valid subsequence to be contained entirely within a single value class. The algorithm enumerates exactly these classes and counts all non-empty subsets inside each, ensuring completeness and no overcounting.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    freq = Counter(arr)
    
    ans = 0
    for v, f in freq.items():
        ans += (1 << f) - 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the reasoning directly. The frequency table compresses the array, and the bit shift `(1 << f)` efficiently computes $2^f$. Subtracting one removes the empty subsequence. No gcd or lcm computation is needed because the structural argument eliminates mixed-value subsequences entirely.

A subtle implementation detail is the use of a bit shift instead of `pow(2, f)`, which avoids floating-point overhead and is standard in competitive programming for integer exponentiation.

## Worked Examples

### Example 1

Input:

```
5
1 2 2 2 3
```

We compute frequencies: 1 appears once, 2 appears three times, 3 appears once.

| Value | Frequency | Contribution $2^f - 1$ |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 7 |
| 3 | 1 | 1 |

Total answer is 9.

This trace shows that only subsequences formed within identical values contribute, and mixing values never appears in the computation.

### Example 2

Input:

```
4
7 7 7 7
```

| Value | Frequency | Contribution |
| --- | --- | --- |
| 7 | 4 | 15 |

Every non-empty subset is valid because all elements are identical, confirming the formula reduces correctly to counting all subsets minus the empty one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to count frequencies and one pass over distinct values |
| Space | O(n) | Storage for frequency map |

The solution scales linearly with input size, which is sufficient for typical constraints up to 10^5 or more, staying comfortably within time limits.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from collections import Counter

    n = int(sys.stdin.readline().strip())
    arr = list(map(int, sys.stdin.readline().split()))
    freq = Counter(arr)

    ans = 0
    for v, f in freq.items():
        ans += (1 << f) - 1
    return str(ans)

# provided sample-like checks
assert run("5\n1 2 2 2 3\n") == "9"

# all equal
assert run("4\n7 7 7 7\n") == str((1 << 4) - 1)

# all distinct
assert run("3\n1 2 3\n") == "3"

# single element
assert run("1\n42\n") == "1"

# two groups
assert run("6\n5 5 1 1 1 9\n") == str((1<<2)-1 + (1<<3)-1 + (1<<1)-1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct | n | only singletons contribute |
| all equal | 2^n - 1 | full subset explosion |
| mixed frequencies | sum per group | independence of values |

## Edge Cases

When all elements are identical, such as `[10, 10, 10]`, the algorithm counts all $2^3 - 1$ subsequences. The frequency map produces a single entry with frequency 3, and the computation correctly aggregates all non-empty subsets.

When all elements are distinct, such as `[1, 2, 3, 4]`, each frequency is 1, so each contributes $2^1 - 1 = 1$. The result is 4, matching the fact that only single-element subsequences are valid.

When there is a dominant value and many rare ones, such as `[5, 5, 5, 1, 2]`, the algorithm cleanly separates contributions by value, ensuring no invalid mixed subsequence is ever considered.
