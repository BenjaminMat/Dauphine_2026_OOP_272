class A:
    def method(self):
        print("Method in A")


class B:
    def method(self):
        print("Method in B")


class C(A):
    def method(self):
        print("Method in C")

class D(B):
    def method(self):
        print("Method in D")


class E():
    def method(self):
        print("Method in E")


class F(A, E):
    def method(self):
        print("Method in F")


class G(F, D, C):
    pass


g = G()
g.method()





"""
MRO Explanation for class G(F, D, C):

Step 1: Direct parent MROs
  MRO(F) = [F, A, E, object]     # F inherits from A, E
  MRO(D) = [D, B, object]         # D inherits from B
  MRO(C) = [C, A, object]         # C inherits from A

Step 2: C3 Linearization - merge parent MROs with [F, D, C]

  Iteration | Take | Reason
  ----------|------|-------
  1         | F    | F not in tail of any list
  2         | D    | A blocked (in tail of [C, A, object])
  3         | B    | A blocked, C/D blocked
  4         | C    | A still blocked by [C, A, object]
  5         | A    | A now safe (removed from all tails)
  6         | E    | E next available
  7         | object | object last

Step 3: Final MRO for G
  MRO(G) = [G, F, D, B, C, A, E, object]

Step 4: Method resolution
  g.method() walks MRO: G (no method) → F (HAS method) ✓

  Output: "Method in F"

Key insight: D and B come BEFORE C and A despite C being "closer" to A
(direct child). The C3 algorithm preserves left-to-right parent order [F, D, C]
over genealogical proximity.
"""

