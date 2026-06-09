---
title: "CF 1676A - Lucky?"
description: "We are given a sequence of short strings, each representing a six-digit ticket number. Each ticket should be split into two halves of equal length. The task is to decide whether the sum of digits in the left half matches the sum of digits in the right half."
date: "2026-06-10T00:57:36+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1676
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 790 (Div. 4)"
rating: 800
weight: 1676
solve_time_s: 95
verified: true
draft: false
---

[CF 1676A - Lucky?](https://codeforces.com/problemset/problem/1676/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of short strings, each representing a six-digit ticket number. Each ticket should be split into two halves of equal length. The task is to decide whether the sum of digits in the left half matches the sum of digits in the right half.

Each test case is independent, so the computation resets for every ticket string. The output is a simple binary judgment per ticket: whether it satisfies this balance condition or not.

Even though the input format is extremely small, the main thing to be careful about is that the digits are given as characters. Treating them as integers requires explicit conversion, otherwise comparisons or arithmetic will silently behave incorrectly.

The constraints are tight enough that any reasonable interpretation is sufficient. With at most 1000 tickets and only six characters per ticket, even a solution that does redundant work per test case would still run comfortably within limits. This pushes the problem firmly into the implementation category, where correctness comes from careful indexing and conversion rather than algorithmic optimization.

The most common edge case here is forgetting that the string can contain leading zeros. A ticket like `"045207"` must be treated exactly as six digits, not as a number that loses leading zeros. Another subtle mistake is accidentally summing ASCII values instead of numeric digit values, which happens if one forgets to subtract `'0'`.

## Approaches

A brute-force way to think about this problem is to explicitly separate the string into two parts and compute the sum of each side. For each ticket, we loop over the first three characters, convert them to integers, and sum them. Then we repeat the same process for the last three characters. Finally, we compare the two results.

This approach is already optimal in this setting. There is no structure to exploit beyond direct aggregation, because the input size per test is constant. Any alternative method would still need to read all six digits at least once, which means we cannot asymptotically improve on linear work per ticket.

The key observation is that the problem does not require any global reasoning or preprocessing. Each ticket is independent, and the computation is fixed-size. So the solution reduces to straightforward character processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (sum halves directly) | O(6t) | O(1) | Accepted |
| Optimal (same, direct implementation) | O(6t) | O(1) | Accepted |

## Algorithm Walkthrough

We process each ticket independently and compute two sums.

1. Read the ticket string. It always has length 6, so we can safely index it without bounds checks.
2. Initialize two accumulators, one for the left half and one for the right half.
3. Add digits at positions 0, 1, and 2 to the left sum after converting each character to an integer. This ensures we are working in numeric space rather than character encoding space.
4. Add digits at positions 3, 4, and 5 to the right sum in the same way.
5. Compare the two sums. If they match, output `"YES"`, otherwise output `"NO"`.

### Why it works

Each ticket is partitioned into two disjoint sets of digits. Since every digit contributes exactly once to either the left or right sum, and there is no overlap, the comparison of sums directly captures the condition described in the problem. There is no hidden dependency between positions, so correctness reduces to accurate per-position accumulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    s = input().strip()
    
    left = 0
    right = 0
    
    left += ord(s[0]) - ord('0')
    left += ord(s[1]) - ord('0')
    left += ord(s[2]) - ord('0')
    
    right += ord(s[3]) - ord('0')
    right += ord(s[4]) - ord('0')
    right += ord(s[5]) - ord('0')
    
    if left == right:
        out.append("YES")
    else:
        out.append("NO")

print("\n".join(out))
```

The solution reads each ticket as a raw string and explicitly strips the newline to avoid accidental character contamination. Each digit is converted using `ord(c) - ord('0')`, which is a reliable constant-time conversion avoiding slower `int()` calls inside tight loops, though in this problem either would be fine.

The sums are computed separately for clarity, ensuring no mixing of indices between halves. The final comparison is done in constant time per test case.

## Worked Examples

We trace two inputs from the sample.

### Example 1

Input ticket: `213132`

| Step | Left digits processed | Right digits processed | Left sum | Right sum | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | - | 2 | 0 | - |
| 2 | 2,1 | - | 3 | 0 | - |
| 3 | 2,1,3 | - | 6 | 0 | - |
| 4 | - | 1 | 6 | 1 | - |
| 5 | - | 1,3 | 6 | 4 | - |
| 6 | - | 1,3,2 | 6 | 6 | YES |

This shows that accumulation is independent per half and only compared at the end.

### Example 2

Input ticket: `973894`

| Step | Left digits processed | Right digits processed | Left sum | Right sum | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | - | 9 | 0 | - |
| 2 | 9,7 | - | 16 | 0 | - |
| 3 | 9,7,3 | - | 19 | 0 | - |
| 4 | - | 8 | 19 | 8 | - |
| 5 | - | 8,9 | 19 | 17 | - |
| 6 | - | 8,9,4 | 19 | 21 | NO |

This confirms that even a small imbalance in any digit propagates into the final comparison.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test processes exactly 6 digits, so total work scales linearly with number of tickets |
| Space | O(1) | Only a constant number of variables are used besides output storage |

The constraints allow up to 1000 tickets, so this linear scan over a constant-sized string is trivially fast. Even with Python overhead, the solution runs well within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        s = input().strip()
        left = sum(ord(s[i]) - 48 for i in range(3))
        right = sum(ord(s[i]) - 48 for i in range(3, 6))
        res.append("YES" if left == right else "NO")
    return "\n".join(res)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""5
213132
973894
045207
000000
055776
""") == """YES
NO
YES
YES
NO"""

# custom cases
assert run("""1
111111
""") == "YES", "all digits equal"

assert run("""1
100001
""") == "YES", "balanced with zeros"

assert run("""1
123456
""") == "NO", "strictly increasing imbalance"

assert run("""1
000999
""") == "NO", "boundary split imbalance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 111111 | YES | symmetric all digits |
| 100001 | YES | leading/trailing zeros |
| 123456 | NO | general imbalance |
| 000999 | NO | extreme skew between halves |

## Edge Cases

The main edge case is handling leading zeros correctly. For example, in `045207`, the left half contains `0,4,5`, which must be treated numerically as `0 + 4 + 5 = 9`. If a programmer accidentally converts the substring `"045"` using integer parsing in a way that drops structure and then processes digits incorrectly, they might misinterpret or mishandle positions, but direct per-character conversion avoids that issue entirely.

Another subtle case is tickets where all digits are zero, such as `000000`. The correct behavior is always `"YES"` because both sums are zero. The algorithm naturally handles this because each character converts to zero and both accumulators remain equal throughout execution.

Finally, cases with maximal imbalance like `999000` test whether the split boundary is handled correctly. The left sum becomes `27` and the right sum becomes `0`, and since the halves are disjoint and consistently indexed, the comparison correctly produces `"NO"` without any off-by-one risk.
