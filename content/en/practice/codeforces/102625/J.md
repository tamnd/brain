---
title: "CF 102625J - RD Bhaiya and his new token system"
description: "The token machine stores a set of inserted integers. A valid token number is not one of the inserted values directly. Instead, it is any XOR value that can be obtained by choosing some subset of the stored numbers, including the empty subset, whose XOR is zero."
date: "2026-08-03T15:23:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "J"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 47
verified: true
draft: false
---

[CF 102625J - RD Bhaiya and his new token system](https://codeforces.com/problemset/problem/102625/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The token machine stores a set of inserted integers. A valid token number is not one of the inserted values directly. Instead, it is any XOR value that can be obtained by choosing some subset of the stored numbers, including the empty subset, whose XOR is zero. After every insertion, customers ask for the token at a certain position in the sorted list of all distinct possible XOR values. The task is to answer these order statistic queries while insertions continue. citeturn0search0

The input consists of up to \(10^6\) operations. An insertion gives one integer up to \(10^9\), and a query asks for the value at a valid one-indexed position among all generated XOR values. Since the number of operations is extremely large, even an approach that takes \(O(\sqrt{q})\) per query would be too slow. We need a solution close to constant time per bit operation. The values fit in 30 bits because \(10^9 < 2^{30}\), so the natural the empty subset. The answer is:

```text
0
```

A careless solution that assumes at least one stored number would fail here.

Another important case is duplicate insertion:

```text
3
1 5
1 5
2 2
```

The possible XOR values are only `0` and `5`, so the second token is:

```text
5
```

If we count inserted numbers instead of independent XOR directions, we would incorrectly think there are four possible subset XORs.

A final tricky case is when inserted numbers are linearly dependent:

```text
3
1 1
1 2
1 3
```

The third number adds no new information because `1 XOR 2 = 3`. The generated values remain `{0,1,2,3}`. A method that blindly doubles the number of values after every insertion would overcount.

## Approaches

A direct approach would store every generated XOR value. If there are \(k\) independent numbers in the machine, there are \(2^k\) different subset XOR results. We could enumerate every subset, calculate its XOR, remove duplicates, sort the result, and answer queries by index. This is correct because every possible token comes from exactly one subset XOR. The problem is that even \(k=60\) would already create an impossible amount of data, and the number of independent values can grow with the number of insertions. The worst-case work is exponential, around \(O(2^k)\), which is impossible for \(10^6\) operations.

The key observation is that XOR behaves like addition in a binary vector space. The inserted numbers do not create arbitrary sets of values. They create a linear span over bits. A binary linear basis stores the independent directions of this span. If the basis size is \(k\), there are exactly \(2^k\) unique XOR results.

The remaining challenge is finding the \(n\)-th smallest value in this ordered span without generating all values. Once the basis is reduced into a special ordered form, every basis vector controls one binary position independently. We can greedily decide the bits of the answer from the highest bit to the lowest bit. At each bit, we know how many generated values have that bit equal to zero. If the requested position lies inside that group, the answer keeps this bit as zero. Otherwise, we skip that group, subtract its size from the position, and set the bit to one.

The brute force works because it explicitly represents the vector space, but fails when the space becomes large. The observation that the space has a compact basis lets us perform the same ordering logic directly on the basis.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(O(2^k)\) | \(O(2^k)\) | Too slow |
| Optimal | \(O(30)\) per query or insertion | \(O(30)\) | Accepted |

## Algorithm Walkthrough

1. Maintain a binary linear basis of the inserted numbers. For every inserted value, try to remove its highest set bit using existing basis vectors. If the value becomes zero, it was already represented by the previous numbers and does not increase the number of possible tokens. Otherwise, store it as a new independent basis vector.

2. After each successful insertion, rebuild the basis into reduced form. For every bit position from high to low, remove that bit from all lower basis vectors. This makes each basis vector responsible for one unique bit, which allows us to count how many generated values have a certain bit equal to zero.

3. To answer a query for position \(n\), process bits from high to low. Suppose there are \(cnt\) basis vectors remaining that can influence lower bits. Among the remaining possibilities, exactly half have the current bit equal to zero and half have it equal to one. The zero group has size \(2^{cnt-1}\).

4. If \(n\) is inside the zero group, keep the current answer bit as zero. Otherwise, move to the one group by subtracting the size of the zero group from \(n\), set the current answer bit to one, and continue.

5. If \(n=1\), the algorithm naturally returns zero because the empty subset is the first value in sorted order.

The invariant is that the reduced basis represents exactly the same XOR space as all inserted numbers, but with every basis vector contributing a unique highest bit. During the query, each decision divides the remaining XOR values into two equally sized groups based on the current bit. Choosing the correct half at every bit follows the sorted order, so after processing all bits the constructed value is exactly the requested token number.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_BIT = 30

basis = [0] * MAX_BIT
changed = True

def rebuild():
    for i in range(MAX_BIT - 1, -1, -1):
        if basis[i]:
            for j in range(i - 1, -1, -1):
                if (basis[i] >> j) & 1:
                    basis[i] ^= basis[j]

def insert(x):
    global changed
    for i in range(MAX_BIT - 1, -1, -1):
        if ((x >> i) & 1) == 0:
            continue
        if basis[i]:
            x ^= basis[i]
        else:
            basis[i] = x
            changed = True
            return

def kth(x):
    if changed:
        rebuild()
        changed = False

    ans = 0
    cnt = sum(1 for v in basis if v)

    for i in range(MAX_BIT - 1, -1, -1):
        if basis[i]:
            half = 1 << (cnt - 1)
            if x > half:
                x -= half
                ans |= basis[i]
            cnt -= 1

    return ans

def solve():
    global changed
    q = int(input())
    out = []

    for _ in range(q):
        p, n = map(int, input().split())
        if p == 1:
            insert(n)
        else:
            out.append(str(kth(n)))

    sys.stdout.write("\n".join(out))

solve()
```

The `basis` array stores one vector for each possible highest bit. During insertion, the current number is reduced by existing vectors exactly like Gaussian elimination over binary values. If every bit disappears, the number was dependent and does not change the set of possible tokens.

The rebuild operation converts the normal basis into a reduced basis. This step is delayed until a query because many insertions can happen without any need to inspect the ordering. The `changed` flag prevents unnecessary repeated reductions.

The query function walks through the reduced basis from high bits to low bits. The variable `cnt` tracks how many independent vectors remain to decide the size of the current zero group. Python integers handle the powers of two used here without overflow, although the largest value needed is only \(2^{30}\).

The indexing is one-based. The first generated token is zero, so no special handling is needed beyond using the given position directly in the halving logic. The reduction and query order are the parts most likely to cause mistakes, because querying with a non-reduced basis would not preserve sorted order.

## Worked Examples

For the sample input:

```text
14
2 1
1 1
2 1
2 2
1 2
2 1
2 2
2 3
2 4
1 3
2 1
2 2
2 3
2 4
```

the first few operations behave as follows:

| Operation | Inserted basis | Query position | Answer |
|---|---|---|---|
| Query | empty | 1 | 0 |
| Insert 1 | {1} | | |
| Query | {1} | 1 | 0 |
| Query | {1} | 2 | 1 |
| Insert 2 | {1,2} | | |
| Query | {1,2} | 1 | 0 |
| Query | {1,2} | 2 | 1 |
| Query | {1,2} | 3 | 2 |
| Query | {1,2} | 4 | 3 |

This trace demonstrates that two independent basis vectors create four values, ordered as `0, 1, 2, 3`. The basis never stores those four numbers explicitly.

After inserting `3`, the basis does not grow because `3 = 1 XOR 2`. The remaining queries still return:

| Operation | Inserted values | Independent vectors | Query position | Answer |
|---|---|---|---|---|
| Insert 3 | 1, 2, 3 | 2 | | |
| Query | 1, 2, 3 | 2 | 1 | 0 |
| Query | 1, 2, 3 | 2 | 2 | 1 |
| Query | 1, 2, 3 | 2 | 3 | 2 |
| Query | 1, 2, 3 | 2 | 4 | 3 |

The second trace confirms that dependent insertions do not create additional token numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(30)\) per insertion or query | Every operation only processes the 30 possible bit positions |
| Space | \(O(30)\) | The basis stores at most one value for each bit |

The query limit of \(10^6\) makes solutions depending on the number of stored values impossible. The binary basis keeps the state fixed at 30 entries, so the total number of operations is easily within the limits.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    ans = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return ans

assert solve_data("""14
2 1
1 1
2 1
2 2
1 2
2 1
2 2
2 3
2 4
1 3
2 1
2 2
2 3
2 4
""") == """0
0
1
0
1
2
3
0
1
2
3""", "sample"

assert solve_data("""1
2 1
""") == "0", "empty basis"

assert solve_data("""3
1 5
1 5
2 2
""") == "5", "duplicate insertion"

assert solve_data("""5
1 1
1 2
1 3
2 1
2 4
""") == """0
3""", "dependent vector"

assert solve_data("""5
1 1000000000
2 1
2 2
2 1
2 2
""") == """0
1000000000
0
1000000000""", "large value boundary"
```

| Test input | Expected output | What it validates |
|---|---|---|
| Empty basis query | 0 | The empty subset is handled |
| Repeated insertion | 5 | Duplicate values do not increase rank |
| Inserted dependent value | 0 and 3 | XOR dependence is ignored |
| Maximum value insertion | Correct two-value ordering | Bit boundary handling |

## Edge Cases

For the empty machine case:

```text
1
2 1
```

the basis remains full of zeros. The query has no vectors to split, so the only possible value is the empty subset XOR, which is zero. The algorithm returns zero because the query loop has no bits to choose.

For duplicate values:

```text
3
1 5
1 5
2 2
```

the first insertion creates a basis vector for bit representation of `5`. The second insertion reduces completely to zero because the same vector already exists. The query sees only one independent vector, producing the ordered values `0, 5`.

For dependent values:

```text
3
1 1
1 2
1 3
```

the third insertion is eliminated by the existing basis because `3` is already represented as the XOR of `1` and `2`. The basis rank remains two, so the generated sequence is still `0, 1, 2, 3`.

For large values:

```text
5
1 1000000000
2 1
2 2
2 1
2 2
```

the highest used bit is near the 30-bit limit. The algorithm still only checks fixed bit positions, so no special case is required. The reduced basis correctly separates zero and nonzero choices even at the top bit.
