---
title: "CF 108B - Datatypes"
description: "We are given several unsigned integer datatypes, each defined by its bit length. A datatype with a bits can store every integer from 0 up to 2^a - 1. We want to know whether there exists some integer x and two datatypes with sizes a[i] < a[j] such that: 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 108
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 83 (Div. 2 Only)"
rating: 1400
weight: 108
solve_time_s: 247
verified: true
draft: false
---

[CF 108B - Datatypes](https://codeforces.com/problemset/problem/108/B)

**Rating:** 1400  
**Tags:** math, sortings  
**Solve time:** 4m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several unsigned integer datatypes, each defined by its bit length. A datatype with `a` bits can store every integer from `0` up to `2^a - 1`.

We want to know whether there exists some integer `x` and two datatypes with sizes `a[i] < a[j]` such that:

1. `x` fits inside the smaller datatype.
2. `x * x` does not fit inside the larger datatype.

If such a pair exists, the language behaves strangely enough that Tuftuf decides to abandon it.

The key observation is that the actual values of `x` matter only through powers of two. Since the maximum number representable in `a` bits is `2^a - 1`, the largest possible square from numbers fitting in `a` bits is roughly `(2^a)^2 = 2^(2a)`. So the question becomes:

Can squaring a number from an `a`-bit type require more than `b` bits, where `a < b`?

The input size reaches `10^5`, so any algorithm that checks every pair directly in quadratic time would perform around `10^10` comparisons in the worst case. That is far beyond what fits in a 2-second limit. We need something closer to `O(n log n)` or `O(n)`.

A subtle part of the problem is that the condition involves existence, not universality. We only need one integer `x` that breaks the larger datatype. A careless solution might test only the maximum value of the smaller datatype and miss simpler witnesses.

Consider this input:

```
2
3 4
```

The correct answer is `"YES"` because `x = 7` fits in 3 bits, but `49` does not fit in 4 bits. A naive implementation that reasons only with bit counts informally might incorrectly think that increasing the datatype by one bit should always be enough.

Another easy mistake is mishandling equal datatype sizes.

```
3
5 5 5
```

The correct answer is `"NO"` because the condition explicitly requires `a[i] < a[j]`. Equal sizes cannot form a valid pair.

A third pitfall is overflow in languages with fixed-width integers. If someone computes `2^a` directly for large `a`, values like `2^10^9` are impossible to store. The intended solution never needs actual powers of two, only relationships between exponents.

## Approaches

The brute-force idea is straightforward. For every ordered pair of datatype sizes `(a, b)` where `a < b`, we ask whether there exists some value fitting in `a` bits whose square exceeds the maximum value representable in `b` bits.

A number fits in `a` bits if:

```
x ≤ 2^a - 1
```

Its square fails to fit in `b` bits if:

```
x^2 > 2^b - 1
```

The largest possible square comes from taking `x = 2^a - 1`. Squaring it gives approximately `2^(2a)`. That means the square can exceed the `b`-bit limit whenever:

```
2a > b
```

So the brute-force solution becomes:

1. Check every pair `(a, b)` with `a < b`.
2. If `2a > b`, answer `"YES"`.

This logic is correct, but checking all pairs costs `O(n^2)`. With `n = 10^5`, this becomes unusable.

The key insight is that only the smallest and largest relevant datatype sizes matter after sorting.

Suppose the array is sorted:

```
a[0] ≤ a[1] ≤ ... ≤ a[n-1]
```

For some datatype size `a[i]`, we want to know whether there exists a larger datatype `a[j]` satisfying:

```
a[j] < 2 * a[i]
```

Because the array is sorted, the easiest candidate is the smallest datatype strictly larger than `a[i]`. If even that datatype is at least `2 * a[i]`, then every later datatype is also too large, and no valid pair exists for this `a[i]`.

So after sorting, we only need to compare neighboring distinct sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(1) apart from sorting | Accepted |

## Algorithm Walkthrough

1. Read the datatype sizes into an array.
2. Sort the array in nondecreasing order.

Sorting lets us examine datatype sizes in increasing order and efficiently reason about larger candidates.
3. Iterate through adjacent pairs in the sorted array.
4. For each adjacent pair `(a[i], a[i+1])`, first check whether they are strictly different.

Equal sizes cannot satisfy the condition because the problem requires `a[i] < a[j]`.
5. If `a[i+1] < 2 * a[i]`, print `"YES"` and terminate.

This means there exists a smaller datatype with size `a[i]` and a larger datatype with size `a[i+1]` such that squaring some number from the smaller type requires more bits than the larger type can hold.
6. If the loop finishes without finding such a pair, print `"NO"`.

### Why it works

A datatype with `a` bits can store numbers up to `2^a - 1`. Squaring the largest possible value gives:

```
(2^a - 1)^2 = 2^(2a) - 2^(a+1) + 1
```

This value is at least `2^b` whenever `2a > b`, which means it no longer fits inside `b` bits.

So the entire problem reduces to finding two datatype sizes with:

```
a < b < 2a
```

After sorting, if such a pair exists anywhere, then there must also exist one among adjacent distinct values. Suppose `(a[i], a[j])` is valid with `i < j`. Since the array is sorted:

```
a[i+1] ≤ a[j] < 2a[i]
```

So the adjacent pair `(a[i], a[i+1])` is already sufficient. Checking adjacent pairs is enough to detect every valid configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    for i in range(n - 1):
        if a[i] < a[i + 1] and a[i + 1] < 2 * a[i]:
            print("YES")
            return

    print("NO")

solve()
```

The first part reads the input and sorts the datatype sizes. Sorting is the foundation of the optimization because it lets us reduce the search to neighboring values.

The loop checks adjacent pairs only. The condition:

```
a[i] < a[i + 1]
```

filters out equal datatype sizes, which are invalid according to the statement.

The second condition:

```
a[i + 1] < 2 * a[i]
```

comes directly from the mathematical derivation. If this inequality holds, then some number fitting in `a[i]` bits has a square that requires more than `a[i+1]` bits.

The implementation never computes actual powers of two, so there is no overflow risk even when datatype sizes reach `10^9`.

The solution exits immediately after finding one valid pair because the problem asks only whether such a pair exists.

## Worked Examples

### Example 1

Input:

```
3
64 16 32
```

After sorting:

```
[16, 32, 64]
```

| i | a[i] | a[i+1] | Distinct? | Check `a[i+1] < 2*a[i]` | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 16 | 32 | Yes | 32 < 32 → No | Continue |
| 1 | 32 | 64 | Yes | 64 < 64 → No | Continue |

No valid pair exists, so the answer is:

```
NO
```

This trace shows the boundary case where the larger datatype is exactly twice the smaller one. Equality is not enough because squaring still fits.

### Example 2

Input:

```
2
3 4
```

After sorting:

```
[3, 4]
```

| i | a[i] | a[i+1] | Distinct? | Check `a[i+1] < 2*a[i]` | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 4 | Yes | 4 < 6 → Yes | Print YES |

The algorithm stops immediately and outputs:

```
YES
```

Indeed, `x = 7` fits in 3 bits, while `49` does not fit in 4 bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(1) apart from sorting | Only a few variables are used |

With `n = 10^5`, an `O(n log n)` solution easily fits within the time limit. The memory usage is minimal because the algorithm works directly on the input array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    for i in range(n - 1):
        if a[i] < a[i + 1] and a[i + 1] < 2 * a[i]:
            print("YES")
            return

    print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("3\n64 16 32\n") == "NO\n", "sample 1"

# sample 2 from statement notes
assert run("2\n3 4\n") == "YES\n", "sample 2"

# minimum size, no valid pair
assert run("2\n1 2\n") == "NO\n", "minimum case"

# all equal values
assert run("4\n5 5 5 5\n") == "NO\n", "equal sizes invalid"

# valid pair appears after sorting
assert run("5\n20 3 100 5 50\n") == "YES\n", "sorting correctness"

# boundary where larger is exactly double
assert run("3\n7 14 28\n") == "NO\n", "strict inequality required"

# large values
assert run("2\n1000000000 1999999999\n") == "YES\n", "large integers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `NO` | Exact doubling is not enough |
| `4 / 5 5 5 5` | `NO` | Equal datatype sizes are invalid |
| `5 / 20 3 100 5 50` | `YES` | Sorting and adjacent checking |
| `3 / 7 14 28` | `NO` | Strict inequality boundary |
| `2 / 1000000000 1999999999` | `YES` | No overflow issues |

## Edge Cases

Consider the case where all datatype sizes are equal.

Input:

```
4
5 5 5 5
```

After sorting, the array stays the same. Every adjacent pair fails the strict comparison:

```
5 < 5
```

So the algorithm never enters the success condition and prints `"NO"`.

This handles the requirement that the larger datatype must truly be larger.

Now consider the exact doubling boundary.

Input:

```
2
16 32
```

The algorithm checks:

```
32 < 2 * 16
32 < 32
```

which is false.

The output is `"NO"` because a 32-bit datatype is exactly large enough to contain squares of all 16-bit numbers.

Finally, consider a case where the valid pair is not adjacent in the original input.

Input:

```
5
100 3 8 20 5
```

After sorting:

```
[3, 5, 8, 20, 100]
```

The algorithm checks adjacent pairs:

```
5 < 6
```

which is true, so it immediately prints `"YES"`.

This demonstrates why sorting is essential. The original order hides the relationship, but the sorted order exposes the smallest larger datatype for each value.
