---
title: "CF 104835C - Baklava Baking"
description: "We are looking at 9-digit numbers that represent possible baklava layer counts. Each such number is a valid configuration, so the search space is simply all integers from 100,000,000 to 999,999,999 inclusive. There are two conditions attached to a valid configuration."
date: "2026-06-28T11:45:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104835
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 12-01-23 Div. 2 (Beginner)"
rating: 0
weight: 104835
solve_time_s: 65
verified: true
draft: false
---

[CF 104835C - Baklava Baking](https://codeforces.com/problemset/problem/104835/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at 9-digit numbers that represent possible baklava layer counts. Each such number is a valid configuration, so the search space is simply all integers from 100,000,000 to 999,999,999 inclusive.

There are two conditions attached to a valid configuration. First, if we reverse the digits of the number, the resulting number must be divisible by 5. Second, the original number itself must be divisible by a given value $K$, which changes across test cases. For each $K$, we need to count how many 9-digit numbers satisfy both conditions simultaneously.

The key observation about divisibility by 5 is that it depends only on the last digit of the reversed number. A number is divisible by 5 if and only if its last digit is either 0 or 5. After reversing a 9-digit number, the last digit becomes the first digit of the original number. Since all valid numbers are 9-digit integers, their first digit is in the range 1 to 9, so the only way for the reversed number to end in 0 or 5 is for the original number to start with 5. This collapses the problem to counting 9-digit numbers starting with digit 5 that are divisible by $K$.

So we are effectively working with numbers of the form:

$$5xxxxxxx x$$

where the remaining 8 digits are free.

The constraints are very large. The number of test cases can be up to $10^5$, and each query asks for a count over a range of up to $10^8$ numbers. Any per-query linear scan over the range is impossible. Even an $O(\sqrt{N})$ or $O(\log N)$ per number strategy would fail.

Edge cases appear when $K$ is large or small. If $K = 1$, every valid 9-digit number starting with 5 is counted. If $K > 999,999,999$, the answer becomes 0 or 1 depending on divisibility structure, but brute forcing divisibility per candidate is infeasible. Another subtle edge case is when reasoning incorrectly assumes uniform divisibility over ranges without considering alignment of multiples.

## Approaches

A brute-force method would iterate over all 900 million possible 9-digit numbers, check whether the first digit is 5, and test divisibility by $K$. Even if checking divisibility is constant time, this is on the order of $10^9$ operations per query, which is far beyond limits.

The structure of the problem is more arithmetic than combinatorial. Once we restrict to numbers starting with 5, we are essentially looking at an arithmetic progression:

$$500000000 \text{ to } 599999999$$

We need to count how many integers in this interval are divisible by $K$.

This transforms the problem into a classic range counting of multiples. Instead of enumerating values, we compute how many multiples of $K$ lie in a closed interval using prefix division:

$$\text{count} = \left\lfloor \frac{R}{K} \right\rfloor - \left\lfloor \frac{L-1}{K} \right\rfloor$$

The divisibility-by-5 constraint has already been absorbed into the interval restriction, so no additional filtering is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^9)$ per query | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Restrict the universe of valid numbers to those whose reversed form ends in 0 or 5. This forces the original number to begin with digit 5, so we define the interval $[L, R] = [500000000, 599999999]$. This removes the digit-reversal condition entirely by converting it into a structural constraint on the number itself.
2. For each test case, read the integer $K$, which defines the divisibility condition for the original number. The task becomes counting how many numbers in $[L, R]$ are divisible by $K$.
3. Compute how many multiples of $K$ are less than or equal to $R$ using integer division $R // K$. This gives the total count of valid multiples up to the upper bound.
4. Compute how many multiples of $K$ are strictly less than $L$ using $(L-1) // K$. This removes all invalid multiples that fall below the interval.
5. Subtract the two values to obtain the number of valid multiples in the range. This directly corresponds to the number of valid baklava configurations for that $K$.

### Why it works

Every valid configuration corresponds to exactly one integer in the interval $[500000000, 599999999]$. The divisibility condition by $K$ partitions integers into disjoint arithmetic progressions of step $K$. Counting how many elements of an interval lie in such a progression is fully determined by boundary alignment, so the floor-division formula is exact and avoids overcounting or missing edge elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

L = 500_000_000
R = 599_999_999

def solve():
    t = int(input())
    for _ in range(t):
        k = int(input())
        if k == 0:
            print(0)
            continue
        ans = R // k - (L - 1) // k
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution fixes the valid universe once at the start, which avoids recomputing boundaries for each query. Each query then reduces to two integer divisions and one subtraction.

A subtle point is handling $K = 0$, although the constraints typically prevent it. The guard ensures robustness, but logically such a case contributes zero valid numbers since divisibility by zero is undefined.

## Worked Examples

We use the provided sample.

### Example 1

Input interval is fixed $[500000000, 599999999]$.

| K | R // K | (L-1) // K | Answer |
| --- | --- | --- | --- |
| 1 | 599999999 | 499999999 | 100000000 |
| 2 | 299999999 | 249999999 | 50000000 |
| 3 | 199999999 | 166666666 | 33333333 |

The pattern shows that as $K$ increases, the density of multiples decreases proportionally.

This confirms that we are not iterating over numbers but counting arithmetic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each query performs constant-time arithmetic operations |
| Space | $O(1)$ | Only fixed bounds and a few variables are stored |

The solution comfortably handles $10^5$ queries because each one is reduced to two integer divisions, which are constant time operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    L = 500_000_000
    R = 599_999_999

    t = int(input())
    out = []
    for _ in range(t):
        k = int(input())
        out.append(str(R // k - (L - 1) // k))
    return "\n".join(out)

# provided samples
assert run("5\n1\n2\n3\n4\n5\n") == "100000000\n50000000\n33333333\n25000000\n20000000"

# custom cases
assert run("1\n1000000000\n") == "0", "k larger than range"
assert run("1\n500000000\n") == "1", "exact boundary match"
assert run("1\n999999999\n") == "0", "no multiple in range"
assert run("3\n1\n2\n3\n") == "100000000\n50000000\n33333333", "mixed small k values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k > R | 0 | no multiples exist |
| k = L | 1 | boundary inclusion |
| k very large | 0 | sparse divisibility |
| small k set | scaled counts | consistent arithmetic progression behavior |

## Edge Cases

A tricky case is when $K$ is larger than the upper bound $R = 599999999$. For example, if $K = 10^9$, both $R // K$ and $(L-1) // K$ are zero, producing an answer of zero. The algorithm naturally handles this without special branching.

Another case is when $K = 1$. Then every number in the interval is valid. The formula gives:

$$599999999 - 499999999 = 100000000$$

which matches exactly the number of 9-digit numbers starting with 5.

Finally, when $K$ divides values near the boundary, such as $K = 500000000$, the interval contains exactly one multiple, namely 500000000 itself. The subtraction correctly preserves inclusion of boundary points, confirming correctness at edges.
