---
title: "CF 102535E - Potent Plants"
description: "The input describes several collections of plants. A collection is written as a string of uppercase letters, where each letter represents one plant and its weight is determined by its position in the alphabet."
date: "2026-08-06T19:49:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "E"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 77
verified: true
draft: false
---

[CF 102535E - Potent Plants](https://codeforces.com/problemset/problem/102535/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes several collections of plants. A collection is written as a string of uppercase letters, where each letter represents one plant and its weight is determined by its position in the alphabet. The first value on each test case is the maximum total weight the growing area can support. The task is to decide whether the sum of all plant weights in the collection is within that limit.

The output is simply whether the collection fits. If the total weight is at most the allowed capacity, the answer is `YES`; otherwise it is `NO`.

The total length of all strings is at most 10 6, which means the solution must process every character only a constant number of times. A quadratic solution would be too slow because repeatedly recalculating weights or checking many combinations could approach 10 12 operations in the largest cases. A linear scan is enough because 10 6 character operations are easily manageable in the given time limit.

A few cases can break careless implementations. If the capacity is exactly equal to the total weight, the answer must still be `YES`. For example:

```
1
3 ABC
```

The weights are 1+2+3=6, so this example actually exceeds the capacity and the output is:

```
NO
```

A correct boundary example is:

```
1
6 ABC
```

The output is:

```
YES
```

An implementation using a strict comparison such as `total < w` would incorrectly reject it.

Another common mistake is treating letters as zero-indexed values. For example:

```
1
1 A
```

The plant `A` weighs 1, so the output is:

```
YES
```

If `A` is accidentally converted using `ord('A') = 65` or by subtracting the wrong offset, the result will be incorrect.

The capacity can also be zero, so a positive-weight plant must always fail:

```
1
0 A
```

The correct output is:

```
NO
```

## Approaches

A direct solution is to simulate the total weight calculation. For every character in the string, convert it into its alphabet position and add that value to a running sum. After processing the whole string, compare the sum with the given capacity. This approach is already optimal because every plant has to be examined at least once.

A slower brute-force mindset would repeatedly scan the collection while trying to build or validate possible totals. For example, checking subsets would require considering up to 2 n possibilities, which is impossible when the string length can reach 10 6. Even a less extreme approach that repeatedly recomputes the sum could perform around 10 12 additions on a large input.

The key observation is that there is no interaction between plants. The total weight is only the sum of independent contributions, so the entire problem reduces to accumulating values during a single pass. There is no need for sorting, dynamic programming, or searching.

The brute-force works because it eventually examines all possible ways to calculate the total, but it fails because the number of possibilities grows too quickly. The observation that each plant contributes a fixed independent value lets us replace the whole process with one linear accumulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2 n ) or worse depending on implementation | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the maximum allowed weight and the plant string. The string contains exactly the information needed to compute the total, because every character maps directly to one weight.
2. Traverse the string character by character. Convert each uppercase letter into its weight using `ord(character) - ord('A') + 1`, then add it to the running total. The `+1` is necessary because alphabet positions start at one for this problem, not zero.
3. After all characters have been processed, compare the accumulated weight with the allowed capacity. If the total does not exceed the limit, print `YES`; otherwise print `NO`.

Why it works:

The invariant during the scan is that after processing any prefix of the string, the running total equals the exact weight of all plants in that prefix. Each step adds the correct contribution of the next plant, so the invariant remains true until the whole string is processed. At the end of the scan, the stored total is exactly the weight of every plant combined. Comparing it with the capacity gives the correct decision.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        w, s = input().split()
        w = int(w)

        total = 0
        for c in s:
            total += ord(c) - ord('A') + 1

        if total <= w:
            ans.append("YES")
        else:
            ans.append("NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program reads all test cases using `sys.stdin.readline`, which is necessary because the total input size can reach one million characters.

The conversion expression `ord(c) - ord('A') + 1` transforms `A` into 1 and `Z` into 26. The accumulated value is stored in Python's integer type, which avoids overflow concerns even when many large letters appear.

The comparison uses `<=` because a collection whose weight exactly matches the available capacity is allowed. No extra memory proportional to the string size is needed because the string is processed with only a single running sum.

## Worked Examples

For the first sample case:

```
130 ACMALGOLYMPICS
```

The scan produces the following state.

| Character | Character weight | Running total |
| --- | --- | --- |
| A | 1 | 1 |
| C | 3 | 4 |
| M | 13 | 17 |
| A | 1 | 18 |
| L | 12 | 30 |
| G | 7 | 37 |
| O | 15 | 52 |
| L | 12 | 64 |
| Y | 25 | 89 |
| M | 13 | 102 |
| P | 16 | 118 |
| I | 9 | 127 |
| C | 3 | 130 |
| S | 19 | 149 |

The final weight is 149, which is larger than the limit 130, so the algorithm prints `NO`.

For the fourth sample case:

```
473 THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG
```

The important state is the final accumulation.

| State | Value |
| --- | --- |
| Capacity | 473 |
| Total after scanning the full string | 473 |
| Comparison | 473 <= 473 |
| Answer | YES |

This case confirms the equality boundary. The algorithm does not require unused capacity, only that the total fits within the limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character in the plant string is converted and added once. |
| Space | O(1) | Only the running total and a few variables are stored. |

The total number of characters over all test cases is at most 10 6, so the linear scan performs about one million conversions and additions. This easily fits within the time limit, and the constant memory usage stays well below the memory limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []
        for _ in range(t):
            w, s = input().split()
            total = sum(ord(c) - ord('A') + 1 for c in s)
            out.append("YES" if total <= int(w) else "NO")
        return "\n".join(out)

    result = solve()
    sys.stdin = old_stdin
    return result

assert run("""4
130 ACMALGOLYMPICS
2020 TWENTYTWENTY
472 THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG
473 THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG
""") == """NO
YES
NO
YES""", "provided samples"

assert run("""3
1 A
0 A
6 ABC
""") == """YES
NO
YES""", "minimum and boundary cases"

assert run("""2
26 Z
25 Z
""") == """YES
NO""", "single maximum letter and off-by-one boundary"

assert run("""1
1000000000 ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
""") == """YES""", "large capacity"

assert run("""1
52 ABZ
""") == """YES""", "mixed values with exact total"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 A` | `YES` | Smallest string and correct letter conversion |
| `1 / 0 A` | `NO` | Zero capacity handling |
| `26 / Z` and `25 / Z` | `YES`, `NO` | Exact boundary comparison |
| Many `Z` characters with large capacity | `YES` | Large totals and integer handling |
| `52 ABZ` | `YES` | Combining different letter weights |

## Edge Cases

The equality boundary is handled correctly because the algorithm accepts totals that are exactly the capacity. For:

```
1
6 ABC
```

the scan calculates 1+2+3=6. The comparison `6 <= 6` succeeds, producing:

```
YES
```

A strict less-than comparison would fail on this case.

The smallest possible plant collection is a single character. For:

```
1
1 A
```

the conversion gives `1`, and the total fits exactly, so the output is:

```
YES
```

This confirms that the alphabet conversion starts from one rather than zero.

Zero capacity is also valid input. For:

```
1
0 A
```

the total becomes `1`, which is larger than `0`, so the algorithm returns:

```
NO
```

Finally, very large collections do not need special handling. A string containing many `Z` characters simply adds 26 for each character. Since every character is processed independently, the same invariant applies regardless of string length, and the final comparison remains correct.
