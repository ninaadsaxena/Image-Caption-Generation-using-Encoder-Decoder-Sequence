# Image Caption Generator

This is a full-stack application that generates captions for images using an Encoder-Decoder sequence model. The backend is built with Python (Flask), and the frontend is built with ReactJS. The application is deployed using Vercel.

## Backend (Python with Flask)

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/image-caption-generator.git
    cd image-caption-generator/backend
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the necessary files**:
    - `tokenizer.pickle`
    - `word_to_index.pickle`
    - `index_to_word.pickle`
    - `model_weights.h5`

5. **Run the Flask app**:
    ```bash
    flask run
    ```

### API Endpoint

- **POST /generate_caption**:
    - **Description**: Generates a caption for an uploaded image.
    - **Request**: `multipart/form-data` with an `image` file.
    - **Response**: JSON object with the generated caption.

## Frontend (ReactJS)

### Setup

1. **Navigate to the frontend directory**:
    ```bash
    cd ../frontend
    ```

2. **Install the dependencies**:
    ```bash
    npm install
    ```

3. **Run the React app**:
    ```bash
    npm start
    ```

### Deployment with Vercel

1. **Backend Deployment**:
    - Create a new project on Vercel and connect it to your GitHub repository.
    - Add a `vercel.json` file in the backend directory:
    ```json
    {
      "version": 2,
      "builds": [
        {
          "src": "app.py",
          "use": "@vercel/python"
        }
      ],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "app.py"
        }
      ]
    }
    ```

2. **Frontend Deployment**:
    - Create a new project on Vercel and connect it to your GitHub repository.
    - Ensure your `package.json` file has the correct build script:
    ```json
    {
      "scripts": {
        "start": "react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test",
        "eject": "react-scripts eject"
      }
    }
    ```

3. **Update the API Endpoint**:
    - Update the API endpoint in the ReactJS frontend to point to the deployed backend URL.

### Project Structure

```
image-caption-generator/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── tokenizer.pickle
│   ├── word_to_index.pickle
│   ├── index_to_word.pickle
│   └── model_weights.h5
└── frontend/
    ├── public/
    ├── src/
    │   ├── App.js
    │   ├── index.js
    │   └── App.css
    ├── package.json
    └── README.md
```

## License

This project is licensed under the MIT License.
