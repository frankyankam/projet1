from flask import Blueprint, jsonify, request
from services.csv_services import load_jobs

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    

    filters = {
        "entreprise": request.args.get("entreprise"),
        "adresse": request.args.get("adresse"),
        "offre": request.args.get("offre"),
    }

    jobs, total = load_jobs(filters=filters, page=page, limit=limit)

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": jobs
    })
