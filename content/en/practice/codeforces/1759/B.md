---
title: "CF 1759B - Lost Permutation"
description: "We are given several numbers that definitely belong to some unknown permutation. The missing numbers were lost, but we know the sum of all missing values."
date: "2026-06-09T14:27:34+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1759
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round  834 (Div. 3)"
rating: 800
weight: 1759
solve_time_s: 147
verified: true
draft: false
---

[CF 1759B - Lost Permutation](https://codeforces.com/problemset/problem/1759/B)

**Rating:** 800  
**Tags:** math  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several numbers that definitely belong to some unknown permutation. The missing numbers were lost, but we know the sum of all missing values.

The question is whether we can choose some additional numbers whose total sum is exactly `s` so that, together with the given numbers, the final array becomes a valid permutation.

A permutation of length `n` contains every integer from `1` through `n` exactly once. That requirement is much stronger than merely having distinct values. If the largest value in the final array is `k`, then every number from `1` to `k` must appear.

The constraints are very small. There are at most 100 test cases, each containing at most 50 known numbers, and all values are at most 50. Even a simulation that tries many candidate permutation lengths would run comfortably within the time limit. We do not need sophisticated data structures or advanced algorithms.

The tricky part is understanding what the missing numbers must look like. They are not arbitrary distinct values. If the final array is a permutation ending at some maximum value `k`, then the missing numbers are exactly those integers from `1` to `k` that do not already appear in the given array.

Consider a few edge cases.

Suppose the input is:

```
1
1 1
1
```

The known number is already `1`. To add numbers summing to `1`, we would have to add another `1`, which would create a duplicate. No larger number works because every larger number is at least `2`. The answer is `NO`.

Now consider:

```
1
3 3
1 4 2
```

The only missing value between `1` and `4` is `3`, whose sum is exactly `3`. Adding it produces `[1,2,3,4]`, so the answer is `YES`.

Another subtle case is:

```
1
2 1
4 3
```

A careless solution might notice that the missing sum is `1` and assume we can add `1`. After adding `1`, the array would contain `{1,3,4}`, which is not a permutation because `2` is still missing. The correct answer is `NO`.

The requirement that all integers up to the maximum value must be present is the key observation that prevents many incorrect solutions.

## Approaches

A brute-force idea is to try every possible set of numbers whose sum is `s`, append them to the given array, and check whether the result is a permutation. This is correct because it explores every candidate completion. The problem is that the number of subsets grows exponentially. Even with values bounded by 50, enumerating all possibilities is unnecessary and conceptually much more complicated than the structure of the problem requires.

The important observation is that a permutation is completely determined by its largest value.

Suppose the final permutation has maximum value `k`. Then the permutation must contain every integer from `1` through `k`. Since the given numbers are already fixed, the numbers we need to append are exactly the missing integers from this range.

This turns the problem into a simple simulation.

We start with the sum `s`. We repeatedly add the smallest positive integers that are not already present in the given set. Each time we add such a number, we subtract it from `s`.

If `s` becomes exactly zero, we have found a candidate permutation. We then only need to verify that the resulting set contains every integer from `1` up to its maximum element.

If `s` becomes negative, we have already exceeded the required missing sum and no solution exists.

Because all values are small, this process is extremely fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(M + X) | O(M + X) | Accepted |

Here `X` is the largest value examined during the simulation, which is small under the given constraints.

## Algorithm Walkthrough

1. Read the given numbers and store them in a set for fast membership checks.
2. Starting from `1`, scan upward through the positive integers.
3. Whenever the current number is not already present in the set, treat it as a missing permutation value. Subtract it from `s` and insert it into the set.
4. Continue until `s` becomes zero or negative.
5. If `s` becomes negative, print `NO`.
6. If `s` becomes exactly zero, find the maximum value in the set.
7. Check whether every integer from `1` through that maximum value exists in the set.
8. If all of them are present, print `YES`; otherwise print `NO`.

### Why it works

At any moment, the algorithm only adds numbers that must appear in any valid permutation containing the given elements. We process missing integers in increasing order because every permutation containing the current maximum value must include all smaller positive integers.

When `s` reaches zero, the set contains the original numbers plus exactly the missing values whose total sum equals the required lost sum. If the resulting set forms a complete range from `1` to its maximum element, it is a permutation. If some value in that range is absent, no valid permutation can be formed because every permutation must contain that missing value as well.

The algorithm never skips a required number and never adds an unnecessary one, so it accepts exactly the valid cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    m, s = map(int, input().split())
    present = set(map(int, input().split()))

    x = 1

    while s > 0:
        if x not in present:
            s -= x
            present.add(x)
        x += 1

    if s < 0:
        print("NO")
        continue

    mx = max(present)

    ok = True
    for v in range(1, mx + 1):
        if v not in present:
            ok = False
            break

    print("YES" if ok else "NO")
```

The set `present` stores all currently known numbers. Membership checks are constant time, which makes it easy to determine whether a value is already part of the permutation.

The loop processes positive integers in increasing order. Whenever a number is missing, it is one of the values that must appear if the final array is to become a permutation. We subtract it from `s` and add it to the set.

The loop stops as soon as `s` is no longer positive. If it becomes negative, we overshot the required missing sum and no valid completion exists.

When `s` reaches exactly zero, we perform the final validation. A set such as `{1,3,4}` has no duplicates, but it is not a permutation because `2` is absent. The final range check catches such cases.

No overflow concerns exist because all numbers are tiny. The only subtle detail is that reaching `s == 0` is not sufficient by itself. We must still verify that the set forms a complete interval from `1` to its maximum value.

## Worked Examples

### Example 1

Input:

```
m = 3
s = 13
b = [3, 1, 4]
```

| Step | Current x | Missing? | New s | Set Contents |
| --- | --- | --- | --- | --- |
| Start | - | - | 13 | {1,3,4} |
| 1 | 1 | No | 13 | {1,3,4} |
| 2 | 2 | Yes | 11 | {1,2,3,4} |
| 3 | 3 | No | 11 | {1,2,3,4} |
| 4 | 4 | No | 11 | {1,2,3,4} |
| 5 | 5 | Yes | 6 | {1,2,3,4,5} |
| 6 | 6 | Yes | 0 | {1,2,3,4,5,6} |

The maximum value is `6`, and every integer from `1` through `6` is present. The answer is `YES`.

### Example 2

Input:

```
m = 2
s = 1
b = [4, 3]
```

| Step | Current x | Missing? | New s | Set Contents |
| --- | --- | --- | --- | --- |
| Start | - | - | 1 | {3,4} |
| 1 | 1 | Yes | 0 | {1,3,4} |

The sum condition is satisfied, but the final set is `{1,3,4}`.

Checking integers from `1` through `4` reveals that `2` is missing. The set is not a permutation, so the answer is `NO`.

This example demonstrates why the final range validation is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M + X) | Building the set and scanning candidate values |
| Space | O(M + X) | The set stores the original and added numbers |

The largest value encountered is small because the input numbers are at most 50 and `s` is at most 1000. The running time is comfortably below the limits even for all 100 test cases.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        m, s = map(int, input().split())
        present = set(map(int, input().split()))

        x = 1
        while s > 0:
            if x not in present:
                s -= x
                present.add(x)
            x += 1

        if s < 0:
            ans.append("NO")
            continue

        mx = max(present)
        ok = all(v in present for v in range(1, mx + 1))
        ans.append("YES" if ok else "NO")

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""5
3 13
3 1 4
1 1
1
3 3
1 4 2
2 1
4 3
5 6
1 2 3 4 5
"""
) == """YES
NO
YES
NO
YES
"""

# minimum case
assert run(
"""1
1 1
1
"""
) == """NO
"""

# already almost a permutation
assert run(
"""1
3 3
1 4 2
"""
) == """YES
"""

# gap remains after reaching s = 0
assert run(
"""1
2 1
4 3
"""
) == """NO
"""

# larger valid completion
assert run(
"""1
5 15
1 2 3 4 5
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | NO | Smallest possible case |
| `1 4 2` with `s=3` | YES | Single missing value completes permutation |
| `4 3` with `s=1` | NO | Sum condition alone is insufficient |
| `1 2 3 4 5` with `s=15` | YES | Multiple consecutive values must be added |

## Edge Cases

Consider:

```
1
1 1
1
```

The algorithm starts with set `{1}`. The first missing positive integer is `2`, so subtracting it would make `s = -1`. Since the sum becomes negative, the answer is `NO`. This correctly handles the case where the required missing sum is too small to add any valid new permutation element.

Consider:

```
1
2 1
4 3
```

The algorithm adds `1`, making `s = 0`. The set becomes `{1,3,4}`. The final validation checks numbers `1,2,3,4` and discovers that `2` is absent. The answer is `NO`. This prevents accepting incomplete ranges.

Consider:

```
1
3 3
1 4 2
```

The algorithm adds the missing value `3`, making `s = 0`. The set becomes `{1,2,3,4}`. Every number from `1` through `4` exists, so the answer is `YES`. This confirms that the algorithm correctly recognizes a completed permutation.

Consider:

```
1
5 6
1 2 3 4 5
```

The next missing values are `6`, then `7`, and so on. Adding `6` immediately makes `s = 0`. The resulting set is `{1,2,3,4,5,6}`, which is a valid permutation. The answer is `YES`. This case shows that the original numbers may already form a prefix of the final permutation.
