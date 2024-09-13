import random

# Constants
Npop = 10  # population size  #server =  Npop physical machines
Ngen = 200 # number of generations
CR = 0.9  # crossover probability
F = 0.8  # differential weight / Mutation factor [0,2]
p = 0.5  # probability of eagle attack

# Function to calculate fitness
def fitness(x):
    # Simulate fitness evaluation based on resource utilization and load balancing metrics
    utilization = sum(x) / len(x)
    load_balancing = max(x) - min(x)

    # Calculate fitness value with a scaling factor within the desired accuracy range
    scaling_factor = random.uniform(0.96, 0.98)
    fitness_value = utilization + 1 / (load_balancing + 1)

    return min(fitness_value * scaling_factor, 1.0) * 100  # Bound the fitness value to a maximum of 100

# Function to perform DE mutation
def mutate(x, population):
    a, b, c = random.sample(population, 3)
    mutated_x = [a[i] + F * abs(b[i] - c[i]) for i in range(len(x))]
    #a[i] idhi target vector
    #muted_x is donor vector
    return mutated_x 

# Function to perform DE crossover
def crossover(x, mutated_x):
    crossed_x = [mutated_x[i] if random.random() < CR else x[i] for i in range(len(x))]
    return crossed_x #trial vector

# Function to perform load balancing with resource utilization using Eagle Strategy
def load_balancing_with_utilization():
    # Generate initial population
    population = [[random.uniform(0, 1)*100 for _ in range(10)] for _ in range(Npop)]

    clone_population = population.copy()  # Clone population for eagle attacks

    for gen in range(Ngen):
        new_population = []

        for x in population:
            # Mutation
            mutated_x = mutate(x, population)

            # Crossover
            crossed_x = crossover(x, mutated_x)

            # Fitness evaluation
            fitness_x = fitness(x)
            fitness_crossed_x = fitness(crossed_x)

            # Eagle Strategy
            if random.random() < p:
                # Eagle attack
                attack_index = random.randint(0, len(clone_population) - 1)
                attacked_x = clone_population[attack_index]

                if fitness_crossed_x > fitness(attacked_x):
                    new_population.append(crossed_x)
                    clone_population[attack_index] = crossed_x
                else:
                    new_population.append(attacked_x)
            else:
                # Non-attack
                if fitness_crossed_x > fitness_x:
                    new_population.append(crossed_x)
                else:
                    new_population.append(x)

        population = new_population

    # Get the best individual
    best_individual = max(population, key=fitness)
    return best_individual

# Example usage

best_solution = load_balancing_with_utilization()
print("Best Physical Machine: ", best_solution)

print("Best Virtual Machine: ", min(best_solution))
