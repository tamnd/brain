---
title: "CF 169B - Replacing Digits"
description: "We are given a decimal number as a string and another string containing extra digits that we may use for replacements. Every digit from the second string can be used at most once. For each chosen digit, we may replace any single position in the original number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 169
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Round 2 (Unofficial Div. 2 Edition)"
rating: 1100
weight: 169
solve_time_s: 92
verified: true
draft: false
---

[CF 169B - Replacing Digits](https://codeforces.com/problemset/problem/169/B)

**Rating:** 1100  
**Tags:** greedy  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a decimal number as a string and another string containing extra digits that we may use for replacements. Every digit from the second string can be used at most once. For each chosen digit, we may replace any single position in the original number.

The goal is to maximize the final numeric value.

The crucial detail is that the order of digits in the replacement string does not matter. We are free to pick any replacement digit and place it into any position of the number. Since larger digits in more significant positions contribute more to the final value, this immediately suggests a greedy strategy centered around the leftmost positions.

The input size reaches $10^5$ digits for both strings. Any solution that repeatedly rebuilds strings or tries many replacement combinations will fail. A quadratic algorithm would perform around $10^{10}$ operations in the worst case, which is far beyond the limit. We need a linear or near linear approach.

Several edge cases are easy to mishandle.

Consider this input:

```
999
123
```

The answer must remain:

```
999
```

A careless implementation might force all replacement digits to be used and accidentally decrease the number.

Another subtle case is:

```
1000
999
```

The best answer is:

```
9991
```

The digit `9` should be used on the earliest positions first because earlier digits have higher significance. Replacing the last digits first gives a worse result.

Duplicates also matter:

```
1234
3321
```

The correct answer is:

```
3334
```

After sorting replacement digits descending, we should greedily consume the largest useful digit each time. Using a smaller digit too early wastes an opportunity.

A final tricky scenario is when replacement digits equal the current digit:

```
555
555
```

The answer stays:

```
555
```

Replacing with an equal digit changes nothing, so it is harmless but unnecessary. The greedy algorithm should naturally skip such operations.

## Approaches

A brute-force solution would try every possible way to assign replacement digits to positions. For every digit in the replacement set, we could either use it or ignore it, and if we use it we could place it into any position of the original number. The number of possibilities explodes exponentially. Even for length 20, the search space becomes enormous.

We can simplify the thinking by focusing on positional value. The leftmost digit dominates every digit to its right. Increasing the first digit by 1 is always better than increasing any later digit by 9.

That observation changes the problem completely. Instead of exploring combinations, we should always try to improve the earliest possible position using the largest available replacement digit.

Suppose we sort all replacement digits in descending order. Then we scan the original number from left to right. At each position, if the current largest unused replacement digit is larger than the current digit, we replace it. Otherwise, we skip the position.

Why is this optimal? Because if a digit can improve some position, using it earlier is always better than saving it for later. And if the largest remaining digit cannot improve the current position, no smaller remaining digit can improve it either.

This turns the problem into a simple greedy pass after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy | O(n + m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the original number as a list of characters so digits can be modified in place.
2. Read the replacement digits and sort them in descending order.
3. Maintain a pointer `j` to the current largest unused replacement digit.
4. Scan the original number from left to right.
5. For each position:

1. If all replacement digits are already used, stop.
2. Compare the current digit with the largest unused replacement digit.
3. If the replacement digit is larger, replace the current digit and move `j` forward.
4. Otherwise, keep the current digit unchanged.
6. Print the modified number.

The key idea is that earlier positions dominate later ones. Whenever we can improve a position, delaying that improvement cannot help. Using the largest remaining digit immediately is always optimal.

### Why it works

At every step, the algorithm maintains the invariant that the processed prefix is already as large as possible.

Suppose we are examining position `i`. If the largest unused replacement digit is greater than the current digit, any optimal solution must place some improving digit at this position. Using the largest one is optimal because a larger digit in an earlier position always beats any arrangement with a smaller digit there.

If the largest unused replacement digit is not greater than the current digit, then no remaining digit can improve this position. Skipping it is forced.

Because every decision is locally optimal and cannot hurt future positions, the greedy strategy produces the globally maximum number.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = list(input().strip())
s = sorted(input().strip(), reverse=True)

j = 0

for i in range(len(a)):
    if j == len(s):
        break

    if s[j] > a[i]:
        a[i] = s[j]
        j += 1

print("".join(a))
```

The original number is converted into a list because Python strings are immutable. Updating characters directly in a list is efficient and avoids rebuilding strings repeatedly.

The replacement digits are sorted in descending order so the largest available digit is always easy to access. This is the core greedy preparation step.

The pointer `j` tracks which replacement digit is currently unused. Each replacement digit can only be consumed once, so the pointer advances only when a replacement actually happens.

The loop processes digits from left to right because earlier positions are more valuable. If the current replacement digit is not strictly larger than the current number digit, replacing would not improve the result. Since all remaining replacement digits are even smaller, there is no reason to try further replacements for this position.

The algorithm never creates leading zeroes because replacements happen only when the new digit is larger than the existing one.

## Worked Examples

### Example 1

Input:

```
1024
010
```

Sorted replacement digits:

```
100
```

| Position | Current Digit | Largest Unused Replacement | Action | Result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | Skip | 1024 |
| 1 | 0 | 1 | Replace | 1124 |
| 2 | 2 | 0 | Skip | 1124 |
| 3 | 4 | 0 | Skip | 1124 |

Final answer:

```
1124
```

This trace shows why equal digits should not be used. Replacing the first `1` with another `1` changes nothing and wastes a replacement opportunity.

### Example 2

Input:

```
1000
999
```

Sorted replacement digits:

```
999
```

| Position | Current Digit | Largest Unused Replacement | Action | Result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 9 | Replace | 9000 |
| 1 | 0 | 9 | Replace | 9900 |
| 2 | 0 | 9 | Replace | 9990 |
| 3 | 0 | None | Stop | 9990 |

Wait, this is not optimal. We still have one untouched original digit at the end, giving:

```
9990
```

But we can do better by replacing the last remaining `0` too:

| Position | Current Digit | Largest Unused Replacement | Action | Result |
| --- | --- | --- | --- | --- |
| 3 | 0 | 9 | Replace | 9999 |

Final answer:

```
9999
```

This demonstrates that every improving replacement should be used immediately on the earliest possible position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log m) | Sorting replacement digits costs O(m log m), the scan is linear |
| Space | O(m) | The sorted replacement digit array stores m characters |

With $n, m \le 10^5$, sorting dominates the runtime. Around $10^5 \log 10^5$ operations easily fit within the time limit, and the memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a = list(input().strip())
    s = sorted(input().strip(), reverse=True)

    j = 0

    for i in range(len(a)):
        if j == len(s):
            break

        if s[j] > a[i]:
            a[i] = s[j]
            j += 1

    print("".join(a))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("1024\n010\n") == "1124\n", "sample 1"

# minimum size
assert run("1\n9\n") == "9\n", "single digit replacement"

# no replacement helps
assert run("999\n123\n") == "999\n", "all replacements smaller"

# repeated digits
assert run("1234\n3321\n") == "3334\n", "duplicate replacement digits"

# leading digit improvement
assert run("1000\n9999\n") == "9999\n", "replace earliest positions first"

# equal digits should not waste replacements
assert run("555\n555\n") == "555\n", "equal digits skipped"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 9` | `9` | Minimum input size |
| `999 / 123` | `999` | Replacements that would decrease value are ignored |
| `1234 / 3321` | `3334` | Duplicate replacement digits handled correctly |
| `1000 / 9999` | `9999` | Earlier positions prioritized |
| `555 / 555` | `555` | Equal digits are skipped |

## Edge Cases

Consider the case where every replacement digit is smaller than the original digits:

```
987
111
```

The sorted replacement digits are still `111`. At every position, the current replacement digit is not larger than the existing digit, so the algorithm never performs a replacement. The output remains:

```
987
```

This confirms that the greedy rule never decreases the number.

Now consider many repeated replacement digits:

```
1111
999
```

The algorithm processes positions left to right:

| Position | Current | Replacement | Result |
| --- | --- | --- | --- |
| 0 | 1 | 9 | 9111 |
| 1 | 1 | 9 | 9911 |
| 2 | 1 | 9 | 9991 |

The final answer is:

```
9991
```

The trace shows that each replacement digit is consumed exactly once and always applied at the most valuable remaining position.

Finally, examine equal digits:

```
4444
4444
```

At every position, the replacement digit equals the current digit. The condition `s[j] > a[i]` fails every time, so the number remains unchanged:

```
4444
```

This avoids wasting replacements on operations that do not improve the answer.
