from __future__ import annotations
from typing import (
    Generic, overload, Any, cast, assert_type, Callable, Literal as L
)

from mutability import *

type A_out[M: (R, W, RK, WK)] = A_[M, None]
type A_r = A_[R, Any]

# Multi-lock version (see "mutability_example.py" for the single-lock version)
class A_(Generic[Mut_M, Mut_L]):
    _val: int

    def __init__(self, val: int) -> None:
        self._val = val
    
    @property
    def val(self) -> int:
        return self._val
    
    class _L1: ...
    @val.setter
    def val(self: A_[W, _L1], val: int) -> None:
        self._val = val
        
    def get_val(self) -> int:
        return self._val
    
    class _L2: ...
    def set_val(self: A_[W, _L2], val: int) -> None:
        self._val = val
        
    class _L3: ...
    @overload
    def set_val_overload(self: A_[W, _L3], x: int) -> int: ...
    @overload
    def set_val_overload(self: A_[W, _L3], x: str) -> str: ...
    def set_val_overload(self, x) -> Any:
        if isinstance(x, float):
            self._val = round(x)
        else:
            self._val = x

    def copy(self) -> A_out[WK]:
        return A_(self._val)
    
    def return_self(self) -> A_[Mut_M, Mut_L]:
        return self
    
    class _L4: ...
    def __iadd__(self: A_[W, _L4], a2: A_r) -> A_[Mut_M, Mut_L]:
        self._val += a2._val
        return cast(A_[Mut_M, Mut_L], self)

    class _L5: ...
    def __imul__(self: A_[W, _L5], n: int) -> A_[Mut_M, Mut_L]:
        self._val *= n
        return cast(A_[Mut_M, Mut_L], self)

    # NOTE: these are just for debugging
    def for_r(self): return 0
    class _L6: ...
    def for_w(self: A_[W, _L6]): return 0
    class _L7: ...
    def for_rk(self: A_[RK, _L7]): return 0
    class _L8: ...
    def for_wk(self: A_[WK, _L8]): return 0

if __name__ == "__main__":
    a = A_[WK, None](8)
    a_r = r(a)
    a_w = w(a)
    a_rk = rk(a)
    a_wk = wk(a)

    assert_type(r(a_r), A_[R, Any])
    assert_type(r(a_w), A_[R, Any])
    assert_type(r(a_rk), A_[R, Any])
    assert_type(r(a_wk), A_[R, Any])

    _ = w(a_r)     # pyright: ignore
    assert_type(w(a_w), A_[W, Any])
    _ = w(a_rk)    # pyright: ignore
    assert_type(w(a_wk), A_[W, Any])

    _ = rk(a_r)    # pyright: ignore
    _ = rk(a_w)    # pyright: ignore
    assert_type(rk(a_rk), A_[RK, Any])
    assert_type(rk(a_wk), A_[RK, Any])

    _ = wk(a_r)    # pyright: ignore
    _ = wk(a_w)    # pyright: ignore
    _ = wk(a_rk)   # pyright: ignore
    assert_type(wk(a_wk), A_[WK, Any])

    assert_type(a_r.for_r, Callable[[], L[0]])
    assert_type(a_w.for_r, Callable[[], L[0]])
    assert_type(a_rk.for_r, Callable[[], L[0]])
    assert_type(a_wk.for_r, Callable[[], L[0]])

    _ = a_r.for_w   # pyright: ignore
    assert_type(a_w.for_w, Callable[[], L[0]])
    _ = a_rk.for_w  # pyright: ignore
    assert_type(a_wk.for_w, Callable[[], L[0]])

    _ = a_r.for_rk  # pyright: ignore
    _ = a_w.for_rk  # pyright: ignore
    assert_type(a_rk.for_rk, Callable[[], L[0]])
    assert_type(a_wk.for_rk, Callable[[], L[0]])

    _ = a_r.for_wk  # pyright: ignore
    _ = a_w.for_wk  # pyright: ignore
    _ = a_rk.for_wk # pyright: ignore
    assert_type(a_wk.for_wk, Callable[[], L[0]])

    _ = a_r.set_val_overload(5)         # pyright: ignore
    assert_type(a_w.set_val_overload(5), int)
    _ = a_rk.set_val_overload(5)        # pyright: ignore
    assert_type(a_wk.set_val_overload(5), int)
    _ = a_r.set_val_overload('asd')     # pyright: ignore
    assert_type(a_w.set_val_overload('asd'), str)
    _ = a_rk.set_val_overload('asd')    # pyright: ignore
    assert_type(a_wk.set_val_overload('asd'), str)

    a_r1 = r(a_r.copy())
    a_r1 += a_r      # pyright: ignore

    a_r2 = r(a_r.copy())

    a_w2 = w(a)
    a_w2 += a_r
    a_w2 += a_w
    a_w2 += a_rk
    a_w2 += a_wk
    assert_type(a_w2, A_[W, Any])

    a_r *= 3        # pyright: ignore
    a_w3 = w(a_wk)
    a_w3 *= 3
    a_w_l1 = w(a_w)
    a_w_l1 *= 3
