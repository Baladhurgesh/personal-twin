from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import sys
from github_scraper_enhanced import EnhancedGitHubScraper
from elevenlabs_kb import ElevenLabsKnowledgeBase

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
OUTPUT_DIR = "project_summaries"
RESUME_DIR = "resumes"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_AGENT_ID = os.getenv('ELEVENLABS_AGENT_ID')

print(f"[Backend API] Starting server...")
print(f"[Backend API] GitHub Token: {'✓ Configured' if GITHUB_TOKEN else '✗ Missing'}")
print(f"[Backend API] OpenRouter Key: {'✓ Configured' if OPENROUTER_API_KEY else '✗ Missing'}")
print(f"[Backend API] ElevenLabs API Key: {'✓ Configured' if ELEVENLABS_API_KEY else '✗ Missing'}")
print(f"[Backend API] ElevenLabs Agent ID: {'✓ Configured' if ELEVENLABS_AGENT_ID else '✗ Missing'}")
print(f"[System Log] Backend API initialized and ready to process GitHub repositories")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'github_token_configured': bool(GITHUB_TOKEN),
        'openrouter_configured': bool(OPENROUTER_API_KEY),
        'elevenlabs_configured': bool(ELEVENLABS_API_KEY)
    })


@app.route('/api/github/analyze', methods=['POST'])
def analyze_github():
    """
    Analyze GitHub profile and generate project summaries.
    
    Request body:
    {
        "username": "github_username"
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "username": "username",
            "repositories": [...],
            "summaries": [...],
            "statistics": {...}
        }
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({
                'success': False,
                'error': 'Username is required'
            }), 400
        
        # Extract username from GitHub URL if provided
        if 'github.com' in username:
            # Handle URLs like https://github.com/username
            username = username.rstrip('/').split('/')[-1]
        
        print(f"\n[API Request] Analyzing GitHub user: {username}")
        print(f"[System Log] Starting GitHub analysis for user: {username}")
        
        # Check API keys
        if not GITHUB_TOKEN:
            print("[Warning] No GitHub token configured - may hit rate limits")
        
        if not OPENROUTER_API_KEY:
            return jsonify({
                'success': False,
                'error': 'OpenRouter API key not configured. Please add OPENROUTER_API_KEY to .env file'
            }), 500
        
        # Create scraper instance
        scraper = EnhancedGitHubScraper(
            github_token=GITHUB_TOKEN,
            openrouter_api_key=OPENROUTER_API_KEY
        )
        
        # Create user-specific output directory
        user_output_dir = os.path.join(OUTPUT_DIR, username)
        
        # Run the analysis
        print(f"[API] Starting scraping and analysis for {username}")
        result = scraper.scrape_and_analyze(username, output_dir=user_output_dir)
        
        if 'error' in result:
            print(f"[API Error] Analysis failed: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
        print(f"[API Success] Analysis complete for {username}")
        print(f"[System Log] Successfully analyzed {result['statistics']['total_repositories']} repositories")
        print(f"[System Log] Generated {result['statistics']['repositories_with_ai_summary']} AI-powered summaries")
        print(f"[System Log] Saved all data to {user_output_dir}/")
        
        # Upload to ElevenLabs Knowledge Base
        kb_documents = []
        if ELEVENLABS_API_KEY:
            try:
                print(f"[API] Uploading project summaries to ElevenLabs Knowledge Base...")
                kb = ElevenLabsKnowledgeBase(
                    api_key=ELEVENLABS_API_KEY,
                    agent_id=ELEVENLABS_AGENT_ID
                )
                
                # Upload all project summaries
                kb_documents = kb.upload_all_project_summaries(user_output_dir, username)
                
                # Optionally update agent if agent_id is configured
                if ELEVENLABS_AGENT_ID and kb_documents:
                    kb.update_agent_knowledge_base(kb_documents)
                
                print(f"[API] ✓ Uploaded {len(kb_documents)} summaries to ElevenLabs KB")
            except Exception as e:
                print(f"[API Warning] Failed to upload to ElevenLabs KB: {e}")
        else:
            print(f"[API] Skipping ElevenLabs upload (API key not configured)")
        
        # Return success response
        response_data = {
            'success': True,
            'message': 'GitHub analysis completed successfully',
            'data': {
                'username': username,
                'repositories': result['statistics'].get('total_repositories', 0),
                'topProjects': result['summaries'][:10] if 'summaries' in result else [],
                'languages': result['statistics'].get('languages_used', []),
                'contributions': result['statistics'].get('total_stars', 0),
                'statistics': result['statistics'],
                'output_directory': user_output_dir,
                'summary_files': len(result.get('summaries', [])),
                'kb_uploaded': len(kb_documents),
                'kb_documents': kb_documents,
            }
        }
        
        print(f"[API] Sending response: {json.dumps({'success': True, 'repositories': response_data['data']['repositories']})}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"[API Error] Exception occurred: {str(e)}")
        print(f"[API Error] Error type: {type(e).__name__}")
        import traceback
        error_trace = traceback.format_exc()
        print(f"[API Error] Full traceback:\n{error_trace}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'message': f'Failed to analyze GitHub profile: {str(e)}'
        }), 500


@app.route('/api/github/summaries/<username>', methods=['GET'])
def get_summaries(username):
    """
    Get all project summaries for a user.
    
    Returns:
    {
        "success": true,
        "data": {
            "username": "username",
            "summaries": [...],
            "statistics": {...}
        }
    }
    """
    try:
        user_output_dir = os.path.join(OUTPUT_DIR, username)
        
        # Check if analysis exists
        if not os.path.exists(user_output_dir):
            return jsonify({
                'success': False,
                'error': f'No analysis found for user: {username}'
            }), 404
        
        # Load summaries JSON
        summaries_file = os.path.join(user_output_dir, f"{username}_all_projects_summary.json")
        stats_file = os.path.join(user_output_dir, f"{username}_statistics.json")
        
        summaries = []
        statistics = {}
        
        if os.path.exists(summaries_file):
            with open(summaries_file, 'r', encoding='utf-8') as f:
                summaries = json.load(f)
        
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                statistics = json.load(f)
        
        print(f"[API] Retrieved summaries for {username}: {len(summaries)} projects")
        print(f"[System Log] Serving {len(summaries)} project summaries for {username}")
        
        return jsonify({
            'success': True,
            'data': {
                'username': username,
                'summaries': summaries,
                'statistics': statistics
            }
        }), 200
        
    except Exception as e:
        print(f"[API Error] Failed to retrieve summaries: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/github/summary/<username>/<project_name>', methods=['GET'])
def get_project_summary(username, project_name):
    """
    Get individual project summary text file.
    
    Returns the .txt file content for a specific project.
    """
    try:
        user_output_dir = os.path.join(OUTPUT_DIR, username)
        summary_file = os.path.join(user_output_dir, f"{project_name}.txt")
        
        if not os.path.exists(summary_file):
            return jsonify({
                'success': False,
                'error': f'Summary not found for project: {project_name}'
            }), 404
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"[API] Serving summary file for {username}/{project_name}")
        
        return jsonify({
            'success': True,
            'data': {
                'username': username,
                'project': project_name,
                'content': content
            }
        }), 200
        
    except Exception as e:
        print(f"[API Error] Failed to retrieve project summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/resume/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze and upload resume to ElevenLabs knowledge base.
    """
    try:
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No resume file provided'
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Get username from form data if provided
        username = request.form.get('username', 'user')
        
        print(f"[API] Resume uploaded: {file.filename}")
        print(f"[System Log] Resume analysis requested for file: {file.filename}")
        
        # Validate file type (accept PDF, DOCX, TXT)
        allowed_extensions = {'.pdf', '.docx', '.txt', '.doc'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
            }), 400
        
        # Create resume directory if it doesn't exist
        os.makedirs(RESUME_DIR, exist_ok=True)
        
        # Create user-specific directory
        user_resume_dir = os.path.join(RESUME_DIR, username)
        os.makedirs(user_resume_dir, exist_ok=True)
        
        # Save file with timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{username}_resume_{timestamp}{file_ext}"
        file_path = os.path.join(user_resume_dir, safe_filename)
        
        # Save the file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"[API] Resume saved to: {file_path}")
        print(f"[System Log] Saved resume file: {safe_filename} ({file_size} bytes)")
        
        # Upload to ElevenLabs Knowledge Base
        kb_document = None
        if ELEVENLABS_API_KEY:
            try:
                print(f"[API] Uploading resume to ElevenLabs Knowledge Base...")
                kb = ElevenLabsKnowledgeBase(
                    api_key=ELEVENLABS_API_KEY,
                    agent_id=ELEVENLABS_AGENT_ID
                )
                
                # Upload resume file
                kb_document = kb.upload_resume(file_path, username)
                
                # Optionally update agent if agent_id is configured
                if ELEVENLABS_AGENT_ID and kb_document:
                    kb.update_agent_knowledge_base([kb_document])
                
                print(f"[API] ✓ Resume uploaded to ElevenLabs KB")
                print(f"[System Log] Resume added to ElevenLabs knowledge base")
            except Exception as e:
                print(f"[API Warning] Failed to upload resume to ElevenLabs KB: {e}")
        else:
            print(f"[API] Skipping ElevenLabs upload (API key not configured)")
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and processed successfully',
            'data': {
                'filename': safe_filename,
                'original_filename': file.filename,
                'size': file_size,
                'path': file_path,
                'username': username,
                'uploaded_at': datetime.now().isoformat(),
                'kb_uploaded': kb_document is not None,
                'kb_document': kb_document
            }
        }), 200
        
    except Exception as e:
        print(f"[API Error] Resume analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/twin/create', methods=['POST'])
def create_twin():
    """
    Create digital twin from resume and GitHub data.
    """
    try:
        print(f"[API] Digital twin creation requested")
        print(f"[System Log] Creating digital twin from resume and GitHub data")
        
        # TODO: Implement twin creation logic
        
        return jsonify({
            'success': True,
            'message': 'Digital twin creation initiated',
            'data': {
                'id': 'twin_' + datetime.now().strftime('%Y%m%d%H%M%S'),
                'created_at': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        print(f"[API Error] Twin creation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/elevenlabs/config', methods=['GET'])
def get_elevenlabs_config():
    """
    Get ElevenLabs agent configuration for the widget.
    
    Returns:
    {
        "success": true,
        "data": {
            "agentId": "agent_id",
            "configured": true
        }
    }
    """
    try:
        if ELEVENLABS_AGENT_ID:
            return jsonify({
                'success': True,
                'data': {
                    'agentId': ELEVENLABS_AGENT_ID,
                    'configured': True
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'ElevenLabs agent not configured',
                'data': {
                    'configured': False
                }
            }), 200
        
    except Exception as e:
        print(f"[API Error] Failed to get ElevenLabs config: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Create output directories if they don't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RESUME_DIR, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"PERSONAL DIGITAL TWIN - BACKEND API")
    print(f"{'='*80}")
    print(f"Starting Flask server...")
    print(f"API will be available at: http://localhost:8000")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Resume directory: {RESUME_DIR}")
    print(f"{'='*80}\n")
    print(f"[System Log] Backend server starting on port 8000")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )

