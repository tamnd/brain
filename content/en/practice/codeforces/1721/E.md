---
title: "CF 1721E - Prefix Function Queries"
description: "We are given a fixed reference string and then asked to process many short query strings. For each query, we temporarily append the query string to the reference, compute the prefix function on the resulting concatenation, and output only the prefix function values corresponding…"
date: "2026-06-15T01:18:56+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "hashing", "string-suffix-structures", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1721
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 134 (Rated for Div. 2)"
rating: 2200
weight: 1721
solve_time_s: 184
verified: false
draft: false
---

[CF 1721E - Prefix Function Queries](https://codeforces.com/problemset/problem/1721/E)

**Rating:** 2200  
**Tags:** dfs and similar, dp, hashing, string suffix structures, strings, trees  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed reference string and then asked to process many short query strings. For each query, we temporarily append the query string to the reference, compute the prefix function on the resulting concatenation, and output only the prefix function values corresponding to the appended part. After each query, the state resets back to the original reference string.

The key difficulty is that the prefix function on position $i$ depends on the longest border of the prefix ending at $i$, which in turn depends on earlier prefix function values and character comparisons. If we recompute everything from scratch for every query, we would repeatedly scan the long base string of length up to $10^6$, which is infeasible given up to $10^5$ queries.

The constraints imply that any solution must treat the base string as preprocessed structure and handle each query in time proportional only to the query length. Since each query string has length at most 10, the total additional work per query must be $O(|t|)$, otherwise the solution will exceed limits.

A naive implementation would recompute the prefix function for $s+t$ in full for each query. That alone already means up to $10^6 + 10$ work per query, repeated $10^5$ times, which is far beyond acceptable.

A subtler failure case appears if one tries to recompute only the suffix part but still repeatedly compares against the full prefix of $s$ without maintaining a persistent automaton or compressed transition structure. The prefix function can “jump back” many times in one step, so per-character simulation against the full string can degrade to linear behavior in the worst case.

For example, if $s = aaaa\ldots a$ and $t = aaaaa$, every prefix-function step repeatedly falls back through long chains of matches. A naive loop that scans backward each time still becomes quadratic in the worst case over all queries.

## Approaches

The brute-force idea is straightforward: for each query, form $s+t$, compute the prefix function using the standard linear KMP procedure, and output the last $|t|$ values. This is correct because the prefix function is defined purely on the concatenated string and does not depend on query structure.

The issue is cost. Each computation is $O(|s|+|t|)$, so across $q$ queries this becomes $O(q|s|)$, which is about $10^{11}$ operations in the worst case. This cannot pass.

The key observation is that the prefix function computation is equivalent to walking in an automaton defined by the prefix-function failure links. If we interpret each prefix length as a state, then each new character causes a transition: we repeatedly follow failure links until we find a state that can be extended by the current character.

This structure suggests preprocessing: we build, for every state $v$ and every letter $c$, the next prefix-function state if we are currently in state $v$ and read $c$. This is exactly the KMP automaton. Once built, each query becomes a simple simulation over this automaton starting from the state corresponding to the full string $s$.

We first compute the prefix function for $s$. This gives us the starting state $cur = p[|s|]$. Then we precompute transitions using the failure links. After that, each character in a query is processed in $O(1)$, producing the next prefix state immediately, and we output it.

This reduces the problem to linear preprocessing plus total linear work over all query characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q(n+m))$ | $O(n)$ | Too slow |
| Optimal (KMP automaton) | (O(n + \sum | t | )) |

## Algorithm Walkthrough

1. Compute the prefix function for the base string $s$. This gives us failure links that allow us to jump to the longest proper prefix which is also a suffix at every position.
2. Treat each prefix length $v$ as a state in an automaton. From state $v$, we want to know where we end up if we append a character $c$.
3. Precompute a transition table `nxt[v][c]` for all states $v$ and letters $c$. To compute it correctly, we reuse previously computed transitions via failure links instead of recomputing matches from scratch.
4. Set the initial state for queries as `cur = p[len(s)]`, which represents the longest prefix-suffix match after reading the whole base string.
5. For each query string $t$, process characters one by one:

1. Update `cur = nxt[cur][t[i]]`.
2. Output `cur` as the prefix function value at that position in the concatenated string.
6. After finishing a query, do nothing to reset, since `cur` already represents the state after $s$, and each query is independent.

The correctness hinges on the fact that the automaton transition encodes exactly the prefix-function update rule: we always move to the longest prefix that can be extended by the next character, and failure links ensure we skip invalid matches efficiently.

### Why it works

At any point, the variable `cur` represents the length of the longest prefix of $s + t_{processed}$ that is also a suffix of that string. This is exactly the definition of the prefix function state. The transition rule maintains this invariant because every update either extends the current matched prefix or falls back along failure links until a valid extension is found. Since failure links always preserve the border property, no valid candidate is skipped, and the resulting state is always maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_pi(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def build_automaton(s, pi):
    n = len(s)
    nxt = [[0] * 26 for _ in range(n + 1)]

    for v in range(n + 1):
        for c in range(26):
            if v < n and ord(s[v]) == ord('a') + c:
                nxt[v][c] = v + 1
            else:
                if v == 0:
                    nxt[v][c] = 0
                else:
                    nxt[v][c] = nxt[pi[v - 1]][c]
    return nxt

def solve():
    s = input().strip()
    q = int(input())
    pi = build_pi(s)
    nxt = build_automaton(s, pi)

    cur = 0
    for ch in s:
        cur = nxt[cur][ord(ch) - 97]

    out = []
    for _ in range(q):
        t = input().strip()
        ans = []
        for ch in t:
            cur = nxt[cur][ord(ch) - 97]
            ans.append(str(cur))
        out.append(" ".join(ans))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first builds the prefix function of the base string, then constructs the full transition table of the KMP automaton. Each state corresponds to a prefix length, and transitions encode the next possible border length after reading a character.

A subtle point is the construction of `nxt`. When a character does not match the expected next character in the prefix, we do not restart from zero immediately. Instead, we follow the failure link `pi[v-1]`, which represents the next best border candidate. This recursion ensures correctness without rechecking characters.

Another detail is the initialization of `cur` by replaying the base string through the automaton. This guarantees consistency with the prefix-function state after processing $s$, avoiding any mismatch between preprocessing and query simulation.

## Worked Examples

Consider the sample:

Input string $s = "aba"$, and query $t = "caba"$.

We track `cur` over time.

| Step | Character | Previous cur | Action | New cur |
| --- | --- | --- | --- | --- |
| 1 | c | 0 | no match at root | 0 |
| 2 | a | 0 | match 'a' | 1 |
| 3 | b | 1 | extend | 2 |
| 4 | a | 2 | extend | 3 |

Output is `0 1 2 3`.

This shows how the automaton naturally tracks growing borders.

Now consider a repetitive case: $s = "aaaa"$, $t = "aaaa"$.

| Step | Char | cur before | behavior | cur after |
| --- | --- | --- | --- | --- |
| 1 | a | 4 | extend match | 5 |
| 2 | a | 5 | extend match | 6 |
| 3 | a | 6 | extend match | 7 |
| 4 | a | 7 | extend match | 8 |

Every step increases the border length, which demonstrates that the automaton handles long repeated matches without backtracking character-by-character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n \cdot 26 + \sum | t |
| Space | $O(n \cdot 26)$ | transition table for all prefix states |

The preprocessing cost is linear in the base string, and each query contributes only its own length. Since total query length is at most $10^6$, the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = sys.stdin.readline().strip()
    q = int(sys.stdin.readline())

    def build_pi(s):
        n = len(s)
        pi = [0]*n
        for i in range(1,n):
            j = pi[i-1]
            while j>0 and s[i]!=s[j]:
                j = pi[j-1]
            if s[i]==s[j]:
                j+=1
            pi[i]=j
        return pi

    def build_automaton(s, pi):
        n=len(s)
        nxt=[[0]*26 for _ in range(n+1)]
        for v in range(n+1):
            for c in range(26):
                if v<n and ord(s[v])==ord('a')+c:
                    nxt[v][c]=v+1
                else:
                    nxt[v][c]=0 if v==0 else nxt[pi[v-1]][c]
        return nxt

    pi = build_pi(s)
    nxt = build_automaton(s, pi)

    cur=0
    for ch in s:
        cur=nxt[cur][ord(ch)-97]

    out=[]
    for _ in range(q):
        t=sys.stdin.readline().strip()
        res=[]
        for ch in t:
            cur=nxt[cur][ord(ch)-97]
            res.append(str(cur))
        out.append(" ".join(res))
    return "\n".join(out)

# provided sample
assert run("""aba
6
caba
aba
bababa
aaaa
b
forces
""") == """0 1 2 3
1 2 3
2 3 4 5 6 7
1 1 1 1
2
0 0 0 0 0 0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single repetition | correct border growth | repeated characters |
| alternating pattern | correct fallback transitions | failure link usage |
| max length query | no overhead per query | linear per character |

## Edge Cases

One edge case is when the query character immediately breaks all existing matches. For example, if $s = "aaaa"$ and the query starts with $b$, the automaton should jump directly to state 0 and stay there. The transition table ensures this because all mismatch paths eventually reach the root state.

Another edge case is when the query continuously extends the match beyond the length of the original string. If $s = "abc"$ and $t = "abcabc"$, the automaton must correctly reuse earlier prefixes as new borders. The failure link chain guarantees that after reaching full match length, further matches continue from the correct border rather than restarting incorrectly.

A final edge case is minimal input where $s$ has length 1. In this case, all transitions either go to state 1 on matching character or state 0 otherwise. The automaton degenerates correctly into a two-state machine, and the logic remains consistent with the general case.
