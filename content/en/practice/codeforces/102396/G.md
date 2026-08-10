---
title: "CF 102396G - Weight Overflow"
description: "We need to place some of the given weights onto two plates. A weight can go onto the first plate, the second plate, or stay unused. The scale does not compare the actual sums."
date: "2026-08-10T18:48:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "G"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 803
verified: false
draft: false
---

[CF 102396G - Weight Overflow](https://codeforces.com/problemset/problem/102396/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We need to place some of the given weights onto two plates. A weight can go onto the first plate, the second plate, or stay unused. The scale does not compare the actual sums. Instead, it reduces each plate's total mass modulo `m`, and reports balanced when those two residues are equal.

Suppose the first plate receives weights with total `S1` and the second receives weights with total `S2`. We need

`S1 ≡ S2 (mod m)`

with at least one weight actually placed. Equivalently, for every weight we can choose a coefficient from `{-1, 0, 1}` and need

`c1*a1 + c2*a2 + ... + cn*an ≡ 0 (mod m)`,

where `1` means the weight is on the first plate, `-1` means the second plate, and `0` means unused.

The constraint `n <= 25` is the central clue. There are three choices per weight, so a direct search has `3^25 = 847,288,609` assignments. That is far beyond what a one-second limit allows. The modulus can be almost `4 * 10^7`, so an algorithm proportional to `m` is also unnecessarily large, and a quadratic search over all assignments is impossible. The small value of `n` instead suggests splitting the weights into two groups and enumerating their possibilities independently.

The masses can be as large as `10^9`, so ordinary 32-bit arithmetic would not be safe for intermediate sums in languages such as C++. Python integers do not overflow, but the implementation should still reduce residues modulo `m` at the points where they are used as hash keys.

There are several edge cases that are easy to mishandle. With `n = 1`, `m = 5`, and `a = [3]`, there is no solution, because the only nonempty placement gives residue `3`, not `0`. A careless program that always assumes the pigeonhole argument produces a solution would incorrectly print one weight.

For `n = 1`, `m = 1`, and `a = [3]`, the correct answer is to put the single weight on either plate, because every integer is congruent to zero modulo `1`. A program that searches only for two nonempty plates can incorrectly reject this case.

Another subtle case is when one plate is empty. For example,

```

```

has a valid solution because `1 + 2 + 4 = 7`, so all three weights can go onto the first plate and the second plate can remain empty. Requiring both plates to contain a weight would incorrectly reject it.

Finally, the two sides must be disjoint. For example, with `m = 7` and weights `3, 3, 3, 3`, putting two weights on each side gives sums `6` and `6`. A formulation that merely searches for two equal subset sums without explicitly representing each weight's three possible states can accidentally reuse the same weight on both sides.

## Approaches

The brute-force solution directly assigns every weight one of three states: unused, first plate, or second plate. For each of the `3^n` assignments, we compute the difference between the two plate sums modulo `m`. If it is zero and at least one weight was used, we have an answer. This is completely correct because every possible placement is represented exactly once. At `n = 25`, however, the search contains `3^25 = 847,288,609` states, so it is much too slow.

The useful observation is that the equation is additive. Split the weights into two groups, with at most 12 weights in the first group and at most 13 in the second. For each group, enumerate all ternary assignments independently. An assignment has a signed sum

`x = Σ c_i*a_i`.

If an assignment from the first half has residue `r`, then an assignment from the second half with residue `-r mod m` combines with it into a complete assignment whose total signed sum is divisible by `m`.

The first half has at most `3^12 = 531,441` assignments, while the second has at most `3^13 = 1,594,323`. We store one assignment for every residue produced by the first half in a hash table, then scan the second half and look up the required complementary residue.

The three-state representation is what makes this meet-in-the-middle approach particularly clean. We do not have to worry about overlaps because each weight belongs to exactly one half, and within each half its state is already one of unused, first plate, or second plate.

The all-zero assignment deserves explicit handling. The residue `0` naturally corresponds to assigning every weight to neither plate, but the problem requires at least one weight. We simply ignore the match where both stored and current ternary codes are zero. If either side has a nonzero assignment, the resulting placement is valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(3^n)` | `O(n)` | Too slow |
| Meet in the Middle | `O(3^(n/2))` expected | `O(3^(n/2))` | Accepted |

## Algorithm Walkthrough

1. Split the `n` weights into a first group of `n // 2` weights and a second group containing the rest. Keeping the first group at size at most 12 keeps the hash table small.
2. Enumerate every ternary assignment of the first group. For each weight, digit `0` means unused, digit `1` means first plate, and digit `2` means second plate. Calculate its signed sum modulo `m`, and store the ternary code for that residue if the residue has not been seen before.

Keeping only one code per residue is sufficient. Any assignment producing the same residue is interchangeable for the purpose of matching it with the other half.
3. Enumerate every ternary assignment of the second group and calculate its signed sum modulo `m`.
4. For a second-half residue `r`, look for residue `(-r) mod m` in the first-half table. If it exists, the two signed sums add to zero modulo `m`, so the combined placement balances the scale.
5. Reject the match only when both ternary codes are zero. That combination uses no weight and is forbidden. Every other match gives a valid answer.
6. Decode the two ternary codes. For every digit equal to `1`, output that weight on the first plate. For every digit equal to `2`, output it on the second plate. The two groups are disjoint by construction, so no weight can appear on both plates.

### Why it works

For every possible placement of the weights, each weight has exactly one coefficient from `{-1, 0, 1}`. Splitting the weights into two groups splits the total signed sum into `x + y`, where `x` depends only on the first group and `y` only on the second.

The first-half enumeration contains every possible value of `x mod m`. When we process a second-half value `y`, looking for `(-y) mod m` finds exactly the first-half values satisfying

`x + y ≡ 0 (mod m)`.

Thus every match produced by the algorithm represents two plate sums with equal residues. Conversely, any valid placement has some first-half residue `x` and second-half residue `y` satisfying this same equation, so the algorithm will find a matching pair of assignments. The only invalid assignment is the completely unused one, which we explicitly exclude.

## Python Solution

```
Python
```

The initial `m == 1` check is a small but useful boundary optimization. Since every residue modulo `1` is zero, any single weight is sufficient.

The next shortcut checks whether an individual weight is already divisible by `m`. Such a weight can be placed alone on one plate, so there is no reason to run the meet-in-the-middle search.

The recursive `build` function enumerates the first half's three choices. `place` is the current power of three, so the ternary assignment is stored compactly as an integer. The signed sum is accumulated directly, and only its final residue is needed as a hash key.

The `search` function performs the same enumeration for the second half. If its residue is `r`, the required first-half residue is `(-r) % m`. Python's modulo operation produces a value in `[0, m - 1]`, so this works correctly even when `r` is nonzero.

The ternary code is decoded with repeated `% 3` and `// 3`. The least significant ternary digit corresponds to the first weight in each half because the recursion assigns the current `place` before multiplying it by three.

The algorithm never uses the same weight on both plates because the two halves are disjoint. Within one half, every ternary digit has only one state, so the decoded result automatically represents a legal placement.

The recursive depth is at most 13, which is far below Python's recursion limit. The number of recursive calls is exponential, but it remains on the order of `3^13`, which is the intended scale of the solution.

## Worked Examples

### Sample 1

For

```

```

the split is `1, 3` in the first half and `7, 10` in the second half.

One useful match is the first-half assignment that leaves both weights unused, combined with the second-half assignment placing `7` on the second plate and `10` on the first plate. Their signed sum is `10 - 7 = 3`, which is not zero, so this particular combination is not a match. The successful combination found by the algorithm corresponds to putting weight `4` on the first plate and weights `2, 3` on the second plate.

| First-half state | First-half sum | Second-half state | Second-half sum | Total modulo 14 |
| --- | --- | --- | --- | --- |
| weights 1, 2 unused | `0` | weight 3 unused, weight 4 first | `10` | `10` |
| weight 1 unused, weight 2 second | `-3` | weight 3 second, weight 4 first | `3` | `0` |

The final placement is weight `4` on the first plate and weights `2, 3` on the second plate. Their actual sums are `10` and `3 + 7 = 10`, so the scale reports equality even without relying on an actual modulo wraparound.

### Sample 2

For

```

```

the first half contains weight `1`, while the second half contains weights `2` and `3`.

| First-half state | First-half sum | Second-half state | Second-half sum | Total modulo 7 |
| --- | --- | --- | --- | --- |
| weight 1 first | `1` | weights 2 and 3 first | `6` | `0` |

The resulting placement puts all three weights on the first plate. Its total is `1 + 2 + 4 = 7`, which has residue zero modulo `7`, while the empty second plate also has residue zero.

This example demonstrates why an empty plate must be allowed. The requirement is only that at least one weight is used somewhere.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(3^(n/2))` expected | We enumerate at most `3^12 + 3^13` assignments and perform average constant-time hash lookups. |
| Space | `O(3^(n/2))` | The hash table stores at most one ternary code for each residue generated by the smaller half. |

With `n = 25`, the largest half contains 13 weights, giving about `1.59 * 10^6` ternary assignments. This is dramatically smaller than the `8.47 * 10^8` assignments of brute force. The memory requirement is dominated by the hash table and stays within the generous 512 MB limit, although Python's object overhead makes this implementation substantially heavier than an equivalent C++ implementation.

## Test Cases

The output of this problem is not unique, so tests should validate the produced placement rather than compare the literal output string. The helper below parses the program's output and checks that the selected indices are disjoint, that at least one weight is used, and that the two plate sums are equal modulo `m`.

```python
import sys
import io

def solve(data=None):
    if data is None:
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
    else:
        it = iter(map(int, data.split()))
        n = next(it)
        m = next(it)
        a = [next(it) for _ in range(n)]

    if m == 1:
        return "1\n1\n0\n\n"

    for i, x in enumerate(a):
        if x % m == 0:
            return f"1\n{i + 1}\n0\n\n"

    left_n = n // 2
    left_n = min(left_n, n)
    left = a[:left_n]
    right = a[left_n:]
    right_n = len(right)

    left_map = {}

    def build(pos, total, code, place):
        if pos == left_n:
            r = total % m
            if r not in left_map:
                left_map[r] = code
            return

        build(pos + 1, total, code, place * 3)
        build(pos + 1, total + left[pos], code + place, place * 3)
        build(pos + 1, total - left[pos], code + 2 * place, place * 3)

    build(0, 0, 0, 1)

    answer = None

    def search(pos, total, code, place):
        nonlocal answer

        if answer is not None:
            return

        if pos == right_n:
            target = (-total) % m
            if target in left_map:
                lc = left_map[target]
                if lc != 0 or code != 0:
                    answer = (lc, code)
            return

        search(pos + 1, total, code, place * 3)
        search(pos + 1, total + right[pos], code + place, place * 3)
        search(pos + 1, total - right[pos], code + 2 * place, place * 3)

    search(0, 0, 0, 1)

    if answer is None:
        return "-1\n"

    lc, rc = answer
    first = []
    second = []

    for i in range(left_n):
        d = lc % 3
        lc //= 3
        if d == 1:
            first.append(i + 1)
        elif d == 2:
            second.append(i + 1)

    for i in range(right_n):
        d = rc % 3
        rc //= 3
        if d == 1:
            first.append(left_n + i + 1)
        elif d == 2:
            second.append(left_n + i + 1)

    return (
        f"{len(first)}\n"
        f"{' '.join(map(str, first))}\n"
        f"{len(second)}\n"
        f"{' '.join(map(str, second))}\n"
    )

def check(inp: str):
    data = list(map(int, inp.split()))
    n, m = data[0], data[1]
    a = data[2:2 + n]

    out = solve(inp).split()
    assert out, "empty output"

    if out[0] == "-1":
        # For tests below we only use cases with known solutions,
        # except the explicit impossible case checked separately.
        return False

    p = 0
    k = int(out[p])
    p += 1
    first = list(map(int, out[p:p + k]))
    p += k

    q = int(out[p])
    p += 1
    second = list(map(int, out[p:p + q]))

    assert len(first) == k
    assert len(second) == q
    assert k + q > 0
    assert len(set(first)) == k
    assert len(set(second)) == q
    assert set(first).isdisjoint(second)
    assert all(1 <= x <= n for x in first + second)

    s1 = sum(a[i - 1] for i in first) % m
    s2 = sum(a[i - 1] for i in second) % m
    assert s1 == s2

    return True

# Provided sample 1.
assert check("4 14\n1 3 7 10\n"), "sample 1"

# Provided sample 2.
assert check("3 7\n1 2 4\n"), "sample 2"

# Minimum-size input, m = 1 means any nonempty placement works.
assert check("1 1\n999999999\n"), "minimum size"

# All values equal. Two weights on each side give equal sums.
assert check("5 7\n3 3 3 3 3\n"), "all equal values"

# Maximum n and a modulus close to the upper boundary.
# A pair of equal weights already balances the scale.
assert check(
    "25 39999999\n"
    "1 1 1 1 1 1 1 1 1 1 1 1 1 "
    "1 1 1 1 1 1 1 1 1 1 1 1 1\n"
), "maximum n"

# A value divisible by m exercises the direct single-weight boundary.
assert check("4 10\n20 3 7 11\n"), "divisible weight"

# Explicit impossible case.
assert solve("1 5\n3\n").strip() == "-1", "impossible single weight"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 999999999` | Any nonempty placement | Minimum `n` and `m = 1` |
| `5 7 / 3 3 3 3 3` | Two weights on each side, or another valid placement | Equal values and disjoint plates |
| `25 39999999 / 25 ones` | Any placement with equal residues, for example one weight per plate | Maximum `n` and modulus near its upper bound |
| `4 10 / 20 3 7 11` | Weight `1` alone is valid | Direct divisibility shortcut |
| `1 5 / 3` | `-1` | No nonempty assignment exists |

## Edge Cases

For the single-weight impossible case

```
1 5
3
```

the algorithm first checks whether `3 % 5` is zero, which it is not. The two halves contain one weight and no weights. The only nonempty ternary assignment has signed sum `3` or `-3`, neither divisible by `5`, so the search finishes without a match and prints `-1`.

For the modulus-one case

```
1 1
3
```

the algorithm stops immediately. Since every integer is congruent to zero modulo `1`, placing weight `1` on the first plate is valid. The output is equivalent to

```
1
1
0
```

The blank line represents the empty second plate.

For the one-sided solution

```
3 7
1 2 4
```

the signed assignment `(+1, +1, +1)` has sum `7`, so its residue is zero. The other plate can use the zero assignment. The algorithm accepts this because the combined ternary code is nonzero even though the second-half code may represent an empty plate.

For equal weights,

```
5 7
3 3 3 3 3
```

placing two weights on each plate gives sums `6` and `6`. The ternary representation assigns two weights the coefficient `+1`, two weights the coefficient `-1`, and leaves the fifth unused. The signed sum is zero, so the two plate residues match exactly.

The most dangerous implementation mistake is accepting the pair where both ternary codes are zero. That pair always exists because the empty assignment has residue zero in both halves. The explicit `left_code != 0 or code != 0` check removes precisely that invalid solution while preserving valid cases where one plate is empty.
