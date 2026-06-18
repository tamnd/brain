---
problem: 959F
contest_id: 959
problem_index: F
name: "Mahmoud and Ehab and yet another xor task"
contest_name: "Codeforces Round 473 (Div. 2)"
rating: 2400
tags: ["bitmasks", "dp", "math", "matrices"]
answer: passed_samples
verified: true
solve_time_s: 71
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a339f5b-7da0-83ec-9af1-078177c4b240
---

# CF 959F - Mahmoud and Ehab and yet another xor task

**Rating:** 2400  
**Tags:** bitmasks, dp, math, matrices  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 11s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a339f5b-7da0-83ec-9af1-078177c4b240  

---

## Solution

## Problem Understanding

We are given an array of integers where each value is treated as a 20-bit number. For every query, we look only at a prefix of the array, specifically the first $l$ elements, and we must count how many subsequences of that prefix have XOR equal to a target value $x$. A subsequence here means we can either take or skip each element independently, so every subset of indices in the prefix is valid.

The key output is not a single subsequence but the number of different subsequences whose XOR of selected elements equals the query value, taken modulo $10^9 + 7$.

The constraints immediately rule out enumerating subsequences. The array and number of queries are both up to $10^5$, and each element contributes to a state space of size $2^{20}$ because XOR values lie in $[0, 2^{20})$. Any solution that processes each query by recomputing subset XORs or even maintaining explicit DP per prefix independently would exceed time limits by many orders of magnitude.

A subtle edge case is the empty subsequence. Its XOR is defined as zero, so any query asking for $x = 0$ must include it if we consider a prefix, even when no elements are chosen.

Another important corner case is repeated values or zeros. For example, if the array contains many zeros, each zero doubles the number of subsequences for any fixed XOR target, but only in a structured way that must be consistently propagated through DP transitions.

## Approaches

A direct approach would enumerate all subsequences of the first $l$ elements for each query. For a fixed prefix of length $l$, this is $2^l$, and across queries this becomes impossible as $l$ can be $10^5$. Even computing DP independently per query would cost $O(q \cdot l \cdot 2^{20})$, which is far beyond feasible.

The standard insight for XOR-subset counting problems is that subset XOR behaves like linear combinations over a vector space over GF(2). Each new element either does not change the space of reachable XORs or increases the dimension by one if it is linearly independent from the current basis.

Instead of tracking all subset counts directly, we maintain a linear basis for XOR values along with a global multiplicative factor representing how many different subsets collapse into the same XOR value due to dependent elements.

The key structural fact is that if the current basis has size $k$, then among the first $i$ elements, exactly $2^{i-k}$ subsets correspond to each reachable XOR value in the span of the basis. This uniformity is what makes counting possible: every XOR value in the span has the same number of generating subsets.

For queries, we reduce the target XOR $x$ using the basis. If it is not representable, the answer is zero. If it is representable, the answer is exactly $2^{l-k}$, where $k$ is the number of basis vectors among the first $l$ elements.

To support prefix queries efficiently, we build the basis incrementally and store snapshots of its size and structure at each prefix position. Each query is then answered in $O(20)$ by reducing $x$ against the stored basis.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot 2^l)$ | $O(1)$ | Too slow |
| Optimal | $O((n+q) \cdot 20)$ | $O(n \cdot 20)$ | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a linear XOR basis.

1. Initialize an array of size 20 representing basis vectors, all set to zero. Also precompute powers of two modulo $10^9+7$.
2. For each element $a_i$, insert it into the XOR basis using standard highest-bit elimination. If it becomes zero after reduction, it is dependent and does not increase basis size.
3. Maintain a running count of the basis rank $k_i$ after processing each prefix $i$. Also store the basis snapshot or at least enough structure to answer reductions for that prefix.
4. For a query $(l, x)$, take the basis corresponding to prefix $l$ and attempt to reduce $x$ by eliminating highest bits using stored basis vectors.
5. If after reduction $x$ becomes zero, the answer is $2^{l - k_l}$. Otherwise, the answer is zero.

The reason the reduction works is that the basis represents a spanning set of all achievable XOR values. If a value cannot be reduced to zero, it lies outside the span and no subsequence produces it.

### Why it works

The set of all subset XORs forms a vector space over GF(2). The basis we maintain is a basis of this space. Every subset corresponds to a linear combination of basis vectors plus choices of dependent elements, which only multiply counts without changing representable XOR values. Because each independent element doubles the number of subsets while increasing dimension only when independent, the number of subsets per representable XOR becomes uniform and equals $2^{\text{free dimensions}}$. This invariant holds at every prefix, ensuring correct answers for all queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXB = 20

def build_powers(n):
    pw = [1] * (n + 1)
    for i in range(1, n + 1):
        pw[i] = (pw[i - 1] * 2) % MOD
    return pw

def insert_basis(basis, x):
    for b in reversed(range(MAXB)):
        if not (x >> b) & 1:
            continue
        if basis[b]:
            x ^= basis[b]
        else:
            basis[b] = x
            return True
    return False

def reduce_x(basis, x):
    for b in reversed(range(MAXB)):
        if (x >> b) & 1:
            if basis[b]:
                x ^= basis[b]
    return x == 0

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    basis = [0] * MAXB
    prefix_basis = [None] * (n + 1)
    rank = 0

    prefix_basis[0] = ([0] * MAXB, 0)

    for i in range(1, n + 1):
        new_basis = basis[:]
        before_rank = sum(1 for x in new_basis if x)
        if insert_basis(new_basis, a[i - 1]):
            rank = before_rank + 1
        else:
            rank = before_rank
        basis = new_basis
        prefix_basis[i] = (basis[:], rank)

    pw = build_powers(n)

    out = []
    for _ in range(q):
        l, x = map(int, input().split())
        b, r = prefix_basis[l]
        if reduce_x(b, x):
            out.append(str(pw[l - r]))
        else:
            out.append("0")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation builds a prefix linear basis, storing for each prefix both the basis vectors and its rank. Each query retrieves the stored state and reduces the target XOR against that basis. If the reduction succeeds, the answer is a power of two determined by how many dependent elements exist in the prefix.

A subtle implementation detail is copying the basis per prefix. This ensures queries do not interfere with later updates. The reduction step must proceed from high bits to low bits to match the canonical basis structure.

The rank computation must reflect the number of independent insertions, not simply the number of non-zero vectors in the basis array, since basis maintenance can shift vectors between positions.

## Worked Examples

We use a simplified trace with a small array.

Input:

```
n = 4, q = 2
a = [1, 2, 3, 0]
queries:
(3, 3)
(4, 1)
```

We track basis insertion:

| i | a[i] | Basis after insertion | rank |
| --- | --- | --- | --- |
| 1 | 1 | {1} | 1 |
| 2 | 2 | {1,2} | 2 |
| 3 | 3 | {1,2} (dependent) | 2 |
| 4 | 0 | {1,2} | 2 |

Query (3,3): reduce 3 using basis {1,2}. 3 = 1 xor 2, reducible to 0, so answer is $2^{3-2} = 2$.

Query (4,1): 1 is representable, so answer is $2^{4-2} = 4$.

This trace shows that dependent elements do not increase rank but still double subset count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\cdot 20)$ | Each insertion and query XOR reduction touches at most 20 bits |
| Space | $O(n \cdot 20)$ | Prefix storage of bases |

The complexity fits comfortably within limits since $2 \cdot 10^5 \cdot 20$ operations is well within typical constraints.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    MAXB = 20
    def insert(basis, x):
        for b in reversed(range(MAXB)):
            if (x >> b) & 1:
                if basis[b]:
                    x ^= basis[b]
                else:
                    basis[b] = x
                    return True
        return False

    def reduce_x(basis, x):
        for b in reversed(range(MAXB)):
            if (x >> b) & 1:
                if basis[b]:
                    x ^= basis[b]
        return x == 0

    basis = [0] * MAXB
    pref = []
    rank = 0

    pref.append((basis[:], rank))
    for i in range(n):
        nb = basis[:]
        before = sum(1 for v in nb if v)
        if insert(nb, a[i]):
            rank = before + 1
        else:
            rank = before
        basis = nb
        pref.append((basis[:], rank))

    out = []
    for _ in range(q):
        l, x = map(int, input().split())
        b, r = pref[l]
        if reduce_x(b[:], x):
            out.append(str(pow(2, l - r, MOD)))
        else:
            out.append("0")

    return "\n".join(out)

# provided samples
assert run("""5 5
0 1 2 3 4
4 3
2 0
3 7
5 7
5 8
""") == """4
2
0
4
0"""

# custom cases
assert run("""1 3
0
1 0
1 1
1 0
""") == """2
0
2""", "single zero element"

assert run("""3 2
1 2 3
3 0
3 3
""") == """2
2""", "full basis small"

assert run("""4 2
0 0 0 0
4 0
4 1
""") == """16
0""", "all zeros"

assert run("""5 2
1 1 1 1 1
5 1
5 0
""") == """16
16""", "duplicates collapse"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero element | 2 / 0 / 2 | empty subsequence handling |
| full basis small | 2 / 2 | representable XOR queries |
| all zeros | 16 / 0 | exponential growth with dependencies |
| duplicates collapse | 16 / 16 | rank stability under repetition |

## Edge Cases

A critical edge case is when the array contains only zeros. The basis remains empty for all prefixes, so every prefix of length $l$ has $2^l$ subsequences with XOR equal to zero, and all non-zero queries return zero. The algorithm handles this because reduction fails for non-zero values and rank remains zero.

Another case is when all elements are identical non-zero values. After the first insertion, every subsequent element is dependent. The rank stays at one, and every prefix behaves as a two-state system: XOR is either zero or that value, with counts scaling as powers of two based on dependent insertions.

A final subtle case is queries where $x = 0$. Even when no basis vectors exist, reduction succeeds immediately, and the answer becomes $2^l$, correctly counting all subsets including the empty one.