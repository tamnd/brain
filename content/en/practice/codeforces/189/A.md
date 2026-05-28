---
title: "CF 189A - Cut Ribbon"
description: "We have a ribbon of total length n. Every cut piece must have one of exactly three allowed lengths: a, b, or c. The goal is not just to split the ribbon successfully, but to maximize how many total pieces we obtain."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 189
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 119 (Div. 2)"
rating: 1300
weight: 189
solve_time_s: 91
verified: true
draft: false
---

[CF 189A - Cut Ribbon](https://codeforces.com/problemset/problem/189/A)

**Rating:** 1300  
**Tags:** brute force, dp  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a ribbon of total length `n`. Every cut piece must have one of exactly three allowed lengths: `a`, `b`, or `c`. The goal is not just to split the ribbon successfully, but to maximize how many total pieces we obtain.

For example, if the ribbon length is `5` and the allowed lengths are `5`, `3`, and `2`, cutting it into a single piece of length `5` works, but cutting it into pieces `3 + 2` produces two pieces, which is better.

The constraint `n ≤ 4000` is small enough for dynamic programming. An algorithm with roughly `O(n)` or `O(n^2)` operations easily fits within the limit. A true brute-force recursion that explores all possible cut sequences would still terminate for these bounds, but it repeats the same subproblems many times and becomes unnecessarily expensive.

The tricky part is that not every intermediate length is reachable. A careless implementation may accidentally treat impossible states as valid and build answers from them.

Consider this example:

```
7 5 2 5
```

The correct answer is `2`, because we can cut `5 + 2`.

Suppose a DP array is initialized with zeros. Then state `dp[1]` would incorrectly appear reachable with value `0`, and later transitions could build fake solutions from it. Impossible states must be marked distinctly, usually with `-1` or negative infinity.

Another subtle case appears when all lengths are equal:

```
9 3 3 3
```

The correct answer is `3`. Some implementations try to remove duplicate lengths or use unnecessary branching logic that complicates transitions. The problem becomes much simpler if we just treat all three lengths uniformly.

One more edge case is when the optimal answer requires many small cuts rather than a larger valid cut:

```
8 5 3 2
```

The valid decompositions include `5 + 3` with two pieces and `2 + 2 + 2 + 2` with four pieces. A greedy strategy that always takes the largest piece first fails here.

## Approaches

A direct brute-force approach tries every possible sequence of cuts. From a ribbon of length `x`, we recursively attempt cutting off `a`, `b`, and `c`, then solve the remaining length.

The recursion is naturally correct because every valid cutting sequence is explored. The problem is repetition. If we compute the best answer for length `20`, we may later recompute it again from another path. The number of recursive calls grows exponentially in the worst case.

For `n = 4000`, exponential complexity is far too large. Even something like `3^30` operations is already impossible within one second.

The key observation is that the problem has overlapping subproblems. The best answer for a ribbon length `x` depends only on the best answers for lengths `x-a`, `x-b`, and `x-c`.

That makes this a classic dynamic programming problem.

We define:

```
dp[i] = maximum number of pieces that can form length i
```

If a length cannot be formed, we keep it marked as impossible.

From a reachable length `i`, we try extending it using each allowed cut size. Every transition adds one more piece.

Because each state depends only on smaller lengths, we can compute the answers iteratively from `0` up to `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) recursion stack | Too slow |
| Optimal Dynamic Programming | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a DP array of size `n + 1`.

Each position `dp[i]` stores the maximum number of pieces that can produce total length `i`.
2. Initialize all states as impossible.

We use `-1` for impossible states because `0` is a valid answer only for length `0`.
3. Set `dp[0] = 0`.

A ribbon of length `0` needs zero pieces, so this is our starting state.
4. Iterate through all lengths from `0` to `n`.

For every reachable length, try adding one more piece of length `a`, `b`, and `c`.
5. For every cut length `x` in `{a, b, c}`:

If `i + x ≤ n`, update:

```
dp[i + x] = max(dp[i + x], dp[i] + 1)
```

We add one because we are using one additional ribbon piece.
6. After processing all states, print `dp[n]`.

The statement guarantees at least one valid cutting exists, so the final answer will always be reachable.

### Why it works

The DP invariant is:

```
dp[i] always stores the maximum number of pieces for total length i
```

We start with the only certainly correct state, `dp[0] = 0`.

Whenever we extend a reachable state by one allowed cut, we create another valid ribbon decomposition. Since every transition adds exactly one piece, taking the maximum preserves the best possible decomposition for every length.

Every valid cutting sequence corresponds to some chain of transitions in the DP. Since all such transitions are explored, the optimal answer for `n` is guaranteed to be found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b, c = map(int, input().split())

    dp = [-1] * (n + 1)
    dp[0] = 0

    cuts = [a, b, c]

    for i in range(n + 1):
        if dp[i] == -1:
            continue

        for x in cuts:
            if i + x <= n:
                dp[i + x] = max(dp[i + x], dp[i] + 1)

    print(dp[n])

solve()
```

The DP array is initialized with `-1` so unreachable states are clearly separated from valid ones. This avoids accidentally building transitions from impossible lengths.

The base case `dp[0] = 0` represents an empty ribbon before any cuts are made.

The outer loop processes every reachable ribbon length. The inner loop attempts all three allowed cuts. If adding a cut stays within bounds, we update the destination state with the best piece count seen so far.

A subtle implementation detail is skipping states where `dp[i] == -1`. Without this check, impossible states would incorrectly generate transitions.

Another detail is using `max`. Different decompositions can reach the same total length, and we must keep the one producing the most pieces.

## Worked Examples

### Example 1

Input:

```
5 5 3 2
```

| Current `i` | `dp[i]` | Transition | Updated State |
| --- | --- | --- | --- |
| 0 | 0 | +5 | dp[5] = 1 |
| 0 | 0 | +3 | dp[3] = 1 |
| 0 | 0 | +2 | dp[2] = 1 |
| 2 | 1 | +3 | dp[5] = 2 |
| 3 | 1 | +2 | dp[5] = 2 |

Final value:

```
dp[5] = 2
```

The trace shows why maximizing is necessary. Length `5` is first reached directly with one piece, then improved later using `3 + 2`.

### Example 2

Input:

```
8 5 3 2
```

| Current `i` | `dp[i]` | Transition | Updated State |
| --- | --- | --- | --- |
| 0 | 0 | +5 | dp[5] = 1 |
| 0 | 0 | +3 | dp[3] = 1 |
| 0 | 0 | +2 | dp[2] = 1 |
| 2 | 1 | +2 | dp[4] = 2 |
| 4 | 2 | +2 | dp[6] = 3 |
| 6 | 3 | +2 | dp[8] = 4 |

Final value:

```
dp[8] = 4
```

This example demonstrates why greedy strategies fail. Using the largest piece first gives only two pieces, while repeated smaller cuts produce four.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each length processes exactly three transitions |
| Space | O(n) | The DP array stores one value per ribbon length |

With `n ≤ 4000`, the algorithm performs only about `3 * 4000` transitions, which is trivial within the time limit. Memory usage is also very small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, a, b, c = map(int, input().split())

    dp = [-1] * (n + 1)
    dp[0] = 0

    for i in range(n + 1):
        if dp[i] == -1:
            continue

        for x in (a, b, c):
            if i + x <= n:
                dp[i + x] = max(dp[i + x], dp[i] + 1)

    print(dp[n])

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("5 5 3 2\n") == "2", "sample 1"

# minimum-size valid input
assert run("1 1 1 1\n") == "1", "minimum case"

# all lengths equal
assert run("9 3 3 3\n") == "3", "all equal lengths"

# greedy would fail here
assert run("8 5 3 2\n") == "4", "many small cuts are optimal"

# boundary-style combination
assert run("7 5 2 5\n") == "2", "mixed reachable states"

# larger input
assert run("4000 1 2 3\n") == "4000", "maximum n with unit cuts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1` | Minimum valid input |
| `9 3 3 3` | `3` | Duplicate cut lengths |
| `8 5 3 2` | `4` | Greedy approaches fail |
| `7 5 2 5` | `2` | Impossible intermediate states handled correctly |
| `4000 1 2 3` | `4000` | Maximum boundary size |

## Edge Cases

Consider this input:

```
7 5 2 5
```

The DP starts with:

```
dp[0] = 0
```

From length `0`, we can reach lengths `5` and `2`.

```
dp[5] = 1
dp[2] = 1
```

From length `2`, adding another `5` reaches `7`:

```
dp[7] = 2
```

Impossible states like `1`, `3`, and `4` remain `-1`, so no invalid transitions are generated from them.

Now consider equal cut sizes:

```
9 3 3 3
```

The algorithm still works normally because each transition is treated independently. The updates become:

```
dp[3] = 1
dp[6] = 2
dp[9] = 3
```

Duplicate values do not require special handling.

Finally, consider a case where greedy fails:

```
8 5 3 2
```

A greedy strategy choosing `5` first produces only:

```
5 + 3 = 8
```

with two pieces.

The DP explores all reachable decompositions, including repeated `2` cuts:

```
2 + 2 + 2 + 2 = 8
```

which correctly gives four pieces.
