import streamlit as st

from src.base import TuringMachine
from src.definitions import primality_test_definition

st.set_page_config(
    page_title="Máquina de Turing - Teste de Primalidade",
)

st.logo(
    image="res/Dc-logo.jpeg",
    size="large",
)

st.markdown(
    body="""
<p style='text-align: center;'>Universidade Federal de São Carlos (UFSCar)</p>
<p style='text-align: center;'>Departamento de Computação (DC)</p>
<p style='text-align: center;'>Vinicius Quaresma da Luz (<a href="mailto:viniciusluz@estudante.ufscar.br">viniciusluz@estudante.ufscar.br</a>)</p>
""",
    unsafe_allow_html=True,
)

st.divider()

st.title("Teste de Primalidade com Máquina de Turing")

st.markdown("Informe um número inteiro maior ou igual a 2 para verificar se é primo.")


number = st.number_input("Digite um número inteiro:", min_value=2, value=7)
verbose = st.checkbox(f"Visualizar estados da máquina {'(impacto pesado na performance)' if number > 30 else ''}", value=True)

if number > 30 and verbose:
    st.warning("Recomendo não usar essa opção com valores acima de 30.")

button_pressed = st.button("Executar Máquina de Turing")

result_info = st.empty()
result_display = st.empty()

if button_pressed:
    turing_machine = TuringMachine(
        definition=primality_test_definition,
        w_1=str(bin(number)[2:]),
        verbose=verbose,
    )

    with st.spinner("Executando a Máquina de Turing..."):
        result = turing_machine.run()

        if result.final_state == "q_accept":
            result_info.success(f"O número {number} é primo.")
        elif result.final_state == "q_reject":
            result_info.error(f"O número {number} não é primo.")

        result_display.markdown(
            f"""
    # Resultado da Máquina de Turing
    - Resultado: `{result.final_state}`
    - Passos: {result.step_count}
    - Tempo gasto: {result.time_spent_in_seconds:.6f} segundos

    ---

    """,
        )
