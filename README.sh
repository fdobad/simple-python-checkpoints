# checkpoints
#
# Usage: Copy checkpoints.py and decorate your functions with @checkpoint.
#        A checkpoins.toml file will be created to track progress.
#        On execution, previously completed functions (with module.method=timestamp lines) will be skipped.
#        On successful completion, checkpoints.toml is deleted and checkpoints_last.toml is created as a record.
#
# Test: This script runs a series of tests on the checkpointing functionality.
#       Including two modules with a orchestrator with multiple checkpointed functions.
#       It simulates crashes and verifies that the checkpointing mechanism

#!/bin/bash

set -e

echo "=== Clean up old checkpoints ==="
rm -f checkpoints.toml checkpoints_last.toml

echo "=== Run with crash after first increment ==="
python3 test_checkpoints.py 1 || true
echo "--- checkpoints.toml after crash 1 ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo

echo "=== Run again (should skip first) ==="
python3 test_checkpoints.py 2 || true
echo "--- checkpoints.toml after crash 2 ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo

echo "=== Run again (should skip first and second) ==="
python3 test_checkpoints.py 3 || true
echo "--- checkpoints.toml after crash 3 ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo

echo "=== Run again (should skip first three) ==="
python3 test_checkpoints.py 4 || true
echo "--- checkpoints.toml after crash 4 ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo

echo "=== Run to completion (should clean up checkpoints.toml, checkpoints_last.toml should exist) ==="
TZ=America/Santiago python3 test_checkpoints.py 0 || true
echo "--- checkpoints.toml after completion ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo "--- checkpoints_last.toml after completion ---"
cat checkpoints_last.toml || echo "No checkpoints_last.toml found"
echo

echo "=== Partial TOML test: simulate missing checkpoints ==="
cp checkpoints_last.toml checkpoints.toml

# Remove first_module.increment_by_two and second_module.increment_by_three from checkpoints.toml
# Keep first_module.increment_by_one and second_module.increment_by_four
python3 -c "
import toml
f = 'checkpoints.toml'
data = toml.load(f)
data['first_module'].pop('increment_by_two', None)
data['second_module'].pop('increment_by_three', None)
with open(f, 'w') as out:
    out.write(toml.dumps(data))
"

echo "--- checkpoints.toml after removing two checkpoints ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo

python3 test_checkpoints.py 5 || true
echo "--- checkpoints.toml after partial run ---"
cat checkpoints.toml || echo "No checkpoints.toml found"
echo "--- checkpoints_last.toml after partial run ---"
cat checkpoints_last.toml || echo "No checkpoints_last.toml found"
echo
