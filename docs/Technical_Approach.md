# Technical Approach: RAG-Powered FAQ Chatbot

## System Architecture
```mermaid
flowchart TB
    subgraph User Layer
        A[Web/Mobile App] -->|HTTP POST| B[API Gateway]
    end

    subgraph n8n Layer
        B --> C{Webhook Router}
        C --> D[Preprocessing Node]
        D --> E[Agent Dispatcher]
        E -->|Simple Query| F[Direct Response Agent]
        E -->|Complex Query| G[RAG Engine]
    end

    subgraph Data Layer
        G --> H[(VectorDB\nChroma/Pinecone)]
        H --> I[Document Chunks]
        G --> J[[LLM Gateway\n(Gemini/OpenAI)]]
    end

    subgraph Output Layer
        F --> K[Response Builder]
        G --> K
        K --> L[User Interface]
    end
```

## Enhanced RAG Pipeline
```mermaid
sequenceDiagram
    participant User
    participant API
    participant Preprocessor
    participant VectorDB
    participant LLM
    participant Cache

    User->>API: POST /ask {question}
    API->>Preprocessor: Sanitize Input
    alt Cached Response
        Preprocessor->>Cache: Check query hash
        Cache-->>API: Return cached answer
    else New Query
        Preprocessor->>VectorDB: Get Similar Chunks
        VectorDB-->>Preprocessor: Top 3 documents
        Preprocessor->>LLM: Generate with Context
        LLM-->>Preprocessor: Formatted Answer
        Preprocessor->>Cache: Store response
        Preprocessor->>API: Return answer
    end
    API->>User: JSON Response
```

## Intelligent Agent Routing
```mermaid
stateDiagram-v2
    [*] --> RequestReceived
    RequestReceived --> InputValidation: Validate JSON
    InputValidation --> QueryClassifier: Clean text

    state QueryClassifier {
        [*] --> Greeting: "Hi/Hello"
        Greeting --> DirectResponse
        [*] --> MetaQuery: "What can you do?"
        MetaQuery --> CapabilitiesAgent
        [*] --> KnowledgeQuery: Default
        KnowledgeQuery --> VectorSearch
    }

    VectorSearch --> LLMOrchestration: Chunks + Question
    LLMOrchestration --> ResponseGeneration
    ResponseGeneration --> [*]
```

## Performance Optimization
```mermaid
gantt
    title Query Processing Timeline
    dateFormat  HH:mm:ss.SSS
    section Request
    HTTP Receiving :00:00.000, 50ms
    JSON Parsing :00:00.050, 20ms
    section Processing
    Vector Search :00:00.070, 300ms
    LLM Generation :00:00.370, 700ms
    section Response
    Formatting :00:01.070, 30ms
    HTTP Send :00:01.100, 40ms
```

## Error Handling Flow
```mermaid
journey
    title Error Recovery Process
    section User Query
      InvalidInput: 5: User sends malformed request
      Timeout: 3: Network delay
    section System Response
      InputError --> Validation: "Return 400 Bad Request"
      Timeout --> Retry: "3 attempts with backoff"
      Fallback --> Cached: "Serve last good response"
    section Metrics
      LogError: 5: Log to monitoring
      AlertTeam: 2: Notify if critical
```

## Component Specifications

```mermaid
classDiagram
    class WebhookListener {
        +path: string
        +methods: POST
        +validateInput()
        +triggerWorkflow()
    }

    class VectorSearch {
        -chunkSize: 512
        -overlap: 128
        +queryEmbeddings()
        +hybridSearch()
    }

    class LLMGateway {
        -model: gemini-pro
        -temperature: 0.3
        +generate(prompt)
        +formatResponse()
    }

    WebhookListener --> VectorSearch : triggers
    VectorSearch --> LLMGateway : provides context
```

## Deployment Architecture
```mermaid
graph LR
    A[User] --> B[Cloudflare]
    B --> C[Load Balancer]
    C --> D[n8n Worker 1]
    C --> E[n8n Worker 2]
    D --> F[(Redis Cache)]
    E --> F
    D --> G[(ChromaDB)]
    E --> G
    G --> H[GCS Document Storage]
```

## How to Generate These Diagrams

1. **Tools Needed**:
   - [Mermaid Live Editor](https://mermaid.live)
   - VS Code with Mermaid plugin
   - PlantUML (alternative)

2. **Export Options**:
```bash
# Convert to PNG
mmdc -i architecture.mmd -o architecture.png -t dark -b transparent

# Convert to PDF
mmdc -i sequence.mmd -o sequence.pdf --scale 2
```

## Key Improvements Over Baseline

```mermaid
pie
    title Feature Comparison
    "Basic RAG" : 35
    "With Agents" : 65
    "Caching" : 45
    "Hybrid Search" : 55
```