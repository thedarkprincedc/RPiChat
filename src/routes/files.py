from pathlib import Path
from services.download_repository import DownloadRepository
from flask import Blueprint, current_app, send_from_directory

files_bp = Blueprint("files", __name__)
#downloadRepository = DownloadRepository(current_app.config["RPI_SQLITE_PATH"])

@files_bp.route("/files/<download_id>")
def files(download_id):
    repository = current_app.config["DOWNLOAD_REPOSITORY"]

    row = repository.get(download_id)
    
    if row is None:
        return {"error": "Download not found"}, 404

    file_path = Path(current_app.config["RPI_OUTPUT_DIR"]) / row["filename"]

    if not file_path.is_file():
        return {"error": "File not found"}, 404
    
    return send_from_directory(
        current_app.config["RPI_OUTPUT_DIR"],
        row['filename'],
        as_attachment=True,
        download_name=row["filename"]
    )