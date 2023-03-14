from fastapi import FastAPI
from routers.payment_system import payment_router


def append_routers(app: FastAPI) -> None:
    app.include_router(payment_router)


def create_app() -> FastAPI:
    app = FastAPI()
    append_routers(app)
    return app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:create_app',
        port=5000,
        reload=True,
        log_level="info"
    )