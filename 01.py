import random

# Parameters
n = 20
min_trials = 10000  # Minimum number of trials before checking error
max_trials = 100000000  # Maximum number of trials to prevent infinite loop
relative_error_threshold = 0.1  # Stop when relative error is below this value

# Simulation
success_count = 0
trial_count = 0

while trial_count < max_trials:
    # Randomly shuffle the boxes
    boxes = list(range(n))
    random.shuffle(boxes)
    
    # Check if all prisoners succeed
    success = True
    for prisoner in range(n):
        # Determine the boxes this prisoner is allowed to check
        start_box = prisoner
        checked_boxes = [(start_box + i) % n for i in range(n // 2)]
        
        # Check if prisoner's number is in one of the checked boxes
        if prisoner not in [boxes[i] for i in checked_boxes]:
            success = False
            break
    
    if success:
        success_count += 1
    
    trial_count += 1

    # Check relative error after minimum trials
    if trial_count >= min_trials:
        estimated_probability = success_count / trial_count
        if success_count > 0:
            relative_error = (1 / (success_count ** 0.5))
        else:
            relative_error = float('inf')

        if relative_error < relative_error_threshold:
            break

# Final estimate
estimated_probability = success_count / trial_count
print(f"Estimated Probability of Success: {estimated_probability:.10f}")
print(f"Number of Trials: {trial_count}")
