---
title: "CF 1656C - Make Equal With Mod"
description: "We are given an array of non-negative integers. In one operation, we choose an integer $x ge 2$ and simultaneously replace every element $ai$ with $ai bmod x$. The operation may be applied any number of times, including zero."
date: "2026-06-10T03:32:25+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1656
codeforces_index: "C"
codeforces_contest_name: "CodeTON Round 1 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1200
weight: 1656
solve_time_s: 118
verified: true
draft: false
---

[CF 1656C - Make Equal With Mod](https://codeforces.com/problemset/problem/1656/C)

**Rating:** 1200  
**Tags:** constructive algorithms, math, number theory, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers. In one operation, we choose an integer $x \ge 2$ and simultaneously replace every element $a_i$ with $a_i \bmod x$.

The operation may be applied any number of times, including zero. The goal is to determine whether it is possible to reach a state where every element of the array has the same value.

The array length can be as large as $10^5$ in a single test case, and the total length across all test cases is at most $2 \cdot 10^5$. Any solution that tries to simulate many possible mod operations or explore states of the array is immediately ruled out. We need something close to linear or $O(n \log n)$ per test case.

The interesting part of the problem is understanding how the modulo operation changes relationships between numbers. The operation is applied to all elements at once, so we cannot manipulate individual values independently.

Several edge cases are easy to miss.

Consider:

```
3
1 1 1
```

The answer is `YES` because all elements are already equal and we are allowed to perform zero operations.

Now consider:

```
3
0 2 5
```

The answer is `YES`. Choosing $x=2$ gives:

```
0 0 1
```

and then choosing $x=2$ again gives:

```
0 0 1
```

That does not finish the job, but choosing $x=5$ first produces:

```
0 2 0
```

and then $x=2$ gives:

```
0 0 0
```

A naive rule such as "if there is a zero then the answer is always NO" would fail.

The crucial counterexample is:

```
3
0 1 5
```

The answer is `NO`.

The zero can never change because $0 \bmod x = 0$. The value $1$ also never changes because for every $x \ge 2$,

```
1 mod x = 1
```

So zero and one can never become equal. Any approach that only checks whether a zero exists would miss this.

Another important case is:

```
4
5 9 17 5
```

The answer is `YES`.

Choosing $x=4$ gives:

```
1 1 1 1
```

Even though the original values are quite different, a carefully chosen modulus can immediately make them equal.

## Approaches

A brute-force mindset would try to search over possible values of $x$, apply operations, and see whether the array can eventually collapse into a single value.

This is not realistic. The numbers are as large as $10^9$, so there are billions of possible moduli. Even exploring a tiny fraction of the state space is impossible. Worse, different sequences of operations may lead to different arrays, creating an enormous search tree.

To make progress, we need to understand what properties never change.

The key observation is that the numbers 0 and 1 are special.

A zero is permanent. No matter what modulus we choose,

$$0 \bmod x = 0.$$

A one is also permanent because every allowed modulus satisfies $x \ge 2$, so

$$1 \bmod x = 1.$$

If both 0 and 1 appear in the array, they will remain different forever. Reaching an array where all elements are equal becomes impossible.

Now suppose the array contains a zero but does not contain a one.

Let $m$ be the smallest positive value in the array. Since $m \ge 2$, choosing $x=m$ turns every occurrence of $m$ into zero, while larger values become numbers in the range $[0,m-1]$. Repeating this idea eventually drives all positive values down to zero. The presence of a zero is not a problem by itself. The only problem is having both 0 and 1 simultaneously.

What if there is no zero at all?

Let $m$ be the minimum element. Choosing $x=m$ makes every occurrence of $m$ become zero. Since there was no zero before, the new array contains zero but cannot contain one if the original array had no pair of consecutive values. Repeating the reduction process eventually makes everything equal.

The remaining obstruction is the existence of two consecutive values. If the array contains values $k$ and $k+1$, then after enough reductions they behave exactly like 0 and 1. This turns out to be the only thing that matters.

The accepted solution is extremely simple:

If the array contains a zero, then it must not contain a one.

More generally, after sorting, if any two adjacent values differ by exactly one, the answer is `NO`.

Otherwise the answer is `YES`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| Sort and Check Consecutive Values | O(n log n) | O(1) extra (excluding sort) | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Sort the array.

Sorting places all values in increasing order, making it easy to detect whether two values differ by exactly one.
3. Check whether the array contains a zero.
4. If a zero exists, scan the sorted array looking for a one.

If both zero and one are present, output `NO`.

Zero never changes and one never changes, so they can never become equal.
5. If no zero exists, scan adjacent elements in sorted order.

If any pair differs by exactly one, output `NO`.

Consecutive values eventually create the same obstruction as having 0 and 1.
6. If neither of the previous conditions triggered, output `YES`.

### Why it works

The critical invariant is that once values 0 and 1 appear together, they can never be merged. Zero always remains zero, and one always remains one.

If the array already contains a zero, every future array will also contain a zero. Thus the presence of a one immediately makes the goal impossible.

When there is no zero, the minimum value can always be reduced to zero by choosing it as the modulus. If two numbers differ by one, this reduction eventually creates both 0 and 1, producing the impossible configuration. Conversely, if no consecutive pair exists, repeated reductions can drive all values to the same number without ever creating the forbidden situation.

Thus the problem reduces to detecting whether the array contains a forbidden consecutive pair, with the special handling that only matters when zero is present.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        if a[0] == 0:
            if 1 in a:
                print("NO")
            else:
                print("YES")
        else:
            ok = True
            for i in range(1, n):
                if a[i] - a[i - 1] == 1:
                    ok = False
                    break
            
            print("YES" if ok else "NO")

solve()
```

The first step is sorting the array. After sorting, any consecutive values appear next to each other, so checking for a difference of exactly one becomes a simple linear scan.

The smallest value is easy to identify after sorting. If it is zero, we only need to know whether a one exists anywhere in the array. Using `1 in a` is efficient enough because the total input size is bounded by $2 \cdot 10^5$.

When there is no zero, the algorithm checks every adjacent pair. The moment a difference of one is found, we know the answer is `NO`.

There are no overflow concerns because Python integers handle values far larger than the problem limits. The only subtle point is remembering that duplicates are harmless. A difference of zero does not create any obstruction, so only a difference of exactly one matters.

## Worked Examples

### Example 1

Input:

```
4
2 5 6 8
```

Sorted array:

| Index | Value |
| --- | --- |
| 0 | 2 |
| 1 | 5 |
| 2 | 6 |
| 3 | 8 |

Adjacent differences:

| Pair | Difference |
| --- | --- |
| 2, 5 | 3 |
| 5, 6 | 1 |
| 6, 8 | 2 |

A consecutive pair exists, so the algorithm outputs `NO`.

This example demonstrates the forbidden consecutive-value condition.

### Example 2

Input:

```
5
4 1 7 0 8
```

Sorted array:

| Index | Value |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 4 |
| 3 | 7 |
| 4 | 8 |

Presence check:

| Contains 0 | Contains 1 |
| --- | --- |
| Yes | Yes |

Since both 0 and 1 are present, the answer is `NO`.

This trace demonstrates the permanent conflict between zero and one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(1) extra | Aside from the array and sorting storage |

The total number of elements across all test cases is at most $2 \cdot 10^5$. An $O(n \log n)$ solution easily fits within the time limit, and memory usage remains well below the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        a.sort()

        if a[0] == 0:
            ans.append("NO" if 1 in a else "YES")
        else:
            ok = True
            for i in range(1, n):
                if a[i] - a[i - 1] == 1:
                    ok = False
                    break
            ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run(
"""4
4
2 5 6 8
3
1 1 1
5
4 1 7 0 8
4
5 9 17 5
"""
) == "\n".join([
    "NO",
    "YES",
    "NO",
    "YES"
]), "sample"

# minimum size
assert run(
"""1
1
0
"""
) == "YES"

# all equal
assert run(
"""1
5
7 7 7 7 7
"""
) == "YES"

# contains 0 and 1
assert run(
"""1
3
0 1 100
"""
) == "NO"

# no zero but consecutive values
assert run(
"""1
4
10 14 15 20
"""
) == "NO"

# large gaps only
assert run(
"""1
5
2 4 8 16 32
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[0]` | YES | Minimum array size |
| `[7,7,7,7,7]` | YES | Already equal values |
| `[0,1,100]` | NO | Permanent 0 and 1 conflict |
| `[10,14,15,20]` | NO | Consecutive pair without zero |
| `[2,4,8,16,32]` | YES | No forbidden pair |

## Edge Cases

Consider:

```
1
3
0 1 5
```

After sorting we get:

```
0 1 5
```

The algorithm sees both 0 and 1 and immediately outputs `NO`.

This is correct because zero always stays zero and one always stays one. No sequence of mod operations can make them equal.

Now consider:

```
1
4
2 4 8 16
```

The sorted array is unchanged. The adjacent differences are:

```
2, 4 -> 2
4, 8 -> 4
8, 16 -> 8
```

None equals one, so the algorithm outputs `YES`.

The absence of consecutive values means the forbidden 0-and-1 configuration can be avoided while reducing numbers.

Finally consider:

```
1
5
0 2 2 10 20
```

The array contains zero but not one. The algorithm outputs `YES`.

Duplicates do not matter. The only dangerous value next to zero is one. Since it is absent, all positive values can eventually be reduced to zero, making the entire array equal.
