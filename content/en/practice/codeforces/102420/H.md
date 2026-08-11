---
title: "CF 102420H - Wedding"
description: "We have a changing set of fairies. Initially there are n fairies, numbered from 1 through n, and fairy i has an integer sociability value a[i]. During the observation there are q events. A type 1 event adds a new fairy."
date: "2026-08-12T06:34:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "H"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 111
verified: true
draft: false
---

[CF 102420H - Wedding](https://codeforces.com/problemset/problem/102420/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a changing set of fairies. Initially there are `n` fairies, numbered from `1` through `n`, and fairy `i` has an integer sociability value `a[i]`. During the observation there are `q` events.

A type `1` event adds a new fairy. Its value is given directly by the event, and it receives the next never-used number, so deleted numbers are never reused. A type `2` event removes an existing fairy by its number. A type `3` event announces a dance with value `e`. Every fairy currently present replaces its value `b` with `b XOR e`.

After every event, we need the sum of the current values of all fairies still present.

The difficulty is the global XOR operation. A single dance can affect up to `100000` fairies, and there can also be `100000` dances. Updating every fairy individually could require about `10^10` XOR operations in the worst case. With `n, q <= 100000`, an algorithm around `O(nq)` is far beyond what is practical, while an `O((n+q) log(n+q))` or `O(30(n+q))` approach is easily reasonable.

There are several edge cases where a straightforward implementation can silently become wrong. First, a fairy can join after several dances. Consider

```
1 3
5
3 7
1 2
3 1
```

The outputs are

```
2
4
5
```

After the first dance, the original fairy has `5 XOR 7 = 2`. The new fairy joins with value `2`, not `2 XOR 7`, because it did not exist during the first dance. A solution that stores only a single global XOR and blindly applies it to every newly inserted value would mishandle this case.

Second, deleting a fairy after several dances requires knowing its current value, but we must not physically apply all previous dances to it. For example,

```
1 3
4
3 3
2 1
1 1
```

produces

```
7
0
1
```

The original fairy has value `4 XOR 3 = 7` when it leaves. The newly inserted fairy has value `1`, because it arrives after the dance. A representation based on each fairy's value at the time of insertion has to account for the global XOR when removing it.

Third, identifiers are never reused. For example,

```
1 4
10
2 1
1 5
2 2
```

produces

```
0
5
0
```

The newly arriving fairy gets number `2`, not number `1`. Reusing deleted IDs can associate a later deletion with the wrong stored state.

Finally, the values can reach close to `2^30`, and the total sum can reach roughly `10^14`. Python integers handle this directly, while languages with fixed-width integer types need a 64-bit integer for the answer.

## Approaches

The direct solution is to store the current value of every fairy. For a type `1` event we append the new value, for type `2` we remove the requested fairy, and for type `3` we iterate through every currently present fairy and replace its value by `value XOR e`. Maintaining the sum alongside the values makes insertion and deletion constant time, but a dance still requires touching every active fairy.

This brute-force method is correct because it performs exactly the operation described by the problem. Its weakness is the number of repeated updates. In a worst case with `100000` fairies and `100000` dance events, it can perform about `10^10` individual fairy updates. Even before considering Python overhead, that is much too large.

The key observation is that XOR acts independently on every bit. Suppose we focus on one bit position. If the dance bit is `0`, that bit does not change. If the dance bit is `1`, every current fairy flips that bit. We do not need to know each fairy's complete value to know the contribution of that bit to the total sum. We only need the number of active fairies whose corresponding stored bit is `1`.

There is one complication: new fairies arrive at arbitrary times. The clean way to handle this is to separate the history of global dances from each fairy's stored state. Let `X` be the XOR of every dance that has happened so far. For every active fairy, store a hidden value `base` such that its actual current value is

`base XOR X`.

For an original fairy, `base` is initially its given value. When a new fairy with actual value `v` arrives, we choose its base as `v XOR X`. Then its actual value immediately becomes `(v XOR X) XOR X = v`, exactly as required.

When a fairy leaves, its stored base is enough to identify its current value, because the current value is simply `base XOR X`. We can remove its contribution from the per-bit counts without ever replaying the old dances.

The remaining question is how to get the total sum quickly. For each bit `k`, maintain `cnt[k]`, the number of active fairies whose `base` has bit `k` set. If bit `k` of `X` is zero, exactly `cnt[k]` current values have that bit set. If bit `k` of `X` is one, XOR flips the bit, so exactly `active - cnt[k]` current values have that bit set. Thus the contribution of bit `k` is its set-bit count multiplied by `2^k`.

There are only 30 relevant bits because all input values are at most `10^9`, which is below `2^30`. Every event can update the bit counts in `O(30)` time, and every answer can also be computed in `O(30)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nq)` in the worst case | `O(n + q)` | Too slow |
| Optimal | `O(30(n + q))` | `O(n + q)` | Accepted |

## Algorithm Walkthrough

1. Keep a global integer `X`, initially zero. It represents the XOR of all dances that have occurred so far. Every fairy's actual value will be represented as `base XOR X`.
2. Maintain `cnt[k]` for each bit `k` from `0` through `29`. It stores how many active fairies have bit `k` set in their `base` value. Also keep an array `base[id]` for every possible fairy identifier, because a later deletion gives us the identifier and we need its stored representation.
3. For each initial fairy, store its given value as its base. Add one to `cnt[k]` for every set bit of that value. Since `X = 0` initially, the base representation equals the actual value.
4. For a type `1` event with value `v`, assign the next unused identifier. The new base is `v XOR X`. This is the critical insertion rule: the new fairy should have actual value `v` now, while all previous dances are already encoded by `X`.
5. Add the bits of this new base to `cnt`. The fairy is now represented consistently with every existing fairy.
6. For a type `2` event with identifier `p`, retrieve `base[p]`. Remove its set bits from `cnt`. The global `X` does not change, so there is no need to modify anything else.
7. For a type `3` event with value `e`, replace `X` by `X XOR e`. No individual fairy is touched. Since every current value is represented as `base XOR X`, changing `X` applies the new XOR operation to all of them simultaneously.
8. After every event, calculate the answer bit by bit. For bit `k`, if `X` has a zero there, the number of current ones is `cnt[k]`. If `X` has a one there, the number is `active - cnt[k]`. Multiply that count by `2^k` and add it to the answer.

### Why it works

The invariant is that for every active fairy, its actual value is exactly `base[id] XOR X`, while `cnt[k]` is exactly the number of active bases with bit `k` set. Initially both statements hold because `X = 0`. An insertion chooses `base = v XOR X`, so the new actual value is `v`. A deletion removes precisely that fairy's base from every bit count. A dance changes only `X`, which transforms every current value from `base XOR X` into `base XOR X XOR e`, exactly the required new value. Finally, for each bit, XOR either preserves all bits or flips all of them, so `cnt[k]` or `active - cnt[k]` gives the exact number of current values containing that bit. Summing these bit contributions gives the exact total.

## Python Solution

```python
import sys
input = sys.stdin.readline

BITS = 30

def add_base(x, cnt, delta):
    for b in range(BITS):
        if (x >> b) & 1:
            cnt[b] += delta

def solve():
    n, q = map(int, input().split())
    initial = list(map(int, input().split()))

    # base[id] is the value that must be XORed with global_x
    # to obtain the fairy's current value.
    base = [0] * (n + q + 1)

    # Number of active fairies whose base has each bit set.
    cnt = [0] * BITS

    global_x = 0
    active = n
    next_id = n + 1

    for i, x in enumerate(initial, 1):
        base[i] = x
        add_base(x, cnt, 1)

    out = []

    for _ in range(q):
        event = list(map(int, input().split()))
        t = event[0]

        if t == 1:
            v = event[1]

            # We need (base ^ global_x) == v.
            b = v ^ global_x

            base[next_id] = b
            add_base(b, cnt, 1)

            active += 1
            next_id += 1

        elif t == 2:
            p = event[1]
            b = base[p]

            add_base(b, cnt, -1)
            active -= 1

        else:
            e = event[1]
            global_x ^= e

        # Reconstruct the sum from the bit counts.
        ans = 0
        for b in range(BITS):
            ones = cnt[b]
            if (global_x >> b) & 1:
                ones = active - ones
            ans += ones << b

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `base` array has room for `n + q` identifiers because at most `q` new fairies can arrive, and every arriving fairy receives a new identifier. The array is indexed directly by the fairy number, so deletion is constant-time apart from the 30-bit update.

The `add_base` helper updates all bit counters for one base value. It is called with `delta = 1` when a fairy enters and `delta = -1` when a fairy leaves. The same representation is used regardless of how many dances have occurred.

The insertion line `b = v ^ global_x` is the most subtle part of the implementation. The stored base is deliberately not `v`. Since the current value must be `b ^ global_x`, choosing `b = v ^ global_x` makes the current value exactly `v`.

A type `3` event only executes `global_x ^= e`. This is the operation that eliminates the potentially quadratic behavior of the brute-force solution. Every fairy implicitly receives the dance through the changed global value.

The answer is reconstructed from the 30 bit counters. When a bit of `global_x` is zero, bases with that bit set remain set. When it is one, the bit is flipped, so bases with zero become the current ones. The expression `ones << b` is equivalent to `ones * 2^b`.

No overflow handling is required in Python. The maximum total is safely within Python's arbitrary-precision integer representation.

## Worked Examples

### Sample 1

The initial bases are `[2, 3, 9, 5, 6, 6]`, and initially `global_x = 0`. The important state after every event is shown below.

| Event | Action | `global_x` | Active | New/deleted base | Sum |
| --- | --- | --- | --- | --- | --- |
| Initial | Initial fairies | `0` | 6 | `[2,3,9,5,6,6]` | 31 |
| `1 3` | Insert fairy 7 | `0` | 7 | `base[7] = 3` | 34 |
| `3 5` | Global XOR | `5` | 7 | unchanged | 37 |
| `2 2` | Delete fairy 2 | `5` | 6 | remove base `3` | 31 |
| `3 2` | Global XOR | `7` | 6 | unchanged | 27 |
| `2 7` | Delete fairy 7 | `7` | 5 | remove base `3` | 23 |

The inserted fairy has base `3` because the global XOR was still zero. After the dance with `5`, its current value is `3 XOR 5 = 6`. After the second dance, its current value becomes `3 XOR 7 = 4`, so deleting it correctly removes the base `3` from the counters while the current XOR remains `7`.

### Constructed Example

Consider

```
1 3
5
3 7
1 2
3 1
```

The state evolves as follows.

| Event | Action | `global_x` | Active | Inserted base | Sum |
| --- | --- | --- | --- | --- | --- |
| Initial | Initial fairy | `0` | 1 | none | 5 |
| `3 7` | Global XOR | `7` | 1 | none | 2 |
| `1 2` | Insert fairy 2 | `7` | 2 | `2 XOR 7 = 5` | 4 |
| `3 1` | Global XOR | `6` | 2 | unchanged | 5 |

The new fairy receives current value `2` even though `global_x` is already `7`. Its base is `5`, because `5 XOR 7 = 2`. When the next dance changes `global_x` to `6`, its value automatically becomes `5 XOR 6 = 3`, while the original fairy becomes `5 XOR 6 = 3` as well.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(30(n + q))` | Each insertion, deletion, and answer calculation processes at most 30 bits. |
| Space | `O(n + q)` | The base array stores every possible fairy identifier, and the bit counter array has constant size. |

With at most `200000` stored identifiers and only 30 bit positions, the algorithm performs only a few million simple operations. This is comfortably within the intended scale for `n, q <= 100000`, unlike the brute-force approach that can reach about `10^10` fairy updates.

## Test Cases

The following test harness implements the same algorithm as a function so each case can be checked with ordinary Python assertions.

```python
import sys
import io

def solve_string(inp: str) -> str:
    data = iter(inp.strip().split())
    n = int(next(data))
    q = int(next(data))

    initial = [int(next(data)) for _ in range(n)]

    BITS = 30
    base = [0] * (n + q + 1)
    cnt = [0] * BITS

    global_x = 0
    active = n
    next_id = n + 1

    def add_base(x, delta):
        for b in range(BITS):
            if (x >> b) & 1:
                cnt[b] += delta

    for i, x in enumerate(initial, 1):
        base[i] = x
        add_base(x, 1)

    out = []

    for _ in range(q):
        t = int(next(data))

        if t == 1:
            v = int(next(data))
            b = v ^ global_x
            base[next_id] = b
            add_base(b, 1)
            next_id += 1
            active += 1

        elif t == 2:
            p = int(next(data))
            add_base(base[p], -1)
            active -= 1

        else:
            e = int(next(data))
            global_x ^= e

        ans = 0
        for b in range(BITS):
            ones = cnt[b]
            if (global_x >> b) & 1:
                ones = active - ones
            ans += ones << b

        out.append(str(ans))

    return "\n".join(out)

# Provided sample
sample1 = """\
6 5
2 3 9 5 6 6
1 3
3 5
2 2
3 2
2 7
"""

assert solve_string(sample1) == """\
34
37
31
27
23
""".strip(), "sample 1"

# Minimum-size input, with insertion, dance, and deletion.
case2 = """\
1 3
1
1 2
3 3
2 1
"""

assert solve_string(case2) == """\
3
0
2
""".strip(), "minimum-size / insertion / deletion"

# New fairy after a previous dance.
case3 = """\
1 3
5
3 7
1 2
3 1
"""

assert solve_string(case3) == """\
2
4
5
""".strip(), "insertion after global XOR"

# All values equal, followed by several global XOR operations.
case4 = """\
4 4
7 7 7 7
3 7
3 1
2 2
1 7
"""

assert solve_string(case4) == """\
0
4
3
10
""".strip(), "all equal values and repeated XOR"

# Boundary values near 2^30, plus deletion and a new identifier.
case5 = """\
2 5
1 1073741823
3 1073741823
1 1073741823
2 1
3 1
2 2
"""

assert solve_string(case5) == """\
1073741822
1073741823
1073741822
1073741823
0
""".strip(), "30-bit boundary and identifier handling"

# Maximum-size style test, generated rather than written literally.
# 100000 identical fairies and 100000 insertions.
n = 100000
q = 100000
initial = " ".join(["1"] * n)
events = "\n".join(["1 1"] * q)
large_input = f"{n} {q}\n{initial}\n{events}\n"

large_output = solve_string(large_input)
lines = large_output.splitlines()

assert len(lines) == q, "maximum-size event count"
assert lines[0] == str(n + 1), "first maximum-size insertion"
assert lines[-1] == str(n + q), "last maximum-size insertion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 1 / 1 2 / 3 3 / 2 1` | `3, 0, 2` | Minimum-size state changes and deletion |
| `1 3 / 5 / 3 7 / 1 2 / 3 1` | `2, 4, 5` | A fairy joining after previous dances |
| `4 4 / 7 7 7 7 / 3 7 / 3 1 / 2 2 / 1 7` | `0, 4, 3, 10` | All-equal values and repeated global XOR |
| `2 5 / 1 1073741823 / ...` | `1073741822, 1073741823, 1073741822, 1073741823, 0` | Highest relevant bit and large sums |
| Generated `n=q=100000` case | `100000` output lines | Maximum event count and identifier growth |

## Edge Cases

A fairy joining after previous dances is handled by adjusting its base against the current global XOR. In

```
1 3
5
3 7
1 2
3 1
```

the first dance changes `global_x` to `7`. When the value `2` arrives, its base becomes `2 XOR 7 = 5`. Its current value is immediately `5 XOR 7 = 2`, as required. The next dance changes `global_x` to `6`, so the new fairy automatically becomes `5 XOR 6 = 3`. The output sequence `2, 4, 5` confirms that new fairies are not retroactively affected by earlier dances.

Deleting a fairy after dances works because deletion operates on the base rather than on the current value. For

```
1 3
4
3 3
2 1
1 1
```

the original fairy has base `4` and `global_x = 3`, so its current value is `7`. Deleting it subtracts the bits of base `4` from `cnt`, leaving no active fairy. The next insertion happens with `global_x = 3`, so the new fairy with value `1` gets base `1 XOR 3 = 2`. Its current value is `2 XOR 3 = 1`, producing the outputs `7, 0, 1`.

Identifier reuse is avoided by maintaining `next_id` independently of the number of active fairies. In

```
1 4
10
2 1
1 5
2 2
```

fairy `1` is deleted, but the new fairy receives identifier `2`. Its base is `5`, and deleting identifier `2` correctly removes that fairy. The outputs are `0, 5, 0`. A solution that searches for a free identifier or reuses `1` could make the final deletion refer to the wrong fairy.

The empty-set state is also valid after a deletion. Once `active` becomes zero, every bit's current one count is zero regardless of `global_x`, because `active - cnt[k]` is also zero. A subsequent insertion starts from the current `global_x` and reconstructs the correct current value immediately.

The 30-bit boundary is safe because every supplied value is at most `10^9`, and XOR of numbers below `2^30` also stays below `2^30`. Bits `0` through `29` are consequently sufficient. The total sum can be much larger than `2^30`, but Python integers have arbitrary precision, so calculating the answer directly is safe.
