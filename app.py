from fastapi import FastAPI
import pickle
from pydantic import BaseModel

        
# Definir a classe do modelo de entrada
class InputData(BaseModel):
    loan_amount: float
    rate_of_interest: float
    Upfront_charges: float
    property_value: float
    term: float
    income: float
    Credit_Score: int
    model: int

# Carregar o modelo salvo
with open("models/modelo.pkl", "rb") as file:
    model = pickle.load(file)

with open("models/modelo2.pkl", "rb") as file:
    model2 = pickle.load(file)

# Criar a instância do FastAPI
app = FastAPI()

# Definir uma rota para receber a entrada e fazer a previsão
@app.post("/predict")
def predict(input_data: InputData):
    # Converter os dados de entrada em um array numpy
    input_array = [[input_data.loan_amount, input_data.rate_of_interest, input_data.property_value, 
                    input_data.Upfront_charges, input_data.income, input_data.term, input_data.Credit_Score]]

    # Fazer a previsão usando o modelo carregado
    if input_data.model == 1:
        prediction = model.predict(input_array)
        probability = model.predict_proba(input_array).max() * 100
    # Retornar a previsão como resultado
    #return {"prediction": prediction.tolist()}
        if prediction == 0:
            return {
                "prediction": "Este cliente provavelmente irá atrasar o pagamento do empréstimo.",
                "probability": f"Modelo preditivo com {probability:.4f}% de probabilidade"
            }
        else:
            return {
                "prediction": "Este cliente tem baixa propensão de atrasar o pagamento do empréstimo.",
                "probability": f"Modelo preditivo com {probability:.4f}% de probabilidade"
            }
    else:
        prediction = model2.predict(input_array)
        return {"prediction": prediction.tolist()}


# Iniciar o servidor FastAPI usando o uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)