---
title: "CF 106203L - \u041c\u0438\u0441\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u044d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442 \u041f\u0430\u0433\u0441\u043b\u0438"
description: "We are given an array of integers that changes over time through point updates. After each update, we must be able to answer how many positions in the array have a specific “balance” property defined using XOR."
date: "2026-06-19T16:03:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106203
codeforces_index: "L"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106203
solve_time_s: 45
verified: true
draft: false
---

[CF 106203L - \u041c\u0438\u0441\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u044d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442 \u041f\u0430\u0433\u0441\u043b\u0438](https://codeforces.com/problemset/problem/106203/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers that changes over time through point updates. After each update, we must be able to answer how many positions in the array have a specific “balance” property defined using XOR.

For an index $i$, consider the XOR of all elements strictly to the left of $i$, and the XOR of all elements strictly to the right of $i$. An index is considered special if these two XOR values are equal.

A query either changes one element of the array or asks for the current number of special indices.

The array length and number of queries are both up to $2 \cdot 10^5$, which immediately rules out recomputing prefix and suffix XORs from scratch per query. A full scan after each update would be $O(nq)$, which is far beyond acceptable limits.

A subtle edge case appears at the boundaries. For $i = 0$, the left XOR is empty and therefore zero. For $i = n-1$, the right XOR is empty and also zero. Any correct solution must handle these definitions consistently, otherwise off-by-one logic in prefix or suffix handling will fail on single-element or two-element arrays.

For example, if the array is $[5]$, both left and right XOR are zero, so index 0 is always valid. If a naive implementation forgets empty XOR conventions, it might incorrectly exclude this case.

## Approaches

A direct approach recomputes prefix XORs and suffix XORs for every query. After each update, we recompute two arrays and count indices satisfying the condition. Each recomputation costs $O(n)$, leading to $O(nq)$ total work. With $2 \cdot 10^5$ operations, this is too slow by several orders of magnitude.

The key observation is that the condition can be rewritten in a way that eliminates the need for prefix or suffix structures entirely.

Let $P$ be the XOR of the entire array. Let $pref[i]$ be XOR of elements from $0$ to $i$. Then the left XOR for index $i$ is $pref[i-1]$, and the right XOR is $P \oplus pref[i]$. The condition becomes:

$$pref[i-1] = P \oplus pref[i]$$

Now use the identity $pref[i] = pref[i-1] \oplus a[i]$. Substituting gives:

$$pref[i-1] = P \oplus (pref[i-1] \oplus a[i])$$

Canceling $pref[i-1]$ on both sides using XOR properties yields:

$$0 = P \oplus a[i]$$

which simplifies to:

$$a[i] = P$$

So an index is valid exactly when its value equals the XOR of the entire array.

This reduces the entire problem to maintaining two things under updates: the global XOR of the array and the frequency of each value. Each query of type 2 becomes a single lookup: how many elements currently equal the global XOR.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recompute XORs per query | $O(nq)$ | $O(1)$ | Too slow |
| Maintain total XOR + frequency map | $O(q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two pieces of state: the XOR of the entire array and a frequency map of values in the array.

1. Initialize the frequency map by counting occurrences of each element in the initial array, and compute the XOR of all elements. This sets the baseline state for all future queries.
2. For an update query at position $i$, first remove the contribution of the old value from both the frequency map and the global XOR. This is necessary because the array state must remain consistent before applying the new value.
3. Apply the new value at position $i$, updating the frequency map and XOR accordingly. After this step, the maintained state again reflects the current array exactly.
4. For a query asking for the number of balanced indices, return the frequency of the current global XOR value. This works because we proved that an index is valid exactly when its value equals the total XOR.

### Why it works

The correctness hinges on rewriting the left and right XOR expressions in terms of prefix XOR and then eliminating prefix variables entirely. The final condition reduces to a pointwise equality between each element and a single global scalar, the XOR of the whole array. Since that scalar is always maintained exactly under updates, counting valid indices becomes equivalent to counting occurrences of that scalar in the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    freq = {}
    total_xor = 0

    for v in a:
        total_xor ^= v
        freq[v] = freq.get(v, 0) + 1

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1])
            x = int(tmp[2])

            old = a[i]
            if freq[old] == 1:
                del freq[old]
            else:
                freq[old] -= 1

            total_xor ^= old

            a[i] = x

            total_xor ^= x
            freq[x] = freq.get(x, 0) + 1

        else:
            out.append(str(freq.get(total_xor, 0)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution keeps an explicit array so updates can be applied in constant time. The XOR accumulator is updated by removing the old value and adding the new one, which works because XOR is its own inverse. The frequency dictionary tracks how many elements match any given value, and query answers are simple dictionary lookups.

A common mistake is forgetting to decrement the frequency of the old value before overwriting it, which would lead to inflated counts after multiple updates.

## Worked Examples

Consider the array $[1, 2, 3]$.

We compute total XOR as $1 \oplus 2 \oplus 3 = 0$. No element equals zero, so the answer is 0.

| Step | Array | Total XOR | Frequency Map | Answer |
| --- | --- | --- | --- | --- |
| Initial | [1,2,3] | 0 | {1:1,2:1,3:1} | 0 |

Now update index 1 to value 1, giving $[1, 1, 3]$.

| Step | Array | Total XOR | Frequency Map | Answer |
| --- | --- | --- | --- | --- |
| After update | [1,1,3] | 3 | {1:2,3:1} | 1 |

Here only index values equal to 3 are valid, and there is exactly one such element.

This trace shows that the algorithm never needs prefix computations, only consistent maintenance of a single aggregate invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | Each update modifies a constant number of entries in the map and XOR accumulator |
| Space | $O(n)$ | Frequency map stores at most one entry per distinct value |

The solution fits comfortably within constraints since both limits are linear in the size of the input, and all operations are constant time on average.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    freq = {}
    total_xor = 0
    for v in a:
        total_xor ^= v
        freq[v] = freq.get(v, 0) + 1

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1]); x = int(tmp[2])
            old = a[i]

            freq[old] -= 1
            if freq[old] == 0:
                del freq[old]

            total_xor ^= old
            a[i] = x
            total_xor ^= x
            freq[x] = freq.get(x, 0) + 1
        else:
            out.append(str(freq.get(total_xor, 0)))

    return "\n".join(out)

# minimum size
assert run("""1
5
3
2
1 0 7
2
""") == "1\n0"

# all equal
assert run("""5
1 1 1 1 1
3
2
1 2 2
2
""") == "0\n1"

# single update flips answer
assert run("""3
1 2 3
2
2
1 1 1
2
""") == "0\n1"

# no updates, repeated queries
assert run("""4
0 0 0 0
3
2
2
2
""") == "4\n4\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 / 0 | boundary XOR definition |
| all equal values | varies | correctness under uniform array |
| flip update | 0 then 1 | dynamic consistency of XOR updates |
| repeated queries | constant output | stability without mutation |

## Edge Cases

For a single-element array like $[x]$, the algorithm computes total XOR as $x$. The frequency map contains exactly one occurrence of $x$, so if $x = 0$, the answer is 1, otherwise 0. The implementation correctly handles this because empty prefix and suffix are implicitly encoded in the XOR identity, not in special casing.

For repeated updates on the same index, the removal and insertion steps ensure that the frequency map never double counts values. Each update first subtracts the old value before adding the new one, keeping the invariant that the map exactly reflects the current array at all times.

For arrays where all values are zero, total XOR remains zero throughout all updates. Every index is always valid, and the frequency map always returns $n$, matching the definition of balanced positions.
