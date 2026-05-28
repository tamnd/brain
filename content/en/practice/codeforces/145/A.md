---
title: "CF 145A - Lucky Conversion"
description: "We are given two strings of equal length, both consisting only of the characters 4 and 7. The goal is to transform the first string into the second using the fewest operations. There are two allowed operations. We may flip a single digit, changing 4 to 7 or 7 to 4."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 145
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 104 (Div. 1)"
rating: 1200
weight: 145
solve_time_s: 122
verified: true
draft: false
---

[CF 145A - Lucky Conversion](https://codeforces.com/problemset/problem/145/A)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings of equal length, both consisting only of the characters `4` and `7`. The goal is to transform the first string into the second using the fewest operations.

There are two allowed operations. We may flip a single digit, changing `4` to `7` or `7` to `4`. We may also swap any two positions inside the first string.

The challenge is to decide when a swap is more valuable than individual flips. A swap can repair two incorrect positions at once, so using swaps intelligently is the key to minimizing the answer.

The string length can be as large as $10^5$. Any algorithm that tries many possible swaps explicitly becomes infeasible. For example, checking all pairs of indices would already require $O(n^2)$ operations, which is around $10^{10}$ comparisons in the worst case. That is far beyond the time limit. We need a linear solution.

A subtle edge case appears when mismatched positions are not complementary.

Consider:

```
a = 444
b = 777
```

Every position differs in the same way: `4 -> 7`. No swap can help because swapping identical digits changes nothing. The correct answer is `3`, one flip per position.

Another tricky case is when mismatches come in opposite directions.

```
a = 47
b = 74
```

At index `0`, we need `4 -> 7`.

At index `1`, we need `7 -> 4`.

One swap fixes both positions immediately, so the answer is `1`. A careless solution that counts mismatches independently would incorrectly return `2`.

A mixed example shows why we must pair complementary mismatches greedily.

```
a = 4477
b = 7744
```

There are two `4 -> 7` mismatches and two `7 -> 4` mismatches. We can repair each pair using one swap, so the answer is `2`, not `4`.

## Approaches

The brute-force idea is straightforward. We examine all mismatched positions and repeatedly try every possible swap to see whether it reduces the number of incorrect characters. If no useful swap exists, we flip one digit.

This approach is correct because it explicitly explores improving operations. The problem is the cost. There can be $O(n)$ mismatches, and trying all swaps among them costs $O(n^2)$. With $n = 10^5$, this is far too slow.

The key observation is that only two mismatch types exist.

A position may require:

```
4 -> 7
```

or

```
7 -> 4
```

Suppose we have one mismatch of each type:

```
a[i] = 4, b[i] = 7
a[j] = 7, b[j] = 4
```

Swapping `a[i]` and `a[j]` fixes both positions in a single operation. No better move exists because one operation cannot repair more than two incorrect positions.

This turns the problem into counting how many complementary mismatches can be paired together.

Let:

```
x = number of positions with 4 -> 7
y = number of positions with 7 -> 4
```

We can perform:

```
min(x, y)
```

swaps.

After using all possible swaps, only one mismatch type remains. Those remaining positions must be fixed individually using flips.

The final answer becomes:

```
swaps + remaining_flips
= min(x, y) + |x - y|
= max(x, y)
```

Even though the simplified formula exists, computing swaps and remaining flips separately makes the reasoning clearer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the two strings `a` and `b`.
2. Initialize two counters:

`cnt47` for positions where `a[i] = 4` and `b[i] = 7`,

`cnt74` for positions where `a[i] = 7` and `b[i] = 4`.
3. Scan the strings from left to right.
4. For each position:

If the characters already match, ignore it because no operation is needed.
5. If the mismatch is `4 -> 7`, increment `cnt47`.
6. If the mismatch is `7 -> 4`, increment `cnt74`.
7. Compute how many swaps are possible:

```
swaps = min(cnt47, cnt74)
```

Each such swap fixes one mismatch from each category.
8. After performing all beneficial swaps, one mismatch type may still remain.

The remaining positions require individual flips:

```
flips = abs(cnt47 - cnt74)
```
9. Print:

```
swaps + flips
```

### Why it works

A swap only helps when two mismatches are complementary. Swapping two identical mismatch types changes nothing useful.

Every complementary pair can always be repaired in one operation, and no operation can repair more than two incorrect positions. This makes greedy pairing optimal.

After all possible pairs are consumed, the remaining mismatches are all identical in direction. Swaps no longer help, so each remaining position must be flipped individually.

Because the algorithm maximizes useful swaps and performs only unavoidable flips afterward, the resulting number of operations is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = input().strip()
b = input().strip()

cnt47 = 0
cnt74 = 0

for x, y in zip(a, b):
    if x == y:
        continue

    if x == '4' and y == '7':
        cnt47 += 1
    else:
        cnt74 += 1

swaps = min(cnt47, cnt74)
flips = abs(cnt47 - cnt74)

print(swaps + flips)
```

The first part reads the two strings and initializes counters for the two mismatch categories.

The loop compares corresponding positions. Matching positions are skipped immediately because they already satisfy the target configuration.

Every mismatch must belong to exactly one of the two possible types. Since the strings contain only `4` and `7`, the `else` branch safely represents `7 -> 4`.

After counting mismatches, the code computes the maximum number of productive swaps. Each swap consumes one mismatch from both categories.

The remaining imbalance cannot be repaired by swapping anymore because all leftover mismatches point in the same direction. Each one requires a flip.

A common mistake is trying to count total mismatches and divide by two. That fails when all mismatches have the same direction. For example:

```
a = 444
b = 777
```

There are three mismatches, but zero useful swaps.

Another subtle point is using `.strip()` when reading input. Without it, the trailing newline becomes part of the string and causes incorrect comparisons.

## Worked Examples

### Example 1

Input:

```
47
74
```

Trace:

| Index | a[i] | b[i] | cnt47 | cnt74 |
| --- | --- | --- | --- | --- |
| 0 | 4 | 7 | 1 | 0 |
| 1 | 7 | 4 | 1 | 1 |

After processing:

| Variable | Value |
| --- | --- |
| swaps | 1 |
| flips | 0 |
| answer | 1 |

This example demonstrates the central greedy idea. One complementary pair exists, so a single swap repairs both positions.

### Example 2

Input:

```
444
777
```

Trace:

| Index | a[i] | b[i] | cnt47 | cnt74 |
| --- | --- | --- | --- | --- |
| 0 | 4 | 7 | 1 | 0 |
| 1 | 4 | 7 | 2 | 0 |
| 2 | 4 | 7 | 3 | 0 |

After processing:

| Variable | Value |
| --- | --- |
| swaps | 0 |
| flips | 3 |
| answer | 3 |

This case shows why counting mismatches alone is insufficient. Every mismatch has the same direction, so swapping never helps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One linear scan through both strings |
| Space | $O(1)$ | Only a few integer counters are stored |

With $n \le 10^5$, a linear algorithm easily fits within the time limit. The memory usage is constant because no auxiliary arrays or data structures are needed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a = input().strip()
    b = input().strip()

    cnt47 = 0
    cnt74 = 0

    for x, y in zip(a, b):
        if x == y:
            continue

        if x == '4' and y == '7':
            cnt47 += 1
        else:
            cnt74 += 1

    swaps = min(cnt47, cnt74)
    flips = abs(cnt47 - cnt74)

    print(swaps + flips)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("47\n74\n") == "1", "sample 1"

# minimum size, already equal
assert run("4\n4\n") == "0", "single equal character"

# all mismatches in one direction
assert run("444\n777\n") == "3", "all flips needed"

# perfectly pairable mismatches
assert run("4477\n7744\n") == "2", "all mismatches repaired by swaps"

# mixed case with leftover flips
assert run("4447\n7774\n") == "2", "one swap and one flip"

# large equal strings
n = 100000
a = "4" * n
b = "4" * n
assert run(f"{a}\n{b}\n") == "0", "maximum size equal strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 4` | `0` | Minimum-size input |
| `444 / 777` | `3` | No swaps possible |
| `4477 / 7744` | `2` | Every mismatch can be paired |
| `4447 / 7774` | `2` | Combination of swaps and flips |
| Large equal strings | `0` | Handles maximum constraints efficiently |

## Edge Cases

Consider the case where every mismatch has the same direction.

Input:

```
444
777
```

The algorithm counts:

```
cnt47 = 3
cnt74 = 0
```

No complementary pair exists, so:

```
swaps = 0
flips = 3
```

The output becomes `3`. This is correct because swapping identical digits never changes the string.

Now consider the opposite scenario where every mismatch can be paired.

Input:

```
4477
7744
```

The algorithm computes:

```
cnt47 = 2
cnt74 = 2
```

Then:

```
swaps = 2
flips = 0
```

The answer is `2`. Each swap repairs two positions simultaneously, which is optimal.

Finally, consider a partially pairable example.

Input:

```
4447
7777
```

The mismatch counts become:

```
cnt47 = 3
cnt74 = 0
```

Again, no swaps are useful. The algorithm correctly outputs `3`.

A careless implementation that computes `mismatches // 2` would incorrectly produce `1`.
