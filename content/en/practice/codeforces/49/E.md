---
title: "CF 49E - Common ancestor"
description: "Each DNA string evolves by repeatedly applying rules of the form a - bc. One character is replaced by exactly two characters, and this operation can be repeated any number of times. Starting from some ancestor string, evolution only increases the length."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 49
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 46 (Div. 2)"
rating: 2300
weight: 49
solve_time_s: 121
verified: true
draft: false
---

[CF 49E - Common ancestor](https://codeforces.com/problemset/problem/49/E)

**Rating:** 2300  
**Tags:** dp  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Each DNA string evolves by repeatedly applying rules of the form `a -> bc`. One character is replaced by exactly two characters, and this operation can be repeated any number of times. Starting from some ancestor string, evolution only increases the length.

We are given two final DNA strings, and we want to know whether they could both originate from the same ancestor. If they can, we must find the minimum possible length of such an ancestor.

The crucial observation is that evolution acts independently on each character of the ancestor. If an ancestor string is:

```
x1 x2 x3 ...
```

then each character expands into some substring, and the concatenation of all expansions produces the final DNA.

The input strings have length at most 50, and there are at most 50 production rules. That is small enough for cubic or quartic dynamic programming, but far too large for brute force generation of all reachable strings. Even a single character can generate exponentially many different strings because rules may branch recursively:

```
c -> cc
```

already creates infinitely many reachable strings.

The alphabet size is only 26, which is extremely important. Any DP indexed by characters is cheap.

A subtle edge case appears when no substitutions exist at all.

Example:

```
ab
ab
0
```

The answer is `2`, because the ancestor can simply be `"ab"` itself. A careless solution that assumes every character must be expanded at least once would incorrectly reject this case.

Another tricky case is recursive productions.

Example:

```
a
aaaa
1
a->aa
```

The correct answer is `1`. One ancestor character can repeatedly expand into the whole target string. A naive BFS over generated strings may never terminate because the grammar is cyclic.

Another important corner case is when the optimal ancestor is longer than one character even though both strings are individually derivable from a single symbol.

Example:

```
ab
ba
2
x->ab
x->ba
```

The answer is `2`, not `1`. No single symbol can generate both strings simultaneously. The shortest common ancestor is `"ab"` itself.

The final subtlety is alignment. Different ancestor characters may expand into substrings of different lengths.

Example:

```
abba
baab
2
x->ab
x->ba
```

The optimal split is not character-by-character. A greedy matching approach fails because the same partition must work for both strings simultaneously.

## Approaches

The brute-force idea is straightforward. For every possible ancestor string, generate all strings reachable from it and check whether both target strings appear.

This is theoretically correct because the evolution process is completely defined by the substitution rules. The problem is that the reachable state space is infinite whenever cycles exist. Even without cycles, the number of generated strings grows exponentially with the number of expansion steps. With target lengths up to 50, brute force becomes hopeless almost immediately.

A better perspective comes from reading the rules backwards.

A rule:

```
a -> bc
```

means that whenever we see adjacent substrings generated from `b` and `c`, they together could have originated from `a`.

This is exactly context-free grammar parsing. Every character is a nonterminal, and each rule combines two symbols into one parent symbol.

Suppose we define:

```
can[c][l][r]
```

to mean that character `c` can generate substring `s[l:r]`.

Then we can compute this with interval DP, identical to CYK parsing. A single character trivially generates itself, and larger intervals are built by splitting them into two smaller intervals and applying grammar rules.

Once we know, for every substring of `s1` and `s2`, which characters can generate it, the original problem becomes another DP.

If some ancestor character `x` can generate substring `s1[l1:r1]` and also substring `s2[l2:r2]`, then one ancestor position can explain both pieces simultaneously.

Now define:

```
dp[i][j]
```

as the minimum ancestor length needed to generate prefixes:

```
s1[:i], s2[:j]
```

We try every pair of ending substrings and check whether there exists a common generating character. If yes, we extend the decomposition by one ancestor character.

This transforms the problem from infinite search into polynomial dynamic programming.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / Infinite | Exponential | Too slow |
| Optimal | O(26 × n³ + | s1 | ² × |

Here `n` is at most 50.

## Algorithm Walkthrough

1. Parse all substitution rules.

For every rule `a -> bc`, store that `a` can combine results from `b` and `c`.
2. Build interval DP for the first string.

Define:

```
can1[ch][l][r]
```

which is true if character `ch` can generate substring `s1[l:r]`.

For length `1`, only the matching character is possible.
3. Expand intervals in increasing order of length.

For every interval `[l, r)`, try every split point `m`.

If some rule:

```
a -> bc
```

satisfies:

```
can1[b][l][m] and can1[c][m][r]
```

then:

```
can1[a][l][r] = True
```

This works because every derivation tree for a nontrivial substring must split into two child derivations at the root rule.
4. Repeat the same DP for the second string.

We now know every character capable of generating every substring in both strings.
5. Define the main DP.

Let:

```
dp[i][j]
```

be the minimum ancestor length needed to generate:

```
s1[:i] and s2[:j]
```

Initialize:

```
dp[0][0] = 0
```
6. Transition by matching one ancestor character.

For every previous state `(i, j)`, try all substring endings:

```
s1[i:ni], s2[j:nj]
```

If there exists a character `c` such that:

```
can1[c][i][ni] and can2[c][j][nj]
```

then one ancestor symbol can generate both substrings, so:

```
dp[ni][nj] = min(dp[ni][nj], dp[i][j] + 1)
```
7. The answer is `dp[len(s1)][len(s2)]`.

If unreachable, print `-1`.

### Why it works

The interval DP computes exactly the set of substrings derivable from each character. This follows inductively from the grammar structure. Length-1 substrings are correct by definition, and every larger derivation must apply one production at the root and split into two smaller derivations.

The second DP partitions both strings into corresponding pieces. Each piece pair is generated from the same ancestor character. Concatenating these ancestor characters forms a valid common ancestor string.

Every valid ancestor induces such a partition, and every partition constructed by the DP corresponds to a valid ancestor. Because transitions add exactly one ancestor character, the DP minimizes ancestor length correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

def build_can(s, rules):
    n = len(s)

    can = [[[-1] * (n + 1) for _ in range(n)] for _ in range(26)]

    for i, ch in enumerate(s):
        can[ord(ch) - ord('a')][i][i + 1] = 1

    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length

            for m in range(l + 1, r):
                for a, b, c in rules:
                    if can[b][l][m] == 1 and can[c][m][r] == 1:
                        can[a][l][r] = 1

    return can

def solve():
    s1 = input().strip()
    s2 = input().strip()

    n = int(input())

    rules = []

    for _ in range(n):
        line = input().strip()

        a = ord(line[0]) - ord('a')
        b = ord(line[3]) - ord('a')
        c = ord(line[4]) - ord('a')

        rules.append((a, b, c))

    can1 = build_can(s1, rules)
    can2 = build_can(s2, rules)

    n1 = len(s1)
    n2 = len(s2)

    dp = [[INF] * (n2 + 1) for _ in range(n1 + 1)]
    dp[0][0] = 0

    for i in range(n1 + 1):
        for j in range(n2 + 1):
            if dp[i][j] == INF:
                continue

            for ni in range(i + 1, n1 + 1):
                for nj in range(j + 1, n2 + 1):

                    ok = False

                    for ch in range(26):
                        if can1[ch][i][ni] == 1 and can2[ch][j][nj] == 1:
                            ok = True
                            break

                    if ok:
                        dp[ni][nj] = min(dp[ni][nj], dp[i][j] + 1)

    ans = dp[n1][n2]

    print(-1 if ans == INF else ans)

solve()
```

The `build_can` function performs the grammar parsing DP. Each state stores whether a character can derive a substring. The intervals are processed in increasing length order because larger derivations depend on smaller intervals.

The representation:

```
can[ch][l][r]
```

is slightly unusual because the right endpoint is exclusive. This avoids many off-by-one mistakes. The substring is always:

```
s[l:r]
```

exactly like Python slicing.

The main DP treats the strings as being partitioned into synchronized chunks. Every transition checks whether one character can derive both chosen substrings.

The nested loops may look expensive, but the limits are tiny. At most:

```
51 × 51 × 51 × 51 × 26
```

checks occur, which easily fits in time.

One subtle implementation detail is that we never require derivation trees to have the same shape. We only require that some common character can generate both substrings independently. The interval DPs already encapsulate all possible derivations.

## Worked Examples

### Example 1

Input:

```
ababa
aba
2
c->ba
c->cc
```

The only useful production is:

```
c -> ba
```

The second rule allows repeated expansion.

The interval DP discovers:

| String | Substring | Generating character |
| --- | --- | --- |
| ababa | ba | c |
| aba | ba | c |

Now the main DP proceeds.

| State | Chosen substrings | Common char | New cost |
| --- | --- | --- | --- |
| (0,0) | a / a | a | 1 |
| (1,1) | ba / ba | c | 2 |
| (3,3) | ba / empty | impossible | - |

The optimal decomposition is:

```
a + c
```

whose length is `2`.

This example demonstrates recursive generation. The character `c` does not directly appear in either final string, but repeated reverse parsing still detects it.

### Example 2

Input:

```
aaaa
aa
1
a->aa
```

Interval parsing finds:

| Substring | Can be generated by |
| --- | --- |
| a | a |
| aa | a |
| aaaa | a |

The recursive rule lets one `a` expand arbitrarily many times.

The main DP becomes:

| State | Selected pieces | Common char | Cost |
| --- | --- | --- | --- |
| (0,0) | aaaa / aa | a | 1 |

So the answer is `1`.

This confirms that derivation depth does not matter. A single ancestor character may generate very different substring lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 × n³ + n⁴ × 26) | Interval parsing plus pairwise substring DP |
| Space | O(26 × n²) | Reachability tables for substrings |

With `n ≤ 50`, the worst-case number of operations is comfortably below the limit. The memory usage is also tiny because the alphabet size is fixed at 26.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

INF = 10**9

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def build_can(s, rules):
        n = len(s)

        can = [[[-1] * (n + 1) for _ in range(n)] for _ in range(26)]

        for i, ch in enumerate(s):
            can[ord(ch) - ord('a')][i][i + 1] = 1

        for length in range(2, n + 1):
            for l in range(n - length + 1):
                r = l + length

                for m in range(l + 1, r):
                    for a, b, c in rules:
                        if can[b][l][m] == 1 and can[c][m][r] == 1:
                            can[a][l][r] = 1

        return can

    s1 = input().strip()
    s2 = input().strip()

    n = int(input())

    rules = []

    for _ in range(n):
        line = input().strip()

        a = ord(line[0]) - ord('a')
        b = ord(line[3]) - ord('a')
        c = ord(line[4]) - ord('a')

        rules.append((a, b, c))

    can1 = build_can(s1, rules)
    can2 = build_can(s2, rules)

    n1 = len(s1)
    n2 = len(s2)

    dp = [[INF] * (n2 + 1) for _ in range(n1 + 1)]
    dp[0][0] = 0

    for i in range(n1 + 1):
        for j in range(n2 + 1):
            if dp[i][j] == INF:
                continue

            for ni in range(i + 1, n1 + 1):
                for nj in range(j + 1, n2 + 1):

                    ok = False

                    for ch in range(26):
                        if can1[ch][i][ni] == 1 and can2[ch][j][nj] == 1:
                            ok = True
                            break

                    if ok:
                        dp[ni][nj] = min(dp[ni][nj], dp[i][j] + 1)

    ans = dp[n1][n2]

    return str(-1 if ans == INF else ans)

# provided sample
assert run(
"""ababa
aba
2
c->ba
c->cc
"""
) == "2"

# identical strings, no rules
assert run(
"""abc
abc
0
"""
) == "3"

# recursive expansion
assert run(
"""aaaa
aa
1
a->aa
"""
) == "1"

# impossible case
assert run(
"""ab
cd
0
"""
) == "-1"

# single-character ancestor expands differently
assert run(
"""aaaa
aaaaaaaa
1
a->aa
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical strings with no rules | 3 | Base case without substitutions |
| recursive `a->aa` | 1 | Infinite derivation chains |
| completely different strings | -1 | Impossible reconstruction |
| large recursive expansion | 1 | Different output lengths from same ancestor |

## Edge Cases

Consider the case with no substitutions.

Input:

```
ab
ab
0
```

The interval DP only marks single-character substrings. No larger substring can be generated by one symbol.

The main DP partitions both strings into:

```
a + b
```

so the answer becomes `2`.

This correctly models that unchanged characters are allowed. Evolution may perform zero operations.

Now consider recursive growth.

Input:

```
aaaa
aa
1
a->aa
```

The interval DP first marks all single `a` substrings. Then length-2 substrings become derivable from `a`. Combining those again makes length-4 substrings derivable from `a`.

The algorithm never explicitly simulates expansion depth. It only tracks derivability of substrings, so cycles are harmless.

Finally, consider incompatible derivations.

Input:

```
ab
ba
2
x->ab
x->ba
```

The interval DP discovers:

```
x generates ab
x generates ba
```

but there is no single substring pair covering both entire strings simultaneously with the same character.

The main DP instead decomposes into:

```
a + b
```

giving answer `2`.

This shows why synchronized partitioning is necessary. Matching derivability independently for the two strings is not sufficient.
