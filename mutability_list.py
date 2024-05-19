from __future__ import annotations
from typing import TYPE_CHECKING, assert_type, Literal as L, Any
from mutability import *

__all__ = ['list_', 'list_out', 'list_r']

if TYPE_CHECKING:
    from typing import (
        overload, Iterable, SupportsIndex, Iterator, Callable, ClassVar,
        Generic, TypeVar
    )
    from _typeshed import SupportsRichComparison, SupportsRichComparisonT
    import sys
    if sys.version_info >= (3, 9):
        from types import GenericAlias

    _T = TypeVar('_T')
    
    # NOTE: These don't depend on a lock => they can be used anywhere
    type list_out[T, M: (R, W, RK, WK)] = list_[T, M, None]
    type list_r[T] = list_[T, R, Any]

    # NOTE: These are Self or depend on `_L` => they can be used only here
    class _L: ...           # lock
    type _list_in[T, M: (R, W, RK, WK)] = list_[T, M, _L]
    type _Self_W[T] = list_[T, W, _L]
    
    class list_(Generic[_T, Mut_M, Mut_L]):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, iterable: Iterable[_T], /) -> None: ...
        def __init__(self, *args) -> None:
            super().__init__()          # to avoid a warning
        def copy(self) -> list_out[_T, WK]: ...
        def append(self: _Self_W[_T], object: _T, /) -> None: ...
        def extend(self: _Self_W[_T], iterable: Iterable[_T], /) -> None: ...
        def pop(self: _Self_W[_T], index: SupportsIndex = -1, /) -> _T: ...
        def index(self, value: _T, start: SupportsIndex = 0,
                  stop: SupportsIndex = sys.maxsize, /) -> int: ...
        def count(self, value: _T, /) -> int: ...
        def insert(self: _Self_W[_T], index: SupportsIndex, object: _T, /
                   ) -> None: ...
        def remove(self: _Self_W[_T], value: _T, /) -> None: ...
        @overload
        def sort(self: _Self_W[SupportsRichComparisonT], *, key: None = None,
                 reverse: bool = False) -> None: ...
        @overload
        def sort(self: _Self_W[_T], *,
                 key: Callable[[_T], SupportsRichComparison],
                 reverse: bool = False) -> None: ...
        def sort(self, *, key = None, reverse = False) -> None: ...
        def __len__(self) -> int: ...
        def __iter__(self) -> Iterator[_T]: ...
        __hash__: ClassVar[None]    # pyright: ignore[reportIncompatibleMethodOverride]
        @overload
        def __getitem__(self, i: SupportsIndex, /) -> _T: ...
        @overload
        def __getitem__(self, s: slice, /) -> list_out[_T, WK]: ...
        def __getitem__(self, s, /) -> Any: ...
        @overload
        def __setitem__(self: _Self_W[_T], key: SupportsIndex, value: _T, /
                        ) -> None: ...
        @overload
        def __setitem__(self: _Self_W[_T], key: slice, value: Iterable[_T], /
                        ) -> None: ...
        def __setitem__(self, key, value) -> None: ...
        def __delitem__(self: _Self_W[_T], key: SupportsIndex | slice, /
                        ) -> None: ...
        @overload
        def __add__(self, value: _list_in[_T, R], /) -> list_out[_T, WK]: ...
        @overload
        def __add__[S](self, value: _list_in[S, R], /) -> list_out[_T | S, WK]: ...
        def __add__(self, value, /) -> Any: ...
        def __iadd__(self: _Self_W[_T], value: Iterable[_T], /
                     ) -> list_out[_T, Mut_M]: ...
        def __mul__(self, value: SupportsIndex, /) -> list_out[_T, Mut_M]: ...
        def __rmul__(self, value: SupportsIndex, /) -> list_out[_T, Mut_M]: ...
        def __imul__(self: _Self_W[_T], value: SupportsIndex, /
                     ) -> list_out[_T, Mut_M]: ...
        def __contains__(self, key: object, /) -> bool: ...
        def __reversed__(self) -> Iterator[_T]: ...
        def __gt__(self, value: list_r[_T], /) -> bool: ...
        def __ge__(self, value: list_r[_T], /) -> bool: ...
        def __lt__(self, value: list_r[_T], /) -> bool: ...
        def __le__(self, value: list_r[_T], /) -> bool: ...
        def __eq__(self, value: object, /) -> bool: ...
        if sys.version_info >= (3, 9):
            def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...
else:
    list_ = list_out = list_r = list

if __name__ == "__main__":
    a = lift([1, 2, 3])
    a_r = r(a)
    a_w = w(a)
    a_rk = rk(a)
    a_wk = wk(a)

    assert_type(r(a_r), list_[int, R, Any])
    assert_type(r(a_w), list_[int, R, Any])
    assert_type(r(a_rk), list_[int, R, Any])
    assert_type(r(a_wk), list_[int, R, Any])

    _ = w(a_r)     # pyright: ignore
    assert_type(w(a_w), list_[int, W, Any])
    _ = w(a_rk)    # pyright: ignore
    assert_type(w(a_wk), list_[int, W, Any])

    _ = rk(a_r)    # pyright: ignore
    _ = rk(a_w)    # pyright: ignore
    assert_type(rk(a_rk), list_[int, RK, Any])
    assert_type(rk(a_wk), list_[int, RK, Any])

    _ = wk(a_r)    # pyright: ignore
    _ = wk(a_w)    # pyright: ignore
    _ = wk(a_rk)   # pyright: ignore
    assert_type(wk(a_wk), list_[int, WK, Any])

    a_r[0] = 0      # pyright: ignore
    a_w[0] = 0
    a_rk[0] = 0     # pyright: ignore
    a_wk[0] = 0

    assert_type((a_r[0], a_w[0], a_rk[0], a_wk[0]), tuple[int, int, int, int])

    def f_r(a: list_[int, R, Any]) -> L[0]: ...
    def f_w(a: list_[int, W, None]) -> L[0]: ...
    def f_rk(a: list_[int, RK, None]) -> L[0]: ...
    def f_wk(a: list_[int, WK, None]) -> L[0]: ...

    assert_type((f_r(a_r), f_r(a_w), f_r(a_rk), f_r(a_wk)),
                tuple[L[0], L[0], L[0], L[0]])

    _ = f_w(a_r)    # pyright: ignore
    assert_type(f_w(a_w), L[0])
    _ = f_w(a_rk)   # pyright: ignore
    assert_type(f_w(a_wk), L[0])

    _ = f_rk(a_r)   # pyright: ignore
    _ = f_rk(a_w)   # pyright: ignore
    assert_type(f_rk(a_rk), L[0])
    assert_type(f_rk(a_wk), L[0])

    _ = f_wk(a_r)   # pyright: ignore
    _ = f_wk(a_w)   # pyright: ignore
    _ = f_wk(a_rk)  # pyright: ignore
    assert_type(f_wk(a_wk), L[0])
