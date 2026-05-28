---
title: "CF 176B - Word Cut"
description: "We start with a string start and want to reach another string end after exactly k operations. One operation chooses a non-empty prefix and a non-empty suffix. If the current word is written as xy, the operation transforms it into yx."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 1700
weight: 176
solve_time_s: 102
verified: true
draft: false
---

[CF 176B - Word Cut](https://codeforces.com/problemset/problem/176/B)

**Rating:** 1700  
**Tags:** dp  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string `start` and want to reach another string `end` after exactly `k` operations.

One operation chooses a non-empty prefix and a non-empty suffix. If the current word is written as `xy`, the operation transforms it into `yx`. Since both parts must be non-empty, every operation is equivalent to rotating the string by some positive amount smaller than its length.

For example:

```
abcdef
split after index 2

ab | cdef  ->  cdefab
```

The crucial observation is that every reachable string is just a cyclic rotation of the original string. No operation changes the relative order of characters, it only changes the starting position.

The input size changes the nature of the problem completely. The string length is at most 1000, which is small enough for quadratic preprocessing over rotations. The dangerous constraint is `k ≤ 100000`. Any solution that simulates all sequences of operations explodes immediately because each step has up to `n - 1` choices.

If `n = 1000` and `k = 100000`, then a brute-force recursion would try roughly:

```
999^100000
```

possible sequences, which is impossible.

The actual challenge is counting operation sequences, not merely checking reachability.

There are several easy-to-miss edge cases.

Suppose:

```
start = "ab"
end = "ab"
k = 1
```

The answer is `0`.

There is only one possible operation:

```
ab -> ba
```

A careless DP that allows "do nothing" transitions would incorrectly produce `1`.

Another tricky case is when multiple rotations produce the same string.

```
start = "abab"
end = "abab"
```

The string `"abab"` appears under two different rotations:

```
rotation 0 -> abab
rotation 2 -> abab
```

These are different states because operations distinguish positions, not final text alone. Ignoring this causes undercounting.

One more subtle situation appears when `start == end` and `k = 0`.

```
abc
abc
0
```

The answer is `1`, because using zero operations is valid.

But:

```
abc
bca
0
```

must produce `0`.

The DP initialization has to encode this correctly.

## Approaches

The brute-force idea is straightforward. At each operation we choose one of the `n - 1` split points and generate the next rotation. After exactly `k` steps we check whether the final string equals `end`.

This is correct because it explicitly enumerates every valid sequence of operations. The problem is the branching factor. Even for `n = 1000` and a tiny `k = 20`, the search space becomes:

```
999^20
```

which is already astronomically large.

We need to exploit structure.

Every operation is a cyclic rotation. More specifically, if we index rotations by how far the string is shifted, then each operation moves from one rotation state to another rotation state.

The next observation is the key simplification:

From any rotation, every other rotation is reachable in exactly one operation, except itself.

Why?

Assume the current rotation is shift `i`. Splitting after `t` characters rotates the string additionally by `t`. Since `t` can be any value from `1` to `n - 1`, we can move to any different rotation in one step, but never stay in place.

This means the graph of states is extremely simple:

```
every node connects to all other nodes
no self-loops
```

Now the actual string contents barely matter. We only care whether the current rotation equals the target rotation or not.

Let:

```
good = number of ways to be at a target rotation
bad  = number of ways to be at a non-target rotation
```

Transitions become simple counting formulas.

If there are `cnt` rotations equal to `end`, then:

From a good state:

- `cnt - 1` moves stay good
- `n - cnt` moves become bad

From a bad state:

- `cnt` moves become good
- `n - cnt - 1` moves stay bad

Now we only need a 2-state DP for `k` steps.

The remaining task is finding how many rotations of `start` equal `end`. Since `n ≤ 1000`, checking all rotations directly is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-1)^k) | O(k) | Too slow |
| Optimal | O(n^2 + k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Generate all cyclic rotations of `start` and count how many of them equal `end`.

Each rotation corresponds to one state in the implicit graph. Multiple rotations may produce the same visible string when the word is periodic.
2. Let `cnt` be the number of rotations equal to `end`.

These are the "good" states. The remaining `n - cnt` states are "bad".
3. Initialize the DP.

If the original `start` already equals `end`, then rotation `0` is good initially.

Otherwise we begin in a bad state.
4. Maintain two values:

```
good = ways to be in a good state
bad  = ways to be in a bad state
```
5. For each operation, compute the next values.

From a good state:

- there are `cnt - 1` good destinations
- there are `n - cnt` bad destinations

From a bad state:

- there are `cnt` good destinations
- there are `n - cnt - 1` bad destinations

So:

```
new_good = good * (cnt - 1) + bad * cnt
new_bad  = good * (n - cnt) + bad * (n - cnt - 1)
```
6. Apply modulo `1e9 + 7` after every update.
7. After exactly `k` steps, output `good`.

### Why it works

The invariant is:

```
good = number of operation sequences that end in any rotation equal to end
bad  = number of operation sequences that end in any other rotation
```

Every operation moves from one rotation to any different rotation exactly once. Because transitions depend only on whether a state is good or bad, not on its exact index, all states inside the same category are symmetric.

The recurrence counts every legal operation exactly once and never counts an illegal self-transition. Since the initialization matches the starting rotation and every step preserves the invariant, the final `good` value is exactly the number of valid operation sequences of length `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

start = input().strip()
end = input().strip()
k = int(input())

n = len(start)

cnt = 0

for shift in range(n):
    rotated = start[shift:] + start[:shift]
    if rotated == end:
        cnt += 1

if start == end:
    good = 1
    bad = 0
else:
    good = 0
    bad = 1

for _ in range(k):
    new_good = (good * (cnt - 1) + bad * cnt) % MOD
    new_bad = (good * (n - cnt) + bad * (n - cnt - 1)) % MOD

    good = new_good
    bad = new_bad

print(good % MOD)
```

The first section counts how many rotations of `start` equal `end`. This is the only place where actual string comparisons matter.

The DP does not track exact rotations. It only tracks whether the current rotation belongs to the target set. This compression works because every state has identical outgoing structure.

The initialization is subtle. If `start == end`, then we begin inside the good category. Otherwise we begin inside the bad category. This handles the `k = 0` case naturally.

The recurrence carefully excludes self-loops. From a good state we can move to only `cnt - 1` other good states, not `cnt`. Forgetting this is the most common bug.

All arithmetic uses modulo `10^9 + 7` because the number of sequences grows exponentially.

## Worked Examples

### Example 1

Input:

```
ab
ab
2
```

There are two rotations:

```
0 -> ab
1 -> ba
```

Only one rotation matches `end`, so:

```
cnt = 1
```

Initial state:

```
good = 1
bad = 0
```

| Step | good | bad |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 0 | 1 |
| 2 | 1 | 0 |

Final answer:

```
1
```

This trace confirms that self-transitions are forbidden. After one move we are forced into `"ba"`.

### Example 2

Input:

```
ababab
ababab
1
```

Rotations equal to `"ababab"`:

```
shift 0
shift 2
shift 4
```

So:

```
cnt = 3
n = 6
```

Initial state:

```
good = 1
bad = 0
```

| Step | good | bad |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 2 | 3 |

Answer:

```
2
```

The two valid operations are rotating by 2 and by 4.

This example demonstrates why counting matching strings instead of matching rotation states is wrong. There are three distinct good rotations even though the visible text is identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 + k) | O(n^2) for checking all rotations, O(k) for DP |
| Space | O(1) | Only a few integer variables are stored |

With `n ≤ 1000`, the rotation check performs at most one million character operations, which is easily fast enough. The DP performs `100000` constant-time updates, also well within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline

    start = input().strip()
    end = input().strip()
    k = int(input())

    n = len(start)

    cnt = 0

    for shift in range(n):
        rotated = start[shift:] + start[:shift]
        if rotated == end:
            cnt += 1

    if start == end:
        good = 1
        bad = 0
    else:
        good = 0
        bad = 1

    for _ in range(k):
        new_good = (good * (cnt - 1) + bad * cnt) % MOD
        new_bad = (good * (n - cnt) + bad * (n - cnt - 1)) % MOD

        good = new_good
        bad = new_bad

    print(good)

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
assert run("ab\nab\n2\n") == "1", "sample 1"

# periodic string, multiple matching rotations
assert run("ababab\nababab\n1\n") == "2", "periodic rotations"

# k = 0, already equal
assert run("abc\nabc\n0\n") == "1", "zero operations valid"

# k = 0, not equal
assert run("abc\nbca\n0\n") == "0", "cannot transform without operations"

# minimum length, impossible parity
assert run("ab\nab\n1\n") == "0", "must move away after one operation"

# unique rotation target
assert run("abcd\nbcda\n1\n") == "1", "single valid split"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ababab / ababab / 1` | `2` | Multiple good rotations from periodicity |
| `abc / abc / 0` | `1` | Correct zero-step initialization |
| `abc / bca / 0` | `0` | No transformation without operations |
| `ab / ab / 1` | `0` | No self-loops allowed |
| `abcd / bcda / 1` | `1` | Single exact rotation |

## Edge Cases

Consider:

```
ab
ab
1
```

The only legal move is:

```
ab -> ba
```

The algorithm computes:

```
cnt = 1
good = 1
bad = 0
```

After one step:

```
new_good = 1 * (1 - 1) + 0 * 1 = 0
```

So the answer becomes `0`, correctly forbidding staying in place.

Now examine a periodic string:

```
abab
abab
1
```

Matching rotations are:

```
shift 0
shift 2
```

So:

```
cnt = 2
```

Initialization:

```
good = 1
bad = 0
```

Transition:

```
new_good = 1 * (2 - 1) = 1
```

Exactly one operation keeps us in a good state:

```
abab -> abab
```

using rotation by 2.

Finally, consider:

```
abc
cab
0
```

We begin in a bad state because the original string does not equal `end`.

```
good = 0
bad = 1
```

Since `k = 0`, the loop never runs and the answer remains `0`.

This confirms that the initialization alone correctly handles zero operations.
