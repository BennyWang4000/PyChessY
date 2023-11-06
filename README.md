# ChessYinPython

The whole idea is not mine. \
If there have any exception or optimization, please feel free to open an issue. :)

## Usage

```python
from PyChessY import ChessY
chessy= ChessY()

moves = chessy.getMovesFromGameGPN(pgn3)
positions = chessy.getPositionsFromGamePGN(moves)

edges = chessy.getEdgesFromPosition(positions[-1])
nodes = chessy.getNodesFromPosition(positions[-1])

do = chessy.getDomainance(nodes, edges)
o = chessy.getOffensiveness(nodes, edges)
d = chessy.getDefensiveness(nodes, positions[-1])
```


## Copyright

> ### ElsevierSoftwareX / SOFTX_2018_142
>
> <https://github.com/ElsevierSoftwareX/SOFTX_2018_142>

```Mathematica
(* ============================================================================== *)
(* ============================================================================== *)
(* ============================================================================== *)
(*                                                                                *)
(* CHESSY                                                                         *)
(* v1.0                                                                           *)
(*                                                                                *)
(* Chess Graph Generation, Visualization and Analysis Toolbox                     *)
(* for Mathematica v10.0+                                                         *)
(*                                                                                *)
(* ============================================================================== *)
(* ============================================================================== *)
(* ============================================================================== *)
(*                                                                                *)
(* AUTHOR  :: Dr. M. Rudolph-Lilith                                               *)
(*                                                                                *)
(* ADDRESS :: Unité de Neurosciences, Information & Complexité (UNIC)             *)
(*            CNRS UPR-3293                                                       *)
(*            Bat. 33, Avenue de la Terrasse 1                                    *)
(*            91198 Gif-sur-Yvette, FRANCE                                        *)
(*                                                                                *)
(* EMAIL   :: which.lilith@gmail.com                                              *)
(*            rudolphlilith@protonmail.com                                        *)
(*                                                                                *)
(* URL     :: http://mrudolphlilith.github.io/contact.html                        *)
(*                                                                                *)
(* ============================================================================== *)
(* ============================================================================== *)
(* ============================================================================== *)
(*                                                                                *)
(* Copyright 2018 M. Rudolph-Lilith                                               *)
(*                                                                                *)
(* Redistribution and use in source and binary forms, with or without             *)
(* modification, are permitted provided that the following conditions are met:    *)
(*                                                                                *)
(* 1. Redistributions of source code must retain the above copyright notice,      *)
(*    this list of conditions and the following disclaimer.                       *)
(*                                                                                *)
(* 2. Redistributions in binary form must reproduce the above copyright notice,   *)
(*    this list of conditions and the following disclaimer in the documentation   *)
(*    and/or other materials provided with the distribution.                      *)
(*                                                                                *)
(* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"    *)
(* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE      *)
(* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE     *)
(* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE      *)
(* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR            *)
(* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF           *)
(* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS       *)
(* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN        *)
(* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)        *)
(* ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE     *)
(* POSSIBILITY OF SUCH DAMAGE.                                                    *)
(*                                                                                *)
(* ============================================================================== *)
(* ============================================================================== *)
(* ============================================================================== *)
```

## TODOs

- [ ] rename all members to small camel
- [ ] finish all analyze method
- [ ] replace using function by parameter to self members


## murmur

The whole of origin code is from above public repository in Mathematica and I have no experience about Mathematica. \
All I want is turn it to Python and make it conform to OOP for practicing and further working. \
i.e. the origin data structure in Mathematica is dictinaries or something like that instead of object.\
