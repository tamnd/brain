---
title: "CF 102470J - Stammering Aliens"
description: "For each test case, we have a lowercase string s and an integer m. We need to find the longest contiguous substring that occurs at least m times in s. Occurrences are allowed to overlap."
date: "2026-08-09T15:38:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102470
codeforces_index: "J"
codeforces_contest_name: "2009-2010 ACM ICPC Southwestern European Regional Programming Contest (SWERC 2009)"
rating: 0
weight: 102470
solve_time_s: 458
verified: true
draft: false
---

[CF 102470J - Stammering Aliens](https://codeforces.com/problemset/problem/102470/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we have a lowercase string `s` and an integer `m`. We need to find the longest contiguous substring that occurs at least `m` times in `s`. Occurrences are allowed to overlap. If several substrings have the same maximum length, we do not need to identify the substring itself. We output the largest starting position among all occurrences of any optimal substring.

The input contains several independent test cases. The first line of a test case gives `m`, followed by the message string. A line containing `m = 0` terminates the input. The string length is between `m` and `40000`, so even a single test case can be large enough that enumerating all substrings and comparing them directly is infeasible. The original problem has a 1 second time limit and 256 MB memory limit.

The overlap condition rules out approaches that treat occurrences as disjoint. For example, with `s = "ababa"` and `m = 2`, the substring `aba` occurs at positions `0` and `2`. The two occurrences share the middle `a`, but both count. The correct output is `3 2`. An implementation that jumps past the end of an occurrence after finding one would incorrectly miss the second occurrence.

The case `m = 1` is another boundary condition. Every substring occurs at least once, so the whole string is automatically optimal. For `m = 1` and `s = "abc"`, the answer is `3 0`. A solution designed only around repeated substrings may incorrectly print `none` because it expects two or more occurrences.

There can also be no valid nonempty substring. For example, with `m = 3` and `s = "abc"`, every one-character substring occurs only once, so nothing can occur three times. The correct output is `none`. A careless implementation might treat the fact that `n >= m` as sufficient and incorrectly output a length-one substring.

Finally, the rightmost-occurrence rule is independent of the maximum length. With `m = 2` and `s = "ababa"`, both `aba` and its occurrences have the optimal length three, and the rightmost occurrence starts at position `2`. Returning the first optimal occurrence, position `0`, gives the wrong answer.

## Approaches

A direct solution starts by considering every possible substring. There are `n(n+1)/2` different positions and lengths, so there are Θ(`n²`) candidates. For each candidate, we could compare it with every possible starting position in the string, and a comparison can inspect Θ(`n`) characters in the worst case. On a string such as a long run of equal characters, almost every comparison reaches the end before discovering a mismatch. The total work is therefore Θ(`n⁴`), with the leading-order comparison work around `n⁴ / 12`. At `n = 40000`, this is far beyond what the time limit allows. Even if we improve the substring comparison with hashing, the straightforward candidate enumeration remains quadratic.

The structure of the problem suggests a stronger representation. We are not interested in arbitrary relationships between substrings. We care about two properties of every substring: its length and all positions where it ends. A suffix automaton groups substrings precisely by their set of ending positions, called their `endpos` set. All substrings represented by one state have exactly the same occurrence positions, while their lengths form one continuous interval from `len(link[v]) + 1` through `len[v]`. This is exactly the information needed here.

Suppose a state `v` has `len[v] = 10` and its occurrence count is at least `m`. Then the longest substring represented by that state has length ten and already satisfies the repetition requirement. We do not have to inspect all shorter strings represented by the same state, because they cannot improve the answer. If several states have the same maximum `len`, their `endpos` sets tell us where their longest representatives occur, so we can also select the rightmost starting position.

The occurrence count of every state can be computed by first assigning one occurrence to every newly created, non-clone state and zero to clones, then propagating counts along suffix links in decreasing `len` order. The same propagation can carry the maximum ending position. This is a standard suffix automaton occurrence-counting technique.

The resulting algorithm is linear in the string length. The suffix automaton has at most `2n - 1` states, and for a fixed lowercase alphabet its construction is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n⁴) | O(n) auxiliary | Too slow |
| Optimal Suffix Automaton | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a suffix automaton while reading the string from left to right. Each state stores `len`, its suffix link, its outgoing transitions, an occurrence counter, and the largest ending position currently known for that state. The state created for the newly appended character starts with occurrence count one and ending position equal to the current index.

The automaton may create a clone when an existing transition points to a state whose represented lengths are too large. A clone copies the transitions and suffix link of the old state but starts with occurrence count zero because creating a clone does not introduce a new occurrence.
2. After construction, count how many states have every possible length. Use counting sort to obtain all states in increasing `len` order. Since every state has `0 <= len <= n`, this sorting is linear rather than comparison-based.

We need decreasing length later because a state's suffix-link parent always has a smaller `len`. Processing children before parents lets every state's accumulated information reach its parent exactly once.
3. Traverse the states in decreasing `len`. For each non-root state `v`, first inspect its accumulated occurrence count. If `occ[v] >= m`, the longest substring represented by `v` is a valid candidate and has length `len[v]`.
4. For a qualifying state, compute its rightmost occurrence from its largest ending position. If `max_end[v]` is the largest ending index, the corresponding occurrence of the longest represented substring starts at

`max_end[v] - len[v] + 1`.

If this length is larger than the current answer, replace both answer values. If the length is equal, keep the larger starting position.
5. After evaluating a state, propagate its occurrence count and maximum ending position to its suffix-link parent. A substring represented by `v` has all of its occurrences as occurrences of the suffix represented by `link[v]`, so both pieces of information must be transferred.
6. If no state with positive length reaches `m` occurrences, print `none`. Otherwise print the maximum qualifying length and its rightmost starting position.

### Why it works

The key invariant is that every suffix automaton state represents exactly one `endpos` equivalence class. All substrings represented by the same state occur at exactly the same ending positions, and the longest such substring has length `len[v]`. After occurrence propagation, `occ[v]` is exactly the number of occurrences of every substring represented by `v`. After maximum-position propagation, `max_end[v]` is the rightmost ending position of those occurrences.

Consequently, every state with `occ[v] >= m` gives one valid substring of length `len[v]`, and no substring represented by that state can be longer. Every substring belongs to some state, so taking the largest `len[v]` over all qualifying states finds the globally longest valid substring. Among states with that same length, `max_end[v] - len[v] + 1` is precisely the rightmost starting position, so the tie-breaking rule is also handled exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(m, s):
    n = len(s)

    # A suffix automaton has at most 2*n states.
    max_states = 2 * n

    transitions = [{} for _ in range(max_states)]
    length = [0] * max_states
    link = [-1] * max_states

    # occ[v] is initially 1 only for newly created states.
    # Clones keep occ = 0.
    occ = [0] * max_states

    # Largest ending position belonging to the state's endpos set.
    max_end = [-1] * max_states

    size = 1
    last = 0

    for i, ch in enumerate(s):
        c = ord(ch) - 97

        cur = size
        size += 1

        length[cur] = length[last] + 1
        occ[cur] = 1
        max_end[cur] = i

        p = last

        while p != -1 and c not in transitions[p]:
            transitions[p][c] = cur
            p = link[p]

        if p == -1:
            link[cur] = 0
        else:
            q = transitions[p][c]

            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = size
                size += 1

                length[clone] = length[p] + 1
                link[clone] = link[q]
                transitions[clone] = transitions[q].copy()

                # The clone represents the same end positions as q
                # before later occurrence propagation.
                max_end[clone] = max_end[q]

                # A clone is not a newly observed occurrence.
                occ[clone] = 0

                while p != -1 and transitions[p].get(c) == q:
                    transitions[p][c] = clone
                    p = link[p]

                link[q] = clone
                link[cur] = clone

        last = cur

    # Counting sort states by len.
    count = [0] * (n + 1)
    for v in range(size):
        count[length[v]] += 1

    for i in range(1, n + 1):
        count[i] += count[i - 1]

    order = [0] * size
    for v in range(size - 1, -1, -1):
        lv = length[v]
        count[lv] -= 1
        order[count[lv]] = v

    best_len = 0
    best_pos = -1

    # Reverse order gives decreasing length.
    for idx in range(size - 1, 0, -1):
        v = order[idx]

        if occ[v] >= m:
            cur_len = length[v]
            cur_pos = max_end[v] - cur_len + 1

            if cur_len > best_len:
                best_len = cur_len
                best_pos = cur_pos
            elif cur_len == best_len and cur_pos > best_pos:
                best_pos = cur_pos

        parent = link[v]

        if parent >= 0:
            occ[parent] += occ[v]
            if max_end[v] > max_end[parent]:
                max_end[parent] = max_end[v]

    if best_len == 0:
        return "none"

    return f"{best_len} {best_pos}"

def solve():
    out = []

    while True:
        line = input()
        if not line:
            break

        m = int(line)
        if m == 0:
            break

        s = input().strip()
        out.append(solve_case(m, s))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The construction maintains `last`, the state corresponding to the entire prefix processed so far. When a new character is appended, `cur` represents that new longest prefix. The first suffix-link loop adds the new transition to every suffix state that did not previously have it.

The transition conflict has two possibilities. If `len[p] + 1 == len[q]`, the existing state `q` already has exactly the required length, so `cur` can link directly to it. Otherwise, `q` represents too wide a range of substring lengths. The clone splits that range at `len[p] + 1`, after which both `cur` and `q` can use the clone as their suffix-link target.

The clone receives a copy of `q`'s transitions. Its occurrence counter stays zero because cloning changes the automaton structure without adding a new position in the original string. Occurrences are recovered later through suffix-link propagation. This distinction is a common source of incorrect suffix automaton implementations.

The `max_end` array follows the same propagation rule as `occ`. If a state contains an occurrence ending at position `i`, every suffix represented by its suffix-link ancestors also occurs ending at `i`. Processing states from larger `len` to smaller `len` makes a single forward propagation sufficient.

The expression `max_end[v] - length[v] + 1` is the starting position of the longest substring represented by `v` at its rightmost ending position. The indexing is zero-based, matching the required output.

Counting sort is used instead of Python's comparison sort because state lengths are integers between zero and `n`. This keeps the complete algorithm linear. No integer overflow is possible in Python, and the maximum number of states is below `80000` for `n <= 40000`.

## Worked Examples

### Sample 1

The actual sample uses `m = 3` and

`baaaababababbababbab`

The important part of the suffix automaton scan is the state representing `babab`. Its longest represented substring has length five, and its occurrence count is three. Its rightmost ending position is `16`, corresponding to starting position `16 - 5 + 1 = 12`.

| Stage | String represented | Length | Occurrences | Rightmost end | Current answer |
| --- | --- | --- | --- | --- | --- |
| Initial | empty string | 0 | 20 | 19 | `0, -1` |
| Candidate found | `babab` | 5 | 3 | 16 | `5, 12` |
| Later states | longer substrings | >5 | <3 | varies | `5, 12` |
| Final | best valid state | 5 | 3 | 16 | `5, 12` |

The state for `babab` is enough to explain the answer. Its three ending positions correspond to starts `5`, `7`, and `12`, so the rightmost occurrence is exactly position `12`. The fact that the three occurrences overlap is naturally handled because the occurrence count is based on ending positions, not on disjoint intervals. The official sample confirms the result `5 12`.

### Sample 2

The second sample uses the same string but `m = 11`. The most frequent single characters already occur only ten times, so no nonempty substring can occur eleven times. Every longer substring has at most as many occurrences as its first character, so it cannot reach eleven either.

| Stage | Relevant quantity | Value |
| --- | --- | --- |
| Input | Required occurrences `m` | 11 |
| String length | `n` | 20 |
| Maximum count of `a` | 10 |
| Maximum count of `b` | 10 |
| Any substring of length at least 2 | Occurrences | at most 10 |
| Final qualifying state | `occ[v] >= 11` | none |
| Output | Result | `none` |

The suffix automaton still builds exactly as it did for Sample 1 because the string is unchanged. Only the threshold used during the final state scan changes. Since no state has an occurrence count of eleven or more, `best_len` remains zero and the program prints `none`. This is the sample's second output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Suffix automaton construction, counting sort by state length, and suffix-link propagation are all linear for the fixed lowercase alphabet. |
| Space | O(n) | There are at most `2n - 1` states, and the transition structure plus state arrays are linear in size. |

With `n <= 40000`, the automaton has fewer than `80000` states. The algorithm makes only a constant amount of work per state and transition, so it comfortably avoids the quadratic or quartic work of direct substring enumeration. The linear suffix automaton approach is also one of the approaches identified in the SWERC solution material through the closely related suffix-tree formulation.

## Test Cases

The following test harness is intended to be placed after the solution code. It uses the `solve()` function through a redirected standard input and checks complete outputs.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue()

# Provided samples
sample = """\
3
baaaababababbababbab
11
baaaababababbababbab
3
cccccc
0
"""

assert run(sample) == """\
5 12
none
4 2
""", "provided samples"

# Minimum-size input, m = 1.
assert run("""\
1
a
0
""") == "1 0\n", "minimum size"

# Boundary case: m = n, but the characters are not all equal.
assert run("""\
3
abc
0
""") == "none\n", "no substring occurs n times"

# Overlapping occurrences and rightmost tie-breaking.
assert run("""\
2
ababa
0
""") == "3 2\n", "overlapping occurrences"

# Maximum-size all-equal string.
s = "a" * 40000
assert run(f"""\
20000
{s}
0
""") == "20001 19999\n", "maximum size all-equal case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `1 0` | Minimum string length and `m = 1` handling |
| `3 / abc` | `none` | Boundary case where `m = n` but no character repeats enough |
| `2 / ababa` | `3 2` | Overlapping occurrences and rightmost tie-breaking |
| `20000 / a...a` with 40000 characters | `20001 19999` | Maximum input size, high repetition count, and occurrence-position arithmetic |

## Edge Cases

For `m = 1`, the root itself is not considered a candidate because it represents the empty string. Every non-root state has at least one occurrence, and the state corresponding to the complete string has `len = n`. Its rightmost ending position is `n - 1`, so its starting position is zero. For `1` and `abc`, the algorithm reaches `best_len = 3` and `best_pos = 0`, producing `3 0`.

For an impossible repetition threshold, consider `3` and `abc`. Each character has occurrence count one, and every longer substring also occurs only once. After propagation, every non-root state has `occ < 3`, so the answer variables remain `best_len = 0` and `best_pos = -1`. The program prints `none`.

For overlapping occurrences, consider `2` and `ababa`. The substring `aba` ends at positions `2` and `4`, so its occurrence count is two. The state representing its end-position class has `len = 3` and `max_end = 4`. The starting position is `4 - 3 + 1 = 2`, giving `3 2`. No disjointness assumption appears anywhere in the algorithm, so the overlap is handled naturally.

For an all-equal string, consider six copies of `c` with `m = 3`. A substring of length four occurs at starts `0`, `1`, and `2`, while length five occurs only twice. The state for `cccc` has length four, occurrence count three, and rightmost ending position five, so its rightmost start is `5 - 4 + 1 = 2`. The result is `4 2`, matching the sample.

For the maximum-size case, take `40000` copies of `a` and require `20000` occurrences. A substring of length `L` in an all-equal string occurs `40000 - L + 1` times. Requiring at least `20000` occurrences gives `L <= 20001`. The longest valid length is thus `20001`, and its rightmost occurrence starts at `40000 - 20001 = 19999`. The suffix automaton produces exactly `20001 19999`, exercising both the largest allowed input and the rightmost-position calculation.
