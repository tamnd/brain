---
title: "CF 102192I - Make ZYB Happy"
description: "We have (n) titles. Title (ti) has a happiness value (hi). For any string (x), look at every title in which (x) occurs at least once. ZYB's happiness from saying (x) is the product of the corresponding (hi)."
date: "2026-08-18T02:09:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "I"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 267
verified: true
draft: false
---

[CF 102192I - Make ZYB Happy](https://codeforces.com/problemset/problem/102192/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) titles. Title (t_i) has a happiness value (h_i). For any string (x), look at every title in which (x) occurs at least once. ZYB's happiness from saying (x) is the product of the corresponding (h_i). Occurring several times inside the same title does not multiply the value again.

For a query (m), every nonempty lowercase string whose length is at most (m) is chosen with equal probability. If a string is not a substring of any title, its happiness is zero. We need the expected happiness modulo (10^9+7).

The input contains at most (10^4) titles, while their total length is at most (3\cdot10^5). This total length is the parameter that matters for the string data structure, because a suffix automaton has linear size in the total input length. The query count can also reach (3\cdot10^5), so answering each query by scanning all lengths is too expensive. The query length can reach (10^6), which means the denominator of the probability distribution must be handled independently of the title lengths.

For a fixed (m), the number of possible strings is

[
D_m=26^1+26^2+\cdots+26^m.
]

The numerator is the sum of the happiness values of all distinct strings of lengths at most (m). A direct enumeration is impossible. Even one title of length (300000) has (300000\cdot300001/2=45000150000) substring occurrences, before removing duplicates.

There are several easy places to make a silent mistake. First, repeated occurrences inside one title must not multiply the happiness more than once. For example,

```
1
aaa
2
1
1
```

The only useful length-one string is `a`, and its happiness is (2), not (2^3), so the answer is (2/26=1/13), namely (153846155) modulo the given prime. An occurrence-based implementation would incorrectly treat the three copies of `a` as three independent contributions.

Second, the same string occurring in several titles must multiply their values. For example,

```
2
a
a
2 3
1
1
```

The string `a` occurs in both titles, so its happiness is (2\cdot3=6). The correct answer is (6/26=461538465). An implementation that stores each distinct string only once without its set of titles could incorrectly use (2+3) or one of the two values.

Third, a query can be longer than every title. Consider

```
1
a
1
1
2
```

For (m=2), only `a` contributes to the numerator, so the numerator is still (1), but the denominator is (26+26^2=702). The answer is (702^{-1}=206552708). The denominator must not be capped at the longest title.

The official archive contains the original problem and the sample data.

## Approaches

The brute-force idea is conceptually simple. Enumerate every candidate string of length at most (m), search for it in every title, determine which titles contain it, multiply their happiness values, and add the result. This is correct because it directly follows the definition of the expected value. Unfortunately, the number of candidates is

[
26+26^2+\cdots+26^m=\Theta(26^m).
]

For (m=10^6), this is beyond any meaningful computation. Even if we avoid enumerating candidates that never occur and instead enumerate all substrings of the titles, a single title of length (300000) has (45000150000) substring occurrences.

The brute force works because every individual string can be evaluated independently, but it fails because almost all of the work is repeated between highly overlapping substrings. The key observation is that suffix automata group substrings that have the same set of ending positions. In particular, all strings represented by one suffix automaton state have exactly the same occurrence set, so they also occur in exactly the same collection of titles. Their happiness value is consequently identical.

This makes a generalized suffix automaton the natural compression. We build one automaton containing all titles, resetting the current state to the root before inserting each new title. For every title, we then walk through it in the automaton. At each reached state, its suffix-link ancestors represent suffixes of the current prefix, so all of those states correspond to substrings occurring in this title. We multiply the state's value by the title's (h_i), but only once per title.

After that, one suffix automaton state still represents several different substring lengths. If a state (v) has length `len[v]` and suffix link (fa[v]), then it represents exactly one distinct substring for every length in

[
[\text{len}[fa[v]]+1,\text{len}[v]].
]

All those substrings have the same occurrence set and therefore the same happiness value. We can add that value to an interval using a difference array. Two prefix sums then turn these state intervals into the total happiness for every exact length and finally the total happiness for every length up to (m).

The generalized suffix automaton construction used here is the standard construction for inserting several strings independently from the root.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(26^m)), or (\Theta(L^2)) just to enumerate substring occurrences | Potentially (\Theta(26^m)) | Too slow |
| Generalized SAM | (O(L+M+Q)) amortized, where (L) is total title length and (M) is the maximum query | (O(L+M+Q)) | Accepted |

## Algorithm Walkthrough

1. Read all titles first and let (L) be their total length. A suffix automaton built by ordinary extension has at most (2L+1) states, so we can reserve enough storage before constructing it.
2. Build a generalized suffix automaton. Before inserting every title, set `last` to the root. When a transition already exists from the current state, reuse it if its length is exactly one greater than the current state's length. Otherwise create a clone, exactly as in the ordinary suffix automaton construction.

The special handling of an existing transition is what lets several independent titles share the same automaton without inserting artificial separator characters.
3. Initialize the happiness value of every state to (1). For each title (t_i), walk through the title from the root. After reaching the state corresponding to the current prefix, follow suffix links upward. Every visited state represents substrings occurring in (t_i), so multiply its stored value by (h_i).

A state only needs to be updated once for one title. Store the current title's index in `seen[state]`. When the upward walk reaches a state already marked with that title index, stop. All of its suffix-link ancestors have already been marked during the earlier walk.
4. After processing every title, state (v) has a value equal to the product of (h_i) over exactly those titles containing the substrings represented by (v).

This works because suffix automaton states are equivalence classes of strings with equal end-position sets. Equal end-position sets imply equal title-membership sets, even though the actual occurrence positions may be different across titles.
5. For every non-root state (v), add `value[v]` to the length interval

[
[\text{len}[fa[v]]+1,\text{len}[v]].
]

Store this with a difference array:

[
diff[\text{len}[fa[v]]+1] += value[v],
]

[
diff[\text{len}[v]+1] -= value[v].
]

There is no need to traverse the suffix-link tree here. Every state already knows its suffix link and its length, so all intervals can be processed directly.
6. Take one prefix sum of the difference array. After this pass, `by_len[k]` is the sum of happiness values of all distinct strings of exactly length (k).
7. Take a second prefix sum. Now `prefix[k]` is the total happiness of every distinct string whose length is between (1) and (k). Strings that are not substrings of any title contribute zero automatically.
8. For every query (m), the desired expectation is

[
\frac{\text{prefix}[m]}
{26^1+26^2+\cdots+26^m}
\pmod {10^9+7}.
]

The numerator becomes constant once (m) exceeds the longest title, but the denominator keeps increasing. This is why queries larger than the longest title must still use their original (m).
9. Since there can be (3\cdot10^5) queries, computing a modular inverse separately for every denominator would add (O(Q\log MOD)) work. Instead, sort the distinct query values, compute their denominators while advancing through the lengths once, and use batch inversion. The product of all denominators is inverted once, after which every individual inverse is recovered in linear time.

### Why it works

Consider any generalized suffix automaton state (v). Its represented strings all have the same end-position set, so they occur in exactly the same titles. The multiplication performed while processing every title consequently gives precisely the happiness value of every string represented by (v). The suffix-link structure partitions all distinct substrings into the disjoint length intervals ((\text{len}[fa[v]],\text{len}[v]]), with one distinct substring for every length in that interval. Adding the state's value to this interval therefore counts every distinct occurring string exactly once. The two prefix sums convert these per-length contributions into the numerator for every query, while the denominator counts every possible random string, including strings that occur nowhere. Hence the final fraction is exactly the required expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array

MOD = 1000000007
ALPHA = 26

def solve():
    n = int(input())
    titles = [input().strip().encode() for _ in range(n)]
    total_len = sum(len(s) for s in titles)
    max_title_len = max(len(s) for s in titles)

    happiness = list(map(int, input().split()))

    q = int(input())
    queries = [int(input()) for _ in range(q)]
    max_query = max(queries)

    # A SAM built from L characters has at most 2L+1 states.
    max_states = 2 * total_len + 5

    # Compact 32-bit arrays are necessary in Python.
    # transitions[state * 26 + c] stores the destination.
    trans = array('i', [0]) * (max_states * ALPHA)
    link = array('i', [0]) * max_states
    length = array('i', [0]) * max_states
    seen = array('i', [0]) * max_states
    value = array('i', [1]) * max_states

    # Root is state 1.
    size = 1

    for s in titles:
        last = 1

        for ch in s:
            c = ch - 97
            p = last
            edge = trans[p * ALPHA + c]

            if edge:
                # The transition already exists.
                qstate = edge

                if length[qstate] == length[p] + 1:
                    last = qstate
                    continue

                # The existing transition is too long, so clone it.
                clone = size + 1
                size = clone

                length[clone] = length[p] + 1
                link[clone] = link[qstate]

                src = qstate * ALPHA
                dst = clone * ALPHA
                trans[dst:dst + ALPHA] = trans[src:src + ALPHA]

                while p and trans[p * ALPHA + c] == qstate:
                    trans[p * ALPHA + c] = clone
                    p = link[p]

                link[qstate] = clone
                last = clone
                continue

            # Create the usual new state.
            new_state = size + 1
            size = new_state
            length[new_state] = length[p] + 1
            last = new_state

            while p and trans[p * ALPHA + c] == 0:
                trans[p * ALPHA + c] = new_state
                p = link[p]

            if p == 0:
                link[new_state] = 1
                continue

            qstate = trans[p * ALPHA + c]

            if length[qstate] == length[p] + 1:
                link[new_state] = qstate
                continue

            # Split qstate with a clone.
            clone = size + 1
            size = clone

            length[clone] = length[p] + 1
            link[clone] = link[qstate]

            src = qstate * ALPHA
            dst = clone * ALPHA
            trans[dst:dst + ALPHA] = trans[src:src + ALPHA]

            link[qstate] = clone
            link[new_state] = clone

            while p and trans[p * ALPHA + c] == qstate:
                trans[p * ALPHA + c] = clone
                p = link[p]

    # For each title, mark every SAM state whose represented strings occur
    # in that title, and multiply its happiness exactly once.
    for tag, (s, h) in enumerate(zip(titles, happiness), 1):
        cur = 1

        for ch in s:
            cur = trans[cur * ALPHA + ch - 97]

            v = cur
            while v and seen[v] != tag:
                seen[v] = tag
                value[v] = value[v] * h % MOD
                v = link[v]

    # Difference array over substring lengths.
    diff = array('i', [0]) * (max_title_len + 2)

    for v in range(2, size + 1):
        left = length[link[v]] + 1
        right = length[v]

        diff[left] += value[v]
        if diff[left] >= MOD:
            diff[left] -= MOD

        diff[right + 1] -= value[v]
        if diff[right + 1] < 0:
            diff[right + 1] += MOD

    # First prefix sum gives the contribution of each exact length.
    # Second prefix sum gives the contribution of all lengths <= m.
    current = 0
    cumulative = 0

    for i in range(1, max_title_len + 1):
        current += diff[i]
        if current >= MOD:
            current -= MOD

        cumulative += current
        if cumulative >= MOD:
            cumulative -= MOD

        diff[i] = cumulative

    # Compute denominators for the distinct queried lengths.
    unique_queries = sorted(set(queries))
    denominators = []

    power = 1
    denominator = 0
    position = 0

    for m in unique_queries:
        while position < m:
            power = power * 26 % MOD
            denominator += power
            if denominator >= MOD:
                denominator -= MOD
            position += 1

        denominators.append(denominator)

    # Batch inversion of all distinct denominators.
    k = len(denominators)
    prefix_product = [1] * k
    product = 1

    for i, d in enumerate(denominators):
        prefix_product[i] = product
        product = product * d % MOD

    inverse_product = pow(product, MOD - 2, MOD)
    inverses = [0] * k

    for i in range(k - 1, -1, -1):
        inverses[i] = inverse_product * prefix_product[i] % MOD
        inverse_product = inverse_product * denominators[i] % MOD

    inverse_by_query = {
        m: inv for m, inv in zip(unique_queries, inverses)
    }

    output = []

    for m in queries:
        if m <= max_title_len:
            numerator = diff[m]
        else:
            numerator = diff[max_title_len]

        answer = numerator * inverse_by_query[m] % MOD
        output.append(str(answer))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The first part of the implementation reads all titles before allocating the automaton. That gives the total length in advance, so the transition table can be stored in one compact `array('i')` with (26(2L+5)) entries. A Python list of lists would use far more memory because every integer and every list carries Python object overhead.

The insertion code is the generalized version of the ordinary suffix automaton extension. The current state is reset to the root for each title. When an existing transition has exactly the required length, it can represent the new prefix directly. If it is longer than required, cloning is necessary to separate the equivalence classes. The clone receives a copy of the outgoing transitions and inherits the old suffix link.

The `seen` array is indexed by the title number. This is cheaper than clearing a boolean array for every title. During one title's traversal, reaching a state whose `seen` value already equals the current title means that state and all suffix-link ancestors above it were already processed.

The root is deliberately skipped when constructing the difference array. It represents the empty string, while the random string in the problem must be nonempty. The interval starts at `length[link[v]] + 1`, and the endpoint is `length[v]`, so the right boundary is inclusive. The subtraction is placed at `right + 1`, which is the standard difference-array convention.

All happiness products are reduced modulo (10^9+7) immediately. Python integers do not overflow, but delaying modular reduction would make the values unnecessarily large and slow down multiplication.

The denominator is not stored for every length. The queries are sorted, and the running power of (26) is advanced only as far as necessary. This uses (O(M)) time where (M) is the largest query. Batch inversion then reduces all denominator inversions to one modular exponentiation plus linear work.

The numerator array only needs to extend to the longest title. Beyond that point there are no new occurring strings, so the numerator remains constant. The denominator, however, continues growing for every larger query.

## Worked Examples

The official sample is

```
2
zybnb
ybyb
3 5
4
1
2
3
4
```

For the first title, the happiness value is (3), and for the second it is (5). The distinct occurring strings grouped by length have the following total happiness.

| Length | Distinct occurring strings | Contribution of this length | Cumulative numerator |
| --- | --- | --- | --- |
| 1 | `z`, `y`, `b`, `n` | (3+15+15+3=36) | 36 |
| 2 | `zy`, `yb`, `bn`, `nb`, `by` | (3+15+3+3+5=29) | 65 |
| 3 | `zyb`, `ybn`, `bnb`, `yby`, `byb` | (3+3+3+5+5=19) | 84 |
| 4 | `zybn`, `ybnb`, `ybyb` | (3+3+5=11) | 95 |

For (m=1), the denominator is (26), so the expectation is (36/26=18/13), giving `769230776`. For (m=2), the denominator is (26+676=702), and the numerator is (65), giving `425925929`. The remaining two queries use numerators (84) and (95), producing the official outputs `891125950` and `633120399`.

The state-level SAM calculation is compressed into those length contributions. A state whose interval is, for example, lengths (2) through (4) contributes its single happiness value to all three of those lengths, which is exactly what the difference array represents.

For a second example, take one title:

```
1
ab
2
3
1
2
3
```

The useful strings are `a`, `b`, and `ab`, each with happiness (2). The processing by length is:

| Length | State contribution after suffix-link intervals | Exact-length total | Cumulative numerator | Denominator |
| --- | --- | --- | --- | --- |
| 1 | `a`, `b` each contribute 2 | 4 | 4 | 26 |
| 2 | `ab` contributes 2 | 2 | 6 | 702 |
| 3 | no occurring string | 0 | 6 | 18278 |

The answers are consequently (4/26=307692310), (6/702=239316241), and (6/18278) modulo (10^9+7).

This example exercises the boundary of the state interval. The substring `ab` must contribute at exactly length (2), while its suffixes `a` and `b` are represented through other states. It also demonstrates that once the query exceeds the maximum title length, the numerator stops changing but the denominator does not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(L+M+Q)) amortized | SAM construction and title marking are linear in the total title size, length aggregation is linear, denominators take (O(M)), and batch inversion plus output takes (O(Q)) |
| Space | (O(L+M+Q)) | The SAM has (O(L)) states and transitions, the length difference array has (O(L)) entries, and queries plus batch-inversion arrays use (O(Q)) space |

Here (L\le3\cdot10^5), (M\le10^6), and (Q\le3\cdot10^5). The compact integer arrays are particularly useful in Python because the transition table contains roughly (26\cdot2L) four-byte integers rather than millions of Python objects. The resulting memory footprint stays comfortably below the stated 256 MB limit, while the algorithm avoids every operation depending exponentially on the query length.

## Test Cases

The following harness assumes the `solve()` function from the solution above. The helper `fraction_mod` computes small expected values directly, while the final case checks the maximum permitted query length without enumerating any strings.

```python
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

def fraction_mod(numerator, m):
    denominator = 26 * (pow(26, m, MOD) - 1) % MOD
    denominator = denominator * pow(25, MOD - 2, MOD) % MOD
    return numerator * pow(denominator, MOD - 2, MOD) % MOD

# Provided sample
sample = """\
2
zybnb
ybyb
3 5
4
1
2
3
4
"""

assert run(sample) == (
    "769230776\n"
    "425925929\n"
    "891125950\n"
    "633120399\n"
), "sample"

# Minimum-size input
case_min = """\
1
a
1
1
1
"""

assert run(case_min) == "576923081\n", "minimum case"

# Same string in three titles, all happiness values equal.
# The string a must contribute 2*2*2 = 8, not 2.
case_equal = """\
3
a
a
a
2 2 2
2
1
2
"""

assert run(case_equal) == (
    str(fraction_mod(8, 1)) + "\n" +
    str(fraction_mod(8, 2)) + "\n"
), "equal values and repeated titles"

# Boundary between exact substring lengths.
# a and b have contribution 2 each, while ab contributes 2.
case_boundary = """\
1
ab
2
3
1
2
3
"""

assert run(case_boundary) == (
    str(fraction_mod(4, 1)) + "\n" +
    str(fraction_mod(6, 2)) + "\n" +
    str(fraction_mod(6, 3)) + "\n"
), "substring-length boundary"

# Maximum permitted query length.
# The numerator is always 1, but the denominator contains 10^6 length levels.
case_max_query = """\
1
a
1
1
1000000
"""

expected_max = fraction_mod(1, 1000000)
assert run(case_max_query) == str(expected_max) + "\n", "maximum query length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| The provided `zybnb`, `ybyb` sample | `769230776`, `425925929`, `891125950`, `633120399` | Complete reference case and overlapping substrings |
| One title `a`, happiness 1, query 1 | `576923081` | Minimum-size input and root/nonempty-string boundary |
| Three identical titles `a`, all happiness 2 | `307692310`, `652421657` | Multiplication across titles and equal happiness values |
| One title `ab`, happiness 2, queries 1, 2, 3 | `307692310`, `239316241`, `6/18278 mod MOD` | Exact interval endpoints and queries beyond the title |
| One title `a`, happiness 1, query (10^6) | `S_1000000^{-1} mod MOD` | Maximum query length and the fact that the denominator keeps growing |

## Edge Cases

Repeated occurrences inside a single title are handled by the `seen` array. For

```
1
aaa
2
1
```

the title is processed from left to right, and the suffix-link walks may encounter the state representing `a` several times. The first encounter multiplies its value by (2), while subsequent encounters see `seen[state] == 1` and stop at that point. Thus `a`, `aa`, and `aaa` each receive happiness (2), rather than multiplying (2) once per occurrence.

The distinction between title membership and occurrence count is also handled correctly for

```
2
a
a
2 3
1
1
```

The first title marks the state for `a` and changes its value from (1) to (2). The second title has a different tag, so it marks the same state again and changes its value from (2) to (6). The resulting numerator for length one is (6), and the answer is (6/26=461538465). The number of times `a` appears inside either title never enters the calculation.

The suffix-link interval boundary is handled by adding a state's value at `len[fa[v]] + 1` and removing it at `len[v] + 1`. For

```
1
ab
2
1
2
```

the states corresponding to the one-character substrings contribute at length one, while the state representing `ab` contributes at length two. The resulting numerators are (4) and (6). If the subtraction were placed at `len[v]` instead of `len[v] + 1`, the length-two contribution would disappear.

A query longer than every title exercises a different boundary. For

```
1
a
1
1
2
```

the only positive-happiness string is `a`, so the numerator remains (1) for both queries. For (m=2), however, there are (26+676=702) possible strings, giving (1/702=206552708). The implementation keeps the numerator at its last computed value while continuing to extend the denominator through every queried length.

Finally, the root state is never added to the difference array. Its represented string is the empty string, while the random choice contains at least one character. Including the root would add a fictitious length-zero contribution and shift every answer.
