#!/usr/bin/env python3
from app import create_app, ensure_admin


if __name__ == "__main__":
    app = create_app()
    ensure_admin(app)
