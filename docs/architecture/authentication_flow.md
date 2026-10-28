# Architecture - Authentication & Security Flow

This document outlines the authentication and token management architecture implemented in the BookMyShow backend.

---

## 1. Hybrid Security Architecture

BookMyShow uses a **Hybrid JWT + HttpOnly Cookie** design pattern to combine the high throughput of stateless token validation with enterprise-grade defenses against credential theft.

| Token Type | Lifespan | Delivery / Storage | Security Profile | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Access Token** | 15 Minutes | HTTP `Authorization: Bearer <token>` | In-Memory (Client) | Grants access to protected endpoints |
| **Refresh Token** | 1 Day | Cookie: `refresh` | `HttpOnly`, `SameSite=Lax`, `Secure` | Obtains new access tokens upon expiry |

### Security Advantages:
- **XSS Protection**: Malicious client-side scripts running in the browser cannot read or extract the `refresh` token because it is protected by the browser's `HttpOnly` flag.
- **CSRF Mitigation**: The short-lived access token is not automatically sent by the browser; it must be explicitly injected into headers by client application code.
- **Stateless Efficiency**: The API gateway verifies access tokens using symmetric cryptographic signatures (`SIGNING_KEY`) without issuing database queries.

---

## 2. Authentication Flows & Sequence Diagrams

### 2.1 Login & Initial Token Issuance

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant Auth as LoginUserView
    participant JWT as SimpleJWT Engine
    participant DB as PostgreSQL (User Table)

    Client->>Auth: POST /api/users/login/ {email, password}
    activate Auth
    Auth->>DB: Lookup User by email
    DB-->>Auth: User record & hashed password
    Auth->>Auth: Verify password hash (PBKDF2)

    alt Invalid Credentials
        Auth-->>Client: 400 Bad Request ("Failed to Login")
    else Valid Credentials
        Auth->>JWT: Generate Access & Refresh Tokens
        JWT-->>Auth: {access_token, refresh_token}
        Note over Auth: Extract refresh_token from body<br/>Attach as HttpOnly Cookie
        Auth-->>Client: 200 OK {access: "..."}<br/>Set-Cookie: refresh=...; HttpOnly; SameSite=Lax
    end
    deactivate Auth
```

---

### 2.2 Token Refresh with Rotation & Blacklisting

When the short-lived access token expires, the client calls `/api/users/refresh/`. The browser automatically includes the `refresh` cookie.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant Refresh as CustomTokenRefreshView
    participant Blacklist as TokenBlacklist Table
    participant JWT as SimpleJWT Engine

    Client->>Refresh: POST /api/users/refresh/ (Cookie: refresh=...)
    activate Refresh

    alt Cookie Missing
        Refresh-->>Client: 401 Unauthorized ("Refresh token missing")
    end

    Refresh->>Blacklist: Check if incoming refresh token is blacklisted
    alt Token is Blacklisted
        Blacklist-->>Refresh: Found in Blacklist
        Refresh-->>Client: 401 Unauthorized ("Token is blacklisted")
    else Token is Valid
        Note over Refresh,Blacklist: Add old refresh token to Blacklist
        Refresh->>JWT: Generate new Access & Refresh Token pair
        JWT-->>Refresh: New tokens
        Note over Refresh: Update Set-Cookie with new refresh token
        Refresh-->>Client: 200 OK {access: "<new_access_token>"}<br/>Set-Cookie: refresh=<new_token>; HttpOnly
    end
    deactivate Refresh
```

---

### 2.3 Logout & Token Invalidation

Logging out completely terminates the session on both client and server:

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant Logout as LogoutView
    participant Blacklist as TokenBlacklist Table

    Client->>Logout: POST /api/users/logout/ (Cookie: refresh=...)
    activate Logout
    Logout->>Blacklist: Insert refresh token into blacklist table
    Note over Logout: Delete 'refresh' cookie (max_age=0)
    Logout-->>Client: 200 OK ("You have logged out successfully")<br/>Set-Cookie: refresh=; Max-Age=0
    deactivate Logout
```

---

## 3. Password Policies & Validation

All user registration and password updates are checked against a strict multi-tiered validator stack defined in [`apps/user/validators.py`](../../apps/user/validators.py):

1. **Length**: Minimum 8 characters.
2. **Character Classes**:
   - At least one uppercase letter (`[A-Z]`).
   - At least one lowercase letter (`[a-z]`).
   - At least one numeric digit (`[0-9]`).
   - At least one special symbol (`[!@#$%^&*(),.?":{}|<>]`).
3. **Similarity & Common Password Checks**: Integrated with Django's `UserAttributeSimilarityValidator` and `CommonPasswordValidator`.

---

## 4. Maintenance: Flushing Expired Blacklisted Tokens

Blacklisted tokens accumulate in PostgreSQL over time. The backend provides a pre-configured command to purge expired tokens:

```bash
pipenv run flushexpiredtokens
```
This can be scheduled as a routine background cron job in production environments.
