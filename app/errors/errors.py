from flask import Blueprint
from flask import jsonify,request
import traceback
from app.utils.logger import logger

error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(400)
def bad_request(e):
    description = getattr(e, 'description', str(e))

    if isinstance(description, list):
        details = []
        for err in description:
            field_path = " -> ".join(str(part) for part in err.get("loc", []))
            message = err.get("msg", "Invalid input")
            details.append({
                "field": field_path,
                "message": message
            })
        return jsonify({
            "error": "Bad Request",
            "message": "Validation failed",
            "details": details
        }), 400

    logger.warning(f"400 Bad Request at {request.path}: {description}")
    return jsonify({
        "error": "Bad Request",
        "message": str(description)
    }), 400


@error_bp.app_errorhandler(401)
def unauthorized(e):
    return jsonify({
        'error': 'Unauthorized',
        'message': e.description if hasattr(e, 'description') else 'Unauthorized access'
    }), 401


@error_bp.app_errorhandler(403)
def handle_forbidden_error(e):
    logger.warning(f"403 Forbidden: {request.path} - {str(e)}")
    return jsonify({"error": "You are not authorized to access this resource."}), 403

@error_bp.app_errorhandler(404)
def handle_not_found_error(e):
    logger.warning(f"404 Not Found: {e}")
    return jsonify({"error": "Resource not found"}), 404

@error_bp.app_errorhandler(500)
def handle_internal_server_error(e):
    if hasattr(e, 'description'):
        logger.error(f"Internal Server Error: {e.description}")
    else:
        logger.exception("Unhandled Exception: %s", traceback.format_exc())
    
    return jsonify({
        "error": "An unexpected error occurred. Please try again later."
    }), 500


@error_bp.app_errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled Exception: %s", traceback.format_exc())
    return jsonify({"error": str(e)}), 500
