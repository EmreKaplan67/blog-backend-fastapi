import uvicorn
import os

def main() -> None:
    uvicorn.run("blog.app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
    
if __name__ == "__main__":
    main()