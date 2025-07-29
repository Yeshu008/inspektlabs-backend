from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.inspection import Inspection
from pydantic import ValidationError
from app.schemas.inspection_schema import InspectionStatusUpdateSchema,InspectionCreateSchema
from app.utils.logger import logger

inspection_bp = Blueprint('inspection', __name__)

@inspection_bp.route('/inspection', methods=['POST'])
@jwt_required()
def create_inspection():
    user_id = get_jwt_identity()
    try:
        payload = InspectionCreateSchema(**request.get_json())
    except ValidationError as e:
        abort(400, description=e.errors())

    vehicle_number = payload.vehicle_number
    damage_report = payload.damage_report
    image_url = str(payload.image_url)

    try:
        inspection = Inspection(vehicle_number=vehicle_number,
                                 damage_report=damage_report,
                                image_url=image_url, 
                                inspected_by=user_id)
        db.session.add(inspection)
        db.session.commit()
        return jsonify({'message': 'Inspection created', 'id': inspection.id}), 201
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"[INSPECTION_CREATION_FAILURE] Inspection: {inspection} - {str(e)}")

@inspection_bp.route('/inspection/<int:id>', methods=['GET'])
@jwt_required()
def get_inspection(id):
    user_id = int(get_jwt_identity())
    inspection = db.session.get(Inspection, id)
    if not inspection:
        abort(404)

    if inspection.inspected_by != user_id:
        abort(403)
    return jsonify({
        'id': inspection.id,
        'vehicle_number': inspection.vehicle_number,
        'damage_report': inspection.damage_report,
        'image_url': inspection.image_url,
        'status': inspection.status,
        'created_at': inspection.created_at.isoformat()
    })

@inspection_bp.route('/inspection/<int:id>', methods=['PATCH'])
@jwt_required()
def update_status(id):
    user_id = int(get_jwt_identity())
    try:
        payload = InspectionStatusUpdateSchema(**request.get_json())
    except ValidationError as e:
        abort(400, description=e.errors())

    status = payload.status

    inspection = db.session.get(Inspection, id)
    if not inspection:
        abort(404)

    if inspection.inspected_by != user_id:
        abort(403)

    try:
        inspection.status = status
        db.session.commit()
        return jsonify({'message': 'Status updated'})
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"[INSPECTION_UPDATE_FAILURE] Inspection: {id} - {str(e)}")

@inspection_bp.route('/inspection')
@jwt_required()
def list_inspections():
    user_id = get_jwt_identity()
    status = request.args.get('status')
    try:
        query = Inspection.query.filter_by(inspected_by=user_id)
        if status:
            query = query.filter_by(status=status)
        inspections = query.all()
        return jsonify([{
            'id': i.id,
            'vehicle_number': i.vehicle_number,
            'status': i.status,
            'created_at': i.created_at.isoformat()
        } for i in inspections])
    except Exception as e:
        abort(500, description=f"[LISTING_INSPECTION_FAILURE] using Status:{status}  for User: {user_id} - {str(e)}")