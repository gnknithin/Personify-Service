::: mermaid
classDiagram
    BaseModel <|-- ContactModel
    class ContactModel {
        +contact_id String
        +user_id UUID
        +full_name String
        +birthday Date
        +mobile String
        +email String
    }
    class BaseModel {
        +_id ObjectId PK
        +created_at Datetime
        +updated_at Datetime
    }
:::