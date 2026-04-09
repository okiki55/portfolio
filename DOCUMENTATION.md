# ML/AI Portfolio - Complete Documentation

A dynamic Flask-based portfolio website for Machine Learning and AI Engineers. This portfolio automatically displays your ML projects, generates input forms from configuration files, and handles predictions through your Python models.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Configuration Files](#configuration-files)
4. [Adding Your Profile Info](#adding-your-profile-info)
5. [Adding ML/AI Projects](#adding-mlai-projects)
6. [Input Types Reference](#input-types-reference)
7. [Creating predict.py](#creating-predictpy)
8. [Output & Charts](#output--charts)
9. [Customization](#cushgtomization)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

Visit `http://localhost:5000`

---

## Project Structure

```
/your-portfolio/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── profile_config.json         # YOUR PROFILE INFO (edit this!)
├── DOCUMENTATION.md            # This file
│
├── static/
│   ├── css/
│   │   └── style.css           # Dark theme styles
│   ├── js/
│   │   └── main.js             # Form handling, animations
│   └── images/
│       ├── profile.jpg         # YOUR PHOTO (replace this!)
│       └── default-project.jpg # Default project thumbnail
│
├── templates/
│   ├── base.html               # Base layout
│   ├── index.html              # Homepage
│   ├── projects.html           # Projects listing
│   ├── project_detail.html     # Individual project page
│   ├── 404.html                # Error page
│   └── 500.html                # Error page
│
└── projects/                   # YOUR ML PROJECTS GO HERE
    ├── house_price_predictor/  # Example ML project
    │   ├── config.json         # Project configuration
    │   ├── predict.py          # Prediction logic
    │   ├── model.pkl           # Your trained model (optional)
    │   └── thumbnail.jpg       # Project image (optional)
    │
    ├── image_classifier/       # Example DL project
    │   ├── config.json
    │   ├── predict.py
    │   └── model.h5            # Keras/TF model (optional)
    │
    └── sentiment_analyzer/     # Example NLP project
        ├── config.json
        └── predict.py
```

---

## Configuration Files

### Files You Need to Edit:

| File | Purpose | Priority |
|------|---------|----------|
| `profile_config.json` | Your name, bio, skills, contact | **Required** |
| `static/images/profile.jpg` | Your profile picture | **Required** |
| `projects/*/config.json` | Define each project's inputs | **Required** |
| `projects/*/predict.py` | Your ML prediction logic | **Required** |

---

## Adding Your Profile Info

Edit `profile_config.json`:

```json
{
  "name": "Your Full Name",
  "title": "ML/AI Engineer",
  "tagline": "Your catchy one-liner about what you do",
  "bio": [
    "First paragraph about your background...",
    "Second paragraph about your expertise...",
    "Third paragraph about your interests..."
  ],
  "email": "your.email@example.com",
  "location": "City, Country",
  "social": {
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "twitter": "https://twitter.com/yourhandle",
    "kaggle": "https://kaggle.com/yourusername"
  },
  "skills": {
    "languages": [
      {"name": "Python", "icon": "python"},
      {"name": "SQL", "icon": "database"}
    ],
    "ml_ai": [
      {"name": "TensorFlow", "icon": "brain"},
      {"name": "PyTorch", "icon": "fire"}
    ],
    "tools": [
      {"name": "Docker", "icon": "docker"},
      {"name": "Git", "icon": "code-branch"}
    ],
    "cloud": [
      {"name": "AWS", "icon": "cloud"}
    ]
  },
  "achievements": [
    "Achievement 1",
    "Achievement 2"
  ],
  "resume_url": "https://link-to-your-resume.pdf"
}
```

### Icon Reference

Icons use Font Awesome. Common icons:
- Languages: `python`, `js`, `database`, `chart-line`
- ML/AI: `brain`, `fire`, `cogs`, `microchip`, `eye`, `tree`
- Tools: `docker`, `code-branch`, `book`, `chart-bar`, `bolt`
- Cloud: `cloud`, `server`, `aws`

---

## Adding ML/AI Projects

### Step 1: Create a Project Folder

Create a new folder inside `projects/`:

```
projects/
└── my_new_project/      # Use underscores, no spaces
    ├── config.json      # Required
    ├── predict.py       # Required
    ├── model.pkl        # Your trained model
    └── thumbnail.jpg    # Optional project image
```

### Step 2: Create config.json

This file defines your project's metadata and input form:

```json
{
  "name": "My ML Project",
  "description": "What does this project do?",
  "type": "ml",
  "tags": ["Regression", "Scikit-learn"],
  "inputs": [
    {
      "name": "feature_1",
      "label": "Feature 1 Label",
      "type": "number",
      "required": true
    }
  ],
  "output": {
    "type": "regression",
    "label": "Prediction",
    "show_chart": true
  }
}
```

### Step 3: Create predict.py

This file contains your prediction logic:

```python
def predict(data):
    """
    Args:
        data: dict with input values
    Returns:
        dict with 'result' key
    """
    # Your ML logic here
    return {'result': prediction_value}
```

### Step 4: Add Your Model (Optional)

Place your trained model file in the project folder:
- `model.pkl` - Scikit-learn models
- `model.joblib` - Scikit-learn (recommended)
- `model.h5` - Keras/TensorFlow models
- `model.pth` - PyTorch models

---

## Input Types Reference

### Number Input

```json
{
  "name": "age",
  "label": "Age",
  "type": "number",
  "min": 0,
  "max": 120,
  "step": 1,
  "default": 25,
  "placeholder": "Enter age",
  "hint": "Patient's age in years",
  "required": true
}
```

### Text Input

```json
{
  "name": "name",
  "label": "Full Name",
  "type": "text",
  "placeholder": "Enter your name",
  "maxlength": 100,
  "required": true
}
```

### Textarea (Long Text)

```json
{
  "name": "description",
  "label": "Description",
  "type": "textarea",
  "rows": 5,
  "placeholder": "Enter detailed description...",
  "required": false
}
```

### Select Dropdown

```json
{
  "name": "category",
  "label": "Category",
  "type": "select",
  "options": ["Option A", "Option B", "Option C"],
  "default": "Option A",
  "placeholder": "Select a category",
  "required": true
}
```

Or with separate values and labels:

```json
{
  "name": "category",
  "label": "Category",
  "type": "select",
  "options": [
    {"value": "a", "label": "Option A"},
    {"value": "b", "label": "Option B"}
  ],
  "default": "a"
}
```

### Radio Buttons

```json
{
  "name": "gender",
  "label": "Gender",
  "type": "radio",
  "options": [
    {"value": "male", "label": "Male"},
    {"value": "female", "label": "Female"},
    {"value": "other", "label": "Other"}
  ],
  "default": "male",
  "required": true
}
```

### Checkbox (Boolean)

```json
{
  "name": "has_feature",
  "label": "Feature Enabled",
  "type": "checkbox",
  "checkbox_label": "Enable this feature",
  "default": false
}
```

### Range Slider

```json
{
  "name": "confidence",
  "label": "Confidence Level",
  "type": "range",
  "min": 0,
  "max": 100,
  "step": 5,
  "default": 50,
  "hint": "Slide to select confidence level"
}
```

### Image Upload (for Deep Learning)

```json
{
  "name": "image",
  "label": "Upload Image",
  "type": "image",
  "accepted_formats": ["jpg", "jpeg", "png", "webp"],
  "required": true
}
```

### Date Input

```json
{
  "name": "date",
  "label": "Select Date",
  "type": "date",
  "required": false
}
```

---

## Creating predict.py

### Basic Template

```python
import pickle
import os

def load_model():
    """Load your trained model."""
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def predict(data):
    """
    Make a prediction.
    
    Args:
        data (dict): Input values from the form.
                     Keys match 'name' fields in config.json
    
    Returns:
        dict: Must contain 'result'. Optional: 'confidence', 
              'details', 'chart_data', 'unit', 'prefix'
    """
    model = load_model()
    
    # Extract and process inputs
    feature_1 = float(data.get('feature_1', 0))
    feature_2 = data.get('feature_2', 'default')
    
    # Prepare features for model
    features = [feature_1, encode(feature_2)]
    
    # Make prediction
    result = model.predict([features])[0]
    
    return {
        'result': result,
        'confidence': 0.95,
        'prefix': '$',  # Shows before result
        'unit': ' USD', # Shows after result
        'details': {
            'metric_1': 'value',
            'metric_2': 'value'
        }
    }
```

### For Classification

```python
def predict(data):
    model = load_model()
    
    # ... process inputs ...
    
    probabilities = model.predict_proba([features])[0]
    classes = ['Class A', 'Class B', 'Class C']
    
    predicted_idx = probabilities.argmax()
    predicted_class = classes[predicted_idx]
    confidence = float(probabilities[predicted_idx])
    
    return {
        'result': predicted_class,
        'confidence': confidence,
        'details': {
            'top_prediction': predicted_class,
            'probability': f"{confidence:.1%}"
        },
        'chart_data': {
            'type': 'doughnut',
            'labels': classes,
            'values': [round(p * 100, 1) for p in probabilities]
        }
    }
```

### For Image Classification

```python
import os
from PIL import Image
import numpy as np

def predict(data):
    image_path = data.get('image')
    
    if not image_path or not os.path.exists(image_path):
        return {'error': 'No image provided'}
    
    # Load and preprocess image
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Load model and predict
    model = load_model()
    predictions = model.predict(img_array)[0]
    
    # Clean up temp file
    os.remove(image_path)
    
    classes = ['Cat', 'Dog', 'Bird']
    predicted_class = classes[np.argmax(predictions)]
    
    return {
        'result': predicted_class,
        'confidence': float(max(predictions)),
        'chart_data': {
            'type': 'bar',
            'labels': classes,
            'values': [round(p * 100, 1) for p in predictions]
        }
    }
```

---

## Output & Charts

### Return Format

```python
return {
    'result': value,           # Required - main prediction
    'confidence': 0.95,        # Optional - 0 to 1
    'prefix': '$',             # Optional - shows before result
    'unit': ' kg',             # Optional - shows after result
    'details': {               # Optional - additional metrics
        'key': 'value'
    },
    'chart_data': {            # Optional - for visualization
        'type': 'bar',
        'labels': [...],
        'values': [...]
    }
}
```

### Chart Types

**Bar Chart:**
```python
'chart_data': {
    'type': 'bar',
    'label': 'Feature Importance',
    'labels': ['Feature 1', 'Feature 2', 'Feature 3'],
    'values': [0.45, 0.30, 0.25]
}
```

**Doughnut/Pie Chart:**
```python
'chart_data': {
    'type': 'doughnut',  # or 'pie'
    'label': 'Distribution',
    'labels': ['Class A', 'Class B', 'Class C'],
    'values': [45, 35, 20]
}
```

**Line Chart:**
```python
'chart_data': {
    'type': 'line',
    'label': 'Trend',
    'labels': ['Jan', 'Feb', 'Mar', 'Apr'],
    'values': [10, 25, 15, 30]
}
```

---

## Customization

### Change Colors

Edit `static/css/style.css`, find the `:root` section:

```css
:root {
    --bg-primary: #0a0a0f;          /* Main background */
    --accent-primary: #00d4ff;       /* Cyan accent */
    --accent-secondary: #7c3aed;     /* Purple accent */
    /* ... */
}
```

### Add Project Thumbnail

Add a `thumbnail.jpg` (400x200 recommended) to your project folder:

```
projects/my_project/
├── config.json
├── predict.py
├── model.pkl
└── thumbnail.jpg    # Your project image
```

### Additional Project Info

Add optional fields to `config.json`:

```json
{
  "name": "My Project",
  "info": "<p>HTML description of your model...</p>",
  "github_url": "https://github.com/you/repo",
  "notebook_url": "https://kaggle.com/your-notebook"
}
```

---

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t ml-portfolio .
docker run -p 5000:5000 ml-portfolio
```

### Environment Variables

Set `SECRET_KEY` in production:

```bash
export SECRET_KEY="your-secure-random-key"
```

---

## Troubleshooting

### "No projects found"

- Check that your project folder is inside `projects/`
- Ensure `config.json` exists and is valid JSON
- Check file permissions

### "Prediction module not found"

- Ensure `predict.py` exists in your project folder
- Check that it has a `predict(data)` function

### "Model not loading"

- Check the model file path in `load_model()`
- Ensure model file exists in the project folder
- Verify pickle/joblib compatibility with your Python version

### Form not showing

- Validate your `config.json` syntax (use a JSON validator)
- Check that `inputs` is an array
- Ensure all required fields (`name`, `type`) are present

### Chart not displaying

- Make sure `output.show_chart` is `true` in config.json
- Verify `chart_data` is returned from `predict()`
- Check browser console for JavaScript errors

---

## Summary: What Goes Where

| What You Want | Where to Put It |
|---------------|-----------------|
| Your name, bio, skills | `profile_config.json` |
| Your profile photo | `static/images/profile.jpg` |
| New ML project | `projects/project_name/config.json` + `predict.py` |
| Project thumbnail | `projects/project_name/thumbnail.jpg` |
| Trained model | `projects/project_name/model.pkl` |
| Custom styles | `static/css/style.css` |

---

## Need Help?

1. Check the example projects in `projects/` folder
2. Review this documentation
3. Check browser console for JavaScript errors
4. Check terminal for Python errors

Good luck with your ML/AI portfolio!
