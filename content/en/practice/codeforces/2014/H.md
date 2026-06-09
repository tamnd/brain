---
title: "CF 2014H - Robin Hood Archery"
description: "For each query we look only at the subarray $al, a{l+1}, dots, ar$. Robin moves first. On every turn a player chooses any remaining target, gains its value, and removes it."
date: "2026-06-08T13:03:20+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "greedy", "hashing"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 1900
weight: 2014
solve_time_s: 122
verified: true
draft: false
---

[CF 2014H - Robin Hood Archery](https://codeforces.com/problemset/problem/2014/H)

**Rating:** 1900  
**Tags:** data structures, divide and conquer, greedy, hashing  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query we look only at the subarray $a_l, a_{l+1}, \dots, a_r$.

Robin moves first. On every turn a player chooses any remaining target, gains its value, and removes it. Since there are no restrictions on which target can be chosen, the game is completely determined by the multiset of values inside the queried segment.

Both players play perfectly. For every query we must determine whether the Sheriff can avoid losing. A tie counts as success for the Sheriff, because the question asks whether he does **not** lose.

The total number of elements and queries over all test cases is at most $2 \cdot 10^5$. Any solution that processes a query in linear time would require roughly $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the limit. We need close to constant or logarithmic work per query after preprocessing.

The game-theoretic part is the first trap. A naive simulation of optimal play looks complicated because players alternate turns. In reality, because every target is available from the start, each player simply takes the currently largest remaining value. The sequence of chosen values is completely determined.

Another easy mistake is to think that only the sum matters. Consider:

```
[1, 2]
```

Robin takes 2, Sheriff takes 1, so Sheriff loses.

The total sum is 3, but that alone tells us nothing.

A second trap is assuming that every even-length segment produces a tie.

```
[1, 1, 2, 3]
```

Robin gets $3+1=4$, Sheriff gets $2+1=3$. Sheriff loses.

The frequencies of values matter.

A more subtle case is:

```
[5, 5, 7]
```

Sorted descending:

```
7, 5, 5
```

Robin gets $7+5=12$, Sheriff gets $5$.

Even though value 5 appears twice, the unmatched 7 decides the game.

Understanding exactly when unmatched values exist is the key observation.

## Approaches

Let us first understand what optimal play looks like.

Since every remaining target can always be selected, a player never benefits from taking a smaller value while a larger value is available. If a larger value remains, taking it immediately can only improve that player's final score.

As a result, the game is equivalent to sorting the values in descending order. Robin receives positions $1,3,5,\dots$ and Sheriff receives positions $2,4,6,\dots$.

Suppose we explicitly sort every queried segment. For a segment of length $m$, we would sort its values and compute alternating sums. This is correct because it exactly matches optimal play.

The problem is complexity. A query may contain $O(n)$ elements, so sorting costs $O(m \log m)$. With up to $2 \cdot 10^5$ queries, this is completely infeasible.

The breakthrough comes from looking at frequencies instead of scores.

Take any value $x$. If it appears an even number of times, then after sorting those copies occupy consecutive positions and split evenly between the two players. Their contribution cancels out.

Only values with odd frequency matter. After pairing equal values together, every odd-frequency value leaves exactly one unpaired copy. These leftover copies are distinct values. When sorted, they alternate between Robin and Sheriff.

Now observe something remarkable. Let the remaining distinct values be

$$b_1 > b_2 > \dots > b_k.$$

Robin receives $b_1, b_3, b_5,\dots$, Sheriff receives $b_2, b_4, b_6,\dots$.

Since the values are strictly decreasing, Robin's total is greater than Sheriff's whenever $k$ is odd. If $k$ is even, the leftovers pair perfectly and the totals are equal.

So the entire game reduces to one question:

Does the segment contain an odd or even number of values whose frequency is odd?

Sheriff avoids losing exactly when that count is even.

We now need a data structure that answers, for any subarray, whether every value appears an even number of times after cancellation.

This is a classic parity query. Assign each distinct value a random 64-bit hash. Let

$$pref[i] = h(a_1) \oplus h(a_2) \oplus \dots \oplus h(a_i).$$

For a query $[l,r]$,

$$X = pref[r] \oplus pref[l-1].$$

Every value appearing an even number of times cancels under XOR. The result is exactly the XOR of hashes corresponding to values with odd frequency.

If no odd-frequency values exist, then $X=0$.

More generally, the number of odd-frequency values is even if and only if the XOR of their hashes equals the XOR of an even-sized set of hashes. The intended solution uses random hashing: assign independent random numbers to values. Then the XOR is zero precisely when all odd-frequency values cancel, and with overwhelming probability nonzero otherwise.

The official observation is even stronger. Sheriff does not lose iff every value frequency in the segment is even. That condition is equivalent to the segment XOR hash being zero.

The probability of collision with 64-bit random numbers is negligible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m \log m)$ per query | $O(m)$ | Too slow |
| Optimal | $O(n+q)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Assign a random 64-bit number to every distinct value

Whenever a value appears for the first time, generate a random 64-bit integer and store it.

Equal values always receive the same hash.

### 2. Build a prefix XOR array

Define

$$pref[0]=0$$

and

$$pref[i]=pref[i-1]\oplus h(a_i).$$

This allows us to obtain the XOR hash of any segment in constant time.

### 3. Process a query

For segment $[l,r]$, compute

$$cur=pref[r]\oplus pref[l-1].$$

Every value occurring an even number of times contributes its hash an even number of times and disappears.

The result is the XOR of hashes corresponding exactly to values whose frequency inside the segment is odd.

### 4. Decide the answer

If

$$cur=0,$$

then every value frequency is even, so the Sheriff can avoid losing. Output `"YES"`.

Otherwise output `"NO"`.

### Why it works

The crucial invariant is that XOR tracks parity.

For any value $x$, its hash appears once for every occurrence of $x$. Since

$$h(x)\oplus h(x)=0,$$

all even occurrences cancel. After taking the XOR of a segment, the only surviving hashes belong to values with odd frequency.

If every frequency is even, the segment XOR equals zero. If at least one odd-frequency value exists, the XOR is nonzero except with negligible collision probability from the random hashes.

The game analysis shows that the Sheriff avoids losing exactly when every value can be paired with another equal value. Thus the query answer is determined entirely by whether the segment XOR hash is zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

MASK = (1 << 64) - 1

def splitmix64(x):
    x = (x + 0x9e3779b97f4a7c15) & MASK
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9 & MASK
    x = (x ^ (x >> 27)) * 0x94d049bb133111eb & MASK
    x ^= x >> 31
    return x & MASK

def solve():
    t = int(input())

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        value_hash = {}
        pref = [0] * (n + 1)

        for i, x in enumerate(a, 1):
            if x not in value_hash:
                value_hash[x] = splitmix64(x)

            pref[i] = pref[i - 1] ^ value_hash[x]

        ans = []

        for _ in range(q):
            l, r = map(int, input().split())

            cur = pref[r] ^ pref[l - 1]

            if cur == 0:
                ans.append("YES")
            else:
                ans.append("NO")

        sys.stdout.write("\n".join(ans) + "\n")

solve()
```

The first part assigns a deterministic 64-bit hash to every distinct value using `splitmix64`. Using a deterministic hash avoids dependence on Python's random generator while preserving the collision resistance needed for the solution.

The prefix array stores cumulative XOR values. Since XOR is its own inverse, the segment XOR is obtained as `pref[r] ^ pref[l - 1]`.

The only subtle detail is indexing. The prefix array is built as a 1-based structure, so query boundaries map naturally to the standard range formula.

Python integers are unbounded, but all hashes are kept inside 64 bits using the mask. This reproduces unsigned 64-bit arithmetic.

## Worked Examples

### Sample 1, Query [2, 3]

Array:

```
[1, 2, 2]
```

Segment:

```
[2, 2]
```

| Value | Frequency | Odd? | Contributes to XOR |
| --- | --- | --- | --- |
| 2 | 2 | No | No |

The segment hash becomes zero.

Output:

```
YES
```

Both copies of 2 cancel. Every frequency is even, so the Sheriff cannot lose.

### Sample 1, Query [1, 3]

Segment:

```
[1, 2, 2]
```

| Value | Frequency | Odd? | Contributes to XOR |
| --- | --- | --- | --- |
| 1 | 1 | Yes | Yes |
| 2 | 2 | No | No |

The segment XOR equals the hash of value 1, which is nonzero.

Output:

```
NO
```

The unmatched value survives, so the condition fails.

### Second Test Case, Query [4, 5]

Segment:

```
[1, 1]
```

| Value | Frequency | Odd? | Contributes to XOR |
| --- | --- | --- | --- |
| 1 | 2 | No | No |

Segment XOR is zero.

Output:

```
YES
```

This demonstrates the core parity invariant. Equal pairs always disappear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | One pass to build prefixes, constant work per query |
| Space | $O(n)$ | Prefix array and hash mapping |

The total sum of all $n$ and all $q$ over the input is at most $2 \cdot 10^5$. An $O(n+q)$ solution performs only a few hundred thousand operations and easily fits within the time limit. Memory usage is linear and comfortably below 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MASK = (1 << 64) - 1

    def splitmix64(x):
        x = (x + 0x9e3779b97f4a7c15) & MASK
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9 & MASK
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb & MASK
        x ^= x >> 31
        return x & MASK

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = []
    t = int(input())

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        mp = {}
        pref = [0] * (n + 1)

        for i, x in enumerate(a, 1):
            if x not in mp:
                mp[x] = splitmix64(x)
            pref[i] = pref[i - 1] ^ mp[x]

        for _ in range(q):
            l, r = map(int, input().split())
            out.append("YES" if (pref[r] ^ pref[l - 1]) == 0 else "NO")

    return "\n".join(out)

# provided sample
assert run(
"""2
3 3
1 2 2
1 2
1 3
2 3
5 3
2 1 2 1 1
1 2
1 3
4 5
"""
) == "\n".join([
    "NO",
    "NO",
    "YES",
    "NO",
    "NO",
    "YES"
])

# minimum size
assert run(
"""1
1 1
5
1 1
"""
) == "NO"

# all equal values
assert run(
"""1
4 3
7 7 7 7
1 4
1 2
2 3
"""
) == "\n".join(["YES", "YES", "YES"])

# odd frequency survives
assert run(
"""1
3 2
5 5 7
1 3
1 2
"""
) == "\n".join(["NO", "YES"])

# boundary ranges
assert run(
"""1
5 2
1 2 1 2 3
1 4
5 5
"""
) == "\n".join(["YES", "NO"])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | NO | Smallest possible segment |
| All equal values | YES for every even-sized range | Pair cancellation |
| 5 5 7 | NO then YES | Odd-frequency survivor |
| Prefix and suffix queries | YES then NO | Boundary indexing |

## Edge Cases

Consider:

```
1
1 1
10
1 1
```

The segment contains one occurrence of 10. Its hash survives in the segment XOR, so the answer is `"NO"`. The algorithm correctly identifies that a single unmatched value remains.

Consider:

```
1
1 1
4 4 9 9
1 4
```

Both values occur twice. The segment XOR becomes

$$h(4)\oplus h(4)\oplus h(9)\oplus h(9)=0.$$

The algorithm outputs `"YES"` because every frequency is even.

Consider:

```
1
1 1
5 5 7
1 3
```

The two copies of 5 cancel, leaving only the hash of 7. The segment XOR is nonzero, producing `"NO"`.

Finally, consider a range touching array boundaries:

```
1
2 1
1 2 1 2
1 4
```

The query uses `pref[4] ^ pref[0]`. The prefix construction deliberately includes `pref[0]=0`, so there is no special handling for ranges beginning at position 1. The answer is `"YES"` because every value appears twice.
