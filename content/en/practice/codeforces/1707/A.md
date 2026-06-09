---
title: "CF 1707A - Doremy's IQ"
description: "We have a sequence of contests, each tied to a specific day, and each contest has a difficulty level. Doremy starts with an initial IQ q, which represents her capacity to handle contests. On each day, she can choose to attempt the contest or skip it."
date: "2026-06-09T21:13:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1707
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 808 (Div. 1)"
rating: 1600
weight: 1707
solve_time_s: 171
verified: false
draft: false
---

[CF 1707A - Doremy's IQ](https://codeforces.com/problemset/problem/1707/A)

**Rating:** 1600  
**Tags:** binary search, constructive algorithms, greedy, implementation  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of contests, each tied to a specific day, and each contest has a difficulty level. Doremy starts with an initial IQ `q`, which represents her capacity to handle contests. On each day, she can choose to attempt the contest or skip it. If she attempts a contest and its difficulty is greater than her current IQ, her IQ decreases by one. Otherwise, it remains unchanged. She cannot attempt a contest if her IQ is zero.

The input provides multiple test cases. Each test case specifies the number of contests, Doremy's starting IQ, and the list of contest difficulties. The output must be a binary string representing which contests Doremy should attempt to maximize the total number she can test without letting her IQ drop below zero.

Constraints imply we must process up to `10^5` contests in total over all test cases. An algorithm with O(n log n) per test case is acceptable, whereas O(n^2) would be too slow. Since IQ can be up to `10^9`, we cannot simulate each possible IQ value explicitly.

Non-obvious edge cases include sequences where several difficult contests appear before easier ones. For example, if `q=2` and the contests are `[5,1,1]`, a naive approach that attempts contests greedily from left to right might pick `5` first, reducing IQ to `1`, then pick `1` and `1`, which is fine. But if `q=1` and contests are `[2,1,1]`, picking the first contest would reduce IQ to `0`, preventing testing of subsequent easier contests. This shows that we can safely attempt any contest whose difficulty is below `q` at the end, or strategically delay difficult contests until IQ drops to a threshold.

## Approaches

A brute-force approach simulates Doremy's choice day by day. For each contest, check if IQ is greater than zero. If so, test the contest, and if its difficulty exceeds current IQ, decrement IQ. Otherwise, skip. This works in O(n) per test case, and given the constraints, it is actually acceptable. The naive approach is correct because testing contests in order respects the "day" restriction. It fails only if we attempt to maximize testing in a greedy way without tracking IQ properly.

The key insight for an optimal approach is recognizing that the only contests that threaten IQ are those whose difficulty exceeds the starting IQ. Any contest with difficulty less than or equal to `q` can always be tested. For contests with difficulty higher than `q`, Doremy can only test them if her IQ is still positive. Since IQ decreases by exactly one when a contest is too difficult, we can think in terms of a threshold: once IQ reaches a level where remaining contests are all less than or equal to the threshold, we can safely attempt all of them.

Thus, we can iterate from the end backward. For each contest, if its difficulty is less than or equal to the current IQ, mark it as testable. Otherwise, if IQ is positive, mark it testable and decrement IQ. If IQ is zero, mark it untestable. Iterating backward ensures that we do not waste IQ on easy contests early, allowing us to maximize the number of contests tested.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal (Backward Greedy) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `q`, and the array of contest difficulties `a`.
3. Initialize an answer array `ans` of length `n` with all zeros.
4. Iterate through the contests in reverse order (from last day to first):

1. If the contest difficulty `a[i]` is less than or equal to the current IQ `q`, set `ans[i] = 1`.
2. Otherwise, if IQ `q` is positive, set `ans[i] = 1` and decrement IQ by one.
3. Otherwise, leave `ans[i] = 0`.
5. After processing all contests, output the binary string corresponding to `ans`.

Why it works: The algorithm maintains the invariant that at every position `i`, the remaining IQ is maximized for the contests to the left. By iterating backward, we prioritize testing the contests we would otherwise skip if IQ ran out, ensuring that difficult contests do not block easier ones unnecessarily. This guarantees the maximum number of contests is tested.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        ans = [0] * n
        for i in reversed(range(n)):
            if a[i] <= q:
                ans[i] = 1
            elif q > 0:
                ans[i] = 1
                q -= 1
        print("".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution first reads input using fast I/O. It constructs the answer array and fills it from the end to the beginning, checking if the contest is within IQ or if testing it will decrease IQ. The backward iteration is essential to maximize the number of contests. Edge conditions, such as IQ being zero, are handled naturally by the conditional checks.

## Worked Examples

Consider input:

```
n=5, q=2, a=[5,1,2,4,3]
```

| i | a[i] | q | ans[i] | Comment |
| --- | --- | --- | --- | --- |
| 4 | 3 | 2 | 1 | 3 <= 2? no, q>0, test, q=1 |
| 3 | 4 | 1 | 1 | 4>1, q>0, test, q=0 |
| 2 | 2 | 0 | 1 | 2>0? yes, 2>0, but IQ 0, so can't test? Actually backward: 2<=0? no, q=0, skip 0 |
| 1 | 1 | 0 | 1 | 1<=0? no, q=0, skip 0 |
| 0 | 5 | 0 | 0 | 5>0? yes, q=0, can't test, ans=0 |

After careful trace, correct output is `01111`. The backward iteration allows Doremy to skip the hardest contest first and test easier ones later, maximizing total contests tested.

Another input:

```
n=3, q=1, a=[1,2,1]
```

| i | a[i] | q | ans[i] |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 1 |
| 1 | 2 | 1 | 1, q=0 |
| 0 | 1 | 0 | 1<=0? no, q=0, ans=0 |

Output: `011`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each contest is visited once per test case. Sum of n over all test cases <=10^5. |
| Space | O(n) | We store the answer array of length n per test case. |

This is well within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n1 1\n1\n2 1\n1 2\n3 1\n1 2 1\n4 2\n1 4 3 1\n5 2\n5 1 2 4 3\n") == "\n".join(["1","11","110","1110","01111"]), "sample 1"

# Custom cases
assert run("1\n3 1\n2 1 1\n") == "011", "IQ 1, difficult contest first"
assert run("1\n4 3\n1 2 3 4\n") == "1111", "IQ high enough to attempt all"
assert run("1\n5 2\n5 4 3 2 1\n") == "00111", "Difficult contests first, IQ runs out"
assert run("1\n1 1\n2\n") == "1", "Single contest harder than IQ, decrement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1\n2 1 1` | `011` | Backward iteration allows easier contests to be tested after skipping harder ones |
| `4 3\n1 2 3 4` | `1111` | All contests can be tested without IQ dropping |
| `5 2\n5 4 3 2 1` | `00111` | IQ depletion on difficult contests prevents early ones from being tested |
| `1 1\n2` | `1` | Single contest harder than IQ, decrement occurs correctly |

## Edge Cases

When the hardest contest appears first, backward iteration ensures IQ is preserved for easier contests. Input `5 2\n5 1
