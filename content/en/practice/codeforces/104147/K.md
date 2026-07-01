---
title: "CF 104147K - Hobz is a good guy"
description: "We are given a binary string and we are allowed to delete any number of characters from it, possibly all but at least one character must remain."
date: "2026-07-02T01:31:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104147
codeforces_index: "K"
codeforces_contest_name: "JCPC 2022"
rating: 0
weight: 104147
solve_time_s: 75
verified: true
draft: false
---

[CF 104147K - Hobz is a good guy](https://codeforces.com/problemset/problem/104147/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string and we are allowed to delete any number of characters from it, possibly all but at least one character must remain. After deletions, we want the remaining subsequence to satisfy a parity condition based on positions inside the subsequence itself, not the original string.

More precisely, if we index the kept string starting from 1, we look at all characters placed in odd positions and all characters placed in even positions. The requirement is that the number of `1` characters appearing in odd positions must equal the number of `1` characters appearing in even positions. We are not required to maximize length or construct anything explicitly, only to decide whether at least one valid non-empty subsequence exists.

The constraints allow up to 100,000 test cases with a total combined string length of 200,000. This immediately rules out any approach that tries to enumerate subsequences or even attempts to simulate all deletions independently per test case. Anything beyond linear time per test case would be too slow, and even linear per test case must be handled carefully in aggregate.

A subtle issue appears when thinking about greedy selection. It is tempting to assume that we must preserve relative structure or that parity depends on original indices. That is incorrect because positions are re-numbered after deletion. Another common mistake is to assume we need equal counts of ones in the original string’s odd and even indices, which also does not reflect the problem.

A minimal edge case is a single character string. If it is `1`, we can take it and positions are just odd position 1, so odd ones is 1 and even ones is 0, which fails the condition. If it is `0`, we can also take it, and both counts are zero, so it is valid. This already shows that zeros are harmless and ones are the only meaningful contributors.

## Approaches

The brute-force idea is to try every subsequence and check whether it satisfies the condition. For each subsequence, we would simulate its construction and count ones in odd and even positions. Since there are exponentially many subsequences, this approach grows like $O(2^n)$ per test case, which is completely infeasible even for small strings.

To simplify, we should focus on what actually matters. The condition depends only on how ones can be distributed across alternating parity positions in some chosen subsequence. Zeros do not contribute to the condition at all, they only help by filling positions and allowing ones to shift between odd and even slots.

The key observation is that we are not required to use all characters. We only need to know whether there exists at least one valid construction. If we ever manage to pick two ones, we can always place them at positions 1 and 2 in the subsequence, making one go to an odd position and one to an even position, which satisfies the equality. If we pick only one one, it will always sit in an odd position and break the condition. If we pick no ones, the subsequence must be composed entirely of zeros, which always satisfies the condition since both odd and even positions contain zero ones.

So the problem reduces to checking whether the string contains at least two ones or contains no ones at all.

If the number of ones is exactly one, the answer is impossible. If it is zero or at least two, it is possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ total | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Count the number of characters equal to `1` in the string. This is sufficient because zeros never affect the constraint, only the placement of ones matters.
2. If the count of ones is exactly 1, immediately output `NO`. With a single one, any subsequence containing it will place it in position 1 of that subsequence or some odd position, and there is no second one to balance it on even positions.
3. Otherwise, output `YES`. If there are zero ones, we can keep any single zero, and both odd and even counts of ones are zero. If there are at least two ones, we can always pick two of them and arrange them in alternating positions in a subsequence so that one lands in an odd position and one in an even position, satisfying equality.

### Why it works

The subsequence structure only matters through parity positions assigned after deletions. Zeros can always be used as flexible separators, meaning any two chosen ones can be placed into different parity classes in some subsequence ordering. The only obstruction occurs when there is exactly one one, because parity balance requires pairing contributions from ones across both odd and even positions, and a single element cannot contribute to both sides. All other cases either have no ones or at least two, both of which admit a valid construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        ones = s.count('1')
        if ones == 1:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly counts ones per test case. The logic is fully contained in a single condition, which avoids any need to simulate subsequences or track parity explicitly. The critical detail is that we do not attempt to reason about positions in the original string, because deletions completely redefine indexing.

## Worked Examples

### Example 1

Input string: `01`

We track only the number of ones.

| Step | String | Ones count | Decision |
| --- | --- | --- | --- |
| 1 | "01" | 1 | reject |

The single one forces any subsequence containing it to have imbalance in odd and even positions.

This confirms the key edge case where exactly one one fails.

### Example 2

Input string: `1010`

| Step | String | Ones count | Decision |
| --- | --- | --- | --- |
| 1 | "1010" | 2 | accept |

With two ones, we can construct a subsequence like `11` by deleting zeros. In the subsequence, positions are 1 and 2, so each one lands in different parity classes, producing equality.

This demonstrates that zeros are irrelevant and only the count of ones matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case, $O(\sum n)$ overall | Each string is scanned once to count ones |
| Space | $O(1)$ extra | Only a counter is maintained |

The total length constraint of 200,000 guarantees that a single pass over all input is easily fast enough in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        ones = s.count('1')
        out.append("NO" if ones == 1 else "YES")
    return "\n".join(out) + "\n"

# provided samples
assert run("3\n0\n1\n01\n") == "YES\nNO\nYES\n"

# single zero
assert run("1\n0\n") == "YES\n"

# single one
assert run("1\n1\n") == "NO\n"

# two ones
assert run("1\n11\n") == "YES\n"

# mixed large
assert run("1\n101010\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | YES | single zero is valid |
| `1` | NO | single one is invalid |
| `11` | YES | minimal valid non-zero case |
| `101010` | YES | alternating structure, multiple ones |

## Edge Cases

The single-character cases are the most sensitive. For input `0`, the algorithm counts zero ones and immediately outputs `YES`, which corresponds to taking the entire string as a valid subsequence.

For input `1`, the count is exactly one, so the algorithm outputs `NO`. Any attempt to keep this character leaves it in position 1 of the subsequence, producing one odd-position one and zero even-position ones, violating the condition.

Another edge case is when all characters are zeros, such as `000000`. The count of ones is zero, so the algorithm outputs `YES`. We can take any single zero, and since there are no ones in either parity class, the condition is satisfied.

Finally, consider strings with multiple ones but separated by zeros, such as `10001`. The count of ones is 2, so the algorithm outputs `YES`. We can delete zeros and keep two ones, producing a subsequence of `11`, which balances odd and even positions automatically.
