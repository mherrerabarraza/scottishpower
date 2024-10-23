from datetime import datetime

import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Load Magazine Information and Magazine Content CSV files
# Is it asssumed that this data was proccessed in a previous steps
# where the info from the magazine was extracted and stored in a CSV file

magazine_content_df = pd.read_csv("../data/random_magazine_data.csv", sep=";")

# Prepare data for insertion
# prepared for using pgvector
def prepare_record(row):
    # Create a content string for the keyword search index
    content = (
        f"title: {row['title']}\n"
        f"author: {row['author']}\n"
        f"publication_date: {row['publication_date']}\n"
        f"category: {row['category']}\n"
        f"content: {row['content']}"
    )
    # The generated vector embedding for vector search
    # https://timescale.github.io/python-vector/tsv_python_getting_started_tutorial.html
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "title": row["title"],
                "author": row["author"],
                "category": row["category"],
                "publication_date": row["publication_date"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )



# Apply preparation DataFrames
records_df = magazine_content_df.apply(prepare_record, axis=1)

# Create tables and insert data
vec.create_tables()

# Create the StreamingDiskANN index to speed up similarity search
vec.create_index()
# Create the GIN index for keyword search
vec.create_keyword_search_index()
# Insert the records into the database
vec.upsert(records_df)
