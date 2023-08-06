from fastapi import FastAPI
from time import sleep

app = FastAPI()


@app.post("/aspekt/{jméno_aspektu}/{text_aspektu}/{fluff}")
def vytvor_karticku_aspektu(jmeno_aspektu: str, text_aspektu: str, fluff: str):
    sleep(10)
    return {"jmeno_aspektu": jmeno_aspektu, "text_aspektu": text_aspektu, "fluff": fluff}