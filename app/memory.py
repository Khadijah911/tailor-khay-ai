from langgraph.store.memory import InMemoryStore
store=InMemoryStore()
phone='09063456960'
store.put(
    namespace=('customers',phone),
    key='preference_1',
    value={
        "type": "preference",
        "content": "Customer prefers afternoon fittings."
    }
)

memories = store.search(
    namespace=("customers", phone)
)

print(memories)