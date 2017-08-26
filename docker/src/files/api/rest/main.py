import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import base64
from flask import Flask, abort, make_response, jsonify, url_for, request, json, send_from_directory
from flask_jsontools import jsonapi
from werkzeug.utils import secure_filename

from rest_utils import register_encoder

from files.model import Session, ArchivosModel

app = Flask(__name__)
register_encoder(app)


@app.route('/files/api/v1.0/archivo/', methods=['OPTIONS'])
@app.route('/files/api/v1.0/archivo/<uid>', methods=['OPTIONS'])
def options(*args, **kargs):
    '''
        para autorizar el CORS
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    '''
    print(request.headers)
    o = request.headers.get('Origin')
    rm = request.headers.get('Access-Control-Request-Method')
    rh = request.headers.get('Access-Control-Request-Headers')

    r = make_response()
    r.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,HEAD,DELETE'
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['Access-Control-Allow-Headers'] = rh
    r.headers['Access-Control-Max-Age'] = 1
    return r

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    r.headers['Access-Control-Allow-Origin'] = '*'
    return r


@app.route('/files/api/v1.0/archivo/', methods=['GET'])
@jsonapi
def archivos():
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    session = Session()
    try:
        return ArchivosModel.archivos(session=session, offset=offset, limit=limit)
    finally:
        session.close()

@app.route('/files/api/v1.0/archivo/<fid>', methods=['GET'])
@jsonapi
def archivo(fid):
    session = Session()
    try:
        return ArchivosModel.archivo(session=session, fid=fid, solo_contenido=False)
    finally:
        session.close()

@app.route('/files/api/v1.0/archivo/<fid>/contenido', methods=['GET'])
def contenido(fid):
    session = Session()
    try:
        arch = ArchivosModel.archivo(session=session, fid=fid)
        response = make_response(base64.b64decode(arch.contenido))
        response.headers['Content-Type'] = arch.tipo
        response.headers['Content-Disposition'] = 'attachment; filename=' + arch.nombre
        return response
    finally:
        session.close()

@app.route('/files/api/v1.0/archivo/<fid>.json', methods=['PUT','POST'])
@jsonapi
def agregar_archivo_json(fid):
    session = Session()
    try:
        data = json.loads(request.get_data())
        logging.debug('agregando archivo json ')
        logging.debug(data)
        ArchivosModel.agregar_archivo(session, fid=data['id'], nombre='', contenido=data['data'])
        session.commit()

    finally:
        session.close()


@app.route('/files/api/v1.0/archivo/', methods=['PUT','POST'])
@jsonapi
def agregar_archivo():
    session = Session()
    try:
        f = request.files['file']
        contenido = f.read()
        ArchivosModel.agregar_archivo(session, nombre='', contenido=base64.b64encode(contenido).decode())
        session.commit()

    finally:
        session.close()


def main():
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()
