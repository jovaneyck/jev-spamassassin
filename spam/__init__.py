import sys

# Old spam is full of odd characters. Replace what the terminal can't encode instead of crashing,
# which happens on Windows when a coding agent pipes the output.
sys.stdout.reconfigure(errors="replace")
