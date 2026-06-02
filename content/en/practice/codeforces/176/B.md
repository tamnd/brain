---
title: "CF 176B - Word Cut"
description: "Each operation chooses a non-empty prefix and a non-empty suffix of the current word and swaps their order. If the current word is written as xy, where both x and y are non-empty, the operation transforms it into yx. A useful way to view this operation is as a cyclic rotation."
date: "2026-06-02T17:10:11+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 1700
weight: 176
solve_time_s: 128
verified: true
draft: false
---

[CF 176B - Word Cut](https://codeforces.com/problemset/problem/176/B)

**Rating:** 1700  
**Tags:** dp  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Each operation chooses a non-empty prefix and a non-empty suffix of the current word and swaps their order. If the current word is written as `xy`, where both `x` and `y` are non-empty, the operation transforms it into `yx`.

A useful way to view this operation is as a cyclic rotation. If the word length is `n` and we split after position `p`, the suffix of length `n-p` moves to the front. Every split corresponds to exactly one non-trivial rotation, and every non-trivial rotation corresponds to exactly one split.

The words `start` and `end` have equal length `n`, where `2 ≤ n ≤ 1000`. We must count how many sequences of exactly `k` split operations transform `start` into `end`. Different split positions produce different operations, so two sequences are considered different if they choose different split points at some step.

The length of the word is at most 1000, but `k` can reach `10^5`. Any algorithm that explicitly tracks all possible operation sequences is hopeless. Even keeping a DP state for every rotation and every step would require about `1000 × 100000 = 10^8` transitions, which is too much.

The crucial observation is that every operation preserves the cyclic order of characters. Starting from a word, we can only reach its rotations. If `end` is not a rotation of `start`, the answer is immediately zero.

Several edge cases are easy to miss.

Consider:

```
ab
ab
0
```

The answer is `1`. We already start at the target and perform no operations. A solution that assumes at least one operation exists would incorrectly return `0`.

Consider:

```
aaaa
aaaa
1
```

Every split produces the same visible string `"aaaa"`, but the operations are still different because they use different split positions. There are `3` valid one-step sequences. Treating states as strings without counting distinct splits would undercount.

Consider:

```
abcd
bcda
1
```

There is exactly one valid split. Rotating left by one position corresponds to splitting after the first character. A solution that counts occurrences of the target rotation rather than actual operation paths may overcount.

## Approaches

The brute-force idea is straightforward. At every step, try all `n-1` possible split positions and recursively generate the resulting word. After exactly `k` operations, check whether the final word equals `end`.

This is correct because it explores every legal sequence of operations. Unfortunately, the branching factor is `n-1`, so the number of explored states is roughly `(n-1)^k`. Even for tiny values of `k`, this becomes enormous.

The next idea is to observe what a split operation really does. Splitting after position `p` rotates the string by `n-p` positions. Repeated splits never change the cyclic order of characters. Every reachable word is simply a rotation of `start`.

Suppose the length is `n`. There are at most `n` different rotation states. We could build a graph whose vertices are rotations and whose edges correspond to choosing one of the `n-1` non-trivial rotations. From any rotation, every other rotation is reachable in exactly one move, while staying in the same rotation is possible only through rotations that happen to produce the same string.

The key simplification comes from grouping rotations into only two categories:

The first category contains rotations equal to `end`.

The second category contains rotations not equal to `end`.

Let `cnt` be the number of rotations of `start` that equal `end`.

Then every rotation belongs to one of two classes, and transitions depend only on the class, not on the specific rotation. This turns the problem into a two-state DP that can be processed for up to `10^5` steps.

To use this DP, we must know whether rotation `0` of `start` is already equal to `end`, and how many total rotations equal `end`. Both quantities can be obtained by searching for occurrences of `end` inside `(start + start)[:-1]`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-1)^k) | O(k) | Too slow |
| Optimal | O(n + k) | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Count target rotations

Let

```
T = start + start
```

Every rotation of `start` corresponds to a starting position in `T`.

Search for all occurrences of `end` in `T[:-1]`. The number of occurrences is exactly the number of rotations of `start` equal to `end`.

Call this value `cnt`.

If `cnt = 0`, then `end` is not a rotation of `start`, and the answer is `0`.

### 2. Determine the initial state

Let

```
good0 = 1 if start == end else 0
```

We define two DP states.

`good[i]` is the number of ways to be at a rotation equal to `end` after `i` operations.

`bad[i]` is the number of ways to be at a rotation not equal to `end` after `i` operations.

Initially:

```
good = good0
bad = 1 - good0
```

There is exactly one starting rotation.

### 3. Derive transition counts

Suppose we are currently in a good rotation.

There are `n-1` possible split positions.

Among all rotations equal to `end`, one of them is the current rotation itself. Since every operation must be non-trivial, we cannot stay where we are.

So the number of transitions from a good state to another good state is:

```
cnt - 1
```

The number of transitions from a good state to a bad state is:

```
n - cnt
```

Now suppose we are in a bad rotation.

Among the `cnt` good rotations, all are reachable in one move.

For bad destinations, one rotation is the current state itself and cannot be chosen. Thus:

```
good transitions = cnt
bad transitions = n - cnt - 1
```

### 4. Update the DP

For each step:

```
new_good =
    good * (cnt - 1)
    + bad * cnt

new_bad =
    good * (n - cnt)
    + bad * (n - cnt - 1)
```

All computations are performed modulo `10^9+7`.

### 5. Repeat for k operations

Apply the transition `k` times.

The answer is the final value of `good`.

### Why it works

Every state of the original problem is a rotation of `start`. The only information relevant to the final goal is whether that rotation equals `end`.

Let `cnt` be the number of rotations representing `end`. From any rotation, choosing a split is equivalent to choosing any other rotation index. The number of outgoing edges to good states and bad states depends only on whether the current state is good or bad. It does not depend on the specific rotation.

Because all states inside the same category have identical transition behavior, aggregating them into two DP states preserves the exact number of paths. The recurrence counts every valid sequence of split positions once, and only once. After processing exactly `k` operations, `good` equals the number of operation sequences ending at a rotation equal to `end`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def kmp_count(text, pattern):
    m = len(pattern)

    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    cnt = 0
    j = 0
    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == m:
            cnt += 1
            j = pi[j - 1]

    return cnt

def solve():
    start = input().strip()
    end = input().strip()
    k = int(input())

    n = len(start)

    cnt = kmp_count((start + start)[:-1], end)

    if cnt == 0:
        print(0)
        return

    good = 1 if start == end else 0
    bad = 1 - good

    for _ in range(k):
        new_good = (good * (cnt - 1) + bad * cnt) % MOD
        new_bad = (good * (n - cnt) + bad * (n - cnt - 1)) % MOD

        good = new_good
        bad = new_bad

    print(good)

if __name__ == "__main__":
    solve()
```

The first part computes `cnt`, the number of rotations of `start` equal to `end`. Using KMP keeps this step linear in the string length.

The expression `(start + start)[:-1]` is important. Without removing the final character, the original rotation would appear twice, causing one extra match.

The DP stores only two values. `good` counts ways to end at a target rotation, while `bad` counts ways to end elsewhere. The transition coefficients come directly from counting how many split operations lead into each category.

A subtle point is the term `cnt - 1` in the good-to-good transition. One of the good rotations is the current rotation itself, but a split operation must be non-empty on both sides, so staying at the same rotation is not allowed as an operation. Forgetting this subtraction is the most common mistake in this problem.

## Worked Examples

### Example 1

Input:

```
ab
ab
2
```

Here `n = 2`.

The rotations are:

```
ab
ba
```

Only one rotation equals `end`, so `cnt = 1`.

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

Answer:

```
1
```

This trace shows that the only possible split alternates between the two rotations.

### Example 2

Input:

```
ababab
ababab
1
```

Rotations equal to `"ababab"` occur at positions `0`, `2`, and `4`.

Thus:

```
cnt = 3
n = 6
```

Initial state:

| Step | good | bad |
| --- | --- | --- |
| 0 | 1 | 0 |

After one operation:

| Step | good | bad |
| --- | --- | --- |
| 1 | 2 | 3 |

Answer:

```
2
```

The two valid operations are exactly the two non-trivial rotations that still produce the same visible string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | KMP runs in O(n), DP performs k iterations |
| Space | O(n) | KMP prefix table stores O(n) values |

With `n ≤ 1000` and `k ≤ 100000`, roughly one hundred thousand DP updates are trivial. The algorithm comfortably fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def kmp_count(text, pattern):
        m = len(pattern)

        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j

        cnt = 0
        j = 0
        for ch in text:
            while j > 0 and ch != pattern[j]:
                j = pi[j - 1]
            if ch == pattern[j]:
                j += 1
            if j == m:
                cnt += 1
                j = pi[j - 1]

        return cnt

    start = input().strip()
    end = input().strip()
    k = int(input())

    n = len(start)
    cnt = kmp_count((start + start)[:-1], end)

    if cnt == 0:
        return "0"

    good = 1 if start == end else 0
    bad = 1 - good

    for _ in range(k):
        ng = (good * (cnt - 1) + bad * cnt) % MOD
        nb = (good * (n - cnt) + bad * (n - cnt - 1)) % MOD
        good, bad = ng, nb

    return str(good)

# provided sample
assert run("ab\nab\n2\n") == "1", "sample 1"

# custom cases
assert run("ab\nab\n0\n") == "1", "zero operations"
assert run("ab\nba\n1\n") == "1", "single valid rotation"
assert run("abcd\nabcd\n1\n") == "0", "cannot stay in place"
assert run("aaaa\naaaa\n1\n") == "3", "all rotations equal"
assert run("abcd\nacbd\n5\n") == "0", "target not a rotation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ab ab 0` | `1` | Base case with no operations |
| `ab ba 1` | `1` | Single non-trivial rotation |
| `abcd abcd 1` | `0` | Staying in the same rotation is forbidden |
| `aaaa aaaa 1` | `3` | Multiple rotations producing identical strings |
| `abcd acbd 5` | `0` | Target is not a rotation of start |

## Edge Cases

Consider:

```
ab
ab
0
```

We have `cnt = 1`. The initial state is `good = 1`, `bad = 0`. Since `k = 0`, the DP performs no transitions. The answer remains `1`. This correctly counts the empty operation sequence.

Consider:

```
aaaa
aaaa
1
```

All four rotations are equal to `"aaaa"`, so `cnt = 4`. Initially `good = 1`.

After one step:

```
good = 1 * (4 - 1) = 3
```

There are exactly three legal split positions, and all of them produce the target string. The algorithm counts operations, not distinct resulting strings.

Consider:

```
abcd
abcd
1
```

Here `cnt = 1`. The recurrence gives:

```
good = 1 * (1 - 1) = 0
```

The only good rotation is the current one, but a split operation cannot leave the rotation unchanged. The algorithm correctly excludes this impossible transition.

Consider:

```
abcd
acbd
3
```

`acbd` is not a rotation of `abcd`, so KMP finds `cnt = 0`. The algorithm immediately returns `0`, reflecting the fact that split operations preserve cyclic order and can never create this arrangement.
