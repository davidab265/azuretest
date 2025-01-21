#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from string import Template

def substitute_env_vars(content: str) -> str:
    """
    Substitute environment variables in the content using custom logic.
    """
    template = Template(content)
    # Get all environment variables as a dictionary
    env_vars = dict(os.environ)
    
    # Add any missing variables with empty strings to prevent KeyError
    required_vars = [
        'GETAPP_RELEASE_TAG', 'API_TAG', 'DELIVERY_TAG', 'DEPLOY_TAG',
        'DISCOVERY_TAG', 'OFFERING_TAG', 'PROJECT_MANAGEMENT_TAG',
        'UPLOAD_TAG', 'GETMAP_TAG', 'DASHBOARD_TAG', 'DOCS_TAG'
    ]
    
    for var in required_vars:
        if var not in env_vars:
            env_vars[var] = ''
    
    try:
        return template.safe_substitute(env_vars)
    except Exception as e:
        print(f"Error during substitution: {str(e)}", file=sys.stderr)
        return content

def process_template(template_path: Path, output_path: Path) -> None:
    """
    Process a template file by replacing environment variables and save to output path.
    Args:
        template_path: Path to the template file
        output_path: Path where the processed file should be saved
    """
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read template and process environment variables
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Use our custom substitution function
        result = substitute_env_vars(template)
        
        # Write processed content to output file
        with open(output_path, 'w') as f:
            f.write(result)
            
        print(f"✓ Processed {template_path} -> {output_path}")
        
    except Exception as e:
        print(f"Error processing {template_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    # Define template mappings (template path -> output path)
    templates = {
        Path("stuff/getapp-release-info-template.txt"): Path("stuff/getapp-release-info.txt"),
        Path("stuff/images-list-template.txt"): Path("getapp-images-list.txt"),
        Path("stuff/docker-compose-template.txt"): Path("docker-compose/docker-compose.yaml")
    }
    
    # Process each template
    workspace = os.getenv('GITHUB_WORKSPACE', '.')
    
    # Debug: Print environment variables
    print("Available environment variables:")
    for key, value in os.environ.items():
        if '_TAG' in key:
            print(f"{key}={value}")
    
    for template_path, output_path in templates.items():
        # Convert paths to absolute paths using GITHUB_WORKSPACE
        full_template_path = Path(workspace) / template_path
        full_output_path = Path(workspace) / output_path
        
        if not full_template_path.exists():
            print(f"Error: Template file not found: {full_template_path}", file=sys.stderr)
            sys.exit(1)
            
        process_template(full_template_path, full_output_path)

if __name__ == "__main__":
    main()