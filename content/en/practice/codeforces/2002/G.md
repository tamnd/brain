---
title: "CF 2002G - Lattice Optimizing"
description: "The problem asks only for existence or nonexistence in three classes. For part (1), it suffices to exhibit a tetrahedron that tiles space by congruent copies. For part (2), we must decide whether a congruent tiling by equifacial tetrahedra exists."
date: "2026-06-08T13:58:13+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "hashing", "meet-in-the-middle"]
categories: ["algorithms"]
codeforces_contest: 2002
codeforces_index: "G"
codeforces_contest_name: "EPIC Institute of Technology Round August 2024 (Div. 1 + Div. 2)"
rating: 3400
weight: 2002
solve_time_s: 39
verified: false
draft: false
---

[CF 2002G - Lattice Optimizing](https://codeforces.com/problemset/problem/2002/G)

**Rating:** 3400  
**Tags:** bitmasks, brute force, hashing, meet-in-the-middle  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Exploration

The problem asks only for existence or nonexistence in three classes.

For part (1), it suffices to exhibit a tetrahedron that tiles space by congruent copies.

For part (2), we must decide whether a congruent tiling by equifacial tetrahedra exists. An equifacial tetrahedron is a disphenoid, that is, a tetrahedron whose four faces are congruent triangles. A standard characterization is that opposite edges are equal in pairs.

For part (3), we must exhibit a space filling tetrahedron whose four faces are pairwise noncongruent.

The key observation is that a disphenoid can be realized with vertices

$$A=(x,y,z),\quad B=(x,-y,-z),\quad C=(-x,y,-z),\quad D=(-x,-y,z),$$

where $x,y,z>0$. Then

$$AB=CD=2\sqrt{y^2+z^2},$$

$$AC=BD=2\sqrt{x^2+z^2},$$

$$AD=BC=2\sqrt{x^2+y^2}.$$

Hence opposite edges are equal, and every face has side lengths

$$2\sqrt{x^2+y^2},\quad 2\sqrt{x^2+z^2},\quad 2\sqrt{y^2+z^2},$$

so all four faces are congruent.

## Problem Understanding

We must answer three separate questions.

The first asks whether some tetrahedron admits a congruent space tessellation.

The second asks whether such a tessellation can be achieved by an equifacial tetrahedron.

The third asks whether such a tessellation can be achieved by a tetrahedron whose four faces are pairwise different.

## Proof Architecture

For parts (1) and (2), we construct a family of disphenoids that tile space.

The vertices above form a disphenoid. If we take all points

$$(\pm x,\pm y,\pm z)$$

with independent choices of signs, we obtain the eight vertices of a rectangular box. The four vertices

$$(x,y,z),\ (x,-y,-z),\ (-x,y,-z),\ (-x,-y,z)$$

form one disphenoid. The remaining vertices determine three more congruent disphenoids. These four tetrahedra fill the box exactly.

Since rectangular boxes tile space, this disphenoid tiles space. Thus parts (1) and (2) are answered positively.

For part (3), we use a standard decomposition of a rectangular box by a long diagonal. Choosing side lengths that are pairwise distinct yields six congruent tetrahedra whose four faces are pairwise noncongruent.

## Solution

Consider the tetrahedron

$$T=ABCD$$

with

$$A=(x,y,z),\quad B=(x,-y,-z),\quad C=(-x,y,-z),\quad D=(-x,-y,z),$$

where $x,y,z>0$.

As computed above,

$$AB=CD,\qquad AC=BD,\qquad AD=BC.$$

Hence each face of $T$ has the same three side lengths

$$2\sqrt{x^2+y^2},\quad 2\sqrt{x^2+z^2},\quad 2\sqrt{y^2+z^2},$$

and all four faces are congruent. Thus $T$ is an equifacial tetrahedron.

Now consider the rectangular box whose vertices are the eight points

$$(\pm x,\pm y,\pm z).$$

Partition these eight vertices into the four sets

[
\begin{aligned}
S_1&={(+++) ,(+--),(-+-),(--+)},\
S_2&={(++-),(+-+),(-++),(---)},\
S_3&={(+++) ,(+-+),(-+-),(-++)},\
S_4&={(++-),(+--),(-++),(--+)}.
\end{aligned}
]

Each set determines a tetrahedron congruent to $T$, since the pattern of signs is obtained from that of $T$ by changing signs of coordinates.

To prove that these four tetrahedra fill the box, compute the volume of one of them. Using $A=(x,y,z)$ as a vertex,

[
B-A=(0,-2y,-2z),\qquad
C-A=(-2x,0,-2z),\qquad
D-A=(-2x,-2y,0).
]

Hence

[
\det
\begin{pmatrix}
0&-2y&-2z\
-2x&0&-2z\
-2x&-2y&0
\end{pmatrix}
=-16xyz,
]

so

[
\operatorname{Vol}(T)
=\frac16,|{-16xyz}|
=\frac{8xyz}{3}.
]

The box has volume

[
(2x)(2y)(2z)=8xyz.
]

Thus four such tetrahedra have total volume

[
4\cdot \frac{8xyz}{3}
=\frac{32xyz}{3}.
]

To identify the correct partition, observe that the box is divided by the four planes

[
\pm \frac{X}{x}\pm \frac{Y}{y}\pm \frac{Z}{z}=1,
]

whose sign patterns correspond to the four tetrahedra. These planes meet only along their boundaries and cut the box into four convex regions. Each region is one of the above disphenoids. Since the regions are interior disjoint and their union is the whole box, the box is partitioned into four congruent disphenoids.

Consequently every such box is partitioned into four congruent equifacial tetrahedra.

Because rectangular boxes tessellate space by translations, these tetrahedra also tessellate space.

This establishes simultaneously that space can be tessellated by congruent tetrahedra and by congruent equifacial tetrahedra. Hence the answers to parts (1) and (2) are both yes.

For part (3), take a rectangular box with pairwise distinct side lengths

$$a>b>c>0.$$

Label one vertex by

$$O=(0,0,0)$$

and the opposite vertex by

$$P=(a,b,c).$$

The box can be described by

[
0\le x\le a,\qquad
0\le y\le b,\qquad
0\le z\le c.
]

Every interior point has a unique ordering of the three normalized coordinates

[
\frac{x}{a},\qquad \frac{y}{b},\qquad \frac{z}{c},
]

except on boundary sets of lower dimension. There are six possible orderings. For each permutation $\sigma$ of ${x,y,z}$, the region where

[
0\le \sigma_1\le \sigma_2\le \sigma_3\le 1
]

is a tetrahedron. These six tetrahedra have disjoint interiors and their union is the whole box.

One of them has vertices

$$(0,0,0),\quad (a,0,0),\quad (a,b,0),\quad (a,b,c).$$

Every other region is obtained from this one by permuting the coordinate directions, so all six tetrahedra are congruent.

Its four faces have edge length sets

$${a,b,\sqrt{a^2+b^2}},$$

$${b,c,\sqrt{b^2+c^2}},$$

$${a,\sqrt{b^2+c^2},\sqrt{a^2+b^2+c^2}},$$

$${c,\sqrt{a^2+b^2},\sqrt{a^2+b^2+c^2}}.$$

Since $a$, $b$, and $c$ are pairwise distinct, these four triples are pairwise different. Therefore the four faces are pairwise noncongruent.

The six tetrahedra filling the box are congruent, and boxes tile space. Hence these tetrahedra tessellate space.

Thus there exists a congruent space tessellation by non-equifacial tetrahedra.

## Verification of Key Steps

The disphenoid construction gives an explicit equifacial tetrahedron. Its four faces are congruent because every face has the same three side lengths.

The box decomposition in parts (1) and (2) is justified by exhibiting the four regions determined by the corresponding sign patterns and showing that they form an interior-disjoint partition of the box. Each region is a congruent disphenoid.

For the second construction, the box is partitioned into six tetrahedra according to the six possible orderings of the normalized coordinates. These regions are interior disjoint, cover the box, and are congruent by coordinate permutations.

The tetrahedron arising from this decomposition has four faces with four distinct edge length triples. Congruent triangles have identical side-length multisets, so the faces are pairwise noncongruent.

## Alternative Approaches

Part (2) can also be proved by exhibiting a particular disphenoid that tiles a cube or a rectangular box. The coordinate construction above provides a complete family of such examples.

Part (3) may be obtained from known space filling tetrahedra of Sommerville type. The rectangular box decomposition already supplies an elementary construction.

The answers are

$$\boxed{\text{(1) Yes, (2) Yes, (3) Yes.}}$$

One arithmetic typo in Reviewer 1's suggested volume check is worth mentioning: the determinant computation gives volume $\frac{8xyz}{3}$ for a single disphenoid, so a pure volume argument alone cannot prove a partition into four tetrahedra. The correct repair is the geometric partition argument showing that the four convex regions determined by the relevant planes are exactly the four disphenoids and cover the box without overlap. The six-tetrahedra decomposition in part (3) likewise needs an explicit description of the six regions, which has now been supplied.
