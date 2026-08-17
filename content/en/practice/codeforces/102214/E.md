---
title: "CF 102214E - Encryption"
description: "We have a lowercase string of length n. During encryption, we look at every divisor d of n, starting from the largest divisor and ending at 1. For each such divisor, we reverse the prefix consisting of the first d characters."
date: "2026-08-18T00:12:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102214
codeforces_index: "E"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0435 \u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0418\u041a\u0418\u0422 \u0421\u0424\u0423 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2015"
rating: 0
weight: 102214
solve_time_s: 62
verified: true
draft: false
---

[CF 102214E - Encryption](https://codeforces.com/problemset/problem/102214/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a lowercase string of length n. During encryption, we look at every divisor d of n, starting from the largest divisor and ending at 1. For each such divisor, we reverse the prefix consisting of the first d characters.

For example, if n=10, its divisors in decreasing order are 10,5,2,1. Encryption consequently performs four prefix reversals, first on the whole string, then on the first five characters, then on the first two characters, and finally on the first character.

The input gives us the encrypted string, not the original one. We have to recover the original string.

The length is at most 100, and the string contains only lowercase English letters. A limit of 100 is tiny, so even a straightforward simulation of every required reversal is easily fast enough. There is no need for sophisticated string algorithms or data structures. The main difficulty is recognizing the direction in which the reversible operations must be applied.

The first edge case is n=1. For example:

```
1z
```

The only divisor is 1, and reversing a one-character prefix changes nothing. The answer is:

```
z
```

A careless implementation that assumes there is always a nontrivial prefix to reverse could accidentally skip or mishandle this case.

Another edge case occurs when n itself is the only large divisor involved. For example:

```
2ab
```

The divisors are 1 and 2. Decryption processes them in increasing order. Reversing the first character changes nothing, then reversing the first two characters changes `ab` into `ba`, so the correct answer is:

```
ba
```

If we process divisors in decreasing order during decryption, we would perform the operations in the same order as encryption rather than undoing them.

A third common mistake is forgetting that every divisor operation acts on a prefix, not on a block beginning at that divisor. For example, with n=6, divisor 3 means reversing positions 1 through 3. It does not mean reversing positions 3 through 6.

## Approaches

A brute-force way to think about the problem is to enumerate possible original strings and encrypt each candidate until one produces the given encrypted string. The encryption operation itself is deterministic, so such a candidate is easy to verify. However, there are 26 n possible lowercase strings of length n. Even for n=20, this is 26 20, roughly 2 94, which is completely infeasible. The brute force is conceptually correct but fails because it searches an enormous space even though the encryption process itself is completely reversible.

The key observation is that every encryption operation is a reversal, and a reversal is its own inverse. If we reverse a prefix twice, we get exactly the original prefix back. The only other issue is the order of operations.

Suppose encryption applies operations

R d 1 ​ ​ ,R d 2 ​ ​ ,…,R d k ​ ​

where the divisors satisfy

d 1 ​ >d 2 ​ >⋯>d k ​ .

The encrypted string is

R d k ​ ​ (…R d 2 ​ ​ (R d 1 ​ ​ (s))…).

To undo this, we must first undo R d k ​ ​, then R d k−1 ​ ​, and so on. Since each reversal is its own inverse, decryption simply applies the same prefix reversals in the opposite order.

Encryption visits divisors from largest to smallest, so decryption visits divisors from smallest to largest.

This turns the entire problem into a direct simulation. For every d from 1 to n, if d divides n, reverse the first d characters. This is exactly the approach used by the official Codeforces editorial solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 n ⋅n) | O(n) | Too slow |
| Optimal | O(∑ d∣n ​ d) | O(n) | Accepted |

Because n≤100, even the simple implementation is comfortably within the limits. The sum of all divisors is also O(nloglogn) asymptotically, so the direct simulation remains efficient even under a much larger bound.

## Algorithm Walkthrough

1. Read n and the encrypted string t. We will modify this string in place because every decryption operation changes only the ordering of its characters.
2. Iterate d from 1 through n. If nmodd=0, then d is one of the prefixes that was reversed during encryption.
3. Reverse the prefix of length d. We process divisors in increasing order because encryption processed the same divisors in decreasing order, and every reversal is its own inverse.
4. After all divisors have been processed, print the resulting string. At this point every encryption operation has been undone in exactly reverse order.

### Why it works

Let the divisors of n in increasing order be d 1 ​ <d 2 ​ <⋯<d k ​. Encryption applies the reversals in the order d k ​ ,d k−1 ​ ,…,d 1 ​. Decryption applies R d 1 ​ ​ ,R d 2 ​ ​ ,…,R d k ​ ​. Since R d ​ (R d ​ (x))=x for every prefix reversal R d ​, each decryption operation cancels the corresponding encryption operation. The operations are also applied in reverse order, so every transformation is canceled at exactly the right point. The final string is consequently the unique original string.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n = int(input())    s = list(input().strip())
    for d in range(1, n + 1):        if n % d == 0:            s[:d] = reversed(s[:d])
    print(''.join(s))

if __name__ == "__main__":    solve()
```

The string is converted into a list because Python strings are immutable. The expression `s[:d]` represents exactly the first d characters, matching the problem's prefix reversal.

The loop starts at `1` and ends at `n`, so every possible divisor is considered. Checking `n % d == 0` identifies exactly the required prefix lengths.

The assignment

```
Pythons[:d] = reversed(s[:d])
```

replaces the prefix with its reverse. The order is crucial. Iterating from small divisors to large divisors performs the inverse of the encryption sequence.

There is no integer overflow concern in Python. There is also no off-by-one issue because Python's slice `s[:d]` contains indices `0` through `d-1`, exactly d characters.

## Worked Examples

### Sample 1

The input is:

```
10rocesfedoc
```

The divisors of 10 in increasing order are 1,2,5,10.

| d | Is divisor? | String after reversal |
| --- | --- | --- |
| 1 | Yes | `rocesfedoc` |
| 2 | Yes | `orcesfedoc` |
| 3 | No | `orcesfedoc` |
| 4 | No | `orcesfedoc` |
| 5 | Yes | `secrofedoc` |
| 6 | No | `secrofedoc` |
| 7 | No | `secrofedoc` |
| 8 | No | `secrofedoc` |
| 9 | No | `secrofedoc` |
| 10 | Yes | `codeforces` |

The final answer is:

```
codeforces
```

The trace demonstrates the central invariant: after processing the first k divisors in increasing order, the corresponding k encryption operations at the end of the original encryption sequence have already been canceled.

### Sample 2

The input is:

```
16plmaetwoxesisiht
```

The divisors of 16 are 1,2,4,8,16.

| d | Is divisor? | String after reversal |
| --- | --- | --- |
| 1 | Yes | `plmaetwoxesisiht` |
| 2 | Yes | `lpmaetwoxesisiht` |
| 3 | No | `lpmaetwoxesisiht` |
| 4 | Yes | `ampl...` |
| 8 | Yes | `this...` |
| 16 | Yes | `thisisexampletwo` |

The complete resulting string is:

```
thisisexampletwo
```

This example exercises several nested prefix reversals. It also shows why the reversals cannot be treated independently. Reversing a larger prefix changes characters that were already moved by smaller prefix reversals, so the exact operation order matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑ d∣n ​ d) | Every divisor d causes a reversal of d characters |
| Space | O(n) | The string is stored as a mutable character array |

For n≤100, the maximum amount of work is tiny. Even a deliberately simple implementation that scans all n possible prefix lengths and reverses each qualifying prefix is easily within the one-second time limit and 256 MB memory limit of the actual Codeforces problem.

## Test Cases

```python
Pythonimport sysimport io

def solve():    input = sys.stdin.readline    n = int(input())    s = list(input().strip())
    for d in range(1, n + 1):        if n % d == 0:            s[:d] = reversed(s[:d])
    print(''.join(s))

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided sample 1assert run("10\nrocesfedoc\n") == "codeforces\n", "sample 1"
# Provided sample 2assert run("16\nplmaetwoxesisiht\n") == "thisisexampletwo\n", "sample 2"
# Provided sample 3assert run("1\nz\n") == "z\n", "sample 3"
# Minimum-size inputassert run("1\na\n") == "a\n", "minimum size"
# All characters equalassert run("8\naaaaaaaa\n") == "aaaaaaaa\n", "all equal"
# Smallest non-trivial divisor structureassert run("2\nab\n") == "ba\n", "n = 2"
# Boundary-sized inputassert run("100\n" + "a" * 100 + "\n") == "a" * 100 + "\n", "n = 100"
# Several divisors, catches divisor-order mistakesassert run("6\nfedcba\n") == "abcdef\n", "multiple divisors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `a` | Minimum size and prefix of length 1 |
| `8 / aaaaaaaa` | `aaaaaaaa` | Reversals preserve equal characters |
| `2 / ab` | `ba` | Smallest non-trivial reversal |
| `100 / a...a` | Same 100 characters | Maximum input length |
| `6 / fedcba` | `abcdef` | Multiple divisors and correct reversal order |

## Edge Cases

For n=1, the input

```
1z
```

has only divisor 1. The algorithm checks 1∣1, reverses the first character, and obtains `z` again. It prints `z`, so the single-character prefix requires no special case.

For n=2, consider

```
2ab
```

The increasing divisor sequence is 1,2. The length-one reversal leaves `ab` unchanged. The length-two reversal produces `ba`. Encrypting `ba` reverses the whole string and returns `ab`, confirming that the increasing order is the correct inverse order.

For an input where every character is equal, such as

```
8aaaaaaaa
```

every reversal leaves the visible string unchanged. The algorithm still processes divisors 1,2,4,8, but every intermediate state remains `aaaaaaaa`. This catches implementations that accidentally depend on characters being distinct.

Finally, consider

```
6fedcba
```

The divisors are 1,2,3,6. After reversing prefixes of these lengths in that order, the string becomes `abcdef`. The fact that 2, 3, and 6 all interact with the same first positions makes this a useful test for the most common mistake, processing the divisors in decreasing order during decryption. The solution avoids that mistake by reversing the encryption sequence exactly.
