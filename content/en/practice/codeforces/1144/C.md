---
title: "CF 1144C - Two Shuffled Sequences"
description: "We are given a multiset of integers that was created by taking two sequences, one strictly increasing and one strictly decreasing, merging all their elements together, and then shuffling the result. The original order inside the merged array is lost."
date: "2026-06-12T03:31:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1144
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 550 (Div. 3)"
rating: 1000
weight: 1144
solve_time_s: 108
verified: false
draft: false
---

[CF 1144C - Two Shuffled Sequences](https://codeforces.com/problemset/problem/1144/C)

**Rating:** 1000  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of integers that was created by taking two sequences, one strictly increasing and one strictly decreasing, merging all their elements together, and then shuffling the result.

The original order inside the merged array is lost. We only know the values that appeared. Our task is to reconstruct any valid pair of sequences whose combined elements exactly match the given numbers.

The key requirement is that the increasing sequence cannot contain duplicate values, and the decreasing sequence cannot contain duplicate values either. Since the final multiset comes from the union of these two sequences, every occurrence of a value must be assigned to one of the two sequences.

The input size reaches $2 \cdot 10^5$. Any solution that tries many different assignments or searches through possibilities is immediately ruled out. We need something close to $O(n \log n)$, which is the natural target when sorting is involved.

A few edge cases deserve attention.

Consider:

```
3
5 5 5
```

The value 5 appears three times. One copy could go into the increasing sequence and one copy into the decreasing sequence, but there is nowhere to place the third copy. Since both sequences must remain strict, no value can appear more than once in the same sequence. The correct answer is:

```
NO
```

A careless solution that only checks whether duplicates exist would miss that frequencies greater than two are impossible.

Consider:

```
4
1 2 3 4
```

Every value appears once. The correct construction is to place all values into the increasing sequence and leave the decreasing sequence empty:

```
YES
4
1 2 3 4
0
```

Some implementations unnecessarily force every value into both sequences and fail on unique values.

Another subtle case is:

```
4
1 1 2 2
```

A valid answer exists:

```
Increasing: 1 2
Decreasing: 2 1
```

The decreasing sequence must be printed in strictly decreasing order. If we simply collect duplicate values in ascending order, we would output `1 2`, which is not decreasing.

## Approaches

A brute-force approach would try assigning every occurrence either to the increasing sequence or to the decreasing sequence, then check whether both sequences can be arranged to satisfy the strict ordering requirements.

If a value appears $k$ times, each copy has assignment choices. Even for moderate inputs this becomes exponential. With $n = 2 \cdot 10^5$, the number of possible assignments is completely infeasible.

The structure of the problem gives a much stronger observation.

Since both sequences are strict, a value may appear at most once in each sequence. That means any value may appear at most twice overall. The moment some frequency exceeds two, the answer is impossible.

Suppose a value appears exactly once. It can safely be placed into the increasing sequence.

Suppose a value appears exactly twice. One copy must go into the increasing sequence and the other copy must go into the decreasing sequence. There is no alternative.

This completely determines the assignment.

After sorting the distinct values, we place one copy of every distinct value into the increasing sequence. This automatically produces a strictly increasing sequence.

Every value that appeared twice contributes one additional copy to the decreasing sequence. If we store those duplicate values and finally reverse their sorted order, the result becomes strictly decreasing.

The entire problem reduces to counting frequencies and sorting distinct values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all numbers and count the frequency of each value.
2. If any value appears more than twice, print `"NO"` and stop.

A value can appear at most once in the increasing sequence and at most once in the decreasing sequence, so frequency three or more is impossible.
3. Sort all distinct values in ascending order.
4. Build the increasing sequence by taking every distinct value exactly once.

Since the values are sorted and distinct, the sequence is strictly increasing.
5. For every value whose frequency is exactly two, add one copy to a second list.

These are the extra copies that cannot remain in the increasing sequence.
6. Reverse this second list.

The duplicate values were collected in ascending order. Reversing them produces a strictly decreasing sequence.
7. Print `"YES"` and output both sequences.

### Why it works

Every value with frequency one must appear in exactly one sequence, and placing it into the increasing sequence never creates a conflict.

Every value with frequency two must contribute one copy to each sequence. Putting one copy into the increasing sequence and one copy into the decreasing sequence is the only possible valid assignment.

The increasing sequence contains each distinct value once, in ascending order, so it is strictly increasing.

The decreasing sequence contains exactly the duplicated values, each appearing once, in descending order, so it is strictly decreasing.

Since every occurrence is assigned exactly once and frequencies greater than two are rejected, the produced sequences form a valid partition of the original multiset whenever a solution exists.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

freq = Counter(a)

for cnt in freq.values():
    if cnt > 2:
        print("NO")
        sys.exit()

inc = []
dec = []

for x in sorted(freq):
    inc.append(x)
    if freq[x] == 2:
        dec.append(x)

dec.reverse()

print("YES")
print(len(inc))
if inc:
    print(*inc)
else:
    print()

print(len(dec))
if dec:
    print(*dec)
else:
    print()
```

The frequency table is the central data structure. It immediately detects impossible cases where a value appears more than twice.

The increasing sequence is built from the sorted distinct values. Using distinct values guarantees strictness automatically.

The decreasing sequence contains exactly those values that appeared twice. The order is important. Collecting duplicates during the ascending traversal gives an increasing list, so we reverse it before printing.

Empty sequences are handled explicitly. The problem allows them, so when a sequence has length zero we still print the required line.

## Worked Examples

### Example 1

Input:

```
7
7 2 7 3 3 1 4
```

Frequency table:

| Value | Frequency |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |
| 7 | 2 |

Processing:

| Current Value | Frequency | inc | dec before reverse |
| --- | --- | --- | --- |
| 1 | 1 | [1] | [] |
| 2 | 1 | [1,2] | [] |
| 3 | 2 | [1,2,3] | [3] |
| 4 | 1 | [1,2,3,4] | [3] |
| 7 | 2 | [1,2,3,4,7] | [3,7] |

After reversing:

| inc | dec |
| --- | --- |
| [1,2,3,4,7] | [7,3] |

Output:

```
YES
5
1 2 3 4 7
2
7 3
```

This demonstrates the main idea. Every distinct value appears once in the increasing sequence, while the second copy of duplicated values moves into the decreasing sequence.

### Example 2

Input:

```
4
1 1 2 2
```

Frequency table:

| Value | Frequency |
| --- | --- |
| 1 | 2 |
| 2 | 2 |

Processing:

| Current Value | Frequency | inc | dec before reverse |
| --- | --- | --- | --- |
| 1 | 2 | [1] | [1] |
| 2 | 2 | [1,2] | [1,2] |

After reversing:

| inc | dec |
| --- | --- |
| [1,2] | [2,1] |

Output:

```
YES
2
1 2
2
2 1
```

This example shows why the reverse operation is necessary. Without it, the decreasing sequence would not actually be decreasing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Frequency counting is $O(n)$, sorting distinct values dominates |
| Space | $O(n)$ | Frequency table and output sequences |

The largest input contains $2 \cdot 10^5$ numbers. Sorting that many values is easily within the limits, and the memory usage remains linear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    freq = Counter(a)

    for cnt in freq.values():
        if cnt > 2:
            return "NO"

    inc = []
    dec = []

    for x in sorted(freq):
        inc.append(x)
        if freq[x] == 2:
            dec.append(x)

    dec.reverse()

    out = []
    out.append("YES")
    out.append(str(len(inc)))
    out.append(" ".join(map(str, inc)))
    out.append(str(len(dec)))
    out.append(" ".join(map(str, dec)))

    return "\n".join(out)

# sample
assert run("7\n7 2 7 3 3 1 4\n").startswith("YES")

# minimum size
assert run("1\n5\n") == "YES\n1\n5\n0\n"

# all equal, impossible
assert run("3\n7 7 7\n") == "NO"

# duplicates exactly twice
assert run("4\n1 1 2 2\n") == "YES\n2\n1 2\n2\n2 1"

# all distinct
assert run("5\n1 2 3 4 5\n") == "YES\n5\n1 2 3 4 5\n0\n"

# boundary style case
assert run("2\n0 200000\n") == "YES\n2\n0 200000\n0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | Single-element solution | Minimum size |
| `7 7 7` | `NO` | Frequency greater than two |
| `1 1 2 2` | Valid split | Duplicate handling |
| `1 2 3 4 5` | Empty decreasing sequence | All values unique |
| `0 200000` | Valid split | Extreme value range |

## Edge Cases

Consider:

```
3
5 5 5
```

The frequency of 5 is 3. During the frequency scan, the algorithm immediately detects a count greater than two and prints:

```
NO
```

This is correct because two strict sequences can contain at most two copies of any value.

Consider:

```
4
1 2 3 4
```

All frequencies equal one.

The algorithm constructs:

```
inc = [1, 2, 3, 4]
dec = []
```

The decreasing sequence is empty, which the problem explicitly allows.

Consider:

```
4
1 1 2 2
```

The algorithm builds:

```
inc = [1, 2]
dec before reverse = [1, 2]
```

After reversing:

```
dec = [2, 1]
```

Both sequences are strict, and every occurrence from the original multiset is used exactly once.

Consider:

```
5
1 1 2 3 3
```

The algorithm produces:

```
inc = [1, 2, 3]
dec = [3, 1]
```

The increasing sequence remains strictly increasing, the decreasing sequence remains strictly decreasing, and all five original occurrences are accounted for. This confirms that duplicated values can coexist safely as long as no value appears more than twice.
