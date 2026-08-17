from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from app.database import Base, engine
from app.routers import auth, students

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Auth",
        "description": "User registration, login (OAuth2 + JWT), and identity check.",
    },
    {
        "name": "Students",
        "description": "CRUD operations on student records, restricted by role (ADMIN / STUDENT).",
    },
]

app = FastAPI(
    title="Student Management API",
    description="A REST API for managing students with JWT authentication and role-based access control.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url=None,
)

app.include_router(auth.router)
app.include_router(students.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Student Management API is running.", "docs": "/docs"}


CUSTOM_DOCS_CSS = """
<style>
.swagger-ui .info {
    background: linear-gradient(135deg, #1f2937 0%, #4338ca 100%);
    padding: 32px 24px;
    border-radius: 12px;
    margin: 20px 0;
}
.swagger-ui .info .title {
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.swagger-ui .info .title small {
    background: rgba(255,255,255,0.15);
    border-radius: 6px;
}
.swagger-ui .info .title small pre {
    color: #ffffff;
}
.swagger-ui .info p {
    color: #e5e7eb;
}
.swagger-ui .info a {
    color: #93c5fd;
}
</style>
"""


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Docs",
    ).body.decode()
    html = html.replace("</head>", CUSTOM_DOCS_CSS + "</head>")
    return HTMLResponse(html)