---
title: "CF 1392D - Omkar and Bed Wars"
description: "Each player sits on a circle and attacks exactly one of their two neighbors. We are given a circular string consisting of L and R. If player i attacks left, we write L. If they attack right, we write R."
date: "2026-06-11T10:10:54+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1392
codeforces_index: "D"
codeforces_contest_name: "Codeforces Global Round 10"
rating: 1700
weight: 1392
solve_time_s: 337
verified: false
draft: false
---

[CF 1392D - Omkar and Bed Wars](https://codeforces.com/problemset/problem/1392/D)

**Rating:** 1700  
**Tags:** dp, greedy  
**Solve time:** 5m 37s  
**Verified:** no  

## Solution
## Problem Understanding

Each player sits on a circle and attacks exactly one of their two neighbors. We are given a circular string consisting of `L` and `R`.

If player `i` attacks left, we write `L`. If they attack right, we write `R`.

A player is considered logical according to the game's rules:

- If exactly one neighbor attacks them, they must attack that neighbor back.
- If zero or two neighbors attack them, either attack direction is acceptable.

We may flip any player's choice from `L` to `R` or from `R` to `L`. Each flipped player costs one operation. We must find the minimum number of flips needed so that every player becomes logical.

The first challenge is understanding what a logical final configuration looks like.

Suppose we look at a player whose attack direction differs from one of its neighbors. For example, a boundary `RL` appears. The left player attacks right and the right player attacks left, so they attack each other. Such positions are already perfectly consistent.

The interesting part is what happens inside a maximal block of equal characters:

```
RRRRR
```

or

```
LLLL
```

Inside such a block, the middle players are problematic. They receive exactly one incoming attack but do not attack back, so some changes are required.

The constraints are large. The total length of all strings is at most `2·10^5`, and there may be up to `10^4` test cases. Any solution that examines all possible flip combinations is impossible. Even an `O(n²)` algorithm would perform around `4·10^10` operations in the worst case. We need a linear solution.

Several edge cases are easy to miss.

Consider:

```
n = 5
RRRRR
```

Because the string is circular, this is one single run of length 5, not five separate positions. A linear run-processing algorithm that forgets the circle would compute the wrong answer.

Another example is:

```
RLRLRL
```

Every player already attacks back the unique player attacking them. The answer is `0`.

A third subtle case is:

```
RRRLLL
```

The first and last runs touch through the circular boundary only if they have the same character. Here they do not, so there are actually two separate runs of length 3. Treating the string as one merged run would be incorrect.

## Approaches

A brute-force approach would try every subset of players to flip and check whether the resulting configuration is logical. There are `2^n` possible flip patterns, which becomes completely infeasible even for `n = 40`, let alone `n = 200000`.

To obtain something useful, we need to understand the structure of valid configurations.

Look at a maximal run of identical characters:

```
RRRRRR
```

Consider three consecutive players inside the run. The middle player is attacked only from one side. Since they attack in the same direction as everyone else, they do not attack back. Such players violate the rule.

Changing one player's direction can repair at most three consecutive positions in a run. This leads to a familiar pattern: every block of three equal consecutive directions requires one modification.

For a linear run of length `k`, the minimum number of changes is:

```
k // 3
```

This is exactly the same counting argument used in many "break long runs" problems.

The only complication is the circular structure.

If the entire circle consists of a single character, such as:

```
RRRRRRR
```

there is only one run of length `n`, and the answer is:

```
(n + 2) // 3
```

Otherwise, at least one boundary exists where adjacent characters differ. Such a boundary breaks the circle naturally. Once we cut the circle at any position where characters differ, the problem becomes linear. Every maximal run can then be processed independently, contributing `length // 3`.

This yields a simple linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether all characters in the circular string are identical.

If they are, the entire circle forms one run of length `n`. The answer is `(n + 2) // 3`.
2. Otherwise, find any position where adjacent characters differ.

Such a position always exists because not all characters are equal.
3. Rotate the circle conceptually so that this position becomes the starting point.

After this cut, the first and last characters of the resulting sequence are different, which means no run wraps around the boundary anymore.
4. Traverse the rotated sequence and compute the length of every maximal run of equal characters.
5. For each run of length `len`, add `len // 3` to the answer.

Every three consecutive equal directions inside a run require one flip, and these requirements are independent between runs.
6. Output the accumulated answer.

### Why it works

When a run has length `len`, every player except those near the boundaries behaves identically. The problematic positions occur in groups of three consecutive equal directions. One carefully chosen flip can repair at most one such group, so at least `len // 3` flips are necessary.

Conversely, placing a flip every third position inside the run achieves exactly `len // 3` changes and makes all players logical. Since different runs are separated by direction changes, their corrections do not interact. Summing `len // 3` over all runs gives the global optimum.

For the special case where the entire circle is one run, there is no natural boundary. The circular run of length `n` requires `ceil(n/3)` changes, which equals `(n + 2) // 3`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        if s.count(s[0]) == n:
            print((n + 2) // 3)
            continue

        pos = 0
        while s[pos] == s[(pos + 1) % n]:
            pos += 1

        s = s[pos + 1:] + s[:pos + 1]

        ans = 0
        cnt = 1

        for i in range(1, n):
            if s[i] == s[i - 1]:
                cnt += 1
            else:
                ans += cnt // 3
                cnt = 1

        ans += cnt // 3
        print(ans)

solve()
```

The first branch handles the special situation where the entire circle is a single run. In that case the standard run decomposition does not work because there is no differing boundary to cut at.

For all other cases, we locate any adjacent pair with different characters. Cutting immediately after such a pair guarantees that the first and last characters of the rotated string are different. This converts the circular run structure into an ordinary linear run structure.

The traversal computes maximal run lengths with a standard counter. Whenever a run ends, we add `run_length // 3` to the answer. After the loop, the final run must also be processed.

A common mistake is forgetting the all-equal case. Without the special handling, the rotation step cannot find a valid cut and the formula becomes incorrect.

Another easy error is cutting at an arbitrary position. If the cut lies inside a run, a circular run may be split into two smaller runs, causing undercounting.

## Worked Examples

### Example 1

Input:

```
6
LRRRRL
```

The string is not uniform.

Choose a boundary where characters differ:

```
L | RRRR | L
```

After rotation, the run lengths are:

| Run | Length | Contribution |
| --- | --- | --- |
| L | 1 | 0 |
| RRRR | 4 | 1 |
| L | 1 | 0 |

Total answer:

| Current Run Length | Added |
| --- | --- |
| 1 | 0 |
| 4 | 1 |
| 1 | 0 |

Answer = `1`.

The only significant run is the block of four `R`s. A run of length four requires exactly one modification.

### Example 2

Input:

```
5
RRRRR
```

All characters are identical.

| n | Formula | Answer |
| --- | --- | --- |
| 5 | (5 + 2) // 3 | 2 |

Answer = `2`.

This example demonstrates why the special case is necessary. There is no differing boundary to cut on, so the generic run-processing approach cannot be applied directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed a constant number of times |
| Space | O(1) | Only a few counters are stored |

The total length over all test cases is at most `2·10^5`, so a linear scan of every string easily fits within the time limit. Memory usage remains constant apart from storing the input string itself.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            s = input().strip()

            if s.count(s[0]) == n:
                out.append(str((n + 2) // 3))
                continue

            pos = 0
            while s[pos] == s[(pos + 1) % n]:
                pos += 1

            s = s[pos + 1:] + s[:pos + 1]

            ans = 0
            cnt = 1

            for i in range(1, n):
                if s[i] == s[i - 1]:
                    cnt += 1
                else:
                    ans += cnt // 3
                    cnt = 1

            ans += cnt // 3
            out.append(str(ans))

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""5
4
RLRL
6
LRRRRL
8
RLLRRRLL
12
LLLLRRLRRRLL
5
RRRRR
"""
) == """0
1
1
3
2"""

# minimum size
assert run(
"""1
3
RLR
"""
) == "0"

# all equal
assert run(
"""1
6
LLLLLL
"""
) == "2"

# single long run after cut
assert run(
"""1
8
RRRRLLRL
"""
) == "1"

# boundary wraparound case
assert run(
"""1
6
RRRLLL
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `RLR` | `0` | Smallest valid size, already logical |
| `LLLLLL` | `2` | All-equal circular run |
| `RRRRLLRL` | `1` | One long run contributes `4 // 3` |
| `RRRLLL` | `2` | Multiple runs, no wraparound merge |

## Edge Cases

Consider:

```
n = 5
RRRRR
```

The algorithm detects that every character is identical. It immediately returns:

```
(5 + 2) // 3 = 2
```

No rotation is attempted. This avoids the failure that occurs if we search forever for a differing boundary.

Now consider:

```
n = 6
RRRLLL
```

The string is not uniform. A differing boundary exists between the third `R` and first `L`.

The run decomposition becomes:

```
RRR
LLL
```

The contributions are:

```
3 // 3 + 3 // 3 = 2
```

giving the correct answer `2`.

Finally, consider:

```
n = 8
RLRLRLRL
```

Every run has length `1`.

The algorithm computes:

```
1 // 3 + 1 // 3 + ...
```

which sums to `0`.

This confirms that already-valid configurations are recognized without any unnecessary modifications.
