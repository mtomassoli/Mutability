from typing import assert_type, Any, overload

from mutability_list import *
from mutability_set import *
from mutability_dict import *
from mutability import *

# NOTE: This is just to better separate wrong code from good one.
wrong = False

def get_sum(xs: list_r[int]) -> int:
    if wrong:
        xs[0] = 7       # type: ignore      xs is read-only
        xs.sort()       # type: ignore      xs is read-only
    return sum(xs)

@overload
def doubled(xs: list_r[int]) -> list_out[int, WK]: ...
@overload
def doubled[K](xs: dict_r[K, int]) -> dict_out[K, int, WK]: ...
def doubled[K](xs: list_r[int] | dict_r[K, int]) -> Any:
    if isinstance(xs, dict_):       # dict_ = dict at runtime
        xs2 = lift({k: v * 2 for k, v in xs.items()})       # WK by default
        assert_type(xs2, dict_[K, int, WK, None])
    else:
        xs2 = lift([x * 2 for x in xs])                     # WK by default
        assert_type(xs2, list_[int, WK, None])
    return xs2

class _L1: ...          # lock
@overload
def double(xs: list_[int, W, _L1]) -> None: ...
@overload
def double(xs: dict_[Any, int, W, _L1]) -> None: ...
def double(xs: list_[int, W, _L1] | dict_[Any, int, W, _L1]) -> None:
    if isinstance(xs, dict_):   # dict_ = dict at runtime
        xs_w = w(xs)            # explicit permission
        for k in xs.keys():
            if wrong:
                xs[k] *= 2      # type: ignore      needs explicit permission
            xs_w[k] *= 2
    else:
        xs_w = w(xs)            # explicit permission
        for i in range(len(xs)):    # pylint: disable=C0200
            if wrong:
                xs[i] *= 2      # type: ignore      needs explicit permission
            xs_w[i] *= 2

class _L2: ...          # lock
def update_keys(src: dict_r[str, int], dest: dict_[str, int, W, _L2],
                keys: set_r[str]) -> None:
    for k in keys:
        if wrong:
            dest[k] = src[k]    # type: ignore      needs explicit permission
            del dest[k]         # type: ignore      needs explicit permission
            del src[k]          # type: ignore      read-only
        w(dest)[k] = src[k]

    # more efficient
    dest_w = w(dest)
    for k in keys:
        dest_w[k] = src[k]
        
class _L3: ...          # lock
def needs_rk_access(xs: list_[Any, RK, _L3]) -> None: ...
        
def do_stuff() -> None:
    xs = lift([6, 3, 8])                    # WK by default
    dxs = lift({str(x): x for x in xs})     # WK by default
    
    print(get_sum(xs))
    
    if wrong:
        double(dxs)         # type: ignore      needs explicit permission
    double(w(dxs))
    double(w(dxs))
    
    needs_rk_access(rk(xs))
    
    xs2 = doubled(r(xs))        # redundant r(.)
    dxs2 = doubled(r(dxs))      # redundant r(.)
    double(wk(xs2))             # xs2 is WK
    double(wk(dxs2))            # dxs2 is WK
    double(w(xs2))              # W is enough
    double(w(dxs2))             # W is enough
    
    # NOTE:
    # * `xs = w(xs)` restricts to `W` AND gives explicit permission.
    # * `xs = restrict(xs, W)` only restricts.
    # * EXCEPTION: `r(xs)` and `restrict(xs, R)` are equivalent because read-
    #       only access does NOT require explicit permission.
    xs = restrict(xs, W)
    if wrong:
        double(xs)          # type: ignore      needs explicit perm
        needs_rk_access(xs) # type: ignore      not enough privileges
        _ = rk(xs)          # type: ignore      can't go from W to RK
    double(w(xs))
    
    xs = w(xs)
    double(xs)
    xs = restrict(xs, W)    # NOTE: it clears the explicit permission
    if wrong:
        double(xs)          # type: ignore      needs explicit perm
    double(w(xs))
    
class MyList[T]:
    class _L4: ...          # lock
    
    xs_shared: list_[T, RK, _L4]
    ys_owned: list_[T, WK, _L4]
    
    def __init__(self, xs: list_[T, RK, _L4], ys: list_[T, WK, _L4]) -> None:
        # NOTE:
        # * `RK` and `WK` are mostly documentation:
        #   * `K` stands for "keep", which means that `__init__` will keep
        #     (using) the value indefinitely.
        #   * Without the `K`, a function MUST only access the value until the
        #     function has returned.
        #   * `RK` gives read-only access, while `WK` read-write access.
        # * This avoids redundant copies of the data.
        self.xs_shared = xs
        self.ys_owned = ys

def do_stuff2():
    # 2-call version
    _ = MyList(rk(lift([1, 2, 3])), wk(lift([4, 5, 6])))
    
    # 1-call version: slightly faster
    _ = MyList(lift_and_rk([1, 2, 3]), lift_and_wk([4, 5, 6]))
    
    xs = lift([1, 2, 3], W)
    ys = lift([4, 5, 6])
    if wrong:
        _ = MyList(xs,          # type: ignore      needs explicit permission
                   wk(ys))
        _ = MyList(rk(xs),      # type: ignore      can't go from W to RK
                   wk(ys))
        _ = lift(xs)            # type: ignore      already lifted
        _ = lift(xs, RK)        # type: ignore      already lifted

if __name__ == "__main__":
    do_stuff()
    do_stuff2()
