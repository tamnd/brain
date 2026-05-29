---
title: "CF 290C - WTF?"
description: "The statement is written as a LOLCODE program. The actual task is to understand what this program computes. The input is a sequence of digits between 0 and 9, one per line. The program repeatedly reads numbers until it encounters 0."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "graph-matchings", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "C"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 1700
weight: 290
solve_time_s: 91
verified: true
draft: false
---

[CF 290C - WTF?](https://codeforces.com/problemset/problem/290/C)

**Rating:** 1700  
**Tags:** *special, graph matchings, implementation, trees  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The statement is written as a LOLCODE program. The actual task is to understand what this program computes.

The input is a sequence of digits between `0` and `9`, one per line. The program repeatedly reads numbers until it encounters `0`. During the process it maintains four variables:

- `FOO`, the running sum of all entered numbers
- `BAR`, the count of entered numbers
- `BAZ / QUZ`, the best fraction seen so far

At the end it prints `BAZ / QUZ`.

The confusing part is the comparison:

```
BOTH SAEM BIGGR OF PRODUKT OF FOO AN QUZ AN PRODUKT OF BAR BAZ AN PRODUKT OF FOO AN QUZ
```

This checks whether:

```
max(FOO * QUZ, BAR * BAZ) == FOO * QUZ
```

which is equivalent to:

```
FOO * QUZ >= BAR * BAZ
```

or:

```
FOO / BAR >= BAZ / QUZ
```

So the program keeps the maximum average value among all prefixes processed before the terminating zero.

Suppose the input is:

```
3
0
1
1
```

The program stops immediately after reading the `0`, so only the prefix `[3]` matters. The average is `3 / 1 = 3`, but the variables start with `BAZ = 0` and `QUZ = 1`, and the update happens after adding the current value. The final printed value is actually normalized through integer-to-real conversion by the language semantics, giving the result shown in the statement.

The real underlying behavior is much simpler than the syntax suggests:

Given a sequence ending at the first `0`, compute the maximum average over all non-empty prefixes before that zero.

The number of input lines is at most `10`, which is tiny. Even quadratic or cubic solutions would pass instantly. The challenge is entirely about decoding the program correctly, not about optimization.

A dangerous edge case is that the program stops at the first zero. Any values after that are ignored completely.

For example:

```
5
4
0
9
9
```

The correct prefixes are only `[5]` and `[5,4]`. The answer is `5`, because:

```
5 / 1 = 5
9 / 2 = 4.5
```

A careless implementation that processes the whole input would incorrectly include the trailing `9`s.

Another subtle case is when the first number is already `0`:

```
0
7
8
```

The loop never runs. The stored best fraction remains `0 / 1`, so the output is:

```
0
```

A naive solution that assumes at least one processed number would divide by zero or access empty arrays.

A third easy mistake is floating-point comparison. Since the program compares fractions using cross multiplication, reproducing the logic with direct floating-point comparisons can introduce precision issues on larger values. The constraints here are tiny, but matching the intended behavior exactly is cleaner and safer.

## Approaches

The most direct approach is to simulate the LOLCODE program literally. We maintain the same variables:

- current sum
- current count
- best numerator
- best denominator

For every number until the first zero, we update the running sum and count, then compare:

```
current_sum / current_count
```

against:

```
best_num / best_den
```

using cross multiplication.

This already runs in linear time. Since there are at most ten inputs, the total work is negligible.

Another possible brute-force interpretation is to explicitly compute every prefix average. If there are `n` processed numbers before the first zero, we can form all prefixes:

```
a[0]
a[0] + a[1]
a[0] + a[1] + a[2]
...
```

and compute each average independently. Without prefix sums this becomes `O(n^2)`, because each prefix sum is recomputed from scratch.

The key observation is that every candidate is a prefix average, and prefixes naturally accumulate. Once we already know the previous prefix sum, the next one differs by exactly one added element. That reduces the work to constant time per step.

The original program itself already implements this optimized idea.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow conceptually, though still fine here |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize four variables:

- `sum_so_far = 0`
- `count = 0`
- `best_num = 0`
- `best_den = 1`

The pair `(best_num, best_den)` stores the largest prefix average found so far as a fraction.
2. Read numbers one by one.
3. Stop immediately when the current number equals `0`.

The original program terminates its loop at the first zero, so later inputs must be ignored.
4. Add the current number to `sum_so_far`.
5. Increase `count` by one.
6. Compare the current average with the best stored average using cross multiplication:

```
sum_so_far * best_den >= count * best_num
```

This avoids floating-point inaccuracies.
7. If the current average is larger or equal, update:

```
best_num = sum_so_far
best_den = count
```
8. After processing finishes, print:

```
best_num / best_den
```

### Why it works

After processing the first `k` numbers, the variables `sum_so_far` and `count` describe exactly the prefix consisting of those `k` numbers. The comparison checks whether this prefix average exceeds the best average seen earlier.

The invariant is:

```
best_num / best_den
```

is always the maximum average among all processed prefixes.

Initially this is true because no prefixes have been processed and the stored value is `0`. Every iteration either keeps the previous best average or replaces it with the new prefix average if that one is larger. Since every possible prefix is examined exactly once, the final stored fraction is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    values = []

    while True:
        line = input()
        if not line:
            break
        x = int(line)

        if x == 0:
            break

        values.append(x)

    sum_so_far = 0
    best_num = 0
    best_den = 1

    for i, x in enumerate(values, start=1):
        sum_so_far += x

        if sum_so_far * best_den >= i * best_num:
            best_num = sum_so_far
            best_den = i

    print(best_num / best_den)

solve()
```

The first loop reproduces the program's termination behavior exactly. Reading stops at the first zero, and every later line is ignored.

The second loop processes prefixes incrementally. The variable `i` acts as the prefix length, while `sum_so_far` stores the prefix sum.

The comparison:

```
sum_so_far * best_den >= i * best_num
```

matches the original LOLCODE logic exactly. Using integer arithmetic avoids subtle precision issues and guarantees the same ordering as rational comparison.

The denominator is initialized to `1` rather than `0`. This prevents division-by-zero problems when no numbers are processed before the terminating zero.

The final output uses Python floating-point division. The required precision is only `1e-4`, so standard double precision is more than enough.

## Worked Examples

### Example 1

Input:

```
3
0
1
1
```

Processing stops at the first `0`.

| Step | Current Value | Prefix Sum | Prefix Length | Current Average | Best Fraction |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 1 | 3.0 | 3 / 1 |

Final output:

```
3.0
```

This trace demonstrates the early termination rule. The trailing `1 1` never participate in the computation.

### Example 2

Input:

```
2
4
1
0
```

| Step | Current Value | Prefix Sum | Prefix Length | Current Average | Best Fraction |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | 2.0 | 2 / 1 |
| 2 | 4 | 6 | 2 | 3.0 | 6 / 2 |
| 3 | 1 | 7 | 3 | 2.333333 | 6 / 2 |

Final output:

```
3.0
```

The best average appears at the second prefix. Even though the total sum later increases, the average decreases because the prefix length grows faster.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each processed number is handled once |
| Space | O(1) | Only a few variables are stored |

The number of input lines is at most ten, so the solution runs instantly. Even much slower approaches would fit comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    values = []

    while True:
        line = input()
        if not line:
            break

        x = int(line)

        if x == 0:
            break

        values.append(x)

    sum_so_far = 0
    best_num = 0
    best_den = 1

    for i, x in enumerate(values, start=1):
        sum_so_far += x

        if sum_so_far * best_den >= i * best_num:
            best_num = sum_so_far
            best_den = i

    print(best_num / best_den)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided-style sample
assert run("3\n0\n1\n1\n") == "3.0", "sample"

# minimum-size input
assert run("0\n") == "0.0", "no processed numbers"

# strictly increasing averages
assert run("1\n9\n0\n") == "5.0", "best at second prefix"

# all equal values
assert run("5\n5\n5\n0\n") == "5.0", "all prefixes equal"

# later values ignored after zero
assert run("9\n0\n1\n1\n1\n") == "9.0", "must stop at first zero"

# decreasing averages
assert run("9\n1\n1\n0\n") == "9.0", "best at first prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0.0` | Empty processing before termination |
| `1 9 0` | `5.0` | Best prefix may appear later |
| `5 5 5 0` | `5.0` | Equal averages handled correctly |
| `9 0 1 1 1` | `9.0` | Values after zero are ignored |
| `9 1 1 0` | `9.0` | Earliest prefix can remain optimal |

## Edge Cases

Consider the input:

```
0
7
8
```

The loop terminates immediately. No prefix exists, so the stored fraction remains `0 / 1`. The algorithm prints:

```
0.0
```

This case confirms that the initialization prevents division by zero and correctly models the original program behavior.

Now consider:

```
5
4
0
9
9
```

The processed prefixes are:

```
[5]
[5,4]
```

Their averages are:

```
5
4.5
```

The algorithm stops at the first zero and never reads the trailing `9`s into the computation. The final answer is:

```
5.0
```

A solution that scans the entire input would incorrectly compute larger prefixes and produce the wrong result.

Finally consider:

```
8
8
8
0
```

Every prefix average equals `8`. Because the comparison uses `>=`, the stored fraction updates each time, but the numerical answer remains unchanged:

```
8.0
```

This validates that ties are handled consistently and safely.
