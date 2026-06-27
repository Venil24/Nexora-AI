"""
backend/app/middleware/error_handler.py
Global error handlers and JSON response helpers.
"""
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from werkzeug.exceptions import HTTPException


def success_response(data=None, message="Success", status_code=200):
    """Standard success response."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400, errors=None):
    """Standard error response."""
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code


def register_error_handlers(app):
    """Register all error handlers on the Flask app."""

    @app.errorhandler(400)
    def bad_request(e):
        return error_response(str(e.description) if hasattr(e, 'description') else "Bad Request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response("Unauthorized — please log in", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error_response("Forbidden — you do not have permission", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_response("Method not allowed", 405)

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return error_response("File too large. Maximum allowed size is 10MB.", 413)

    @app.errorhandler(422)
    def unprocessable(e):
        return error_response("Validation error", 422)

    @app.errorhandler(429)
    def rate_limited(e):
        return error_response("Too many requests. Please slow down.", 429)

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Internal error: {e}")
        return error_response("Internal server error. Please try again later.", 500)

    @app.errorhandler(NoAuthorizationError)
    def jwt_missing(e):
        return error_response("Authentication token missing or invalid", 401)

    @app.errorhandler(InvalidHeaderError)
    def jwt_invalid_header(e):
        return error_response("Invalid Authorization header format", 401)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error_response(e.description, e.code)
