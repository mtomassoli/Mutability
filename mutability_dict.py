from __future__ import annotations
from typing import TYPE_CHECKING, assert_type, Literal as L, Any
from mutability import *


__all__ = ['dict_', 'dict_out', 'dict_r']

if TYPE_CHECKING:
    from typing import (
        overload, Iterable, Iterator, Self, ClassVar, TypeVar, final, Generic,
        KeysView, ValuesView, ItemsView
    )
    from types import MappingProxyType
    from _typeshed import SupportsKeysAndGetItem
    import sys
    if sys.version_info >= (3, 9):
        from types import GenericAlias

    _KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
    _VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.

    @final
    class dict_keys(KeysView[_KT_co], Generic[_KT_co, _VT_co]):  # undocumented
        def __eq__(self, value: object) -> bool: ...
        if sys.version_info >= (3, 10):
            @property
            def mapping(self) -> MappingProxyType[_KT_co, _VT_co]: ...

    @final
    class dict_values(ValuesView[_VT_co], Generic[_KT_co, _VT_co]):  # undocumented
        if sys.version_info >= (3, 10):
            @property
            def mapping(self) -> MappingProxyType[_KT_co, _VT_co]: ...

    @final
    class dict_items(ItemsView[_KT_co, _VT_co]):  # undocumented
        def __eq__(self, value: object) -> bool: ...
        if sys.version_info >= (3, 10):
            @property
            def mapping(self) -> MappingProxyType[_KT_co, _VT_co]: ...

    _K = TypeVar('_K')
    _V = TypeVar('_V')
    
    # NOTE: Don't depend on a lock => can be used anywhere
    type dict_out[K, V, M: (R, W, RK, WK)] = dict_[K, V, M, None]
    type dict_r[K, V] = dict_[K, V, R, Any]

    # NOTE: Self or depend on `_L` => can be used only here
    class _L: ...           # lock
    type _dict_in[K, V, M: (R, W, RK, WK)] = dict_[K, V, M, _L]
    type _Self_W[K, V] = dict_[K, V, W, _L]

    class dict_(Generic[_K, _V, Mut_M, Mut_L]):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self: dict_[str, _V, Mut_M, Mut_L], **kwargs: _V) -> None: ...     # pyright: ignore[reportInvalidTypeVarUse]
        @overload
        def __init__(self, map: SupportsKeysAndGetItem[_K, _V], /) -> None: ...
        @overload
        def __init__(self: dict_[str, _V, Mut_M, Mut_L],        # pyright: ignore[reportInvalidTypeVarUse]
                     map: SupportsKeysAndGetItem[str, _V], /, **kwargs: _V
                     ) -> None: ...
        @overload
        def __init__(self, iterable: Iterable[tuple[_K, _V]], /) -> None: ...
        @overload
        def __init__(self: dict_[str, _V, Mut_M, Mut_L],        # pyright: ignore[reportInvalidTypeVarUse]
                     iterable: Iterable[tuple[str, _V]], /, **kwargs: _V
                     ) -> None: ...
        @overload
        def __init__(self: dict_[str, str, Mut_M, Mut_L],       # pyright: ignore[reportInvalidTypeVarUse]
                     iterable: Iterable[list[str]], /) -> None: ...
        @overload
        def __init__(self: dict_[bytes, bytes, Mut_M, Mut_L],   # pyright: ignore[reportInvalidTypeVarUse]
                     iterable: Iterable[list[bytes]], /) -> None: ...
        def __init__(self, *args, **kwargs) -> None: ...
        def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
        def copy(self) -> dict_out[_K, _V, WK]: ...
        def keys(self) -> dict_keys[_K, _V]: ...
        def values(self) -> dict_values[_K, _V]: ...
        def items(self) -> dict_items[_K, _V]: ...
        @classmethod
        @overload
        def fromkeys[T](cls, iterable: Iterable[T], value: None = None, /
                        ) -> dict_out[T, Any | None, WK]: ...
        @classmethod
        @overload
        def fromkeys[S, T](cls, iterable: Iterable[T], value: S, /
                           ) -> dict_out[T, S, WK]: ...
        @classmethod
        def fromkeys(cls, *args) -> Any: ...
        @overload
        def get(self, key: _K, /) -> _V | None: ...
        @overload
        def get(self, key: _K, default: _V, /) -> _V: ...
        @overload
        def get[T](self, key: _K, default: T, /) -> _V | T: ...
        def get(self, *args) -> Any: ...
        @overload
        def pop(self: _Self_W[_K, _V], key: _K, /) -> _V: ...
        @overload
        def pop(self: _Self_W[_K, _V], key: _K, default: _V, /) -> _V: ...
        @overload
        def pop[T](self: _Self_W[_K, _V], key: _K, default: T, /) -> _V | T: ...
        def pop(self, *args) -> Any: ...
        def __len__(self) -> int: ...
        def __getitem__(self, key: _K, /) -> _V: ...
        def __setitem__(self: _Self_W[_K, _V], key: _K, value: _V, /) -> None: ...
        def __delitem__(self: _Self_W[_K, _V], key: _K, /) -> None: ...
        def __iter__(self) -> Iterator[_K]: ...
        def __eq__(self, value: object, /) -> bool: ...
        def __reversed__(self) -> Iterator[_K]: ...
        __hash__: ClassVar[None]        # type: ignore[assignment]
        if sys.version_info >= (3, 9):
            def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...
            @overload
            def __or__(self, value: dict_r[_K, _V], /) -> dict_out[_K, _V, WK]: ...
            @overload
            def __or__[T1, T2](self, value: dict_r[T1, T2], /
                               ) -> dict_out[_K | T1, _V | T2, WK]: ...
            def __or__(self, *args) -> Any: ...
            @overload
            def __ror__(self, value: dict_r[_K, _V], /) -> dict_out[_K, _V, WK]: ...
            @overload
            def __ror__[T1, T2](self, value: dict_r[T1, T2], /
                                ) -> dict_out[_K | T1, _V | T2, WK]: ...
            def __ror__(self, *args) -> Any: ...
            @overload
            def __ior__(self: _Self_W[_K, _V],
                        value: SupportsKeysAndGetItem[_K, _V], /
                        ) -> dict_[_K, _V, Mut_M, Mut_L]: ...
            @overload
            def __ior__(self: _Self_W[_K, _V], value: Iterable[tuple[_K, _V]], /
                        ) -> dict_[_K, _V, Mut_M, Mut_L]: ...
            def __ior__(self, *args) -> Any: ...
else:
    dict_ = dict_out = dict_r = dict

if __name__ == "__main__":
    a = lift({'a': 1, 'b': 2, 'c': 3})
    a_r = r(a)
    a_w = w(a)
    a_rk = rk(a)
    a_wk = wk(a)

    assert_type(r(a_r), dict_[str, int, R, Any])
    assert_type(r(a_w), dict_[str, int, R, Any])
    assert_type(r(a_rk), dict_[str, int, R, Any])
    assert_type(r(a_wk), dict_[str, int, R, Any])

    _ = w(a_r)     # pyright: ignore
    assert_type(w(a_w), dict_[str, int, W, Any])
    _ = w(a_rk)    # pyright: ignore
    assert_type(w(a_wk), dict_[str, int, W, Any])

    _ = rk(a_r)    # pyright: ignore
    _ = rk(a_w)    # pyright: ignore
    assert_type(rk(a_rk), dict_[str, int, RK, Any])
    assert_type(rk(a_wk), dict_[str, int, RK, Any])

    _ = wk(a_r)    # pyright: ignore
    _ = wk(a_w)    # pyright: ignore
    _ = wk(a_rk)   # pyright: ignore
    assert_type(wk(a_wk), dict_[str, int, WK, Any])

    a_r[''] = 0     # pyright: ignore
    a_w[''] = 0
    a_rk[''] = 0    # pyright: ignore
    a_wk[''] = 0

    assert_type((a_r[''], a_w[''], a_rk[''], a_wk['']),
                tuple[int, int, int, int])

    def f_r(a: dict_[str, int, R, Any]) -> L[0]: ...
    def f_w(a: dict_[str, int, W, None]) -> L[0]: ...
    def f_rk(a: dict_[str, int, RK, None]) -> L[0]: ...
    def f_wk(a: dict_[str, int, WK, None]) -> L[0]: ...

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
