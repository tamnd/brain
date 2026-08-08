---
title: "CF 102440A - \u0414\u043e\u043c\u0430\u0448\u043d\u044f\u044f \u0430\u043a\u0443\u043b\u0430"
description: "We have a sequence of food units, where each position stores a food type. The shark can eat exactly k units in one feeding, and all those units must have the same type. A chosen interval is successful if all food inside it can be partitioned into groups of exactly k equal types."
date: "2026-08-09T00:51:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "A"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 588
verified: true
draft: false
---

[CF 102440A - \u0414\u043e\u043c\u0430\u0448\u043d\u044f\u044f \u0430\u043a\u0443\u043b\u0430](https://codeforces.com/problemset/problem/102440/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of food units, where each position stores a food type. The shark can eat exactly `k` units in one feeding, and all those units must have the same type. A chosen interval is successful if all food inside it can be partitioned into groups of exactly `k` equal types.

For a fixed interval, the order of its elements does not matter. What matters is the number of occurrences of every food type. The interval is valid exactly when every such count is divisible by `k`.

The task is to count all contiguous subarrays satisfying that condition. With `n` up to `2 * 10^5`, there can be

[
\frac{n(n+1)}2 = 20,000,100,000
]

different intervals in the largest case. A quadratic algorithm would already have to process around twenty billion intervals, which is far beyond what a normal contest time limit allows. We need a method that processes each array position only a constant number of times, giving roughly linear complexity.

Several boundary cases are easy to mishandle. If `k = 1`, every interval is valid because every individual food unit can be eaten separately. For example,

```
1 1
1
```

has answer `1`, while an implementation that only looks for groups of length greater than one could incorrectly return zero.

If `k > n`, no non-empty interval can contain `k` copies of any type, so no interval can be valid. For example,

```
3 4
1 1 1
```

has answer `0`. A solution that checks only whether the total length is divisible by `k` might accidentally count the empty prefix or mishandle short intervals.

Repeated occurrences of the same type also have to be counted modulo `k`, rather than merely checking whether all types occur the same number of times. For example,

```
4 2
1 1 1 1
```

has answer `3 + 1 = 4`, because the three intervals of length two and the whole interval of length four are valid. An approach that only recognizes the first complete group of `k` units would miss the longer interval.

## Approaches

A direct solution can enumerate every interval and maintain the frequency of each food type while extending its right endpoint. For a fixed left endpoint, add `a[r]` one position at a time and keep a counter telling how many food types currently have a frequency that is not divisible by `k`. When that counter becomes zero, the current interval is valid. This correctly checks every interval without repeatedly scanning all `n` types.

The problem is the number of intervals. There are `n(n+1)/2` of them, which reaches `20,000,100,000` when `n = 200000`. Even though each interval is processed in constant time in this optimized brute-force version, quadratic time is still too slow.

The key observation is that divisibility depends only on the frequency of every type modulo `k`. Consider prefixes of the array. For each prefix, define its state as the vector

[
(c_1 \bmod k,\ c_2 \bmod k,\ \ldots,\ c_n \bmod k),
]

where `c_x` is the number of occurrences of type `x` in that prefix.

Suppose prefixes ending at positions `l - 1` and `r` have exactly the same state. Subtracting their frequency vectors tells us that every type occurs a multiple of `k` times in the interval `[l, r]`. Hence that interval is valid.

The converse is also true. If `[l, r]` is valid, every type contributes a multiple of `k`, so the two prefix states are equal modulo `k`.

Thus the original problem becomes a standard prefix-state counting problem: scan the array, compute the state of every prefix, and count how many pairs of equal states exist. If a state has appeared `f` times before, the current prefix creates exactly `f` new valid intervals.

The obstacle is that the complete state has up to `n` coordinates, so storing it as a tuple would require `O(n)` work per position. Instead, we maintain a randomized 128-bit fingerprint of the state. Give every food type `x` a random 128-bit weight `w[x]`. If its current residue is `c[x]`, its contribution to the fingerprint is `c[x] * w[x]`. When one occurrence of type `x` is added, its residue increases by one modulo `k`, so the total fingerprint changes by a known amount. We can update it in constant time.

The fingerprint is probabilistic rather than mathematically collision-free, but a 128-bit random value makes an accidental collision negligibly unlikely. This is the same idea as randomized hashing of a large vector, except here the vector changes one coordinate at a time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Assign every food type `x` a random 128-bit weight `w[x]`. We will represent the vector of all frequency residues by the fingerprint

[
H = \sum_x c_x w_x \pmod {2^{128}},
]

where `c_x` is the current frequency of type `x` modulo `k`.

We do not need to store the whole vector. The fingerprint is enough for comparing prefix states with overwhelming probability.
2. Initialize every residue to zero, so the empty prefix has fingerprint `0`. Put this fingerprint into a frequency dictionary with count `1`.

The initial occurrence represents prefix position `0`. If a later prefix has the same state, the interval between these two prefixes starts at position `1`.
3. Scan the array from left to right. For the current food type `x`, increase its residue modulo `k`.

If its old residue is less than `k - 1`, the residue increases by one, so add `w[x]` to the fingerprint. If the old residue is `k - 1`, the new residue becomes zero, so the contribution changes from `(k - 1)w[x]` to zero. In that case subtract `(k - 1)w[x]`.
4. After updating the fingerprint, look it up in the dictionary. If it has already appeared `f` times, add `f` to the answer.

Every previous prefix with the same state forms a valid interval ending at the current position. We count all of those intervals at once.
5. Increase the frequency of the current fingerprint in the dictionary. Continue until every position has been processed.
6. Return the accumulated answer.

### Why it works

For every prefix, the maintained residue for a food type is exactly its occurrence count modulo `k`. Consider two prefixes, one ending before an interval and one ending at its right endpoint. Their states are equal exactly when every food type has the same residue in both prefixes. Subtracting the two prefix counts means every food type occurs a multiple of `k` times inside the interval. Such an interval can be divided into groups of exactly `k` equal food units, so the shark can eat it completely.

Conversely, if an interval can be eaten completely, each type occurs a multiple of `k` times, so removing that interval from the later prefix does not change any residue. The two prefix states are equal. Thus valid intervals correspond exactly to equal prefix states.

The dictionary counts every pair of equal states once, so every valid interval is counted and no invalid interval is counted. The only approximation is the randomized fingerprint: two different states could theoretically receive the same 128-bit value, but the probability is negligible.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

MASK = (1 << 128) - 1

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    # A fresh random weight for every food type.
    rng = random.Random()
    weight = [0] + [rng.getrandbits(128) for _ in range(n)]

    # residue[x] = current frequency of type x modulo k.
    residue = [0] * (n + 1)

    # Frequency of every prefix fingerprint.
    seen = {0: 1}

    state = 0
    answer = 0

    for x in a:
        r = residue[x]

        if r == k - 1:
            # (k - 1) * w[x] -> 0
            state = (state - (k - 1) * weight[x]) & MASK
            residue[x] = 0
        else:
            state = (state + weight[x]) & MASK
            residue[x] = r + 1

        answer += seen.get(state, 0)
        seen[state] = seen.get(state, 0) + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The `residue` array stores exactly the information that changes when a new food unit is processed. For a type whose residue is `r`, adding one unit changes it to `r + 1` unless it reaches `k`, in which case it wraps back to zero.

The fingerprint is maintained consistently with that residue. For the usual transition, the contribution changes by `+weight[x]`. On the wraparound transition, the old contribution `(k - 1) * weight[x]` disappears entirely, so we subtract that value.

The `& MASK` operation keeps the fingerprint modulo `2^128`. Python integers can grow arbitrarily large, so without this mask the state would accumulate unnecessarily large values. The mask also gives us a fixed 128-bit fingerprint.

The dictionary starts with `{0: 1}` because the empty prefix is a real prefix state. Forgetting it would lose every valid interval beginning at position `1`. The answer is updated before inserting the current state, so only earlier prefixes are used to form intervals ending at the current position.

Python integers handle the final answer safely. The maximum number of intervals is about `2 * 10^10`, which is well within Python's integer range.

## Worked Examples

### Sample 1

The input is

```
6 2
1 2 1 2 1 2
```

Each type has to occur an even number of times. We track the residues modulo two. For readability, the table shows the exact residue vector rather than its random fingerprint.

| Position | Added type | State after position | Number of previous equal states | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | `(0, 0)` | 1 | 0 |
| 1 | 1 | `(1, 0)` | 0 | 0 |
| 2 | 2 | `(1, 1)` | 0 | 0 |
| 3 | 1 | `(0, 1)` | 0 | 0 |
| 4 | 2 | `(0, 0)` | 1 | 1 |
| 5 | 1 | `(1, 0)` | 1 | 2 |
| 6 | 2 | `(1, 1)` | 1 | 3 |

At position four, the state returns to `(0, 0)`, so `[1, 4]` is valid. At positions five and six, the states `(1, 0)` and `(1, 1)` repeat their earlier versions, producing two more valid intervals. The final answer is `3`.

The trace demonstrates the central invariant: a repeated prefix residue state is exactly a valid interval.

### Sample 2

The input is

```
6 6
1 1 1 1 1 1
```

There is only one food type, and its count must be divisible by six.

| Position | Added type | State after position | Number of previous equal states | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | `(0)` | 1 | 0 |
| 1 | 1 | `(1)` | 0 | 0 |
| 2 | 1 | `(2)` | 0 | 0 |
| 3 | 1 | `(3)` | 0 | 0 |
| 4 | 1 | `(4)` | 0 | 0 |
| 5 | 1 | `(5)` | 0 | 0 |
| 6 | 1 | `(0)` | 1 | 1 |

Only the final prefix returns to residue zero. It matches the empty prefix, so the whole array is the only valid interval.

This example exercises the wraparound case `k - 1 -> 0`. Handling that transition as simply `state += weight[x]` would be incorrect because the contribution of that type has to disappear completely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) expected | Each array element causes O(1) residue and hash updates, followed by expected O(1) dictionary operations. |
| Space | O(n) | The residue array, random weights, and at most `n + 1` prefix states are stored. |

With `n <= 200000`, the algorithm performs only a constant amount of work per food unit and stores a linear number of integers. This is comfortably within the intended scale of the problem, while the quadratic approach would have to process up to about twenty billion intervals.

## Test Cases

```python
import sys
import io
import random

MASK = (1 << 128) - 1

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    rng = random.Random()
    weight = [0] + [rng.getrandbits(128) for _ in range(n)]
    residue = [0] * (n + 1)

    seen = {0: 1}
    state = 0
    answer = 0

    for x in a:
        r = residue[x]

        if r == k - 1:
            state = (state - (k - 1) * weight[x]) & MASK
            residue[x] = 0
        else:
            state = (state + weight[x]) & MASK
            residue[x] = r + 1

        answer += seen.get(state, 0)
        seen[state] = seen.get(state, 0) + 1

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("6 2\n1 2 1 2 1 2\n") == "3", "sample 1"
assert run("6 6\n1 1 1 1 1 1\n") == "1", "sample 2"
assert run("9 3\n1 2 3 1 2 3 1 2 3\n") == "1", "sample 3"

# Minimum-size input
assert run("1 1\n1\n") == "1", "minimum size"

# All intervals are valid when k = 1:
# n * (n + 1) / 2 = 6 * 7 / 2 = 21
assert run("6 1\n1 2 1 2 3 3\n") == "21", "k = 1"

# k > n, so no non-empty interval can contain k equal units
assert run("3 4\n1 1 1\n") == "0", "k greater than n"

# Catches the wraparound and prefix-boundary cases.
# Valid intervals are [1,2], [2,3], [3,4], [1,4].
assert run("4 2\n1 1 1 1\n") == "4", "multiple complete groups"

# Maximum-size all-equal case.
# Only the whole array has 200000 occurrences, divisible by k.
n = 200000
assert run(
    f"{n} {n}\n" + " ".join(["1"] * n) + "\n"
) == "1", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum input and `k = 1` boundary |
| `6 1 / 1 2 1 2 3 3` | `21` | Every interval is valid when `k = 1` |
| `3 4 / 1 1 1` | `0` | No interval can contain enough food when `k > n` |
| `4 2 / 1 1 1 1` | `4` | Multiple complete groups and modulo wraparound |
| `200000 200000 / 1 ... 1` | `1` | Maximum `n`, maximum `k`, and large answer-state processing |

## Edge Cases

When `k = 1`, every frequency is automatically zero modulo one. The prefix state never changes, so all `n + 1` prefixes have the same state. The dictionary consequently counts every pair of prefixes, giving `n(n+1)/2`. For `n = 6`, this is `21`, exactly as the corresponding test checks.

When `k > n`, no non-empty interval can contain `k` copies of any one type. In the input `3 4 / 1 1 1`, the residues progress from `0` to `1`, then `2`, then `3`, and never return to zero. The initial state is never repeated, so the answer remains `0`.

For repeated complete groups, consider `4 2 / 1 1 1 1`. The states are `0, 1, 0, 1, 0`. The state zero occurs at positions `0`, `2`, and `4`, producing three intervals, while state one occurs at positions `1` and `3`, producing one more. The answer is `3 + 1 = 4`.

The wraparound transition deserves special attention. If the current residue is `k - 1`, adding one occurrence makes it zero, not `k`. For `k = 2`, a type changes from residue `1` to residue `0`. The code subtracts `(k - 1) * weight[x]`, which is exactly the old contribution, so that type contributes nothing to the new state.

Finally, a valid interval may start at the first array position. That is why the empty prefix is inserted into `seen` before processing any elements. Without that initial state, an input such as `6 6 / 1 1 1 1 1 1` would fail to count the full array, even though its frequency is exactly divisible by `k`.
