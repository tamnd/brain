---
title: "CF 105475C - Word Expansion"
description: "We start with a single string made of lowercase letters. Each letter is not static: it expands into another string according to a fixed substitution table of size 26. If a character is x, it is replaced by the string px."
date: "2026-06-23T02:11:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105475
codeforces_index: "C"
codeforces_contest_name: "XXII Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 105475
solve_time_s: 80
verified: true
draft: false
---

[CF 105475C - Word Expansion](https://codeforces.com/problemset/problem/105475/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a single string made of lowercase letters. Each letter is not static: it expands into another string according to a fixed substitution table of size 26. If a character is `x`, it is replaced by the string `p_x`. One application of the operation replaces every character in the current string simultaneously.

After repeating this transformation `k` times, the string can become extremely large. Instead of constructing it, we are asked a much more specific question: what is the character at position `i` (1-indexed) in the final expanded string?

The key difficulty is that both `k` and `i` can be large. The index can be as large as 10^18, which makes any approach that explicitly builds strings impossible. Even tracking the full string length is infeasible because it can grow exponentially with each transformation step.

A naive approach that fully simulates each expansion would fail quickly. Even if each letter expands to at most 10 characters, after 20 steps the string can already exceed 10^20 in size, and indexing into it would be impossible without construction.

A subtle edge case appears when expansions produce empty or short strings. A careless approach that assumes uniform growth per character or tries to maintain prefix sums without careful propagation of structure would break on cases like a letter mapping to a single character repeatedly, which creates long chains without branching.

For example, if `a -> b`, `b -> c`, `c -> c`, then after many steps the entire string collapses into a single repeated character. A naive expansion-based simulation might still attempt to rebuild full intermediate strings unnecessarily, even though the answer is determined by a single dependency chain.

## Approaches

The central issue is that the transformation defines a directed rewriting system over characters. Each letter becomes a string, and that string defines how indices propagate forward.

A brute-force method directly constructs the full string after each of the `k` transformations. Each step replaces every character by its expansion. If the total length after k steps is N, each transformation costs O(N), and N itself grows multiplicatively. Even under the smallest constraints, this quickly explodes beyond feasibility. The core reason is that we repeatedly recompute entire strings even though the query only needs one position.

The key observation is that we never need the full string. We only need to know how positions map backward through transformations. Instead of expanding forward, we track how an index in the final string originates from earlier strings.

If we know, for each character `c`, the length of its expansion after t steps, we can decide which character contributes the i-th position. Once we identify which character it came from, we subtract prefix offsets and continue recursively for the previous step.

This suggests a reverse simulation: instead of building strings, we maintain a function `len[c][t]` describing how long the expansion of character `c` becomes after `t` steps. Then, to answer a query, we walk from step `k` down to 0, each time selecting the correct child segment.

To compute `len[c][t]`, we use dynamic programming. At step 0, each character has length 1. For transitions, the length of `c` at step t is the sum of lengths of characters in `p_c` at step t-1. Since `k` can be up to 10^4, we compute these values iteratively.

Once lengths are known, answering the query becomes a deterministic descent: at each step, we locate which character in the expansion contains position `i`, then update `i` accordingly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Expansion | Exponential | Exponential | Too slow |
| DP on lengths + backward traversal | O(26 * k * 26 + k) | O(26 * k) | Accepted |

## Algorithm Walkthrough

We split the solution into preprocessing of expansion lengths and then a query traversal.

1. Precompute a table `len[c][t]`, where `len[c][t]` is the length of the string obtained by expanding character `c` exactly `t` times. We initialize `len[c][0] = 1` because at step 0 each letter is itself. This forms the base case of our recursion.
2. For each step `t` from 1 to `k`, compute `len[c][t]` by iterating over the characters in `p_c`. For each character `x` in `p_c`, we add `len[x][t-1]`. This works because one transformation replaces `c` with `p_c`, and each symbol in that string independently expands according to previous step lengths.
3. To answer a query `(s, k, i)`, we first conceptually start at step `k` and position `i` within the expansion of the initial string `s`.
4. We iterate over characters of `s`, treating each as a block whose size is `len[c][k]`. We find the first block where `i` falls. Once identified, we subtract the sizes of earlier blocks and focus on that character. This reduces the problem to finding the answer inside the expansion of a single character.
5. Now we repeatedly simulate the descent of a single character from step `k` to step 0. At step `t`, we look at `p_c` and determine which character’s expansion contains position `i` using precomputed lengths at level `t-1`. We subtract prefix sums until we find the correct child, then continue with that child at step `t-1`.
6. When `t` reaches 0, we have reached a base character, which is the answer.

### Why it works

At every level of recursion, we maintain the invariant that `i` refers to a valid position inside the expansion of a specific character at a specific depth. The DP table guarantees that segment lengths at each step are correct, so prefix subtraction always selects the correct subtree. Since each transformation is a disjoint concatenation of expansions, the position mapping is well-defined and never ambiguous.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    while True:
        line = input().strip()
        if not line:
            return
        parts = line.split()
        if not parts:
            continue

        s = parts[0]
        k = int(parts[1])
        i = int(parts[2])

        p = [input().strip() for _ in range(26)]

        # dp[c][t] = length after t expansions
        dp = [[0] * (k + 1) for _ in range(26)]

        for c in range(26):
            dp[c][0] = 1

        for t in range(1, k + 1):
            for c in range(26):
                total = 0
                for ch in p[c]:
                    total += dp[ord(ch) - 97][t - 1]
                    if total > 10**18:
                        total = 10**18
                dp[c][t] = total

        # find starting character at level k
        cur_i = i
        cur_t = k

        # reduce from initial string s
        for ch in s:
            c = ord(ch) - 97
            if cur_i > dp[c][cur_t]:
                cur_i -= dp[c][cur_t]
            else:
                cur = c
                break

        # descend
        while cur_t > 0:
            for ch in p[cur]:
                nxt = ord(ch) - 97
                if cur_i > dp[nxt][cur_t - 1]:
                    cur_i -= dp[nxt][cur_t - 1]
                else:
                    cur = nxt
                    cur_t -= 1
                    break

        print(chr(cur + 97))

if __name__ == "__main__":
    solve()
```

The first phase builds a DP table where each row corresponds to a letter and each column corresponds to the number of transformations applied. The saturation at 10^18 is a practical safeguard against overflow since we only need comparisons with i, not exact huge values.

The initial loop over `s` collapses the problem from a multi-character string into a single starting character with an adjusted index. The second loop performs the actual inverse traversal of the transformation tree, using prefix subtraction to decide which branch contains the target position.

The critical implementation detail is consistently using the correct depth `cur_t - 1` when inspecting children. Any mismatch between the DP level and traversal level breaks correctness immediately.

## Worked Examples

### Example 1

Input:

```
s = "ab", k = 1, i = 3
```

Assume:

```
a -> "bc"
b -> "a"
```

DP lengths:

| char | len at 1 |
| --- | --- |
| a | 2 |
| b | 1 |

Traversal over `s`:

| step | char | block length | remaining i | chosen |
| --- | --- | --- | --- | --- |
| 1 | a | 2 | 3 -> 1 | skip |
| 2 | b | 1 | 1 | b |

Now descend from `b` at k=1:

`b -> "a"`, so answer is `a`.

This shows how the initial string is treated as concatenated weighted blocks.

### Example 2

Input:

```
s = "a", k = 2, i = 1
```

Assume:

```
a -> "ab"
b -> "c"
c -> "c"
```

DP:

| char | len at 2 |
| --- | --- |
| a | 2 |
| b | 1 |
| c | 1 |

Start at `a`, k=2, i=1:

`a -> "ab"`, so we go to `a` at level 1.

At level 1, `a -> "ab"` again, so we go to first `a` at level 0, yielding `a`.

This trace shows repeated descent preserves correctness across multiple levels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 * k * 26 + | s |
| Space | O(26 * k) | DP table storing expansion lengths |

The constraints allow up to k = 10^4, and the constant factor of 26 is small. The solution comfortably fits within both time and memory limits because all operations are simple integer additions and linear scans over fixed alphabets.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample (as given format)
assert run("""rb 2 16
mqbh
dar
owkk
h
d
qs
dxr
mo
frx
j
bld
efsa
cbyn
c
yg
x
pk
orel
nm
apqf
kho
kmco
h
wnku
w
sqmg
ljj 1 6
vsw
d
q
bx
x
v
rrbl
ptns
fw
qf
mafa
rr
sof
b
n
vqh
fb
a
x
pqc
c
hch
vfrk
l
oz
kpqp
""") == "h\nf"

# custom 1: no expansion
assert run("""a 0 1
abcdefghijklmnopqrstuvwxyz
""") == "a"

# custom 2: simple chain
assert run("""a 2 1
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
""") == "c"

# custom 3: boundary index in concatenation
assert run("""ab 1 2
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
""") == "b"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identity expansion | a | k=0 base correctness |
| full chain depth | c | multi-step propagation |
| boundary in string split | b | correct prefix subtraction |

## Edge Cases

One fragile situation is when the query index falls exactly on the boundary between two expanded characters in the initial string. Suppose `s = "ab"`, with `a` expanding to length 3 and `b` to length 2 at the final step, and `i = 3`. The algorithm first checks `a`, sees that `i` is within its block, and correctly does not subtract past it. If instead `i = 4`, it subtracts the full length of `a` and continues inside `b`. This boundary handling depends entirely on strict `>` comparisons in prefix subtraction.

Another case is deep single-character chains like `a -> b -> c -> c`. Even after large `k`, the DP table stabilizes, and traversal simply follows a deterministic pointer chain. The algorithm never needs to expand strings, only to repeatedly resolve a single index through decreasing levels.

A third case is very large `i`. Since we cap DP values at 10^18, comparisons remain valid. Even if actual expansions exceed that cap, correctness is preserved because we only need to know whether `i` lies inside or outside a segment, not its exact size beyond the threshold.
