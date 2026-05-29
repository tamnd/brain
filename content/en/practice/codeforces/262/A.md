---
title: "CF 262A - Roma and Lucky Numbers"
description: "We are given several integers and a limit k. A digit is called lucky if it is either 4 or 7. For every number in the list, we need to count how many lucky digits appear in its decimal representation. If that count is at most k, the number is considered valid."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 262
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 160 (Div. 2)"
rating: 800
weight: 262
solve_time_s: 144
verified: true
draft: false
---

[CF 262A - Roma and Lucky Numbers](https://codeforces.com/problemset/problem/262/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several integers and a limit `k`. A digit is called lucky if it is either `4` or `7`. For every number in the list, we need to count how many lucky digits appear in its decimal representation. If that count is at most `k`, the number is considered valid. The task is to print how many valid numbers exist.

For example, if the number is `4471`, it contains three lucky digits because the digits `4`, `4`, and `7` are lucky. If `k = 2`, this number does not qualify.

The constraints are very small. There are at most 100 numbers, and each number has at most 10 digits because `a_i ≤ 10^9`. Even a direct digit-by-digit simulation is tiny in terms of work. At worst, we inspect about `100 × 10 = 1000` digits. Any reasonable implementation easily fits within the time limit.

The main danger is not performance but correctness in counting lucky digits.

One easy mistake is checking whether the whole number itself is lucky instead of counting lucky digits inside it. Consider this input:

```
3 1
14 28 74
```

The correct output is:

```
3
```

`14` contains one lucky digit, `28` contains zero, and `74` contains two. Wait, with `k = 1`, only `14` and `28` qualify, so the correct answer is actually:

```
2
```

A careless implementation that only checks whether a number consists entirely of `4` and `7` would produce the wrong result.

Another subtle case is numbers with zero lucky digits. They still count if `k ≥ 0`. Example:

```
2 0
123 456
```

The correct output is:

```
1
```

`123` has zero lucky digits, while `456` has one lucky digit because of the `4`.

A third common bug appears when processing digits using arithmetic operations. If someone repeatedly divides the number by 10 without careful handling, they may forget to process the last digit. For example:

```
1 1
7
```

The correct output is:

```
1
```

Missing the final digit would incorrectly count zero lucky digits.

## Approaches

The most direct solution is to process every number independently and inspect every digit. For each digit, we check whether it equals `4` or `7`. We count how many such digits exist, and if the count does not exceed `k`, we increase the answer.

This brute-force approach is already completely sufficient because the input size is tiny. With at most 100 numbers and at most 10 digits per number, the total amount of work is negligible.

A more complicated strategy is unnecessary because the problem structure is simple. We are not comparing numbers against each other, and there are no large constraints that require preprocessing or advanced data structures. The only useful observation is that each number can be evaluated independently by scanning its digits once.

The optimal solution is effectively the same as the brute-force solution because the straightforward approach already runs in constant practical time for the given limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force digit scanning | O(n × d) | O(1) | Accepted |
| Optimal digit scanning | O(n × d) | O(1) | Accepted |

Here, `d` is the number of digits in a number, at most 10.

## Algorithm Walkthrough

1. Read `n` and `k`.
2. Read the list of `n` integers.
3. Initialize `answer = 0`.
4. For each number:

1. Convert the number to a string so each digit can be inspected easily.
2. Count how many characters are `'4'` or `'7'`.
3. If this count is less than or equal to `k`, increase `answer` by 1.
5. Print `answer`.

The string approach is the cleanest option here because Python strings allow direct iteration over digits without worrying about division or modulo edge cases.

### Why it works

For every number, the algorithm examines every digit exactly once and counts precisely the digits equal to `4` or `7`. A number is counted in the final answer if and only if its lucky digit count is at most `k`, which matches the definition from the problem. Since every number is processed independently and no digits are skipped or double-counted, the algorithm always produces the correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))

    answer = 0

    for number in numbers:
        lucky_count = 0

        for digit in str(number):
            if digit == '4' or digit == '7':
                lucky_count += 1

        if lucky_count <= k:
            answer += 1

    print(answer)

solve()
```

The program starts by reading the input values and storing the numbers in a list.

For each number, the code converts it to a string. This avoids manual digit extraction with `% 10` and `// 10`, which is more error-prone for beginners. Iterating through the string gives direct access to every digit character.

The variable `lucky_count` tracks how many digits are either `4` or `7`. After scanning the whole number, we compare the count with `k`. If the condition is satisfied, we increase the final answer.

One subtle point is the comparison `<= k`. The problem asks for numbers with “not more than” `k` lucky digits, so equality must be included.

## Worked Examples

### Example 1

Input:

```
3 4
1 2 4
```

| Number | Digits | Lucky Digit Count | Count ≤ k | Answer After Processing |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | Yes | 1 |
| 2 | 2 | 0 | Yes | 2 |
| 4 | 4 | 1 | Yes | 3 |

Final output:

```
3
```

This example shows that numbers with zero lucky digits are still valid as long as the count does not exceed `k`.

### Example 2

Input:

```
3 2
447 228 74
```

| Number | Digits | Lucky Digit Count | Count ≤ k | Answer After Processing |
| --- | --- | --- | --- | --- |
| 447 | 4, 4, 7 | 3 | No | 0 |
| 228 | 2, 2, 8 | 0 | Yes | 1 |
| 74 | 7, 4 | 2 | Yes | 2 |

Final output:

```
2
```

This trace demonstrates the boundary condition where a number with exactly `k` lucky digits still qualifies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × d) | Each digit of each number is inspected once |
| Space | O(1) | Only a few counters are used |

Since `n ≤ 100` and each number has at most 10 digits, the total work is extremely small. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))

    answer = 0

    for number in numbers:
        lucky_count = 0

        for digit in str(number):
            if digit == '4' or digit == '7':
                lucky_count += 1

        if lucky_count <= k:
            answer += 1

    print(answer)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("3 4\n1 2 4\n") == "3", "sample 1"

# minimum-size input
assert run("1 0\n1\n") == "1", "single number with zero lucky digits"

# exact boundary case
assert run("2 2\n74 447\n") == "1", "exactly k lucky digits should count"

# all numbers valid
assert run("4 5\n444 777 123 987\n") == "4", "all numbers satisfy condition"

# no numbers valid
assert run("3 0\n4 7 47\n") == "0", "all contain at least one lucky digit"

# mixed case
assert run("5 1\n12 47 400 89 1234\n") == "3", "mixed lucky digit counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 1` | `1` | Minimum-size input |
| `2 2 / 74 447` | `1` | Exact equality with `k` |
| `4 5 / 444 777 123 987` | `4` | Every number accepted |
| `3 0 / 4 7 47` | `0` | Strict zero-lucky-digit condition |
| `5 1 / 12 47 400 89 1234` | `3` | Mixed valid and invalid numbers |

## Edge Cases

Consider the case where numbers contain no lucky digits at all:

```
2 0
123 456
```

The algorithm processes `123` digit by digit. None of its digits are `4` or `7`, so `lucky_count = 0`. Since `0 <= 0`, it is counted.

For `456`, the digit `4` is lucky, so `lucky_count = 1`. Since `1 > 0`, it is rejected.

The final answer is:

```
1
```

This confirms that zero lucky digits is a valid count when `k = 0`.

Now consider a boundary case where the number has exactly `k` lucky digits:

```
1 2
74
```

The digits `7` and `4` are both lucky, so `lucky_count = 2`. The condition checks `2 <= 2`, which is true, so the number is accepted.

The output becomes:

```
1
```

This verifies that equality is included.

Finally, consider a single-digit lucky number:

```
1 1
7
```

The algorithm converts `7` to the string `"7"` and processes its only digit. The lucky count becomes 1, which satisfies the limit.

The output is:

```
1
```

This confirms that no digits are skipped during iteration.
