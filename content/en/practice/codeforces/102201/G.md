---
title: "CF 102201G - Good Set"
description: "We work inside the Boolean universe of all (k)-bit integers, so there are (2^k) possible elements. A good set is a nonempty family of these integers that is closed under both bitwise AND and bitwise OR."
date: "2026-08-18T01:44:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "G"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 329
verified: true
draft: false
---

[CF 102201G - Good Set](https://codeforces.com/problemset/problem/102201/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We work inside the Boolean universe of all (k)-bit integers, so there are (2^k) possible elements. A good set is a nonempty family of these integers that is closed under both bitwise AND and bitwise OR. The input gives several distinct integers that must all belong to the family, and the task is to count every good family satisfying that requirement.

The key difficulty is that the universe contains at most (128) integers, but a family of them could have (2^{128}) different candidates. Directly enumerating subsets of the universe is impossible. The small bound (k\le 7) is instead telling us that the number of bit positions is tiny. We should exploit the structure of a sublattice of the Boolean lattice rather than the size (2^k) of the universe.

There are two boundary cases that deserve special attention. First, (n=0) means there are no required integers. The empty requirement does not mean that the answer is (0), because every nonempty good set is valid. For example, with (k=1,n=0), the valid sets are ({0}), ({1}), and ({0,1}), so the answer is (3). Second, a singleton is always closed under AND and OR. Thus for (k=2,n=1,a_1=0), the singleton ({0}) must be counted. Forgetting singleton lattices is an easy mistake when building a representation that assumes both the empty set and the full universe are present.

There is another subtle case caused by the word "distinct". An input such as (k=3,n=2) with values (1,1) is invalid, so an "all equal values" test cannot occur in a legal input. The relevant situation is (n=1), where the single required value can have any bit pattern.

## Approaches

The obvious brute force is to enumerate every subset of the (2^k) possible integers, test whether it contains all required values, and then test every pair of elements for closure under AND and OR. Even for (k=7), this means considering (2^{128}) families, which is far beyond reach. The problem is not asking us to optimize a scan over (128) elements. It requires us to avoid enumerating arbitrary families altogether.

The useful observation is that a good family is exactly a sublattice of the Boolean lattice. Every finite sublattice has a minimum element, obtained by ANDing all of its members, and a maximum element, obtained by ORing all of its members. Coordinates that are always (0) or always (1) can be separated immediately. The remaining coordinates are the ones that actually vary inside the family.

Now consider those variable coordinates. Two coordinates are equivalent if every member of the good set gives them the same bit. Equivalently, they always occur together. We can replace each equivalence class by one abstract coordinate. After this compression, every remaining coordinate is genuinely distinguishable by some member of the lattice, so the resulting sublattice has full rank.

A full-rank sublattice of a Boolean lattice of rank (r) is in bijection with a partial order on (r) labeled elements. Given a partial order, take all of its downward-closed subsets. They are closed under intersection and union, and because the order is antisymmetric they distinguish all (r) abstract coordinates. Conversely, from a full-rank sublattice, define (x\le y) when every lattice element containing (y) also contains (x). The resulting relation is a partial order, and the original lattice is exactly its family of ideals.

This turns the original problem into a very small enumeration. We choose which bit positions are variable, partition those positions into equivalence classes, and then choose a partial order on the classes. The required integers impose only one condition on that partial order: every required integer must correspond to an ideal.

For a fixed partition, each block has a signature describing which required integers contain that block. A partial-order relation (x<y) is allowed only when every required integer containing (y) also contains (x). Rather than explicitly constructing that relation constraint, we enumerate the partial orders themselves. Since (k\le7), the number of labeled partial orders is only (1,3,19,219,4231,130023,5941889) for ranks (1) through (7).

The partial orders can be generated recursively. Start with a partial order on (r) labeled vertices and insert a new vertex. Its predecessors form a down-set (D), its successors form an up-set (U), and every element of (D) must be below every element of (U). Every valid pair ((D,U)) gives exactly one extension, so this generates every labeled partial order exactly once.

The final implementation does not construct all ideals of every partial order. For a vertex (v), let (down[v]) be its strict predecessors. A subset (S) fails to be an ideal precisely when it contains (v) but misses some member of (down[v]). We encode all (2^r) subsets as bits of one Python integer. This lets us compute the set of non-ideals of a partial order using only a handful of bit operations, then test every partition against it with one integer AND.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{2^k}\cdot 2^{2k})) | (O(2^k)) | Too slow |
| Structural enumeration | (O(P_7\cdot k\cdot Q_7)) | (O(P_7)) generated states are streamed | Accepted |

Here (P_7=5,941,889) is the number of labeled partial orders on seven elements, and (Q_7) is the number of distinct partition constraints relevant to the input. With (k\le7), all these quantities are small enough for the structural enumeration.

## Algorithm Walkthrough

1. Read the required integers and compute the signature of every bit position. The signature of coordinate (b) is a bitset over the input values, with bit (i) set exactly when (a_i) contains coordinate (b). A coordinate whose signature varies across the required values cannot be fixed inside a valid family, while a constant coordinate may either remain fixed or become part of a variable block.
2. Enumerate every variable-coordinate mask (V) that contains all varying coordinates. Coordinates outside (V) are fixed, and their fixed values are already determined by the common input pattern.
3. For every (V), enumerate every partition of its coordinates into nonempty blocks. A block is valid only when all of its coordinates have the same input signature. Otherwise two coordinates in the same equivalence class would already be distinguished by a required integer, which is impossible.
4. For every valid partition, map each required integer to a subset of the blocks. The subset contains block (j) exactly when that whole block is present in the required integer. Encode the collection of these required block-subsets as one integer `req`, where bit (S) is set if subset (S) occurs among the requirements. Group equal `req` values and keep their multiplicity, because different coordinate partitions can impose the same condition on the abstract partial order.
5. Generate all partial orders on (0,1,\ldots,r-1) recursively. When adding the new vertex (r), choose a down-set (D) of the old order as its predecessors. The possible successors form the common upper bounds of all elements of (D). Any up-set (U) inside that common-upper-bound set gives a valid extension.
6. For every generated partial order, compute a bitset `bad` whose set bits are exactly the subsets that are not ideals. For every vertex (v), every subset containing (v) but not containing all of `down[v]` is bad. The union of these sets over all vertices is the complete non-ideal mask.
7. A partition constraint `req` is satisfied exactly when `req & bad == 0`. Add the multiplicity of every satisfied constraint to the answer for this partial-order rank.
8. The case (n=0) is handled separately. There are no input signatures to constrain the construction, so we use the precomputed numbers of labeled partial orders and a Stirling-number partition count to count all possible fixed-coordinate choices and all possible variable-coordinate partitions.

After processing all partial orders, the accumulated count is exactly the number of distinct good sets containing every required integer.

### Why it works

Every good set has a unique set of coordinates that vary, a unique partition of those coordinates into classes that always behave identically, and a unique full-rank sublattice on those classes. The latter is uniquely represented by a partial order, whose ideals are exactly the possible members of the good set.

The input constraints are preserved exactly because a required integer belongs to the represented lattice if and only if its block representation is an ideal of the chosen partial order. The construction considers every possible coordinate decomposition and every possible partial order, while each resulting good set has only one such canonical decomposition. Hence every valid good set is counted once, and no invalid set is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Number of labeled partial orders on 0..7 elements.
POSets = [1, 1, 3, 19, 219, 4231, 130023, 5941889]

def partitions(mask):
    """Yield every unordered partition of the set bits of mask."""
    if mask == 0:
        yield ()
        return

    bit = mask & -mask
    rest = mask ^ bit

    for p in partitions(rest):
        # Put bit into an existing block.
        for i in range(len(p)):
            q = list(p)
            q[i] |= bit
            yield tuple(q)

        # Start a new block. Blocks stay ordered by their minimum bit.
        yield (bit,) + p

def solve_case(k, a):
    n = len(a)

    if n == 0:
        # g[r] = number of sublattices of B_r containing both
        # the empty set and the full set.
        # g[r] = sum_j S(r,j) * POSets[j].
        stirling = [[0] * 8 for _ in range(8)]
        stirling[0][0] = 1
        for i in range(1, 8):
            for j in range(1, i + 1):
                stirling[i][j] = stirling[i - 1][j - 1] + j * stirling[i - 1][j]

        bounded = [0] * 8
        for r in range(8):
            bounded[r] = sum(
                stirling[r][j] * POSets[j]
                for j in range(r + 1)
            )

        ans = 0
        for r in range(k + 1):
            # Choose r variable coordinates. Every other coordinate
            # can independently be fixed to 0 or 1.
            ans += (
                (1 << (k - r))
                * __import__("math").comb(k, r)
                * bounded[r]
            )
        return ans

    # Signature of every original coordinate.
    # Bit i is set when coordinate b occurs in a[i].
    sig = [0] * k
    for i, x in enumerate(a):
        bit = 1 << i
        for b in range(k):
            if (x >> b) & 1:
                sig[b] |= bit

    # Coordinates with non-constant signatures must be variable.
    varying = 0
    for b in range(k):
        if sig[b] != 0 and sig[b] != (1 << n) - 1:
            varying |= 1 << b

    # queries[r] is a dictionary:
    #   required-ideal-mask -> number of coordinate partitions producing it
    queries = [dict() for _ in range(k + 1)]

    all_coords = (1 << k) - 1

    # Every variable mask must contain all genuinely varying coordinates.
    optional = all_coords ^ varying
    sub = optional

    while True:
        V = varying | sub

        for blocks in partitions(V):
            r = len(blocks)

            # Every block must consist of coordinates with identical
            # signatures among the required elements.
            block_sig = []
            valid = True

            for block in blocks:
                first = block & -block
                b0 = first.bit_length() - 1
                s = sig[b0]

                rest = block ^ first
                while rest:
                    bit = rest & -rest
                    b = bit.bit_length() - 1
                    if sig[b] != s:
                        valid = False
                        break
                    rest ^= bit

                if not valid:
                    break
                block_sig.append(s)

            if not valid:
                continue

            # Convert every required integer into its block mask.
            req = 0
            for i in range(n):
                mask = 0
                ibit = 1 << i

                for j, s in enumerate(block_sig):
                    if s & ibit:
                        mask |= 1 << j

                req |= 1 << mask

            queries[r][req] = queries[r].get(req, 0) + 1

        if sub == 0:
            break
        sub = (sub - 1) & optional

    # For r=0 there is exactly one partial order.
    # Its only subset is the empty set, which is always an ideal.
    answer = 0
    if queries[0]:
        # A legal r=0 representation is a singleton.
        answer += sum(queries[0].values())

    # Process all partial orders of every rank in one recursive generation.
    for target in range(1, k + 1):
        if not queries[target]:
            continue

        # We generate only up to this target. Since targets are processed
        # separately, the code remains simple and k <= 7 keeps this safe.
        qitems = list(queries[target].items())

        contain_all = [0] * (1 << target)
        subset_count = 1 << target
        full_subset_bits = (1 << subset_count) - 1

        for d in range(subset_count):
            x = 0
            s = d
            while s < subset_count:
                x |= 1 << s
                s += 1
            contain_all[d] = x

        # The loop above is intentionally replaced below by a direct
        # construction, which is faster for these tiny dimensions.
        for d in range(subset_count):
            x = 0
            for s in range(subset_count):
                if (s & d) == d:
                    x |= 1 << s
            contain_all[d] = x

        contains_vertex = [
            contain_all[1 << v]
            for v in range(target)
        ]

        local_answer = 0

        def process(down):
            nonlocal local_answer

            bad = 0
            for v in range(target):
                bad |= contains_vertex[v] & (
                    full_subset_bits ^ contain_all[down[v]]
                )

            for req, multiplicity in qitems:
                if (req & bad) == 0:
                    local_answer += multiplicity

        def generate(m, down):
            if m == target:
                process(down)
                return

            old_all = (1 << m) - 1

            up = [0] * m
            for v in range(m):
                mask = 0
                for w in range(m):
                    if (down[w] >> v) & 1:
                        mask |= 1 << w
                up[v] = mask

            size = 1 << m
            is_down = [False] * size
            is_up = [False] * size
            is_down[0] = True
            is_up[0] = True

            for s in range(1, size):
                bit = s & -s
                v = bit.bit_length() - 1
                rest = s ^ bit

                is_down[s] = (
                    is_down[rest]
                    and (down[v] & ~s) == 0
                )
                is_up[s] = (
                    is_up[rest]
                    and (up[v] & ~s) == 0
                )

            xbit = 1 << m

            for D in range(size):
                if not is_down[D]:
                    continue

                # U must consist only of elements strictly above every
                # member of D.
                C = old_all
                bits = D
                while bits:
                    bit = bits & -bits
                    v = bit.bit_length() - 1
                    C &= up[v]
                    bits ^= bit

                U = C
                while True:
                    if is_up[U]:
                        nd = list(down)
                        nd.append(D)

                        bits2 = U
                        while bits2:
                            bit = bits2 & -bits2
                            v = bit.bit_length() - 1
                            nd[v] |= xbit
                            bits2 ^= bit

                        generate(m + 1, tuple(nd))

                    if U == 0:
                        break
                    U = (U - 1) & C

        generate(0, ())
        answer += local_answer

    return answer

def main():
    k, n = map(int, input().split())

    if n:
        a = list(map(int, input().split()))
    else:
        a = []

    print(solve_case(k, a))

if __name__ == "__main__":
    main()
```

The first part of `solve_case` handles (n=0), where there is no required signature information. The number of bounded sublattices of rank (r) is obtained by partitioning the (r) coordinates into equivalence classes and putting a full-rank partial order on those classes. The Stirling numbers count the partitions.

For (n>0), `sig[b]` records exactly which required values contain coordinate (b). The mask `varying` identifies coordinates whose values are not constant across the required input. Such coordinates must be variable in every valid lattice, while every other coordinate may be fixed or variable.

The `partitions` generator uses the smallest remaining coordinate to keep the blocks canonically ordered. This avoids counting the same unordered partition several times.

The dictionary `queries[r]` is the bridge between the original bit positions and the abstract poset. A single dictionary key describes all required subsets that must be ideals. Its multiplicity records how many different coordinate partitions lead to exactly that same abstract requirement.

The recursive `generate` function constructs partial orders by inserting a new largest-labeled vertex. `D` contains its predecessors and `U` its successors. The predecessor set has to be a down-set, the successor set has to be an up-set, and every predecessor has to be below every successor. These conditions are exactly what makes the resulting relation transitive.

The `bad` bitset is the most useful implementation trick. `contain_all[d]` contains every subset mask that contains `d`. For a vertex (v), the expression `contains_vertex[v] & ~contain_all[down[v]]` represents all subsets containing (v) but missing at least one predecessor. Their union is precisely the collection of non-ideals.

Python integers are arbitrary precision, so the bitsets here can safely contain (2^7=128) bits. There is no integer overflow issue. The subset mask for a partition uses at most seven bits, while the outer `req` mask uses at most (128) bits.

## Worked Examples

### Sample 1

The first sample is (k=2,n=1,a_1=0). Since there is only one required value, both bit positions have constant signature (0). They can either be fixed or become variable.

| Variable coordinates | Partition | Number of abstract blocks | Valid partial orders containing 0 |
| --- | --- | --- | --- |
| none | empty partition | 0 | 1 |
| bit 0 | ({0}) | 1 | 1 |
| bit 1 | ({1}) | 1 | 1 |
| both | ({0,1}) | 1 | 1 |
| both | ({0},{1}) | 2 | 3 |

The first four representations give four good sets. The final partition has two blocks, and every partial order on two labeled elements has the empty set as an ideal, so all three partial orders work. The total is (1+1+1+1+3=7), matching the sample output.

This trace also demonstrates why a singleton such as ({0}) must be counted. The zero-block representation is a genuine good set, not an invalid empty family.

### Sample 2

For (k=4) and required values (1,2,7), the coordinate signatures are different enough that several coordinates are forced to remain variable. For every candidate variable mask, the partition step rejects any block containing coordinates whose required signatures differ.

For a surviving partition, each required integer becomes a subset of the abstract blocks. The partial-order generator then counts only orders in which all three of those subsets are ideals.

| Required value | Abstract block mask |
| --- | --- |
| 1 | determined by blocks containing bit 0 |
| 2 | determined by blocks containing bit 1 |
| 7 | determined by blocks containing bits 0, 1, 2 |

Every accepted partial order represents one distinct good set after expanding the abstract blocks back into their original coordinates. Summing all valid partitions and orders gives (29), the sample output.

The important invariant here is that a required value is never checked by explicitly constructing the entire lattice. Its membership is reduced to the single question of whether its abstract block subset is an ideal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(P_7\cdot k + C_k\cdot P_7)) in the worst structural enumeration | (P_7=5,941,889), while (k\le7) and the number of relevant partition constraints is tiny |
| Space | (O(k2^k)) besides recursion | All subset conditions use at most (128) bits, and partial orders are streamed rather than stored |

The crucial difference from brute force is that the algorithm enumerates partial orders on at most seven abstract coordinates instead of arbitrary subsets of a (128)-element universe. The largest labeled partial-order count is about (5.9) million, which is finite and manageable, and the recursive generator never stores all of them simultaneously.

## Test Cases

```python
# This test harness assumes the editorial solution has been placed above
# in a file named solution.py. For a standalone local test, copy the
# solve_case function and main implementation into the same file.

import sys
import io

# Reuse the solve_case function from the solution.
# The helper accepts exactly the input format used by the judge.
def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        k, n = map(int, input().split())
        a = list(map(int, input().split())) if n else []
        print(solve_case(k, a))
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("2 1\n0\n") == "7", "sample 1"
assert run("4 3\n1 2 7\n") == "29", "sample 2"

# Minimum k, one required value.
assert run("1 1\n0\n") == "2", "minimum size"

# Same boundary case, but requiring the other element.
assert run("1 1\n1\n") == "2", "upper boundary"

# Two extreme elements in B_2.
# The valid families are {0,3}, {0,1,3}, {0,2,3}, and the full B_2.
assert run("2 2\n0 3\n") == "4", "fixed minimum and maximum"

# Maximum-size input. Requiring every element forces the entire universe.
assert run(
    "7 128\n" +
    " ".join(map(str, range(128))) +
    "\n"
) == "1", "all elements required"

# No required elements.
assert run("7 0\n") == "12982681", "empty requirement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | 2 | Minimum (k), singleton and full-set cases |
| `1 1 / 1` | 2 | Symmetric upper boundary |
| `2 2 / 0 3` | 4 | Required minimum and maximum, including intermediate lattices |
| `7 128 / 0 ... 127` | 1 | Maximum (n), forcing the unique full universe |
| `7 0` | 12982681 | Empty requirement and the separate (n=0) counting formula |

## Edge Cases

For (k=1,n=1,a_1=0), the input has only the two possible integers, (0) and (1). The good sets containing (0) are ({0}) and ({0,1}), so the answer is (2). The algorithm obtains one representation with no variable coordinates and one with the single coordinate variable.

For (k=2,n=1,a_1=0), the answer is (7). The zero-block representation gives ({0}), one-block representations give ({0,1}), ({0,2}), and ({0,3}), and the two-block representation contributes all three partial orders on two elements. The total is (7).

For (k=2,n=2) with required values (0) and (3), both coordinates vary across the input, so both must belong to the variable part. The one-block partition gives ({0,3}). The two-block partition gives three full-rank sublattices corresponding to the three partial orders on two labeled elements. Thus the answer is (4).

For (k=7,n=128), every possible integer is required. Every bit position varies, so no coordinate can be fixed. Moreover, every coordinate must form its own equivalence class, because the input contains values distinguishing every pair of coordinates. The required block subsets are all (128) subsets of the seven abstract coordinates. The only partial order for which every subset is an ideal is the antichain, whose ideal lattice is the entire Boolean lattice. Hence the answer is exactly (1).

For (n=0), there is no signature information and every coordinate may be fixed to (0), fixed to (1), or placed into one of the variable equivalence classes. For rank (r), the number of bounded sublattices is the Stirling transform of the partial-order counts. Combining this with the choice of variable coordinates and the (2^{k-r}) assignments of fixed coordinates gives (12,982,681) good sets for (k=7). This case cannot be handled by the signature-based requirement check because there are no required values from which to derive signatures.
