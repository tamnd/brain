---
title: "CF 102420E - \u041b\u0435\u043d\u0438\u0432\u044b\u0435 \u043b\u0435\u0441\u043e\u0440\u0443\u0431\u044b"
description: "We have an ordered sequence of (n) lumberjacks. Lumberjack (i) works on one interval ([li,ri]), and on that interval he lowers the wall by exactly half a meter."
date: "2026-08-12T00:42:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 122
verified: true
draft: false
---

[CF 102420E - \u041b\u0435\u043d\u0438\u0432\u044b\u0435 \u043b\u0435\u0441\u043e\u0440\u0443\u0431\u044b](https://codeforces.com/problemset/problem/102420/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an ordered sequence of (n) lumberjacks. Lumberjack (i) works on one interval ([l_i,r_i]), and on that interval he lowers the wall by exactly half a meter. For a chosen contiguous group of lumberjacks (a,a+1,\ldots,b), we need the total decrease to be an integer at every coordinate on the wall.

Since every contribution is (0.5), the only thing that matters is parity. At every coordinate, the number of selected intervals covering that coordinate must be even. The answer is the number of contiguous subarrays of lumberjacks satisfying this parity condition.

The official constraints allow (n=200,000), while the contest page gives a 2 second time limit and 512 MB of memory. An (O(n^2)) enumeration performs about (n(n+1)/2), roughly (2\cdot10^{10}), subarray checks in the worst case. Even if each check were extremely cheap, that is far beyond what can fit into the time limit. We need a linear or near-linear algorithm.

The coordinates can be as small as (-10^9) and as large as (10^9), so treating every integer coordinate as an array index is impossible. Only the interval endpoints matter, which gives us at most (2n) relevant coordinates.

There are several edge cases that are easy to mishandle. With a single lumberjack, for example, the answer is zero:

```
1
1 2
```

The one interval contributes half a meter on ([1,2]), so it can never form an integer change by itself. An implementation that counts every interval because the endpoints are different would be wrong.

A second common mistake is forgetting that the empty change is allowed when a group of intervals cancels completely. For example:

```
2
1 3
1 3
```

The answer is (1), because choosing both lumberjacks makes the decrease exactly one meter on ([1,3]). More generally, identical intervals cancel in pairs when we only look at parity.

Negative coordinates also have to work without special handling:

```
2
-5 -2
-5 -2
```

Again the answer is (1). Any solution based on direct array indexing by coordinates would fail here unless it performs coordinate compression.

Finally, an interval can have the same endpoint as another interval's endpoint without the intervals being identical. For example:

```
3
1 2
2 3
1 3
```

The answer is (1). The three intervals together cancel at the parity level, while no proper nonempty prefix does. A solution that reasons only about interval lengths or only about how many endpoints are shared will miss the actual parity structure.

## Approaches

The direct approach is to examine every pair ((a,b)). For each chosen subarray, we could maintain the number of selected intervals covering every relevant coordinate and check whether all those counts are even. This is correct because the physical condition is exactly that every half-meter contribution occurs an even number of times. Even with coordinate compression and efficient updates, there are (\Theta(n^2)) possible subarrays. For (n=200,000), there are (20,000,100,000) of them, so the quadratic approach is not viable.

The useful observation comes from looking at an interval through its endpoints instead of through every point inside it. Imagine walking along the number line. The parity of the number of active intervals changes exactly when we cross an endpoint. An interval ([l,r]) toggles the parity at (l) and toggles it back at (r). Thus, if we represent the set of endpoint coordinates with odd multiplicity, an interval is represented by toggling exactly two coordinates, (l) and (r).

For a collection of intervals, the final coverage parity is zero everywhere exactly when every endpoint coordinate occurs an even number of times. In algebraic terms, every interval is a vector over (\mathrm{GF}(2)), with a (1) at its two endpoints, and the chosen group is valid precisely when the XOR of all these vectors is zero.

Now consider prefix groups. Let (P_i) be the XOR of the endpoint vectors of lumberjacks (1) through (i), with (P_0=0). The intervals from (a) through (b) have XOR

[
P_b \oplus P_{a-1}.
]

This XOR is zero exactly when

[
P_b=P_{a-1}.
]

So the original problem becomes a familiar prefix-state counting problem: compute the state after every lumberjack and count equal states. If one state has appeared (k) times, the next occurrence creates (k) new valid subarrays.

The states are actually parity sets over up to (2n) coordinates, so storing them literally would be too expensive. We can give every coordinate a random 128-bit fingerprint and XOR the fingerprints of endpoints. With two independent 64-bit components, equal parity sets always produce equal fingerprints, while the probability that two different parity sets collide is negligible. A fresh random seed makes it impractical for input data to be constructed specifically to cause a collision.

The brute-force approach works because it explicitly checks every interval group, but fails because there are quadratically many groups. The observation that an interval is completely characterized, for parity purposes, by its two endpoints lets us turn every group into a prefix XOR comparison, reducing the whole task to one pass with a hash map.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) or worse | (O(n)) | Too slow |
| Prefix XOR with 128-bit fingerprints | (O(n)) expected | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Assign every coordinate a random 128-bit fingerprint, represented as two independent 64-bit integers. The same coordinate must always receive the same pair, while different coordinates should almost certainly receive different fingerprints.
2. Start with prefix state ((0,0)). This represents the empty collection of lumberjacks. Put this state into a frequency map with count (1), because every later prefix equal to it forms a valid subarray starting at lumberjack (1).
3. Process lumberjacks from left to right. For interval ([l_i,r_i]), XOR the fingerprint of (l_i) and the fingerprint of (r_i) into the current prefix state. Both endpoints are toggled because an interval changes the active coverage parity when entering and when leaving it.
4. Look up the new prefix state in the frequency map. If it has appeared (k) times before, add (k) to the answer. Each previous occurrence corresponds to a prefix (P_j) with (P_j=P_i), and the lumberjacks (j+1,\ldots,i) consequently have zero XOR.
5. Increase the frequency of the current state. The state is now available to form valid subarrays ending at some later position.
6. After all (n) lumberjacks have been processed, output the accumulated answer.

### Why it works

For every coordinate (x), the parity of the selected coverage changes only when an interval starts or ends at (x). Thus an interval contributes exactly two parity toggles, one at each endpoint. A group of intervals has integer height change everywhere precisely when every coordinate is toggled an even number of times, which is exactly when the XOR of their endpoint vectors is zero.

The prefix state (P_i) stores the XOR of the first (i) intervals. A subarray (a,\ldots,b) has zero endpoint parity exactly when (P_{a-1}\oplus P_b=0), or equivalently (P_{a-1}=P_b). The frequency map counts exactly how many choices of (a-1) give this equality. Hence every valid subarray is counted once, and no invalid subarray is counted.

The only approximation is replacing the full parity vector by a random 128-bit fingerprint. A collision between two different parity vectors could theoretically produce a wrong answer, but with two independent 64-bit values the probability is negligible for this input size.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

MASK = (1 << 64) - 1
SM_CONST = 0x9E3779B97F4A7C15

def splitmix64(x):
    x = (x + SM_CONST) & MASK
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK
    return (x ^ (x >> 31)) & MASK

def solve():
    n = int(input())

    seed1 = random.SystemRandom().getrandbits(64)
    seed2 = random.SystemRandom().getrandbits(64)

    state1 = 0
    state2 = 0

    freq = {(0, 0): 1}
    answer = 0

    def fingerprint(x):
        # x is allowed to be negative, so normalize it to 64 bits.
        ux = x & MASK
        h1 = splitmix64(ux ^ seed1)
        h2 = splitmix64(ux ^ seed2)
        return h1, h2

    for _ in range(n):
        l, r = map(int, input().split())

        l1, l2 = fingerprint(l)
        r1, r2 = fingerprint(r)

        state1 ^= l1 ^ r1
        state2 ^= l2 ^ r2

        state = (state1, state2)
        answer += freq.get(state, 0)
        freq[state] = freq.get(state, 0) + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The `splitmix64` function turns a coordinate into a well-mixed 64-bit value. Two independent seeds produce two independent fingerprints, giving the prefix state a total of 128 bits. The use of `& MASK` is necessary because Python integers do not naturally wrap at 64 bits, while the mixing function is defined over unsigned 64-bit arithmetic.

The prefix state starts at zero and is inserted into `freq` before processing any interval. That initial occurrence represents (P_0), which is needed for subarrays beginning with lumberjack (1). Forgetting it loses every valid prefix.

For each interval, the code XORs both endpoint fingerprints into the state. XOR is exactly the operation needed for parity: applying the same coordinate twice cancels it because (x\oplus x=0). The order of the two endpoint updates does not matter.

The answer is updated before increasing the frequency of the current state. This makes the map represent only earlier prefixes. Adding the current state first would incorrectly allow a zero-length subarray, which is not among the choices (a\le b).

Python integers have arbitrary precision, but all fingerprint arithmetic is explicitly reduced to 64 bits inside `splitmix64`. The final answer itself can be as large as (n(n+1)/2), around (2\cdot10^{10}), which Python handles directly.

## Worked Examples

For Sample 1, the intervals are ([1,3]), ([2,3]), ([2,3]), and ([1,3]). We can write (A_x) for the fingerprint of coordinate (x). The prefix state is represented symbolically as an XOR of these fingerprints.

| i | Interval | Prefix state | Previous equal states | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | (0) | 1 | 0 |
| 1 | ([1,3]) | (A_1\oplus A_3) | 0 | 0 |
| 2 | ([2,3]) | (A_1\oplus A_2) | 0 | 0 |
| 3 | ([2,3]) | (A_1\oplus A_3) | 1 | 1 |
| 4 | ([1,3]) | (0) | 1 | 2 |

At (i=3), the state equals the state after the first lumberjack, so lumberjacks (2) through (3) form a valid group. At (i=4), the state returns to zero, matching the empty prefix, so all four lumberjacks form another valid group. The answer is (2).

For Sample 2, the intervals are ([1,2]), ([2,3]), and ([1,3]).

| i | Interval | Prefix state | Previous equal states | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | (0) | 1 | 0 |
| 1 | ([1,2]) | (A_1\oplus A_2) | 0 | 0 |
| 2 | ([2,3]) | (A_1\oplus A_3) | 0 | 0 |
| 3 | ([1,3]) | (0) | 1 | 1 |

Only the complete sequence returns to the initial state. Its three intervals have endpoint multiset (1,2,2,3,1,3), so every coordinate occurs exactly twice. The answer is (1).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) expected | Each lumberjack performs a constant number of 64-bit hash operations and expected (O(1)) hash-map operations. |
| Space | (O(n)) | The frequency map contains at most (n+1) distinct prefix states. |

With (n\le200,000), a single linear pass is appropriate for the 2 second, 512 MB limits given by the contest page. The implementation performs only constant work per lumberjack and stores at most one entry for each prefix state.

## Test Cases

The test harness below uses the same fingerprint idea as the submitted solution, but exposes the algorithm through `solve_text` so each case can be checked with an assertion.

```python
import sys
import io
import random

MASK = (1 << 64) - 1
SM_CONST = 0x9E3779B97F4A7C15

def splitmix64(x):
    x = (x + SM_CONST) & MASK
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK
    return (x ^ (x >> 31)) & MASK

def solve_text(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))

    seed1 = 0x123456789ABCDEF0
    seed2 = 0x0FEDCBA987654321

    def fingerprint(x):
        ux = x & MASK
        return (
            splitmix64(ux ^ seed1),
            splitmix64(ux ^ seed2),
        )

    s1 = 0
    s2 = 0
    freq = {(0, 0): 1}
    ans = 0

    for _ in range(n):
        l = int(next(it))
        r = int(next(it))

        l1, l2 = fingerprint(l)
        r1, r2 = fingerprint(r)

        s1 ^= l1 ^ r1
        s2 ^= l2 ^ r2

        state = (s1, s2)
        ans += freq.get(state, 0)
        freq[state] = freq.get(state, 0) + 1

    return str(ans)

def run(inp: str) -> str:
    return solve_text(inp)

assert run("""4
1 3
2 3
2 3
1 3
""") == "2", "sample 1"

assert run("""3
1 2
2 3
1 3
""") == "1", "sample 2"

assert run("""1
1 2
""") == "0", "single interval can never be valid"

assert run("""4
1 3
1 3
1 3
1 3
""") == "4", "four equal intervals, every even-length subarray"

assert run("""2
-1000000000 1000000000
-1000000000 1000000000
""") == "1", "coordinate boundaries and negative values"

n = 200000
max_case = str(n) + "\n" + "\n".join(["-1 1"] * n) + "\n"
assert run(max_case) == str((n // 2) * ((n + 1) // 2)), "maximum-size all-equal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 2` | `0` | Minimum size and the fact that one nonempty interval cannot cancel itself. |
| `4 / 1 3` repeated four times | `4` | Repeated identical intervals and counting every even-length subarray. |
| `2 / -1000000000 1000000000` repeated twice | `1` | Extreme coordinate values and negative coordinates. |
| `200000 / -1 1` repeated | `10000000000` | Maximum (n), large answer, and linear scalability. |

## Edge Cases

The single-lumberjack case

```
1
1 2
```

starts with state (0), then XORs the fingerprints of (1) and (2), producing a nonzero state because the two coordinates are different. The state has not appeared before, so the answer remains (0). This is exactly what we need, since one half-meter contribution cannot become a whole meter.

For two identical intervals,

```
2
1 3
1 3
```

the first interval produces (A_1\oplus A_3). The second applies exactly the same XOR, so the state becomes zero again. The frequency of zero was initially (1), representing (P_0), so the second prefix contributes one valid subarray. The output is (1).

For extreme coordinates,

```
2
-1000000000 1000000000
-1000000000 1000000000
```

the coordinates are normalized to unsigned 64-bit values before hashing. Both occurrences of each endpoint receive identical fingerprints, so the two intervals cancel exactly in the prefix state. The answer is (1), with no special case for negative coordinates.

For the maximum-size all-equal input, every interval has the same endpoint vector. A subarray is valid exactly when it contains an even number of intervals. For (n=200,000), there are (100,000) even-length choices for each suitable starting parity, giving

[
100000\cdot100000=10^{10}
]

valid subarrays. The prefix-state method counts them through repeated alternation between two states, and Python's integer type safely stores the answer.
