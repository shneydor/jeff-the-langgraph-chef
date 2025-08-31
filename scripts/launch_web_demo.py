#!/usr/bin/env python3
"""Launch Jeff's web demonstration interface."""

import sys
from pathlib import Path

# Add project root to Python path with error handling
try:
    project_root = Path(__file__).parent.parent
    if not project_root.exists():
        print(f"❌ Error: Project root directory not found: {project_root}")
        sys.exit(1)
    sys.path.insert(0, str(project_root))
except Exception as e:
    print(f"❌ Error setting up project path: {e}")
    sys.exit(1)

if __name__ == "__main__":
    from jeff.web_demo import main
    main()