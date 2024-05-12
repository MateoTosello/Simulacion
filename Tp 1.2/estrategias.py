import random


def spin_wheel():
    return random.randint(0, 36)


def martingale_strategy(initial_bet, target_profit, max_rounds):
    balance = 0
    bet = initial_bet
    round = 0

    while balance < target_profit and round < max_rounds:
        result = spin_wheel()
        if result % 2 == 0:  # Red
            balance += bet
            bet = initial_bet
        else:  # Black
            balance -= bet
            bet *= 2
        round += 1

    if balance >= target_profit:
        return True
    else:
        return False


def dalembert_strategy(initial_bet, target_profit, max_rounds):
    balance = 0
    bet = initial_bet
    round = 0

    while balance < target_profit and round < max_rounds:
        result = spin_wheel()
        if result % 2 == 0:  # Red
            balance += bet
            if bet > initial_bet:
                bet -= 1
        else:  # Black
            balance -= bet
            bet += 1
        round += 1

    if balance >= target_profit:
        return True
    else:
        return False


def fibonacci_strategy(initial_bet, target_profit, max_rounds):
    balance = 0
    bet = initial_bet
    round = 0
    fib = [1, 1]

    while balance < target_profit and round < max_rounds:
        result = spin_wheel()
        if result % 2 == 0:  # Red
            balance += bet
            if len(fib) > 2:
                fib.pop()
                fib[-1] = fib[-1] + fib[-2]
        else:  # Black
            balance -= bet
            fib.append(fib[-1] + fib[-2])
            bet = fib[-1]
        round += 1

    if balance >= target_profit:
        return True
    else:
        return False


def simulate_game(strategy, initial_bet, target_profit, max_rounds, num_simulations):
    successful_runs = 0
    for _ in range(num_simulations):
        if strategy(initial_bet, target_profit, max_rounds):
            successful_runs += 1


# Parámetros de la simulación
initial_bet = 10
target_profit = 100
max_rounds = 1000
num_simulations = 1000

# Simulación de la estrategia de Martingala
martingale_success_rate = simulate_game(
    martingale_strategy, initial_bet, target_profit, max_rounds, num_simulations)
print("Martingale Success Rate:", martingale_success_rate)

# Simulación de la estrategia de D'Alembert
dalembert_success_rate = simulate_game(
    dalembert_strategy, initial_bet, target_profit, max_rounds, num_simulations)
print("D'Alembert Success Rate:", dalembert_success_rate)

# Simulación de la estrategia de Fibonacci
fibonacci_success_rate = simulate_game(
    fibonacci_strategy, initial_bet, target_profit, max_rounds, num_simulations)
print("Fibonacci Success Rate:", fibonacci_success_rate)
