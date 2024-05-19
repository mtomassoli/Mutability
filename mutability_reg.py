from typing import overload, Any, TypeVar

from mutability_tvars import Mut_M, Mut_L, Mut_M2, Mut_L2
from mutability_example import A_
from mutability_example2 import A_ as A2_
from mutability_list import list_
from mutability_set import set_
from mutability_dict import dict_

# NOTE:
# * W and RK are subtypes of R; WK is a subtype of W and RK.
# * `Mut_M` is covariant.
# * `Mut_M` is in covariant position (i.e. `return` position) in `do_conv`.
# * If `Mut_M` were in contravariant position (i.e. argument position), then,
#   for instance,
#     `do_conv: (..., m1: R, ...) -> ...`
#   would be assignable to
#     `do_conv: (..., m1: M, ...) -> ...`
#   for any `M` in {`R`, `W`, `RK`, `WK`}`.
# * See also "mutability.py".

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')

class Liftable[T]: ...

@overload
def do_conv(obj: Liftable[dict[_T1, _T2]] | dict_[_T1, _T2, Mut_M, Mut_L],
            m2: Mut_M2, d2: Mut_L2
            ) -> tuple[Mut_M, dict_[_T1, _T2, Mut_M2, Mut_L2]]: ...
@overload
def do_conv(obj: Liftable[set[_T1]] | set_[_T1, Mut_M, Mut_L],
            m2: Mut_M2, d2: Mut_L2
            ) -> tuple[Mut_M, set_[_T1, Mut_M2, Mut_L2]]: ...
@overload
def do_conv(obj: Liftable[list[_T1]] | list_[_T1, Mut_M, Mut_L],
            m2: Mut_M2, d2: Mut_L2
            ) -> tuple[Mut_M, list_[_T1, Mut_M2, Mut_L2]]: ...
@overload
def do_conv(obj: A2_[Mut_M, Mut_L], m2: Mut_M2, d2: Mut_L2
            ) -> tuple[Mut_M, A2_[Mut_M2, Mut_L2]]: ...
@overload
def do_conv(obj: A_[Mut_M, Mut_L], m2: Mut_M2, d2: Mut_L2
            ) -> tuple[Mut_M, A_[Mut_M2, Mut_L2]]: ...
def do_conv(*args, **kwargs) -> Any: ...
