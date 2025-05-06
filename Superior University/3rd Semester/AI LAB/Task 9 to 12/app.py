from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained SVR model
with open('svr_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the form
        features = [float(request.form[str(i)]) for i in range(11)]  # Expecting 11 inputs
        final_input = np.array(features).reshape(1, -1)
        
        # Validate input size
        if final_input.shape[1] != 11:
            raise ValueError("Invalid number of inputs. Please provide all required features.")
        
        # Make prediction
        prediction = model.predict(final_input)
        return render_template('index.html', prediction_text=f"Predicted Wine Quality: {prediction[0]:.2f}")
    except ValueError as ve:
        return render_template('index.html', prediction_text=f"Error: {str(ve)}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)