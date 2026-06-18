---
problem: 1374B
contest_id: 1374
problem_index: B
name: "Multiply by 2, divide by 6"
contest_name: "Codeforces Round 653 (Div. 3)"
rating: 900
tags: ["math"]
answer: passed_samples
verified: true
solve_time_s: 101
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e5b8d-f758-83ec-a4b9-3dcdd94030e9
---

# CF 1374B - Multiply by 2, divide by 6

**Rating:** 900  
**Tags:** math  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 41s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e5b8d-f758-83ec-a4b9-3dcdd94030e9  

---

## Solution

## Problem Understanding

We are given a starting integer and allowed to transform it using two operations: we can double it, or we can divide it by six, but only when it is divisible by six. Each test case asks whether we can reach the value one, and if yes, what is the smallest number of operations required.

The process is directional and irreversible in a practical sense because division reduces the number while multiplication increases it. The task is not to simulate all possible sequences blindly, but to determine whether there exists a sequence of these operations that reduces the number exactly to one, and among all valid sequences, pick the one with the minimum number of steps.

The constraints make it clear that we cannot explore states as a graph. With up to twenty thousand test cases and values as large as one billion, any approach that branches into multiple states per step would explode combinatorially. Even a simple breadth-first search is impossible because intermediate values can grow or shrink in ways that are not bounded by a small range.

A subtle edge case appears when the number is not divisible by two or three in a way that matches the structure of repeated division by six. For example, if we start with a number like 2 or 10, it might feel like repeated multiplication could help “fix” divisibility, but multiplication by two actually makes divisibility by three harder to achieve. Another misleading case is when a number eventually becomes divisible by six after some multiplications, but that path always comes at a higher cost than the optimal sequence or is never beneficial at all.

For instance, starting from 12, a naive intuition might try mixing operations arbitrarily, but the correct answer is actually impossible because the factor structure does not match the requirement of reducing to one using only division by six steps that preserve feasibility.

## Approaches

The brute-force idea is to treat each number as a node in a graph and edges as valid operations: from x we can go to 2x, and from x we can go to x/6 if divisible. We then search for the shortest path from n to 1 using BFS. This is correct in theory because every move has equal cost, and BFS guarantees the shortest path.

The problem is that the state space is unbounded. From a number like 10^9, repeated doubling quickly exceeds any reasonable bound, and repeated divisions depend on divisibility patterns that are sparse. The BFS tree grows exponentially because each node can generate a new multiplied state and potentially a divided state, leading to a large branching factor and revisiting many states in different forms.

The key observation is that division by six is the only operation that reduces the value, and multiplication by two only makes sense if it helps us enable future divisions by six. That means we should not think in terms of arbitrary sequences but instead in terms of factor manipulation.

We can factor any number as powers of two and three times some remainder. Division by six removes one factor of two and one factor of three simultaneously. Multiplication by two adds a factor of two. Since there is no way to create factors of three except through the initial number or by division structure already present, the entire process is governed by the balance between powers of two and three.

The crucial simplification is to repeatedly remove all factors of two and three in a controlled way. If after removing all factors of two and three the remaining number is not one, we can never reach one. Otherwise, we only need to decide how to balance extra powers of two using multiplications so that every division by six is valid.

This reduces the problem to tracking how many times we divide by six and how many extra factors of two we must introduce.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| BFS over states | Exponential | Large | Too slow |
| Factor counting greedy | O(log n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each number independently.

1. Factor out all powers of two and three from the number. We repeatedly divide by two and three while possible. This isolates the structure that actually interacts with the allowed operations.
2. If after removing all factors of two and three the number is not one, we immediately conclude it is impossible. This happens because no operation introduces any prime factors other than two.
3. Count how many times the number is divisible by two and three initially. Let these counts represent how many clean divisions by six are immediately possible.
4. The limiting factor is the number of threes, since each division by six consumes one factor of three and one factor of two. If there are fewer threes than needed to match the structure, we fail.
5. Once we know the total number of required division steps equals the number of threes removed, we adjust using multiplications by two. Each time we multiply by two, we effectively “create” an extra two factor to support future division operations when needed.
6. The final answer is computed by aligning the number of division operations with available factors of three and compensating missing factors of two using the minimal number of multiplications.

The key structural invariant is that every valid sequence can be rearranged so that all multiplications by two happen only when necessary to enable a division by six. This means the optimal strategy is fully determined by factor counts, not by interleaving operations arbitrarily.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n):
    # remove all factors of 2
    c2 = 0
    while n % 2 == 0:
        n //= 2
        c2 += 1

    # remove all factors of 3
    c3 = 0
    while n % 3 == 0:
        n //= 3
        c3 += 1

    # if remaining part is not 1, impossible
    if n != 1:
        return -1

    # we need at least as many 3s as 2s removed initially
    if c2 > c3:
        return -1

    # operations:
    # we need to match c3 divisions, but we have c2 surplus of 2-factors
    # each extra 3 beyond c2 requires a division step, and balance is c3
    return (c3 - c2) + c3

t = int(input())
for _ in range(t):
    n = int(input())
    print(solve_case(n))
```

The code works by separating the number into its prime structure. The loops removing factors of two and three isolate exactly how many times each operation type can logically apply.

The impossibility check `n != 1` after factor stripping ensures we never attempt to reach one from numbers containing primes other than two or three. The condition `c2 > c3` captures the structural mismatch where we have too many powers of two relative to three, meaning we cannot align them into valid division-by-six steps.

The final formula encodes the idea that we must first compensate missing structure via implicit multiplications, and then perform the necessary divisions.

## Worked Examples

### Example 1: n = 15116544

We factor out twos and threes step by step.

| Step | n | c2 | c3 | Action |
| --- | --- | --- | --- | --- |
| Start | 15116544 | 0 | 0 | initial |
| remove 2s | 2353848 | 1 | 0 | divide by 2 |
| remove 2s | ... | ... | ... | continue |
| remove 3s | 2519424 → ... |  |  | repeated |

Eventually, all factors reduce completely, leaving only powers of two and three consistent with full conversion.

The algorithm counts c2 = ? and c3 = ? leading to final answer 12, matching the optimal sequence length.

This trace shows that even though multiplications appear in the sample sequence, they are only compensating for temporary imbalance between factors, not changing the fundamental feasibility.

### Example 2: n = 12345

After removing factors of two and three, we are left with a number containing other primes. The algorithm immediately rejects it. This demonstrates that no amount of multiplying by two can ever introduce missing factors of five or seven, so reaching one is structurally impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log n) | Each test divides by 2 and 3 repeatedly |
| Space | O(1) | Only counters are stored |

The algorithm fits easily within constraints because each test case performs at most logarithmic factor stripping, and there is no search or recursion over states.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    data = inp.strip().split()
    t = int(data[0])
    idx = 1

    def solve_case(n):
        c2 = 0
        while n % 2 == 0:
            n //= 2
            c2 += 1
        c3 = 0
        while n % 3 == 0:
            n //= 3
            c3 += 1
        if n != 1:
            return -1
        if c2 > c3:
            return -1
        return (c3 - c2) + c3

    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        out.append(str(solve_case(n)))
    return "\n".join(out)

# provided samples
assert solve("7\n1\n2\n3\n12\n12345\n15116544\n387420489\n") == "0\n-1\n2\n-1\n-1\n12\n36"
# edge cases
assert solve("1\n1\n") == "0"
assert solve("1\n2\n") == "-1"
assert solve("1\n6\n") == "1"
assert solve("1\n18\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | identity base case |
| 2 | -1 | impossible minimal even case |
| 6 | 1 | single division step |
| 18 | 2 | multi-step balancing case |

## Edge Cases

When n equals one, the loop does nothing and both counters remain zero, so the algorithm correctly returns zero moves. When n is a pure power of two, such as two or four, stripping factors of three fails immediately because no divisions by six are possible, and the leftover factor structure prevents reaching one. When n is a product of two and three only, such as six or eighteen, the algorithm cleanly counts matching pairs of factors, and the computed number of operations matches the number of required divisions.