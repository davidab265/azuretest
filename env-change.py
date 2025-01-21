#!/usr/bin/env python3
import os
import sys
from pathlib import Path

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
            result = os.path.expandvars(template)
        
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