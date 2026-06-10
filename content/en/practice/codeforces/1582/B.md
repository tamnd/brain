---
title: "CF 1582B - Luntik and Subsequences"
description: "We are given several arrays. For each array, let the sum of all elements be $s$. We need to count how many subsequences have sum exactly $s-1$. A subsequence is formed by deleting any number of elements, possibly none of them or all of them."
date: "2026-06-10T09:58:23+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 900
weight: 1582
solve_time_s: 94
verified: true
draft: false
---

[CF 1582B - Luntik and Subsequences](https://codeforces.com/problemset/problem/1582/B)

**Rating:** 900  
**Tags:** combinatorics, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several arrays. For each array, let the sum of all elements be $s$. We need to count how many subsequences have sum exactly $s-1$.

A subsequence is formed by deleting any number of elements, possibly none of them or all of them. The order of the remaining elements stays unchanged.

The array length is at most 60, which is small enough to scan the array directly, but the number of subsequences is $2^{60}$, which is enormous. Enumerating all subsequences is completely impossible. Even $2^{40}$ operations would already be too many for a one second limit.

The values themselves can be as large as $10^9$, but that does not matter much because we never need dynamic programming over sums. The structure of the problem turns out to depend only on how many zeros and ones appear.

Several edge cases are easy to miss.

Consider

```
1
2
1 0
```

The total sum is 1. We need subsequences whose sum is 0. Both the empty subsequence and the subsequence containing only 0 satisfy this, so the answer is 2. A solution that forgets the empty subsequence would return 1.

Consider

```
1
2
1000 1000
```

The total sum is 2000. To obtain 1999, we would have to remove elements summing to 1, but there is no such element or combination. The answer is 0. A careless approach might incorrectly assume that every array has at least one valid subsequence.

Another interesting case is

```
1
4
1 1 0 0
```

The total sum is 2. A nearly full subsequence must have sum 1. We can remove exactly one of the ones, and each remaining set of zeros may be chosen independently. Since there are two zeros, that contributes $2^2=4$ choices. There are two ways to choose which one is removed, so the answer is $2 \times 4 = 8$.

## Approaches

A brute-force solution checks every subsequence, computes its sum, and counts how many equal $s-1$. This works because the definition directly asks about subsequences. The problem is the number of subsequences. With $n=60$, there are

$$2^{60}\approx 1.15\times 10^{18}$$

possibilities, which is far beyond anything practical.

The key observation comes from looking at the complement. A subsequence with sum $s-1$ means that the removed elements have total sum 1.

Since all numbers are non-negative, the only way for removed elements to sum to 1 is to remove exactly one element equal to 1 and remove no positive number larger than 1.

Zeros do not affect sums, so each zero may either stay or be removed independently. If there are $z$ zeros and $o$ ones, we have $o$ choices for which one is removed and $2^z$ ways to decide which zeros remain.

The answer is simply

$$o \times 2^z$$

Scanning the array once gives both counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read one test case.
2. Count how many elements are equal to 0. Let this count be $z$.

Zeros are special because including or excluding them never changes the sum.
3. Count how many elements are equal to 1. Let this count be $o$.

A valid subsequence must exclude exactly one element whose value is 1.
4. Compute the answer as

$$o \times 2^z$$

There are $o$ choices for the removed one, and every zero independently has two possibilities.
5. Output the result.

### Why it works

Suppose a subsequence has sum $s-1$. Equivalently, the removed elements have sum 1.

Because every array element is non-negative, no element greater than 1 can be removed. Removing two or more ones would already contribute at least 2. Thus exactly one element equal to 1 must be removed.

Zeros contribute nothing to the removed sum, so they may be either removed or kept without affecting validity.

Every valid subsequence corresponds to one choice of a removed one and one independent choice for each zero. Conversely, every such combination produces a valid subsequence. Since this correspondence is one-to-one, the count is exactly $o \times 2^z$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    zeros = 0
    ones = 0

    for x in a:
        if x == 0:
            zeros += 1
        elif x == 1:
            ones += 1

    print(ones * (1 << zeros))
```

The program processes each test case independently.

The loop over the array counts zeros and ones. Values larger than 1 are ignored because they can never belong to the removed set whose sum must equal 1.

The expression `1 << zeros` computes $2^{\text{zeros}}$. With at most 60 elements, the largest value is $2^{60}$, which easily fits inside Python's arbitrary-precision integers.

The order of multiplication does not matter. If there are no ones, the answer automatically becomes zero.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| Step | zeros | ones | Answer |
| --- | --- | --- | --- |
| Start | 0 | 0 | - |
| Read 1 | 0 | 1 | - |
| Read 2 | 0 | 1 | - |
| Read 3 | 0 | 1 | - |
| Read 4 | 0 | 1 | - |
| Read 5 | 0 | 1 | - |
| Final | 0 | 1 | 1 |

Only one element equal to 1 exists, and there are no zeros. We must remove that one element, producing exactly one valid subsequence.

### Example 2

Input:

```
2
1 0
```

| Step | zeros | ones | Answer |
| --- | --- | --- | --- |
| Start | 0 | 0 | - |
| Read 1 | 0 | 1 | - |
| Read 0 | 1 | 1 | - |
| Final | 1 | 1 | 2 |

The single one must be removed. The zero may either stay or be removed, giving two possibilities. One corresponds to the subsequence `(0)`, and the other corresponds to the empty subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass over the array |
| Space | $O(1)$ | Only two counters are stored |

Since $n\le 60$, the work per test case is tiny. Even with 1000 test cases, the program performs only about sixty thousand element inspections, which is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        zeros = 0
        ones = 0

        for x in a:
            if x == 0:
                zeros += 1
            elif x == 1:
                ones += 1

        ans.append(str(ones * (1 << zeros)))

    return "\n".join(ans)

# provided samples
assert run(
"""5
5
1 2 3 4 5
2
1000 1000
2
1 0
5
3 0 2 1 1
5
2 1 0 3 0
"""
) == """1
0
2
4
4"""

# minimum size
assert run(
"""1
1
0
"""
) == "0"

# single one
assert run(
"""1
1
1
"""
) == "1"

# all zeros
assert run(
"""1
4
0 0 0 0
"""
) == "0"

# multiple ones and zeros
assert run(
"""1
4
1 1 0 0
"""
) == "8"

# maximum-style case with many zeros
assert run(
"""1
5
1 0 0 0 0
"""
) == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | 0 | No one exists, answer must be zero |
| `1` | 1 | Single element array |
| `0 0 0 0` | 0 | All zeros |
| `1 1 0 0` | 8 | Multiple removable ones and independent zero choices |
| `1 0 0 0 0` | 16 | Correct computation of $2^z$ |

## Edge Cases

Consider

```
1
2
1 0
```

We have `ones = 1` and `zeros = 1`. The algorithm returns

$$1 \times 2^1 = 2$$

The two valid subsequences are `(0)` and the empty subsequence. Since zeros can be removed freely, the algorithm naturally counts both.

Consider

```
1
2
1000 1000
```

There are no ones and no zeros. The algorithm computes

$$0 \times 2^0 = 0$$

No collection of removed elements can have sum 1, so the answer is correctly zero.

Consider

```
1
4
1 1 0 0
```

The counters become `ones = 2` and `zeros = 2`. The answer is

$$2 \times 2^2 = 8$$

Exactly one of the two ones must be removed. Each zero may independently stay or disappear. The algorithm counts all eight possibilities without enumerating subsequences.
