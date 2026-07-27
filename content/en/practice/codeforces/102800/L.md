---
title: "CF 102800L - Swimmer"
description: "Each swimmer moves back and forth in a lane of length m. Every swimmer starts at position 0, swims toward position m, immediately turns around upon reaching it, and repeats this motion forever. The speed of swimmer i is fixed and equal to x[i] meters per second."
date: "2026-07-27T17:44:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "L"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 57
verified: true
draft: false
---

[CF 102800L - Swimmer](https://codeforces.com/problemset/problem/102800/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each swimmer moves back and forth in a lane of length `m`. Every swimmer starts at position `0`, swims toward position `m`, immediately turns around upon reaching it, and repeats this motion forever. The speed of swimmer `i` is fixed and equal to `x[i]` meters per second. Every query asks for the position of one specific swimmer after a given number of seconds.

The swimmers never interact with each other, so every query is completely independent. The only information needed for a query is the swimmer's speed, the lane length, and the elapsed time.

The constraints are the real challenge. There can be up to `10^6` swimmers and `10^6` queries. Any algorithm that simulates movement second by second is immediately impossible because a single query may involve up to `10^9` seconds. Even simulating every turn would also fail, since a fast swimmer may complete hundreds of millions of trips. With one million queries, only constant time work per query is practical. Reading the input alone already takes linear time in the input size, so the algorithm should spend only `O(1)` additional work for each query.

Several edge cases are easy to mishandle.

Consider reaching the wall exactly.

```
Input
1 5 1
1
5 1
```

The swimmer has traveled exactly `5` meters, so the correct answer is

```
5
```

A careless implementation that always reflects after taking a remainder could incorrectly return `0`.

Now consider landing exactly at the end of a complete back and forth cycle.

```
Input
1 5 1
1
10 1
```

The swimmer has gone from `0` to `5` and back to `0`, so the correct answer is

```
0
```

Confusing the cycle length with `m` instead of `2m` would incorrectly return `5`.

Another common mistake is forgetting that the swimmer reverses direction after reaching the far wall.

```
Input
1 3 1
2
2 1
```

The swimmer travels `4` meters in total. After reaching position `3`, one meter of movement remains while heading back, so the answer is

```
2
```

Simply computing `(speed × time) % m` would incorrectly return `1`.

## Approaches

The most direct solution is to simulate the swimmer's movement. Starting from position `0`, repeatedly advance the swimmer until reaching one of the walls, reverse direction, and continue until the requested time has elapsed. This matches the physical process exactly, so it is obviously correct. Unfortunately, it is far too slow. A single query may involve billions of seconds or hundreds of millions of turns, making the worst case completely infeasible.

The key observation is that the swimmer's motion is perfectly periodic. Imagine extending the lane into a straight infinite line instead of reflecting at the walls. After traveling a total distance

```
distance = speed × time
```

the swimmer would simply be at that distance from the start.

Reflection can be modeled by folding this infinite line every `2m` meters. One complete period consists of swimming from `0` to `m` and then back from `m` to `0`, giving a cycle length of `2m`.

Let

```
r = (speed × time) mod (2m)
```

If `r ≤ m`, the swimmer is still on the outward trip, so the position is simply `r`.

Otherwise, the swimmer is on the return trip. The remaining distance from the far wall is `r - m`, so the position is

```
2m - r
```

Each query now requires only one multiplication, one modulo operation, and one comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible to bound efficiently, up to `O(speed × time)` simulation | `O(1)` | Too slow |
| Optimal | `O(1)` per query | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the number of swimmers, the lane length, and the number of queries.
2. Read the speeds of all swimmers into an array so each query can access its swimmer's speed in constant time.
3. Compute the cycle length as `cycle = 2 × m`, because every complete outward and return trip covers exactly `2m` meters.
4. For each query, retrieve the swimmer's speed and compute the total distance traveled as `speed × time`.
5. Reduce this distance modulo `cycle`. Everything before the last incomplete cycle repeats exactly, so only the remainder affects the current position.
6. If the remainder is at most `m`, the swimmer is moving away from the start, so output the remainder.
7. Otherwise, the swimmer is moving back toward the start. Reflect the remainder across the far wall by outputting `cycle - remainder`.

### Why it works

The swimmer's position depends only on where they are within the current `2m` meter cycle. Every full cycle ends at exactly the same position and direction as it began, so removing complete cycles with a modulo operation preserves the answer. Inside one cycle, the path is a straight segment from `0` to `m` followed by a straight segment from `m` back to `0`. The two formulas correspond exactly to these two halves, so every possible remainder maps to the correct physical position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    speeds = list(map(int, input().split()))

    cycle = 2 * m
    out = []

    for _ in range(q):
        p, k = map(int, input().split())
        r = (speeds[k - 1] * p) % cycle
        if r <= m:
            out.append(str(r))
        else:
            out.append(str(cycle - r))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The program first stores every swimmer's speed so that each query can access it with direct indexing. Since swimmers are numbered from one while Python lists are zero indexed, the code uses `k - 1`.

The cycle length is computed once because it never changes. Every query performs the same sequence of arithmetic operations. Python integers safely handle values as large as `10^9 × 10^9 = 10^18`, so overflow is not an issue.

The comparison uses `<= m` rather than `< m`. When the remainder is exactly `m`, the swimmer has just reached the far wall and is still located at position `m`. Using a strict comparison would incorrectly reflect this point back to itself only by coincidence, and using different formulas in other languages could introduce subtle bugs.

The modulo is taken with `2m`, not `m`. Using `m` would completely lose information about whether the swimmer is moving outward or returning.

## Worked Examples

### Example 1

```
Input
1 3 2
5
1 1
7 1
```

| Query | Speed | Time | Total Distance | Remainder mod 6 | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 5 | 5 | 1 |
| 2 | 5 | 7 | 35 | 5 | 1 |

Both queries end at the same remainder because the swimmer completes several full cycles before reaching the same point again. The trace confirms that only the remainder inside one cycle matters.

### Example 2

```
Input
2 5 3
2 3
2 1
2 2
5 2
```

| Query | Speed | Time | Total Distance | Remainder mod 10 | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 4 | 4 | 4 |
| 2 | 3 | 2 | 6 | 6 | 4 |
| 3 | 3 | 5 | 15 | 5 | 5 |

The second query demonstrates the reflection step because the remainder exceeds `m`. The third query lands exactly on the turning point, confirming that the boundary value is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + q)` | Reading the speeds takes linear time, each query is constant time. |
| Space | `O(n)` | The speed array is stored once. |

The input itself already contains `n` speeds and `q` queries, so linear preprocessing is unavoidable. Constant work for every query easily satisfies the constraints, even when both `n` and `q` are one million.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n, m, q = map(int, input().split())
    speeds = list(map(int, input().split()))
    cycle = 2 * m
    ans = []
    for _ in range(q):
        p, k = map(int, input().split())
        r = (speeds[k - 1] * p) % cycle
        if r <= m:
            ans.append(str(r))
        else:
            ans.append(str(cycle - r))
    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

# provided sample
assert run("1 3 2\n5\n1 1\n7 1\n") == "1\n1"

# minimum input
assert run("1 1 1\n1\n0 1\n") == "0"

# exact turning point
assert run("1 5 1\n1\n5 1\n") == "5"

# complete cycle
assert run("1 5 1\n1\n10 1\n") == "0"

# reflection
assert run("1 3 1\n2\n2 1\n") == "2"

# multiple swimmers
assert run("2 5 2\n2 3\n2 1\n2 2\n") == "4\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single swimmer, zero time | `0` | Minimum input and no movement |
| Reach position `m` exactly | `5` | Correct handling of the turning point |
| Complete cycle | `0` | Correct modulo period of `2m` |
| Reflection example | `2` | Returning half of the cycle |
| Multiple swimmers | `4`, `4` | Correct indexing into the speed array |

## Edge Cases

When the swimmer reaches the far wall exactly, the remainder equals `m`.

```
Input
1 5 1
1
5 1
```

The algorithm computes `r = 5 mod 10 = 5`. Since `5 ≤ 5`, it returns `5`, matching the swimmer's actual position at the wall.

When the swimmer completes an entire round trip, the remainder becomes zero.

```
Input
1 5 1
1
10 1
```

The algorithm computes `r = 10 mod 10 = 0`. The first branch returns `0`, which is exactly the starting position after one complete cycle.

When the swimmer has already turned around, reflection is required.

```
Input
1 3 1
2
2 1
```

The total distance is `4`. The algorithm computes `r = 4 mod 6 = 4`. Since `4 > 3`, it returns `6 - 4 = 2`. Physically, the swimmer reaches position `3` after `1.5` seconds and then swims back one more meter, ending at position `2`, exactly matching the computed result.
