---
title: "TAOCP 7.1.3: Bitwise Tricks and Techniques"
description: "Section 7.1.3 exercises: 46/219 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.1.3"
section_title: "Bitwise Tricks and Techniques"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7010300
draft: false
---

# Section 7.1.3. Bitwise Tricks and Techniques

Exercises from [TAOCP Volume 4](../) Section 7.1.3: 46/219 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) | &#9654; [*15*] | simple | solved | 2m02s |
| [2](02.md) |  [*16*] | medium | solved | 2m23s |
| [3](03.md) |  [*M20*] | math-medium | solved | 5m55s |
| [4](04.md) | &#9654; [*M16*] | math-medium | verified | 39s |
| [5](05.md) |  [*M21*] | math-medium | verified | 2m44s |
| [6](06.md) |  [*M22*] | math-medium | solved | 3m11s |
| [7](07.md) |  [*M22*] | math-medium | solved | 4m59s |
| [8](08.md) | &#9654; [*M22*] | math-medium | verified | 41s |
| [9](09.md) |  [*M26*] | math-hard | verified | 43s |
| [10](10.md) |  [*HM40*] | hm-project | solved | 3m21s |
| [11](11.md) | &#9654; [*M26*] | math-hard | solved | 50s |
| [12](12.md) |  [*M26*] | math-hard | solved | 1m51s |
| [13](13.md) |  [*M32*] | math-hard | solved | 43s |
| 14 |  [*M30*] | math-hard | - | - |
| 15 | &#9654; [*M30*] | math-hard | - | - |
| 16 |  [*M31*] | math-hard | - | - |
| 17 |  [*HM36*] | hm-project | - | - |
| 18 |  [*M25*] | math-medium | - | - |
| 19 | &#9654; [*M37*] | math-project | - | - |
| 20 | &#9654; [*21*] | medium | - | - |
| 21 |  [*22*] | medium | - | - |
| 22 |  [*21*] | medium | - | - |
| 23 | &#9654; [*27*] | hard | - | - |
| 24 | &#9654; [*M30*] | math-hard | - | - |
| 25 | &#9654; [*15*] | simple | - | - |
| 26 |  [*22*] | medium | - | - |
| 27 |  [*21*] | medium | - | - |
| 28 |  [*16*] | medium | - | - |
| 29 |  [*20*] | medium | - | - |
| 30 |  [*20*] | medium | - | - |
| 31 | &#9654; [*20*] | medium | - | - |
| 32 |  [*20*] | medium | - | - |
| 33 | &#9654; [*26*] | hard | - | - |
| 34 |  [*M23*] | math-medium | - | - |
| 35 | &#9654; [*M26*] | math-hard | - | - |
| 36 |  [*20*] | medium | - | - |
| 37 |  [*16*] | medium | - | - |
| 38 |  [*17*] | medium | - | - |
| 39 | &#9654; [*20*] | medium | - | - |
| 40 | &#9654; [*21*] | medium | - | - |
| 41 |  [*M22*] | math-medium | - | - |
| 42 |  [*M21*] | math-medium | - | - |
| 43 | &#9654; [*20*] | medium | - | - |
| 44 | &#9654; [*23*] | medium | - | - |
| 45 | &#9654; [*20*] | medium | - | - |
| 46 |  [*22*] | medium | - | - |
| 47 |  [*10*] | simple | - | - |
| 48 |  [*M21*] | math-medium | - | - |
| 49 | &#9654; [*M30*] | math-hard | - | - |
| 50 |  [*M37*] | math-project | - | - |
| 51 |  [*23*] | medium | - | - |
| 52 |  [*22*] | medium | - | - |
| 53 | &#9654; [*M25*] | math-medium | - | - |
| 54 |  [*22*] | medium | - | - |
| 55 | &#9654; [*26*] | hard | - | - |
| 56 |  [*24*] | medium | - | - |
| 57 |  [*22*] | medium | - | - |
| 58 | &#9654; [*M32*] | math-hard | - | - |
| 59 |  [*M30*] | math-hard | - | - |
| 60 |  [*HM28*] | hm-hard | - | - |
| 61 |  [*46*] | research | - | - |
| 62 | &#9654; [*22*] | medium | - | - |
| 63 |  [*19*] | medium | - | - |
| 64 |  [*22*] | medium | - | - |
| 65 |  [*M16*] | math-medium | - | - |
| 66 | &#9654; [*M26*] | math-hard | - | - |
| 67 |  [*M31*] | math-hard | - | - |
| 68 |  [*20*] | medium | - | - |
| 69 |  [*25*] | medium | - | - |
| 70 | &#9654; [*31*] | hard | - | - |
| 71 |  [*20*] | medium | - | - |
| 72 |  [*25*] | medium | - | - |
| 73 |  [*22*] | medium | - | - |
| 74 |  [*22*] | medium | - | - |
| 75 | &#9654; [*32*] | hard | - | - |
| 76 |  [*27*] | hard | - | - |
| 77 |  [*26*] | hard | - | - |
| 78 |  [*M27*] | math-hard | - | - |
| 79 | &#9654; [*20*] | medium | - | - |
| 80 |  [*20*] | medium | - | - |
| 81 |  [*21*] | medium | - | - |
| 82 |  [*21*] | medium | - | - |
| 83 | &#9654; [*33*] | hard | - | - |
| 84 |  [*25*] | medium | - | - |
| [85](85.md) |  [*22*] | medium | verified | 4m14s |
| 86 |  [*M27*] | math-hard | - | - |
| 87 | &#9654; [*20*] | medium | - | - |
| 88 |  [*20*] | medium | - | - |
| 89 |  [*23*] | medium | - | - |
| 90 |  [*20*] | medium | - | - |
| 91 | &#9654; [*26*] | hard | - | - |
| 92 | &#9654; [*21*] | medium | - | - |
| 93 |  [*18*] | medium | - | - |
| 94 |  [*21*] | medium | - | - |
| 95 |  [*22*] | medium | - | - |
| 96 |  [*21*] | medium | - | - |
| 97 |  [*23*] | medium | - | - |
| 98 |  [*20*] | medium | - | - |
| 99 | &#9654; [*28*] | hard | - | - |
| [100](100.md) |  [*25*] | medium | solved | 4m22s |
| [101](101.md) | &#9654; [*22*] | medium | verified | 57s |
| [102](102.md) |  [*25*] | medium | solved | 2m38s |
| [103](103.md) | &#9654; [*22*] | medium | verified | 2m45s |
| [104](104.md) |  [*22*] | medium | solved | 3m10s |
| [105](105.md) |  [*30*] | hard | solved | 5m09s |
| [106](106.md) |  [**] |  | solved | 3m43s |
| [107](107.md) | &#9654; [*22*] | medium | solved | 4m17s |
| [108](108.md) |  [*26*] | hard | solved | 2m38s |
| [109](109.md) |  [*20*] | medium | solved | 2m33s |
| [110](110.md) | &#9654; [*30*] | hard | solved | 3m50s |
| [111](111.md) |  [*23*] | medium | verified | 1m25s |
| [112](112.md) |  [*46*] | research | solved | 4m35s |
| [113](113.md) |  [*23*] | medium | verified | 3m07s |
| [114](114.md) |  [*16*] | medium | solved | 4m34s |
| [115](115.md) | &#9654; [*24*] | medium | verified | 5m |
| [116](116.md) |  [*HM30*] | hm-hard | solved | 4m39s |
| [117](117.md) |  [*HM46*] | hm-research | verified | 3m08s |
| [118](118.md) |  [*30*] | hard | solved | 3m44s |
| [119](119.md) |  [*20*] | medium | solved | 6m03s |
| [120](120.md) | &#9654; [*M25*] | math-medium | solved | 4m34s |
| [121](121.md) | &#9654; [*M25*] | math-medium | verified | 4m53s |
| [122](122.md) |  [*M22*] | math-medium | solved | 3m10s |
| [123](123.md) |  [*M23*] | math-medium | solved | 4m10s |
| [124](124.md) |  [*M38*] | math-project | solved | 4m28s |
| [125](125.md) |  [*M33*] | math-hard | verified | 1m25s |
| [126](126.md) |  [*M46*] | math-research | solved | 4m53s |
| [127](127.md) |  [*HM40*] | hm-project | solved | 3m25s |
| [128](128.md) |  [*M46*] | math-research | solved | 4m36s |
| [129](129.md) |  [*M46*] | math-research | solved | 2m11s |
| [130](130.md) |  [*M46*] | math-research | solved | 2m12s |
| [131](131.md) | &#9654; [*23*] | medium | verified | 3m12s |
| 132 | &#9654; [*M27*] | math-hard | - | - |
| 133 | &#9654; [*20*] | medium | - | - |
| 134 |  [*15*] | simple | - | - |
| 135 |  [*22*] | medium | - | - |
| 136 |  [*29*] | hard | - | - |
| 137 |  [*21*] | medium | - | - |
| 138 |  [*24*] | medium | - | - |
| 139 |  [*25*] | medium | - | - |
| 140 |  [*27*] | hard | - | - |
| 141 | &#9654; [*30*] | hard | - | - |
| 142 | &#9654; [*33*] | hard | - | - |
| 143 |  [*20*] | medium | - | - |
| 144 |  [*16*] | medium | - | - |
| 145 |  [*17*] | medium | - | - |
| 146 | &#9654; [*M20*] | math-medium | - | - |
| 147 | &#9654; [*M20*] | math-medium | - | - |
| 148 |  [*M21*] | math-medium | - | - |
| 149 | &#9654; [*23*] | medium | - | - |
| 150 | &#9654; [*25*] | medium | - | - |
| 151 |  [*22*] | medium | - | - |
| 152 |  [*M21*] | math-medium | - | - |
| 153 | &#9654; [*M20*] | math-medium | - | - |
| 154 |  [*20*] | medium | - | - |
| 155 | &#9654; [*M21*] | math-medium | - | - |
| 156 |  [*21*] | medium | - | - |
| 157 |  [*M21*] | math-medium | - | - |
| 158 |  [*M26*] | math-hard | - | - |
| 159 |  [*M34*] | math-hard | - | - |
| 160 |  [*M29*] | math-hard | - | - |
| 161 |  [*20*] | medium | - | - |
| 162 | &#9654; [*HM37*] | hm-project | - | - |
| 163 |  [*HM41*] | hm-project | - | - |
| 164 |  [*23*] | medium | - | - |
| 165 |  [*21*] | medium | - | - |
| 166 |  [*M23*] | math-medium | - | - |
| 167 |  [*24*] | medium | - | - |
| 168 | &#9654; [*23*] | medium | - | - |
| 169 |  [*22*] | medium | - | - |
| 170 | &#9654; [*21*] | medium | - | - |
| 171 |  [*24*] | medium | - | - |
| 172 |  [*M29*] | math-hard | - | - |
| 173 | &#9654; [*M30*] | math-hard | - | - |
| 174 |  [*M46*] | math-research | - | - |
| 175 |  [*15*] | simple | - | - |
| 176 |  [*M24*] | math-medium | - | - |
| 177 |  [*M22*] | math-medium | - | - |
| 178 |  [*20*] | medium | - | - |
| 179 | &#9654; [*34*] | hard | - | - |
| 180 | &#9654; [*M24*] | math-medium | - | - |
| 181 |  [*HM20*] | hm-medium | - | - |
| 182 |  [*M31*] | math-hard | - | - |
| 183 | &#9654; [*M29*] | math-hard | - | - |
| 184 | &#9654; [*M22*] | math-medium | - | - |
| 185 | &#9654; [*23*] | medium | - | - |
| 186 |  [*HM22*] | hm-medium | - | - |
| 187 |  [*M29*] | math-hard | - | - |
| 188 | &#9654; [*25*] | medium | - | - |
| 189 |  [*25*] | medium | - | - |
| 190 |  [*23*] | medium | - | - |
| 191 |  [*M30*] | math-hard | - | - |
| 192 |  [*HM38*] | hm-project | - | - |
| 193 | &#9654; [*M21*] | math-medium | - | - |
| 194 |  [*M24*] | math-medium | - | - |
| 195 | &#9654; [*HM25*] | hm-medium | - | - |
| 196 |  [*21*] | medium | - | - |
| 197 |  [*22*] | medium | - | - |
| 198 | &#9654; [*21*] | medium | - | - |
| 199 | &#9654; [*23*] | medium | - | - |
| 200 |  [*20*] | medium | - | - |
| 201 |  [*20*] | medium | - | - |
| 202 |  [*20*] | medium | - | - |
| 203 |  [*22*] | medium | - | - |
| 204 | &#9654; [*22*] | medium | - | - |
| 205 | &#9654; [*22*] | medium | - | - |
| 206 |  [*20*] | medium | - | - |
| 207 |  [*22*] | medium | - | - |
| 208 | &#9654; [*23*] | medium | - | - |
| 209 | &#9654; [*21*] | medium | - | - |
| 210 |  [*22*] | medium | - | - |
| 211 | &#9654; [*M25*] | math-medium | - | - |
| 212 |  [*M32*] | math-hard | - | - |
| 213 | &#9654; [*HM26*] | hm-hard | - | - |
| 214 | &#9654; [*HM28*] | hm-hard | - | - |
| 215 | &#9654; [*21*] | medium | - | - |
| 216 | &#9654; [*M26*] | math-hard | - | - |
| 217 |  [*40*] | project | - | - |
| 218 | &#9654; [*M30*] | math-hard | - | - |
| 219 | &#9654; [*20*] | medium | - | - |
