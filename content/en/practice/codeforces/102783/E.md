---
title: "CF 102783E - Spooky Numbers"
description: "Francine has a collection of decimal digits and wants to arrange some of them into the largest possible spooky number. A spooky number is a non-negative integer divisible by 2, 3, and 5, which means it must be divisible by 30."
date: "2026-07-27T19:58:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 50
verified: true
draft: false
---

[CF 102783E - Spooky Numbers](https://codeforces.com/problemset/problem/102783/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

Francine has a collection of decimal digits and wants to arrange some of them into the largest possible spooky number. A spooky number is a non-negative integer divisible by 2, 3, and 5, which means it must be divisible by 30. She may discard digits, but the remaining digits must be used exactly once in the chosen number, and the resulting number cannot contain unnecessary leading zeroes. The task is to print the largest valid number that can be formed, or `-1` if no valid number exists.

The divisibility rules are the main constraints on the algorithm. Divisibility by 30 is equivalent to divisibility by 3 and having a last digit of 0. Since a number with up to `100000` digits cannot be handled by normal integer operations, any approach that tries to construct and test many possible numbers is impossible. Even generating a small fraction of permutations would be far beyond the available time. The intended solution needs to work by counting digits and using properties of divisibility rather than performing arithmetic on the entire number.

The largest valid number must preserve as many large digits as possible while satisfying the divisibility conditions. A careless implementation can fail on the smallest cases. For example:

```
Input
1
0
```

The correct output is:

```
0
```

A solution that rejects all single-digit numbers because it expects a non-zero leading digit would incorrectly print `-1`.

Another important case is when the digits are not divisible by 3 together. For example:

```
Input
6
2 3 1 3 1 0
```

The correct output is:

```
33210
```

Using every digit gives `332110`, whose digit sum is not divisible by 3. A greedy solution that always keeps every digit would fail, so some digits must be removed.

A third edge case is when the only possible ending digit is missing. For example:

```
Input
4
1 2 3 4
```

The correct output is:

```
-1
```

No arrangement can end in `0`, so no number can be divisible by 30. Sorting the digits alone without checking this condition would produce an invalid answer.

## Approaches

The direct approach is to try possible subsets of digits, arrange each subset in descending order, and check whether the resulting number is divisible by 30. This is correct because the largest valid arrangement would eventually appear among all choices. The problem is the number of possibilities. With `n` digits, there are `2^n` subsets, and even for a few hundred digits this is already impossible. For `n = 100000`, brute force is not remotely close to feasible.

The structure of the problem gives a much simpler path. A number divisible by 30 must end with zero, because divisibility by 10 is required. It must also have a digit sum divisible by 3. The ending zero is a fixed requirement, and the remaining task is only to remove the smallest amount of digit value needed to make the digit sum correct.

Suppose we keep all available digits. If the total digit sum is already divisible by 3, we only need to sort all digits descending. If the remainder is 1, we can either remove one digit whose value has remainder 1, or remove two digits whose values have remainder 2. If the remainder is 2, the symmetric choice applies. To maximize the final number, removing fewer digits is always better, and if we must remove the same number of digits, removing the smallest possible digits gives the largest result.

The divisibility rules reduce the whole problem to maintaining counts of the ten possible digits. Sorting the final digits in descending order gives the maximum numeric value because every kept digit is used and larger digits appear earlier.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each digit appears and calculate the total digit sum. The counts are enough because digits with the same value are interchangeable.
2. Check whether a zero exists. If there is no zero, no number can be divisible by 30, so the answer is impossible. The zero is required as the final digit.
3. Compute the remainder of the digit sum modulo 3. If it is not zero, remove digits that fix the remainder. Removing a single digit is preferable because it keeps more digits. If that is impossible, remove two digits whose combined remainder is correct.
4. After removing the necessary digits, collect all remaining digits in descending order. The largest digits must appear first because the number is compared lexicographically when it has the same length.
5. Handle the special case where all remaining digits are zero. The answer should be a single `0`, not a string containing many zeroes, because those extra zeroes do not increase the value.

Why it works: The only conditions for divisibility by 30 are ending in zero and having a digit sum divisible by 3. The algorithm always keeps the zero requirement satisfied and removes the minimum possible number of digits to repair the digit sum. Among all ways with the same number of removed digits, it removes the smallest digits, leaving the lexicographically largest possible arrangement. Sorting the remaining digits descending then produces the maximum number that satisfies both conditions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data):
    arr = data.split()
    if not arr:
        return ""

    n = int(arr[0])
    digits = list(map(int, arr[1:]))

    cnt = [0] * 10
    total = 0

    for d in digits:
        cnt[d] += 1
        total += d

    if cnt[0] == 0:
        return "-1"

    def remove_digit_with_remainder(rem):
        for d in range(1, 10):
            if d % 3 == rem and cnt[d] > 0:
                cnt[d] -= 1
                return True
        return False

    def remove_two_with_remainder(rem):
        for d in range(1, 10):
            if d % 3 == rem and cnt[d] > 0:
                for e in range(d, 10):
                    if e % 3 == rem and cnt[e] > 0:
                        if d == e and cnt[d] < 2:
                            continue
                        cnt[d] -= 1
                        cnt[e] -= 1
                        return True
        return False

    remainder = total % 3

    if remainder == 1:
        if not remove_digit_with_remainder(1):
            if not remove_two_with_remainder(2):
                return "-1"
    elif remainder == 2:
        if not remove_digit_with_remainder(2):
            if not remove_two_with_remainder(1):
                return "-1"

    ans = []
    for d in range(9, -1, -1):
        ans.append(str(d) * cnt[d])

    result = "".join(ans)

    if result == "":
        return "-1"

    if result[0] == "0":
        return "0"

    return result

if __name__ == "__main__":
    print(solve(sys.stdin.read()))
```

The solution first stores digit frequencies instead of storing a potentially large integer. This avoids integer conversion entirely because the number may contain `100000` digits.

The removal helpers search for digits by their remainder modulo 3. The first helper removes one digit, while the second removes two digits. Digits are checked from small to large because removing smaller digits preserves a larger final number.

After fixing the digit sum, the construction phase iterates from `9` down to `0`. Repeating each digit according to its remaining count creates the largest possible ordering. The zero check after construction handles cases such as `0000`, where the correct representation is just `0`.

## Worked Examples

### Example 1

Input:

```
1
0
```

| Step | Digit counts | Sum remainder | Action | Result |
| --- | --- | --- | --- | --- |
| Start | `0:1` | 0 | Zero exists | Continue |
| Build | `0` | 0 | Sort descending | `0` |

The only available digit already satisfies all conditions. This confirms the single-zero edge case.

### Example 2

Input:

```
6
2 3 1 3 1 0
```

| Step | Digit counts | Sum | Remainder | Action |
| --- | --- | --- | --- | --- |
| Start | `0:1, 1:2, 2:1, 3:2` | 10 | 1 | Need to remove remainder-1 digit |
| Remove | `1:1` remains removed | 9 | 0 | Divisible by 3 |
| Build | `3 3 2 1 0` | 9 | 0 | Output `33210` |

The trace shows why removing the smallest possible digit is correct. Removing a `1` fixes the divisibility while keeping all larger digits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every input digit is counted once, and the final construction only processes the ten digit values. |
| Space | O(1) | The algorithm stores only ten digit counters and a few variables. |

The input size can reach `100000` digits, so linear processing is required. The solution easily fits because it never performs operations proportional to the size of the number squared or any conversion to an integer.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    import collections

    def solve(data):
        arr = data.split()
        if not arr:
            return ""
        n = int(arr[0])
        digits = list(map(int, arr[1:]))

        cnt = [0] * 10
        total = 0
        for d in digits:
            cnt[d] += 1
            total += d

        if cnt[0] == 0:
            return "-1"

        def remove_one(rem):
            for d in range(1, 10):
                if d % 3 == rem and cnt[d]:
                    cnt[d] -= 1
                    return True
            return False

        def remove_two(rem):
            for d in range(1, 10):
                if d % 3 == rem and cnt[d]:
                    for e in range(d, 10):
                        if e % 3 == rem and cnt[e] - (d == e) > 0:
                            cnt[d] -= 1
                            cnt[e] -= 1
                            return True
            return False

        r = total % 3
        if r == 1:
            if not remove_one(1) and not remove_two(2):
                return "-1"
        elif r == 2:
            if not remove_one(2) and not remove_two(1):
                return "-1"

        ans = "".join(str(d) * cnt[d] for d in range(9, -1, -1))
        return "0" if ans and ans[0] == "0" else ans

    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    res = solve(sys.stdin.read())
    sys.stdin = old
    return res

assert run("1\n0\n") == "0", "sample 1"
assert run("6\n2 3 1 3 1 0\n") == "33210", "sample 2"

assert run("1\n5\n") == "-1", "no zero"
assert run("3\n0 0 0\n") == "0", "all zeros"
assert run("5\n9 8 7 6 0\n") == "98760", "already divisible"
assert run("4\n1 1 1 0\n") == "110", "remove one digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `-1` | Missing required zero |
| `3 / 0 0 0` | `0` | All-zero normalization |
| `5 / 9 8 7 6 0` | `98760` | Keeping all digits when already valid |
| `4 / 1 1 1 0` | `110` | Correct removal for digit sum divisibility |

## Edge Cases

For the input:

```
1
0
```

the algorithm sees that a zero exists and the digit sum remainder is already zero. The construction phase creates `"0"`. The special handling prevents the output from becoming a longer sequence of zeroes.

For the input:

```
6
2 3 1 3 1 0
```

the total sum is `10`, which leaves remainder `1` when divided by `3`. The algorithm searches for a single digit with remainder `1` and removes `1`. The remaining digits have sum `9`, and sorting them gives `33210`.

For the input:

```
4
1 2 3 4
```

the counter for zero is empty, so the algorithm stops immediately with `-1`. No later arrangement step can fix this because every divisible-by-30 number must end in zero.
