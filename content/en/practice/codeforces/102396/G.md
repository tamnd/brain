---
title: "CF 102396G - Weight Overflow"
description: "We have up to 25 weights, and each weight can be handled in exactly one of three ways: it can be placed on the first plate, placed on the second plate, or left unused. The scale does not compare the actual sums."
date: "2026-08-11T23:31:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "G"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 427
verified: false
draft: false
---

[CF 102396G - Weight Overflow](https://codeforces.com/problemset/problem/102396/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have up to 25 weights, and each weight can be handled in exactly one of three ways: it can be placed on the first plate, placed on the second plate, or left unused. The scale does not compare the actual sums. It first reduces each plate's total modulo `m`, then compares those residues. We need a nonempty assignment for which the two residues are equal.

If weight `i` is on the first plate, give it coefficient `+1`. If it is on the second plate, give it coefficient `-1`. If it is unused, give it coefficient `0`. The condition becomes

[
\sum_{i=1}^{n} c_i a_i \equiv 0 \pmod m,
]

where every coefficient satisfies (c_i\in{-1,0,1}), and not all coefficients are zero. Once such coefficients are found, positive coefficients describe the first plate and negative coefficients describe the second.

The constraints point toward exponential search rather than polynomial dynamic programming. There are only 25 weights, so exponential dependence on `n` can be acceptable if the exponent is reduced by splitting the weights. A direct enumeration has (3^{25}=847288609443) possible assignments, which is far beyond the one second limit. The value of `m` can be almost (4\cdot10^7), so a conventional DP array indexed by residues would also be too large for a transition for every weight. The official problem constraints are `n <= 25` and `m < 4 * 10^7`, with a one second time limit and 512 MB of memory.

Several small cases can expose incorrect implementations.

For `m = 1`, every nonempty placement is valid because every integer is congruent to zero modulo 1. For example,

```
1 1
5
```

can be answered by putting weight 1 on the first plate and nothing on the second. An implementation that only searches for two different subsets may accidentally report `-1`.

A weight whose mass is already divisible by `m` is an immediate answer. For example,

```
1 7
14
```

is solved by putting weight 1 on either plate. The modulo condition is about the residue, not about the raw sum.

The empty assignment must never be accepted. For example,

```
1 7
1
```

has no solution. The only signed sums are `0`, from using nothing, and `1` or `-1`, from using the weight. A careless meet-in-the-middle implementation may find residue zero from the empty assignment on both halves and incorrectly accept it.

The same weight cannot be put on both plates. For example,

```
2 10
3 3
```

is solved by putting weight 1 on one plate and weight 2 on the other. Both plate residues are 3. A representation that treats the two sides as independent subsets without remembering that they must be disjoint could accidentally use one index twice.

Finally, equality is modulo `m`, not equality of the ordinary sums. For

```
2 5
7 2
```

putting the two weights on opposite plates works because `7 mod 5 = 2 mod 5`, even though their actual masses differ.

## Approaches

The most direct solution considers every weight independently and tries all three choices: unused, first plate, or second plate. For every assignment we compute the signed sum modulo `m` and accept if it is zero and at least one weight was selected. This is correct because every legal placement corresponds to exactly one vector of coefficients from `{-1,0,1}`.

The problem is the number of assignments. With 25 weights there are

[
3^{25}=847288609443
]

possibilities. Even if checking one assignment took only a few machine instructions, hundreds of billions of states cannot fit into the time limit.

The useful observation is that the signed sum is additive. Split the weights into two disjoint halves. For an assignment in the first half, let its signed sum be `x`. For an assignment in the second half, let its signed sum be `y`. Together they form a valid solution exactly when

[
x+y\equiv0\pmod m.
]

So instead of enumerating all (3^n) assignments, we enumerate roughly (3^{n/2}) assignments in each half and match complementary residues.

With 25 weights, one half has at most 12 weights and the other has at most 13. Their search spaces contain at most (3^{12}=531441) and (3^{13}=1594323) assignments respectively. We store one assignment for every residue produced by the first half in a hash table, then enumerate the second half and look for the residue that is its modular negation.

There is one subtle point in storing the empty assignment. Residue zero is always produced by doing nothing. If we store only that assignment, a later search that also produces zero could accidentally combine two empty assignments. The implementation explicitly rejects that case, and it also prefers a nonempty first-half assignment for residue zero when one exists.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n)) | (O(n)) | Too slow |
| Meet in the Middle | (O(3^{n/2})) | (O(3^{n/2})) | Accepted |

The modular arithmetic also means that every intermediate sum can be reduced immediately. Python integers are unbounded, so there is no integer overflow concern even though the original masses can be as large as (10^9).

## Algorithm Walkthrough

1. Split the weights into two consecutive halves. If `n = 25`, the first half contains 12 weights and the second contains 13. The halves are disjoint, which means any assignment chosen independently in each half automatically uses every weight at most once.
2. Enumerate every ternary assignment of the first half. For each weight, coefficient `0` means unused, `1` means the first plate, and `2` means the second plate. Convert these choices to coefficients `0`, `+1`, and `-1`, and calculate the signed sum modulo `m`.
3. Store one ternary encoding for every residue encountered in the first half. If the residue is zero and the table currently contains only the empty encoding, replace it when a nonempty encoding with the same residue appears. The stored encoding is enough to reconstruct which weights belong to each plate.
4. Enumerate every ternary assignment of the second half. Suppose its signed sum is `s`. A compatible assignment from the first half must have residue `(-s) mod m`, because the combined signed sum has to be zero modulo `m`.
5. Look up `(-s) mod m` in the first-half table. If it is absent, this second-half assignment cannot form a solution. If it is present, combine the two encodings.
6. Reject the combination only when both encodings are empty. Any other combination contains at least one selected weight and has total signed sum divisible by `m`, so it is a valid answer.
7. Decode the two ternary encodings. A digit representing `+1` goes to the first plate, while a digit representing `-1` goes to the second plate. Print the two index sets.

Why it works: every legal placement has a unique signed representation with coefficients in `{-1,0,1}`. Splitting the indices divides its signed sum into a contribution from each half, say `x` and `y`, with `x + y ≡ 0 (mod m)`. During the second-half enumeration, the algorithm searches exactly for a first-half residue equal to `-y`, so every possible solution is considered. Conversely, every pair returned by the lookup has `x + y ≡ 0`, and the halves are disjoint, so their decoded assignments form a legal placement. The explicit empty-assignment check guarantees that at least one weight is actually placed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_map(values, mod):
    """
    Map residue -> one ternary encoding for this half.

    Ternary digit:
        0 = unused
        1 = first plate
        2 = second plate
    """
    result = {}

    def dfs(pos, total, code, place):
        if pos == len(values):
            old = result.get(total)
            if old is None or (total == 0 and old == 0 and code != 0):
                result[total] = code
            return

        # Leave this weight unused.
        dfs(pos + 1, total, code, place * 3)

        # Put it on the first plate.
        nxt = total + values[pos]
        if nxt >= mod:
            nxt -= mod
        dfs(pos + 1, nxt, code + place, place * 3)

        # Put it on the second plate.
        nxt = total - values[pos]
        if nxt < 0:
            nxt += mod
        dfs(pos + 1, nxt, code + 2 * place, place * 3)

    dfs(0, 0, 0, 1)
    return result

def find_in_second(values, mod, first_map):
    """
    Search all ternary assignments of the second half.
    Returns (first_code, second_code), or None.
    """

    answer = None

    def dfs(pos, total, code, place):
        nonlocal answer

        if answer is not None:
            return

        if pos == len(values):
            need = (-total) % mod
            first_code = first_map.get(need)

            if first_code is not None:
                if first_code != 0 or code != 0:
                    answer = (first_code, code)
            return

        # Unused.
        dfs(pos + 1, total, code, place * 3)

        if answer is not None:
            return

        # First plate.
        nxt = total + values[pos]
        if nxt >= mod:
            nxt -= mod
        dfs(pos + 1, nxt, code + place, place * 3)

        if answer is not None:
            return

        # Second plate.
        nxt = total - values[pos]
        if nxt < 0:
            nxt += mod
        dfs(pos + 1, nxt, code + 2 * place, place * 3)

    dfs(0, 0, 0, 1)
    return answer

def decode(code, length, offset, first, second):
    for i in range(length):
        digit = code % 3
        code //= 3

        index = offset + i + 1

        if digit == 1:
            first.append(index)
        elif digit == 2:
            second.append(index)

def solve():
    n, mod = map(int, input().split())
    a = list(map(int, input().split()))

    # Reducing the masses once makes every later transition smaller.
    a = [x % mod for x in a]

    # A split near the middle minimizes the larger ternary search space.
    mid = n // 2
    left = a[:mid]
    right = a[mid:]

    first_map = build_map(left, mod)
    answer = find_in_second(right, mod, first_map)

    if answer is None:
        print(-1)
        return

    left_code, right_code = answer

    first_plate = []
    second_plate = []

    decode(left_code, len(left), 0, first_plate, second_plate)
    decode(right_code, len(right), mid, first_plate, second_plate)

    print(len(first_plate))
    print(*first_plate)
    print(len(second_plate))
    print(*second_plate)

if __name__ == "__main__":
    solve()
```

The first preprocessing line reduces every `a[i]` modulo `m`. This is mathematically safe because only residues affect the final comparison. It also lets each recursive transition stay inside the interval `[0, m)` using one conditional adjustment rather than repeatedly constructing larger integers.

`build_map` performs the entire first-half search. The `code` variable is a base-three encoding of the decisions already made. The `place` variable is the current power of three, so choosing the first plate adds `place` to the encoding and choosing the second plate adds `2 * place`.

The signed sum is kept modulo `m` after every choice. For a positive transition, adding a value can reach at most `2m - 2`, so one subtraction is sufficient. For a negative transition, the result can be as low as `-(m - 1)`, so one addition is sufficient. This avoids a `%` operation at every recursive node.

The special handling of residue zero is easy to overlook. The empty assignment must be stored because it can legitimately combine with a nonempty assignment from the other half. However, if a nonempty first-half assignment also produces zero, it is better to replace the empty encoding with it. The condition in `build_map` handles exactly that case.

`find_in_second` searches the other half. For every signed residue `total`, it calculates `(-total) % mod` and performs one dictionary lookup. The recursion stops immediately after a valid pair is found, so typical inputs finish much earlier than the full (3^{13}) enumeration.

The ternary encoding uses the least significant digit for the earliest weight in each half. `decode` repeatedly takes `code % 3` and then divides by three, which recovers the decisions in the same order in which they were generated. The index offset for the second half is `mid`, because its first local position corresponds to global weight `mid + 1`.

Python does not have fixed-width integer overflow, so sums such as the original masses are safe. The implementation still performs modular reduction throughout the search because the algorithm itself operates on residue classes.

## Worked Examples

For Sample 1,

```
4 14
1 3 7 10
```

the split is `[1, 3]` and `[7, 10]`.

| Stage | Assignment | Signed sum modulo 14 | Required first-half residue |
| --- | --- | --- | --- |
| First half | `+1, +3` | 4 |  |
| Second half | empty | 0 | 0 |
| Second half | `+7` | 7 | 7 |
| Second half | `+10` | 10 | 4 |
| Match | `(+1,+3)` with `(+10)` | `4 + 10 = 14 ≡ 0` | 4 |

The algorithm can consequently put weights 1, 2, and 4 on the first plate and leave the second plate empty. Their total is 14, so the scale computes `14 mod 14 = 0` on the first plate and `0` on the second. The sample's output is different, but both are valid because the problem asks for any valid construction.

For Sample 2,

```
3 7
1 2 4
```

the split is `[1]` and `[2, 4]`.

| Stage | Assignment | Signed sum modulo 7 | Required first-half residue |
| --- | --- | --- | --- |
| First half | `+1` | 1 |  |
| Second half | `+2` | 2 | 5 |
| Second half | `-2` | 5 | 2 |
| Second half | `+4` | 4 | 3 |
| Second half | `-4` | 3 | 4 |
| Second half | `+2,+4` | 6 | 1 |
| Match | `+1` with `+2,+4` | `1 + 6 = 7 ≡ 0` | 1 |

The resulting construction places all three weights on the first plate. Its sum is 7, whose residue modulo 7 is zero, while the second plate is empty. This is exactly the sample's construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(3^{n/2})) | Each half is enumerated once, and every state performs constant-time modular arithmetic and, for the second half, a hash-table lookup. |
| Space | (O(3^{n/2})) | The first half stores one ternary encoding for each distinct residue, with at most (3^{n/2}) entries. |

For `n = 25`, the larger half has only 13 weights, so it contains at most `3^13 = 1,594,323` assignments. The smaller half has at most `3^12 = 531,441` assignments. This is several orders of magnitude smaller than the direct `3^25` search and fits comfortably within the 512 MB memory limit. The maximum value of `m` does not appear as a dimension of the DP, so the large modulo bound does not make the memory usage proportional to 40 million.

## Test Cases

Because the output is not unique, tests should validate the returned placement rather than compare the exact output string. The following harness checks that every reported index is valid, no index is used twice, at least one weight is placed, and the two plate sums have equal residues.

```python
import sys
import io

# Paste the solve_data implementation from the solution here.
def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        # Call the submitted solve() here.
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    n, mod = data[0], data[1]
    a = data[2:2 + n]

    tokens = out.split()
    if not tokens:
        return False

    if tokens[0] == "-1":
        return True

    p = 0

    k = int(tokens[p])
    p += 1
    first = list(map(int, tokens[p:p + k]))
    p += k

    q = int(tokens[p])
    p += 1
    second = list(map(int, tokens[p:p + q]))
    p += q

    if p != len(tokens):
        return False

    if k + q == 0:
        return False

    if any(x < 1 or x > n for x in first + second):
        return False

    if len(set(first)) != len(first):
        return False

    if len(set(second)) != len(second):
        return False

    if set(first) & set(second):
        return False

    s1 = sum(a[i - 1] for i in first) % mod
    s2 = sum(a[i - 1] for i in second) % mod

    return s1 == s2

# Provided sample 1.
sample1 = """\
4 14
1 3 7 10
"""
assert validate(sample1, solve_data(sample1)), "sample 1"

# Provided sample 2.
sample2 = """\
3 7
1 2 4
"""
assert validate(sample2, solve_data(sample2)), "sample 2"

# Minimum-size case and m = 1.
case1 = """\
1 1
123456789
"""
assert validate(case1, solve_data(case1)), "minimum size and modulo 1"

# A weight is itself divisible by m.
case2 = """\
1 7
14
"""
assert validate(case2, solve_data(case2)), "single divisible weight"

# Equal weights must be placed on opposite plates.
case3 = """\
2 10
3 3
"""
assert validate(case3, solve_data(case3)), "all equal values"

# Maximum n, with no signed sum able to reach a nonzero multiple
# of m. The total absolute sum is smaller than m.
case4 = "25 39999989\n" + " ".join(str(1 << i) for i in range(25)) + "\n"
result4 = solve_data(case4)
assert result4.strip() == "-1", "maximum-size no-solution case"

# Empty assignment must not be accepted.
case5 = """\
1 7
1
"""
assert solve_data(case5).strip() == "-1", "empty assignment"
```

The first two tests confirm the sample constructions while allowing the program to produce a different valid assignment. The third test checks the smallest possible `n` and the special case `m = 1`. The fourth checks the direct single-weight solution when a mass is divisible by the modulus. The fifth checks that two equal weights can balance on opposite plates without reusing an index. The sixth is a maximum-size stress case that forces the algorithm to explore the search space and confirms that the implementation can correctly report that no solution exists. The final test specifically catches the common mistake of accepting the empty assignment.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 14 / 1 3 7 10` | Any valid placement | Sample 1 |
| `3 7 / 1 2 4` | Any valid placement | Sample 2 |
| `1 1 / 123456789` | A nonempty placement | Minimum size and `m = 1` |
| `1 7 / 14` | Weight 1 on either plate | Direct divisible weight |
| `2 10 / 3 3` | One weight on each plate | Equal values and disjointness |
| `25 39999989 / 1 2 4 ... 2^24` | `-1` | Maximum-size exhaustive search |
| `1 7 / 1` | `-1` | Empty assignment rejection |

## Edge Cases

When `m = 1`, every residue is zero. For the input

```
1 1
5
```

the first-half map contains residue zero from both the empty assignment and the assignment using the weight. The implementation deliberately prefers the nonempty encoding for residue zero. The second half is empty, so the resulting construction contains weight 1 and is accepted.

When a single weight is divisible by `m`, the empty assignment in the other half is enough to complete it. For

```
1 7
14
```

the signed residue of weight 1 is zero. The first-half map stores a nonempty encoding for residue zero, and the second-half search can use its empty assignment. The combined placement contains one weight and has signed sum zero modulo 7.

For equal weights, consider

```
2 10
3 3
```

The assignment `+3 - 3` has signed sum zero. Since the two weights belong to different halves, the meet-in-the-middle lookup finds residue `3` from one half and residue `7`, its modular negation, from the other half. The decoded result puts the two different indices on opposite plates, giving residues `3` and `3`.

For an impossible case,

```
1 7
1
```

the only nonempty signed sums are `1` and `-1`, whose residues are `1` and `6`. Neither is zero. The only zero residue comes from choosing nothing, but the second-half search explicitly rejects the pair where both encodings are zero, so the program prints `-1`.

For the maximum-size case, the split contains 12 and 13 weights. The first map has room for at most (3^{12}) distinct assignments, while the second enumeration examines at most (3^{13}). No part of the implementation depends linearly on the potentially enormous value of `m`, and every assignment is represented compactly by a ternary integer rather than by a list of selected indices.

The central invariant is simple: every stored residue represents a real signed assignment of its half, and every second-half state is matched only against the modular complement of its own signed sum. Once a pair is found, their coefficients describe a valid placement over disjoint sets of indices, so the equality of the two plate residues follows directly from the equation (x+y\equiv0\pmod m).
