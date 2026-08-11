---
title: "CF 102396D - Cutting Pizza"
description: "We have a circular pizza and (n) people. Person (i) needs one sector whose angle is exactly (alphai) degrees. The sectors can be placed anywhere on the pizza and do not have to appear in the input order. Any unused part of the pizza can stay in the box."
date: "2026-08-11T23:24:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "D"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 662
verified: true
draft: false
---

[CF 102396D - Cutting Pizza](https://codeforces.com/problemset/problem/102396/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular pizza and (n) people. Person (i) needs one sector whose angle is exactly (\alpha_i) degrees. The sectors can be placed anywhere on the pizza and do not have to appear in the input order. Any unused part of the pizza can stay in the box.

A cut can be a radius, which creates one boundary ray, or a diameter, which creates two opposite boundary rays at once. After making all cuts, every requested sector must be one of the resulting sectors, with no extra cut passing through its interior. The task is to minimize the number of cuts and output an actual set of cuts achieving that minimum. The official examples are (4) copies of (90^\circ), two copies of (30^\circ), and (200^\circ,80^\circ,80^\circ).

The small bound (n\le16) is the main algorithmic clue. We cannot afford to enumerate all permutations, since (16!) is about (2.09\cdot10^{13}). Once we also consider which pieces belong to opposite halves of the pizza, a straightforward permutation-based search is far beyond what a one-second limit can tolerate. The intended solution can afford exponential algorithms in (n), but it needs something around (2^n) or (3^n), not factorial time. The fact that every angle is an integer and the whole pizza has only (360^\circ) also gives us a small angular state space, although the cleaner solution uses subset sums rather than a (360)-state geometry DP.

There are several boundary cases that can make a seemingly reasonable implementation wrong. A single request of (180^\circ), for example, needs only one diameter. The input `1 / 180` has answer `1`, because the diameter itself is the two boundaries of the requested half-pizza. Treating every requested sector as requiring two independent radius cuts would output `2`.

Another important case is when the total requested angle is exactly (360^\circ). For `3 / 200 80 80`, the three requested sectors can be placed consecutively around the whole pizza. The three boundary rays are (0,200,280), so only three radius cuts are needed. A solution that always starts with (n+1) cuts would incorrectly count both the beginning and the end as different boundaries, even though they are the same ray after a full revolution.

A more subtle case is `2 / 30 30`. Three radius cuts would be enough if we put the two (30^\circ) sectors next to each other, but two diameter cuts are better. Cutting diameters at (0^\circ) and (30^\circ) creates (30^\circ) sectors at both (0\ldots30) and (180\ldots210). The two requested sectors are opposite copies, so the answer is `2`. This is exactly the kind of symmetry a purely linear arrangement misses.

Finally, an angle larger than (180^\circ) prevents any diameter from being used in the interior of that requested sector. For example, in `3 / 200 80 80`, a diameter would put a cut ray inside the (200^\circ) sector if that sector crossed the diameter. Since every requested piece must be a complete sector with no cut inside it, the large piece forces us toward a radius-only construction.

## Approaches

The most direct brute force is to decide how the requested sectors are arranged around the pizza, which sectors belong to the two semicircles created by a possible diameter, and where the boundaries between groups occur. Even if we only enumerate permutations and binary choices for the two sides, we already get roughly

[
n!,2^n
]

possibilities. At (n=16), this is about (1.37\cdot10^{18}) combinations. Checking each arrangement would also require constructing its boundaries and counting diameter pairings, so this approach is nowhere close to feasible.

The useful observation is that we should not care about the exact identities of the individual cuts while constructing the solution. A diameter is useful because it can serve two opposite boundary rays with one cut. Fix one diameter and call its two rays (0^\circ) and (180^\circ). The requested sectors can then be distributed between the two semicircles. Inside a semicircle, several requested sectors may be placed consecutively, with arbitrary unused gaps between them.

Suppose we want two groups of requested sectors, one on each side of a diameter, to start at the same boundary and finish at another common boundary. Let their total requested angles be (x) and (y). The interval between those two common boundaries must have length at least (\max(x,y)). If (x=y), both groups can simply be placed consecutively. If (x<y), the shorter side can still touch both boundaries if it contains at least two requested sectors, because we can insert the unused gap between its sectors. A one-sector group cannot touch both endpoints unless its angle already equals the interval length.

This gives us the central combinatorial object: a paired block. A paired block consists of a subset (U) of people split into two nonempty subsets (A) and (B), one for each semicircle. Its required length is

[
w(U)=\max\left(\sum_{i\in A}\alpha_i,\sum_{i\in B}\alpha_i\right).
]

The split is valid when both groups can touch both ends of the block. Since one group always has sum (w(U)), only the smaller group needs checking. If its sum is strictly smaller than (w(U)), it must contain at least two sectors so that the missing angle can be inserted as an internal gap. If the two sums are equal, a one-sector group is also fine.

Every paired block gives us one additional common boundary between the two semicircles. A common boundary saves one cut because one diameter can serve both sides. The paired blocks are placed consecutively from (0^\circ) toward (180^\circ).

The remaining requested sectors do not have to be paired. After all paired blocks have been placed, suppose their total length is (P). There are (180-P) degrees left in each semicircle. The remaining sectors must be divided between the two semicircles so that the total angle assigned to each side is at most this remaining capacity. This is just a subset-sum check.

There is one more saving to handle. If one semicircle is filled exactly up to (180^\circ), its beginning and ending rays are opposite and are actually one diameter cut. Thus the beginning and end boundaries should not be counted separately. The same idea handles a complete (360^\circ) radius-only arrangement.

Because (n) is only (16), we can enumerate every subset and compute the best possible paired split for that subset. Then a subset DP partitions some of the people into paired blocks while minimizing the total length consumed by those blocks. For each number of paired blocks, we retain the minimum possible consumed angle. Finally we test whether the unpaired people can fit into the remaining two semicircles.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n!2^n)) | (O(n)) | Too slow |
| Subset DP | (O(n3^n)) | (O(n2^n)) | Accepted |

## Algorithm Walkthrough

1. Compute the total requested angle (S=\sum\alpha_i). The value (S) tells us how much angular space has to be occupied and immediately gives the capacity requirement for two semicircles.
2. For every subset (U), compute its total angle `sum[U]`. We also compute a bitset describing every subset sum obtainable from (U), together with a second bitset containing sums obtainable using at least two elements.
3. For each subset (U) containing at least two people, find the largest possible smaller side of a valid split (U=A\cup B). If the two sides have equal sums, the split is valid immediately. Otherwise the smaller side must contain at least two people, because it needs an internal gap to touch both ends of the paired block.
4. Store the resulting block length and the actual split. If the smaller side has sum (t), the larger side has sum `sum[U] - t`, so the block consumes `sum[U] - t` degrees in each semicircle.
5. Run a subset DP. The state `dp[mask][k]` stores the minimum total length occupied by exactly (k) paired blocks using only people from `mask`. People not included in `mask` are still free and will be placed later.
6. When processing a mask, look at its least significant person. Either leave that person unpaired, or make a paired block containing that person. Restricting every chosen block to contain the least remaining person gives each partition a unique decomposition and avoids counting the same collection of blocks in many orders.
7. For every DP state, let the occupied paired-block length be (P). The remaining capacity of each semicircle is (C=180-P). The unpaired people can be distributed between the two sides exactly when some subset of them has sum between `remaining_sum - C` and `C`. Their subset-sum bitset lets us test this in constant-time bit operations after the DP state is known.
8. Among all feasible states, maximize the number (k) of paired blocks. If several states have the same (k), prefer one where a semicircle can be filled exactly to (180^\circ), because then its two endpoint rays are one diameter cut and save one more cut.
9. Reconstruct the paired blocks from the DP parent pointers. For each paired block, place its first group on the upper semicircle and its second group on the lower semicircle. Both groups start at the current common boundary and end at the next common boundary. If a group's total is smaller than the block length and it contains at least two sectors, put the unused angle between its sectors.
10. Place the remaining people after the paired blocks, splitting them according to the subset-sum reconstruction. Each side now fits inside its remaining (180^\circ) capacity.
11. Collect every ray that is needed as a sector boundary. For each pair of opposite rays (x) and (x+180), emit one diameter if both rays are needed. Otherwise emit a radius for the needed ray. This final compression also handles the (180^\circ) and (360^\circ) boundary cases automatically.

### Why it works

Every useful diameter either creates a boundary needed by both semicircles or identifies the two ends of a semicircle. Between two consecutive common boundaries, the requested sectors on each side form two groups. Their total angles determine the minimum possible distance between the common boundaries, which is exactly the maximum of the two group sums. The validity condition for a shorter group follows from whether it can touch both endpoints.

The DP considers every possible paired group because every valid split of a subset is represented by its subset (U). It also considers every possible collection of disjoint paired groups because the least-set-bit recurrence either leaves the first person unpaired or puts that person into exactly one chosen block. For every number of blocks it keeps the minimum occupied angle, so no state with the same used people and block count can be better for fitting the remaining people.

After the paired blocks are fixed, the only remaining question is whether the unused sectors fit into the two remaining semicircular capacities. The subset-sum test is exactly that condition. Thus every feasible geometric arrangement is represented by some DP state, and every DP state that passes the capacity test can be constructed geometrically. Maximizing the number of paired blocks, followed by taking the (180^\circ) endpoint saving when available, minimizes the number of cuts.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    N = 1 << n
    ALL = N - 1
    INF = 10**9

    total = [0] * N
    reach = [0] * N
    reach2 = [0] * N
    popcnt = [0] * N

    # Bit i in reach[mask] means that this subset of mask
    # can have total angle i.
    reach[0] = 1

    for mask in range(1, N):
        bit = mask & -mask
        i = bit.bit_length() - 1
        rem = mask ^ bit

        total[mask] = total[rem] + a[i]
        popcnt[mask] = popcnt[rem] + 1

        r = reach[rem]
        reach[mask] = r | (r << a[i])

        # At least two elements:
        # either a >=2-element subset already exists in rem,
        # or we take i together with a nonempty subset of rem.
        nonempty = r & ~1
        reach2[mask] = reach2[rem] | (nonempty << a[i])

    # For each subset U:
    # weight[U] = minimum length of a paired block using U.
    # split[U] = one side of the corresponding split.
    weight = array('H', [0]) * N
    split = array('H', [0]) * N

    for mask in range(1, N):
        if popcnt[mask] < 2:
            continue

        s = total[mask]
        half = s // 2

        # First try a perfectly balanced split.
        if s % 2 == 0 and ((reach[mask] >> half) & 1):
            small = half
            need_two = False
        else:
            # Otherwise the smaller side must contain >= 2 elements.
            limited = reach2[mask] & ((1 << (half + 1)) - 1)
            if not limited:
                continue
            small = limited.bit_length() - 1
            need_two = True

        large = s - small

        # The paired block must fit into a semicircle.
        if large > 180:
            continue

        # Recover an actual subset having sum == small.
        x = mask
        target = small
        side = 0

        while target:
            bit = x & -x
            i = bit.bit_length() - 1
            rem = x ^ bit

            source = reach2[rem] if need_two else reach[rem]

            if (source >> target) & 1:
                x = rem
            else:
                side |= bit
                target -= a[i]
                x = rem

        if side == 0:
            continue

        weight[mask] = large
        split[mask] = side

    # dp[mask][k] = minimum total length of k paired blocks
    # using exactly the people in mask.
    K = n // 2
    W = K + 1

    dp = [None] * N
    dp[0] = [INF] * W
    dp[0][0] = 0

    # choice[mask * W + k] is the paired block used to obtain
    # the state. Zero means that the least significant person
    # was left unpaired.
    choice = array('H', [0]) * (N * W)

    for mask in range(1, N):
        bit = mask & -mask
        without = mask ^ bit

        cur = dp[without][:]

        sub = without
        while sub:
            block = sub | bit
            w = weight[block]

            if w:
                rem = mask ^ block
                prev = dp[rem]

                max_k = min(K - 1, popcnt[rem] // 2)

                for k in range(max_k + 1):
                    old = prev[k]
                    if old == INF:
                        continue

                    nw = old + w
                    if nw < cur[k + 1]:
                        cur[k + 1] = nw
                        choice[mask * W + k + 1] = block

            sub = (sub - 1) & without

        dp[mask] = cur

    # We need enough saving to fit everything into two semicircles.
    required = max(0, total[ALL] - 180)

    best_k = -1
    best_mask = -1
    best_p = INF
    best_e = False
    best_left = 0

    # Try the largest number of paired blocks first.
    for k in range(K, -1, -1):
        found = False
        found_e = False
        candidate = None

        for mask in range(N):
            p = dp[mask][k]
            if p == INF or p > 180:
                continue

            capacity = 180 - p
            rem = ALL ^ mask
            rs = total[rem]

            # The remaining people must be split between the
            # two semicircles, each with capacity 'capacity'.
            low = max(0, rs - capacity)
            high = min(capacity, rs)

            if low > high:
                continue

            bits = reach[rem]
            allowed = bits & ((1 << (high + 1)) - 1)

            if low:
                allowed &= ~((1 << low) - 1)

            if not allowed:
                continue

            # Prefer an exact capacity on one side.
            exact = (
                capacity <= high
                and capacity >= low
                and ((bits >> capacity) & 1)
            )

            if exact and not found_e:
                found_e = True
                candidate = (mask, p, capacity, rem, True)
            elif not found_e and candidate is None:
                target = allowed.bit_length() - 1
                candidate = (mask, p, capacity, rem, False)

            found = True

        if found:
            best_k = k
            best_mask, best_p, capacity, rem, best_e = candidate
            break

    # If no partition into two semicircles exists, no diameter can
    # be used without cutting through a requested sector.
    if best_k == -1:
        need = [False] * 360
        need[0] = True

        cur_angle = 0
        for x in a:
            cur_angle += x
            if cur_angle < 360:
                need[cur_angle] = True

        cuts = []
        for ang in range(180):
            x = need[ang]
            y = need[ang + 180]

            if x and y:
                cuts.append((ang, 1))
            elif x:
                cuts.append((ang, 0))
            elif y:
                cuts.append((ang + 180, 0))

        out = [str(len(cuts))]
        out.extend(f"{ang} {typ}" for ang, typ in cuts)
        sys.stdout.write("\n".join(out))
        return

    # Recover the paired blocks.
    blocks = []
    mask = best_mask
    k = best_k

    while mask:
        block = choice[mask * W + k]

        if block:
            blocks.append((block, split[block]))
            mask ^= block
            k -= 1
        else:
            bit = mask & -mask
            mask ^= bit

    blocks.reverse()

    # Recover the remaining people assigned to one semicircle.
    paired_mask = best_mask
    remaining = ALL ^ paired_mask
    capacity = 180 - best_p

    rs = total[remaining]
    low = max(0, rs - capacity)
    high = min(capacity, rs)

    bits = reach[remaining]

    if best_e and ((bits >> capacity) & 1):
        target = capacity
    else:
        allowed = bits & ((1 << (high + 1)) - 1)
        if low:
            allowed &= ~((1 << low) - 1)
        target = allowed.bit_length() - 1

    top_remaining = 0
    x = remaining
    t = target

    while t:
        bit = x & -x
        i = bit.bit_length() - 1
        rem = x ^ bit

        if (reach[rem] >> t) & 1:
            x = rem
        else:
            top_remaining |= bit
            t -= a[i]
            x = rem

    bottom_remaining = remaining ^ top_remaining

    need = [False] * 360
    need[0] = True

    def place_group(mask, start, length):
        if mask == 0:
            return

        ids = []
        x = mask
        while x:
            bit = x & -x
            ids.append(bit.bit_length() - 1)
            x ^= bit

        cur = start

        for j, i in enumerate(ids):
            if j + 1 == len(ids):
                end = start + length
            else:
                cur += a[i]
                end = cur

            need[end % 360] = True

    pos = 0

    # Paired blocks occupy the same interval in both semicircles.
    for block, side_a in blocks:
        side_b = block ^ side_a

        sa = total[side_a]
        sb = total[side_b]
        length = max(sa, sb)

        place_group(side_a, pos, length)
        place_group(side_b, 180 + pos, length)

        pos += length

    # Place unpaired people after all paired blocks.
    def place_consecutive(mask, start):
        cur = start
        x = mask

        while x:
            bit = x & -x
            i = bit.bit_length() - 1
            cur += a[i]
            need[cur % 360] = True
            x ^= bit

    place_consecutive(top_remaining, pos)
    place_consecutive(bottom_remaining, 180 + pos)

    # Compress opposite required rays into diameter cuts.
    cuts = []

    for ang in range(180):
        x = need[ang]
        y = need[ang + 180]

        if x and y:
            cuts.append((ang, 1))
        elif x:
            cuts.append((ang, 0))
        elif y:
            cuts.append((ang + 180, 0))

    out = [str(len(cuts))]
    out.extend(f"{ang} {typ}" for ang, typ in cuts)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation builds subset sums as Python integers used as bitsets. A single bit at position (x) means that angle (x) can be obtained by selecting some people from the subset. Python's arbitrary-precision integers make these subset-sum transitions very compact and fast.

The second bitset, `reach2`, represents sums obtainable using at least two people. This distinction is needed for an unequal paired block. If one side has total (x) and the other has total (y>x), the shorter side needs at least two sectors to touch both ends of the interval. With only one sector, it would have to have angle exactly (y).

The `weight` array stores the minimum interval length of a valid paired block. If a subset has total (s) and its smaller side can have total (t), the larger side has total (s-t), so the interval consumes `s - t` degrees. Choosing the largest possible valid (t) minimizes that interval.

The main subset DP uses the least significant person as a canonical choice. Leaving that person unpaired copies the state from the mask without that person. Otherwise, a paired block containing that person is removed, and its weight is added. This canonical choice prevents the same block partition from being generated in every possible block order.

At the final stage, `dp[mask][k]` tells us how much of the two semicircles has already been reserved by the (k) paired blocks. The complement contains all unpaired people. The subset-sum bitset determines whether those remaining sectors can be divided between the two remaining capacities.

The reconstruction mirrors the DP exactly. A paired block is placed in the same angular interval on both semicircles. If one side has less requested angle than the interval length, the implementation puts the unused angle immediately before the last sector. This guarantees that the first and last rays of the group are still actual requested-sector boundaries.

The final `need` array is deliberately constructed as a set of rays rather than directly emitting cuts. This avoids fragile special cases around (0^\circ), (180^\circ), and (360^\circ). Once all required rays are known, every antipodal pair is naturally represented by one diameter.

Python integers do not overflow here, and the largest subset sum is only (360). The main implementation detail that needs care is the distinction between an angle modulo (360) and the two different rays (0^\circ) and (360^\circ). They are the same ray, so the code always stores angles modulo (360).

## Worked Examples

### Sample 1

The input is:

```
4
90 90 90 90
```

We can divide the four requests into two paired blocks. Each block contains one (90^\circ) sector on each side, so each block has length (90^\circ). The two blocks occupy the full (180^\circ) semicircle.

| Step | Paired block | Upper sum | Lower sum | Block length | Position |
| --- | --- | --- | --- | --- | --- |
| 1 | 90 / 90 | 90 | 90 | 90 | 0 -> 90 |
| 2 | 90 / 90 | 90 | 90 | 90 | 90 -> 180 |

The required rays are (0^\circ,90^\circ,180^\circ,270^\circ). The pairs (0/180) and (90/270) are antipodal, so each pair becomes one diameter.

The output therefore contains two cuts, for example:

```
2
0 1
90 1
```

This demonstrates both sources of savings. Each paired block gives a common boundary, and because the whole semicircle reaches (180^\circ), the two endpoints of that semicircle are one diameter.

### Sample 2

The input is:

```
2
30 30
```

The two requests form one paired block.

| Step | Paired block | Upper sum | Lower sum | Block length | Position |
| --- | --- | --- | --- | --- | --- |
| 1 | 30 / 30 | 30 | 30 | 30 | 0 -> 30 |

The two sectors are placed at (0\ldots30) and (180\ldots210). The required rays are (0^\circ,30^\circ,180^\circ,210^\circ).

| Ray pair | Required? | Cut |
| --- | --- | --- |
| 0 and 180 | both | diameter at 0 |
| 30 and 210 | both | diameter at 30 |

Thus two cuts are sufficient.

This example demonstrates why merely arranging the requests consecutively is not enough. Consecutive placement would use the rays (0,30,60), requiring three cuts. Splitting the requests between opposite semicircles creates one additional shared boundary and reduces the answer to two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n3^n)) | The subset DP considers submasks containing a canonical least element, with up to (O(n)) block-count states. |
| Space | (O(n2^n)) | DP states, subset-sum bitsets, and reconstruction information are stored for all masks. |

For (n\le16), (2^n=65536), so the exponential state space is small enough for the intended solution. The subset-sum operations are especially efficient because they use Python integers as bitsets. The (3^n) transition bound is the part that dominates the running time, but (3^{16}=43,046,721), which is practical with the compact subset representation and pruning by the number of possible paired blocks.

## Test Cases

The following tests validate the produced cuts rather than comparing the exact angles printed by the program, because the problem allows any optimal construction.

```python
# Save the submitted solution as solution.py before running this file.

import subprocess

def run(inp: str) -> str:
    p = subprocess.run(
        ["python3", "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return p.stdout

def validate(inp: str, out: str, expected_min_cuts: int):
    data = list(map(int, inp.split()))
    n = data[0]
    a = data[1:1 + n]

    lines = out.strip().splitlines()
    m = int(lines[0])

    assert m == len(lines) - 1
    assert m == expected_min_cuts

    rays = set()

    for line in lines[1:]:
        angle, typ = map(int, line.split())
        assert 0 <= angle < 360
        assert typ in (0, 1)

        rays.add(angle)

        if typ == 1:
            rays.add((angle + 180) % 360)

    rays = sorted(rays)
    assert rays

    sectors = []
    for i in range(len(rays)):
        x = rays[i]
        y = rays[(i + 1) % len(rays)]
        if i + 1 == len(rays):
            y += 360
        sectors.append(y - x)

    sectors.sort()

    wanted = sorted(a)

    # Every requested sector must occur as a complete atomic sector.
    i = 0
    j = 0
    while i < len(wanted) and j < len(sectors):
        if wanted[i] == sectors[j]:
            i += 1
        j += 1

    assert i == len(wanted)

# Sample 1
sample1 = """\
4
90 90 90 90
"""
out = run(sample1)
validate(sample1, out, 2)

# Sample 2
sample2 = """\
2
30 30
"""
out = run(sample2)
validate(sample2, out, 2)

# Sample 3
sample3 = """\
3
200 80 80
"""
out = run(sample3)
validate(sample3, out, 3)

# Minimum-size input: one 180-degree sector is exactly one diameter.
case4 = """\
1
180
"""
out = run(case4)
validate(case4, out, 1)

# All equal values. Eight opposite pairs of 1-degree sectors
# require nine distinct boundary positions.
case5 = """\
16
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""
out = run(case5)
validate(case5, out, 9)

# Boundary case: the requested sectors fill exactly one semicircle.
case6 = """\
3
60 60 60
"""
out = run(case6)
validate(case6, out, 3)

# A 180-degree subset can be made into one side of a diameter,
# reducing the number of radius cuts.
case7 = """\
3
100 80 50
"""
out = run(case7)
validate(case7, out, 3)
```

The custom cases cover the important structural boundaries:

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 180` | `1` | A single half-pizza is one diameter cut. |
| `16 / sixteen 1s` | `9` | Maximum (n), many paired blocks, and repeated equal angles. |
| `3 / 60 60 60` | `3` | Exact (180^\circ) total and the endpoint-identification case. |
| `3 / 100 80 50` | `3` | A (180^\circ) subset can create a useful diameter even without two symmetric groups. |

## Edge Cases

For a single (180^\circ) request, the input is:

```
1
180
```

The construction places the sector from (0^\circ) to (180^\circ). Both rays belong to the same diameter, so the final compression sees the required pair (0/180) and emits one diameter. The output has exactly one cut.

For a full (360^\circ) arrangement, consider:

```
3
200 80 80
```

No diameter can safely cross the (200^\circ) request, so the solution falls back to consecutive radius cuts. The boundaries are (0,200,280), and after the last (80^\circ) sector the angle returns to (360^\circ=0^\circ). The first and last boundary are the same ray, giving exactly three cuts.

For repeated equal requests, consider:

```
2
30 30
```

The DP finds one paired block containing both people, split as (30/30). Its length is (30^\circ). The sectors are placed from (0) to (30) and from (180) to (210). Both boundary pairs are antipodal, so the two required cuts are diameters at (0^\circ) and (30^\circ).

For the less obvious case:

```
3
100 80 50
```

The (100^\circ) and (80^\circ) sectors can occupy one complete semicircle, from (0^\circ) to (180^\circ). The (50^\circ) sector occupies (180^\circ) to (230^\circ) in the other semicircle. The required rays are (0^\circ,100^\circ,180^\circ,230^\circ). Since (0^\circ) and (180^\circ) are opposite, one diameter replaces two radius cuts. The final answer is three cuts.

The DP handles this last case through the final two-semicircle partition rather than requiring the paired-block DP to manufacture a symmetric pair of requested sectors. This distinction matters because a diameter is allowed to create an extra boundary on the opposite side. The opposite ray does not have to be an endpoint of another requested sector, as long as the extra cut does not pass through a requested sector.

For a maximum-size instance with sixteen equal (1^\circ) requests, the DP can create eight paired blocks. Each pair occupies one degree on opposite semicircles, producing common boundaries at (0,1,\ldots,8). Nine diameter cuts are required. The remaining (172^\circ) on each side is simply unused, so no additional cuts are needed.
