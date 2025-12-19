# Security Policy

## Supported Versions

Currently supported versions of FinanceFlow:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT open a public issue

Security vulnerabilities should be reported privately to prevent exploitation.

### 2. Email the maintainers

Send an email to: **[your-security-email@example.com]**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Wait for response

We will:
- Acknowledge receipt within **24 hours**
- Provide an initial assessment within **72 hours**
- Work on a fix and keep you updated
- Credit you in the security advisory (if desired)

### 4. Coordinated disclosure

We request:
- Allow us reasonable time to fix the issue before public disclosure
- We will coordinate with you on disclosure timing
- We will credit you for the discovery (unless you prefer to remain anonymous)

## Security Best Practices

### For Deployment

If you're deploying FinanceFlow in production:

1. **Use Environment Variables**
   - Never commit API keys, passwords, or secrets
   - Use `.env` file (which is gitignored)

2. **Enable Authentication**
   - Currently single-user mode
   - Add JWT authentication for multi-user deployments
   - Use strong passwords and session management

3. **Database Security**
   - Use PostgreSQL instead of SQLite for production
   - Enable database encryption
   - Regular backups
   - Secure connection strings

4. **API Security**
   - Enable CORS properly (don't use `*` in production)
   - Rate limiting for API endpoints
   - Input validation on all endpoints
   - Use HTTPS only

5. **Dependency Updates**
   - Regularly update dependencies
   - Monitor for security advisories
   - Use `pip audit` and `npm audit`

### For Development

1. **Never commit**
   - `.env` files
   - Database files
   - API keys or secrets
   - Personal data

2. **Use Virtual Environments**
   - Always use `.venv` for Python
   - Use `node_modules` for frontend (local)

3. **Review Dependencies**
   - Check for known vulnerabilities
   - Use trusted packages only
   - Keep dependencies updated

## Known Security Considerations

### Current Version (2.0.0)

**⚠️ Important Notes:**

1. **No Authentication**
   - Current version is single-user
   - No login/authentication system
   - Suitable for personal use only
   - **DO NOT** deploy publicly without adding authentication

2. **SQLite Database**
   - File-based database (not suitable for multi-user)
   - No encryption by default
   - For production: use PostgreSQL with encryption

3. **Local Storage**
   - Some data stored in browser localStorage
   - Cleared when browser cache is cleared
   - Not encrypted

4. **API Endpoints**
   - Currently public (no auth required)
   - Anyone with URL access can modify data
   - Add JWT authentication before deploying publicly

5. **AI/ML Models**
   - Models stored locally
   - No sensitive data in models
   - User data used for predictions only (not stored in model)

## Planned Security Enhancements

Version 2.1 will include:
- [ ] JWT-based authentication
- [ ] User registration and login
- [ ] Session management
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Input sanitization improvements

Version 3.0 will include:
- [ ] OAuth2 integration
- [ ] Two-factor authentication
- [ ] Encryption at rest
- [ ] Audit logging
- [ ] Role-based access control

## Security Checklist for Contributors

When contributing:

- [ ] No hardcoded secrets or API keys
- [ ] Input validation for all user inputs
- [ ] SQL injection prevention (using parameterized queries)
- [ ] XSS prevention (React escapes by default)
- [ ] CSRF tokens for state-changing operations
- [ ] Proper error handling (don't leak sensitive info)
- [ ] Dependencies are up-to-date
- [ ] No sensitive data in logs

## Contact

For security issues: **[your-security-email@example.com]**

For general issues: [GitHub Issues](https://github.com/yourusername/financeflow/issues)

---

**Thank you for helping keep FinanceFlow secure! 🔒**
