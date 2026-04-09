"""
Flask ML/AI Portfolio Application
=================================
A dynamic portfolio website for ML/AI engineers with auto-generated
project pages and prediction capabilities.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import importlib.util
import sys
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / 'projects'
PROFILE_CONFIG_PATH = BASE_DIR / 'profile_config.json'


def load_profile_config():
    """Load profile configuration from JSON file."""
    if PROFILE_CONFIG_PATH.exists():
        with open(PROFILE_CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}


def get_all_projects():
    """
    Dynamically load all projects from the projects directory.
    Each project folder must contain a config.json file.
    """
    projects = []
    
    if not PROJECTS_DIR.exists():
        PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        return projects
    
    for project_folder in sorted(PROJECTS_DIR.iterdir()):
        if project_folder.is_dir():
            config_path = project_folder / 'config.json'
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    config['id'] = project_folder.name
                    config['folder_path'] = str(project_folder)
                    
                    # Check for thumbnail
                    thumbnail_path = project_folder / 'thumbnail.jpg'
                    if thumbnail_path.exists():
                        config['thumbnail_url'] = f'/project-assets/{project_folder.name}/thumbnail.jpg'
                    else:
                        config['thumbnail_url'] = '/static/images/default-project.jpg'
                    
                    projects.append(config)
                except json.JSONDecodeError:
                    print(f"Error loading config for {project_folder.name}")
                    continue
    
    return projects


def get_project_by_id(project_id):
    """Get a specific project by its folder name."""
    project_folder = PROJECTS_DIR / project_id
    config_path = project_folder / 'config.json'
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        config['id'] = project_id
        config['folder_path'] = str(project_folder)
        
        # Check for thumbnail
        thumbnail_path = project_folder / 'thumbnail.jpg'
        if thumbnail_path.exists():
            config['thumbnail_url'] = f'/project-assets/{project_id}/thumbnail.jpg'
        else:
            config['thumbnail_url'] = '/static/images/default-project.jpg'
        
        return config
    return None


def run_prediction(project_id, input_data):
    """
    Run prediction for a specific project.
    Dynamically loads and executes the project's predict.py file.
    """
    project_folder = PROJECTS_DIR / project_id
    predict_path = project_folder / 'predict.py'
    
    if not predict_path.exists():
        return {'error': 'Prediction module not found'}
    
    try:
        # Dynamically import the predict module
        spec = importlib.util.spec_from_file_location("predict", predict_path)
        predict_module = importlib.util.module_from_spec(spec)
        
        # Add project folder to path for model loading
        original_cwd = os.getcwd()
        os.chdir(project_folder)
        sys.path.insert(0, str(project_folder))
        
        try:
            spec.loader.exec_module(predict_module)
            result = predict_module.predict(input_data)
        finally:
            os.chdir(original_cwd)
            sys.path.remove(str(project_folder))
        
        return result
    except Exception as e:
        return {'error': str(e)}


# ============== ROUTES ==============

@app.route('/')
def index():
    """Homepage with profile info and project preview."""
    profile = load_profile_config()
    projects = get_all_projects()
    return render_template('index.html', profile=profile, projects=projects)


@app.route('/projects')
def projects_list():
    """All projects listing page."""
    profile = load_profile_config()
    projects = get_all_projects()
    return render_template('projects.html', profile=profile, projects=projects)


@app.route('/project/<project_id>')
def project_detail(project_id):
    """Individual project page with dynamic input form."""
    profile = load_profile_config()
    project = get_project_by_id(project_id)
    
    if project is None:
        return render_template('404.html', profile=profile), 404
    
    return render_template('project_detail.html', profile=profile, project=project)


@app.route('/project-assets/<project_id>/<filename>')
def serve_project_asset(project_id, filename):
    """Serve static assets from project folders (thumbnails, etc.)."""
    project_folder = PROJECTS_DIR / project_id
    return send_from_directory(project_folder, filename)


# ============== API ENDPOINTS ==============

@app.route('/api/projects', methods=['GET'])
def api_projects():
    """API endpoint to get all projects as JSON."""
    projects = get_all_projects()
    return jsonify(projects)


@app.route('/api/predict/<project_id>', methods=['POST'])
def api_predict(project_id):
    """
    API endpoint for running predictions.
    
    Accepts form data or JSON. For image uploads, use multipart/form-data.
    Returns prediction result with optional chart data.
    """
    project = get_project_by_id(project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    # Collect input data
    input_data = {}
    
    # Handle both JSON and form data
    if request.is_json:
        input_data = request.get_json()
    else:
        # Handle form data including file uploads
        for field in project.get('inputs', []):
            field_name = field['name']
            field_type = field['type']
            
            if field_type == 'image':
                # Handle image upload
                if field_name in request.files:
                    file = request.files[field_name]
                    if file.filename:
                        # Save temporarily and pass path
                        import tempfile
                        temp_dir = tempfile.mkdtemp()
                        temp_path = os.path.join(temp_dir, file.filename)
                        file.save(temp_path)
                        input_data[field_name] = temp_path
            elif field_type == 'checkbox':
                input_data[field_name] = field_name in request.form
            elif field_type == 'number' or field_type == 'range':
                value = request.form.get(field_name)
                if value:
                    try:
                        input_data[field_name] = float(value)
                    except ValueError:
                        input_data[field_name] = 0
            else:
                input_data[field_name] = request.form.get(field_name, '')
    
    # Run prediction
    result = run_prediction(project_id, input_data)
    
    return jsonify(result)


# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def page_not_found(e):
    profile = load_profile_config()
    return render_template('404.html', profile=profile), 404


@app.errorhandler(500)
def internal_error(e):
    profile = load_profile_config()
    return render_template('500.html', profile=profile), 500


# ============== MAIN ==============

if __name__ == '__main__':
    # Ensure directories exist
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / 'static' / 'images').mkdir(parents=True, exist_ok=True)
    
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=3000)
