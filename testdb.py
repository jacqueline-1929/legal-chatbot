from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define a schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=2048)
]
schema = CollectionSchema(fields, "Example collection")

# Create a collection
collection = Collection("example_collection", schema)
collection.create_index(field_name="vector", index_params={"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "L2"})

# Insert vectors
vectors = np.random.rand(10, 2048).astype(np.float32)
entities = [{"name": "vector", "values": vectors}]
collection.insert(entities)

# Perform a similarity search
query_vector = np.random.rand(1, 2048).astype(np.float32)
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(query_vector, "vector", search_params, limit=5)

# Print results
for result in results[0]:
    print(result)

# Clean up
collection.drop()