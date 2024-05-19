from typing import TypeVar

# NOTE: Mut_M is covariant so, for instance, if a function requires an
#   X_[..., W, ...], one can pass an X_[..., W, ...] or an X_[..., WK, ...].

class R: ...
class W(R): ...
class RK(R): ...
class WK(W, RK): ...

Mut_M = TypeVar('Mut_M', 'R', 'W', 'RK', 'WK', covariant=True)
Mut_M2 = TypeVar('Mut_M2', 'R', 'W', 'RK', 'WK', covariant=True)
Mut_L = TypeVar('Mut_L')
Mut_L2 = TypeVar('Mut_L2')
