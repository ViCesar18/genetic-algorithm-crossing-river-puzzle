import random

from genes import Genes
from person import Person

def generate_random_chromosome(n):
  states = []

  for _ in range(n):
    state = []

    for _ in range(8):
      state.append(random.randint(Genes.LEFT.value, Genes.RIGHT.value))
    
    states.append(state)
    state = []
  
  return states


def calculate_avaliation(state: list):
  if state.count(Genes.CROSSING.value) > 2 or \
    (state.count(Genes.CROSSING.value) != 0 and (state[Person.DAD.value] != Genes.CROSSING.value and state[Person.MOM.value] != Genes.CROSSING.value and state[Person.POLICEMAN.value] != Genes.CROSSING.value)) or \
    (state[Person.POLICEMAN.value] != state[Person.THIEF.value] and state.count(state[Person.THIEF.value]) != 1) or \
    (state[Person.DAD.value] == Genes.CROSSING.value and (state[Person.GIRL_1.value] == Genes.CROSSING.value or state[Person.GIRL_2.value] == Genes.CROSSING.value)) or \
    (state[Person.MOM.value] == Genes.CROSSING.value and (state[Person.BOY_1.value] == Genes.CROSSING.value or state[Person.BOY_2.value] == Genes.CROSSING.value)):
    return -1
  else:
    return state.count(Genes.RIGHT.value)


def fitness_function(states: list):
  avaliations = []

  for state in states:
    avaliations.append({
      'state': state,
      'avaliation_number': calculate_avaliation(state)
    })
  
  return avaliations


def select(avaliations: list):
  selected_avaliations = filter(lambda a: a['avaliation_number'] != -1, avaliations)

  states = []

  for selected_avaliation in selected_avaliations:
    states.append(selected_avaliation['state'])

  return states


def crossover(states: list):
  if len(states) % 2 != 0:
    states.append(states[0])

  cross_states = []

  for i in range(len(states)):
    if i % 2 == 0:
      father1 = states[i]
      father2 = states[i + 1]

      s1_father1 = father1[:4]
      s2_father1 = father1[4:]

      s1_father2 = father2[:4]
      s2_father2 = father2[4:]

      cross_states.append(s1_father1 + s2_father2)
      cross_states.append(s2_father1 + s1_father2)

  return cross_states


def mutate(states: list):
  for state in states:
    i = random.randint(0, 7)
    n = random.randint(0, 2)

    aux_state = state.copy()

    aux_state[i] = n

    if calculate_avaliation(aux_state) >= calculate_avaliation(state):
      state[i] = n

  return states


def has_final_state(states: list):
  for state in states:
    if state.count(Genes.RIGHT.value) == 8:
      return True
  
  return False


mean = []
for _ in range(30):
  states = generate_random_chromosome(100)

  i = 0
  while not has_final_state(states):
    avaliations = fitness_function(states)

    selected_states = select(avaliations)

    cross_states = crossover(selected_states)

    states = mutate(cross_states)

    if len(states) <= 0:
      states += generate_random_chromosome(100)
    
    i += 1
  
  mean.append(i)


print(f'Média de cruzamentos para chegar ao Estado Objetivo (30 execuções): {sum(mean) / len(mean)}')
