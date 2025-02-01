# Multilingual FAQ System

A Django-based FAQ management system with multilingual support, built with modern best practices and security in mind.

## 🚀 Quick Start for Reviewers

### Prerequisites
- Python 3.8+
- Git

### Setup (5 minutes)
1. Clone and setup:
```bash
git clone [repository-url]
cd barathfd
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

2. Configure environment:
```bash
# Copy .env.example to .env
copy .env.example .env  # On Windows
# Edit .env if needed - default values work for local testing
```

3. Initialize database:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

4. Run the server:
```bash
python manage.py runserver
```

### 🧪 Testing the Application

1. **Admin Interface** (5 minutes)
   - Visit: http://localhost:8000/admin
   - Login with superuser credentials
   - Try creating a FAQ entry
   - Test multilingual features

2. **Public Interface** (5 minutes)
   - Visit: http://localhost:8000
   - Browse existing FAQs
   - Test language switching: add ?lang=hi or ?lang=bn to URL

3. **API Testing** (5 minutes)
   - List FAQs: GET http://localhost:8000/api/faqs/
   - View in Hindi: GET http://localhost:8000/api/faqs/?lang=hi
   - View in Bengali: GET http://localhost:8000/api/faqs/?lang=bn

### 🎯 Key Features to Review

1. **Multilingual Support**
   - Content in English, Hindi, and Bengali
   - Language switching via URL parameter
   - Automatic translation caching

2. **Admin Features**
   - Rich text editor for FAQ answers
   - Multilingual content management
   - User authentication and authorization

3. **API Capabilities**
   - RESTful endpoints
   - Language-specific responses
   - Rate limiting and authentication

4. **Security Features**
   - CSRF protection
   - XSS prevention
   - Secure session handling

### 📝 Review Criteria

1. **Functionality** (40%)
   - All features working as described
   - No critical bugs
   - Smooth multilingual switching

2. **Code Quality** (30%)
   - Clean, well-organized code
   - Proper documentation
   - Following Django best practices

3. **Security** (20%)
   - Proper authentication
   - Data validation
   - Security best practices

4. **Performance** (10%)
   - Quick page loads
   - Efficient database queries
   - Proper caching

### 🐛 Common Issues & Solutions

1. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Ensure DEBUG=True in development
   - Clear browser cache

2. **Database Issues**
   - Delete db.sqlite3 and run migrations again
   - Check database settings in .env

3. **Translation Not Working**
   - Verify language code in URL (?lang=hi)
   - Check Redis connection if using caching

## Features

- 🌐 **Multilingual Support**
  - English, Hindi, and Bengali languages
  - Automatic translation using Google Translate API
  - Cached translations for performance
  - Language selection via query parameter

- 📝 **FAQ Management**
  - Rich text editor (CKEditor) for answers
  - Admin interface for content management
  - Support for multiple languages per FAQ
  - Automatic ordering by creation date

- 🔒 **Security**
  - Secure authentication system
  - CSRF protection
  - XSS prevention
  - Secure session handling
  - HTTPS enforcement (in production)

- 🚀 **Performance**
  - Redis caching
  - Database query optimization
  - Static file compression
  - Translation caching

- 🔄 **API Support**
  - RESTful API using Django REST Framework
  - Language-specific responses
  - Rate limiting
  - Token authentication

## Requirements

- Python 3.8+
- PostgreSQL
- Redis
- Node.js (for static assets)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multilingual-faq.git
   cd multilingual-faq
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration

The following environment variables are available for configuration:

### Django Settings
- `DEBUG`: Set to False in production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Settings
- `DATABASE_URL`: PostgreSQL connection URL

### Cache Settings
- `REDIS_URL`: Redis connection URL

### Security Settings
- `SECURE_SSL_REDIRECT`: Enable HTTPS redirect
- `SESSION_COOKIE_SECURE`: Secure session cookie
- `CSRF_COOKIE_SECURE`: Secure CSRF cookie

### Email Settings
- `EMAIL_HOST`: SMTP host
- `EMAIL_PORT`: SMTP port
- `EMAIL_USE_TLS`: Use TLS for email
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password

### Google Translate Settings
- `GOOGLE_TRANSLATE_API_KEY`: Google Translate API key

## Usage

1. Access the admin interface at `/admin`
2. Add FAQs in the primary language (English)
3. Translations will be generated automatically
4. View FAQs on the home page
5. Switch languages using the `?lang=` parameter

## API Endpoints

- `GET /api/faqs/`: List all FAQs
- `GET /api/faqs/?lang=hi`: List FAQs in Hindi
- `POST /api/faqs/`: Create new FAQ (admin only)
- `PUT /api/faqs/<id>/`: Update FAQ (admin only)
- `DELETE /api/faqs/<id>/`: Delete FAQ (admin only)

## API Documentation

### Authentication

The API uses token-based authentication. To get a token:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

### FAQ Endpoints

#### List FAQs
```bash
# Get FAQs in default language (English)
curl http://localhost:8000/api/faqs/

# Get FAQs in Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Get FAQs in Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

#### Create FAQ (Requires Authentication)
```bash
curl -X POST http://localhost:8000/api/faqs/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this?",
    "answer": "This is a test FAQ."
  }'
```

#### Update FAQ (Requires Authentication)
```bash
curl -X PUT http://localhost:8000/api/faqs/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Updated question?",
    "answer": "Updated answer."
  }'
```

#### Delete FAQ (Requires Authentication)
```bash
curl -X DELETE http://localhost:8000/api/faqs/1/ \
  -H "Authorization: Token your_token_here"
```

## Contributing

We welcome contributions! Here's how you can help:

### Setting up Development Environment

1. Fork the repository
2. Create a virtual environment and install dependencies
3. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes
5. Run tests
   ```bash
   pytest
   ```
6. Check code style
   ```bash
   flake8
   ```

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the requirements.txt if you add dependencies
3. Run all tests and ensure they pass
4. Follow the commit message convention:
   - feat: Add new feature
   - fix: Bug fix
   - docs: Documentation changes
   - style: Code style changes
   - refactor: Code refactoring
   - test: Add or update tests
   - chore: Routine tasks, maintenance

5. Create a Pull Request with a clear title and description

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Write docstrings for classes and methods
- Keep functions small and focused
- Write meaningful commit messages

## Security Considerations

1. Always use HTTPS in production
2. Keep the secret key secure
3. Disable DEBUG in production
4. Regularly update dependencies
5. Use strong passwords
6. Monitor application logs
7. Configure proper CORS settings

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
