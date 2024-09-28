from fastapi import FastAPI, File, UploadFile
import pandas as pd
import uvicorn
import pickle
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter

app = FastAPI()
router = APIRouter()

# Allow CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pickled model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

@app.post("/predict")
async def predict_chiller_frequency(csv_file: UploadFile = File(...)):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file.file)

        # Ensure the DataFrame has the correct columns for your model
        if not all(col in df.columns for col in model.feature_names_in_):
            return JSONResponse(status_code=400, content={"message": "CSV file must contain correct columns"})

        # Make predictions using the model
        predictions = model.predict(df)

        # Add "chiller_frequency" column to the DataFrame
        df["chiller_frequency"] = predictions.tolist()

        # Create a temporary in-memory file object
        in_memory_file = BytesIO()

        # Save the modified DataFrame back to CSV format
        df.to_csv(in_memory_file, index=False)

        # Reset the in-memory file stream to the beginning
        in_memory_file.seek(0)

        # Return the updated CSV data as a download
        return StreamingResponse(
            content=in_memory_file,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=updated_{csv_file.filename}"
            }
        )

    except pd.errors.ParserError:
        # Handle CSV parsing errors
        return JSONResponse(status_code=400, content={"message": "Invalid CSV file format."})
    
    except Exception as e:
        # Log the exception and return a JSON response with error details
        print(f"Error occurred: {e}")
        return JSONResponse(status_code=500, content={"message": f"An error occurred during file processing: {str(e)}"})
    
@app.get("/dashboard/")
async def get_dashboard_data():
    # Replace this with logic to access the processed data from your model's predictions
    # (e.g., calculate average, highest, and lowest efficiency from the DataFrame)
    average_efficiency = "55%"
    highest_efficiency = "62%"
    lowest_efficiency = "48%"
    return {
        "average_efficiency": average_efficiency,
        "highest_efficiency": highest_efficiency,
        "lowest_efficiency": lowest_efficiency,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
