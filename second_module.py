from checkpoints import checkpoint
from first_module import global_counter

@checkpoint()
def increment_by_three():
    global_counter["value"] += 3
    print(f"second_module.increment_by_three: {global_counter['value']}")
    return 0

@checkpoint()
def increment_by_four():
    global_counter["value"] += 4
    print(f"second_module.increment_by_four: {global_counter['value']}")
    return 0