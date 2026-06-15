---
title: "CF 1220A - Cards"
description: "We are given a multiset of letters that originally came from writing several binary words, where each word is either the string \"zero\" representing digit 0 or \"one\" representing digit 1."
date: "2026-06-15T19:09:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1220
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 586 (Div. 1 + Div. 2)"
rating: 800
weight: 1220
solve_time_s: 131
verified: true
draft: false
---

[CF 1220A - Cards](https://codeforces.com/problemset/problem/1220/A)

**Rating:** 800  
**Tags:** implementation, sortings, strings  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of letters that originally came from writing several binary words, where each word is either the string `"zero"` representing digit 0 or `"one"` representing digit 1. These words were concatenated and then all letters were shuffled, so we lose all structure except the raw character counts.

Our task is to reconstruct the binary number that could have produced these letters, but among all valid reconstructions we must output the maximum possible binary number. That means we want as many `1` digits as possible, because in binary representation any `1` contributes more value than a `0` in the same position.

The key constraint is that every letter must be used exactly, and every digit we form must correspond to either `"zero"` or `"one"`.

The input size is up to 100000 characters. This immediately rules out any approach that tries to permute or search over arrangements. Even quadratic methods would be too slow in the worst case. We need a linear or near-linear reconstruction based purely on counting and greedy extraction.

A subtle edge case appears when letters overlap heavily between words. For example, `"o"`, `"n"`, `"e"` overlap with `"z"`, `"e"`, `"r"`, `"o"` only in the letter `'o'` and `'e'`. A naive attempt to greedily pick words without careful ordering could fail if it does not prioritize extracting `"one"` first.

Another edge case is when there are no full words of `"one"` or `"zero"` even though letters exist. For example, `"noe"` cannot form either word and should not appear due to constraints, but intermediate greedy logic must avoid assuming partial matches are valid.

## Approaches

A brute-force interpretation would attempt to reconstruct the sequence by trying all permutations of grouping letters into chunks of size 3 or 4 and checking whether each chunk forms `"one"` or `"zero"`. Even if we fix grouping sizes, we would still need to try combinations of partitions of the string, which grows exponentially with n. At n = 100000, this is completely infeasible.

The crucial observation is that each digit corresponds to a fixed multiset of characters. We are not arranging letters arbitrarily, we are decomposing a multiset into known fixed multisets:

`zero → {z, e, r, o}`

`one → {o, n, e}`

This is a classic multiset decomposition problem. The greedy strategy is to determine how many times each word can be formed independently from character counts.

The only coupling between the two words is the shared letters `'o'` and `'e'`, but we can resolve this cleanly by prioritizing extraction of `"one"` first. The reason is that `"one"` uses `'n'`, which does not appear in `"zero"`, so it is uniquely identifiable. Once all `"one"` words are extracted, remaining letters naturally form `"zero"` words if possible.

After counting how many `"one"` we can form, we subtract their letter usage from the frequency table, and then count `"zero"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (partition search) | Exponential | O(n) | Too slow |
| Optimal (frequency + greedy extraction) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by counting letters and extracting words in a deterministic order.

1. Count the frequency of every character in the input string. This gives a global constraint on how many words we can form.
2. Determine how many times we can form `"one"`. Since `"one"` requires `'n'`, and only `"one"` uses `'n'`, the number of `"one"` words is exactly the count of `'n'`.
3. For each `"one"` we remove, we decrement the counts of `'o'`, `'n'`, and `'e'`. This step ensures we do not reuse letters that have already been committed.
4. After removing all `"one"` words, compute how many `"zero"` words can be formed. This is constrained by the remaining counts of `'z'`, `'e'`, `'r'`, and `'o'`. Since all letters are independent after removing `"one"`, the number of `"zero"` words is limited by the minimum frequency among these required letters.
5. Construct the final answer by printing all `"one"` digits first (to maximize binary value), followed by all `"zero"` digits.

The ordering is crucial because binary numbers are maximized by placing 1s in higher significance positions, and since output is space-separated digits, placing all ones first ensures lexicographically and numerically maximal output.

### Why it works

The correctness relies on the fact that `"one"` has a unique identifying letter `'n'` that does not appear in `"zero"`. This makes the number of `"one"` words fixed and independent of any ordering choice. Once all occurrences of `"one"` are removed, the remaining multiset contains only valid combinations of `"zero"` words if the input is guaranteed valid. The greedy separation does not lose optimality because there is no alternative way to trade a `"one"` for a `"zero"` without violating the fixed letter constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - 97] += 1

    o = ord('o') - 97
    n = ord('n') - 97
    e = ord('e') - 97
    z = ord('z') - 97
    r = ord('r') - 97

    ones = cnt[n]

    # build ones
    cnt[o] -= ones
    cnt[n] -= ones
    cnt[e] -= ones

    zeros = min(cnt[z], cnt[e], cnt[r], cnt[o])

    res = []
    res.extend(["1"] * ones)
    res.extend(["0"] * zeros)

    sys.stdout.write(" ".join(res))

if __name__ == "__main__":
    solve()
```

The implementation is driven entirely by frequency accounting. We explicitly rely on `'n'` as the pivot for counting `"one"` words, since it uniquely appears there. After subtracting its contribution, we safely compute `"zero"` counts from remaining letters.

The final concatenation step ensures correctness of ordering, since all `"1"` digits are placed before `"0"` digits.

A subtle implementation detail is that we must subtract all letters used by `"one"` before counting `"zero"`. If we skip this step, shared letters like `'o'` and `'e'` would be double-counted, producing an inflated number of `"zero"` words.

## Worked Examples

### Example 1

Input:

```
4
ezor
```

Frequency table starts as:

`e:1 z:1 o:1 r:1`

| Step | ones | remaining e | remaining z | remaining o | remaining r | zeros |
| --- | --- | --- | --- | --- | --- | --- |
| initial | - | 1 | 1 | 1 | 1 | - |
| after ones | 0 | 1 | 1 | 1 | 1 | - |
| zero count | - | 1 | 1 | 1 | 1 | 1 |

We form one `"zero"` and zero `"one"`.

Output:

```
0
```

This shows the case where no `"one"` can be formed due to absence of `'n'`.

### Example 2

Input:

```
7
onezeroo
```

Frequency:

`o:3 n:1 e:2 z:1 r:1`

| Step | ones | o | n | e | z | r | zeros |
| --- | --- | --- | --- | --- | --- | --- | --- |
| initial | - | 3 | 1 | 2 | 1 | 1 | - |
| after ones | 1 | 2 | 0 | 1 | 1 | 1 | - |
| zero count | - | 2 | 0 | 1 | 1 | 1 | 1 |

We output `"1 0"`.

This confirms that removing `"one"` first prevents double counting `'o'` and `'e'`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass for counting plus constant-time arithmetic over alphabet |
| Space | O(1) | Fixed size frequency array of 26 letters |

The solution is linear in the input size and uses constant auxiliary memory. This is well within limits for n up to 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import Counter

    data = sys.stdin.read().strip().split()
    n = int(data[0])
    s = data[1]

    cnt = [0]*26
    for ch in s:
        cnt[ord(ch)-97] += 1

    o = ord('o')-97
    n_ = ord('n')-97
    e = ord('e')-97
    z = ord('z')-97
    r = ord('r')-97

    ones = cnt[n_]
    cnt[o] -= ones
    cnt[n_] -= ones
    cnt[e] -= ones

    zeros = min(cnt[z], cnt[e], cnt[r], cnt[o])

    res = ["1"]*ones + ["0"]*zeros
    return " ".join(res)

# provided sample
assert run("4\nezor") == "0"

# custom cases
assert run("3\none") == "1"
assert run("4\nzero") == "0"
assert run("8\nonezeroe") == "1 0"
assert run("12\noneonezerozero") == "1 1 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `one` | `1` | minimal one-only case |
| `zero` | `0` | minimal zero-only case |
| `onezeroe` | `1 0` | mixed reconstruction |
| `oneonezerozero` | `1 1 0 0` | multiple repetitions and ordering |

## Edge Cases

One edge case is when no `"one"` can be formed because `'n'` is absent. For input `"zerozero"`, the algorithm sets `ones = 0`, and directly computes `"zero"` from remaining letters, producing `"0 0"` correctly.

Another edge case is when letters are abundant but unbalanced. For `"oneoneonezero"`, the count of `'n'` strictly limits `"one"` words, ensuring we do not overproduce ones even if `'o'` and `'e'` are plentiful.

Finally, cases where both words are fully interleaved in letters are handled safely because subtraction of `"one"` letters guarantees no interference in counting `"zero"`.
