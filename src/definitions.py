"""Este arquivo contém as definições das sub-rotinas e das máquinas principais usadas no projeto."""

from src.base import Direction, TuringMachineDefinition


binary_addition = TuringMachineDefinition(
    Q={"q0", "q1", "q2", "q3", "q4"},
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q0",
    F={"q4"},
    delta={
        # Fase 1: Mover até a extremidade direita sem alterar a fita.
        # Esta fase é idêntica à da máquina de subtração.
        ("q0", ("0", "*", "*")): ("q0", ("*", "*", "*"), Direction.RIGHT),
        ("q0", ("1", "*", "*")): ("q0", ("*", "*", "*"), Direction.RIGHT),
        # Encontrou a extremidade direita, agora move para a esquerda e começa a somar.
        ("q0", ("B", "B", "B")): ("q1", ("B", "B", "B"), Direction.LEFT),
        # Fase 2: Soma (q1 -> Sem "vai-um")
        ("q1", ("0", "0", "B")): ("q1", ("0", "0", "0"), Direction.LEFT),
        ("q1", ("1", "0", "B")): ("q1", ("1", "0", "1"), Direction.LEFT),
        ("q1", ("0", "1", "B")): ("q1", ("0", "1", "1"), Direction.LEFT),
        ("q1", ("1", "1", "B")): ("q2", ("1", "1", "0"), Direction.LEFT),
        ("q1", ("1", "B", "B")): ("q1", ("1", "B", "1"), Direction.LEFT),
        ("q1", ("0", "B", "B")): ("q1", ("0", "B", "0"), Direction.LEFT),
        # Fase 3: Soma (q2 -> Com "vai-um")
        ("q2", ("0", "0", "B")): ("q1", ("0", "0", "1"), Direction.LEFT),
        ("q2", ("1", "0", "B")): ("q2", ("1", "0", "0"), Direction.LEFT),
        ("q2", ("0", "1", "B")): ("q2", ("0", "1", "0"), Direction.LEFT),
        ("q2", ("1", "1", "B")): ("q2", ("1", "1", "1"), Direction.LEFT),
        ("q2", ("1", "B", "B")): ("q2", ("1", "B", "0"), Direction.LEFT),
        ("q2", ("0", "B", "B")): ("q1", ("0", "B", "1"), Direction.LEFT),
        # Fase 4: Finalização
        # Se a soma terminar sem "vai-um" pendente.
        ("q1", ("B", "B", "B")): ("q3", ("B", "B", "B"), Direction.RIGHT),
        # Se a soma terminar e ainda houver um "vai-um" (ex: 11+01=100), escreve o último bit.
        ("q2", ("B", "B", "B")): ("q1", ("B", "B", "1"), Direction.LEFT),
        ("q3", ("*", "*", "*")): ("q4", ("*", "*", "*"), Direction.RIGHT),
    },
)

# Similar ao Binary addition, mas apenas incrementa em 1 a fita 2.
increment_tape2 = TuringMachineDefinition(
    Q={"q_inc2_seek_end", "q_inc2_add_carry", "q_inc2_rewind", "q_inc2_end"},
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_inc2_seek_end",
    F={"q_inc2_end"},
    delta={
        # Fase 1: Mover para a extremidade direita da entrada.
        ("q_inc2_seek_end", ("0", "*", "*")): ("q_inc2_seek_end", ("*", "*", "*"), Direction.RIGHT),
        ("q_inc2_seek_end", ("1", "*", "*")): ("q_inc2_seek_end", ("*", "*", "*"), Direction.RIGHT),
        ("q_inc2_seek_end", ("B", "B", "B")): ("q_inc2_add_carry", ("B", "B", "B"), Direction.LEFT),
        # Fase 2: Adicionar 1 e propagar o "vai-um" (carry) para a esquerda.
        # Se encontrar um 0, vira 1 e termina o incremento.
        ("q_inc2_add_carry", ("*", "0", "*")): ("q_inc2_rewind", ("*", "1", "*"), Direction.LEFT),
        # Se encontrar um 1, vira 0 e continua o "vai-um".
        ("q_inc2_add_carry", ("*", "1", "*")): ("q_inc2_add_carry", ("*", "0", "*"), Direction.LEFT),
        # Se chegar ao início da fita (lê Branco), escreve o último "vai-um".
        ("q_inc2_add_carry", ("*", "B", "*")): ("q_inc2_rewind", ("*", "1", "*"), Direction.LEFT),
        # Fase 3: Rebobinar para o início da fita.
        ("q_inc2_rewind", ("0", "*", "*")): ("q_inc2_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_inc2_rewind", ("1", "*", "*")): ("q_inc2_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_inc2_rewind", ("B", "B", "B")): ("q_inc2_end", ("B", "B", "B"), Direction.RIGHT),
    },
)

binary_subtraction = TuringMachineDefinition(
    Q={"q0", "q1", "q2", "q3"},
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q0",
    F={"q3"},
    delta={
        # Fase 1: Mover até a extremidade direita sem alterar a fita.
        ("q0", ("0", "0", "B")): ("q0", ("0", "0", "B"), Direction.RIGHT),
        ("q0", ("0", "1", "B")): ("q0", ("0", "1", "B"), Direction.RIGHT),
        ("q0", ("1", "0", "B")): ("q0", ("1", "0", "B"), Direction.RIGHT),
        ("q0", ("1", "1", "B")): ("q0", ("1", "1", "B"), Direction.RIGHT),
        ("q0", ("1", "B", "B")): ("q0", ("1", "B", "B"), Direction.RIGHT),
        ("q0", ("0", "B", "B")): ("q0", ("0", "B", "B"), Direction.RIGHT),
        # Encontrou a extremidade direita, agora move para a esquerda e começa a subtrair.
        ("q0", ("B", "B", "B")): ("q1", ("B", "B", "B"), Direction.LEFT),
        # Fase 2: Subtração (q1 -> Sem Empréstimo)
        ("q1", ("0", "0", "B")): ("q1", ("0", "0", "0"), Direction.LEFT),
        ("q1", ("1", "0", "B")): ("q1", ("1", "0", "1"), Direction.LEFT),
        ("q1", ("1", "1", "B")): ("q1", ("1", "1", "0"), Direction.LEFT),
        ("q1", ("0", "1", "B")): ("q2", ("0", "1", "1"), Direction.LEFT),
        ("q1", ("1", "B", "B")): ("q1", ("1", "B", "1"), Direction.LEFT),
        ("q1", ("0", "B", "B")): ("q1", ("0", "B", "0"), Direction.LEFT),
        # Fase 3: Empréstimo (q2 -> Com Empréstimo)
        ("q2", ("0", "0", "B")): ("q2", ("0", "0", "1"), Direction.LEFT),
        ("q2", ("0", "1", "B")): ("q2", ("0", "1", "0"), Direction.LEFT),
        ("q2", ("1", "1", "B")): ("q2", ("1", "1", "1"), Direction.LEFT),
        ("q2", ("1", "0", "B")): ("q1", ("1", "0", "0"), Direction.LEFT),
        ("q2", ("1", "B", "B")): ("q1", ("1", "B", "0"), Direction.LEFT),
        ("q2", ("0", "B", "B")): ("q2", ("0", "B", "1"), Direction.LEFT),
        # Fase 4: Finalização
        ("q1", ("B", "B", "B")): ("q3", ("B", "B", "B"), Direction.RIGHT),
        ("q2", ("B", "B", "B")): ("q3", ("B", "B", "B"), Direction.RIGHT),
    },
)

copy_2 = TuringMachineDefinition(
    Q={
        "q_copy2_0",
        "q_copy2_write0",
        "q_copy2_write1",
        "q_copy2_rewind",
        "q_copy2_end",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_copy2_0",
    F={"q_copy2_end"},
    delta={
        # Mover até encontrar a extremidade direita da fita.
        # Escrevemos 0's no caminho.
        ("q_copy2_0", ("0", "*", "*")): ("q_copy2_0", ("*", "0", "*"), Direction.RIGHT),
        ("q_copy2_0", ("1", "*", "*")): ("q_copy2_0", ("*", "0", "*"), Direction.RIGHT),
        ("q_copy2_0", ("B", "B", "B")): ("q_copy2_write0", ("B", "B", "B"), Direction.LEFT),
        # Escrever 0 na fita 2.
        ("q_copy2_write0", ("*", "*", "*")): ("q_copy2_write1", ("*", "0", "*"), Direction.LEFT),
        # Mover para a esquerda até encontrar o primeiro símbolo da fita 1.
        ("q_copy2_write1", ("*", "*", "*")): ("q_copy2_rewind", ("*", "1", "*"), Direction.LEFT),
        ("q_copy2_rewind", ("0", "*", "*")): ("q_copy2_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_copy2_rewind", ("1", "*", "*")): ("q_copy2_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_copy2_rewind", ("B", "B", "B")): ("q_copy2_end", ("*", "*", "*"), Direction.RIGHT),
    },
)

copy_tape1_on_tape3 = TuringMachineDefinition(
    Q={
        "q_copytape1ontape3_0",
        "q_copytape1ontape3_write0",
        "q_copytape1ontape3_write1",
        "q_copytape1ontape3_rewind",
        "q_copytape1ontape3_end",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_copytape1ontape3_0",
    F={"q_copytape1ontape3_end"},
    delta={
        ("q_copytape1ontape3_0", ("0", "*", "*")): ("q_copytape1ontape3_0", ("*", "*", "0"), Direction.RIGHT),
        ("q_copytape1ontape3_0", ("1", "*", "*")): ("q_copytape1ontape3_0", ("*", "*", "1"), Direction.RIGHT),
        ("q_copytape1ontape3_0", ("B", "B", "B")): ("q_copytape1ontape3_rewind", ("B", "B", "B"), Direction.LEFT),
        ("q_copytape1ontape3_rewind", ("0", "*", "*")): ("q_copytape1ontape3_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_copytape1ontape3_rewind", ("1", "*", "*")): ("q_copytape1ontape3_rewind", ("*", "*", "*"), Direction.LEFT),
        ("q_copytape1ontape3_rewind", ("B", "B", "B")): ("q_copytape1ontape3_end", ("*", "*", "*"), Direction.RIGHT),
    },
)

compare_tape1_and_tape2 = TuringMachineDefinition(
    Q={
        "q_comparetape1andtape2_compare",
        "q_comparetape1andtape2_rewind_true",
        "q_comparetape1andtape2_rewind_false",
        "q_comparetape1andtape2_true",
        "q_comparetape1andtape2_false",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_comparetape1andtape2_compare",
    F={"q_comparetape1andtape2_true", "q_comparetape1andtape2_false"},
    delta={
        ("q_comparetape1andtape2_compare", ("0", "0", "*")): ("q_comparetape1andtape2_compare", ("0", "0", "*"), Direction.RIGHT),
        ("q_comparetape1andtape2_compare", ("1", "1", "*")): ("q_comparetape1andtape2_compare", ("1", "1", "*"), Direction.RIGHT),
        ("q_comparetape1andtape2_compare", ("1", "0", "*")): ("q_comparetape1andtape2_rewind_false", ("1", "1", "*"), Direction.LEFT),
        ("q_comparetape1andtape2_compare", ("0", "1", "*")): ("q_comparetape1andtape2_rewind_false", ("1", "1", "*"), Direction.LEFT),
        # Não encontrou diferença após percorrer as fitas.
        ("q_comparetape1andtape2_compare", ("B", "B", "B")): ("q_comparetape1andtape2_rewind_true", ("B", "B", "B"), Direction.LEFT),
        # Lógica de rebobinação.
        ("q_comparetape1andtape2_rewind_true", ("0", "*", "*")): ("q_comparetape1andtape2_rewind_true", ("0", "*", "*"), Direction.LEFT),
        ("q_comparetape1andtape2_rewind_true", ("1", "*", "*")): ("q_comparetape1andtape2_rewind_true", ("1", "*", "*"), Direction.LEFT),
        ("q_comparetape1andtape2_rewind_false", ("0", "*", "*")): ("q_comparetape1andtape2_rewind_false", ("0", "*", "*"), Direction.LEFT),
        ("q_comparetape1andtape2_rewind_false", ("1", "*", "*")): ("q_comparetape1andtape2_rewind_false", ("1", "*", "*"), Direction.LEFT),
        ("q_comparetape1andtape2_rewind_true", ("B", "B", "B")): ("q_comparetape1andtape2_true", ("*", "*", "*"), Direction.RIGHT),
        ("q_comparetape1andtape2_rewind_false", ("B", "B", "B")): ("q_comparetape1andtape2_false", ("*", "*", "*"), Direction.RIGHT),
    },
)

# CORRIGIDO: Compara se o valor na Fita 3 é maior ou igual ao valor na Fita 2.
compare_tape3_greater_equal_tape2 = TuringMachineDefinition(
    Q={
        "q_cge_start",
        "q_cge_compare",
        "q_cge_rewind_true",
        "q_cge_rewind_false",
        "q_cge_true",
        "q_cge_false",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_cge_compare",
    F={"q_cge_true", "q_cge_false"},
    delta={
        ("q_cge_compare", ("*", "0", "0")): ("q_cge_compare", ("*", "*", "*"), Direction.RIGHT),
        ("q_cge_compare", ("*", "1", "1")): ("q_cge_compare", ("*", "*", "*"), Direction.RIGHT),
        ("q_cge_compare", ("*", "0", "1")): ("q_cge_rewind_true", ("*", "*", "*"), Direction.LEFT),
        ("q_cge_compare", ("*", "1", "0")): ("q_cge_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_cge_compare", ("B", "B", "B")): ("q_cge_rewind_true", ("*", "*", "*"), Direction.LEFT),
        ("q_cge_start", ("B", "B", "B")): ("q_cge_compare", ("B", "B", "B"), Direction.RIGHT),
        # Rebobinação.
        ("q_cge_rewind_true", ("0", "*", "*")): ("q_cge_rewind_true", ("0", "*", "*"), Direction.LEFT),
        ("q_cge_rewind_true", ("1", "*", "*")): ("q_cge_rewind_true", ("1", "*", "*"), Direction.LEFT),
        ("q_cge_rewind_true", ("B", "B", "B")): ("q_cge_true", ("B", "B", "B"), Direction.RIGHT),
        ("q_cge_rewind_false", ("0", "*", "*")): ("q_cge_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_cge_rewind_false", ("1", "*", "*")): ("q_cge_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_cge_rewind_false", ("B", "B", "B")): ("q_cge_false", ("B", "B", "B"), Direction.RIGHT),
    },
)

check_remainder_is_zero = TuringMachineDefinition(
    Q={
        "q_checkremainder_0",
        "q_checkremainder_rewind_true",
        "q_checkremainder_rewind_false",
        "q_checkremainder_true",
        "q_checkremainder_false",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_checkremainder_0",
    F={"q_checkremainder_true", "q_checkremainder_false"},
    delta={
        ("q_checkremainder_0", ("*", "*", "0")): ("q_checkremainder_0", ("*", "*", "*"), Direction.RIGHT),
        ("q_checkremainder_0", ("*", "*", "1")): ("q_checkremainder_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_checkremainder_0", ("B", "B", "B")): ("q_checkremainder_rewind_true", ("B", "B", "B"), Direction.LEFT),
        # Rebobinação.
        ("q_checkremainder_rewind_true", ("0", "*", "*")): ("q_checkremainder_rewind_true", ("0", "*", "*"), Direction.LEFT),
        ("q_checkremainder_rewind_true", ("1", "*", "*")): ("q_checkremainder_rewind_true", ("1", "*", "*"), Direction.LEFT),
        ("q_checkremainder_rewind_true", ("B", "B", "B")): ("q_checkremainder_true", ("B", "B", "B"), Direction.RIGHT),
        ("q_checkremainder_rewind_false", ("0", "*", "*")): ("q_checkremainder_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_checkremainder_rewind_false", ("1", "*", "*")): ("q_checkremainder_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("q_checkremainder_rewind_false", ("B", "B", "B")): ("q_checkremainder_false", ("B", "B", "B"), Direction.RIGHT),
    },
)

cleanup_tape3 = TuringMachineDefinition(
    Q={
        "q_cleanup_0",
        "q_cleanup_rewind",
        "q_cleanup_end",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_cleanup_0",
    F={
        "q_cleanup_end",
    },
    delta={
        ("q_cleanup_0", ("0", "*", "*")): ("q_cleanup_0", ("*", "*", "*"), Direction.RIGHT),
        ("q_cleanup_0", ("1", "*", "*")): ("q_cleanup_0", ("*", "*", "*"), Direction.RIGHT),
        ("q_cleanup_0", ("B", "B", "B")): ("q_cleanup_rewind", ("B", "B", "B"), Direction.LEFT),
        ("q_cleanup_rewind", ("0", "*", "*")): ("q_cleanup_rewind", ("0", "*", "B"), Direction.LEFT),
        ("q_cleanup_rewind", ("1", "*", "*")): ("q_cleanup_rewind", ("1", "*", "B"), Direction.LEFT),
        ("q_cleanup_rewind", ("B", "B", "B")): ("q_cleanup_end", ("B", "B", "B"), Direction.RIGHT),
    },
)

primality_test_definition = TuringMachineDefinition(
    Q={
        # Estados do Orquestrador
        "q_start",
        "q_accept",
        "q_reject",
        # Sub-rotina: INIT_DIVISOR
        "init__q0",
        "init__q_write0",
        "init__q_write1",
        "init__q_fill_zeros",
        "init__q_rewind",
        # Sub-rotina: COMPARE_EQUALITY (N == D)
        "compare_eq__q_seek_end",
        "compare_eq__q_compare",
        "compare_eq__q_notequal_rewind",
        # Sub-rotina: COPY_TAPE_1_TO_3
        "copy__q_copy",
        "copy__q_rewind",
        # Sub-rotina: COMPARE_GREATER_EQUAL (T3 >= T2)
        "compare_ge__q_seek_end",
        "compare_ge__q_compare_len",
        "compare_ge__q_rewind_msb",
        "compare_ge__q_compare_msb",
        "compare_ge__q_rewind_false",
        "compare_ge__q_rewind_true",
        # Sub-rotina: SUBTRACT
        "subtract__q0",
        "subtract__q1",
        "subtract__q2",
        "subtract__q_rewind",
        # Sub-rotina: CHECK_REMAINDER_IS_ZERO
        "check_remainder__q_check",
        "check_remainder__q_rewind",
        # Sub-rotina: CLEANUP_TAPE_3
        "cleanup__q_0",
        "cleanup__q_rewind",
        # Sub-rotina: INCREMENT_DIVISOR
        "increment__q_seek_end",
        "increment__q_add_carry",
        "increment__q_rewind",
    },
    Sigma={"0", "1"},
    Gamma={"0", "1", "B"},
    BlankSymbol="B",
    q0="q_start",
    F={"q_accept", "q_reject"},
    delta={
        # ======================================================================
        # Ponto de Entrada
        # ======================================================================
        ("q_start", ("*", "*", "*")): ("init__q0", ("*", "*", "*"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 1: INIT_DIVISOR (FITA_2 <- 2)
        # ======================================================================
        ("init__q0", ("0", "*", "*")): ("init__q0", ("*", "0", "*"), Direction.RIGHT),
        ("init__q0", ("1", "*", "*")): ("init__q0", ("*", "0", "*"), Direction.RIGHT),
        ("init__q0", ("B", "B", "B")): ("init__q_write0", ("B", "B", "B"), Direction.LEFT),
        ("init__q_write0", ("*", "*", "*")): ("init__q_write1", ("*", "0", "*"), Direction.LEFT),
        ("init__q_write1", ("*", "*", "*")): ("init__q_fill_zeros", ("*", "1", "*"), Direction.LEFT),
        ("init__q_fill_zeros", ("0", "*", "*")): ("init__q_fill_zeros", ("*", "0", "*"), Direction.LEFT),
        ("init__q_fill_zeros", ("1", "*", "*")): ("init__q_fill_zeros", ("*", "0", "*"), Direction.LEFT),
        ("init__q_fill_zeros", ("B", "B", "B")): ("init__q_rewind", ("B", "B", "B"), Direction.RIGHT),
        ("init__q_rewind", ("0", "*", "*")): ("init__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("init__q_rewind", ("1", "*", "*")): ("init__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("init__q_rewind", ("B", "B", "B")): ("compare_eq__q_seek_end", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 2: COMPARE_EQUALITY (SE FITA_1 == FITA_2)
        # ======================================================================
        ("compare_eq__q_seek_end", ("0", "*", "*")): ("compare_eq__q_seek_end", ("0", "*", "*"), Direction.RIGHT),
        ("compare_eq__q_seek_end", ("1", "*", "*")): ("compare_eq__q_seek_end", ("1", "*", "*"), Direction.RIGHT),
        ("compare_eq__q_seek_end", ("B", "B", "B")): ("compare_eq__q_compare", ("B", "B", "B"), Direction.LEFT),
        ("compare_eq__q_compare", ("0", "0", "*")): ("compare_eq__q_compare", ("0", "0", "*"), Direction.LEFT),
        ("compare_eq__q_compare", ("1", "1", "*")): ("compare_eq__q_compare", ("1", "1", "*"), Direction.LEFT),
        ("compare_eq__q_compare", ("B", "B", "B")): ("q_accept", ("B", "B", "B"), Direction.RIGHT),
        ("compare_eq__q_compare", ("0", "1", "*")): ("compare_eq__q_notequal_rewind", ("*", "*", "*"), Direction.LEFT),
        ("compare_eq__q_compare", ("1", "0", "*")): ("compare_eq__q_notequal_rewind", ("*", "*", "*"), Direction.LEFT),
        ("compare_eq__q_notequal_rewind", ("0", "*", "*")): ("compare_eq__q_notequal_rewind", ("*", "*", "*"), Direction.LEFT),
        ("compare_eq__q_notequal_rewind", ("1", "*", "*")): ("compare_eq__q_notequal_rewind", ("*", "*", "*"), Direction.LEFT),
        ("compare_eq__q_notequal_rewind", ("B", "B", "B")): ("copy__q_copy", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 3: COPY_TAPE_1_TO_3 (FITA_3 <- FITA_1)
        # ======================================================================
        ("copy__q_copy", ("0", "*", "*")): ("copy__q_copy", ("*", "*", "0"), Direction.RIGHT),
        ("copy__q_copy", ("1", "*", "*")): ("copy__q_copy", ("*", "*", "1"), Direction.RIGHT),
        ("copy__q_copy", ("B", "B", "B")): ("copy__q_rewind", ("B", "B", "B"), Direction.LEFT),
        ("copy__q_rewind", ("0", "*", "*")): ("copy__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("copy__q_rewind", ("1", "*", "*")): ("copy__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("copy__q_rewind", ("B", "B", "B")): ("compare_ge__q_seek_end", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 4: COMPARE_GREATER_EQUAL (SE FITA_3 >= FITA_2)
        # ======================================================================
        ("compare_ge__q_seek_end", ("0", "*", "*")): ("compare_ge__q_seek_end", ("0", "*", "*"), Direction.RIGHT),
        ("compare_ge__q_seek_end", ("1", "*", "*")): ("compare_ge__q_seek_end", ("1", "*", "*"), Direction.RIGHT),
        ("compare_ge__q_seek_end", ("B", "B", "B")): ("compare_ge__q_compare_len", ("B", "B", "B"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "0", "0")): ("compare_ge__q_compare_len", ("*", "0", "0"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "1", "1")): ("compare_ge__q_compare_len", ("*", "1", "1"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "0", "1")): ("compare_ge__q_compare_len", ("*", "0", "1"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "1", "0")): ("compare_ge__q_compare_len", ("*", "1", "0"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "B", "0")): ("compare_ge__q_rewind_true", ("*", "B", "0"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "B", "1")): ("compare_ge__q_rewind_true", ("*", "B", "1"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "0", "B")): ("compare_ge__q_rewind_false", ("*", "0", "B"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("*", "1", "B")): ("compare_ge__q_rewind_false", ("*", "1", "B"), Direction.LEFT),
        ("compare_ge__q_compare_len", ("B", "B", "B")): ("compare_ge__q_rewind_msb", ("B", "B", "B"), Direction.RIGHT),
        ("compare_ge__q_rewind_msb", ("0", "*", "*")): ("compare_ge__q_rewind_msb", ("0", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_msb", ("1", "*", "*")): ("compare_ge__q_rewind_msb", ("1", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_msb", ("B", "B", "B")): ("compare_ge__q_compare_msb", ("B", "B", "B"), Direction.RIGHT),
        ("compare_ge__q_compare_msb", ("*", "0", "0")): ("compare_ge__q_compare_msb", ("*", "0", "0"), Direction.RIGHT),
        ("compare_ge__q_compare_msb", ("*", "1", "1")): ("compare_ge__q_compare_msb", ("*", "1", "1"), Direction.RIGHT),
        ("compare_ge__q_compare_msb", ("*", "0", "1")): ("compare_ge__q_rewind_true", ("*", "0", "1"), Direction.LEFT),
        ("compare_ge__q_compare_msb", ("*", "1", "0")): ("compare_ge__q_rewind_false", ("*", "1", "0"), Direction.LEFT),
        ("compare_ge__q_compare_msb", ("B", "B", "B")): ("compare_ge__q_rewind_true", ("B", "B", "B"), Direction.LEFT),
        ("compare_ge__q_rewind_true", ("0", "*", "*")): ("compare_ge__q_rewind_true", ("*", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_true", ("1", "*", "*")): ("compare_ge__q_rewind_true", ("*", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_true", ("B", "B", "B")): ("subtract__q0", ("B", "B", "B"), Direction.RIGHT),
        ("compare_ge__q_rewind_false", ("0", "*", "*")): ("compare_ge__q_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_false", ("1", "*", "*")): ("compare_ge__q_rewind_false", ("*", "*", "*"), Direction.LEFT),
        ("compare_ge__q_rewind_false", ("B", "B", "B")): ("check_remainder__q_check", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 5: SUBTRACT (FITA_3 <- FITA_3 - FITA_2)
        # ======================================================================
        ("subtract__q0", ("0", "*", "*")): ("subtract__q0", ("*", "*", "*"), Direction.RIGHT),
        ("subtract__q0", ("1", "*", "*")): ("subtract__q0", ("*", "*", "*"), Direction.RIGHT),
        ("subtract__q0", ("B", "B", "B")): ("subtract__q1", ("B", "B", "B"), Direction.LEFT),
        ("subtract__q1", ("*", "0", "0")): ("subtract__q1", ("*", "*", "0"), Direction.LEFT),
        ("subtract__q1", ("*", "0", "1")): ("subtract__q1", ("*", "*", "1"), Direction.LEFT),
        ("subtract__q1", ("*", "1", "1")): ("subtract__q1", ("*", "*", "0"), Direction.LEFT),
        ("subtract__q1", ("*", "1", "0")): ("subtract__q2", ("*", "*", "1"), Direction.LEFT),
        ("subtract__q2", ("*", "0", "1")): ("subtract__q1", ("*", "*", "0"), Direction.LEFT),
        ("subtract__q2", ("*", "0", "0")): ("subtract__q2", ("*", "*", "1"), Direction.LEFT),
        ("subtract__q2", ("*", "1", "1")): ("subtract__q2", ("*", "*", "1"), Direction.LEFT),
        ("subtract__q2", ("*", "1", "0")): ("subtract__q2", ("*", "*", "0"), Direction.LEFT),
        ("subtract__q1", ("B", "B", "B")): ("subtract__q_rewind", ("B", "B", "B"), Direction.RIGHT),
        ("subtract__q2", ("B", "B", "B")): ("subtract__q_rewind", ("B", "B", "B"), Direction.RIGHT),
        ("subtract__q_rewind", ("0", "*", "*")): ("subtract__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("subtract__q_rewind", ("1", "*", "*")): ("subtract__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("subtract__q_rewind", ("B", "B", "B")): ("compare_ge__q_seek_end", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 6: CHECK_REMAINDER_IS_ZERO (SE FITA_3 == 0)
        # ======================================================================
        ("check_remainder__q_check", ("*", "*", "0")): ("check_remainder__q_check", ("*", "*", "*"), Direction.RIGHT),
        ("check_remainder__q_check", ("*", "*", "1")): ("check_remainder__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("check_remainder__q_check", ("B", "B", "B")): ("q_reject", ("B", "B", "B"), Direction.RIGHT),
        ("check_remainder__q_rewind", ("0", "*", "*")): ("check_remainder__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("check_remainder__q_rewind", ("1", "*", "*")): ("check_remainder__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("check_remainder__q_rewind", ("B", "B", "B")): ("cleanup__q_0", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 7: CLEANUP_TAPE_3 (Limpa Fita 3)
        # ======================================================================
        ("cleanup__q_0", ("*", "*", "0")): ("cleanup__q_0", ("*", "*", "B"), Direction.RIGHT),
        ("cleanup__q_0", ("*", "*", "1")): ("cleanup__q_0", ("*", "*", "B"), Direction.RIGHT),
        ("cleanup__q_0", ("B", "B", "B")): ("cleanup__q_rewind", ("B", "B", "B"), Direction.LEFT),
        ("cleanup__q_rewind", ("0", "*", "*")): ("cleanup__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("cleanup__q_rewind", ("1", "*", "*")): ("cleanup__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("cleanup__q_rewind", ("B", "B", "B")): ("increment__q_seek_end", ("B", "B", "B"), Direction.RIGHT),
        # ======================================================================
        # SUB-ROTINA 8: INCREMENT_DIVISOR (FITA_2 <- FITA_2 + 1)
        # ======================================================================
        ("increment__q_seek_end", ("0", "*", "*")): ("increment__q_seek_end", ("*", "*", "*"), Direction.RIGHT),
        ("increment__q_seek_end", ("1", "*", "*")): ("increment__q_seek_end", ("*", "*", "*"), Direction.RIGHT),
        ("increment__q_seek_end", ("B", "B", "B")): ("increment__q_add_carry", ("B", "B", "B"), Direction.LEFT),
        ("increment__q_add_carry", ("*", "0", "*")): ("increment__q_rewind", ("*", "1", "*"), Direction.LEFT),
        ("increment__q_add_carry", ("*", "1", "*")): ("increment__q_add_carry", ("*", "0", "*"), Direction.LEFT),
        ("increment__q_add_carry", ("*", "B", "*")): ("increment__q_rewind", ("*", "1", "*"), Direction.LEFT),
        ("increment__q_rewind", ("0", "*", "*")): ("increment__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("increment__q_rewind", ("1", "*", "*")): ("increment__q_rewind", ("*", "*", "*"), Direction.LEFT),
        ("increment__q_rewind", ("B", "B", "B")): ("compare_eq__q_seek_end", ("B", "B", "B"), Direction.RIGHT),
    },
)
