import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.books import Sections

section_field = {
    's_id': fields.Integer,
    's_name': fields.String,
    's_image': fields.String,
    'book_count': fields.Integer
    # 'is_deleted': fields.Boolean
}


## SECTION CRUD
class ManageSections(Resource):
    def get(self, section_id):      ## View Section by ID
        section = Sections.query.get(section_id)
        if (section is None) or (section.is_deleted):      ## Don't display deleted Sections
            return {'message': {'error': 'Section Not Found'}}, 404
        return marshal(section, section_field), 200

    @auth_required('token')
    @roles_required('librarian')
    def post(self):     ## Create new Section
        formData = request.form.to_dict()
        ## Check if Section name is Unique
        if ('s_name' in formData) and (formData['s_name']!='') and \
            (Sections.query.filter_by(s_name=formData['s_name']).first() is None):
            section = Sections(**formData)
        else:
            return {'message': {'error': 'Section Name must be Unique'}}, 400
        if 's_image' in request.files:      ## Check if Image Uploaded
            image = request.files['s_image']
            if image.filename != "":
                extension = '.'+image.filename.split('.')[-1]
                ## Get ID of last section added to database (+1 - new section ID)
                lastest_id = Sections.query.order_by(Sections.s_id.desc()).first()        
                if lastest_id:
                    lastest_id = lastest_id.s_id+1
                else:       ## If first Section - ID=1
                    lastest_id = 1
                img_path = 'image_'+str(lastest_id)+extension       ## Save image name with ID of new section
                image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                section.s_image = img_path
            else:
                return {'message': {'error': 'Improper Image'}}, 400
        else:
            return {'message': {'error': 'Improper Image'}}, 400
        db.session.add(section)
        db.session.commit()
        return {'message': {'success': 'New Section Created!'}}, 200
        
    @auth_required('token')
    @roles_required('librarian')
    def put(self, section_id):      ## Update Section 
        formData = request.form.to_dict()
        section = Sections.query.get(section_id)
        if not ('s_name' in formData or 's_image' in request.files):        ## Any one field is compulsory
            return {'message': {'error': 'Atleast one field needs to be filled!'}}, 400 
        
        if 's_name' in formData:
            ## Check if Section name is Unique
            if (formData['s_name']!='') and (Sections.query.filter_by(s_name=formData['s_name']).first() is None):
                section.s_name = formData['s_name']
            else:
                return {'message': {'error': 'Section Name must be Unique'}}, 400
        if 's_image' in request.files:      ## Check if Image Uploaded
            image = request.files['s_image']
            if image.filename != "":
                # extension = '.'+image.filename.split('.')[-1]
                # img_path = "_".join(formData['s_name'].split())+extension
                img_path = section.s_image
                image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                section.s_image = img_path
        db.session.commit()
        return {'message': {'success': f'Section with ID {section_id} has been Updated successfully!'}}, 200
        
    @auth_required('token')
    @roles_required('librarian')
    def delete(self, section_id):       ## Delete Section 
        pass

class DisplaySections(Resource):
    def get(self):      ## Display all Sections
        section = Sections.query.filter_by(is_deleted=False).all()
        return marshal(section, section_field), 200

class SectionAnalytics(Resource):
    @auth_required('token')
    @roles_required('librarian')
    def get(self):      ## Section wise distribution 
        pass 
