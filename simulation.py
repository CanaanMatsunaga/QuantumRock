from qiskit import *
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram



def encode_choices(qc, choices, qubits):
    for idx, choice in enumerate(choices, start=1):
        qc.x(qubits[idx - 1]) if choice == 2 else qc.x(qubits[idx]) if choice == 3 else qc.x(qubits[idx + 1]) if choice == 1 else None

def create_superposition_and_entanglement(qc, qubits):
    for qubit in qubits:
        qc.h(qubit)

def number_to_word(choice):
    if choice == 1:
        return "Rock"
    elif choice == 2:
        return "Scissors"
    elif choice == 3:
        return "Paper"
    else:
        return "Invalid Choice"

qc = QuantumCircuit(3, 2)
c0 = 0
c1 = 1

player1_move = input("Player 1, choose Classical (C) or Quantum (Q): ").lower()
if player1_move == 'c':
    print("Player 1, choose:")
    print("1. Rock")
    print("2. Scissors")
    print("3. Paper")
    player1_choice = int(input())
    print(f"Player 1's choice: {number_to_word(player1_choice)}")
    player1_quantum_choice = None
else:
    print("Player 1, pick two numbers between 1 and 3 (separated by a space): ")
    quantum_choices = [int(x) for x in input().split()]
    print(f"Player 1's Quantum choices: {', '.join(number_to_word(choice) for choice in quantum_choices)}")
    player1_quantum_choice = quantum_choices

player2_move = input("Player 2, choose Classical (C) or Quantum (Q): ").lower()
if player2_move == 'c':
    print("\nPlayer 2, choose:")
    print("1. Rock")
    print("2. Scissors")
    print("3. Paper")
    player2_choice = int(input())
    print(f"Player 2's choice: {number_to_word(player2_choice)}")
    player2_quantum_choice = None
else:
    print("\nPlayer 2, pick two numbers between 1 and 3 (separated by a space): ")
    quantum_choices = [int(x) for x in input().split()]
    print(f"Player 2's Quantum choices: {', '.join(number_to_word(choice) for choice in quantum_choices)}")
    player2_quantum_choice = quantum_choices

create_superposition_and_entanglement(qc, range(3))

if player1_quantum_choice:
    encode_choices(qc, player1_quantum_choice, range(3))

if player2_quantum_choice:
    encode_choices(qc, player2_quantum_choice, range(3))

qc.measure(0, c0)
qc.measure(2, c1)

simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()

counts = result.get_counts()
outcome = list(counts.keys())[0]

print("\nQuantum Circuit:")
print(qc)

print("\nMeasurement Outcomes:")
print(outcome)

print("\nResults:")
print(f"Player 1's choice: {number_to_word(player1_choice)}")
print(f"Player 2's choice: {number_to_word(player2_choice)}")

if player1_choice == player2_choice:
    winner = "It's a tie!"
elif (player1_choice == 1 and player2_choice == 3) or \
     (player1_choice == 2 and player2_choice == 1) or \
     (player1_choice == 3 and player2_choice == 2):
    winner = f"Player 2 wins! {number_to_word(player2_choice)} beats {number_to_word(player1_choice)}"
else:
    winner = f"Player 1 wins! {number_to_word(player1_choice)} beats {number_to_word(player2_choice)}"

print("\nResult:")
print(winner)
