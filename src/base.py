from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple, Set
from enum import Enum
import streamlit as st

from src.exceptions import MissingTransitionError

write: callable
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if not get_script_run_ctx():
        write = print
    else:
        write = st.markdown
except ModuleNotFoundError:
    write = print


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


State = str
TapeBlock = Tuple[str, str, str]
Delta = Dict[Tuple[State, TapeBlock], Tuple[State, TapeBlock, Direction]]


class TuringMachineDefinition:
    Q: Set[State]
    Sigma: Set[str]
    Gamma: Set[str]
    delta: Delta
    q0: State
    BlankSymbol: str
    F: Set[State]

    def __init__(
        self,
        Q: Set[State],
        Sigma: Set[str],
        Gamma: Set[str],
        delta: Delta,
        q0: State,
        BlankSymbol: str,
        F: Set[State],
    ):
        self.Q = Q
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.delta = delta
        self.q0 = q0
        self.BlankSymbol = BlankSymbol
        self.F = F


@dataclass
class TuringMachineExecutionResult:
    step_count: int
    final_state: State
    time_spent_in_seconds: Optional[float] = None


class TuringMachine:
    _definition: TuringMachineDefinition
    _tape: Dict[int, TapeBlock]
    _head_position: int
    _current_state: State
    _verbose: bool
    _step_count: int

    def __init__(
        self,
        definition: TuringMachineDefinition,
        w_1: str,
        w_2: Optional[str] = None,
        w_3: Optional[str] = None,
        verbose: bool = False,
    ):
        self._verbose = verbose
        self._definition = definition
        self._current_state = self._definition.q0
        self._head_position = 0
        self._step_count = 0

        max_len = len(w_1)
        if w_2:
            max_len = max(max_len, len(w_2))
        if w_3:
            max_len = max(max_len, len(w_3))

        w_1 = w_1.ljust(max_len, self._definition.BlankSymbol)
        w_2 = (w_2 or "").ljust(max_len, self._definition.BlankSymbol)
        w_3 = (w_3 or "").ljust(max_len, self._definition.BlankSymbol)

        self._tape = {i: (w_1[i], w_2[i], w_3[i]) for i in range(max_len)}

    @property
    def current_tape_block(self) -> TapeBlock:
        return self._tape.get(self._head_position, (self._definition.BlankSymbol,) * 3)

    def run(self) -> TuringMachineExecutionResult:
        """Executa a máquina de Turing até atingir um estado final."""
        start_time = datetime.now()

        while self._current_state not in self._definition.F:
            self.step()

        if self._verbose:
            write("\n**A máquina encerrou sua execução.**")
            write(f"Estado final: `{self._current_state}`")

        if not self._tape and self._verbose:
            write("A fita está vazia.")
            return

        min_idx = min(self._tape.keys())
        max_idx = max(self._tape.keys())

        tape_range = range(min_idx, max_idx + 1)

        track_1_content = "".join(self._tape.get(i, (self._definition.BlankSymbol,) * 3)[0] for i in tape_range).strip(self._definition.BlankSymbol)
        track_2_content = "".join(self._tape.get(i, (self._definition.BlankSymbol,) * 3)[1] for i in tape_range).strip(self._definition.BlankSymbol)
        track_3_content = "".join(self._tape.get(i, (self._definition.BlankSymbol,) * 3)[2] for i in tape_range).strip(self._definition.BlankSymbol)

        if self._verbose:
            write(f"**Conteúdo da fita 1**: `{track_1_content or '(vazio)'}`")
            write(f"**Conteúdo da fita 2**: `{track_2_content or '(vazio)'}`")
            write(f"**Conteúdo da fita 3**: `{track_3_content or '(vazio)'}`")
            write(f"**Posição da cabeça**: {self._head_position}")
            write(f"**Contagem de passos**: {self._step_count}")

        return TuringMachineExecutionResult(
            step_count=self._step_count,
            final_state=self._current_state,
            time_spent_in_seconds=(datetime.now() - start_time).total_seconds(),
        )

    def step(self):
        self._step_count += 1

        if self._verbose:
            current_state_parts = self._current_state.split("__")
            if len(current_state_parts) > 1:
                write(f"->          δ({current_state_parts[-1]}, {self.current_tape_block})")
                write(f"Sub-rotina: {current_state_parts[0]}")
            else:
                write(
                    f"-> δ({self._current_state}, {self.current_tape_block})",
                )
        self._print_tape_state()
        next_state, write_template, direction = self._find_transition()
        current_symbols = self.current_tape_block
        new_symbols_to_write = tuple(current_symbols[i] if write_template[i] == "*" else write_template[i] for i in range(3))

        if self._verbose:
            next_state_parts = next_state.split("__")
            if len(next_state_parts) > 1:
                write(f"- Próximo estado: `{next_state_parts[-1]}` (Parte da sub-rotina: *{next_state_parts[0]}*)")
            else:
                write(f"- Próximo estado: {next_state}")

            write(f"- Escrever:       `{new_symbols_to_write}`")
            write(f"- Direção:        {direction.name}\n\n")
            write("---")

        self._current_state = next_state
        self._tape[self._head_position] = new_symbols_to_write
        self._head_position += direction.value

    def _find_transition(self) -> Tuple[State, TapeBlock, Direction]:
        current_symbols = self.current_tape_block

        for (
            state,
            read_symbols,
        ), transition_output in self._definition.delta.items():
            if state == self._current_state:
                is_match = all(read_symbols[i] == current_symbols[i] or read_symbols[i] == "*" for i in range(3))
                if is_match:
                    return transition_output

        raise MissingTransitionError(f"∄ δ({self._current_state}, {current_symbols})")

    def _print_tape_state(self):
        """Imprime o estado visual da fita com as três trilhas e o controle."""
        if not self._verbose:
            return

        if not self._tape:
            write(
                "F1:    | B | B | B ...\nF2:    | B | B | B ...\nF3:    | B | B | B ...\nCTRL:    ^",
                self._current_state,
            )
            return

        # Determina o range da fita para visualização
        min_idx = min(min(self._tape.keys()), self._head_position - 2)
        max_idx = max(max(self._tape.keys()), self._head_position + 2)

        # Constroi as três trilhas
        track1 = []
        track2 = []
        track3 = []
        ctrl_line = []

        for i in range(min_idx, max_idx + 1):
            block = self._tape.get(i, (self._definition.BlankSymbol,) * 3)
            track1.append(f" {block[0]} ")
            track2.append(f" {block[1]} ")
            track3.append(f" {block[2]} ")

            if i == self._head_position:
                ctrl_line.append(" ^  ")
            elif i < self._head_position:
                ctrl_line.append("    ")

        write(
            f"""
```
F1:         |{"|".join(track1)}| B ...
F2:         |{"|".join(track2)}| B ...
F3:         |{"|".join(track3)}| B ...
CTRL:        {"".join(ctrl_line)} {self._current_state}
```
"""
        )
