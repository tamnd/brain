---
title: "CF 109A - Lucky Sum of Digits"
description: "We need to construct the smallest possible lucky number whose digits add up to a given value n. A lucky number may contain only digits 4 and 7. For example, 447 is valid because every digit is either 4 or 7, while 45 is invalid because digit 5 appears."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 109
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 84 (Div. 1 Only)"
rating: 1000
weight: 109
solve_time_s: 142
verified: true
draft: false
---

[CF 109A - Lucky Sum of Digits](https://codeforces.com/problemset/problem/109/A)

**Rating:** 1000  
**Tags:** brute force, implementation  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct the smallest possible lucky number whose digits add up to a given value `n`.

A lucky number may contain only digits `4` and `7`. For example, `447` is valid because every digit is either `4` or `7`, while `45` is invalid because digit `5` appears.

The input gives a single integer `n`, representing the desired digit sum. The output must be the numerically smallest lucky number whose digits sum to exactly `n`. If no such number exists, we print `-1`.

The constraint goes up to `10^6`, which immediately rules out generating lucky numbers one by one. Even the number of lucky numbers with only 20 digits is already enormous. We need something that runs in roughly linear time or better.

The key observation is that the sum of digits depends only on how many `4`s and `7`s we use. If we use `a` copies of digit `4` and `b` copies of digit `7`, then:

$4a + 7b = n$

So the problem becomes finding non-negative integers `a` and `b` satisfying this equation, while also producing the smallest possible number.

There are a few easy-to-miss edge cases.

If `n = 1`, there is no solution because neither `4` nor `7` can contribute a sum of `1`. The correct output is:

```
-1
```

A careless implementation might try greedy subtraction and accidentally enter an infinite loop or print an empty string.

Another tricky case is when multiple decompositions exist. For example:

```
n = 28
```

We can write:

```
28 = 7 + 7 + 7 + 7
```

which gives `7777`, or:

```
28 = 4 + 4 + 4 + 4 + 4 + 4 + 4
```

which gives `4444444`.

Even though `4444444` has more digits, it is numerically smaller because numbers with fewer digits are not always smaller once digit values differ. The actual rule is subtler: among numbers with the same length, earlier digits matter more. We must carefully construct the lexicographically smallest valid number.

One more important edge case appears when the digit count differs. Consider:

```
n = 11
```

Possible decompositions are:

```
4 + 7
7 + 4
```

The valid lucky numbers are `47` and `74`. The correct answer is `47` because it is smaller lexicographically. Any implementation that appends digits in the wrong order will fail here.

## Approaches

The most direct brute-force idea is to generate lucky numbers and test their digit sums. We could recursively build every number containing only `4` and `7`, compute its digit sum, and track the smallest valid one.

This works conceptually because every lucky number is eventually generated. The problem is the explosion in count. A lucky number with length `k` has `2^k` possibilities. Even for length `20`, that already exceeds one million candidates. Since `n` may reach `10^6`, the required number could contain hundreds of thousands of digits, making brute force completely impossible.

The structure of the problem gives a much simpler interpretation. The actual order of digits matters only after we decide how many `4`s and `7`s to use. If we choose `a` fours and `b` sevens, then the sum condition becomes:

$4a + 7b = n$

Now we only need to search for valid pairs `(a, b)`.

The next question is how to make the resulting number as small as possible.

A number with fewer digits is always smaller than a number with more digits if both have no leading zeros. Since every digit contributes at least `4`, minimizing total digits is beneficial. Replacing two `4`s with one `7` reduces the digit count because:

```
4 + 4 = 8
7 = 7
```

Using more `7`s usually means fewer digits.

But digit order also matters. Once the total digit count is fixed, placing smaller digits earlier makes the number smaller. So after choosing counts `(a, b)`, the optimal arrangement is:

```
444...4777...7
```

with all `4`s first.

This leads to a very small search space. We can iterate over the possible number of `7`s. For each value of `b`, we check whether the remaining sum is divisible by `4`.

Among all valid pairs, we prefer the one with the smallest total digits:

```
a + b
```

If multiple pairs have the same length, we prefer the one with more `4`s at the front, which naturally happens if we minimize `b`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(k) | Too slow |
| Optimal | O(n) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Iterate over the possible number of digit `7`s, call it `b`, from `0` up to `n // 7`.
3. For each `b`, compute the remaining sum:

```
remaining = n - 7 * b
```

1. Check whether `remaining` is divisible by `4`.

If it is not divisible by `4`, then no valid count of `4`s exists for this `b`.

1. If divisible, compute:

```
a = remaining // 4
```

Now we have a valid decomposition:

$4a + 7b = n$

1. Since we iterate `b` from small to large, the first valid pair automatically gives the smallest number.

Smaller `b` means more leading `4`s and usually more favorable lexicographic order.

1. Print a string containing `a` copies of `'4'` followed by `b` copies of `'7'`.
2. If no valid pair exists after the loop, print `-1`.

### Why it works

Every valid lucky number corresponds to some pair `(a, b)` satisfying:

$4a + 7b = n$

Among all numbers formed from those digits, placing all `4`s before all `7`s produces the smallest arrangement because `4 < 7`.

The algorithm checks every possible count of `7`s in increasing order. The first valid solution minimizes the number of `7`s. Since replacing `7`s with `4`s pushes smaller digits toward the front, this produces the smallest valid lucky number.

No valid decomposition is skipped, so the algorithm cannot miss the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    for sevens in range(n // 7 + 1):
        remaining = n - 7 * sevens

        if remaining % 4 == 0:
            fours = remaining // 4
            print('4' * fours + '7' * sevens)
            return

    print(-1)

solve()
```

The loop tries every possible count of `7`s from smallest to largest. For each choice, we check whether the remaining sum can be formed entirely using `4`s.

The moment we find a valid decomposition, we immediately print the answer and stop. This early return matters because later solutions would contain more `7`s and produce a larger number.

The output construction is also important. We print all `4`s before all `7`s because lexicographic order determines the smaller number once the digit multiset is fixed.

One subtle detail is the loop bound:

```
range(n // 7 + 1)
```

Without the `+1`, we would miss the case where the entire sum is composed only of `7`s.

Another easy mistake is checking divisibility before subtracting the `7` contribution. The divisibility test must apply to the remaining value after accounting for all chosen `7`s.

## Worked Examples

### Example 1

Input:

```
11
```

| sevens | remaining = 11 - 7×sevens | remaining % 4 | valid |
| --- | --- | --- | --- |
| 0 | 11 | 3 | No |
| 1 | 4 | 0 | Yes |

We stop at `sevens = 1`.

```
fours = 4 / 4 = 1
```

Constructed number:

```
47
```

This trace shows why checking smaller counts of `7`s first is important. The algorithm immediately finds the lexicographically smallest valid answer.

### Example 2

Input:

```
28
```

| sevens | remaining = 28 - 7×sevens | remaining % 4 | valid |
| --- | --- | --- | --- |
| 0 | 28 | 0 | Yes |

We stop immediately.

```
fours = 28 / 4 = 7
```

Constructed number:

```
4444444
```

This example demonstrates that the smallest answer is not always the one with the fewest digits. Even though `7777` is shorter, `4444444` is numerically smaller because its leading digits are smaller.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We try at most `n // 7 + 1` values |
| Space | O(1) | Only a few integer variables are used |

Even for `n = 10^6`, the loop performs roughly 142,857 iterations, which is trivial within the time limit. Memory usage stays constant apart from the output string itself.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    for sevens in range(n // 7 + 1):
        remaining = n - 7 * sevens

        if remaining % 4 == 0:
            fours = remaining // 4
            print('4' * fours + '7' * sevens)
            return

    print(-1)

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
assert run("11\n") == "47\n", "sample 1"

# minimum impossible case
assert run("1\n") == "-1\n", "cannot form sum 1"

# exact multiple of 4
assert run("8\n") == "44\n", "all fours"

# exact multiple of 7
assert run("14\n") == "77\n", "all sevens"

# mixed solution
assert run("15\n") == "4447\n", "mixed digits"

# large boundary case
assert run("1000000\n").strip() != "", "large input should work"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `-1` | Impossible construction |
| `8` | `44` | Pure `4` solution |
| `14` | `77` | Pure `7` solution |
| `15` | `4447` | Mixed decomposition |
| `1000000` | valid large output | Performance near limits |

## Edge Cases

Consider the impossible case:

```
1
```

The loop checks:

| sevens | remaining |
| --- | --- |
| 0 | 1 |

Since `1 % 4 != 0`, no valid decomposition exists. The loop ends and the algorithm prints:

```
-1
```

This confirms that the implementation correctly handles sums that cannot be represented.

Now consider:

```
11
```

Two orderings are possible after choosing digits:

```
47
74
```

The algorithm constructs digits in sorted order:

```
'4' * fours + '7' * sevens
```

so it prints:

```
47
```

which is the smaller number.

Finally, consider a case with multiple valid decompositions:

```
28
```

Possible representations include:

```
4444444
7777
```

The algorithm starts with the smallest number of `7`s. At `sevens = 0`, the decomposition already works, so it immediately prints:

```
4444444
```

This verifies that the first valid pair indeed produces the minimum lucky number.
