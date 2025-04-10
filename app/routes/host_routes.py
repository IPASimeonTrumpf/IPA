from flask import Blueprint, render_template, request, jsonify

from ..utils import validate, get_timestamp
from ..services.host_service import get_host_by_id, scan_host_by_id

from ..repositories.port__repository import create_port

host_blueprint: Blueprint = Blueprint("host", __name__, static_folder="static")


@host_blueprint.route("/host/<id>")
def serve_get_host_by_id(id):
    """returns a overview of the host with the scan options etc"""
    # validation
    id_as_str = validate(id)
    id_as_int: int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return "invalid id", 400

    host = get_host_by_id(id_as_int)

    if host == None:
        # if no host has been found return a 404
        return "Host not found", 404

    return render_template("host.html", host=host), 200


@host_blueprint.route("/scan_host", methods=["POST"])
def serve_scan_host():
    """Endpoint to start a scan on a host"""
    # validation
    input_host_id = request.json["host_id"]
    input_option = request.json["option"]
    option = validate(input_option)
    try:
        host_id = int(input_host_id)
    except ValueError:
        return "Invalid id", 400
    host = get_host_by_id(host_id)
    if host == None:
        # if theres no host return 404
        return "Host not found", 404

    # check if the option exists
    if option != "1000" and option != "all" and option != "ping":
        # validate specific ports
        if option.__contains__(","):
            for port in option.split(","):
                try:
                    test = int(port)
                except ValueError:
                    return "Invalid port", 400
        else:
            # return a meaningful error
            return "Invalid option for specific scan", 400

    # performs the scan
    result = scan_host_by_id(id=host.id, option=option)

    return jsonify({"msg": result}), 200


@host_blueprint.route("/results/<id>")
def get_results_of_host(id):
    """shows the results of all scans on this host"""
    # validation
    id_as_str = validate(id)
    id_as_int: int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return "invalid id", 400
    host = get_host_by_id(id_as_int)
    if not host:
        return "Host not found", 404

    return render_template("results.html", host=host)


@host_blueprint.route("/export_results/<id>")
def export_results(id):
    """returns the template with builtin css and no additional buttons"""
    # validation
    id_as_str = validate(id)
    id_as_int: int = 0
    try:
        id_as_int = int(id_as_str)
    except ValueError:
        return "invalid id", 400

    host = get_host_by_id(id_as_int)
    if not host:
        return "Host not found", 404

    return render_template("result_for_export.html", host=host)
