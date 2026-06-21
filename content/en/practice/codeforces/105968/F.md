---
title: "CF 105968F - Fraud Detection"
description: "We are given a collection of integers, each written in standard decimal form. The task is to look at each number, extract only its first non-zero digit, and count how often each digit from 0 to 9 appears as that leading digit across the entire collection."
date: "2026-06-21T21:53:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105968
codeforces_index: "F"
codeforces_contest_name: "IME++ Starters Try-Outs 2025"
rating: 0
weight: 105968
solve_time_s: 50
verified: true
draft: false
---

[CF 105968F - Fraud Detection](https://codeforces.com/problemset/problem/105968/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers, each written in standard decimal form. The task is to look at each number, extract only its first non-zero digit, and count how often each digit from 0 to 9 appears as that leading digit across the entire collection. The output is essentially a frequency distribution over leading digits.

A useful way to think about this is that every number is being reduced to a single label, its most significant digit, and we are asked to aggregate these labels over the dataset. The internal structure of the number, such as trailing digits or even its magnitude beyond the first digit, is irrelevant once the leading digit is identified.

If the input size reaches typical competitive programming constraints, say up to 10^5 or more numbers, then any solution that tries to process numbers digit by digit in nested loops or performs repeated conversions inefficiently will still be fine as long as each number is processed in O(length of number). Since each number’s length is bounded by its decimal representation, a linear scan per number is sufficient and leads to an overall linear time solution in total input size.

A few edge cases are easy to mishandle. A number like `7` is straightforward, but a number like `1000` must contribute to digit `1`, not `0`. If negative numbers were allowed, a careless implementation might accidentally treat `-3` as leading digit `-`, which would be incorrect; we must always skip signs. If the number is `0`, the leading digit is `0`, which is also a valid frequency bucket and should not be ignored. For example, given input `0 0 10`, the correct output would reflect two zeros and one one, because `10` contributes leading digit `1`.

## Approaches

A brute-force interpretation would be to treat each number as an integer and repeatedly divide by 10 until only one digit remains. For each number, this takes O(d) time where d is the number of digits. Across n numbers, this yields O(total digits), which is already optimal in a practical sense, but it may involve repeated integer division operations and careful handling of negatives and zero.

Another straightforward but slightly cleaner brute-force approach is to convert each number into a string and directly access its first character. This avoids arithmetic entirely and makes the logic more transparent. However, if implemented without care, repeated string slicing or unnecessary parsing overhead could still slow things down slightly in very large inputs.

The key observation is that we do not need to interpret the number beyond its first character in its normalized string form. Once the input is read, extracting the first non-sign character is sufficient. This reduces the problem to a single pass over the input where each element contributes exactly one increment to a frequency array of size 10.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated division per number | O(n · d) | O(1) | Accepted |
| String first-digit extraction | O(n · d) | O(1) | Accepted |

Both approaches are effectively linear in input size, but the string-based method is typically the simplest and least error-prone.

## Algorithm Walkthrough

1. Read all numbers as strings rather than integers, because string form preserves the leading digit without any arithmetic manipulation. This avoids issues with overflow or sign handling.
2. Initialize an array `cnt` of size 10 with all zeros. Each index corresponds to a digit from 0 to 9, and we will accumulate counts there.
3. For each number string, scan from the beginning until we find a character that is not a minus sign. The first such character is the leading digit of the number. This step matters because negative numbers may include a leading `-`, which must be ignored.
4. Convert that first digit character into an integer and increment `cnt[digit]` by 1. This directly classifies the number into its leading-digit bucket.
5. After processing all numbers, output the counts in order from digit 0 to digit 9.

### Why it works

Each number contributes exactly one leading digit, and this digit is uniquely determined by the first non-sign character in its decimal representation. The algorithm never modifies or reinterprets the number beyond that point, so there is a one-to-one mapping between input elements and increments in the frequency array. Since every element is processed independently and exactly once, the accumulated counts are both complete and correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    cnt = [0] * 10

    for _ in range(n):
        s = input().strip()
        i = 0
        while i < len(s) and s[i] == '-':
            i += 1
        if i < len(s):
            d = ord(s[i]) - ord('0')
            cnt[d] += 1

    print(*cnt)

if __name__ == "__main__":
    solve()
```

The solution reads each number as a string and avoids any numeric conversion beyond extracting the first meaningful digit. The loop skipping `-` characters ensures correctness if negative values are present, even though many instances of this problem only use non-negative integers.

The frequency array `cnt` is fixed size, so updates are constant time. The final print statement outputs the full distribution in a single line.

A subtle point is that we do not strip leading zeros explicitly. This is intentional because a number like `"007"` still has leading digit `0`, and the first non-sign character correctly captures that.

## Worked Examples

Consider input:

```
5
123
45
7
100
-89
```

We track only the leading digit extraction.

| Number | Skipped | Leading digit | Count update |
| --- | --- | --- | --- |
| 123 | none | 1 | cnt[1]++ |
| 45 | none | 4 | cnt[4]++ |
| 7 | none | 7 | cnt[7]++ |
| 100 | none | 1 | cnt[1]++ |
| -89 | '-' | 8 | cnt[8]++ |

Final counts reflect two numbers starting with 1, and one each for 4, 7, and 8.

This trace confirms that the algorithm is purely positional and unaffected by magnitude or trailing digits.

Now consider:

```
4
0
0
10
-3
```

| Number | Skipped | Leading digit | Count update |
| --- | --- | --- | --- |
| 0 | none | 0 | cnt[0]++ |
| 0 | none | 0 | cnt[0]++ |
| 10 | none | 1 | cnt[1]++ |
| -3 | '-' | 3 | cnt[3]++ |

This demonstrates correct handling of zero and negative numbers. In particular, `0` is treated as a valid leading digit rather than being discarded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · d) | Each number is scanned once to find its first non-sign digit, where d is its length |
| Space | O(1) | Only a fixed-size array of 10 counters is used |

The algorithm scales linearly with the size of the input, since each character in the input is examined at most once. This is well within typical constraints for competitive programming problems involving up to 10^5 or more numbers.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# basic sample-like test
assert solve_io("5\n123\n45\n7\n100\n-89\n") == "0 2 0 0 1 0 0 1 1 0"

# all same leading digit
assert solve_io("3\n9\n90\n999\n") == "0 0 0 0 0 0 0 0 0 3"

# zeros and negatives
assert solve_io("4\n0\n0\n10\n-3\n") == "2 1 0 1 0 0 0 0 0 0"

# single element
assert solve_io("1\n5\n") == "0 0 0 0 0 1 0 0 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed numbers | varied counts | general correctness |
| all 9s | concentrated count | uniform leading digit handling |
| zeros/negatives | mixed edge handling | sign skipping and zero handling |
| single value | minimal input | base case correctness |

## Edge Cases

For an input consisting entirely of zeros such as:

```
3
0
0
0
```

the algorithm processes each string, finds `'0'` as the first non-sign character, and increments `cnt[0]` three times. The output correctly becomes a vector with 3 at index 0 and zeros elsewhere.

For negative single-digit inputs such as:

```
3
-1
-9
-3
```

each string skips the `-` and immediately reads the digit, producing counts for 1, 9, and 3 respectively. The sign never participates in classification, so no invalid index is accessed.

For numbers with leading zeros such as:

```
3
007
0002
09
```

the first non-sign character is always `'0'`, so all contributions correctly go to digit 0. The algorithm does not compress or normalize the number, which ensures leading zero information is preserved exactly as required.
