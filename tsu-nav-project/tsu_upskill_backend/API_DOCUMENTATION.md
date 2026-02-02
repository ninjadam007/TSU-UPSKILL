# API Documentation - TSU UPSKILL Backend

## Base URL
```
http://localhost:8000/api
https://your-deployed-domain.com/api
```

## Authentication

All endpoints require JWT token in header (except registration and login):
```
Authorization: Bearer {access_token}
```

---

## Authentication Endpoints

### 1. Register New User
```
POST /auth/register/
Content-Type: application/json

{
  "student_id": "6820310001",
  "email": "student@tsu.ac.th",
  "username": "student",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123"
}

Response (201):
{
  "success": true,
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": 1,
    "student_id": "6820310001",
    "email": "student@tsu.ac.th",
    "first_name": "John",
    "last_name": "Doe",
    "is_email_verified": false,
    "role": "student"
  }
}
```

### 2. Verify Email
```
POST /auth/verify-email/
Content-Type: application/json

{
  "token": "verification_token_from_email"
}

Response (200):
{
  "success": true,
  "message": "Email verified successfully"
}
```

### 3. Login
```
POST /auth/login/
Content-Type: application/json

{
  "student_id": "6820310001",
  "password": "SecurePass123"
}

Response (200):
{
  "success": true,
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "student_id": "6820310001",
    "email": "student@tsu.ac.th",
    "is_email_verified": true
  }
}
```

### 4. Get Current User Profile
```
GET /auth/me/
Authorization: Bearer {access_token}

Response (200):
{
  "id": 1,
  "student_id": "6820310001",
  "username": "student",
  "email": "student@tsu.ac.th",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "081234567",
  "department": "Computer Science",
  "role": "student",
  "is_email_verified": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 5. Update Profile
```
PUT /auth/update-profile/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Jane",
  "phone_number": "0812345678",
  "department": "Engineering"
}

Response (200):
{
  "success": true,
  "message": "Profile updated successfully",
  "user": { ... }
}
```

### 6. Change Password
```
POST /auth/change-password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "OldPass123",
  "new_password": "NewPass123",
  "confirm_password": "NewPass123"
}

Response (200):
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## Location Endpoints

### 1. Get All Locations
```
GET /locations/?search=building&category=1&page=1
Authorization: Bearer {access_token}

Query Parameters:
- search: Search term (name, description, building code)
- category: Filter by category ID
- page: Page number (default: 1)
- ordering: Order by field (name, created_at)

Response (200):
{
  "count": 50,
  "next": "http://.../?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Building A",
      "category": {
        "id": 1,
        "name": "Building",
        "icon": "fa-building"
      },
      "description": "Main building",
      "latitude": 8.6328,
      "longitude": 100.4945,
      "building_code": "BLK-A",
      "floor": 3,
      "room_number": "A101",
      "opening_hours": "8:00 AM - 5:00 PM",
      "phone_number": "+66-74-XXX-XXX",
      "email": "bldg@tsu.ac.th",
      "is_bookmarked": false,
      "is_active": true
    }
  ]
}
```

### 2. Get Location Categories
```
GET /location-categories/

Response (200):
[
  {
    "id": 1,
    "name": "Building",
    "description": "University Buildings",
    "icon": "fa-building"
  },
  {
    "id": 2,
    "name": "Classroom",
    "description": "Classrooms and Lecture Halls",
    "icon": "fa-chalkboard"
  }
]
```

### 3. Bookmark Location
```
POST /locations/{location_id}/bookmark/
Authorization: Bearer {access_token}

Response (201):
{
  "success": true,
  "message": "Location bookmarked"
}
```

### 4. Remove Bookmark
```
DELETE /locations/{location_id}/unbookmark/
Authorization: Bearer {access_token}

Response (204):
(No content)
```

### 5. Get My Bookmarks
```
GET /locations/my-bookmarks/
Authorization: Bearer {access_token}

Response (200):
[
  {
    "id": 1,
    "location": { ... },
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Chat Endpoints

### 1. Create Chat Session
```
POST /chat/sessions/
Authorization: Bearer {access_token}

Response (201):
{
  "id": 1,
  "title": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "message_count": 0,
  "last_message": null,
  "messages": []
}
```

### 2. Send Message to AI
```
POST /chat/sessions/{session_id}/send-message/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "content": "Where is the library?"
}

Response (200):
{
  "success": true,
  "messages": [
    {
      "id": 1,
      "sender": "user",
      "content": "Where is the library?",
      "is_fallback_to_admin": false,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "sender": "ai",
      "content": "The library is located in Building B, 2nd floor...",
      "is_fallback_to_admin": false,
      "created_at": "2024-01-15T10:30:01Z"
    }
  ],
  "is_fallback": false
}
```

### 3. Get Chat Sessions
```
GET /chat/sessions/
Authorization: Bearer {access_token}

Response (200):
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Where is the library?",
      "message_count": 3,
      "last_message": {
        "id": 6,
        "sender": "admin",
        "content": "The library is open 24/7...",
        "created_at": "2024-01-15T11:00:00Z"
      }
    }
  ]
}
```

### 4. Get Session Messages
```
GET /chat/sessions/{session_id}/messages/
Authorization: Bearer {access_token}

Response (200):
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    { "id": 1, "sender": "user", "content": "...", "created_at": "..." },
    { "id": 2, "sender": "ai", "content": "...", "created_at": "..." }
  ]
}
```

---

## Admin Endpoints

### 1. Get Dashboard Statistics
```
GET /admin/dashboard/
Authorization: Bearer {access_token}

Response (200):
{
  "total_users": 150,
  "pending_questions": 5,
  "total_locations": 50,
  "verified_users": 145
}
```

### 2. Get All Users
```
GET /admin/dashboard/users/?search=6820310001
Authorization: Bearer {access_token}

Response (200):
[
  {
    "id": 1,
    "student_id": "6820310001",
    "email": "student@tsu.ac.th",
    "first_name": "John",
    "role": "student",
    "is_email_verified": true
  }
]
```

### 3. Get Pending Questions
```
GET /admin/dashboard/pending-questions/
Authorization: Bearer {access_token}

Response (200):
[
  {
    "id": 1,
    "message": {
      "id": 5,
      "sender": "ai",
      "content": "I don't know the answer...",
      "is_fallback_to_admin": true,
      "created_at": "2024-01-15T10:30:00Z"
    },
    "user_name": "John Doe",
    "user_email": "student@tsu.ac.th",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### 4. Respond to Pending Question
```
POST /admin/dashboard/respond-to-question/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "question_id": 1,
  "response": "The library is located at..."
}

Response (200):
{
  "success": true,
  "message": "Response sent successfully"
}
```

### 5. Get Activity Log
```
GET /admin/dashboard/activity-log/
Authorization: Bearer {access_token}

Response (200):
[
  {
    "user": "6820310001",
    "action": "Message from user",
    "timestamp": "2024-01-15T10:30:00Z",
    "content": "Where is the cafeteria?"
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": {
    "field": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Only admins can access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 429 Too Many Requests
```json
{
  "detail": "Request was throttled."
}
```

---

## Rate Limiting

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour

---

## Important Notes

1. All dates are in UTC (ISO 8601 format)
2. Email must end with @tsu.ac.th
3. Student ID must be exactly 10 digits
4. Passwords must be at least 8 characters
5. Email verification token expires in 24 hours
6. JWT access token expires in 24 hours
7. Use refresh token to get new access token
