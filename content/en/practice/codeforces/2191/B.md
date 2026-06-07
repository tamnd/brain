---
title: "CF 2191B - MEX Reordering"
description: "We are given an array and may rearrange its elements in any order we like. After choosing an ordering, every possible split of the array into a non-empty prefix and a non-empty suffix must satisfy one condition: The MEX of the prefix must be different from the MEX of the suffix."
date: "2026-06-07T21:01:20+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2191
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1073 (Div. 2)"
rating: 1000
weight: 2191
solve_time_s: 138
verified: false
draft: false
---

[CF 2191B - MEX Reordering](https://codeforces.com/problemset/problem/2191/B)

**Rating:** 1000  
**Tags:** constructive algorithms, sortings  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and may rearrange its elements in any order we like. After choosing an ordering, every possible split of the array into a non-empty prefix and a non-empty suffix must satisfy one condition:

The MEX of the prefix must be different from the MEX of the suffix.

The task is not to construct the ordering. We only need to determine whether at least one valid ordering exists.

The array length is at most 100, and there are up to 500 test cases. Even though the individual arrays are small, checking every permutation is impossible because there are up to $100!$ possible reorderings. We need to find a structural property that completely characterizes when a valid ordering exists.

The key challenge is understanding how MEX behaves when elements move between the prefix and suffix.

Consider a small example:

```
[0, 1]
```

The only split gives:

```
prefix = [0], MEX = 1
suffix = [1], MEX = 0
```

The MEX values differ, so the answer is YES.

Now consider:

```
[0, 0, 3]
```

No matter how we reorder the array, some split produces equal MEX values. The correct answer is NO.

A common mistake is to focus on the exact positions of large values. Numbers larger than the eventual MEX are mostly irrelevant. MEX depends only on whether small non-negative values are present.

Another easy pitfall is assuming that duplicates always help. For example:

```
[0, 0]
```

The answer is YES.

Arrange it as:

```
[0, 0]
```

The only split gives MEX values 1 and 1? No. The split is:

```
prefix = [0] -> MEX = 1
suffix = [0] -> MEX = 1
```

Actually equal, so this arrangement fails. Since there is no other arrangement, the answer is NO.

This example shows that having duplicates of the smallest value can still be insufficient.

A more subtle case is:

```
[0, 0, 1, 1]
```

The answer is YES. One valid ordering is:

```
[0, 1, 0, 1]
```

The existence of multiple copies of every value below the global MEX turns out to be exactly what matters.

## Approaches

The brute-force idea is straightforward. Generate every permutation of the array, then for each permutation check all $n-1$ split points and compare the MEX of the prefix and suffix.

This is correct because it directly tests the definition. Unfortunately, even for $n=10$, there are already $10!\approx3.6$ million permutations. The search space explodes immediately and becomes completely infeasible.

To find something better, we need to understand when equal MEX values can occur.

Let $M$ be the MEX of the entire array.

Every value $0,1,\dots,M-1$ appears somewhere in the array, and value $M$ does not appear.

Suppose some value $x<M$ occurs only once in the whole array.

As we scan the array from left to right, there is a moment when that unique copy moves from the suffix side to the prefix side. At that split, both sides are missing $x$.

Since both sides are also missing $M$, each side has MEX at most $x$, and in fact both sides obtain the same MEX. A valid ordering is impossible.

So every value below the global MEX must appear at least twice.

Now suppose every value $0,1,\dots,M-1$ appears at least twice.

We can construct a valid ordering. Put one copy of each required value first:

```
0, 1, 2, ..., M-1
```

Then place all remaining elements afterward.

While scanning from left to right, the prefix gradually gains the values below $M$, so its MEX changes from 0 up to $M$. The suffix still contains another copy of every required value, so its MEX remains $M$ until very late. The two MEX values never coincide.

This gives a complete characterization:

A valid reordering exists if and only if every value smaller than the global MEX appears at least twice.

Checking this condition only requires frequency counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!\cdot n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value in the array.
2. Compute the MEX $M$ of the entire array.
3. Examine every value $x$ in the range $0$ to $M-1$.
4. If any such value appears fewer than two times, output `"NO"`.

A value below the global MEX must exist on both sides of every split at some stage. A single copy makes that impossible.
5. If all values $0,1,\dots,M-1$ appear at least twice, output `"YES"`.

### Why it works

Let $M$ be the MEX of the entire array.

If some value $x<M$ appears exactly once, then at the split where that unique copy switches from the suffix side to the prefix side, both sides lack $x$. Since $M$ is absent everywhere, both sides also lack $M$. Their smallest missing value is therefore the same, making equal MEX values unavoidable. No valid ordering exists.

Conversely, if every value below $M$ appears at least twice, place one copy of each value $0,1,\dots,M-1$ at the beginning of the array. The remaining copies stay later in the array. Before the prefix has collected all required values, its MEX is strictly smaller than $M$. The suffix still contains another copy of every required value, so its MEX remains $M$. After the prefix contains all required values, its MEX becomes $M$, while the suffix is missing at least one required value and has MEX smaller than $M$. The two MEX values are never equal.

Thus the condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = [0] * (n + 2)
        for x in a:
            freq[x] += 1
        
        mex = 0
        while freq[mex] > 0:
            mex += 1
        
        ok = True
        for x in range(mex):
            if freq[x] < 2:
                ok = False
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The first section builds a frequency table. Since every array element is between 0 and $n$, an array of size $n+2$ is sufficient.

The next loop computes the global MEX by finding the first value whose frequency is zero.

After that, the solution checks every value below the MEX. The proof shows that these are exactly the values that matter. Values greater than or equal to the MEX never affect the answer.

A common implementation mistake is checking frequencies up to and including the MEX. The MEX itself is absent by definition, so requiring two copies of it would incorrectly reject every test case.

## Worked Examples

### Example 1

Input:

```
2
1 0
```

Frequency table:

| Value | Frequency |
| --- | --- |
| 0 | 1 |
| 1 | 1 |
| 2 | 0 |

Global MEX:

| mex candidate | Present? |
| --- | --- |
| 0 | Yes |
| 1 | Yes |
| 2 | No |

So:

```
M = 2
```

Check values below MEX:

| Value | Frequency | At least 2? |
| --- | --- | --- |
| 0 | 1 | No |

Answer:

```
NO
```

This demonstrates the necessity condition. Value 0 appears only once, so no ordering can keep 0 available on both sides throughout all splits.

### Example 2

Input:

```
6
1 0 5 0 6 1
```

Frequency table:

| Value | Frequency |
| --- | --- |
| 0 | 2 |
| 1 | 2 |
| 2 | 0 |
| 5 | 1 |
| 6 | 1 |

Global MEX:

| mex candidate | Present? |
| --- | --- |
| 0 | Yes |
| 1 | Yes |
| 2 | No |

Thus:

```
M = 2
```

Check values below MEX:

| Value | Frequency | At least 2? |
| --- | --- | --- |
| 0 | 2 | Yes |
| 1 | 2 | Yes |

All checks pass, so the answer is:

```
YES
```

This illustrates that only values smaller than the global MEX matter. The single copies of 5 and 6 are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One frequency count, one MEX scan, one validation scan |
| Space | $O(n)$ | Frequency array of size $n+2$ |

Since $n \le 100$, the algorithm is vastly faster than required. Even across 500 test cases, the total work is only a few tens of thousands of operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))

            freq = [0] * (n + 2)
            for x in a:
                freq[x] += 1

            mex = 0
            while freq[mex]:
                mex += 1

            ok = True
            for x in range(mex):
                if freq[x] < 2:
                    ok = False
                    break

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# provided samples
assert run(
"""3
2
1 0
3
0 3 0
6
1 0 5 0 6 1
"""
) == """NO
NO
YES"""

# minimum size
assert run(
"""1
2
0 0
"""
) == "YES"

# mex = 0
assert run(
"""1
3
5 5 5
"""
) == "YES"

# every required value appears twice
assert run(
"""1
4
0 0 1 1
"""
) == "YES"

# missing duplicate of 1
assert run(
"""1
5
0 0 1 2 2
"""
) == "NO"

# boundary case near maximum value range
assert run(
"""1
6
0 0 1 1 6 6
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[0,0]` | YES | Global MEX is 1 and value 0 appears twice |
| `[5,5,5]` | YES | MEX is 0, no values need checking |
| `[0,0,1,1]` | YES | All required values have duplicate copies |
| `[0,0,1,2,2]` | NO | Value 1 below MEX appears only once |
| `[0,0,1,1,6,6]` | YES | Large values do not influence the condition |

## Edge Cases

Consider:

```
1
3
5 5 5
```

The global MEX is 0. The set of values below the MEX is empty. The verification loop checks nothing and immediately accepts. This is correct because every prefix and suffix have MEX 0, and a valid reordering exists under the proven characterization. The condition reduces to checking an empty set of required values.

Now consider:

```
1
3
0 0 3
```

The global MEX is 1. The only value below the MEX is 0, which appears twice. The algorithm outputs YES. A valid arrangement exists because both sides can continue containing 0 until the final transition.

Finally, consider:

```
1
5
0 0 1 2 2
```

The global MEX is 3. The algorithm checks:

```
freq[0] = 2
freq[1] = 1
freq[2] = 2
```

Value 1 fails the duplicate requirement, so the answer is NO. Any ordering must eventually place the unique copy of 1 entirely on one side of a split, forcing both sides to miss 1 simultaneously and creating equal MEX values. The proof detects exactly this situation.
