---
title: "CF 106103H - Square"
description: "We are given multiple test cases, and each test case consists of four stick lengths. Each stick is rigid: we cannot cut it, extend it, or bend it. The task is to determine whether these four sticks can be arranged to form a geometric square."
date: "2026-06-25T11:44:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106103
codeforces_index: "H"
codeforces_contest_name: "AGM 2025, Final Round, Day 2"
rating: 0
weight: 106103
solve_time_s: 36
verified: true
draft: false
---

[CF 106103H - Square](https://codeforces.com/problemset/problem/106103/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple test cases, and each test case consists of four stick lengths. Each stick is rigid: we cannot cut it, extend it, or bend it. The task is to determine whether these four sticks can be arranged to form a geometric square.

A square here means a closed loop with four equal-length sides and right angles. Since we are only allowed to use the sticks as straight segments, the only freedom we have is how to assign each stick to a side of the square.

The key modeling step is to translate the geometric requirement into a constraint on the stick lengths. A square has four sides, all equal. Because each stick is a single rigid segment, each side of the square must correspond to exactly one stick. There is no operation that allows us to split or merge sticks into smaller segments, so the structure of the final shape is completely determined by equality of the four input values.

The input size is small per test case, but there can be up to 10^4 test cases. That means any solution that does constant work per test case is fine, while anything involving sorting large structures or nested loops over test cases would still be fine but unnecessary. The constraints push us toward a direct constant-time check.

A subtle edge case arises when one tries to overthink grouping. For example, one might imagine combining sticks like 1, 2, 1, 2 to form four sides of length 2 or 3. This is invalid because sticks cannot be broken or concatenated. Another mistake is assuming we only need the total sum to be divisible by 4, which would be correct in a flexible cutting problem but not here.

Concrete failing intuition:

Input:

```
1
1 2 1 2
```

Some might guess we can form a square of side 1.5 or that pairing helps, but we cannot split sticks, so no configuration produces four equal sides. Correct output is `NO`.

Input:

```
1
5 5 5 5
```

All sticks already match, so we can directly assign each to a side. Output is `YES`.

## Approaches

A brute-force interpretation would try to assign sticks to four sides and verify geometric feasibility. Since we only have four sticks, one could attempt all permutations of assignments and even consider grouping decisions if splitting were allowed. That quickly becomes unnecessary complexity because the structure of the target shape is extremely rigid: every side must match a single stick exactly. Even a naive geometric construction step would still collapse to checking equality of side lengths after realizing no alternative assembly is legal.

The key observation is that the square constraint eliminates all degrees of freedom. Once we accept that each side must be exactly one stick, the problem reduces to verifying whether all four values are identical. Any deviation breaks at least one side equality condition, making the construction impossible.

So the “geometry” part disappears entirely, and what remains is a simple equality test over four integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force arrangements | O(1) (constant permutations) | O(1) | Overkill |
| Check all equal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four stick lengths for a test case. These represent the only available segments that can form the square.
2. Compare all four values against the first stick. The reasoning is that if a square is possible, every side must be identical, so all must match a single reference value.
3. If any stick differs from the first, immediately conclude that forming a square is impossible.
4. If all four values match, conclude that they directly form the four sides of a square.

The decision is entirely local to each test case, so there is no interaction between cases and no accumulated state.

### Why it works

A square requires four equal sides. Since sticks cannot be modified, each side must be exactly one stick. That means the multiset of side lengths must contain a single unique value repeated four times. Any deviation introduces at least one side with a different length, breaking the definition of a square. There is no alternative construction that compensates for mismatched lengths, so equality is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        if a == b == c == d:
            out.append("YES")
        else:
            out.append("NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and performs a single chained equality check. The chained comparison `a == b == c == d` is a compact way to ensure all values are identical without explicitly writing pairwise conditions. Output is buffered to avoid repeated I/O overhead.

A common implementation mistake is checking only partial equality, such as `a == b and c == d`, which incorrectly accepts cases like `1 1 2 2`. Another mistake is sorting and checking adjacent equality, which is still correct but unnecessary overhead for such small fixed-size input.

## Worked Examples

Consider the input:

```
1
1 2 3 4
```

| Step | a | b | c | d | Decision |
| --- | --- | --- | --- | --- | --- |
| Read | 1 | 2 | 3 | 4 | - |
| Compare | 1 | 2 | 3 | 4 | mismatch found |
| Output | - | - | - | - | NO |

This shows a case where all values differ, so no square can be formed.

Now consider:

```
1
2 2 2 2
```

| Step | a | b | c | d | Decision |
| --- | --- | --- | --- | --- | --- |
| Read | 2 | 2 | 2 | 2 | - |
| Compare | 2 | 2 | 2 | 2 | all equal |
| Output | - | - | - | - | YES |

This confirms that identical sticks trivially form a square.

These two traces cover both acceptance and rejection paths, showing that the algorithm only depends on equality structure and not ordering or pairing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant number of comparisons over four integers |
| Space | O(1) | Only a few variables are used, output buffering aside |

The solution is well within limits because even for 10^4 test cases, we only perform a few integer comparisons per case. No sorting, recursion, or graph processing is involved.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()

    def solve():
        input = sys.stdin.readline
        t = int(input())
        res = []
        for _ in range(t):
            a, b, c, d = map(int, input().split())
            res.append("YES" if a == b == c == d else "NO")
        print("\n".join(res))

    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("7\n1 2 3 4\n1 1 1 1\n2 2 2 2\n1 2 1 2\n1 1 5 5\n5 5 5 5\n4 10 5 9\n") == \
"NO\nYES\nYES\nNO\nNO\nYES\nNO"

# all equal minimum case
assert run("1\n1 1 1 1\n") == "YES", "all equal"

# one differing element
assert run("1\n1 1 1 2\n") == "NO", "single mismatch"

# alternating pairs
assert run("1\n3 3 4 4\n") == "NO", "pair symmetry not enough"

# larger identical values
assert run("1\n100 100 100 100\n") == "YES", "large equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | simplest valid square |
| single mismatch | NO | detects minimal violation |
| pair symmetry | NO | prevents incorrect pairing assumption |
| large equal values | YES | no numeric edge issues |

## Edge Cases

A common failure case is assuming pairing is enough, such as treating `(a == b and c == d)` as sufficient. For input `1 1 2 2`, that logic incorrectly returns YES. The correct algorithm rejects it immediately because not all four values match.

Input:

```
1
1 1 2 2
```

Execution:

The first comparison passes for `a == b`, but `a == c` fails, so the algorithm stops and returns `NO`.

Another subtle case is when values are all distinct but form a visually “balanced” set like `2 3 4 5`. There is no partial structure that helps; the check fails immediately on the second comparison.

Input:

```
1
2 3 4 5
```

The mismatch is detected during the first equality scan, producing `NO` without needing any further reasoning.
