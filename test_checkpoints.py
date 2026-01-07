import sys
from first_module import increment_by_one, increment_by_two, global_counter
from second_module import increment_by_three, increment_by_four
from checkpoints import cleanup_all_markers

def main():
    # Accept a crash point as a command-line argument
    crash_at = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    try:
        if crash_at == 1:
            raise Exception("Crash after first increment")
        increment_by_one()

        if crash_at == 2:
            raise Exception("Crash after second increment")
        increment_by_two()

        if crash_at == 3:
            raise Exception("Crash after third increment")
        increment_by_three()

        if crash_at == 4:
            raise Exception("Crash after fourth increment")
        increment_by_four()

        print(f"Final counter value: {global_counter['value']}")
        cleanup_all_markers()
    except Exception as e:
        print(f"Simulated crash: {e}")
        print(f"Counter value at crash: {global_counter['value']}")

if __name__ == "__main__":
    main()