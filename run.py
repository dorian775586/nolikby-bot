    import asyncio
    import os
    from fastapi import FastAPI
    import uvicorn
    from tgbot import dp, bot, main

    web_app = FastAPI()

    @web_app.get("/")
    async def read_root():
        return {"message": "Telegram bot is running in the background"}

    # Объединенный запуск: бот и веб-сервер
    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        
        # Запуск веб-сервера Uvicorn
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(web_app, host="0.0.0.0", port=port)
    
