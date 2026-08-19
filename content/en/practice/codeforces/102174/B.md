---
title: "CF 102174B - \u70bc\u91d1\u672f"
description: "We have (m) existing materials, each represented by a lowercase string (si). A new material is acceptable if its string has exactly length (n), but it must not occur as a contiguous substring of any existing (si)."
date: "2026-08-19T15:18:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "B"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 138
verified: true
draft: false
---

[CF 102174B - \u70bc\u91d1\u672f](https://codeforces.com/problemset/problem/102174/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (m) existing materials, each represented by a lowercase string (s_i). A new material is acceptable if its string has exactly length (n), but it must not occur as a contiguous substring of any existing (s_i). We only need to output one such string, and the statement guarantees that one exists.

The useful way to look at the problem is to forget the chemistry terminology and ask a pure string question: among all (26^n) lowercase strings of length (n), find one that is absent from the collection of all length-(n) substrings of the input strings.

Let

[
S=\sum_i |s_i|.
]

We have (S\le 3\times 10^5), while (n) can be as large as (10^5). This immediately rules out algorithms depending on (26^n), because even (26^{10}) is already far beyond anything we can enumerate. It also rules out checking every candidate against every input string directly. The total input itself is only a few hundred thousand characters, so the intended solution should process it roughly linearly.

There is a particularly useful counting observation. A string (s_i) contains at most (|s_i|-n+1) different starting positions for length-(n) substrings, and hence the total number of distinct forbidden strings is at most

[
\sum_i \max(0, |s_i|-n+1)\le S.
]

So although there are (26^n) possible answers, at most (3\times10^5) of them can actually be forbidden. We only need a way to enumerate a small number of candidates and test membership quickly.

One edge case is when every existing string is shorter than (n). For example,

```
3 2
a
bc
```

There is no length-3 substring anywhere, so `aaa` is already a valid answer. A careless implementation that assumes every input string contributes at least one window could produce incorrect loop bounds or an empty candidate set.

Another edge case occurs when the first candidate is present but the next one is not. For example,

```
3 1
aaaa
```

The string `aaa` occurs, but `aab` does not. The correct output can be `aab`. An implementation that only checks repeated-character candidates such as `aaa`, `bbb`, and so on would miss valid answers.

A third case is (n=1). For example,

```
1 25
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
```

Every one-letter string except `z` is forbidden, so `z` is the answer. The candidate-generation code must work when the string consists of only one position.

## Approaches

The direct brute-force approach is conceptually simple. Enumerate every one of the (26^n) lowercase strings of length (n), and for each candidate check whether it occurs in any input string. If we use straightforward substring matching, checking one candidate can take (O(Sn)) time in the worst case, giving

[
O(26^nSn).
]

Even if substring membership were reduced to (O(1)) using a perfect lookup structure, merely enumerating (26^n) candidates is already impossible for large (n). The brute force is correct because it examines the complete answer space, but the answer space is exponentially larger than the input.

The key observation is that the input can forbid only a linear number of length-(n) strings. Across all input strings there are at most (S) length-(n) windows. Consequently, after examining at most (S+1) distinct candidates, at least one candidate must be absent.

This changes the problem completely. We do not need to understand all (26^n) strings. We can enumerate candidates in lexicographic order and stop as soon as we find one whose fingerprint does not belong to the set of fingerprints of forbidden substrings.

A rolling polynomial hash lets us calculate the fingerprint of every length-(n) window in (O(1)) amortized time per window. We store all those fingerprints in a hash set. We then enumerate candidate strings beginning with `aaa...a`, followed by `aaa...b`, and so on. The candidate can be maintained as a base-26 counter, and its hash can be updated according to the positions that change. Across (K) consecutive candidates, the total number of changed trailing positions is (O(K)), so candidate generation is also linear in the number of candidates.

Hashing introduces the usual possibility of collisions. We use a large prime modulus (2^{61}-1) and choose the base randomly. A collision can make a forbidden candidate look forbidden as well, so it can only delay the search, not cause us to output a string that is actually present. With a randomized 61-bit polynomial hash, the probability of enough collisions to affect the intended complexity is negligible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(26^nSn)) | (O(n)) | Too slow |
| Rolling Hash + candidate enumeration | Expected (O(S+n)) | (O(S+n)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and all existing strings, and choose a random polynomial-hash base. We use the prime modulus (P=2^{61}-1), which gives a very large hash space while keeping Python integer arithmetic manageable.
2. Precompute (B^n\bmod P). This is the factor needed to remove the oldest character when a length-(n) rolling window moves one position to the right.
3. Scan every input string with a rolling window of length (n). If the string is shorter than (n), it contributes no forbidden candidate. Otherwise, calculate the hash of every length-(n) window and insert it into a set.
4. Initialize the candidate to `a` repeated (n) times. Its polynomial hash is computed from the fact that every character has value (1). This is the lexicographically smallest possible length-(n) string.
5. Check whether the candidate hash is present in the forbidden-hash set. If it is absent, output the candidate immediately. A candidate that occurs in an input string must have exactly the same hash as one of the stored windows, so a missing hash certifies that the candidate is absent.
6. If the candidate is forbidden, increment it as a base-26 number. Starting from the last position, every trailing `z` becomes `a`, and the first non-`z` character is increased by one. For every changed position, update the candidate hash by adding the change multiplied by the appropriate power of the base.
7. Repeat the membership check and increment until a missing hash is found. There cannot be more than (S) distinct forbidden strings, so after at most (S+1) distinct candidates, a valid answer must appear, ignoring the negligible probability of hash collisions.

Why it works: the forbidden-hash set contains the fingerprint of every actual length-(n) substring of every existing material. The candidate enumeration visits distinct length-(n) strings in lexicographic order. Whenever its hash is absent from the set, the candidate cannot equal any existing length-(n) substring, so it is a valid new material. Since the input can contain at most (S) length-(n) windows in total, it cannot forbid more than (S) distinct candidates. Thus one of the first (S+1) candidates must be valid.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

MOD = (1 << 61) - 1

def solve():
    n, m = map(int, input().split())

    # Randomized base makes adversarial hash collisions extremely unlikely.
    base = random.randrange(256, MOD - 1)

    pow_n = pow(base, n, MOD)

    forbidden = set()

    for _ in range(m):
        s = input().strip()
        if len(s) < n:
            continue

        h = 0

        # Hash of the first window.
        for i in range(n):
            h = (h * base + (ord(s[i]) - 96)) % MOD
        forbidden.add(h)

        # Roll the window.
        for i in range(n, len(s)):
            old = ord(s[i - n]) - 96
            new = ord(s[i]) - 96
            h = (h * base + new - old * pow_n) % MOD
            forbidden.add(h)

    # Candidate is represented by values 0..25.
    # Its polynomial character values are values + 1.
    candidate = bytearray(b'a' * n)

    # Hash of a^n.
    h = (pow(base, n, MOD) - 1) * pow(base - 1, MOD - 2, MOD) % MOD

    # The formula above is the geometric sum:
    # 1 * base^(n-1) + ... + 1.
    #
    # Handle base == 1, which is astronomically unlikely but easy to avoid.
    if base == 1:
        h = n % MOD

    powers = [1] * n
    for i in range(1, n):
        powers[i] = powers[i - 1] * base % MOD

    while True:
        if h not in forbidden:
            sys.stdout.write(candidate.decode())
            return

        # Increment the base-26 number.
        pos = n - 1

        while pos >= 0 and candidate[pos] == ord('z'):
            # z -> a changes the character value from 26 to 1.
            h = (h - 25 * powers[n - 1 - pos]) % MOD
            candidate[pos] = ord('a')
            pos -= 1

        if pos < 0:
            # The statement guarantees that an answer exists.
            return

        # Increase the first non-z character by one.
        h = (h + powers[n - 1 - pos]) % MOD
        candidate[pos] += 1

if __name__ == "__main__":
    solve()
```

The input strings are processed one at a time, so there is no need to keep all of them in memory. For a string of length at least (n), the first window is hashed directly. Every subsequent window is obtained from the previous hash by multiplying by the base, adding the new character, and subtracting the old character multiplied by (B^n).

The candidate is stored as a `bytearray`, which avoids repeatedly constructing Python strings while searching. Its characters are treated as values from (1) to (26), while the byte values themselves are ASCII codes from `a` to `z`.

The candidate hash can be updated locally when the base-26 counter is incremented. If a position changes from `a` to `b`, its hash contribution increases by (B^k). If it changes from `z` to `a`, its contribution decreases by (25B^k). The exponent (k=n-1-\text{pos}) is exactly the number of positions to its right.

The powers array is indexed by this exponent. Since the candidate starts at all `a`, its initial hash is the geometric sum (1+B+\cdots+B^{n-1}). The special `base == 1` branch avoids division by zero in the geometric-sum formula, although the random choice makes that event effectively impossible.

There is no integer-overflow issue in Python because integers have arbitrary precision. The modulus is applied after each arithmetic update, keeping the stored hash bounded by (2^{61}).

## Worked Examples

For the first sample, the input is

```
3 1
a
```

The only existing string has length smaller than (n=3), so it contributes no forbidden length-3 substring.

| Candidate | Hash in forbidden set? | Action |
| --- | --- | --- |
| `aaa` | No | Output `aaa` |

The sample output uses `zzz`, but any valid string is accepted. Here `aaa` is valid because the only existing material is `a`, which has no substring of length three.

For the second sample, the input is

```
3 2
ac
ak
```

Again, both existing strings have length two, so neither contains a length-3 substring.

| Candidate | Hash in forbidden set? | Action |
| --- | --- | --- |
| `aaa` | No | Output `aaa` |

The supplied output `fun` is another valid answer. This trace also exercises the boundary where an input string is exactly one character shorter than the requested answer length.

For a case where the first candidate is actually forbidden, consider

```
3 1
aaaa
```

The length-3 windows are both `aaa`, so the forbidden set contains only the hash of `aaa`.

| Candidate | Hash in forbidden set? | Action |
| --- | --- | --- |
| `aaa` | Yes | Increment candidate |
| `aab` | No | Output `aab` |

The duplicate occurrence of `aaa` is stored only once because the forbidden structure is a set. The candidate `aab` is absent, so the search stops immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(S+n)) | Every input character participates in one rolling-hash update, and at most (S+1) candidates are examined. Candidate increments take (O(1)) amortized time. |
| Space | (O(S+n)) | The set contains at most (S) hashes, while the candidate and powers array use (O(n)) memory. |

Here (S\le3\times10^5), so the algorithm processes only a few hundred thousand characters and maintains a similarly sized hash set. This is compatible with the stated 256 MB memory limit, and it avoids every factor exponential in (n).

## Test Cases

```python
import io
import random

MOD = (1 << 61) - 1

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    base = random.randrange(256, MOD - 1)
    pow_n = pow(base, n, MOD)

    forbidden = set()

    for _ in range(m):
        s = next(it)

        if len(s) < n:
            continue

        h = 0
        for i in range(n):
            h = (h * base + ord(s[i]) - 96) % MOD
        forbidden.add(h)

        for i in range(n, len(s)):
            old = ord(s[i - n]) - 96
            new = ord(s[i]) - 96
            h = (h * base + new - old * pow_n) % MOD
            forbidden.add(h)

    candidate = bytearray(b'a' * n)

    powers = [1] * n
    for i in range(1, n):
        powers[i] = powers[i - 1] * base % MOD

    if base == 1:
        h = n % MOD
    else:
        h = (pow(base, n, MOD) - 1) * pow(base - 1, MOD - 2, MOD) % MOD

    while True:
        if h not in forbidden:
            return candidate.decode()

        pos = n - 1

        while pos >= 0 and candidate[pos] == ord('z'):
            h = (h - 25 * powers[n - 1 - pos]) % MOD
            candidate[pos] = ord('a')
            pos -= 1

        assert pos >= 0, "The original problem guarantees an answer."

        h = (h + powers[n - 1 - pos]) % MOD
        candidate[pos] += 1

# Provided sample 1.
assert solve_data("""\
3 1
a
""") == "aaa", "sample 1"

# Provided sample 2.
assert solve_data("""\
3 2
ac
ak
""") == "aaa", "sample 2"

# Minimum n. Every character except z is forbidden.
case = "1 25\n" + "\n".join(chr(ord('a') + i) for i in range(25)) + "\n"
assert solve_data(case) == "z", "minimum n"

# Off-by-one case: aaa occurs in aaaa, but aab does not.
assert solve_data("""\
3 1
aaaa
""") == "aab", "window boundary"

# Multiple strings cover every length-2 string beginning with a.
case = "2 26\n" + "\n".join("a" + chr(ord('a') + i) for i in range(26)) + "\n"
assert solve_data(case) == "ba", "candidate increment"

# Maximum-size input. The only forbidden length-100000 string is a^100000.
# The next lexicographic candidate is a^(99999)b.
n = 100000
s = "a" * 300000
case = f"{n} 1\n{s}\n"
assert solve_data(case) == "a" * (n - 1) + "b", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 25` followed by `a` through `y` | `z` | Minimum (n) and complete coverage of 25 alphabet symbols |
| `3 1 / aaaa` | `aab` | A forbidden first candidate and the exact length-(n) window boundary |
| `2 26` followed by `aa` through `az` | `ba` | Base-26 candidate increment and transition from `az` to `ba` |
| `100000 1 / a` repeated 300000 times | `a...ab` | Maximum (n), maximum total input size, and long candidate handling |

## Edge Cases

When every input string is shorter than (n), the forbidden set remains empty. For

```
3 2
a
bc
```

there is no length-3 window at all. The candidate starts as `aaa`, its hash is absent, and the algorithm outputs `aaa` immediately. The crucial boundary is the `len(s) < n` check, which prevents attempting to construct a nonexistent window.

When the first candidate is present, the algorithm does not assume that a different repeated-character string will work. For

```
3 1
aaaa
```

the only distinct length-3 substring is `aaa`. The first candidate is rejected, the counter changes its last position from `a` to `b`, producing `aab`, and the second candidate is accepted.

When (n=1), the powers array has exactly one element and the candidate has exactly one byte. For

```
1 25
a
b
...
y
```

the candidate moves through the alphabet one character at a time until it reaches `z`. There is no special case in the enumeration logic for a one-character string.

When the candidate increment crosses a run of `z` characters, every trailing `z` must become `a` before the preceding character is incremented. For example, after `azz`, the next candidate is `baa`, not `bzz` or `aza`. The hash update subtracts (25B^k) for every reset position, then adds the contribution of the incremented position. This is the part most likely to suffer from an off-by-one error, so the `az` to `ba` test explicitly exercises it.
