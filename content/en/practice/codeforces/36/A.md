---
title: "CF 36A - Extra-terrestrial Intelligence"
description: "We are given a binary string representing Vasya's observations over several days. A character '1' means a signal was rec"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 36
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 36"
rating: 1300
weight: 36
solve_time_s: 81
verified: true
draft: false
---

[CF 36A - Extra-terrestrial Intelligence](https://codeforces.com/problemset/problem/36/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing Vasya's observations over several days. A character `'1'` means a signal was received on that day, while `'0'` means no signal appeared.

The task is to determine whether the received signals follow a perfectly regular pattern. More precisely, if we look at the positions of all `'1'` characters, the gaps between consecutive positions must all be identical. If every interval is the same, we print `"YES"`. Otherwise, we print `"NO"`.

For example, in the string `001001001`, the signals appear at positions `2`, `5`, and `8`. The gaps are `3` and `3`, so the pattern is regular.

The constraints are very small. The string length is at most `100`, which means even inefficient solutions would easily run within the limits. A quadratic solution with around `10^4` operations is trivial for a 2-second time limit. Still, this problem is mainly about clean implementation and correctly handling positions of signals.

The tricky part is not performance, but correctly interpreting the spacing between signals.

Consider the input:

```
5
10101
```

The signal positions are `0`, `2`, and `4`. The gaps are `2` and `2`, so the answer is `"YES"`.

A careless implementation might instead count zeros between signals and accidentally compare `1` and `1`, which happens to work here, but can become confusing when mixed with indexing logic.

Another subtle case is when consecutive signals appear without zeros between them:

```
6
111000
```

The positions are `0`, `1`, and `2`. The gaps are `1` and `1`, so the answer is `"YES"`.

An incorrect approach that assumes every signal must have at least one zero between them would fail here.

A more dangerous edge case is when only some intervals match:

```
7
1001001
```

The signal positions are `0`, `3`, and `6`. The gaps are `3` and `3`, so the answer is `"YES"`.

But:

```
7
1001010
```

The positions are `0`, `3`, and `5`. The gaps are `3` and `2`, so the correct answer is `"NO"`.

If we only compare the first and last signals, we might incorrectly conclude the pattern is regular.

## Approaches

The most direct brute-force idea is to collect every position containing `'1'`, then explicitly compute all consecutive differences and compare them.

Suppose the signal positions are stored in an array:

```
pos = [2, 5, 8, 11]
```

We compute:

```
5 - 2 = 3
8 - 5 = 3
11 - 8 = 3
```

If every difference equals the first one, the pattern is regular.

This approach is already fast enough. With at most `100` characters, even repeatedly scanning the string would work comfortably within limits.

A more naive brute-force variant could try every possible interval length and verify whether all signals follow it. That would still pass because the constraints are tiny, but it performs unnecessary work and complicates the implementation.

The key observation is that the problem only depends on the distances between consecutive `'1'` positions. Once we know the first interval, every later interval must match it exactly. Nothing else matters.

That observation reduces the task to a simple linear scan over the signal positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the binary string.
2. Traverse the string and store the indices where the character is `'1'`.

These indices represent the days when signals were received.
3. Compute the distance between the first two signal positions.

This becomes the expected interval that every later pair must follow.
4. Iterate through the remaining consecutive pairs of signal positions.

For each pair, compute the difference between their indices.
5. Compare the current difference with the expected interval.

If any interval differs, print `"NO"` immediately because the pattern is not regular.
6. If all intervals match, print `"YES"`.

### Why it works

The only condition required by the problem is equality of all intervals between successive signals. The algorithm directly checks exactly that property.

Let the signal positions be:

```
p₀, p₁, p₂, ..., pₖ
```

The sequence is valid if and only if:

```
p₁ - p₀ = p₂ - p₁ = ... = pₖ - pₖ₋₁
```

The algorithm computes the first difference and verifies every later difference against it. Since every required interval is checked exactly once, the algorithm cannot incorrectly accept or reject a sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

positions = []

for i in range(n):
    if s[i] == '1':
        positions.append(i)

gap = positions[1] - positions[0]

for i in range(2, len(positions)):
    if positions[i] - positions[i - 1] != gap:
        print("NO")
        break
else:
    print("YES")
```

The first part of the code reads the input and gathers every index containing `'1'`. Using indices directly keeps the logic simple and avoids confusion about counting zeros between signals.

The variable `gap` stores the expected interval between signals. Since the statement guarantees at least three `'1'` characters, accessing `positions[1]` is always safe.

The loop starts from index `2` because the first interval is already used as the reference. For every later signal, we compare its distance from the previous signal against `gap`.

The `for-else` structure is convenient here. If the loop finishes without hitting `break`, every interval matched and we print `"YES"`.

A common off-by-one mistake is mixing zero counts with index differences. For example, positions `0` and `3` are separated by a distance of `3`, even though there are only two zeros between them. Using indices directly avoids that ambiguity.

## Worked Examples

### Example 1

Input:

```
8
00111000
```

The signal positions are `2`, `3`, and `4`.

| Step | Current Position | Previous Position | Difference | Expected Gap |
| --- | --- | --- | --- | --- |
| Initial | 3 | 2 | 1 | 1 |
| Check | 4 | 3 | 1 | 1 |

All differences equal `1`, so the output is:

```
YES
```

This example shows that consecutive signals are allowed. The interval can be `1`.

### Example 2

Input:

```
7
1001010
```

The signal positions are `0`, `3`, and `5`.

| Step | Current Position | Previous Position | Difference | Expected Gap |
| --- | --- | --- | --- | --- |
| Initial | 3 | 0 | 3 | 3 |
| Check | 5 | 3 | 2 | 3 |

The second interval differs from the first, so the output is:

```
NO
```

This trace demonstrates why checking only the first and last signals is insufficient. Every consecutive interval matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The string is scanned once, and signal positions are checked once |
| Space | O(n) | In the worst case, every character is `'1'` |

With `n ≤ 100`, the solution easily fits within both the time and memory limits. Even much slower approaches would pass, but the linear solution is clean and directly matches the problem structure.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    positions = []

    for i in range(n):
        if s[i] == '1':
            positions.append(i)

    gap = positions[1] - positions[0]

    for i in range(2, len(positions)):
        if positions[i] - positions[i - 1] != gap:
            print("NO")
            return

    print("YES")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("8\n00111000\n") == "YES", "sample 1"

# custom cases
assert run("5\n10101\n") == "YES", "equal spacing"
assert run("7\n1001010\n") == "NO", "unequal spacing"
assert run("6\n111000\n") == "YES", "consecutive signals"
assert run("3\n111\n") == "YES", "minimum size"
assert run("10\n1001001001\n") == "YES", "large equal intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10101` | `YES` | Regular spacing with zeros between signals |
| `1001010` | `NO` | Unequal intervals |
| `111000` | `YES` | Consecutive signals with interval 1 |
| `111` | `YES` | Minimum valid input size |
| `1001001001` | `YES` | Repeated larger interval |

## Edge Cases

Consider the case with consecutive signals:

```
6
111000
```

The positions array becomes:

```
[0, 1, 2]
```

The expected gap is:

```
1 - 0 = 1
```

The remaining check is:

```
2 - 1 = 1
```

All intervals match, so the algorithm prints `"YES"`.

This case confirms that intervals of length `1` are completely valid.

Now consider an irregular pattern:

```
7
1001010
```

The positions are:

```
[0, 3, 5]
```

The expected gap is `3`.

The next interval is:

```
5 - 3 = 2
```

Since `2 != 3`, the algorithm immediately prints `"NO"`.

This demonstrates that every consecutive interval is checked independently.

Finally, consider a perfectly regular sparse pattern:

```
9
100100100
```

The positions are:

```
[0, 3, 6]
```

The expected gap is:

```
3
```

The second interval is also `3`, so the algorithm prints `"YES"`.

This confirms that the actual number of zeros does not matter. Only equality of consecutive distances matters.
