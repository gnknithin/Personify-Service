::: mermaid
classDiagram
    BaseSQLIdModel <|-- UserModel
    class UserModel {
        +username String
        +password String
        +full_name String
        +date_of_birth Date
        +email String
    }
    BaseSQLModel <|-- BaseSQLIdModel
    class BaseSQLIdModel {
        <<Abstract>>
        +id UUID
    }
    class BaseSQLModel {
        <<Abstract>>
        +created_at Datetime
        +updated_at Datetime
    }
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