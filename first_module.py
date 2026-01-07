from checkpoints import checkpoint

global_counter = {"value": 0}

@checkpoint()
def increment_by_one():
    global_counter["value"] += 1
    print(f"first_module.increment_by_one: {global_counter['value']}")
    return 0

@checkpoint()
def increment_by_two():
    global_counter["value"] += 2
    print(f"first_module.increment_by_two: {global_counter['value']}")
    return 0