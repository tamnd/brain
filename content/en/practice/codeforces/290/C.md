---
title: "CF 290C - WTF?"
description: "The input is not a conventional mathematical specification. Instead, it is a small program written in LOLCODE. The task is to determine what that program computes and print the resulting real number. The first input value is read into a variable that controls a loop."
date: "2026-06-05T16:40:26+07:00"
tags: ["codeforces", "competitive-programming", "*special", "graph-matchings", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "C"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 1700
weight: 290
solve_time_s: 127
verified: true
draft: false
---

[CF 290C - WTF?](https://codeforces.com/problemset/problem/290/C)

**Rating:** 1700  
**Tags:** *special, graph matchings, implementation, trees  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is not a conventional mathematical specification. Instead, it is a small program written in LOLCODE. The task is to determine what that program computes and print the resulting real number.

The first input value is read into a variable that controls a loop. Let that value be `n`. Then the program reads exactly `n` additional digits, each between `0` and `9`.

While processing the sequence, it maintains:

- `FOO`, the sum of all values seen so far.
- `BAR`, the number of values seen so far.
- `BAZ / QUZ`, a fraction representing the best prefix average found so far.

After reading each new value, the program compares the current prefix average

$$\frac{\text{FOO}}{\text{BAR}}$$

with the stored best average

$$\frac{\text{BAZ}}{\text{QUZ}}.$$

If the current average is at least as large, it replaces the stored fraction.

At the end, it prints

$$\frac{\text{BAZ}}{\text{QUZ}},$$

which is exactly the maximum average over all prefixes of the sequence.

Since `n` is itself a digit, it lies between `0` and `9`. The statement says the input contains between 1 and 10 lines, which matches one line for `n` and up to nine additional values. The data size is tiny, so even a quadratic solution would fit comfortably. The real challenge is understanding what the program does.

A common mistake is to search for the maximum individual value instead of the maximum prefix average.

Consider:

```
3
0
1
1
```

The largest value is `1`, but the prefix averages are:

```
0
0.5
0.666667
```

The correct answer is:

```
0.666667
```

Another easy mistake is to maximize the average over arbitrary subarrays instead of prefixes.

For:

```
3
1
0
9
```

The subarray `[9]` has average `9`, but the program only considers prefixes. The prefix averages are:

```
1
0.5
3.333333
```

The correct answer is:

```
3.333333
```

A third subtle point is the comparison between fractions. The original program never converts to floating point. It compares

$$\frac{a}{b} \ge \frac{c}{d}$$

by checking

$$a \cdot d \ge c \cdot b.$$

Using floating point here would still work for this problem because the numbers are tiny, but reproducing the program exactly is cleaner with integer arithmetic.

## Approaches

The most direct interpretation is to simulate the program literally.

We read the sequence, compute every prefix average, keep the largest one seen so far, and print it at the end. Since there are at most nine values, even storing all averages and scanning them later would be trivial.

The interesting part is understanding how the program itself performs the comparison. Instead of computing real numbers, it stores the best average as a fraction `BAZ / QUZ`. When a new prefix with sum `FOO` and length `BAR` appears, it compares

$$\frac{\text{FOO}}{\text{BAR}}$$

and

$$\frac{\text{BAZ}}{\text{QUZ}}$$

using cross multiplication:

$$\text{FOO} \cdot \text{QUZ}$$

versus

$$\text{BAR} \cdot \text{BAZ}.$$

This avoids floating point arithmetic entirely.

The brute force idea and the optimal idea are effectively the same here because the input size is so small. We process prefixes once from left to right and maintain the best average seen so far.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (store all prefix averages) | O(n) | O(n) | Accepted |
| Optimal (track best fraction online) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the first number `n`.
2. Initialize:

- `sum_prefix = 0`
- `count = 0`
- `best_sum = 0`
- `best_count = 1`

The fraction `best_sum / best_count` represents the best prefix average found so far.
3. Repeat `n` times:

- Read the next digit `x`.
- Add it to `sum_prefix`.
- Increment `count`.
4. Compare the current prefix average with the stored best average using cross multiplication:

- If

$$\text{sum\_prefix} \cdot \text{best\_count}
\ge
\text{count} \cdot \text{best\_sum},$$

then update:

- `best_sum = sum_prefix`
- `best_count = count`

This is exactly the comparison performed by the LOLCODE program.
5. After all values have been processed, output

$$\frac{\text{best\_sum}}{\text{best\_count}}.$$

### Why it works

After processing any prefix, the pair `(best_sum, best_count)` stores the largest prefix average among all prefixes seen so far.

Initially this is true because the stored value is `0/1`. Whenever a new prefix is processed, we compare its average against the stored maximum. If it is larger or equal, we replace the stored fraction. Otherwise we keep the previous one. By induction, after the final iteration the stored fraction represents the maximum average over all prefixes, which is exactly what the program prints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = [int(line.strip()) for line in sys.stdin if line.strip()]

    n = data[0]

    prefix_sum = 0
    cnt = 0

    best_sum = 0
    best_cnt = 1

    for x in data[1:1 + n]:
        prefix_sum += x
        cnt += 1

        if prefix_sum * best_cnt >= cnt * best_sum:
            best_sum = prefix_sum
            best_cnt = cnt

    print(best_sum / best_cnt)

if __name__ == "__main__":
    solve()
```

The first value determines how many subsequent numbers belong to the sequence. As each value is read, the running sum and prefix length are updated.

The key line is the comparison

```
prefix_sum * best_cnt >= cnt * best_sum
```

which checks whether

$$\frac{\text{prefix\_sum}}{\text{cnt}}
\ge
\frac{\text{best\_sum}}{\text{best\_cnt}}$$

without using floating point arithmetic.

The stored fraction is updated only when the current prefix average is at least as large as the best one seen previously. At the end, dividing the stored numerator and denominator reproduces the program's final output.

## Worked Examples

### Sample 1

Input:

```
3
0
1
1
```

| Step | x | prefix_sum | cnt | best_sum | best_cnt |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 |
| 2 | 1 | 1 | 2 | 1 | 2 |
| 3 | 1 | 2 | 3 | 2 | 3 |

Final answer:

$$\frac{2}{3}=0.666667$$

This trace shows the stored fraction moving from `0/1` to `1/2` and finally to `2/3`, matching the increasing sequence of prefix averages.

### Example 2

Input:

```
3
5
0
0
```

| Step | x | prefix_sum | cnt | best_sum | best_cnt |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 | 1 |
| 1 | 5 | 5 | 1 | 5 | 1 |
| 2 | 0 | 5 | 2 | 5 | 1 |
| 3 | 0 | 5 | 3 | 5 | 1 |

Final answer:

$$\frac{5}{1}=5$$

The first prefix already has the maximum average. Later prefixes have averages `2.5` and `1.666...`, so the stored fraction never changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each value is processed once |
| Space | O(1) | Only a few running variables are stored |

The input size is extremely small, but even for much larger values this linear scan would be efficient. The memory usage remains constant throughout execution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    data = [int(line.strip()) for line in sys.stdin if line.strip()]
    n = data[0]

    prefix_sum = 0
    cnt = 0
    best_sum = 0
    best_cnt = 1

    for x in data[1:1 + n]:
        prefix_sum += x
        cnt += 1

        if prefix_sum * best_cnt >= cnt * best_sum:
            best_sum = prefix_sum
            best_cnt = cnt

    return f"{best_sum / best_cnt}\n"

# provided sample
out = float(run("3\n0\n1\n1\n"))
assert abs(out - 0.666667) < 1e-4

# minimum non-empty sequence
assert run("1\n0\n") == "0.0\n", "single zero"

# single positive value
assert run("1\n9\n") == "9.0\n", "single element"

# best prefix is the first one
assert run("3\n5\n0\n0\n") == "5.0\n", "early maximum"

# all equal values
assert run("4\n7\n7\n7\n7\n") == "7.0\n", "constant average"

# maximum average appears at the end
out = float(run("3\n1\n0\n9\n"))
assert abs(out - (10.0 / 3.0)) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0` | Smallest meaningful sequence |
| `1 9` | `9` | Single-element prefix |
| `3 5 0 0` | `5` | Best prefix occurs immediately |
| `4 7 7 7 7` | `7` | Equal averages throughout |
| `3 1 0 9` | `10/3` | Best prefix occurs at the end |

## Edge Cases

Consider the input

```
1
0
```

There is only one prefix. After processing the value, the stored fraction becomes `0/1`, and the algorithm outputs `0`. No special handling is required.

Consider

```
3
5
0
0
```

The prefix averages are:

```
5
2.5
1.666667
```

The first prefix remains optimal. The cross-multiplication comparison correctly rejects the later prefixes because:

$$5 \cdot 1 > 2 \cdot 5$$

and

$$5 \cdot 1 > 3 \cdot 5.$$

Consider

```
4
7
7
7
7
```

Every prefix average equals `7`. Because the program uses a non-strict comparison (`>=`), it updates the stored fraction on ties. The final stored fraction becomes `28/4`, which still evaluates to `7`. The output remains correct regardless of which equal-average prefix is retained.

Consider

```
3
1
0
9
```

A solution that maximizes arbitrary subarrays would choose `[9]` and return `9`, which is wrong. The algorithm only evaluates prefixes:

```
1
0.5
3.333333
```

and correctly returns `10/3`.
