from database.memory import save_memory, load_memories

save_memory(
    "08073143931",
    "preference",
    "Customer prefers afternoon appointments."
)

print(load_memories("08073143931"))