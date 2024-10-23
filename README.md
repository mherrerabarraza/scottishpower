
# Hybrid Search API for Magazine Data

This project implements an API with one endpoint to perform a hybrid search in a table of 1 million records. The hybrid search combines keyword-based and vector-based searches, providing both types of results. The data model consists of two tables: one containing the main information of a magazine and the other containing all the content of the magazine.

## Prerequisites

- Docker
- Python 3.9
- OpenAI API key (Provided)
- PostgreSQL GUI client (DBeaver, PGAdmin, etc.)

## Getting Started

1. Create a copy of `example.env.docker` and rename it to `.env`.
2. Open `.env` and fill in the OpenAI API key (provided), leaving everything else unchanged.
3. Run the Docker container:

   ```bash
   docker-compose up --build -d
   ```

4. Go to [http://localhost:8000/docs](http://localhost:8000/docs) to view the API documentation and run queries.

## Data Model

This solution is based on a magazine database with two tables:

- **Table 1: Magazine Information**
  - Fields: `id`, `title`, `author`, `publication_date`, `category`, etc.
- **Table 2: Magazine Content**
  - Fields: `id`, `magazine_id` (foreign key to Magazine Information), `content`, `vector_representation`, etc.

The table structure for vector search is enhanced with OpenAI embeddings, resulting in:

- `id`: Generated using `UUID` with the current timestamp (`datetime.now()`).
- `metadata`: Contains the original data such as title, author, category, and publication date.
- `contents`: A processed representation of the original content for keyword search.
- `embeddings`: Vector representations (generated using OpenAI embeddings) of the content.

## How It Works

### Indexing

Two indices are created to optimize search performance:

1. **DiskANN Index** for vector-based searches, allowing fast similarity searches on vector representations (embeddings).
2. **GIN Index** for keyword-based searches, optimizing full-text search queries.

More information on how this indexing improves performance can be found [here](https://www.timescale.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost/).

## Hybrid Search

The hybrid search combines both keyword-based and semantic search results. Here’s how each search works:

### Keyword Search

The keyword search is based on PostgreSQL full-text search functionality, using `ts_vector` and `websearch_to_tsquery`:

```sql
SELECT id, contents, ts_rank_cd(to_tsvector('english', contents), query) as rank
FROM {self.vector_settings.table_name}, websearch_to_tsquery('english', %s) query
WHERE to_tsvector('english', contents) @@ query
ORDER BY rank DESC
LIMIT %s
```

### Semantic Search

The semantic search leverages vector representations (embeddings) generated using OpenAI. It finds records based on vector similarity.

### Combining Results

The hybrid search merges both keyword and semantic search results, removes duplicates, and returns the most relevant results based on ranking.

## Example Query

```bash
GET /search?query=information about Programming
```

### Complete Response:

```json
{
  "hybrid_results": [
    {
      "id": "f137935a-9120-11ef-a15a-01321b5fdce0",
      "content": "title: User-centric system-worthy benchmark
author: Crystal White
publication_date: 2002-08-14
category: Programming
content: Information list data child provide return room. Still staff perform effect. Remain sport over enter real yard agent. Adult present yeah road throughout entire technology whole.",
      "search_type": "keyword"
    },
    {
      "id": "5804e736-9121-11ef-b546-5ca07f23a3d3",
      "content": "title: Cross-group interactive methodology
author: Alicia Lewis
publication_date: 2009-10-14
category: Programming
content: Ahead music than develop exactly. Skill yourself radio choice. Live while top hit project west position. True information assume true contain memory.",
      "search_type": "keyword"
    },
    {
      "id": "76c2fb4a-9121-11ef-81d3-a14c56ae2976",
      "content": "title: Programmable empowering flexibility
author: Jason Kelly
publication_date: 2011-09-04
category: Programming
content: Sort theory say this. Able table win appear watch. Force though or run. These movement performance stand.",
      "search_type": "semantic"
    },
    {
      "id": "b0f18f34-9121-11ef-b476-8ff107dbd79c",
      "content": "title: Programmable cohesive standardization
author: Jacob Gonzalez
publication_date: 2003-01-14
category: Programming
content: Performance white test. Statement seat only morning system. Stage example guy single policy. Behavior more require draw herself task human.",
      "search_type": "semantic"
    },
    {
      "id": "e67195ce-9120-11ef-9635-866b78430aaa",
      "content": "title: Tech Monthly
author: John Doe
publication_date: 2020-01-01
category: Programming
content: Java is a great programming language to learn in 2020",
      "search_type": "semantic"
    },
    {
      "id": "33656c5c-9121-11ef-b374-162a5a0fee76",
      "content": "title: Programmable interactive knowledge user
author: Maria Taylor
publication_date: 2019-03-27
category: Historical
content: Peace former nothing draw still seem. Technology of economic Mr no statement show. Data offer range even allow cell girl. Morning nor stay. Plant west wear after side service goal. Wait suffer most work.",
      "search_type": "semantic"
    },
    {
      "id": "6534d47a-9121-11ef-9842-d852d84bbc48",
      "content": "title: Business-focused even-keeled complexity
author: Dr. Elaine Pham
publication_date: 2020-03-06
category: Programming
content: Prepare this argue ago whatever. Through sea reveal type care traditional. Operation yes wide charge wonder history more machine. Position operation certain. Evening would fire throw.",
      "search_type": "semantic"
    }
  ],
  "synthesized_response": {
    "thought_process": [
      "The retrieved data contains various articles related to programming, but they are mostly abstract and do not provide specific information about programming concepts, languages, or practices.",
      "One article mentions Java as a great programming language to learn in 2020, which is a specific piece of information.",
      "The rest of the articles seem to be more about methodologies, benchmarks, and abstract concepts related to programming rather than concrete information about programming itself.",
      "There is not enough detailed context to provide a comprehensive overview of programming as a field."
    ],
    "answer": "The retrieved information includes several articles related to programming, but they mostly focus on abstract concepts, methodologies, and benchmarks. One specific piece of information is that Java was recommended as a great programming language to learn in 2020. However, there is insufficient detailed context to provide a comprehensive overview of programming as a field."
  }
}
```

