import sys

from src.base import TuringMachine
from src.definitions import primality_test_definition
from src.other import is_prime_fn

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main.py [True,False] <valor> ")
        sys.exit(1)

    verbose = sys.argv[1].lower() == "true"
    value = int(sys.argv[2])

    machine = TuringMachine(
        definition=primality_test_definition,
        verbose=verbose,
        w_1=str(bin(value)[2:]),
    )

    result = machine.run()
    print("==| Resultado da Máquina de Turing |==")
    print(
        f"Resultado: {result.final_state}, Passos: {result.step_count}",
    )
    print(
        f"Tempo gasto: {result.time_spent_in_seconds:.6f} segundos\n",
    )

    print("Para fins de comparação, a função is_prime_fn também será executada.\n")

    print("==| Resultado da função is_prime_fn |==")
    result_fn = is_prime_fn(value)
    print(
        f"Resultado da função: {result_fn.is_prime}, Passos: {result_fn.step_count}",
    )
    print(f"Tempo gasto na função: {result_fn.time_spent_in_seconds:.6f} segundos")

    print("\n==| Comparação de Desempenho |==")
    percentage_diff = (result.time_spent_in_seconds - result_fn.time_spent_in_seconds) / result_fn.time_spent_in_seconds * 100 if result_fn.time_spent_in_seconds > 0 else float("inf")
    print(f"A máquina de Turing levou {result.time_spent_in_seconds:.6f} segundos, enquanto a função levou {result_fn.time_spent_in_seconds:.6f} segundos.")
    print(f"A máquina de Turing foi {percentage_diff:.2f}% mais {'rápida' if percentage_diff < 0 else 'lenta'} que a função.")
    print(f"A máquina de Turing executou {result.step_count} passos, enquanto a função executou {result_fn.step_count} passos.")
    print("==| Fim da execução |==")
