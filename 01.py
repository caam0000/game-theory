# version 0.2
import random
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import time

# Parameters
n = 20
min_trials = 10000  # Minimum number of trials before checking error
max_trials = 100000000  # Maximum number of trials to prevent infinite loop
relative_error_threshold = 0.1  # Stop when relative error is below this value
num_workers = multiprocessing.cpu_count()  # Use all available cores

print("The script is running")
print(f"n is specified as: {n}")
print("good luck")

def run_trial(n):
    """Perform a single trial of the prisoner problem."""
    boxes = list(range(n))
    random.shuffle(boxes)

    for prisoner in range(n):
        start_box = prisoner
        checked_boxes = [(start_box + i) % n for i in range(n // 2)]
        if prisoner not in [boxes[i] for i in checked_boxes]:
            return 0  # Failure
    return 1  # Success

def main():
    trial_count = 0
    success_count = 0

    start_time = time.time()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        batch_size = 5000  # Collect results in batches
        while trial_count < max_trials:
            # Submit batch
            futures = [executor.submit(run_trial, n) for _ in range(batch_size)]
            results = [future.result() for future in futures]

            success_count += sum(results)
            trial_count += batch_size

            estimated_probability = success_count / trial_count
            if success_count > 0:
                relative_error = (1 / (success_count ** 0.5))
            else:
                relative_error = float('inf')

            if trial_count % 10000 == 0:
                print(f"Trials: {trial_count}, Successes: {success_count}")

            if trial_count % 100000 == 0:
                elapsed_time = time.time() - start_time
                print(f"The calculated relative error rate is: {relative_error:.5f}, and the goal is {relative_error_threshold}")
                print(f"The estimated probability right now is {estimated_probability:.10f}")
                print(f"Time elapsed: {elapsed_time:.2f} seconds")

            # Check relative error after minimum trials
            if trial_count >= min_trials and relative_error < relative_error_threshold:
                break

    estimated_probability = success_count / trial_count
    end_time = time.time()

    print(f"Estimated Probability of Success: {estimated_probability:.10f}")
    print(f"Number of Trials: {trial_count}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
