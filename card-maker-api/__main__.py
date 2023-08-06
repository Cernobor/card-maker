import uvicorn

def run_server(port:int, log_level:str):

    uvicorn.run("card-maker-api.api:app", port=port, reload=True, log_level=log_level, host="0.0.0.0")


def run():
    run_server(port=5000, log_level="info")
    return 0

if __name__ == "__main__":
    run()