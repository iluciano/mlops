from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Definir a classe do modelo de entrada
class InputData(BaseModel):
    loan_amount: float
    rate_of_interest: float
    Interest_rate_spread: float
    Upfront_charges: float
    income: float

# Carregar o modelo salvo
with open("models/modelo.pkl", "rb") as file:
    model = pickle.load(file)

# Criar a instância do FastAPI
app = FastAPI()

# Definir uma rota para receber a entrada e fazer a previsão
@app.post("/predict")
def predict(input_data: InputData):
    # Converter os dados de entrada em um array numpy
    input_array = [[input_data.loan_amount, input_data.rate_of_interest, input_data.Interest_rate_spread, 
                    input_data.Upfront_charges, input_data.income]]

    # Fazer a previsão usando o modelo carregado
    prediction = model.predict(input_array)
    probability = model.predict_proba(input_array).max() * 100

    # Retornar a previsão como resultado
    #return {"prediction": prediction.tolist()}
    if prediction == 1:
        return {
            "prediction": "Este cliente provavelmente irá atrasar o pagamento do empréstimo.",
            "probability": f"Modelo preditivo com {probability:.4f}% de probabilidade"
        }
    else:
        return {
            "prediction": "Este cliente tem baixa propensão de atrasar o pagamento do empréstimo.",
            "probability": f"Modelo preditivo com {probability:.4f}% de probabilidade"
        }

# Iniciar o servidor FastAPI usando o uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)