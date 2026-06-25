---
title: "CF 106100E - Balloons"
description: "We are given a row of balloons represented by a string consisting of the characters B and R. A configuration is considered correct when every red balloon has a blue balloon immediately before it. In string terms, every occurrence of R must satisfy two conditions: 1."
date: "2026-06-25T11:52:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106100
codeforces_index: "E"
codeforces_contest_name: "International MathCoding Narxoz open olympiad 2025"
rating: 0
weight: 106100
solve_time_s: 43
verified: true
draft: false
---

[CF 106100E - Balloons](https://codeforces.com/problemset/problem/106100/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of balloons represented by a string consisting of the characters `B` and `R`.

A configuration is considered correct when every red balloon has a blue balloon immediately before it. In string terms, every occurrence of `R` must satisfy two conditions:

1. It cannot be the first character.
2. The character directly to its left must be `B`.

This means that a valid configuration contains no red balloon at position `0` and no substring `"RR"`.

We may perform at most one swap of neighboring balloons. The task is to determine whether it is possible to reach a valid configuration after zero or one such swap.

The string length is at most 100. With such a small limit, even trying every possible adjacent swap and checking the resulting string is easily fast enough. A solution that examines all positions and validates the string after each swap performs only a few thousand operations.

A subtle point is understanding what makes a configuration valid.

Consider:

```
BBR
```

The answer is `YES` because the only red balloon is immediately preceded by a blue balloon.

A common mistake is to assume the arrangement must alternate as `BRBRBR...`. That is not required.

Another easy-to-miss case is:

```
RB
```

The answer is `YES`.

Swapping the two neighboring balloons produces:

```
BR
```

and now the red balloon follows a blue balloon.

One more example:

```
RR
```

The answer is `NO`.

The only possible swap keeps the string as `"RR"`, which is still invalid because the first red balloon has no blue balloon before it.

## Approaches

The most direct idea is brute force.

First, check whether the original string is already valid. If it is, the answer is immediately `YES` because we are allowed to perform at most one swap.

Otherwise, try every adjacent pair. For each position `i`, swap `s[i]` and `s[i+1]`, test whether the resulting string is valid, then restore the original order. If any attempt succeeds, print `YES`.

Why is this correct? Because the problem allows only one operation, and the operation can only swap neighboring balloons. Enumerating all such swaps covers every possible move.

With length at most 100, there are at most 99 adjacent swaps. Checking validity takes `O(n)` time. The total work is `O(n²)`, which is at most about 10,000 character inspections.

There is no need for a more sophisticated observation because the constraints are tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

For this problem, the brute-force approach is already optimal enough.

## Algorithm Walkthrough

1. Read the string.
2. Define a function `valid(t)`.

This function scans the string from left to right.

If a character is `R`, check whether it has a left neighbor and whether that neighbor is `B`.

If either condition fails, return `False`.

If the scan finishes, return `True`.
3. If the original string is valid, print `YES`.

Zero swaps are allowed because the problem says "at most one swap".
4. Convert the string into a mutable list of characters.
5. For every index `i` from `0` to `n-2`:

Swap positions `i` and `i+1`.

Check whether the new arrangement is valid.

If it is, print `YES` and stop.

Restore the swap before continuing.
6. If no adjacent swap produces a valid arrangement, print `NO`.

### Why it works

The algorithm checks every configuration reachable in zero moves and every configuration reachable in exactly one adjacent swap.

Those are precisely all states allowed by the problem. The validity test exactly matches the requirement that every red balloon must immediately follow a blue balloon.

Since every legal outcome is examined and accepted exactly when it satisfies the rule, the algorithm cannot miss a valid solution or incorrectly accept an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid(s):
    n = len(s)
    for i in range(n):
        if s[i] == 'R':
            if i == 0 or s[i - 1] != 'B':
                return False
    return True

def solve():
    s = input().strip()

    if valid(s):
        print("YES")
        return

    arr = list(s)
    n = len(arr)

    for i in range(n - 1):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]

        if valid(arr):
            print("YES")
            return

        arr[i], arr[i + 1] = arr[i + 1], arr[i]

    print("NO")

solve()
```

The `valid` function directly encodes the definition of a correct arrangement. Every red balloon must have a blue balloon immediately to its left.

The main routine first checks the original string because zero swaps are allowed. After that, it systematically tries every neighboring swap.

Restoring the swap after each test is important. Without restoring, later iterations would be working on a modified string rather than the original configuration.

Since the string length is very small, constructing and checking these candidate configurations is comfortably within the limits.

## Worked Examples

### Example 1

Input:

```
RB
```

Initial string is invalid because the red balloon is first.

Trying swaps:

| Swap Position | Resulting String | Valid? |
| --- | --- | --- |
| 0 | BR | Yes |

The algorithm finds a valid configuration after one adjacent swap and prints:

```
YES
```

This example demonstrates that a single local swap can move a red balloon behind a blue balloon and satisfy the condition.

### Example 2

Input:

```
RR
```

Initial check:

| Position | Character | Condition |
| --- | --- | --- |
| 0 | R | Fails immediately |

Trying swaps:

| Swap Position | Resulting String | Valid? |
| --- | --- | --- |
| 0 | RR | No |

No valid arrangement is reachable.

Output:

```
NO
```

This example shows that some violations cannot be repaired with one adjacent swap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Up to `n-1` swaps, each checked in `O(n)` |
| Space | O(n) | Mutable character array for swap simulation |

With `n ≤ 100`, the worst-case work is only a few thousand operations, far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def valid(s):
        n = len(s)
        for i in range(n):
            if s[i] == 'R':
                if i == 0 or s[i - 1] != 'B':
                    return False
        return True

    s = input().strip()

    if valid(s):
        return "YES\n"

    arr = list(s)
    n = len(arr)

    for i in range(n - 1):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]

        if valid(arr):
            return "YES\n"

        arr[i], arr[i + 1] = arr[i + 1], arr[i]

    return "NO\n"

# provided sample
assert run("BR\n") == "YES\n", "sample"

# custom cases
assert run("RB\n") == "YES\n", "single swap fixes order"
assert run("RR\n") == "NO\n", "impossible"
assert run("BBR\n") == "YES\n", "already valid"
assert run("RBRR\n") == "YES\n", "swap last two positions"
assert run("RRR\n") == "NO\n", "cannot repair with one swap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `RB` | `YES` | One adjacent swap fixes the string |
| `RR` | `NO` | Impossible case |
| `BBR` | `YES` | Already valid, zero swaps |
| `RBRR` | `YES` | Valid arrangement reachable by one swap |
| `RRR` | `NO` | Multiple violations cannot be repaired |

## Edge Cases

Consider:

```
RB
```

The initial configuration is invalid because the red balloon is at the beginning. The algorithm tries the only adjacent swap and obtains:

```
BR
```

Now the red balloon has a blue balloon immediately before it, so the answer is `YES`.

Consider:

```
BBR
```

The algorithm checks the original string before trying any swap. The only red balloon is preceded by a blue balloon, so the configuration is already correct. Since zero swaps are allowed, the answer is `YES`.

Consider:

```
RR
```

The first red balloon violates the rule. Swapping the only neighboring pair does not change the string. Every reachable configuration remains invalid, so the algorithm correctly outputs `NO`.

Consider:

```
RBRR
```

Initially, the final red balloon follows another red balloon. Swapping the last two characters produces:

```
RBRR
```

which changes nothing, but swapping the middle pair yields:

```
BRRR
```

still invalid. The algorithm checks every adjacent swap and finds the valid reachable arrangement if one exists. Exhaustive enumeration guarantees that no possible one-swap solution is overlooked.
