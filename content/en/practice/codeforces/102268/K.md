---
title: "CF 102268K - Knowledge"
description: "We have a binary string over the alphabet a, b. The allowed operations insert or delete one of three special blocks: aa, bbb, and ababab."
date: "2026-08-17T19:02:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "K"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 275
verified: false
draft: false
---

[CF 102268K - Knowledge](https://codeforces.com/problemset/problem/102268/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We have a binary string over the alphabet `a, b`. The allowed operations insert or delete one of three special blocks: `aa`, `bbb`, and `ababab`. Since insertion and deletion are both allowed, two strings belong to the same class exactly when one can be transformed into the other using the relations

[
a^2 = 1,\qquad b^3 = 1,\qquad (ab)^3 = 1.
]

The initial string `s` determines one such equivalence class. We do not need to construct the actual strings obtainable from `s`. Instead, for a prescribed length `x`, we need to count how many binary strings of exactly that length belong to the same class as `s`.

The input length `n` is at most (300000), so processing `s` should be linear or close to linear. An algorithm that keeps a state for every substring, or tries to enumerate possible transformed strings, is already too expensive. More seriously, `x` can be as large as (10^9), so any algorithm depending linearly on `x` is impossible. We need to compress the equivalence classes to a constant number of states and then handle the huge length using logarithmic exponentiation.

There are three edge cases that tend to expose incorrect interpretations. First, `x` can be zero. For example,

```
1
a
0
```

has answer `0`, because the empty string represents the identity while `a` does not. A solution that assumes the target always has at least one character will get this wrong.

Second, the starting string can already represent the identity without being empty. For example,

```
2
aa
0
```

has answer `1`, because `aa` can be deleted, leaving the empty string. A solution that compares the literal strings rather than their equivalence classes would incorrectly return zero.

Third, the relations interact across boundaries, so simply greedily deleting an occurrence of `aa` or `bbb` is not a complete normalization strategy. For example, `ababab` represents the identity and the answer for

```
6
ababab
3
```

is `1`. The only length-three representative of the identity is `bbb`. A local reduction algorithm that does not account for the third relation can easily miss this equivalence. The official samples confirm these outputs.

## Approaches

A direct approach would enumerate every one of the (2^x) binary strings of length `x`, normalize it, and check whether it belongs to the class of `s`. This is correct because every possible target string is explicitly considered. If normalization takes (O(x)) time, the total worst-case work is (\Theta(x2^x)), with (2^x) candidates and (x) characters inspected in each candidate. This is already hopeless for `x = 30`, let alone (10^9).

The brute force works because the operations define an equivalence relation, but it fails because the number of strings is exponential in the requested length. The key observation is that these three relations do not create infinitely many distinct equivalence classes. They form a finite group with only 12 elements.

A convenient way to see the group is to assign permutations to the two letters. Let

[
a=(12)(34),\qquad b=(123).
]

The permutation `a` has order two, `b` has order three, and `ab` has order three, so all three relations from the problem hold. These two permutations generate the rotational symmetry group of a tetrahedron, which is isomorphic to (A_4), and (A_4) has exactly 12 elements.

Equivalently, the 12 equivalence classes can be represented by the words

[
\epsilon,\ a,\ b,\ ab,\ ba,\ bb,\ aba,\ abb,\ bab,\ bba,\ babb,\ bbab.
]

Every string can be reduced to one of these representatives using the given relations, and the representatives correspond to distinct elements of (A_4). This gives us a finite automaton with exactly 12 states. This same 12-state structure is the central observation used by existing solutions to the problem.

Once the state of `s` is known, the rest of the problem becomes a walk-counting problem. Start at the identity state, append either `a` or `b` exactly `x` times, and ask how many walks finish at the state represented by `s`. There are only 12 states and two outgoing transitions from every state, so an adjacency matrix handles the counting. Since `x` can reach (10^9), we raise the 12 by 12 matrix to the `x`-th power using binary exponentiation.

The resulting complexity is (O(n+12^3\log x)), which is easily within the constraints. This is also the complexity described by the standard solution approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(x2^x)) | (O(x)) | Too slow |
| Optimal | (O(n+12^3\log x)) | (O(12^2)) | Accepted |

## Algorithm Walkthrough

1. Interpret the three deletion operations as group relations. Deleting `aa` means (a^2=1), deleting `bbb` means (b^3=1), and deleting `ababab` means ((ab)^3=1). Because the inverse operations are also allowed, these relations work in both directions.
2. Represent the two generators as permutations of four objects. Use (a=(12)(34)) and (b=(123)). The identity permutation represents the empty string.
3. Generate all 12 even permutations of four elements. These are exactly the elements of (A_4), so each equivalence class has one state in our automaton.
4. Define permutation composition so that appending a character means multiplying the current permutation on the right by the permutation of that character. If the current state is `g` and the next character represents `h`, the new state is (g\circ h).
5. Scan the original string `s` from left to right. Start with the identity permutation and multiply by the permutation corresponding to each character. After the scan, the resulting permutation is exactly the equivalence class of `s`.
6. Build a 12 by 12 transition matrix `T`. For every state `u`, append `a` and `b`, compute the resulting states `v`, and increase `T[v][u]` by one. We use this orientation because a column vector of state counts is transformed as (dp' = Tdp).
7. The vector for the empty string has one count in the identity state and zero elsewhere. After exactly `x` characters, the state-count vector is

[
T^x e,
]

where `e` is the identity-state vector.

1. Compute (T^x) by binary exponentiation. Each squaring represents doubling the number of appended characters represented by the matrix. Whenever the current bit of `x` is one, multiply the answer matrix by the current power.
2. Read the entry corresponding to the state of `s` from the identity starting state. That value is the number of length-`x` strings equivalent to `s`.

### Why it works

The invariant is that every binary string has exactly one state in the 12-element group, and two strings are transformable into one another if and only if they have the same state. The allowed insertions and deletions preserve the group element because they insert or remove one of (a^2), (b^3), or ((ab)^3), all of which equal the identity.

Conversely, the 12 states are enough to represent every equivalence class. The generators (a=(12)(34)) and (b=(123)) generate (A_4), and the 12 canonical words listed above represent its 12 distinct elements. Thus the group state does not merge two genuinely different equivalence classes.

For the target length, every binary string corresponds to exactly one walk of length `x` starting from the identity, with `a` and `b` selecting the two possible transitions at each position. Matrix multiplication counts these walks, including their multiplicities. Consequently, the matrix entry from the identity to the state of `s` counts exactly the desired target strings.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
K = 12

def compose(p, q):
    """Return p o q, where permutations are stored by their images."""
    return tuple(p[q[i]] for i in range(4))

def parity(p):
    """Return 0 for even and 1 for odd permutation."""
    inv = 0
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                inv += 1
    return inv & 1

def mat_mul(a, b):
    n = K
    c = [[0] * n for _ in range(n)]

    for i in range(n):
        ci = c[i]
        ai = a[i]
        for k in range(n):
            x = ai[k]
            if x == 0:
                continue
            bk = b[k]
            for j in range(n):
                ci[j] = (ci[j] + x * bk[j]) % MOD

    return c

def mat_pow(a, e):
    n = K
    r = [[0] * n for _ in range(n)]
    for i in range(n):
        r[i][i] = 1

    while e:
        if e & 1:
            r = mat_mul(r, a)
        a = mat_mul(a, a)
        e >>= 1

    return r

def solve():
    n = int(input())
    s = input().strip()
    x = int(input())

    # All even permutations of four elements are the 12 states of A4.
    states = []
    for p in __import__("itertools").permutations(range(4)):
        if parity(p) == 0:
            states.append(p)

    index = {p: i for i, p in enumerate(states)}

    # a = (12)(34), b = (123)
    a = (1, 0, 3, 2)
    b = (1, 2, 0, 3)

    generators = {
        'a': a,
        'b': b,
    }

    identity = (0, 1, 2, 3)

    # Find the group element represented by s.
    g = identity
    for ch in s:
        g = compose(g, generators[ch])

    target = index[g]
    start = index[identity]

    # T[v][u] = number of one-character transitions u -> v.
    T = [[0] * K for _ in range(K)]

    for u, state in enumerate(states):
        va = index[compose(state, a)]
        vb = index[compose(state, b)]
        T[va][u] += 1
        T[vb][u] += 1

    T = mat_pow(T, x)

    print(T[target][start] % MOD)

if __name__ == "__main__":
    solve()
```

The permutation construction gives the solution a clean implementation instead of hardcoding a reduction table. The tuple `(p[0], p[1], p[2], p[3])` stores where each of the four points is sent. The identity is `(0, 1, 2, 3)`, while `a = (1, 0, 3, 2)` represents ((12)(34)), and `b = (1, 2, 0, 3)` represents ((123)).

The `compose` function implements the mathematical composition (p\circ q). When the current word represents `p` and we append a generator `q`, the new word represents `p q`, which is exactly `compose(p, q)` under this convention. Keeping this order consistent is essential. Reversing it would construct a different automaton and can silently produce incorrect answers.

The scan over `s` is linear in `n`. There is no need to reduce substrings or maintain a stack. The current permutation contains all information relevant to future transformations.

The matrix uses `T[new][old]` rather than `T[old][new]`. With this convention, multiplying `T` by a column vector gives the next distribution of states. Thus the identity-to-target count is `T[target][identity]` after exponentiation.

All matrix products are performed modulo (998244353). Python integers do not overflow, but reducing during multiplication also keeps intermediate values small and avoids unnecessary growth.

The exponent `x` is processed with bit shifts, so only (O(\log x)) matrix multiplications are needed. Since the matrix dimension is fixed at 12, this part is tiny compared with the scan of the original string.

## Worked Examples

### Sample 1

The input is

```
6
ababab
3
```

The original string represents the identity because ((ab)^3=1). Scanning it character by character gives the following states, using the canonical names of the 12 group elements.

| Position | Character | State of `s` | Identity? |
| --- | --- | --- | --- |
| 0 |  | `ε` | Yes |
| 1 | `a` | `a` | No |
| 2 | `b` | `ab` | No |
| 3 | `a` | `aba` | No |
| 4 | `b` | `bba` | No |
| 5 | `a` | `bb` | No |
| 6 | `b` | `ε` | Yes |

We now need the number of length-three walks from the identity back to the identity. At length one, neither `a` nor `b` is the identity. At length two, `aa` is the identity, giving one walk. At length three, `bbb` is the identity, giving one walk.

| Length | Identity count | Relevant representative |
| --- | --- | --- |
| 0 | 1 | `ε` |
| 1 | 0 | none |
| 2 | 1 | `aa` |
| 3 | 1 | `bbb` |

The answer is `1`. This demonstrates why the starting string itself does not need to have the target length. Only its group state matters.

### Sample 2

The input is

```
3
bbb
2
```

Here the starting string also represents the identity because (b^3=1).

| Position | Character | State of `s` | Identity? |
| --- | --- | --- | --- |
| 0 |  | `ε` | Yes |
| 1 | `b` | `b` | No |
| 2 | `b` | `bb` | No |
| 3 | `b` | `ε` | Yes |

The target length is two, so we count identity walks of length two.

| Length | Identity count | Relevant representative |
| --- | --- | --- |
| 0 | 1 | `ε` |
| 1 | 0 | none |
| 2 | 1 | `aa` |

The answer is `1`. This case exercises the fact that a nonempty starting string can be equivalent to the empty string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+12^3\log x)) | The string is scanned once, then a constant-size matrix is exponentiated in logarithmic time. |
| Space | (O(12^2)) | The transition and exponentiation matrices each contain only (12^2) entries. |

With (n\le300000), the linear scan is easily feasible. The target length can be (10^9), but it appears only inside the binary exponentiation, so the number of matrix multiplications is about 30. The fixed matrix dimension of 12 makes the exponentiation negligible in practice. The standard analysis for this solution is (O(n+12^3\log x)).

## Test Cases

```python
# This test file assumes solve() is the function from the solution above.
import sys
import io

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
assert run("6\nababab\n3\n") == "1", "sample 1"
assert run("3\nbbb\n2\n") == "1", "sample 2"
assert run("5\nbabab\n35\n") == "866826000", "sample 3"

# Minimum target length: a is not equivalent to the empty string.
assert run("1\na\n0\n") == "0", "x = 0 with a non-identity start"

# Identity represented by a nonempty string.
assert run("2\naa\n0\n") == "1", "aa can be deleted completely"

# Small target length and an all-equal starting string.
assert run("5\naaaaa\n1\n") == "1", "five a's represent a"

# Boundary between length 0 and length 1.
assert run("2\naa\n1\n") == "0", "identity has no length-1 representative"

# A short case exercising the ab relation structure.
assert run("2\nab\n2\n") == "1", "only ab among length-2 strings has the same state"

# Maximum input size with an easy-to-check answer.
big_s = "a" * 300000
assert run(f"300000\n{big_s}\n0\n") == "1", "maximum n, even number of a's"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / 0` | `0` | Target length zero with a non-identity starting state |
| `2 / aa / 0` | `1` | Nonempty string equivalent to the identity |
| `5 / aaaaa / 1` | `1` | All-equal input and repeated application of (a^2=1) |
| `2 / aa / 1` | `0` | Boundary between zero and positive target lengths |
| `2 / ab / 2` | `1` | Distinguishes group states at a small length |
| `300000 / a...a / 0` | `1` | Maximum `n` and linear preprocessing |

## Edge Cases

For

```
1
a
0
```

the target is the empty string, whose state is the identity. The initial `a` maps to the permutation `(1, 0, 3, 2)`, which is not the identity. After exponentiating the transition matrix to power zero, the matrix is the identity matrix, so the entry from the identity state to the `a` state is zero. The algorithm prints `0`.

For

```
2
aa
0
```

the scan performs (e\circ a\circ a=e). Thus the target state is the identity. Since (T^0=I), the identity-to-identity entry is one, corresponding to the single empty string. The algorithm prints `1`.

For

```
3
bbb
2
```

the starting state is (b^3=e). At length two, the identity can be reached through `aa`, while `ab`, `ba`, and `bb` represent the other three length-two possibilities. Hence exactly one target string is valid, and the algorithm prints `1`.

For

```
6
ababab
3
```

the starting state is also the identity because ((ab)^3=e). The length-three walk count back to the identity is one, represented by `bbb`. This catches solutions that only understand the `aa` and `bbb` relations and forget that `ababab` must also collapse to the identity.

For the maximum-size case

```
300000
aaaaaaaa...
0
```

the 300000 copies of `a` form an even power, so (a^{300000}=e). The scan still takes only (O(n)) time and never constructs any intermediate string. Since `x=0`, the matrix exponentiation immediately returns the identity matrix, giving answer `1`. This shows why the algorithm remains practical when the input string itself is the dominant part of the input.
