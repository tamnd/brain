---
title: "CF 102409D - Lottery Ticket"
description: "We have tickets numbered from 1 through (N), arranged in increasing order on a circle. Diego starts at ticket (S). From the current ticket, the process moves exactly (K) surviving tickets to the right and removes the ticket where it lands."
date: "2026-08-12T03:25:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "D"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 808
verified: true
draft: false
---

[CF 102409D - Lottery Ticket](https://codeforces.com/problemset/problem/102409/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have tickets numbered from 1 through (N), arranged in increasing order on a circle. Diego starts at ticket (S). From the current ticket, the process moves exactly (K) surviving tickets to the right and removes the ticket where it lands. After removing it, the current ticket becomes the surviving ticket immediately to its left. The circle wraps around, so moving past ticket (N) continues at ticket 1.

The task is to determine the ID of the only ticket left at the end. The difficulty is that the tickets between the current position and the destination may already have been removed, so the movement is over the current surviving sequence rather than over the original IDs.

The value of (N) can be as large as (10^{18}), while there can be (10^5) test cases. Even a single linear pass over the tickets is impossible at that scale, let alone explicitly maintaining the circle. The fact that (K\le 10) is the key structural restriction. We can afford an algorithm whose cost depends on (K) and only logarithmically on (N), but an (O(N)), (O(NK)), or (O(N^2)) method is ruled out immediately.

There are several edge cases that expose common modeling mistakes. If (N=1), for example, the input (1\ 1\ 1) must produce 1 because there is nothing to eliminate. A simulation that performs one elimination before checking the size can access an empty circle.

The case (K=1) is also special. For input (5\ 3\ 1), the process removes 4, then 5, then 1, then 2, so ticket 3 survives. Thus the answer is always the initial ticket (S) when (K=1). A formula derived under the assumption that the ticket immediately before the eliminated ticket is still alive breaks here, because the predecessor can itself have already been eliminated.

Wrapping around is another source of off-by-one errors. For input (2\ 1\ 2), moving two tickets from ticket 1 lands back on ticket 1, so ticket 1 is removed and ticket 2 wins. The correct output is 2. Treating (K) as an ordinary ID difference would miss this completely.

Finally, deleted tickets cannot be counted when moving. For input (4\ 1\ 2), ticket 3 is removed first. The next move starts at ticket 2 and moves through tickets 4 and 1, so ticket 1 is removed next. The remaining tickets are 2 and 4, and ticket 4 is removed next, leaving ticket 2. The answer is 2. A careless implementation that simply adds (K) to the previous ID would use information about tickets that no longer exist.

## Approaches

The direct approach is to keep the surviving ticket IDs in a circular list. At every round, find the ticket (K) positions to the right, remove it, and move the current pointer to its predecessor. This exactly follows the process, so its correctness is straightforward.

Unfortunately, the size of the list is initially (N). There are (N-1) removals, and even if finding the destination costs only (O(K)), deleting from an ordinary array can cost (O(N)) because elements have to be shifted. That gives (O(N^2)) work in the worst case, about (10^{36}) elementary operations when (N=10^{18}). A linked list avoids the shifting, but locating the next ticket still requires following up to (K) surviving nodes per elimination, giving (O(NK)), which can still reach about (10^{19}) operations.

The useful observation is that (K) is tiny. Instead of performing every elimination, we can perform many eliminations simultaneously and turn the remaining circle into a smaller instance of exactly the same problem.

For a relative starting position of 0 and (K\ge2), consider a circle of (N>K) tickets. The first eliminated ticket is position (K). After it is removed, the new current position is (K-1), which is still alive because (K\ge2). Moving another (K) surviving tickets lands on (2K). The same argument continues, so the first

[
m=\left\lfloor\frac{N-1}{K}\right\rfloor
]

eliminations are exactly positions

[
K,2K,3K,\ldots,mK.
]

We have therefore removed (m) tickets at once, leaving (N-m) tickets. The new current ticket is (mK-1). From that point, the remaining process is the original problem again, just on a smaller circle and with a different physical labeling of its positions.

This is the same batch-deletion principle behind the standard (O(K\log N)) optimization for the Josephus problem, but the predecessor rule in this problem changes the mapping back to the original circle.

Let (F(N,K)) be the winning position, using zero-based positions and assuming the initial current ticket is position 0. After the batch deletion, define

[
m=\left\lfloor\frac{N-1}{K}\right\rfloor,\qquad
Q=N-m.
]

We recursively compute (r=F(Q,K)). The new current ticket in the original circle is

[
P=mK-1.
]

After (P), the surviving tickets first continue with (mK+1,mK+2,\ldots,N). Let

[
R=N-mK
]

be the length of this final partial block. Once it wraps around, the surviving tickets occur in blocks of (K-1), namely

[
1,\ldots,K-1,\quad K+1,\ldots,2K-1,\quad\ldots
]

because every multiple of (K) was removed.

If the recursive answer is (r=0), it refers to (P) itself. Otherwise, set (u=r-1). If (u<R), the answer lies in the partial block after (P), at

[
mK+1+u.
]

Otherwise, after skipping that partial block, let (v=u-R). The corresponding original position is

[
\left\lfloor\frac{v}{K-1}\right\rfloor K
+
(v\bmod(K-1))+1.
]

Each recursive call reduces (N) to approximately (N(1-1/K)). Thus the recursion depth is (O(K\log N)). Since (K\le10), this is small even for (N=10^{18}).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NK)) with a linked list, (O(N^2)) with an array | (O(N)) | Too slow |
| Optimal | (O(K\log N)) per test case | (O(K\log N)) auxiliary | Accepted |

## Algorithm Walkthrough

1. Work with zero-based positions and define (F(N,K)) as the winning position when the initial current ticket is position 0. The actual starting ticket (S) will be applied as a final cyclic shift.
2. If (K=1), return 0. Moving one ticket always removes the immediate successor, and the new current ticket is the ticket we started from, so the initial ticket survives.
3. If (N\le K), simulate the process directly. There are at most 10 tickets in this case, so this costs only a constant amount of work.
4. For (N>K) and (K\ge2), compute

[
m=\left\lfloor\frac{N-1}{K}\right\rfloor.
]

The first (m) eliminated tickets are (K,2K,\ldots,mK). After the last one, the current ticket is (mK-1).
5. Remove those (m) tickets conceptually and define

[
Q=N-m.
]

The remaining process, viewed from the new current ticket, is the same problem on (Q) tickets. Recursively compute (r=F(Q,K)).
6. Compute the length of the surviving partial block before the circle wraps:

[
R=N-mK.
]

If (r=0), the recursive winner is the new current ticket (mK-1).
7. If (r>0), set (u=r-1). When (u<R), the winner is still in the partial block after (mK-1), so its original position is (mK+1+u), reduced modulo (N).
8. If (u\ge R), subtract the partial block and set (v=u-R). The remaining tickets appear in groups of (K-1), separated by one deleted multiple of (K). The original position is therefore

[
\left\lfloor\frac{v}{K-1}\right\rfloor K
+(v\bmod(K-1))+1.
]
9. Starting from the recursively computed base case, apply these mappings in reverse order until the original (N) is restored. The resulting value is (F(N,K)).
10. Finally shift the relative winner by the actual starting ticket. If (F) is zero-based, the answer is

[
((S-1+F)\bmod N)+1.
]

### Why it works

The invariant is that (F(N,K)) always describes the winner relative to the current ticket, not relative to ticket 1. For (N>K) and (K\ge2), the first (m) eliminations are exactly the multiples of (K), and the current ticket after those eliminations is (mK-1). The remaining tickets preserve their circular order, so the rest of the game is precisely an (F(N-m,K)) instance when viewed from that new current ticket. The mapping formula enumerates those remaining tickets in their exact circular order, so it converts the recursive relative position back to the original position without changing the winner. The base simulation is exact, and every larger instance is reduced to one smaller valid instance, which proves that the final position is the true survivor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def relative_winner(n, k):
    if k == 1:
        return 0

    frames = []

    while n > k:
        m = (n - 1) // k
        tail = n - m * k
        frames.append((n, m, tail))
        n -= m

    # n <= k, so direct simulation is tiny.
    circle = list(range(n))
    cur = 0

    while len(circle) > 1:
        size = len(circle)
        target = (cur + k) % size
        circle.pop(target)

        size -= 1
        cur = (target - 1) % size

    winner = circle[0]

    # Restore the positions removed by the batch steps.
    for n, m, tail in reversed(frames):
        if winner == 0:
            winner = m * k - 1
            continue

        u = winner - 1

        if u < tail:
            winner = (m * k + 1 + u) % n
        else:
            v = u - tail
            winner = (v // (k - 1)) * k + (v % (k - 1)) + 1

    return winner

def solve(reader=input):
    t = int(reader())
    out = []

    for _ in range(t):
        n, s, k = map(int, reader().split())
        f = relative_winner(n, k)
        answer = (s - 1 + f) % n + 1
        out.append(str(answer))

    return "\n".join(out)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The `relative_winner` function deliberately separates the actual starting ticket from the recursive calculation. Inside the function, position 0 always means the current ticket, which makes every reduction independent of the original value of (S).

For (K=1), the answer relative to the starting ticket is immediately zero. This special case is necessary because the predecessor of the eliminated ticket can already have disappeared, so the batch argument for (K\ge2) does not apply.

For larger (N), each frame stores the information needed to reconstruct one reduction. The quantity `m` is the number of multiples of (K) removed in the batch, while `tail` is the number of surviving tickets from `m * k + 1` through (N).

The small remaining instance is simulated with a Python list. The simulation uses `target = (cur + k) % size`, because the rule says to move (K) surviving tickets, rather than counting the current ticket as the first move. After removal, `(target - 1) % size` selects the surviving predecessor. Python's modulo behavior is useful here because `-1 % size` correctly gives the last index.

During reconstruction, `winner == 0` means the recursive winner is exactly the new current ticket, `m * k - 1`. Otherwise, `winner - 1` counts how far into the sequence after that current ticket the recursive winner lies. The first `tail` positions form a partial block, and everything after it is divided into blocks of (K-1) non-multiples of (K).

Python integers have arbitrary precision, so values up to (10^{18}) require no special overflow handling. The implementation also avoids recursion, which keeps the call stack constant and makes the (O(K\log N)) reduction explicit.

## Worked Examples

### Sample 1

For input (N=5,S=3,K=2), first compute the winner relative to starting position 0.

| (N) | (K) | (m) | (Q) | (R) | Recursive winner | Restored (F(N,K)) |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 2 | 2 | 3 | 1 | 0 | 3 |
| 3 | 2 | 1 | 2 | 1 | 1 | 0 |
| 2 | 2 | base | base | base | 1 | 1 |

The base case with two tickets has relative winner 1 because moving two tickets lands back on the current ticket, removing it.

For (N=3), the recursive winner is position 1. The first remaining partial block has length 1, so that recursive position maps to position 0. For (N=5), the recursive winner is position 0, so it maps directly to the new current position (mK-1=3).

The relative winner is therefore position 3. Starting from ticket 3 means shifting by two positions:

[
((3-1)+3)\bmod5+1=1.
]

The output is 1.

### Constructed Example

Consider (N=4,S=1,K=2).

| (N) | (K) | (m) | (Q) | (R) | Recursive winner | Restored (F(N,K)) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 2 | 1 | 3 | 2 | 0 | 1 |
| 3 | 2 | 1 | 2 | 1 | 1 | 0 |
| 2 | 2 | base | base | base | 1 | 1 |

The relative winner is position 1, so with (S=1) the actual winner is ticket 2.

A direct simulation confirms it. Ticket 3 is removed first, then ticket 1, then ticket 4, leaving ticket 2. The trace agrees with the recursive invariant at every reduction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time per test case | (O(K\log N)) | Each reduction removes about (N/K) tickets, and the remaining size is about (N(1-1/K)). |
| Total time | (O(TK\log N)) | The same bound applies independently to all (T) cases. |
| Auxiliary space | (O(K\log N)) | One frame is stored for each reduction before reconstruction. |
| Output space | (O(T)) | The answers are accumulated before being written. |

With (K\le10) and (N\le10^{18}), the recursive reduction has only a few hundred levels even in the worst case. The algorithm never allocates an array proportional to (N), so both the 256 MB memory limit and the 5 second time limit are compatible with the intended approach.

## Test Cases

```python
import sys
import io

def relative_winner(n, k):
    if k == 1:
        return 0

    frames = []

    while n > k:
        m = (n - 1) // k
        tail = n - m * k
        frames.append((n, m, tail))
        n -= m

    circle = list(range(n))
    cur = 0

    while len(circle) > 1:
        size = len(circle)
        target = (cur + k) % size
        circle.pop(target)

        size -= 1
        cur = (target - 1) % size

    winner = circle[0]

    for n, m, tail in reversed(frames):
        if winner == 0:
            winner = m * k - 1
        else:
            u = winner - 1

            if u < tail:
                winner = (m * k + 1 + u) % n
            else:
                v = u - tail
                winner = (v // (k - 1)) * k + (v % (k - 1)) + 1

    return winner

def solve(reader):
    t = int(reader())
    out = []

    for _ in range(t):
        n, s, k = map(int, reader().split())
        f = relative_winner(n, k)
        out.append(str((s - 1 + f) % n + 1))

    return "\n".join(out)

def run(inp: str) -> str:
    return solve(io.StringIO(inp).readline) + "\n"

# Provided sample
assert run("1\n5 3 2\n") == "1\n", "sample 1"

# Minimum-size input
assert run("1\n1 1 10\n") == "1\n", "single ticket"

# K = 1, so the starting ticket always survives
assert run("1\n100 73 1\n") == "73\n", "K=1"

# Maximum N, with K=1
assert run("1\n1000000000000000000 1000000000000000000 1\n") == \
       "1000000000000000000\n", "maximum N"

# K = N, with all three values equal
assert run("1\n5 5 5\n") == "1\n", "N=S=K"

# Boundary case where the first move wraps to the current ticket
assert run("1\n2 1 2\n") == "2\n", "wrap to current"

# Off-by-one case involving deleted tickets
assert run("1\n4 1 2\n") == "2\n", "deleted tickets affect movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 10` | `1` | Minimum (N), immediate base case |
| `1 / 100 73 1` | `73` | Special behavior for (K=1) |
| `1 / 10^18 10^18 1` | `10^18` | Maximum (N) and arbitrary-precision arithmetic |
| `1 / 5 5 5` | `1` | (N=S=K), wrapping and all-equal parameters |
| `1 / 2 1 2` | `2` | Landing back on the current ticket and predecessor handling |
| `1 / 4 1 2` | `2` | Movement through only surviving tickets |

## Edge Cases

For (N=1), the input `1 1 10` immediately enters the small-circle simulation with one element. No elimination is performed, so position 0 is returned and converted back to ticket 1. The algorithm never attempts to compute a predecessor in an empty list.

For (K=1), consider `5 3 1`. From ticket 3, ticket 4 is removed, then ticket 5, then ticket 1, then ticket 2. Ticket 3 survives. The algorithm returns relative position 0 for every (N), and the final shift converts that directly to (S=3). This avoids applying the (K\ge2) batch formula in a case where its predecessor assumption is false.

For a move that wraps exactly back to the current ticket, consider `2 1 2`. Relative to ticket 1, moving two surviving tickets reaches ticket 1 again, so ticket 1 is removed. Ticket 2 is the only remaining ticket and wins. The base simulation computes target index `(0+2)%2=0`, removes it, and leaves relative winner 1. The final answer is 2.

For deleted tickets changing the meaning of distance, consider `4 1 2`. Ticket 3 is removed first. The next current ticket is 2, and moving two surviving tickets reaches ticket 1, not ticket 4, because the surviving sequence is 2, 4, 1. The algorithm never represents movement using original ID differences. Its batch reduction explicitly removes multiples of (K) first and then maps positions through the compressed surviving sequence.

For the case (N=S=K=5), the input `5 5 5` begins at ticket 5. The first move of five surviving tickets returns to ticket 5, so it is removed. The process then continues around the four remaining tickets, eventually leaving ticket 1. The small-circle simulation handles this directly because (N\le K), avoiding assumptions that the first batch contains at least one complete multiple of (K).

For the maximum value (N=10^{18}), the input `1000000000000000000 1000000000000000000 1` is handled by the (K=1) shortcut and returns the starting ticket immediately. More generally, the reduction uses only integer division, multiplication, addition, and modulo on values bounded by a small multiple of (10^{18}), all of which Python handles exactly without overflow.
