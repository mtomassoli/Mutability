from typing import TYPE_CHECKING
from mutability_tvars import R, W, RK, WK, Mut_M, Mut_L

__all__ = [
    'R', 'W', 'RK', 'WK', 'Mut_M', 'Mut_L', 'r', 'w', 'rk', 'wk', 'lift',
    'lift_and_w', 'lift_and_rk', 'lift_and_wk', 'restrict'
]

if TYPE_CHECKING:
    from typing import Any, Callable, overload, TypeVar
    # NOTE: importing "mutability_reg.py" here instead of at the top avoids a
    #   (runtime) circular dependence.
    from mutability_reg import do_conv, Liftable
    
    FROM = TypeVar('FROM')
    TO = TypeVar('TO')

    # NOTE:
    # * Pyright detects that `do_conv` is NOT assignable to `__st` for all
    #   combinations of `m1` (M before the conversion) and `m2` (M after the
    #   conversion). That's on purpose, since we only want to support lecit
    #   conversions (e.g. from `W` to `R`, but not vice versa).
    #   For this reason, it's perfectly safe to suppress the error with a type
    #   ignore.
    # * Note that `m1` is in covariant position in `do_conv` for technical
    #   reasons. See "mutability_reg.py" for details.

    def r(obj: FROM, *,
          __st: Callable[[FROM, R, Any], tuple[Any, TO]] = do_conv
          ) -> TO: ...

    def w(obj: FROM, *,
          __st: Callable[[FROM, W, Any], tuple[W | WK, TO]] = do_conv,          # pyright: ignore[reportArgumentType]
          ) -> TO: ...

    def rk(obj: FROM, *,
           __st: Callable[[FROM, RK, Any], tuple[RK | WK, TO]] = do_conv,       # pyright: ignore[reportArgumentType]
           ) -> TO: ...

    def wk(obj: FROM, *,
           __st: Callable[[FROM, WK, Any], tuple[WK, TO]] = do_conv,            # pyright: ignore[reportArgumentType]
           ) -> TO: ...

    # NOTE: the overload for `R` must be the last since it's the widest one
    @overload
    def lift[M: (W, RK, WK), FROM, TO](
        obj: FROM, m: type[M] = WK, *,
        __st: Callable[[Liftable[FROM], M, None], tuple[Any, TO]] = do_conv,
        ) -> TO: ...
    @overload
    def lift[FROM, TO](
        obj: FROM, m: type[R], *,
        __st: Callable[[Liftable[FROM], R, Any], tuple[Any, TO]] = do_conv,
        ) -> TO: ...
    def lift(*args, **kwargs) -> Any: ...
    
    # NOTE: Since `R` does NOT need explicit permission, `lift_then_r` is
    #   equivalent to `lift(..., R)`.

    def lift_and_w(
        obj: FROM, *,
        __st: Callable[[Liftable[FROM], W, Any], tuple[Any, TO]] = do_conv,
        ) -> TO:
        """1-call version of `w(lift(.))"""
        ...             # pylint: disable=W2301

    def lift_and_rk(
        obj: FROM, *,
        __st: Callable[[Liftable[FROM], RK, Any], tuple[Any, TO]] = do_conv,
        ) -> TO:
        """1-call version of `rk(lift(.))"""
        ...             # pylint: disable=W2301

    def lift_and_wk(
        obj: FROM, *,
        __st: Callable[[Liftable[FROM], WK, Any], tuple[Any, TO]] = do_conv,
        ) -> TO:
        """1-call version of `wk(lift(.))"""
        ...             # pylint: disable=W2301
    
    # NOTE: the overloads must be listed from narrowest (WK) to widest (R)
    @overload
    def restrict[FROM, TO](
        obj: FROM, m: type[WK], *,
        __st: Callable[[FROM, WK, None], tuple[WK, TO]] = do_conv,              # pyright: ignore[reportArgumentType]
        ) -> TO: ...
    @overload
    def restrict[FROM, TO](
        obj: FROM, m: type[RK], *,
        __st: Callable[[FROM, RK, None], tuple[RK | WK, TO]] = do_conv,         # pyright: ignore[reportArgumentType]
        ) -> TO: ...
    @overload
    def restrict[FROM, TO](
        obj: FROM, m: type[W], *,
         __st: Callable[[FROM, W, None], tuple[W | WK, TO]] = do_conv,          # pyright: ignore[reportArgumentType]
        ) -> TO: ...
    @overload
    def restrict[FROM, TO](
        obj: FROM, m: type[R], *,
        __st: Callable[[FROM, R, Any], tuple[Any, TO]] = do_conv,
        ) -> TO: ...
    def restrict(*args, **kwargs) -> Any: ...
else:
    def _ident1(x):
        return x
    def _ident2(x, y=None):
        return x
    r = rk = w = wk = lift_and_w = lift_and_rk = lift_and_wk = _ident1
    lift = restrict = _ident2
