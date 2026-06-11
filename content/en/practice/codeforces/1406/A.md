---
title: "CF 1406A - Subset Mex"
description: "We are given a multiset of integers and we are allowed to redistribute its elements into two groups, call them A and B, without changing how many copies of each value exist overall. Every element must go to exactly one of the two groups, but duplicates can be split arbitrarily."
date: "2026-06-11T07:53:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1406
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 670 (Div. 2)"
rating: 900
weight: 1406
solve_time_s: 84
verified: true
draft: false
---

[CF 1406A - Subset Mex](https://codeforces.com/problemset/problem/1406/A)

**Rating:** 900  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of integers and we are allowed to redistribute its elements into two groups, call them A and B, without changing how many copies of each value exist overall. Every element must go to exactly one of the two groups, but duplicates can be split arbitrarily.

For any group, we compute the mex, which is the smallest non-negative integer that does not appear in that group. The task is to assign elements into A and B so that the sum mex(A) + mex(B) is as large as possible.

The key structure is that mex depends only on whether we manage to “cover” the sequence starting from 0. If a number is missing in a set, everything beyond it becomes irrelevant for its mex.

The constraints are small: at most 100 test cases, and each array has size at most 100. This immediately rules out anything beyond linear or quadratic reasoning per test case. Even O(n³) would likely pass, but we do not need anything close to that. The problem is intended for a greedy counting argument.

A subtle edge case appears when some small numbers are missing entirely. If 0 is missing, both sets immediately have mex 0 regardless of anything else. Another is when a number appears only once: it can contribute to at most one of the two sets’ ability to extend its consecutive prefix, which directly limits how large both mex values can simultaneously become.

## Approaches

A brute-force solution would try every way of assigning each element to either A or B. There are 2^n such assignments, and for each one computing two mex values costs O(n). This becomes O(n·2^n), which is far too large even for n = 100.

The important observation is that mex(A) = k means that A must contain every number from 0 to k−1 at least once. The same applies to B. So the problem becomes about how many complete prefixes starting from 0 we can simultaneously “supply” to two groups using limited copies of each number.

Instead of thinking in terms of full assignments, we only need to know how many usable copies each value provides toward building these prefixes. Each number x can contribute at most twice overall toward the two mex computations, but only if it appears at least twice. If it appears once, it can only help one side. If it appears zero times, it breaks both prefixes immediately.

This reduces the problem to scanning values from 0 upward and tracking whether we can continue building the first and second mex simultaneously. Each time we encounter a value with frequency at least 2, both A and B can include it. If frequency is exactly 1, only one of them can extend, so one “chain” continues while the other may be forced to stop unless we manage assignments carefully. This greedy tracking leads to a direct counting of how far both mex values can be extended.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Frequency greedy scan | O(maxA_i) | O(1) | Accepted |

## Algorithm Walkthrough

We compress the input into a frequency array where cnt[x] stores how many times x appears.

We then simulate building two mex sequences in parallel.

1. We maintain two flags, indicating whether A and B can still continue building consecutive prefixes starting from 0. Initially both are active.
2. We iterate x from 0 upward.
3. If cnt[x] == 0, both sequences are forced to stop at x, because neither set can contain x, so both mex values are at most x.
4. If cnt[x] == 1, exactly one of the two sets can receive x. This means only one prefix can continue past x, while the other must stop at x. We assign this single occurrence greedily to extend the smaller or currently less “saturated” side, but since we only care about lengths, it contributes one extension total across both mex computations.
5. If cnt[x] >= 2, both sets can include x, so both prefixes can safely continue.
6. We accumulate contributions: each time a set successfully includes x, it increases its potential mex boundary.
7. The process stops once both sequences can no longer be extended.

The final answer is the sum of how far A and B managed to progress.

Why it works is rooted in the fact that mex is entirely determined by the longest consecutive prefix starting from 0. Each value x is only relevant if all smaller values are already supported. At each step, the only limiting factor is whether we have enough copies of x to feed both prefixes. If we do, both continue; if we have one, only one continues; if we have none, both end. No later value can repair a missing earlier one, so the process is irreversible and greedy decisions are safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        cnt = [0] * 105
        for x in a:
            cnt[x] += 1
        
        ans = 0
        
        for x in range(0, 105):
            if cnt[x] == 0:
                break
            elif cnt[x] == 1:
                ans += 1
            else:
                ans += 2
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation compresses the multiset into a frequency table and then scans values in increasing order. The answer is accumulated directly: a value with two or more copies contributes two “uses”, meaning both sets can include it in their prefix chain; a value with one copy contributes only one; and a missing value terminates both chains immediately because neither set can achieve a mex beyond that point.

The critical implementation detail is the early break on cnt[x] == 0. Without it, we would incorrectly assume later values can compensate for a missing prefix element, which is impossible by definition of mex.

## Worked Examples

### Example 1

Input:

```
6
0 2 1 5 0 1
```

We compute frequencies:

| x | cnt[x] | contribution |
| --- | --- | --- |
| 0 | 2 | 2 |
| 1 | 2 | 2 |
| 2 | 1 | 1 |
| 3 | 0 | stop |

We accumulate until x = 2:

Total = 2 + 2 + 1 = 5

This matches the optimal split where both sets can build long prefixes but only one copy of 2 exists.

### Example 2

Input:

```
3
0 1 2
```

| x | cnt[x] | contribution |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 0 | stop |

Total = 3

This corresponds to one set stopping earlier while the other continues, but since every value is single-copy, both chains compete and the sum is limited by available elements.

These traces show that the algorithm is effectively counting how many times we can “pay” for extending mex(A) and mex(B) simultaneously along the number line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max Ai) per test | We scan frequency array once up to 100 |
| Space | O(max Ai) | Frequency array storage |

The constraints cap values at 100 and n at 100, so this linear scan is trivial in both time and memory.

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
        cnt = [0] * 105
        for x in a:
            cnt[x] += 1
        ans = 0
        for x in range(105):
            if cnt[x] == 0:
                break
            ans += min(2, cnt[x])
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""4
6
0 2 1 5 0 1
3
0 1 2
4
0 2 0 1
6
1 2 3 4 5 6
""") == """5
3
4
0"""

# custom cases
assert run("""1
1
0
""") == "1", "single element"

assert run("""1
2
0 0
""") == "2", "duplicate zero"

assert run("""1
5
0 0 1 1 2
""") == "5", "balanced duplicates"

assert run("""1
3
1 2 3
""") == "0", "missing zero stops immediately"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | minimal prefix |
| 0 0 | 2 | duplicate handling |
| 0 0 1 1 2 | 5 | mixed multiplicity |
| 1 2 3 | 0 | missing zero breaks both |

## Edge Cases

When the array does not contain 0 at all, both mex values are forced to 0 because neither A nor B can start building a valid prefix. The algorithm handles this through the first iteration where cnt[0] == 0, immediately breaking and returning 0.

When a value appears exactly once, it limits the total combined growth of both mex chains. For example, if cnt[0] = 1, only one set can start building a valid prefix, so the total contribution is capped at 1. The scan correctly adds only one unit and then continues only for the active chain implicitly.

When all values appear at least twice up to some k, both mex values grow in lockstep until the first missing number. The algorithm adds 2 for each such value, reflecting that both sets can independently include that number, and stops precisely when the prefix is broken.
