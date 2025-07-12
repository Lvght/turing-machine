from dataclasses import dataclass
from datetime import datetime


@dataclass
class IsPrimeResult:
    time_spent_in_seconds: float
    is_prime: bool
    step_count: int


def is_prime_fn(value: int) -> IsPrimeResult:
    """Função simples para compararmos com a máquina de Turing."""
    time_start = datetime.now()
    step_count = 1

    if value <= 1:
        time_spent = (datetime.now() - time_start).total_seconds()
        return IsPrimeResult(
            time_spent_in_seconds=time_spent,
            is_prime=False,
            step_count=step_count,
        )

    for i in range(2, int(value**0.5) + 1):
        step_count += 1
        if value % i == 0:
            return IsPrimeResult(
                time_spent_in_seconds=(datetime.now() - time_start).total_seconds(),
                is_prime=False,
                step_count=step_count,
            )

    return IsPrimeResult(
        time_spent_in_seconds=(datetime.now() - time_start).total_seconds(),
        is_prime=True,
        step_count=step_count,
    )
