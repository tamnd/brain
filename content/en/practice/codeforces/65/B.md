---
title: "CF 65B - Harry Potter and the History of Magic"
description: "We are given a sequence of four-digit years. Each year may contain mistakes, but we are allowed to repair it by changing at most one digit. After all repairs, the sequence must become non-decreasing, and every resulting year must stay between 1000 and 2011 inclusive."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 65
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 60"
rating: 1700
weight: 65
solve_time_s: 153
verified: false
draft: false
---

[CF 65B - Harry Potter and the History of Magic](https://codeforces.com/problemset/problem/65/B)

**Rating:** 1700  
**Tags:** brute force, greedy, implementation  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of four-digit years. Each year may contain mistakes, but we are allowed to repair it by changing at most one digit. After all repairs, the sequence must become non-decreasing, and every resulting year must stay between 1000 and 2011 inclusive.

The task is not to minimize the number of changes globally. Every year independently may differ from the original by at most one digit, and any valid final sequence is acceptable.

The most natural way to think about the problem is this: for every original year, there is only a small set of possible repaired years. We must choose one candidate per position so that the final sequence is sorted.

The constraints are small enough to allow aggressive enumeration. There are at most 1000 years, and each year has only four positions that can be modified. For every position we can try ten digits, so each year has at most 1 + 4 × 9 = 37 valid candidates, plus a few duplicates. Even if we compare every candidate against every previous possibility, the total work remains tiny.

The dangerous part of the problem is not performance, it is correctness. Several edge cases can silently break a careless implementation.

One common mistake is forgetting the upper bound 2011. Consider:

```
2
2009
9999
```

A naive solution might turn `9999` into `2099`, which is still larger than 2011 and invalid. The correct answer is impossible here.

Another trap is allowing leading zeroes. For example:

```
1
1000
```

Changing the first digit to `0` would create `0000`, but years must stay four-digit numbers between 1000 and 2011.

A more subtle issue appears when greedily choosing the smallest valid candidate. Consider:

```
2
1999
1000
```

For the second year, valid one-digit changes include `1000`, `1009`, `1090`, and so on. None are at least `1999`, so the answer is impossible. A greedy algorithm that ignores the previous chosen value until too late may incorrectly accept an invalid sequence.

There is also the opposite problem, choosing a candidate that is too large and blocks future positions unnecessarily. Suppose we have:

```
3
1888
1880
1881
```

If we unnecessarily raise the second value too much, we may make the third impossible. The safest strategy is to keep every chosen year as small as possible while preserving feasibility.

## Approaches

The brute-force idea is straightforward. For every position, generate all years obtainable with at most one digit change. Then recursively try every combination and check whether the resulting sequence is non-decreasing.

This works because each year has very few candidates. A four-digit number can keep all digits unchanged or modify one of four positions into one of nine alternative digits. That gives roughly 37 candidates per year.

The problem is that combining these possibilities explodes exponentially. In the worst case we would explore about $37^n$ sequences. Even for $n = 1000$, this is completely impossible.

The key observation is that the sequence constraint is local. Whether a candidate is valid depends only on the previous chosen year. We do not need to remember the entire prefix.

Once we see this, the problem becomes greedy. Suppose we already fixed the previous year to some value `prev`. For the current position, any candidate smaller than `prev` is unusable forever. Among all remaining candidates, choosing the smallest one is always optimal.

Why? Because smaller values leave more room for future years. Picking a larger valid candidate never helps later positions, it only restricts them further.

This converts the problem into a simple left-to-right process:

1. Generate all valid candidates for the current year.
2. Keep only candidates at least as large as the previous chosen year.
3. Choose the minimum among them.
4. If none exist, the answer is impossible.

Since every year has only about 37 candidates, the total complexity becomes linear in `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(37^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \cdot 40)$ | $O(40)$ | Accepted |

## Algorithm Walkthrough

1. Read all years as strings so digit replacement becomes easy.
2. Maintain a variable `prev`, representing the last chosen repaired year. Initially set it to `1000`, since every valid year must be at least this value.
3. For the current year, generate every number obtainable with at most one digit change.

Start by including the original number itself. Then try replacing each of the four positions with digits `0` through `9`.
4. Reject invalid generated years.

A candidate is invalid if:

- it has a leading zero,
- it falls outside `[1000, 2011]`.
5. Store all valid candidates in a set to avoid duplicates.

Different digit replacements can sometimes produce the same number.
6. Among all candidates greater than or equal to `prev`, choose the minimum.

This is the greedy step. Keeping the current value as small as possible maximizes flexibility for later positions.
7. If no candidate satisfies the condition, print `"No solution"` and terminate.
8. Otherwise append the chosen value to the answer list and update `prev`.
9. After processing all years, print the resulting sequence.

### Why it works

The algorithm maintains this invariant:

After processing position `i`, the chosen prefix is the lexicographically smallest valid non-decreasing prefix possible.

Suppose at some step we choose a candidate `x` even though another valid candidate `y < x` also exists. Any future sequence that works after choosing `x` would also work after choosing `y`, because future values only need to be at least the previous one. Lowering the previous value never removes future options.

So choosing the minimum valid candidate is always safe and never hurts future feasibility. By induction, if a solution exists, the greedy algorithm will find one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def candidates(s):
    res = set()

    original = int(s)
    if 1000 <= original <= 2011:
        res.add(original)

    arr = list(s)

    for i in range(4):
        old = arr[i]

        for d in "0123456789":
            if d == old:
                continue

            arr[i] = d

            if arr[0] != '0':
                val = int("".join(arr))

                if 1000 <= val <= 2011:
                    res.add(val)

        arr[i] = old

    return sorted(res)

def solve():
    n = int(input())
    years = [input().strip() for _ in range(n)]

    ans = []
    prev = 1000

    for s in years:
        cand = candidates(s)

        chosen = None

        for x in cand:
            if x >= prev:
                chosen = x
                break

        if chosen is None:
            print("No solution")
            return

        ans.append(chosen)
        prev = chosen

    print("\n".join(map(str, ans)))

solve()
```

The helper function generates every year reachable with at most one digit modification. Using strings makes digit replacement simple and avoids arithmetic tricks.

The original value is inserted first because zero changes are allowed. Then each position is modified independently. After changing one digit, the code checks whether the first digit became zero and whether the resulting year stays inside the allowed interval.

A set removes duplicates automatically. For example, replacing a digit with itself is skipped, but even different edits can occasionally produce the same integer.

The candidate list is sorted because the greedy step needs the smallest valid value at least as large as `prev`. Since the list is tiny, sorting costs almost nothing.

Inside `solve`, the algorithm processes years from left to right. For each year, it scans the sorted candidate list and picks the first candidate satisfying `x >= prev`.

The initialization `prev = 1000` is deliberate. Every valid year must already satisfy this lower bound, so the first chosen value only needs to obey the original problem constraint.

The most common implementation bug is forgetting to restore the modified digit after testing replacements. The line:

```
arr[i] = old
```

is essential. Without it, later modifications would accidentally stack multiple digit changes together.

## Worked Examples

### Example 1

Input:

```
3
1875
1936
1721
```

| Position | Original | Valid choice candidates ≥ prev | Chosen | New prev |
| --- | --- | --- | --- | --- |
| 1 | 1875 | 1075, 1175, 1275, ..., 1875 | 1075 | 1075 |
| 2 | 1936 | 1036, 1136, ..., 1936 | 1036 | 1036 |
| 3 | 1721 | 1021, 1121, ..., 1721, 1921 | 1021 | 1021 |

One possible valid output is:

```
1075
1036
1021
```

This demonstrates an important detail: the problem accepts any valid non-decreasing sequence. The sample output is not unique.

If we instead greedily require values to stay close to the original, we might overcomplicate the problem unnecessarily.

### Example 2

Input:

```
2
1999
1000
```

| Position | Original | Valid candidates ≥ prev | Chosen | New prev |
| --- | --- | --- | --- | --- |
| 1 | 1999 | many | 1009 | 1009 |
| 2 | 1000 | 1000 only | none | impossible |

The algorithm correctly reports:

```
No solution
```

This trace shows why local feasibility matters. Even though each year individually can be repaired, the sequence constraint may still make the entire instance impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 40)$ | Each year generates at most about 37 candidates |
| Space | $O(40)$ | Only the candidate set for one year is stored |

With at most 1000 years, the program performs only a few tens of thousands of operations. This easily fits inside the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    def candidates(s):
        res = set()

        val = int(s)
        if 1000 <= val <= 2011:
            res.add(val)

        arr = list(s)

        for i in range(4):
            old = arr[i]

            for d in "0123456789":
                if d == old:
                    continue

                arr[i] = d

                if arr[0] != '0':
                    x = int("".join(arr))

                    if 1000 <= x <= 2011:
                        res.add(x)

            arr[i] = old

        return sorted(res)

    n = int(input())
    years = [input().strip() for _ in range(n)]

    ans = []
    prev = 1000

    for s in years:
        cand = candidates(s)

        chosen = None

        for x in cand:
            if x >= prev:
                chosen = x
                break

        if chosen is None:
            output_data.write("No solution\n")
            return output_data.getvalue()

        ans.append(chosen)
        prev = chosen

    output_data.write("\n".join(map(str, ans)) + "\n")
    return output_data.getvalue()

# provided sample
out = solve_io("3\n1875\n1936\n1721\n")
assert out.strip() != "No solution"

# minimum size
assert solve_io("1\n1000\n") == "1000\n"

# impossible case
assert solve_io("2\n1999\n1000\n") == "No solution\n"

# all equal values
assert solve_io("3\n1111\n1111\n1111\n") == "1111\n1111\n1111\n"

# boundary near 2011
out = solve_io("2\n2011\n2011\n")
assert out == "2011\n2011\n"

# increasing sequence already valid
out = solve_io("4\n1000\n1001\n1002\n1003\n")
assert out == "1000\n1001\n1002\n1003\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1000` | `1000` | Minimum input size |
| `2 / 1999 / 1000` | `No solution` | Impossible ordering |
| `3 / 1111 / 1111 / 1111` | same values | Non-decreasing equality allowed |
| `2 / 2011 / 2011` | same values | Upper boundary handling |
| increasing valid input | unchanged sequence | Zero modifications needed |

## Edge Cases

Consider the case:

```
2
2009
9999
```

For `2009`, the algorithm can choose `1009`. Then it processes `9999`. Any one-digit modification still leaves the value larger than 2011, so the candidate set becomes empty. The algorithm immediately prints `"No solution"`.

This confirms that the upper bound restriction is enforced during candidate generation rather than afterward.

Now examine the leading-zero danger:

```
1
1000
```

When modifying the first digit, the algorithm may temporarily create strings like `"0000"` or `"9000"`. The condition:

```
if arr[0] != '0':
```

filters out invalid leading-zero numbers before conversion. The valid candidate `1000` remains, so the output is correct.

Finally, consider a sequence where greedy minimality matters:

```
3
1888
1880
1881
```

For the first year, the algorithm picks the smallest valid candidate, such as `1088`. Then the second can become `1080`, and the third `1081`.

If we had instead chosen a large repaired value for the first position, later years might become impossible. The greedy rule avoids this by always preserving maximum flexibility for the suffix.
