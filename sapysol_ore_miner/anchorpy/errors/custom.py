import typing
from anchorpy.error import ProgramError


class EpochActive(ProgramError):
    def __init__(self) -> None:
        super().__init__(0, "The epoch is still active and cannot be reset")

    code = 0
    name = "EpochActive"
    msg = "The epoch is still active and cannot be reset"


class EpochExpired(ProgramError):
    def __init__(self) -> None:
        super().__init__(1, "The epoch has expired and needs reset")

    code = 1
    name = "EpochExpired"
    msg = "The epoch has expired and needs reset"


class InvalidHash(ProgramError):
    def __init__(self) -> None:
        super().__init__(2, "The provided hash was invalid")

    code = 2
    name = "InvalidHash"
    msg = "The provided hash was invalid"


class InsufficientHashDifficulty(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            3, "The provided hash does not satisfy the difficulty requirement"
        )

    code = 3
    name = "InsufficientHashDifficulty"
    msg = "The provided hash does not satisfy the difficulty requirement"


class InsufficientBusRewards(ProgramError):
    def __init__(self) -> None:
        super().__init__(4, "The bus has insufficient rewards to mine at this time")

    code = 4
    name = "InsufficientBusRewards"
    msg = "The bus has insufficient rewards to mine at this time"


class InvalidClaimAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            5, "The claim amount cannot be larger than the claimable rewards"
        )

    code = 5
    name = "InvalidClaimAmount"
    msg = "The claim amount cannot be larger than the claimable rewards"


CustomError = typing.Union[
    EpochActive,
    EpochExpired,
    InvalidHash,
    InsufficientHashDifficulty,
    InsufficientBusRewards,
    InvalidClaimAmount,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    0: EpochActive(),
    1: EpochExpired(),
    2: InvalidHash(),
    3: InsufficientHashDifficulty(),
    4: InsufficientBusRewards(),
    5: InvalidClaimAmount(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
