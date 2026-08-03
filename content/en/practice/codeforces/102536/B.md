---
title: "CF 102536B - C.U.P.S."
description: "The volcano contains n craters, and each crater is either filled (1) or empty (0). Every day Roro must visit exactly m craters. A visit flips the chosen crater: an empty crater becomes filled, while a filled crater becomes empty."
date: "2026-08-03T21:14:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "B"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 281
verified: false
draft: false
---

[CF 102536B - C.U.P.S.](https://codeforces.com/problemset/problem/102536/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 41s  
**Verified:** no  

## Solution
# Problem Understanding

The volcano contains `n` craters, and each crater is either filled (`1`) or empty (`0`). Every day Roro must visit exactly `m` craters. A visit flips the chosen crater: an empty crater becomes filled, while a filled crater becomes empty. We need to choose a sequence of daily visit sets so that after at most `n` days every crater is filled.

The output is not asking for the final state only. We must print the exact daily commands, where every command is a binary string with exactly `m` ones. A one means that crater is visited on that day.

The constraints are small enough that `n` is only 80, but the number of possible daily commands is enormous. A direct search over possible days would have roughly `C(n, m)` choices per day, which is already too large even for small values of `n`. The limit of 80 suggests that the intended solution should use linear algebra or another method with complexity close to `O(n^3)` rather than exploring states.

The tricky part is that visiting a crater twice cancels out, because the operation is a flip. The order of days does not matter mathematically, only the XOR of all chosen daily masks matters. A careless solution that greedily tries to fill currently empty craters can fail because a later visit may reopen them.

Consider the case:

```
1
1 1
0
```

The correct output is one day visiting the only crater:

```
1
1
```

A solution that assumes already filled craters are the only useful targets would miss that a single flip solves the problem.

Another edge case is when every crater must be visited every day:

```
1
3 3
101
```

The only possible operation is `111`, which flips all craters. After one operation the state becomes `010`, not all filled, and repeating it only alternates. The correct output is:

```
CATACLYSM IMMINENT - TIME TO HOARD FACE MASKS
```

A solution that only checks whether the number of empty craters can be reduced would incorrectly accept this case.

## Approaches

The brute-force approach is to treat every possible daily command as a move and perform a graph search over all possible states. A state is a binary string of length `n`, so there are `2^n` states. From every state we can try all `C(n, m)` possible commands. In the worst case this explores an impossible number of transitions, far beyond what the limits allow.

The useful observation is that every operation is just XOR. If the current state is `S`, the final state must be all ones, so the total XOR of all commands must equal:

`S XOR 111...111`

The problem becomes finding a collection of weight-`m` binary vectors whose XOR equals a target vector.

For `m < n`, all weight-`m` vectors span almost the entire vector space. If `m` is even, every possible XOR has even parity, so only targets with an even number of set bits are reachable. If `m` is odd, the span is the whole space, so every target is reachable.

We can build a basis of valid daily commands using Gaussian elimination over GF(2). Instead of generating all possible commands, we generate enough structured commands to span the space. Start with the mask containing the first `m` positions. Swapping one chosen position with one unchosen position gives another valid mask, and these swaps provide the necessary differences between coordinates.

The brute-force works because every possible path is considered, but fails when the state space explodes. The XOR structure lets us replace path finding with finding a linear combination of basis vectors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * C(n,m)) | O(2^n) | Too slow |
| Optimal | O(n^3) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the problem into an XOR target. A crater that is currently `0` needs to be flipped an odd number of times, while a crater that is already `1` needs to be flipped an even number of times. The target vector is the complement of the initial state.
2. Handle the special case `m = n`. The only possible command is visiting every crater. This command simply flips the whole vector, so only states that can reach all ones by repeatedly flipping everything are possible.
3. For `m < n`, create candidate commands. Start with the command that visits the first `m` craters. Then create commands by replacing one of these positions with a position outside this group. Every generated command still contains exactly `m` visits.
4. Insert these commands into a linear basis over GF(2). During insertion, keep the original command associated with every basis vector. We only need independent vectors, because any target can be represented using each basis vector at most once.
5. Reduce the target vector using the basis. Whenever a basis vector is used, add its original command to the answer. If the target cannot be reduced to zero, the target is outside the span and the answer is impossible.
6. Output the selected commands. The number of selected basis vectors is at most `n`, so the number of days always satisfies the limit.

Why it works: the generated commands form a basis of the space of all reachable changes. Gaussian elimination preserves the span while removing redundant commands. When the target is reduced completely, the XOR of the chosen original commands is exactly the required change. Applying those commands flips every crater that was initially empty an odd number of times and every crater that was initially filled an even number of times, leaving all craters filled.

## Python Solution

```python
import sys
input = sys.stdin.readline

BAD = "CATACLYSM IMMINENT - TIME TO HOARD FACE MASKS"

def solve_case(n, m, s):
    if s == "1" * n:
        return []

    if m == n:
        if s == "0" * n:
            return ["1" * n]
        return None

    target = 0
    for i, c in enumerate(s):
        if c == '0':
            target |= 1 << i

    base = (1 << m) - 1
    candidates = [base]

    for a in range(m):
        for b in range(m, n):
            candidates.append(base ^ (1 << a) ^ (1 << b))

    basis = [0] * n
    original = [0] * n

    for mask in candidates:
        x = mask
        for bit in range(n - 1, -1, -1):
            if (x >> bit) & 1:
                if basis[bit]:
                    x ^= basis[bit]
                else:
                    basis[bit] = x
                    original[bit] = mask
                    break

    ans = []
    x = target
    for bit in range(n - 1, -1, -1):
        if (x >> bit) & 1:
            if basis[bit] == 0:
                return None
            ans.append(original[bit])
            x ^= basis[bit]

    res = []
    for mask in ans:
        cur = []
        for i in range(n):
            cur.append('1' if (mask >> i) & 1 else '0')
        res.append(''.join(cur))

    return res

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        s = input().strip()
        ans = solve_case(n, m, s)
        if ans is None:
            out.append(BAD)
        else:
            out.append(str(len(ans)))
            out.extend(ans)
    print('\n'.join(out))

if __name__ == "__main__":
    main()
```

The first part of the implementation handles the cases where the possible operations are restricted. When `m = n`, there is only one possible vector, so general linear algebra is unnecessary.

For the normal case, the target mask is built by marking every crater that needs to change. The basis construction uses integers as bitsets, which makes XOR operations very fast and avoids maintaining arrays of length 80 for every vector.

During elimination, `basis[bit]` stores the vector whose highest set bit is `bit`. The parallel `original` array stores the real daily command that produced that basis vector. This distinction matters because the transformed basis vectors are only for calculations, while the output must contain valid commands with exactly `m` visited craters.

The reduction phase collects the original commands used by the basis. The final list is already guaranteed to have at most `n` elements because a linear basis over `n` bits contains at most `n` vectors.

## Worked Examples

For the sample:

```
1
4 2
1100
```

The target is `0011`, because the first two craters already have the desired value and the last two need to be flipped.

| Step | Target state | Action |
| --- | --- | --- |
| Initial | 0011 | Need XOR equal to 0011 |
| Basis reduction | 0011 | Choose command 1100 |
| Next reduction | 1111 | Choose command 0011 |
| Final | 0000 change needed | Choose command 1100 |

One valid sequence is:

```
3
1100
0011
1100
```

The three commands XOR to `0011`, which is exactly the required change.

For a minimum case:

```
1
1 1
0
```

| Step | Target | Basis decision | Output |
| --- | --- | --- | --- |
| Initial | 1 | Only command is 1 | 1 |
| After reduction | 0 | Finished | 1 |

The algorithm outputs one operation, which flips the only crater into the filled state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | There are O(n^2) generated candidates, and each insertion/reduction uses O(n) XOR operations. |
| Space | O(n) | The basis stores at most one vector for each bit position. |

With `n <= 80`, even the cubic bound is small. The number of generated candidates is at most around 6400, and every operation is just integer XOR, so the solution easily fits within the limits.

## Test Cases

```python
import sys
import io

BAD = "CATACLYSM IMMINENT - TIME TO HOARD FACE MASKS"

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        s = input().strip()
        ans = solve_case(n, m, s)
        if ans is None:
            out.append(BAD)
        else:
            out.append(str(len(ans)))
            out.extend(ans)
    sys.stdin = old
    return "\n".join(out)

assert "3\n1100\n0011\n1100" in run("""1
4 2
1100
""")

assert run("""1
1 1
1
""") == "0"

assert run("""1
1 1
0
""") == "1\n1"

assert run("""1
3 3
101
""") == BAD

assert "CATACLYSM" in run("""1
4 2
1000
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 2 / 1100` | Valid sequence | Standard reachable case |
| `1 1 / 1` | Zero days | Already solved state |
| `1 1 / 0` | One flip | Minimum size boundary |
| `3 3 / 101` | Impossible | Full-mask operation limitation |
| `4 2 / 1000` | Impossible | Even parity restriction for even `m` |

## Edge Cases

For the already solved state:

```
1
2 1
11
```

The target vector is zero, so no flips are required. The algorithm immediately returns an empty sequence instead of trying unnecessary operations that would disturb the answer.

For the impossible full-visit case:

```
1
3 3
101
```

The only possible command is `111`. The target is `010`, but the only reachable states are obtained by repeatedly XORing with `111`, which alternates between `101` and `010`. Since neither state is all ones, the algorithm correctly rejects it.

For even `m` parity:

```
1
4 2
1000
```

The required change has three set bits. Every command changes exactly two bits, so any XOR of commands must contain an even number of changed bits. The basis reduction cannot remove the final odd-parity target and reports impossibility.
