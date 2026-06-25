---
title: "CF 106449A - Faking Data"
description: "The problem gives a collection of integers representing a dataset. We need to inspect the first meaningful digit of every number, meaning the leftmost non-zero digit after ignoring the sign."
date: "2026-06-25T09:21:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106449
codeforces_index: "A"
codeforces_contest_name: "2026 Spring UT CS104c Midterm #2"
rating: 0
weight: 106449
solve_time_s: 33
verified: true
draft: false
---

[CF 106449A - Faking Data](https://codeforces.com/problemset/problem/106449/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a collection of integers representing a dataset. We need to inspect the first meaningful digit of every number, meaning the leftmost non-zero digit after ignoring the sign. The task is to decide whether the digit `1` appears as this leading digit more often than every other digit. If it does, the dataset is considered suspicious; otherwise it is not.

For example, the number `-4200` contributes the leading digit `4`, because the minus sign is not part of the number and the first digit that carries value is `4`. The number `0` is a special case because it has no non-zero digit. Since the definition of a leading significant digit does not apply to zero, zero values do not contribute to any digit count.

The input size is the main reason the solution needs to be simple. With up to millions of numbers, we can only afford work proportional to the amount of input. Any approach that compares numbers with each other or repeatedly scans digits in expensive ways would quickly become too slow. Reading each number once and extracting its first digit is enough.

The tricky cases are mostly around extracting the digit correctly. A number such as `-1000` must count as a leading `1`, not `-` or `0`. A number like `0` must not accidentally increase the count of some digit. A number whose first digit is not unique in the input can also expose incorrect comparisons.

Consider the input:

```
3
0 0 1
```

The correct output is:

```
suspicious
```

Only the number `1` contributes, so digit `1` appears once and all other digits appear zero times. A careless implementation that treats zero as having leading digit `0` would still pass here, but it would fail on cases where many zeros exist.

For another example:

```
4
0 0 0 1
```

The correct output is:

```
suspicious
```

Zeros should not compete with digit `1`. Counting zeros as leading digits would incorrectly make digit `0` win.

A negative value also needs attention:

```
2
-999 100
```

The correct output is:

```
suspicious
```

The leading digits are `9` and `1`. The sign must be ignored before extracting the digit.

## Approaches

A direct brute-force approach would collect the leading digit of every number and repeatedly compare frequencies to determine whether digit `1` is the largest. This is correct because the only required information is the frequency of each leading digit. However, if the comparison is implemented by checking every digit against every other digit for every number, it can become unnecessarily large. With `n` numbers, that style can reach around `10n` operations, which is still not terrible here, but it misses the simpler structure of the problem.

The useful observation is that there are only ten possible leading digits. We do not need to store the numbers or perform complicated comparisons. We only need a frequency array of size ten. While reading each number, we find its leading significant digit and increment the corresponding counter. After processing the entire dataset, we compare the count of digit `1` with the maximum count among the other nine digits.

The brute-force method works because the answer depends only on digit frequencies, but it spends effort repeatedly checking information that can be summarized immediately. The frequency array reduces the problem to a single pass over the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10n) | O(1) | Accepted in theory, but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create an array of ten counters, where index `d` stores how many numbers have leading digit `d`.
2. Read each number and remove the sign if it is negative. The absolute value is enough because the leading digit depends only on the magnitude.
3. If the number is zero, ignore it because it has no significant leading digit.
4. For every non-zero number, repeatedly remove the last digits until only the first digit remains. Increment the counter of that digit.
5. After all numbers are processed, compare the count of digit `1` with every other digit count. If it is strictly larger than all of them, print `suspicious`; otherwise print `unfortunately not`.

The reason this works is that the problem only asks about the distribution of leading digits. The algorithm maintains exactly those frequencies and nothing else. Once the counts are known, the answer is determined by a single comparison.

Why it works:

The invariant is that after processing any prefix of the input, the frequency array contains the exact number of occurrences of each leading significant digit among the processed numbers. Each processed non-zero number contributes exactly once to the counter of its true leading digit, while zero contributes nothing. After all numbers are processed, the invariant gives the complete frequency distribution, so checking whether digit `1` has the greatest frequency gives exactly the required result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    cnt = [0] * 10

    nums = input().split()
    for s in nums:
        x = int(s)
        if x == 0:
            continue

        x = abs(x)
        while x >= 10:
            x //= 10

        cnt[x] += 1

    for d in range(10):
        if d != 1 and cnt[1] <= cnt[d]:
            print("unfortunately not")
            return

    print("suspicious")

if __name__ == "__main__":
    solve()
```

The code stores only ten counters because the possible answers are digits from `0` to `9`. The input numbers are processed immediately, so there is no need to keep the whole dataset in memory.

The `abs` call removes the effect of negative signs. The loop dividing by ten moves from a full number toward its first digit. For example, `58320` becomes `5832`, then `583`, then `58`, then `5`.

The zero check happens before this process because repeatedly dividing zero would leave it as zero forever, incorrectly treating it as a valid leading digit. The final loop uses a strict comparison. If another digit has the same frequency as digit `1`, digit `1` is not appearing more often, so the answer must be negative.

## Worked Examples

### Sample 1

Input:

```
5
99999999999 999999999999999 -99999999999 9999999999 420
```

The trace:

| Number | Leading digit | Count of 1 | Other counts changed |
| --- | --- | --- | --- |
| 99999999999 | 9 | 0 | 9 becomes 1 |
| 999999999999999 | 9 | 0 | 9 becomes 2 |
| -99999999999 | 9 | 0 | 9 becomes 3 |
| 9999999999 | 9 | 0 | 9 becomes 4 |
| 420 | 4 | 0 | 4 becomes 1 |

The final counts have digit `9` appearing four times and digit `1` appearing zero times, so the output is:

```
unfortunately not
```

This trace shows that the sign is ignored and only the leading digit matters.

### Sample 2

Input:

```
10
38123 2118328 11273 -44884 18381238 99484832 87372 777372 -588382 123
```

The trace:

| Number | Leading digit | Count of 1 | Count of 9 |
| --- | --- | --- | --- |
| 38123 | 3 | 0 | 0 |
| 2118328 | 2 | 0 | 0 |
| 11273 | 1 | 1 | 0 |
| -44884 | 4 | 1 | 0 |
| 18381238 | 1 | 2 | 0 |
| 99484832 | 9 | 2 | 1 |
| 87372 | 8 | 2 | 1 |
| 777372 | 7 | 2 | 1 |
| -588382 | 5 | 2 | 1 |
| 123 | 1 | 3 | 1 |

Digit `1` appears three times, while every other digit appears at most once. The result is:

```
suspicious
```

This demonstrates the strict comparison requirement. Digit `1` does not need to be the only digit that appears, it only needs to have a larger count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each number is reduced by dividing by ten, where `A` is the absolute value of the number. Since the number of digits is bounded, this is effectively O(n). |
| Space | O(1) | Only ten counters are stored. |

The maximum number of digits is small even for very large integers, so every input value is handled with a tiny constant amount of work. The algorithm easily fits the intended limits because it performs one pass through the dataset.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n_line = input().strip()
    if not n_line:
        return ""

    n = int(n_line)
    cnt = [0] * 10

    for s in input().split():
        x = int(s)
        if x == 0:
            continue
        x = abs(x)
        while x >= 10:
            x //= 10
        cnt[x] += 1

    for d in range(10):
        if d != 1 and cnt[1] <= cnt[d]:
            return "unfortunately not\n"
    return "suspicious\n"

assert solve_io("""5
99999999999 999999999999999 -99999999999 9999999999 420
""") == "unfortunately not\n", "sample 1"

assert solve_io("""10
38123 2118328 11273 -44884 18381238 99484832 87372 777372 -588382 123
""") == "suspicious\n", "sample 2"

assert solve_io("""1
1
""") == "suspicious\n", "single one"

assert solve_io("""5
0 0 0 10 19
""") == "suspicious\n", "zeros ignored"

assert solve_io("""4
-999 -888 123 456
""") == "unfortunately not\n", "negative values and ties"

assert solve_io("""6
111 123 199 1000 0 -100
""") == "suspicious\n", "many leading ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `suspicious` | Minimum non-zero case |
| `0 0 0 10 19` | `suspicious` | Zero values must not count |
| `-999 -888 123 456` | `unfortunately not` | Negative numbers and competing digits |
| `111 123 199 1000 0 -100` | `suspicious` | Repeated leading digit and ignored zero |

## Edge Cases

For the case:

```
3
0 0 1
```

The algorithm skips both zeros, then extracts leading digit `1` from the final number. The count array becomes `cnt[1] = 1` and all other counts remain zero, so the answer is `suspicious`.

For the case:

```
2
-999 100
```

The algorithm converts `-999` into `999`, extracts digit `9`, then extracts digit `1` from `100`. The counts are `cnt[9] = 1` and `cnt[1] = 1`. Since digit `1` is tied instead of strictly larger, the answer is `unfortunately not`.

For a large collection where every value starts with the same digit, such as:

```
5
700 71 7999 0 -7123
```

the algorithm counts four occurrences of leading digit `7` and ignores the zero. Digit `1` does not exceed that count, so it correctly rejects the dataset. This catches solutions that only check whether digit `1` appears frequently rather than checking whether it appears more often than every other digit.
