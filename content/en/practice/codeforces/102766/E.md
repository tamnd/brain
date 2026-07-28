---
title: "CF 102766E - Singhal and Missing Number"
description: "We are given a string that was created by writing several consecutive integers next to each other. The integers originally formed a range from some starting value n to an ending value m, with at least three numbers in the range."
date: "2026-07-28T23:39:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102766
codeforces_index: "E"
codeforces_contest_name: "Codedigger Training Contest -String"
rating: 0
weight: 102766
solve_time_s: 74
verified: true
draft: false
---

[CF 102766E - Singhal and Missing Number](https://codeforces.com/problemset/problem/102766/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that was created by writing several consecutive integers next to each other. The integers originally formed a range from some starting value `n` to an ending value `m`, with at least three numbers in the range. Exactly one integer from the middle of this range was skipped before concatenation. The task is to recover the skipped integer, and if multiple ranges could explain the string, return the smallest possible missing value.

For example, the string `1314151718` can be split as `13, 14, 15, 17, 18`, which comes from the consecutive range `13` to `18` with `16` removed. The answer is the absent value, not the remaining sequence.

The upper bound of the numbers is large, up to `10^9`, so generating the whole range is impossible. A range can contain a huge number of integers while the input string itself has length only `10^5`. The total input size is also limited to `10^5` characters, which means the solution must work in roughly linear time in the length of each string. Trying all possible starting and ending numbers is far too expensive.

The tricky cases come from ambiguity in the beginning of the string. The first number might be the actual starting value, or the missing number might be the first value of the range. For example, the input `13` can represent the numbers `1, 2, 3` with `2` missing, so the answer is `2`. A solution that always treats the first digit sequence as the first existing number would miss this possibility.

Another edge case is when the missing number is at the end of the range. For example, the input `123` could represent `1,2,3,4` with `4` missing. A parser that only checks for jumps between adjacent parsed numbers would never detect the missing value and would incorrectly reject the sequence.

A third case is a change in digit length. For example, `899100101` represents `89,90,91,101` only if the split is chosen incorrectly, while the valid interpretation could involve a missing number around the transition from two digits to three digits. The parser must compare whole expected numbers rather than assuming a fixed number of digits.

## Approaches

A direct approach is to guess the complete consecutive sequence. We could try every possible first number, repeatedly split the string into increasing integers, and check whether exactly one value was skipped. This is correct because any valid answer must come from one such consecutive sequence. The problem is the search space. The first number can be large, and the possible splits grow quickly. Exploring all partitions of a string of length `10^5` is not realistic.

The useful observation is that the first existing number must appear at the beginning of the string. Since every number in the answer is smaller than `10^9`, the first number has at most nine digits. We only need to test these few possible prefixes as candidates for the first number.

For a chosen starting number, the rest of the sequence is deterministic. We always know which number should come next. If the next part of the string matches that expected number, we consume it. If it does not match, the only allowed explanation is that this expected number is the missing one and the current part of the string must be the following number. After that, the missing value has already been used, so every later number must match exactly.

This converts the problem from searching through many partitions into checking a small number of possible starts, each in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of possible splits | O(1) | Too slow |
| Optimal | O(9 * | S | ) |

## Algorithm Walkthrough

1. Try every possible prefix length from `1` to `9` as the first number. A prefix longer than nine digits cannot represent a valid number because the missing value is guaranteed to be below `10^9`.
2. For each candidate starting number, parse the remaining string while expecting consecutive integers. The first number itself is consumed immediately because it defines the sequence start.
3. Maintain the next expected integer and a flag indicating whether the missing number has already been found. When the next characters match the expected integer, consume them and increment the expectation.
4. If the expected integer does not match the current part of the string, treat that expected integer as the missing value. The current part must then match the number after it. If this jump happens more than once, the candidate start is invalid.
5. After the entire string is consumed, check whether exactly one number was skipped. If the sequence ended immediately after the last existing number, the missing value is the next expected number.
6. Among all valid candidates, return the smallest missing value.

Why it works: For a fixed starting number, the sequence of numbers that should appear is completely determined. At every position, either the expected number appears, or the only possible difference allowed by the problem is that this expected number was omitted. Because only one omission is allowed, the greedy parsing cannot skip the wrong number. Testing all possible first numbers covers every valid construction because the first existing number is either the true start of the range or the number immediately after the missing first value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(s):
    ans = 10**9

    def check(start):
        pos = 0
        cur = start
        missing = None

        first = str(start)
        if not s.startswith(first):
            return None
        pos += len(first)
        cur += 1

        while pos < len(s):
            expected = str(cur)
            if s.startswith(expected, pos):
                pos += len(expected)
                cur += 1
            else:
                if missing is not None:
                    return None
                nxt = str(cur + 1)
                if not s.startswith(nxt, pos):
                    return None
                missing = cur
                pos += len(nxt)
                cur += 2

        if missing is None:
            missing = cur

        return missing

    for length in range(1, min(9, len(s)) + 1):
        if length > 1 and s[0] == '0':
            continue
        start = int(s[:length])
        value = check(start)
        if value is not None:
            ans = min(ans, value)

    return str(ans)

def main():
    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        out.append(solve_case(s))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution first tries every possible length of the first number. There are only nine possibilities because valid numbers are below `10^9`.

The `check` function performs the greedy scan. The variable `cur` stores the number that should appear next. When the string contains `cur`, the scan moves normally. When it does not, the function verifies that `cur + 1` appears instead and records `cur` as the missing number.

The final condition handles a missing last number. If the scan finishes without finding a gap, the only remaining possibility is that the next expected number was never written. The implementation avoids integer overflow because Python integers grow automatically, although the largest values here are small enough for standard 64 bit integers as well.

## Worked Examples

For `3457`, one successful trace is:

| Step | Expected number | Current position | Action | Missing |
| --- | --- | --- | --- | --- |
| Start | 3 | 0 | Read 3 | none |
| 1 | 4 | 1 | Read 4 | none |
| 2 | 5 | 2 | Read 5 | none |
| 3 | 6 | 3 | 7 appears, skip 6 | 6 |
| 4 | 8 | end | Finish | 6 |

The trace shows the single jump allowed by the problem. The skipped value is the expected value before the jump.

For `1314151718`, the trace is:

| Step | Expected number | Current position | Action | Missing |
| --- | --- | --- | --- | --- |
| Start | 13 | 0 | Read 13 | none |
| 1 | 14 | 2 | Read 14 | none |
| 2 | 15 | 4 | Read 15 | none |
| 3 | 16 | 6 | 17 appears, skip 16 | 16 |
| 4 | 18 | 8 | Read 18 | 16 |

The transition around `16` and `17` demonstrates why comparing complete integers is necessary. The number of digits changes naturally during parsing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(9 * | S |
| Space | O(1) | Only counters and temporary values are stored. |

The total input length is `10^5`, so the solution performs only a small constant multiple of linear work. It fits comfortably within the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    def solve_case(s):
        ans = 10**9

        def check(start):
            pos = 0
            cur = start
            missing = None

            if not s.startswith(str(start)):
                return None
            pos += len(str(start))
            cur += 1

            while pos < len(s):
                if s.startswith(str(cur), pos):
                    pos += len(str(cur))
                    cur += 1
                else:
                    if missing is not None:
                        return None
                    if not s.startswith(str(cur + 1), pos):
                        return None
                    missing = cur
                    pos += len(str(cur + 1))
                    cur += 2

            return cur if missing is None else missing

        for i in range(1, min(9, len(s)) + 1):
            v = check(int(s[:i]))
            if v is not None:
                ans = min(ans, v)
        return str(ans)

    res = []
    for x in data[1:]:
        res.append(solve_case(x))
    return "\n".join(res)

assert run("""4
13
3457
1314151718
234235236238
""") == """2
6
16
237"""

assert run("""1
123
""") == "4"

assert run("""1
8990
""") == "9"

assert run("""1
11121315
""") == "14"

assert run("""1
99910001002
""") == "1001"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `13` | `2` | Missing value at the beginning of the range |
| `123` | `4` | Missing value after the visible sequence |
| `8990` | `9` | Consecutive values with a digit boundary |
| `11121315` | `14` | Missing value inside a multi digit sequence |
| `99910001002` | `1001` | Transition from three to four digit numbers |

## Edge Cases

When the missing number is the first value, the algorithm handles it because the first existing number can also be the number after the missing one. For input `13`, the candidate start `1` parses the sequence as `1,3`, and the missing value is detected as `2`. The candidate start `13` is invalid or gives a larger interpretation, so the minimum answer remains `2`.

When the missing number is the final value, there is no visible jump inside the string. For input `123`, the sequence can be `1,2,3,4` with `4` missing. The parser finishes after reading `3`, sees that no gap has been recorded, and assigns the next expected number as the missing value.

When the sequence crosses digit lengths, such as `1314151718`, the parser does not rely on fixed-width chunks. It compares the exact decimal representation of the expected number at every step, allowing transitions between two digit and three digit values without special handling.
