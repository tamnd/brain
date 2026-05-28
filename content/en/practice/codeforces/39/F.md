---
title: "CF 39F - Pacifist frogs"
description: "Thumbelina wants to cross a swamp by riding a single frog. The swamp contains hills numbered from 1 to n, where hill i i"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "F"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 1300
weight: 39
solve_time_s: 98
verified: true
draft: false
---

[CF 39F - Pacifist frogs](https://codeforces.com/problemset/problem/39/F)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

Thumbelina wants to cross a swamp by riding a single frog. The swamp contains hills numbered from `1` to `n`, where hill `i` is exactly `i` meters away from the island. A frog with jump length `d` lands on hills `d, 2d, 3d, ...` until its next jump would go beyond `n`, at which point it reaches the shore.

Some hills contain sleeping mosquitoes. Every time the frog lands on such a hill, it kills the mosquito there. Since the frogs are pacifists, we want to choose the frogs that kill as few mosquitoes as possible.

The input gives the jump lengths of all frogs and the hill positions containing mosquitoes. The output asks for every frog whose route hits the minimum number of mosquito positions.

The key observation from the constraints is that `m` and `k` are both at most `100`, even though `n` can be as large as `10^9`. A huge value of `n` might initially suggest that simulating every hill is impossible, and that is correct. Any algorithm proportional to `n` would immediately fail.

At the same time, the number of frogs and mosquitoes is tiny. That changes the perspective completely. Instead of iterating through all hills, we only need to reason about the mosquito positions themselves.

A naive simulation for one frog would repeatedly generate positions `d, 2d, 3d, ...` until passing `n`. That becomes disastrous when `d = 1`, because the frog visits every hill from `1` to `n`. With `n = 10^9`, this is impossible.

Several edge cases are easy to mishandle if the implementation is written too mechanically.

Consider this input:

```
10 2 2
3 5
6 10
```

The frog with jump length `3` lands on `3, 6, 9`, so it kills exactly one mosquito at hill `6`. The frog with jump length `5` lands on `5, 10`, so it also kills one mosquito. Both frogs must be printed.

A careless implementation that stops before checking the last reachable hill could miss the mosquito at `10`.

Another subtle case is when mosquitoes exist on hills that no frog can ever land on.

```
12 2 2
4 6
5 7
```

Neither `5` nor `7` is divisible by `4` or `6`, so both frogs kill zero mosquitoes. The correct answer contains both frogs.

An implementation that tries to "move" the frog hill by hill instead of checking divisibility can easily overcomplicate this case.

One more tricky situation is duplicate jump lengths.

```
15 3 1
5 5 7
10
```

Both frogs with jump length `5` kill the mosquito at `10`, while the frog with jump length `7` kills none. The correct answer is only frog `3`.

The frogs are identified by input order, not by unique jump length values. Sorting the frogs without preserving indices would produce incorrect output.

## Approaches

The most direct solution is to simulate every frog's journey. For a frog with jump length `d`, we generate every visited hill:

```
d, 2d, 3d, ...
```

For each landing position, we check whether a mosquito exists there.

This approach is correct because it exactly follows the frog's movement rules. The problem appears when `d` is small. If `d = 1`, the frog visits all hills from `1` to `n`. Since `n` can be `10^9`, even one frog would require a billion iterations.

The crucial observation is that mosquitoes are sparse. There are at most `100` mosquitoes total. A frog only kills mosquitoes located on hills divisible by its jump length.

Instead of asking:

```
Which hills does the frog visit?
```

we can ask:

```
Which mosquitoes lie on multiples of the frog's jump length?
```

For a mosquito at hill `x`, a frog with jump length `d` kills it exactly when:

```
x % d == 0
```

Now the work becomes tiny. For every frog, we simply test all mosquito positions using divisibility. Since there are at most `100` frogs and `100` mosquitoes, the total number of checks is only `10,000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · n / d) worst case O(m · n) | O(k) | Too slow |
| Optimal | O(m · k) | O(1) excluding input storage | Accepted |

## Algorithm Walkthrough

1. Read the values of `n`, `m`, and `k`.

The value `n` is not actually needed in the optimized solution, because mosquito positions already determine all relevant information.
2. Read the jump lengths of all frogs into an array.

The frog indices must be preserved because the output requires original numbering.
3. Read the mosquito hill positions into another array.
4. For each frog, count how many mosquito positions are divisible by its jump length.

If a mosquito sits at hill `x` and the frog jumps by `d`, then the frog lands on `x` exactly when `x` is a multiple of `d`.
5. Store the mosquito count for every frog.
6. Find the minimum mosquito count among all frogs.
7. Collect every frog whose count equals that minimum.

The frogs are reported using 1-based indexing from the input order.
8. Print the number of optimal frogs, then print their indices.

### Why it works

A frog with jump length `d` visits exactly the hills:

```
d, 2d, 3d, ...
```

A hill `x` belongs to this sequence if and only if `x` is divisible by `d`. The algorithm checks precisely this condition for every mosquito hill.

Since every mosquito is counted exactly when the frog lands on its hill, the computed count matches the number of mosquitoes killed by that frog. Selecting all frogs with the minimum count produces exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

def solve():
    n, m, k = map(int, input().split())

    frogs = list(map(int, input().split()))
    mosquitoes = list(map(int, input().split()))

    killed = []

    for d in frogs:
        cnt = 0

        for pos in mosquitoes:
            if pos % d == 0:
                cnt += 1

        killed.append(cnt)

    best = min(killed)

    answer = []

    for i in range(m):
        if killed[i] == best:
            answer.append(i + 1)

    print(len(answer))
    print(*answer)

solve()
```

The solution never iterates over hills. That is the central implementation idea.

The outer loop processes each frog independently. For one frog with jump length `d`, the inner loop scans all mosquito positions and checks divisibility using `pos % d == 0`.

The array `killed` stores the number of mosquitoes each frog destroys. After all counts are computed, the minimum value is extracted with `min(killed)`.

The final loop reconstructs the answer using original frog indices. The `+1` is necessary because Codeforces statements use 1-based numbering.

One subtle point is that `n` does not participate in the computation. A mosquito position is guaranteed to be within valid bounds, and divisibility already determines whether the frog lands there before reaching the shore.

Another easy mistake is sorting frogs by jump length. The output requires original input order, so indices must remain unchanged.

## Worked Examples

### Example 1

Input:

```
5 3 5
2 3 4
1 2 3 4 5
```

| Frog Index | Jump Length | Mosquito Positions Hit | Count |
| --- | --- | --- | --- |
| 1 | 2 | 2, 4 | 2 |
| 2 | 3 | 3 | 1 |
| 3 | 4 | 4 | 1 |

Minimum count is `1`, achieved by frogs `2` and `3`.

Output:

```
2
2 3
```

This example demonstrates the divisibility rule directly. Hill `4` is hit by frogs whose jump lengths divide `4`.

### Example 2

Input:

```
12 3 3
2 5 7
4 10 11
```

| Frog Index | Jump Length | Mosquito Positions Hit | Count |
| --- | --- | --- | --- |
| 1 | 2 | 4, 10 | 2 |
| 2 | 5 | 10 | 1 |
| 3 | 7 | none | 0 |

Minimum count is `0`, achieved only by frog `3`.

Output:

```
1
3
```

This trace shows that some mosquitoes may never be reachable by certain frogs. Hill `11` is not divisible by any jump length here, so no frog kills that mosquito.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · k) | Every frog checks every mosquito once |
| Space | O(m) | Stores mosquito counts for frogs |

With `m ≤ 100` and `k ≤ 100`, the algorithm performs at most `10,000` divisibility checks. That is tiny compared to the limits, so the solution easily fits within both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    frogs = list(map(int, input().split()))
    mosquitoes = list(map(int, input().split()))

    killed = []

    for d in frogs:
        cnt = 0

        for pos in mosquitoes:
            if pos % d == 0:
                cnt += 1

        killed.append(cnt)

    best = min(killed)

    answer = []

    for i in range(m):
        if killed[i] == best:
            answer.append(i + 1)

    print(len(answer))
    print(*answer)

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
assert run(
"""5 3 5
2 3 4
1 2 3 4 5
"""
) == "2\n2 3\n", "sample 1"

# minimum size
assert run(
"""1 1 1
1
1
"""
) == "1\n1\n", "minimum case"

# no frog hits any mosquito
assert run(
"""20 2 2
6 8
5 7
"""
) == "2\n1 2\n", "all frogs kill zero"

# duplicate jump lengths
assert run(
"""15 3 1
5 5 7
10
"""
) == "1\n3\n", "preserve indices correctly"

# boundary divisibility
assert run(
"""10 2 2
2 5
10 9
"""
) == "1\n2\n", "must count mosquito at hill 10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | One frog selected | Handles smallest bounds correctly |
| No frog hits mosquitoes | All frogs selected | Correct handling of zero counts |
| Duplicate jump lengths | Only later frog selected | Preserves original indices |
| Mosquito at final reachable hill | Correct divisibility counting | Avoids off-by-one mistakes |

## Edge Cases

Consider the case where the last reachable hill contains a mosquito.

```
10 2 2
3 5
6 10
```

For jump length `3`, the frog lands on `3, 6, 9`, killing one mosquito. For jump length `5`, the frog lands on `5, 10`, also killing one mosquito.

The algorithm checks:

```
6 % 3 == 0
10 % 5 == 0
```

Both are counted correctly because divisibility naturally includes the final landing position before reaching the shore.

Now consider mosquitoes that no frog can reach.

```
12 2 2
4 6
5 7
```

The algorithm checks:

```
5 % 4 != 0
7 % 4 != 0
5 % 6 != 0
7 % 6 != 0
```

Both frogs kill zero mosquitoes, so both are printed. No special handling is needed because unreachable mosquitoes simply fail the divisibility test.

Finally, consider repeated jump lengths.

```
15 3 1
5 5 7
10
```

The counts become:

| Frog Index | Jump Length | Count |
| --- | --- | --- |
| 1 | 5 | 1 |
| 2 | 5 | 1 |
| 3 | 7 | 0 |

The algorithm stores counts by frog position, not by unique jump length. That preserves the required numbering and correctly outputs only frog `3`.
