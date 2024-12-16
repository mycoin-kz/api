# Crypto Signals Platform

A Django-based REST API platform that provides cryptocurrency investment signals and analysis tools.

## Features

- User authentication (Google, Facebook, Twitter)
- Cryptocurrency watchlist management
- Technical indicators and sentiment analysis
- Social media metrics integration
- Code repository analysis

## Tech Stack

- Python 3.9+
- Django 4.1
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Project Structure

```
backend/
├── api/                    # Django project settings
├── auth_module/           # Authentication related code
├── main_module/          # Core business logic
│   ├── models/          # Database models
│   ├── services/       # Business logic services
│   ├── serializers/   # API serializers
│   └── views/        # API endpoints
├── oneshots/           # One-time scripts
└── requirements.txt    # Python dependencies
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all functions and classes
- Keep functions small and focused

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=.
```

### Adding New Features

1. Create a new branch from `main`
2. Write tests first (TDD approach)
3. Implement the feature
4. Add documentation
5. Submit a pull request

## API Documentation

API documentation is available at `/api/docs/` when running the server.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
