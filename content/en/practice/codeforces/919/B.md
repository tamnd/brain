---
title: "CF 919B - Perfect Number"
description: "A positive integer is called perfect when the sum of all of its decimal digits is exactly 10. We are given an integer k, and we must output the k-th smallest positive integer whose digit sum equals 10. The ordering is the usual numerical ordering."
date: "2026-06-12T09:48:09+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dp", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 919
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 460 (Div. 2)"
rating: 1100
weight: 919
solve_time_s: 94
verified: true
draft: false
---

[CF 919B - Perfect Number](https://codeforces.com/problemset/problem/919/B)

**Rating:** 1100  
**Tags:** binary search, brute force, dp, implementation, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

A positive integer is called _perfect_ when the sum of all of its decimal digits is exactly 10.

We are given an integer `k`, and we must output the `k`-th smallest positive integer whose digit sum equals 10. The ordering is the usual numerical ordering. For example, the first perfect number is `19` because `1 + 9 = 10`, the second is `28`, and so on.

The constraint is very small. We only need the first `10,000` perfect numbers. That immediately suggests that generating candidates one by one is feasible. The challenge is not handling huge input sizes, but finding a clean way to enumerate perfect numbers in increasing order.

A useful observation is that numbers with digit sum 10 are not rare. Among the first few hundred thousand integers there are already many of them. Since `k ≤ 10000`, even a straightforward search will finish comfortably within the time limit.

There are a few edge cases worth checking.

For input

```
1
```

the answer is

```
19
```

A careless solution that starts searching from `10` and forgets to check every number might miss the very first valid value.

For input

```
2
```

the answer is

```
28
```

A solution that accidentally counts numbers whose digit sum is _at most_ 10 instead of _exactly_ 10 would incorrectly include values such as `10`.

For larger positions, duplicate counting can become an issue if the generation logic is flawed. For example, both `109` and `190` have digit sum 10. We must count every distinct integer exactly once and preserve numerical order.

## Approaches

The most direct idea is to inspect positive integers in increasing order. For each integer, compute the sum of its digits. Whenever the sum equals 10, increase a counter. When the counter reaches `k`, output the current number.

This approach is correct because it examines integers in strictly increasing order and counts exactly those whose digit sum is 10. The moment the counter becomes `k`, we have found the `k`-th smallest perfect number.

The remaining question is whether it is fast enough. The answer is yes. The 10,000-th perfect number is not very large, and computing a digit sum takes only a handful of operations. Even checking a few hundred thousand numbers is trivial within a 2 second limit.

There is also a small observation that appears frequently in accepted solutions. Every perfect number ends with some digit, and appending a trailing `0` does not change the digit sum. One can derive a more specialized generation method from this fact. However, the constraints are so small that the simple enumeration solution is already fully sufficient and easier to reason about.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration | O(N log N) | O(1) | Accepted |
| Direct generation observation | O(k log N) | O(1) | Accepted |

Here `N` denotes the largest number inspected before finding the answer.

## Algorithm Walkthrough

1. Read `k`.
2. Initialize a counter `found = 0`.
3. Start checking integers in increasing order, beginning from `1`.
4. For the current integer, compute the sum of its decimal digits.
5. If the digit sum equals `10`, increment `found`.
6. If `found == k`, output the current integer and stop.
7. Otherwise continue to the next integer.

The key idea is that numbers are processed in increasing order. Every valid number is counted exactly once, so the `k`-th time we encounter a valid number must correspond to the `k`-th smallest perfect number.

### Why it works

At every step, `found` equals the number of perfect numbers encountered among all integers already examined.

This invariant is true initially because no integers have been processed and `found = 0`. Whenever a new integer is checked, we increase `found` exactly when that integer is perfect. Thus the invariant remains true after every iteration.

Since integers are visited in increasing order, when `found` first becomes `k`, exactly `k` perfect numbers have appeared up to and including the current integer. Hence the current integer is precisely the `k`-th smallest perfect number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(x):
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s

def solve():
    k = int(input())
    
    found = 0
    num = 1
    
    while True:
        if digit_sum(num) == 10:
            found += 1
            if found == k:
                print(num)
                return
        num += 1

solve()
```

The function `digit_sum` computes the sum of decimal digits using repeated division by 10.

The main loop scans integers in increasing order. Every time a number has digit sum 10, the counter is increased. As soon as the counter reaches `k`, the current number is printed.

The most common mistake is an off by one error in the counting logic. The comparison must happen after incrementing the counter, because the current number itself may be the answer.

Python integers are unbounded, so there is no overflow concern.

## Worked Examples

### Example 1

Input:

```
1
```

| Current number | Digit sum | Found |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| ... | ... | ... |
| 19 | 10 | 1 |

When `19` is processed, the digit sum equals 10. The counter becomes 1, which matches `k`, so the answer is `19`.

### Example 2

Input:

```
2
```

| Current number | Digit sum | Found |
| --- | --- | --- |
| 19 | 10 | 1 |
| 20 | 2 | 1 |
| 21 | 3 | 1 |
| ... | ... | ... |
| 28 | 10 | 2 |

The first perfect number encountered is `19`. The second is `28`, so the algorithm outputs `28`.

This trace demonstrates that valid numbers are counted in numerical order, which is exactly the ordering required by the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each checked number requires computing its digit sum, which takes O(log N) digits |
| Space | O(1) | Only a few integer variables are stored |

For `k ≤ 10000`, the required search range is small enough that this straightforward enumeration easily fits within the time limit. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    k = int(input())

    def digit_sum(x):
        s = 0
        while x:
            s += x % 10
            x //= 10
        return s

    found = 0
    num = 1

    while True:
        if digit_sum(num) == 10:
            found += 1
            if found == k:
                print(num)
                return
        num += 1

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("1\n") == "19", "sample 1"

# custom cases
assert run("2\n") == "28", "second perfect number"
assert run("3\n") == "37", "third perfect number"
assert run("10\n") == "109", "crosses into three digits"
assert run("20\n") == "208", "larger counting check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `19` | Minimum valid position |
| `2` | `28` | Consecutive counting |
| `3` | `37` | Early sequence correctness |
| `10` | `109` | Transition from two digits to three digits |
| `20` | `208` | Larger counting and ordering |

## Edge Cases

Consider the smallest possible query:

```
1
```

The algorithm checks integers in order. The first number whose digit sum equals 10 is `19`. The counter becomes 1 and matches `k`, so the output is:

```
19
```

This confirms that the search starts early enough and does not skip the first valid answer.

Consider:

```
2
```

The valid numbers encountered are `19`, then `28`. After processing `19`, the counter is 1. After processing `28`, the counter becomes 2 and the algorithm stops. The output is:

```
28
```

This verifies that counting is based on exact digit sum equality rather than any weaker condition.

Consider:

```
10
```

The first ten perfect numbers are:

`19, 28, 37, 46, 55, 64, 73, 82, 91, 109`

The algorithm reaches `109` as the tenth valid number and outputs:

```
109
```

This exercises the transition into three digit numbers and confirms that digit sums are computed correctly regardless of the number of digits.
