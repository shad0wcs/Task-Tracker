from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def test():
    a = {'message': 'Task Tracker API'}
    return a