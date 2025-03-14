from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById, WritePatient
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS (permitiendo solo tu dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hl7-patient-write-laura-garcia-8518.onrender.com"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Endpoint para verificar si la API está funcionando
@app.get("/status")
async def check_status():
    return {"message": "API is running on hl7-patient-write-laura-garcia-8518.onrender.com"}

# Endpoint para obtener un paciente por su ID
@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    print(f"🔍 Buscando paciente con ID: {patient_id}")
    status, patient = GetPatientById(patient_id)
    
    if status == 'success':
        return patient
    elif status == 'notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

# Endpoint para agregar un nuevo paciente
@app.post("/patient", response_model=dict)
async def add_patient(request: Request):
    new_patient_dict = dict(await request.json())
    print(f"📝 Recibiendo nuevo paciente: {new_patient_dict}")
    
    status, patient_id = WritePatient(new_patient_dict)
    
    if status == 'success':
        return {"_id": patient_id}  # Devuelve el ID del paciente creado
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")

# Ejecutar el servidor con uvicorn
if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8000))  # Usa el puerto de Render si está definido
    uvicorn.run(app, host="0.0.0.0", port=port)
