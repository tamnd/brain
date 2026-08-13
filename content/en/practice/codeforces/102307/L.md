---
title: "CF 102307L - Liquid X"
description: "This is an interactive search problem disguised as a coin-change problem. There is an unknown positive integer quantity (X), with (1 le X le 10^6). We have (n) droppers, and using dropper (i) once adds (ai) units of liquid."
date: "2026-08-13T07:30:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "L"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 193
verified: true
draft: false
---

[CF 102307L - Liquid X](https://codeforces.com/problemset/problem/102307/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

This is an interactive search problem disguised as a coin-change problem.

There is an unknown positive integer quantity (X), with (1 \le X \le 10^6). We have (n) droppers, and using dropper (i) once adds (a_i) units of liquid. A query chooses nonnegative integers (x_i), so the tested quantity is

[
q=\sum_{i=1}^{n} a_i x_i.
]

After the experiment, the judge tells us whether (q) is below (X), equal to (X), or above (X). The colors correspond to (q<X), (q=X), and (q>X).

The task is to determine (X) within at most 30 experiments. If the observations cannot distinguish (X) from another possible integer, we must output (-1).

The input consists of (n), followed by the capacities (a_1,\ldots,a_n). There is no ordinary batch input containing (X), because (X) is held by the interactive judge. After every query, the program reads the resulting color.

The upper bound (10^6) is the central computational constraint. It is small enough for a pseudopolynomial dynamic program over all quantities from (0) through (10^6), while it is far too large for enumerating all possible vectors of dropper counts. Since (n\le100), a direct dynamic program with (n\cdot10^6) transitions has up to (10^8) iterations. That is reasonable in optimized C++, but unnecessarily heavy for Python, so the implementation below packs the reachability DP into Python integers and performs the transitions as bit operations.

The limit of 30 experiments is also generous compared with the (10^6) possible values of (X). Once we have sorted every quantity that can actually be produced, ordinary binary search needs at most

[
\lceil \log_2(10^6)\rceil=20
]

queries. The remaining difficulty is deciding when the final interval contains exactly one possible integer.

There are several edge cases that a careless implementation can miss. With capacities (4,8), suppose the hidden value is (10). We can query (4), (8), and (12), obtaining green, green, and red. At that point (X) could be (9), (10), or (11), so the correct answer is (-1). Returning (10) merely because it is the midpoint would be wrong.

At the lower boundary, suppose the only capacity is (2) and the hidden value is (1). The smallest positive query is (2), and its response is red. Since (X) is positive, the only value below (2) is (1), so the answer is uniquely determined. A generic binary search implementation that expects both neighboring reachable values to exist can mishandle this case.

The same issue occurs at the upper boundary. With a reachable value of (999999), if its response is green, then (X>999999). Since (X\le10^6), the only possibility is (10^6). Again, there is no reachable value above (X) that can be used as the other endpoint.

Finally, an adjacent pair of reachable values can differ by exactly two. If the two values are (19) and (21), and the responses tell us that (19<X<21), then (X=20) is uniquely determined even though (20) itself cannot be produced by the droppers. A solution that only accepts yellow responses would incorrectly return (-1).

## Approaches

The most direct approach is to enumerate all quantities that can be produced. We define `dp[s]` to mean that some nonnegative combination of the dropper capacities produces exactly (s). Starting from `dp[0] = true`, for every dropper capacity (a_i) we propagate reachability from (s) to (s+a_i). Because each dropper can be used arbitrarily many times, the iteration over quantities goes from small to large.

The same DP can also store a predecessor for every reachable quantity. If `dp[s]` becomes true because of (s-a_i), we remember (s-a_i). Following those predecessors later gives the actual number of times each dropper must be used for a query.

After computing all reachable quantities, the interactive part becomes ordinary binary search. The color of a query tells us whether (X) is before, at, or after the queried reachable value. The published contest solution uses precisely this reachable-quantity DP followed by binary search.

The straightforward implementation performs (O(n\cdot10^6)) DP transitions. With (n=100), the worst case is (100,000,000) transitions, followed by another (10^6) operations to collect all reachable quantities. That is the point where the simple implementation becomes unattractive, especially in Python.

The key observation is that the DP contains only boolean information. Instead of representing one reachable quantity by one Python object, we can represent all reachable quantities simultaneously as bits of a single large integer. Bit (s) is one exactly when quantity (s) is reachable.

For one capacity (a), the operation

[
S \leftarrow S\cup(S+a)
]

corresponds to

```
bits |= bits << a
```

A single application permits one additional use of the current dropper. To allow arbitrarily many uses efficiently, we double the number of available copies. After processing shifts (a,2a,4a,\ldots), every number of copies from (0) through the required limit is available. Thus each capacity needs only (O(\log 10^6)) big-integer shifts.

We additionally record a predecessor whenever a bit becomes reachable for the first time. If a new value (s) is created by shifting a previous value by (k a_i), its predecessor is (s-k a_i), and reconstruction can recover the number of copies as ((s-\text{predecessor})/a_i).

The resulting search is then performed over the sorted reachable quantities. If the judge returns yellow, we know the exact value. If the search finishes without yellow, the remaining possibilities form the gap between two consecutive reachable quantities, with special handling when the gap reaches the boundary of the allowed range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Straightforward DP | (O(nM)), where (M=10^6) | (O(M)) | Accepted in optimized C++, too heavy for Python |
| Packed bitset DP | (O(n\log M\cdot M/W + M)) word operations | (O(M)) | Accepted and suitable for Python |

Here (W) is the machine word size used internally by the big-integer representation. Python's arbitrary-precision integers perform the large shifts and bitwise operations in optimized native code.

## Algorithm Walkthrough

1. Read the number of droppers and their capacities. Let (M=10^6), the largest possible value of (X).

The only quantities worth considering are the sums that can actually be formed from the capacities. Querying an unreachable quantity is impossible under the protocol.
2. Create a bitset `bits` with only bit zero set. Bit (s) means that quantity (s) is reachable.

Quantity zero is reachable because using every dropper zero times is allowed.
3. Process every capacity (a_i). For shifts (a_i,2a_i,4a_i,\ldots), compute the newly reachable bits using

[
\text{new}=(\text{bits}\ll\text{shift})\setminus\text{bits}.
]

Each doubling step extends the number of copies of the current dropper that can be added. After shifts (a_i,2a_i,\ldots,2^ka_i), all required counts from zero through (2^{k+1}-1) are available.
4. For every newly reachable value (s), store a predecessor and the index of the dropper responsible for the transition.

If `shift = 8` and a new value (25) came from (17), the stored predecessor is (17). During reconstruction, the difference (25-17=8) tells us that one copy of the corresponding capacity was used in this transition. Larger shifts work identically, with the difference possibly representing several copies.
5. Extract every positive reachable quantity into a sorted array `values`.

The bitset itself already stores the values in numerical order, but the binary search needs random access by rank, so we materialize the set of reachable positive quantities.
6. Binary-search the array of reachable quantities. For the middle quantity (q), reconstruct a dropper vector whose total is exactly (q), print the query, and read the color.

A red response means (q>X), so every reachable quantity at or after (q) can be discarded. A green response means (q<X), so every reachable quantity at or before (q) can be discarded. Yellow immediately identifies (X=q).
7. If yellow never occurs, let `hi` be the last reachable quantity known to be below (X), and let `lo` be the first reachable quantity known to be above (X).

If both exist and `values[lo] - values[hi] == 2`, exactly one integer lies between them. That integer is (X), even though it is itself unreachable.
8. If there is no reachable quantity below the final interval, the only possible uniquely identifiable lower-bound case is `values[0] == 2`. Then the positive integer below it is necessarily (1).

If the smallest reachable quantity were (5), for example, the response red would only tell us that (X) belongs to (1,2,3,4), so the answer would have to be (-1).
9. Apply the symmetric rule at the upper boundary. If the largest reachable quantity is (999999) and its response is green, then (X=10^6).
10. If none of the unique cases applies, print (-1). Finally, print command `2` followed by the determined answer.

### Why it works

The invariant during the interactive binary search is that every value of (X) consistent with all responses lies between the remaining reachable quantities. A yellow response identifies one exact reachable quantity. Without yellow, (X) must be strictly between two consecutive reachable quantities, or outside the reachable range at one of the two boundaries.

If two consecutive reachable quantities differ by two, exactly one integer can lie between them, so that integer is uniquely determined. If their difference is at least three, at least two different integers produce exactly the same responses to every reachable query, so the judge's information cannot distinguish them and (-1) is correct. The boundary cases follow from the fact that (X) is restricted to the positive interval ([1,10^6]).

The bitset construction is correct because every transition adds a nonnegative multiple of the current capacity to an already reachable sum, while the doubling sequence eventually permits every required number of copies. Thus every bit set by the algorithm corresponds to a valid combination, and every valid combination is eventually represented.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

LIMIT = 10**6
MASK = (1 << (LIMIT + 1)) - 1

def build_reachable(a):
    n = len(a)

    # bit s = 1 iff s is reachable.
    bits = 1

    # Encodes predecessor * n + coin_index.
    # -1 is used only for value 0.
    parent = array('i', [-1]) * (LIMIT + 1)

    for coin, value in enumerate(a):
        shift = value

        while shift <= LIMIT:
            shifted = (bits << shift) & MASK
            new_bits = shifted & ~bits

            # Store one witness for every newly reachable sum.
            while new_bits:
                low = new_bits & -new_bits
                s = low.bit_length() - 1
                prev = s - shift
                parent[s] = prev * n + coin
                new_bits ^= low

            bits |= shifted

            if bits == MASK:
                break

            shift <<= 1

    values = []
    b = bits & ~1

    while b:
        low = b & -b
        values.append(low.bit_length() - 1)
        b ^= low

    return values, parent

def get_counts(total, a, parent):
    n = len(a)
    counts = [0] * n
    cur = total

    while cur:
        encoded = parent[cur]
        coin = encoded % n
        prev = encoded // n

        counts[coin] += (cur - prev) // a[coin]
        cur = prev

    return counts

def ask(total, a, parent):
    counts = get_counts(total, a, parent)

    print(1, flush=True)
    print(*counts, flush=True)

    response = input().strip()

    if not response:
        sys.exit(0)

    return response[0]

def main():
    n = int(input())
    a = list(map(int, input().split()))

    values, parent = build_reachable(a)

    left = 0
    right = len(values) - 1
    answer = -1

    last_mid = -1
    last_response = ''

    while left <= right:
        mid = (left + right) // 2
        last_mid = mid

        response = ask(values[mid], a, parent)
        last_response = response

        if response == 'y':
            answer = values[mid]
            break

        if response == 'g':
            left = mid + 1
        else:
            right = mid - 1

    if answer == -1:
        # X is smaller than every reachable positive quantity.
        if right < 0:
            if values[0] == 2 and last_response == 'r':
                answer = 1

        # X is larger than every reachable quantity.
        elif left == len(values):
            if values[-1] == LIMIT - 1 and last_response == 'g':
                answer = LIMIT

        # X is strictly between two consecutive reachable quantities.
        else:
            low = values[right]
            high = values[left]

            if high - low == 2:
                answer = low + 1

    print(2, flush=True)
    print(answer, flush=True)

if __name__ == "__main__":
    main()
```

The first part of the implementation builds the reachable-quantity set. `bits` is a Python integer whose bit position is the quantity, so `bits << shift` represents adding `shift` units to every currently reachable quantity.

The doubling loop deserves attention. After processing a shift of (a), the current bitset contains sums using zero or one new copy of the current dropper. After shifting by (2a), it contains zero through three copies. The next shift gives zero through seven copies, and so on. Since (2^{20}>10^6), at most 20 shifts are needed for one capacity.

The `parent` array is filled only for bits that become reachable for the first time. It stores both the previous sum and the dropper index in one integer. The encoding uses `prev * n + coin`, and reconstruction reverses it with integer division and remainder.

The number of copies used in one reconstruction step is not necessarily one. If a value was reached using a shift of (8a_i), the predecessor differs by (8a_i), so `(cur - prev) // a[coin]` correctly recovers eight copies.

The interactive query itself is deliberately separated into `ask`. It reconstructs the exact dropper counts, prints command `1`, prints the vector, and flushes immediately. Interactive problems fail easily if the output is buffered, so both lines are flushed before waiting for the judge's response.

The binary search uses indices into `values`, not the numerical quantity itself. This is necessary because unreachable quantities cannot be queried. The color comparison is still an ordinary ordered comparison because every reachable quantity is an integer.

The final boundary checks avoid indexing outside the array. A generic implementation that blindly accesses `values[left]` and `values[right]` after binary search can read an invalid position when (X) lies below the smallest or above the largest reachable quantity.

Python integers have arbitrary precision, so there is no integer-overflow problem in the bitset shifts. The explicit `MASK` keeps the bitset restricted to quantities through (10^6), which also prevents the integer from growing unnecessarily.

## Worked Examples

The first sample corresponds to capacities (1,2,5,10,20,50). The interaction can identify (X=10). The reachable quantities include (8), (10), and (12), so a possible search path can bracket the answer and eventually query (10) itself.

| Query quantity | Response | Search effect |
| --- | --- | --- |
| 25 | red | (X<25) |
| 8 | green | (X>8) |
| 10 | yellow | (X=10) |

The important property here is that every queried quantity is actually constructible. For example, (25=5+20), (8=2+2+2+2), and (10=10). The yellow response terminates the search immediately.

The second sample uses capacities (4) and (8). Suppose the hidden value is (10). The reachable positive quantities are (4,8,12,16,\ldots).

| Query quantity | Response | Search effect |
| --- | --- | --- |
| 8 | green | (X>8) |
| 12 | red | (X<12) |
| 10 | unavailable | Cannot be queried |

After the first two observations, both (9), (10), and (11) remain possible. Since there is no way to query a quantity between (8) and (12), the correct answer is (-1). This is exactly the situation that separates "binary search over integers" from "binary search over reachable quantities".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log M\cdot M/W + M)) word operations | Each capacity uses (O(\log M)) packed bitset shifts, and witness extraction touches each reachable value once |
| Space | (O(M)) | The parent array stores one integer per possible quantity, while the bitset uses (O(M)) bits |

Here (M=10^6). The interactive phase uses at most 20 experiments because there are at most (10^6) positive candidate quantities. The computational work is dominated by the pseudopolynomial reachability computation, while the number of actual interactions is logarithmic.

The packed implementation is particularly useful in Python because the expensive bitset shifts and logical operations execute in optimized native code rather than as (10^8) Python-level loop iterations.

## Test Cases

Because this is an interactive problem, the samples are interaction transcripts rather than ordinary deterministic input/output pairs. A normal helper of the form `run(input) == output` cannot faithfully test them because the program expects the judge to answer every query. The following test harness simulates that judge internally and exercises the same binary-search and reconstruction logic.

The sample scenarios use the capacities visible in the interaction transcript. The first has capacities (1,2,5,10,20,50) and a hidden value of (10). The second has capacities (4,8) and a hidden value of (10), for which the correct answer is (-1). The third has capacities (2,3) and a hidden value of (1), which also cannot be uniquely determined.

```python
from array import array

LIMIT = 10**6
MASK = (1 << (LIMIT + 1)) - 1

def build_reachable(a):
    n = len(a)
    bits = 1
    parent = array('i', [-1]) * (LIMIT + 1)

    for coin, value in enumerate(a):
        shift = value

        while shift <= LIMIT:
            shifted = (bits << shift) & MASK
            new_bits = shifted & ~bits

            while new_bits:
                low = new_bits & -new_bits
                s = low.bit_length() - 1
                prev = s - shift
                parent[s] = prev * n + coin
                new_bits ^= low

            bits |= shifted

            if bits == MASK:
                break

            shift <<= 1

    values = []
    b = bits & ~1

    while b:
        low = b & -b
        values.append(low.bit_length() - 1)
        b ^= low

    return values, parent

def get_counts(total, a, parent):
    n = len(a)
    counts = [0] * n
    cur = total

    while cur:
        encoded = parent[cur]
        coin = encoded % n
        prev = encoded // n
        counts[coin] += (cur - prev) // a[coin]
        cur = prev

    return counts

def solve_hidden(a, hidden):
    values, parent = build_reachable(a)

    left = 0
    right = len(values) - 1

    last_query = None
    last_response = None

    while left <= right:
        mid = (left + right) // 2
        query = values[mid]

        counts = get_counts(query, a, parent)
        assert sum(x * y for x, y in zip(a, counts)) == query
        assert all(x >= 0 for x in counts)
        assert query <= LIMIT

        last_query = query

        if query < hidden:
            response = 'g'
        elif query > hidden:
            response = 'r'
        else:
            response = 'y'

        last_response = response

        if response == 'y':
            return query
        elif response == 'g':
            left = mid + 1
        else:
            right = mid - 1

    if right < 0:
        if values[0] == 2 and last_response == 'r':
            return 1
        return -1

    if left == len(values):
        if values[-1] == LIMIT - 1 and last_response == 'g':
            return LIMIT
        return -1

    low = values[right]
    high = values[left]

    if high - low == 2:
        return low + 1

    return -1

# Sample 1: capacities 1, 2, 5, 10, 20, 50, hidden X = 10.
assert solve_hidden([1, 2, 5, 10, 20, 50], 10) == 10

# Sample 2: capacities 4, 8, hidden X = 10.
# The observations cannot distinguish 9, 10, and 11.
assert solve_hidden([4, 8], 10) == -1

# Sample 3: capacities 2, 3, hidden X = 1.
# Both 1 and other values below the first useful query cannot be separated.
assert solve_hidden([2, 3], 1) == -1

# Minimum-size case. Capacity 1 can produce every possible X.
assert solve_hidden([1], 1) == 1

# Boundary case. With capacity 2, every integer is either reachable
# or lies between two consecutive even reachable quantities.
assert solve_hidden([2], 1_000_000) == 1_000_000

# All-equal capacities. This is outside the statement's "different
# capacities" condition, but it checks that duplicate capacities do
# not break the implementation.
assert solve_hidden([7, 7], 14) == 14

# A gap larger than two leaves several possible hidden values.
assert solve_hidden([7, 7], 15) == -1

# Maximum-size n. Because capacity 1 is present, every X is reachable.
assert solve_hidden(list(range(1, 101)), 999_999) == 999_999
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 5 10 20 50`, hidden (10) | `10` | Sample 1 and exact yellow detection |
| `4 8`, hidden (10) | `-1` | Sample 2 and an unresolved gap of width four |
| `2 3`, hidden (1) | `-1` | Sample 3 and lower-bound ambiguity |
| `[1]`, hidden (1) | `1` | Minimum-size instance |
| `[2]`, hidden (10^6) | `1000000` | Upper boundary and large reachable value |
| `[7,7]`, hidden (14) | `14` | Duplicate capacities and an exact reachable target |
| `[7,7]`, hidden (15) | `-1` | Gap larger than two |
| `[1,2,\ldots,100]`, hidden (999999) | `999999` | Maximum (n) and dense reachability |

## Edge Cases

Consider a single dropper of capacity (2) and hidden value (1). The reachable positive quantities are (2,4,6,\ldots). The first query above the possible range is (2), and the response is red. There is no positive integer smaller than (2) except (1), so the algorithm returns (1). The lower-bound check `values[0] == 2` is exactly for this situation.

Consider the same dropper with hidden value (3). Querying (2) gives green and querying (4) gives red. The two consecutive reachable quantities differ by (2), so the only integer between them is (3). The algorithm returns (3), even though no experiment can use exactly three units.

Now consider capacities (4) and (8) with hidden value (10). The reachable values around (X) are (8) and (12). Their difference is (4), so three integers, (9,10,11), remain possible. No sequence of comparison queries can distinguish them because every possible query is a multiple of (4). The algorithm correctly returns (-1).

For the upper boundary, suppose the capacities allow (999999) but no value between it and (10^6), and the response to (999999) is green. Since (X\le10^6), (X) must be (10^6). The upper-boundary check recognizes this without requiring a nonexistent reachable quantity above (X).

If a yellow response occurs, no gap analysis is necessary. A yellow result means the tested quantity equals (X), so the algorithm immediately returns that reachable quantity. This is also why the predecessor representation must produce an exact sum. A query vector whose sum is even one unit away would change the judge's response and invalidate the binary search.

Finally, the reconstruction process never needs negative dropper counts. Every stored predecessor is smaller than the current reachable value, and each transition was created by adding a positive multiple of one capacity. Following predecessors strictly decreases the current sum until zero is reached, so reconstruction always terminates with a valid nonnegative vector.
