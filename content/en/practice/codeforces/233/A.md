---
title: "CF 233A - Perfect Permutation"
description: "We need to construct a permutation of numbers from 1 to n with two conditions. The first condition is p[p[i]] = i for every position i. Applying the permutation twice must return us to the original index. This means every element points back to its partner."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 233
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 144 (Div. 2)"
rating: 800
weight: 233
solve_time_s: 86
verified: true
draft: false
---

[CF 233A - Perfect Permutation](https://codeforces.com/problemset/problem/233/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct a permutation of numbers from `1` to `n` with two conditions.

The first condition is `p[p[i]] = i` for every position `i`. Applying the permutation twice must return us to the original index. This means every element points back to its partner.

The second condition is `p[i] != i` for every `i`. No element is allowed to stay in its own position.

Together, these conditions force the permutation to consist entirely of swaps between pairs of indices. If `i` maps to `j`, then `j` must map back to `i`, and neither can map to themselves.

The input contains a single integer `n`, the size of the permutation. The output is either one valid perfect permutation or `-1` if no such permutation exists.

The constraint is very small, `n ≤ 100`, so performance is not a concern. Even brute force would technically fit. The real challenge is recognizing the mathematical structure hidden inside the conditions.

The tricky cases come from odd values of `n`.

For example:

Input:

```
1
```

Output:

```
-1
```

There is only one possible permutation, `[1]`, but it violates `p[i] != i`.

Another important case:

Input:

```
3
```

A careless approach might try:

```
2 1 3
```

The first two positions form a valid swap, but position `3` maps to itself, which is forbidden.

The smallest valid case is:

Input:

```
2
```

Output:

```
2 1
```

Here:

`p[1] = 2`

`p[2] = 1`

Applying the permutation twice returns to the original index, and no position stays fixed.

## Approaches

A brute-force solution would generate every permutation of size `n` and check whether it satisfies both conditions. The check itself is easy. For each index `i`, verify that `p[p[i]] == i` and `p[i] != i`.

This works because the constraints are tiny, but factorial growth becomes unreasonable very quickly. Even `10!` already means more than 3 million permutations. A full brute-force search is unnecessary once we understand what the conditions imply.

The key observation is that the permutation must be composed entirely of disjoint pairs.

Suppose `p[i] = j`. Since `p[p[i]] = i`, we immediately get:

```
p[j] = i
```

So every element must belong to a 2-cycle:

```
i <-> j
```

Single-element cycles are forbidden because `p[i] != i`.

That means the array must be partitioned into pairs. This is only possible when `n` is even.

Once we see that, construction becomes trivial. We simply swap adjacent numbers:

```
1 <-> 2
3 <-> 4
5 <-> 6
...
```

For example, when `n = 6`:

```
2 1 4 3 6 5
```

Applying the permutation twice returns every index to itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! × n) | O(n) | Too slow conceptually |
| Optimal | O(n) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Check whether `n` is odd.

If `n` is odd, print `-1` and stop. A perfect permutation consists entirely of pairs, so an odd number of elements always leaves one unpaired element.
3. Otherwise, iterate through numbers from `1` to `n` in steps of `2`.
4. For each pair `(i, i + 1)`, output:

```
i + 1, i
```

This creates a 2-cycle:

```
i -> i + 1
i + 1 -> i
```
5. Print the constructed permutation.

### Why it works

Every pair `(i, i + 1)` forms a swap. For any element inside the pair, applying the permutation once moves to the partner, and applying it again returns to the original position.

For example:

```
p[i] = i + 1
p[i + 1] = i
```

Then:

```
p[p[i]] = p[i + 1] = i
```

No element maps to itself because every element swaps with another element.

Since the entire permutation is made from independent 2-cycles, the conditions hold for all indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n % 2 == 1:
        print(-1)
        return

    ans = []

    for i in range(1, n + 1, 2):
        ans.append(str(i + 1))
        ans.append(str(i))

    print(" ".join(ans))

solve()
```

The first condition handled in the code is whether `n` is odd. An odd-sized set cannot be completely partitioned into pairs, so no perfect permutation exists.

The loop advances by `2` each time because we process indices in pairs. For every pair `(i, i + 1)`, the numbers are appended in reversed order. This directly creates the required 2-cycle structure.

The implementation uses strings inside the list to avoid repeated integer-to-string conversions during output construction.

The bounds are tiny, but the solution still runs in linear time and uses fast input style consistent with competitive programming conventions.

## Worked Examples

### Example 1

Input:

```
1
```

Execution trace:

| Step | n | Condition | Action |
| --- | --- | --- | --- |
| 1 | 1 | n is odd | Print `-1` |

Output:

```
-1
```

This demonstrates the impossibility of pairing all elements when the size is odd.

### Example 2

Input:

```
4
```

Execution trace:

| Iteration | i | Added values | Current permutation |
| --- | --- | --- | --- |
| 1 | 1 | 2, 1 | 2 1 |
| 2 | 3 | 4, 3 | 2 1 4 3 |

Output:

```
2 1 4 3
```

Verification:

| Position | p[i] | p[p[i]] |
| --- | --- | --- |
| 1 | 2 | 1 |
| 2 | 1 | 2 |
| 3 | 4 | 3 |
| 4 | 3 | 4 |

Each element returns to itself after two applications, and no element stays fixed after one application.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is processed exactly once |
| Space | O(n) | The output array stores the permutation |

The maximum value of `n` is only `100`, so this solution easily fits within the time and memory limits. Even much slower solutions would pass, but the linear construction is the intended mathematical observation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    if n % 2 == 1:
        print(-1)
        return

    ans = []

    for i in range(1, n + 1, 2):
        ans.append(str(i + 1))
        ans.append(str(i))

    print(" ".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("1\n") == "-1\n", "sample 1"

# smallest valid case
assert run("2\n") == "2 1\n", "n = 2"

# small even case
assert run("4\n") == "2 1 4 3\n", "n = 4"

# odd size greater than 1
assert run("5\n") == "-1\n", "odd n"

# maximum boundary
expected = "2 1 4 3 6 5 8 7 10 9 12 11 14 13 16 15 18 17 20 19 22 21 24 23 26 25 28 27 30 29 32 31 34 33 36 35 38 37 40 39 42 41 44 43 46 45 48 47 50 49 52 51 54 53 56 55 58 57 60 59 62 61 64 63 66 65 68 67 70 69 72 71 74 73 76 75 78 77 80 79 82 81 84 83 86 85 88 87 90 89 92 91 94 93 96 95 98 97 100 99\n"
assert run("100\n") == expected, "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `-1` | Minimum impossible case |
| `2` | `2 1` | Smallest valid permutation |
| `4` | `2 1 4 3` | Multiple independent swaps |
| `5` | `-1` | Odd size rejection |
| `100` | alternating swaps | Maximum boundary case |

## Edge Cases

The first critical edge case is when `n = 1`.

Input:

```
1
```

The algorithm immediately checks parity:

```
1 % 2 == 1
```

Since the value is odd, it prints:

```
-1
```

This is correct because the only possible permutation is:

```
1
```

which violates the requirement `p[i] != i`.

Another subtle case is any larger odd value, such as:

Input:

```
3
```

The algorithm again detects odd parity and prints:

```
-1
```

This avoids a common mistake where someone swaps only the first two elements:

```
2 1 3
```

Here, the third position maps to itself, so the permutation is invalid.

A boundary case with the largest allowed even value is:

Input:

```
100
```

The algorithm generates:

```
2 1 4 3 6 5 ...
```

Every adjacent pair forms a valid 2-cycle. No index is left unmatched, and all conditions remain satisfied across the full range from `1` to `100`.
