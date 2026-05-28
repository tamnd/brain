---
title: "CF 199A - Hexadecimal's theorem"
description: "We are given a single integer n, and the statement guarantees that n itself is a Fibonacci number. The task is to represent n as the sum of three Fibonacci numbers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 199
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 125 (Div. 2)"
rating: 900
weight: 199
solve_time_s: 97
verified: true
draft: false
---

[CF 199A - Hexadecimal's theorem](https://codeforces.com/problemset/problem/199/A)

**Rating:** 900  
**Tags:** brute force, constructive algorithms, implementation, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer `n`, and the statement guarantees that `n` itself is a Fibonacci number. The task is to represent `n` as the sum of three Fibonacci numbers. The three values are allowed to repeat, and zero is also a valid Fibonacci number because the sequence starts with `F0 = 0`.

The problem sounds like a number theory search problem at first, but the constraints completely change the situation. The value of `n` is smaller than `10^9`, which means the Fibonacci sequence contains very few relevant numbers. Fibonacci values grow exponentially, so there are only around 45 Fibonacci numbers below `10^9`. Even cubic brute force over all Fibonacci values would still be small enough.

The most dangerous mistake is overthinking the theorem. The statement tries to suggest that we need to prove or search for a decomposition, but the input is already guaranteed to be a Fibonacci number. That immediately creates a trivial construction.

For example, if the input is:

```
5
```

then:

```
0 0 5
```

is already valid because all three numbers are Fibonacci numbers and their sum is `5`.

Another easy mistake is forgetting that `0` is part of the Fibonacci sequence. A careless implementation might generate Fibonacci numbers starting from `1, 1`, which would incorrectly reject valid answers such as:

```
1
```

The correct output can be:

```
0 0 1
```

A third subtle case is the minimum value:

```
0
```

The correct output is:

```
0 0 0
```

Some implementations accidentally treat zero as a special impossible case, even though it is itself a Fibonacci number.

## Approaches

The brute force approach is straightforward. First generate every Fibonacci number up to `10^9`. Since the sequence grows quickly, this list has only about 45 elements. Then try every triple `(a, b, c)` and check whether:

```
a + b + c = n
```

This works because the search space is tiny. Around `45^3 ≈ 91,000` combinations is completely acceptable within a 2 second limit.

The brute force is correct because it explicitly checks every possible combination of Fibonacci numbers. The problem is not performance here, but unnecessary complexity. We are solving a much harder problem than the statement actually requires.

The key observation is that the input itself is guaranteed to be a Fibonacci number. Since zero is also Fibonacci, we can always write:

```
n = 0 + 0 + n
```

This immediately gives a valid construction for every possible input. No searching, dynamic programming, or number theory machinery is needed.

The problem is really testing whether we notice the simplest valid representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k³) | O(k) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

Here `k` is the number of Fibonacci numbers below `10^9`, roughly 45.

## Algorithm Walkthrough

1. Read the integer `n`.
2. Print three Fibonacci numbers whose sum equals `n`.
3. Since `0` is a Fibonacci number and `n` is guaranteed to be a Fibonacci number, output:

```
0 0 n
```

1. This construction always works because:

```
0 + 0 + n = n
```

and all three terms are valid Fibonacci numbers.

### Why it works

The correctness comes directly from the problem guarantees. The Fibonacci sequence includes zero, and the input `n` is guaranteed to belong to the sequence as well. The algorithm outputs exactly three Fibonacci numbers, and their sum equals the required target. There is no input for which this construction fails.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

print(0, 0, n)
```

The implementation is intentionally minimal because the mathematical observation removes all complexity from the problem.

The program reads the given Fibonacci number and immediately prints `0 0 n`. There is no need to generate the Fibonacci sequence or validate anything because the statement already guarantees that `n` is Fibonacci.

One subtle detail is that zero must be treated as a valid Fibonacci number. The entire construction depends on that fact. Since the sequence is defined starting from `F0 = 0`, the output is always legal.

## Worked Examples

### Example 1

Input:

```
3
```

Trace:

| Step | n | Output |
| --- | --- | --- |
| Read input | 3 |  |
| Construct answer | 3 | 0 0 3 |

Verification:

```
0 + 0 + 3 = 3
```

All three values are Fibonacci numbers.

This example demonstrates the core observation of the problem. Even though the sample output uses `1 1 1`, we are free to print any valid decomposition.

### Example 2

Input:

```
0
```

Trace:

| Step | n | Output |
| --- | --- | --- |
| Read input | 0 |  |
| Construct answer | 0 | 0 0 0 |

Verification:

```
0 + 0 + 0 = 0
```

This example exercises the minimum boundary case. The algorithm still works without any special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only input reading and printing are performed |
| Space | O(1) | No extra data structures are used |

The solution easily fits within the limits. It performs a constant amount of work regardless of the input value.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    print(0, 0, n)

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

# provided sample
assert run("3\n") == "0 0 3\n", "sample 1"

# minimum value
assert run("0\n") == "0 0 0\n", "minimum case"

# small Fibonacci number
assert run("1\n") == "0 0 1\n", "small Fibonacci"

# medium Fibonacci number
assert run("13\n") == "0 0 13\n", "medium case"

# large Fibonacci number below 1e9
assert run("832040\n") == "0 0 832040\n", "large Fibonacci"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `0 0 3` | Standard valid decomposition |
| `0` | `0 0 0` | Minimum boundary case |
| `1` | `0 0 1` | Correct handling of repeated small Fibonacci values |
| `13` | `0 0 13` | General correctness |
| `832040` | `0 0 832040` | Large valid Fibonacci input |

## Edge Cases

The first non-obvious case is the smallest possible input:

```
0
```

The algorithm prints:

```
0 0 0
```

The sum is still zero, and all values belong to the Fibonacci sequence. This confirms that the construction handles the lower boundary correctly.

Another subtle case is:

```
1
```

Some implementations accidentally reject this because they forget that repeated Fibonacci numbers are allowed. Our algorithm outputs:

```
0 0 1
```

which is valid immediately.

A more deceptive case is a larger Fibonacci number such as:

```
144
```

The algorithm outputs:

```
0 0 144
```

There is no need to search for combinations like `55 + 89 + 0`. The direct construction always succeeds because the input itself is already Fibonacci.
