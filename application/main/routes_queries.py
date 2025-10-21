from flask import redirect, url_for, request , jsonify, json, session ,current_app as app, render_template
from . import *
from flask_uploads import UploadSet, configure_uploads, IMAGES
from models.routes_database import *
import shutil
from pathlib import Path, PurePath
import ast
from datetime import datetime

from functools import wraps
from flask import session, jsonify

query=main
CORS(query)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx','doc', 'xls','xlsx', 'mp4'])
IMAGE_FOLDER = os.path.join('static', 'image')

import unicodedata
import re
from werkzeug.utils import secure_filename


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def custom_secure_filename(filename):
    name, ext = os.path.splitext(filename)  # Split name and extension
    name = secure_filename(name)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^A-Za-z0-9_.-]', '_', name)
    name = name[:100]  # limit filename length if needed
    return name + ext  # Reattach extension

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'data' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@query.route('/save_personal_info', methods=['GET', 'POST'])
@login_required
def save_personal_info():
	p=request.form
	if p['info_id']==0 or p['info_id']=="0":
		insert="""
			insert into tbl_personal_info set f_name='"""+str(p['fname'].title())+"""',m_name='"""+str(p['mname'].title())+"""',
			l_name='"""+str(p['lname'].title())+"""',ename='"""+str(p['ename'].title())+"""', address='"""+str(p['address'].title())+"""',about='"""+str(p['about'])+"""',email='"""+str(p['email'])+"""',
			phone='"""+str(p['phone'])+"""',dob='"""+str(p['date_of_birth'])+"""'
		"""
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]
			
			n_path = Path(__file__).parent / "../static/uploads/emp_photo" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="emp_photo//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");

				update="update tbl_personal_info set img='"+str(path_location)+"' where info_id='"+str(rd)+"'"
				cud(update)
		return jsonify("Succesfuly saved")
	else:
		update="""
			update tbl_personal_info set f_name='"""+str(p['fname'].title())+"""',m_name='"""+str(p['mname'].title())+"""',
			l_name='"""+str(p['lname'].title())+"""',ename='"""+str(p['ename'].title())+"""', address='"""+str(p['address'].title())+"""',about='"""+str(p['about'])+"""',email='"""+str(p['email'])+"""',
			phone='"""+str(p['phone'])+"""',dob='"""+str(p['date_of_birth'])+"""' where info_id='"""+str(p['info_id'])+"""'
		"""
		cud(update)
		for filename_array in request.files:
			file=request.files[filename_array]
			
			n_path = Path(__file__).parent / "../static/uploads/emp_photo" / str(p['info_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="emp_photo//"+str(p['info_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");

				update1="update tbl_personal_info set img='"+str(path_location)+"' where info_id='"+str(p['info_id'])+"'"
				cud(update1)
		return jsonify("Succesfully Updated")


@query.route('/get_personal_info', methods=['GET', 'POST'])
@login_required
def get_personal_info():
	p=json.loads(request.data)
	sel="""
		select * from tbl_personal_info
		where info_id='"""+str(p['info_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_info', methods=['GET', 'POST'])
@login_required
def get_info():
	sel="select *,concat(f_name,' ',m_name,' ',L_name, ' ', IFNULL(CONCAT(' ',ename,' '),'')) fullname, img loc from tbl_personal_info"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_ordinance_for_number', methods=['GET', 'POST'])
@login_required
def get_ordinance_for_number():
	sel="select * from tbl_ordinance"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_councilor', methods=['POST','GET'])
@login_required
def get_councilor():
	try:
		sel = "SELECT tpi.info_id,concat(f_name,' ',m_name,' ',L_name, ' ', IFNULL(CONCAT(' ',ename,' '),'')) fullname FROM sp_councilor sc LEFT JOIN tbl_personal_info tpi ON sc.councilor = tpi.info_id"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_sp', methods=['GET', 'POST'])
@login_required
def get_sp():
	select="select * from tbl_sp"
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_sp_budget', methods=['GET', 'POST'])
@login_required
def get_sp_budget():
	select="""
		select * from tbl_sp_budget tsb
		left join tbl_sp ts on ts.sp_id=tsb.sp_id
	"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/get_sp_data', methods=['GET', 'POST'])
@login_required
def get_sp_data():
	p=json.loads(request.data)
	sel="select sp_id from tbl_sp_budget where sp_budget_id='"+str(p['sp_budget_id'])+"'"
	rd=pyread(sel)
	select="""
		select *, concat(tpi_mayor.f_name,' ',tpi_mayor.m_name,' ',tpi_mayor.l_name) mayor_fullname,tsbb.allocation mayor_allocation,tsbb.balance_id mayor_balance_id,
		concat(tpi_vmayor.f_name,' ',tpi_vmayor.m_name,' ',tpi_vmayor.l_name) vmayor_fullname,tsbb2.allocation vmayor_allocation,tsbb2.balance_id vmayor_balance_id,
		concat(tpi_sec.f_name,' ',tpi_sec.m_name,' ',tpi_sec.l_name) sec_fullname,tsbb3.allocation sec_allocation,tsbb3.balance_id sec_balance_id,
		concat(tpi_coun.f_name,' ',tpi_coun.m_name,' ',tpi_coun.l_name) councilors,tsbb4.allocation councilor_allocation,tsbb4.balance_id counc_balance_id
		from tbl_sp ts
		left join sp_member sm on ts.sp_id=sm.sp_id
		left join sp_councilor sc on sm.sp_member_id=sc.sp_member_id
		left join tbl_personal_info tpi_mayor on tpi_mayor.info_id=sp_mayor
		left join tbl_personal_info tpi_vmayor on tpi_vmayor.info_id=sp_vice_mayor
		left join tbl_personal_info tpi_sec on tpi_sec.info_id=sp_secretary
		left join tbl_personal_info tpi_coun on tpi_coun.info_id=sc.councilor

		left join tbl_sp_budget_balance tsbb on tsbb.info_id=sm.sp_mayor
		left join tbl_sp_budget_balance tsbb2 on tsbb2.info_id=sm.sp_vice_mayor
		left join tbl_sp_budget_balance tsbb3 on tsbb3.info_id=sm.sp_secretary

		left join tbl_sp_budget_balance tsbb4 on tsbb4.info_id=sc.councilor

		where ts.sp_id='"""+str(rd[0]['sp_id'])+"""' group by sc.sp_councilor
	"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/sel_personal_info', methods=['GET', 'POST'])
def sel_personal_info():
	select="select info_id,concat(f_name,' ',m_name,' ',L_name, ' ', IFNULL(CONCAT(' ',ename,' '),'')) fullname from tbl_personal_info"
	rd=pyread(select)
	return jsonify(rd)


@query.route('/save_sp', methods=['GET', 'POST'])
@login_required
def save_sp():
	p=request.form
	title=p['title'].replace("'","''")

	p=json.loads(p['Serialized'])
	year_range = p['sp_year'] +'-' +p['sp_year2']

	if p['sp_id']==0 or p['sp_id']=="0":
		insert_sp="insert into tbl_sp set sp_year='"+str(year_range)+"', sp_title='"+str(title)+"'"
		r_id=cud_callbackid(insert_sp)

		insert_sp_member="insert into sp_member set sp_vice_mayor='"+str(p['vmayor'])+"', sp_secretary='"+str(p['secretary'])+"', sp_id='"+str(r_id)+"'"
		r_id2=cud_callbackid(insert_sp_member)
		
		for n in p['council_name']:
			insert_sp_councilor="insert into sp_councilor set councilor='"+str(n['council_name'])+"', sp_member_id='"+str(r_id2)+"'"
			cud(insert_sp_councilor)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="logo":
				x=x+1
				file_name="logo["+str(x)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_sp_logo" / str(r_id)
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_sp_logo//"+str(r_id)
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					update_sp="update tbl_sp set sp_logo='"+str(path_location)+"' where sp_id='"+str(r_id)+"'"
					cud(update_sp)


			if str(split[0])=="citylogo":
				y=y+1
				file_name="citylogo["+str(y)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_city_logo" / str(r_id)
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_city_logo//"+str(r_id)
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					update_sp="update tbl_sp set city_logo='"+str(path_location)+"' where sp_id='"+str(r_id)+"'"
					cud(update_sp)

		return jsonify('Succesfuly saved')
	else:
		update_sp="""
			update tbl_sp set sp_year='"""+str(year_range)+"""', sp_title='"""+str(title)+"""' where sp_id='"""+str(p['sp_id'])+"""'
		"""
		cud(update_sp)

		update_sp_member="""
			update sp_member set sp_vice_mayor='"""+str(p['vmayor'])+"""', 
			sp_secretary='"""+str(p['secretary'])+"""' where sp_id='"""+str(p['sp_id'])+"""'
		"""
		cud(update_sp_member)

		select="select sp_member_id from sp_member where sp_id='"+str(p['sp_id'])+"'"
		rd=pyread(select)

		delete="delete from sp_councilor where sp_member_id='"+str(rd[0]['sp_member_id'])+"'"
		cud(delete)

		for n in p['council_name']:
			insert_sp_councilor="insert into sp_councilor set councilor='"+str(n['council_name'])+"', sp_member_id='"+str(rd[0]['sp_member_id'])+"'"
			cud(insert_sp_councilor)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="logo":
				x=x+1
				file_name="logo["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_sp_logo" / str(p['sp_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_sp_logo//"+str(p['sp_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					update_sp="update tbl_sp set sp_logo='"+str(path_location)+"' where sp_id='"+str(p['sp_id'])+"'"
					cud(update_sp)


			if str(split[0])=="citylogo":
				y=y+1
				file_name="citylogo["+str(y)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_city_logo" / str(p['sp_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_city_logo//"+str(p['sp_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					update_sp="update tbl_sp set city_logo='"+str(path_location)+"' where sp_id='"+str(p['sp_id'])+"'"
					cud(update_sp)
		return jsonify("Succesfuly Updated")

@query.route('/del_sp', methods=['GET', 'POST'])
@login_required
def del_sp():
	p=json.loads(request.data)
	delete="delete from tbl_sp where sp_id='"+str(p['sp_id'])+"'"
	cud(delete)
	return jsonify('Succesfuly Deleted')

@query.route('/get_sp_member', methods=['GET', 'POST'])
@login_required
def get_sp_member():
	p=json.loads(request.data)
	try:
		select="""
				SELECT
					ts.sp_id,
					ts.sp_logo,
					ts.city_logo,
					ts.sp_title,
					ts.`status`,
					ts.sp_year,
					sm.sp_member_id,

					CONCAT(tpi_myr.f_name, " ",tpi_myr.m_name, " ", tpi_myr.l_name) mayor,
					CONCAT(tpi_vmyr.f_name, " ",tpi_vmyr.m_name, " ", tpi_vmyr.l_name) vice_mayor,
					CONCAT(tpi_sec.f_name, " ",tpi_sec.m_name, " ", tpi_sec.l_name) secretary,

					sm.sp_mayor,sm.sp_vice_mayor,sm.sp_secretary
				FROM
					tbl_sp ts
					LEFT JOIN sp_member sm ON ts.sp_id = sm.sp_id
					LEFT JOIN tbl_personal_info tpi_myr ON tpi_myr.info_id = sm.sp_mayor
					LEFT JOIN tbl_personal_info tpi_vmyr ON tpi_vmyr.info_id = sm.sp_vice_mayor 
					LEFT JOIN tbl_personal_info tpi_sec ON tpi_sec .info_id = sm.sp_secretary
					where 
						ts.sp_id ='"""+str(p['sp_id'])+"""'
			"""
		rd = pyread(select)

		sel = """SELECT
					*,
					CONCAT( tpi.f_name, " ", tpi.m_name, " ", tpi.l_name ) council_fullname
				FROM
					sp_councilor sc
					LEFT JOIN sp_member sm ON sc.sp_member_id = sm.sp_member_id
					LEFT JOIN tbl_personal_info tpi ON tpi.info_id = sc.councilor 
				WHERE
					sc.sp_member_id =  '"""+str(rd[0]['sp_member_id'])+"""' 
			"""
		res = pyread(sel)

		rd[0]['councilors'] = res

		return jsonify(rd)
	except Exception as e:
		prnt_R(e)
		return e
		


@query.route('/get_sp_member_deduction', methods=['GET', 'POST'])
@login_required
def get_sp_member_deduction():
	p=json.loads(request.data)
	select="""
		SELECT
			*, 
			COALESCE(sum(tsbbe.deduction),0) total_deduction,
			concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) fullname,
			(case when (allocation-sum(tsbbe.deduction)) is NULL then 
				 tsbb.allocation
			else
				allocation-sum(tsbbe.deduction)
			end ) remaining
		FROM
			tbl_sp ts

			left join tbl_sp_budget tsb on tsb.sp_id=ts.sp_id
			left join tbl_sp_budget_balance tsbb on tsbb.sp_budget_id=tsb.sp_budget_id
			left join tbl_personal_info tpi on tpi.info_id=tsbb.info_id
			
			left join tbl_sp_budget_balance_expenses tsbbe on tsbbe.balance_id=tsbb.balance_id

			where ts.sp_id='"""+str(p['sp_id'])+"""'
			group by tsbb.balance_id
		"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/get_committee', methods=['GET', 'POST'])
def get_committee():
	select="""
		select * from tbl_committee tc
		left join tbl_sp ts on ts.sp_id=tc.sp_id 
		where ts.`status`='ACTIVE'
	"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/get_committeeBySp', methods=['GET', 'POST'])
@login_required
def get_committeeBySp():
	p=json.loads(request.data)
	select="""
		select * from tbl_committee where sp_id='"""+str(p['sp_id'])+"""'
	"""
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_committee_petition_minutes_file', methods=['GET', 'POST'])
@login_required
def get_committee_petition_minutes_file():
	p=json.loads(request.data)
	select="""
			select * from tbl_minutes_path_committee_petition 
			where petition_id='"""+str(p['petition_id'])+"""' 
			and committee_id='"""+str(p['committee_id'])+"""'
		"""
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_committee_member', methods=['GET', 'POST'])
@login_required
def get_committee_member():
	p=json.loads(request.data)
	select="""
			select *,concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) fullname from tbl_committee tc
			left join tbl_committee_members tcm on tcm.committee_id=tc.committee_id
			left join tbl_personal_info tpi on tpi.info_id =tcm.committee_members
			where tc.committee_id='"""+str(p['committee_id'])+"""'
		"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/save_sp_budget', methods=['GET', 'POST'])
@login_required
def save_sp_budget():
	p=json.loads(request.data)
	insert="insert into tbl_sp_budget set sp_id='"+str(p['sp_id'])+"', budget_year='"+str(p['year'])+"' "
	rd=cud_callbackid(insert)
	sel="select * from sp_member where sp_id='"+str(p['sp_id'])+"'"
	s_rd=pyread(sel)

	member_arr=[s_rd[0]['sp_mayor'],s_rd[0]['sp_vice_mayor'],s_rd[0]['sp_secretary']]

	for i in range(len(member_arr)):
		if member_arr[i]:
			insert_member="insert into tbl_sp_budget_balance set info_id='"+str(member_arr[i])+"' , allocation=0,expenses=0, balance=0, sp_budget_id='"+str(rd)+"'"
			cud(insert_member)

	sel_counc="select * from sp_councilor where sp_member_id='"+str(s_rd[0]['sp_member_id'])+"'"
	sc_rd=pyread(sel_counc)
	for x in range(len(sc_rd)):
		insert_member="insert into tbl_sp_budget_balance set info_id='"+str(sc_rd[x]['councilor'])+"' , allocation=0,expenses=0, balance=0, sp_budget_id='"+str(rd)+"'"
		cud(insert_member)
	return jsonify("Succesfuly Saved")


@query.route('/update_sp_budget_year', methods=['GET', 'POST'])
@login_required
def update_sp_budget_year():
	p=json.loads(request.data)
	upd="update tbl_sp_budget set budget_year='"+str(p['budget_year'])+"' where sp_budget_id='"+str(p['sp_buget_id'])+"'"
	cud(upd)
	return jsonify("Succesfuly Updated")



@query.route('/get_committee_co_chair', methods=['GET', 'POST'])
@login_required
def get_committee_co_chair():
	p=json.loads(request.data)
	sel="""
		select *,concat(tpi.f_name,' ',tpi.m_name,' ',l_name) as co_chairman_fullname 
		from tbl_committee tc
		left join tbl_personal_info tpi on tpi.info_id=tc.co_chairman
		where committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_committee', methods=['GET', 'POST'])
@login_required
def save_committee():
	p=json.loads(request.data)
	if p['committee_id']==0 or p['committee_id']=="0":
		insert="insert into tbl_committee set committee='"+str(p['committee_name'])+"', phone_no='"+str(p['phone'])+"', email='"+str(p['committee_email'])+"', chairman='"+str(p['committee_chair'])+"', co_chairman='"+str(p['co_chairman'])+"' , sp_id='"+str(p['sangunian_council'])+"'"
		rd_id=cud_callbackid(insert)

		if 'members' in p:
			for n in p['members']:
				insert_member="insert into tbl_committee_members set committee_members='"+str(n)+"', committee_id='"+str(rd_id)+"' "
				cud(insert_member)

		return jsonify("Succesfuly Saved")
	else:

		update="update tbl_committee set committee='"+str(p['committee_name'])+"', phone_no='"+str(p['phone'])+"', email='"+str(p['committee_email'])+"', chairman='"+str(p['committee_chair'])+"', co_chairman='"+str(p['co_chairman'])+"', sp_id='"+str(p['sangunian_council'])+"'  where committee_id='"+str(p['committee_id'])+"'"
		cud(update)

		delete="delete from tbl_committee_members where committee_id='"+str(p['committee_id'])+"'"
		cud(delete)

		if 'members' in p:
			for n in p['members']:
				select="select count(*) counter from tbl_committee_members where committee_members='"+str(n)+"' and committee_id='"+str(p['committee_id'])+"'"
				rd_if_exist=pyread(select)

				if rd_if_exist[0]['counter']==0 or rd_if_exist[0]['counter']=="0":
					insert_member="insert into tbl_committee_members set committee_members='"+str(n)+"', committee_id='"+str(p['committee_id'])+"' "
					cud(insert_member)

		return jsonify("Succesfuly Updated")


@query.route('/get_committee_ordinance', methods=['GET', 'POST'])
@login_required
def get_committee_ordinance():
	p=json.loads(request.data)

	sel="""
		select *,
		(
			CASE
			    WHEN `status` = 1 THEN "Propose Ordinance"
				WHEN `status` = 2 THEN "2nd Reading Ordinance"
				WHEN `status` = 3 THEN "3rd Reading Ordinance"
				WHEN `status` = 4 THEN "3rd Reading Ordinance Excemption"
				WHEN `status` = 5 THEN "For Mayor's Approval"
				WHEN `status` = 6 THEN "Approved Ordinance"
				WHEN `status` = 7 THEN "Veto Ordinance"
				WHEN `status` = 8 THEN "Archive Ordinance"
			    ELSE "No status"
			END) stats_ordinance
			 from tbl_ordinance tbo
			 left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		where tcro.committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/delete_committee_ref_ordinance', methods=['GET', 'POST'])
@login_required
def delete_committee_ref_ordinance():
	p=json.loads(request.data)
	sel="""
		select count(*) counter from tbl_ordinance_file_committee 
		where committee_id="""+str(p['committee_id'])+""" and ordinance_id="""+str(p['ordinance_id'])+"""
	"""
	rd=pyread(sel)
	
	if rd[0]['counter']==0 or rd[0]['counter']=="0":
		delete="""
			delete from tbl_committee_ref_ordinance 
			where committee_id="""+str(p['committee_id'])+""" and ordinance_id="""+str(p['ordinance_id'])+"""
			and committee_ref_id='"""+str(p['committee_ref_id'])+"""' 
		"""
		cud(delete)
		return jsonify("Successfully Deleted")
	else:

		return jsonify("You cannot Remove From referal")


@query.route('/delete_committee_ref_resolution', methods=['GET', 'POST'])
@login_required
def delete_committee_ref_resolution():
	p=json.loads(request.data)
	sel="""
		select count(*) counter from tbl_resolution_file_committee 
		where committee_id="""+str(p['committee_id'])+""" and resolution_id="""+str(p['resolution_id'])+"""
	"""
	rd=pyread(sel)
	if rd[0]['counter']==0 or rd[0]['counter']=="0":
		delete="""
			delete from tbl_committee_ref_resolution 
			where committee_id="""+str(p['committee_id'])+""" and resolution_id="""+str(p['resolution_id'])+"""
			and committee_resolution_id='"""+str(p['committee_resolution_id'])+"""'
		"""
		cud(delete)
		return jsonify("Successfully Deleted")
	else:
		return jsonify("You cannot Remove From referal")


@query.route('/delete_committee_ref_petition', methods=['GET', 'POST'])
@login_required
def delete_committee_ref_petition():
	p=json.loads(request.data)
	sel="""
		select count(*) counter from tbl_petition_path_committee 
		where committee_id="""+str(p['committee_id'])+""" and petition_id="""+str(p['petition_id'])+"""
	"""
	rd=pyread(sel)
	if rd[0]['counter']==0 or rd[0]['counter']=="0":
		delete="""
			delete from tbl_committee_ref_petition 
			where committee_id="""+str(p['committee_id'])+""" and petition_id="""+str(p['petition_id'])+""" 
			and committee_ref_petition_id='"""+str(p['committee_ref_petition_id'])+"""'
		"""
		cud(delete)
		return jsonify("Successfully Deleted")
	else:
		return jsonify("You cannot Remove From referal")


@query.route('/get_committee_resolution', methods=['GET', 'POST'])
@login_required
def get_committee_resolution():
	p=json.loads(request.data)
	sel="""
		select * from tbl_resolution tr
		left join tbl_committee_ref_resolution tcrr on tcrr.resolution_id=tr.resolution_id
		where tcrr.committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_ordinance', methods=['GET', 'POST'])
@login_required
def get_ordinance():
	select="""
		select *,(CASE 
			WHEN `source_of_document` = 1 THEN "SANGGUNIANG FILES"
			WHEN `source_of_document` = 2 THEN "SANGGUNIANG PANLALAWIGAN"
			WHEN `source_of_document` = 3 THEN ""
			ELSE "OTHER"
		END) stats, 
		(
			CASE
			    WHEN tbo.`status` = 1 THEN "Propose Ordinance"
				WHEN tbo.`status` = 2 THEN "2nd Reading Ordinance"
				WHEN tbo.`status` = 3 THEN "3rd Reading Ordinance"
				WHEN tbo.`status` = 4 THEN "3rd Reading Ordinance Excemption"
				WHEN tbo.`status` = 5 THEN "For Mayor's Approval"
				WHEN tbo.`status` = 6 THEN "Approved Ordinance"
				WHEN tbo.`status` = 7 THEN "Veto Ordinance"
				WHEN tbo.`status` = 8 THEN "Archive Ordinance"
			    ELSE "No status"
			END) stats_ordinance, tc.title category_title, tcro.committee_id committee_idss, GROUP_CONCAT(tcro.committee_id) as ref_committee from tbl_ordinance tbo
		left join tbl_category tc on tc.category_id=tbo.category
		left join tbl_ordinance_file_committee tofc on tofc.ordinance_id=tbo.ordinance_id
		left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		left join tbl_sp ts on ts.sp_id=tbo.sp_id where ts.`status`='ACTIVE'
		GROUP BY tbo.ordinance_id
	"""
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_ordinance_status', methods=['GET', 'POST'])
@login_required
def get_ordinance_status():
	p=json.loads(request.data)
	select="""
		select *,(CASE 
			WHEN `source_of_document` = 1 THEN "SANGUNIAN FILES"
			WHEN `source_of_document` = 2 THEN "SANGUNIAN PANLALAWIGAN"
			WHEN `source_of_document` = 3 THEN ""
			ELSE "OTHER"
		END) stats, 
		(
			CASE
			    WHEN tbo.`status` = 1 THEN "Propose Ordinance"
				WHEN tbo.`status` = 2 THEN "2nd Reading Ordinance"
				WHEN tbo.`status` = 3 THEN "3rd Reading Ordinance"
				WHEN tbo.`status` = 4 THEN "3rd Reading Ordinance Excemption"
				WHEN tbo.`status` = 5 THEN "For Mayor's Approval"
				WHEN tbo.`status` = 6 THEN "Approved Ordinance"
				WHEN tbo.`status` = 7 THEN "Veto Ordinance"
				WHEN tbo.`status` = 8 THEN "Archive Ordinance"
			    ELSE "No status"
			END) stats_ordinance, tc.title category_title, tcro.committee_id committee_idss, GROUP_CONCAT(Distinct tcro.committee_id) as ref_committee from tbl_ordinance tbo
		left join tbl_category tc on tc.category_id=tbo.category
		left join tbl_ordinance_file_committee tofc on tofc.ordinance_id=tbo.ordinance_id
		left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		left join tbl_sp ts on ts.sp_id=tbo.sp_id
		where tbo.`status`='"""+str(p['status'])+"""' and ts.`status`='ACTIVE' and type_ord='Ordinance'
		GROUP BY tbo.ordinance_id
	"""
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_ordinance_status_appropriation', methods=['GET', 'POST'])
@login_required
def get_ordinance_status_appropriation():
	p=json.loads(request.data)
	select="""
		select *,(CASE 
			WHEN `source_of_document` = 1 THEN "SANGUNIAN FILES"
			WHEN `source_of_document` = 2 THEN "SANGUNIAN PANLALAWIGAN"
			WHEN `source_of_document` = 3 THEN ""
			ELSE "OTHER"
		END) stats, 
		(
			CASE
			    WHEN tbo.`status` = 1 THEN "Propose Ordinance"
				WHEN tbo.`status` = 2 THEN "2nd Reading Ordinance"
				WHEN tbo.`status` = 3 THEN "3rd Reading Ordinance"
				WHEN tbo.`status` = 4 THEN "3rd Reading Ordinance Excemption"
				WHEN tbo.`status` = 5 THEN "For Mayor's Approval"
				WHEN tbo.`status` = 6 THEN "Approved Ordinance"
				WHEN tbo.`status` = 7 THEN "Veto Ordinance"
				WHEN tbo.`status` = 8 THEN "Archive Ordinance"
			    ELSE "No status"
			END) stats_ordinance, tc.title category_title, tcro.committee_id committee_idss, GROUP_CONCAT(Distinct tcro.committee_id) as ref_committee from tbl_ordinance tbo
		left join tbl_category tc on tc.category_id=tbo.category
		left join tbl_ordinance_file_committee tofc on tofc.ordinance_id=tbo.ordinance_id
		left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		left join tbl_sp ts on ts.sp_id=tbo.sp_id
		where tbo.`status`='"""+str(p['status'])+"""' and ts.`status`='ACTIVE' and type_ord='Appropriation Ordinance'
		GROUP BY tbo.ordinance_id
	"""
	rd=pyread(select)
	return jsonify(rd)

@query.route('/get_resolution', methods=['GET', 'POST'])
@login_required
def get_resolution():
	p=json.loads(request.data)
	sel="""	
		select * ,
		(CASE 
			WHEN tr.`status` = 1 THEN "Propose Resolution"
			WHEN tr.`status` = 2 THEN "2nd Reading Resolution"
			WHEN tr.`status` = 3 THEN "3rd Reading Resolution"
			WHEN tr.`status` = 4 THEN "3rd Reading Resolution Excemption"
			WHEN tr.`status` = 5 THEN "For Mayor's Approval"
			WHEN tr.`status` = 6 THEN "Approved Resolution"
			WHEN tr.`status` = 7 THEN "Veto Resolution"
			WHEN tr.`status` = 8 THEN "Archive Resolution"
		    ELSE "No status"
		END) stats,  tcg.title category_title, tc.committee_id committee_ids, group_concat(tcrf.committee_id) as ref_committee
		from tbl_resolution tr
		left join tbl_category tcg on tcg.category_id=tr.category
		left join tbl_committee_ref_resolution tcrf on tcrf.resolution_id=tr.resolution_id
		left join tbl_committee tc on tc.committee_id=tcrf.committee_id
		left join tbl_resolution_file_committee trfc on trfc.resolution_id=tr.resolution_id
		left join tbl_sp ts on ts.sp_id=tr.sp_id
		left join tbl_committee tc2 on tc2.sp_id=ts.sp_id
		where tr.`status`='"""+str(p['status'])+"""' and ts.`status`='ACTIVE'
		GROUP BY tr.resolution_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_resolution_list', methods=['GET', 'POST'])
@login_required
def get_resolution_list():
	try:
		sel="""	
			select *
			from tbl_resolution
		"""
		return jsonify(pyread(sel))
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/view_resolution', methods=['GET','POST'])
@login_required
def view_resolution():
	sel="""
		select * ,
		(CASE 
			WHEN tr.`status` = 1 THEN "Propose Resolution"
			WHEN tr.`status` = 2 THEN "2nd Reading Resolution"
			WHEN tr.`status` = 3 THEN "3rd Reading Resolution"
			WHEN tr.`status` = 4 THEN "3rd Reading Resolution Excemption"
			WHEN tr.`status` = 5 THEN "For Mayor's Approval"
			WHEN tr.`status` = 6 THEN "Approved Resolution"
			WHEN tr.`status` = 7 THEN "Veto Resolution"
			WHEN tr.`status` = 8 THEN "Archive Resolution"
		    ELSE "No status"
		END) stats, tcg.title category_title, tc.committee_id committee_ids, group_concat(tcrf.committee_id) as ref_committee
		from tbl_resolution tr
		left join tbl_category tcg on tcg.category_id=tr.category
		left join tbl_committee_ref_resolution tcrf on tcrf.resolution_id=tr.resolution_id
		left join tbl_committee tc on tc.committee_id=tcrf.committee_id
		left join tbl_resolution_file_committee trfc on trfc.resolution_id=tr.resolution_id
		left join tbl_sp ts on ts.sp_id=tr.sp_id
		left join tbl_committee tc2 on tc2.sp_id=ts.sp_id where ts.`status`='ACTIVE'
		GROUP BY tr.resolution_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_member_allocation', methods=['GET', 'POST'])
@login_required
def save_member_allocation():
	p=json.loads(request.data)
	update="update tbl_sp_budget_balance set  allocation='"+str(p['allocation'])+"' where balance_id ='"+str(p['balance_id'])+"'"
	cud(update)
	return jsonify("Succesfuly Saved")


@query.route('/get_session', methods = ['GET','POST'])
@login_required
def get_session():
	sel="""
		select * from tbl_session ts 
		LEFT JOIN tbl_sp tsp ON tsp.sp_id = ts.sp_number 
		where tsp.`status`='ACTIVE'
		order by session_date desc
	"""
	rd=pyread(sel)
	return jsonify(rd)
  
  
@query.route('/save_gov_classification', methods=['GET', 'POST'])
@login_required
def save_gov_classification():
	p=json.loads(request.data)
	title=p['title'].replace("'","''")
	try:
		if p['h_gov_classification']==0 or p['h_gov_classification']=="0":
			insert="insert into tbl_governance_classification set title='"+str(title)+"'"
			cud(insert)
			return jsonify("Succesfuly Saved")
		else:
			update="update tbl_governance_classification set title='"+str(title)+"' where classification_id='"+str(p['h_gov_classification'])+"'"
			cud(update)
			return jsonify("Succesfuly Updated")
	except Exception as e:
		raise e
	

@query.route('/get_gov_classification', methods=['GET', 'POST'])
@login_required
def get_gov_classification():
	sel="select * from tbl_governance_classification"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_category', methods=['GET', 'POST'])
@login_required
def save_category():
	p=json.loads(request.data)
	title=p['title'].replace("'","''")
	if p['h_category_id']==0 or p['h_category_id']=="0":
		insert="insert into tbl_category set title='"+str(title)+"'"
		cud(insert)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_category set title='"+str(title)+"' where category_id='"+str(p['h_category_id'])+"'"
		cud(update)
		return jsonify("Succesfuly Updated")

@query.route('/get_category', methods=['GET', 'POST'])
@login_required
def get_category():
	sel="select * from tbl_category"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_category', methods=['GET', 'POST'])
@login_required
def del_category():
	p=json.loads(request.data)
	delete="delete from tbl_category where category_id ='"+str(p['category_id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/del_classification', methods=['GET', 'POST'])
@login_required
def del_classification():
	p=json.loads(request.data)
	delete="delete from tbl_governance_classification where classification_id ='"+str(p['classification_id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/save_capital_outlay', methods=['GET', 'POST'])
@login_required
def save_capital_outlay():
	p=json.loads(request.data)
	descr=p['description'].replace("'","''")
	insert_co_added="insert into tbl_capital_outlay_added set amount_added='"+str(p['amount'])+"',description='"+str(descr)+"', added_date=curdate()"
	cud(insert_co_added)
	return jsonify("Succesfuly Added")

@query.route('/save_capital_outlay_deduction', methods=['GET', 'POST'])
@login_required
def save_capital_outlay_deduction():
	p=json.loads(request.data)
	descr=p['description'].replace("'","''")
	insert_co_added="insert into tbl_capital_outlay_deduction set amount_deduction='"+str(p['amount'])+"',description='"+str(descr)+"', deduction_date=curdate()"
	rd_insert_co_added=cud_callbackid(insert_co_added)

	if 'items' in p:
		for i in range(len(p['items'])):
			insert_item="insert into tbl_capital_outlay_deduction_item set item='"+str(p['items'][i])+"', co_deduction_id='"+str(rd_insert_co_added)+"'"
			cud(insert_item)
	return jsonify("Succesfuly Added")


@query.route('/get_capital_outlay', methods=['GET', 'POST'])
@login_required
def get_capital_outlay():
	sel="""
		select COALESCE(COALESCE(sum(amount_added),0)-2nd.amount_deduction,0) balance from tbl_capital_outlay_added,
		(select COALESCE(sum(amount_deduction),0) amount_deduction from tbl_capital_outlay_deduction ) 2nd
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_added_co_details', methods=['GET', 'POST'])
@login_required
def get_added_co_details():
	sel="select * from tbl_capital_outlay_added"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_deduction_co_details', methods=['GET', 'POST'])
@login_required
def get_deduction_co_details():
	sel="""
		select * from tbl_capital_outlay_deduction
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_deduction_items', methods=['GET', 'POST'])
@login_required
def get_deduction_items():
	p=json.loads(request.data)
	sel="""
		select * from tbl_capital_outlay_deduction_item 
		where co_deduction_id='"""+str(p['co_deduction_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_sp_budget_balance', methods=['GET', 'POST'])
@login_required
def get_sp_budget_balance():
	p=json.loads(request.data)
	sel="""
		select *,history_allocation allocations,tsbbe.deduction,tsbbe.history_allocation-tsbbe.deduction remaining_balance 
		from tbl_sp_budget_balance_expenses tsbbe
		left join tbl_sp_budget_balance tsbb on tsbb.balance_id=tsbbe.balance_id
		where tsbbe.balance_id='"""+str(p['balance_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		return jsonify(rd)
	else:
		sel="select *,allocation allocations,balance_id balance_expenses_id,expenses deduction,balance remaining_balance,'' description from tbl_sp_budget_balance where balance_id='"+str(p['balance_id'])+"'"
		rd=pyread(sel)
		return jsonify(rd)


@query.route('/del_added_capital_outlay', methods=['GET', 'POST'])
@login_required
def del_added_capital_outlay():
	p=json.loads(request.data)
	delete="delete from tbl_capital_outlay_added where co_added_id='"+str(p['co_added_id'])+"'"
	cud(delete)
	return jsonify('Succesfuly Deleted')


@query.route('/del_deduction_capital_outlay', methods=['GET', 'POST'])
@login_required
def del_deduction_capital_outlay():
	p=json.loads(request.data)
	delete="delete from tbl_capital_outlay_deduction where co_deduction_id='"+str(p['co_deduction_id'])+"'"
	cud(delete)
	return jsonify('Succesfuly Deleted')



@query.route('/get_sp_mem_remaining_bal', methods=['GET', 'POST'])
@login_required
def get_sp_mem_remaining_bal():
	p=json.loads(request.data)
	sel="""
		select max(balance_expenses_id) remaining_balance_id from tbl_sp_budget_balance_expenses
		where balance_id='"""+str(p['balance_id'])+"""'
	"""
	rd=pyread(sel)
	if rd[0]['remaining_balance_id']==None:
		sel="""
			select allocation remaining_balance,balance deduction from tbl_sp_budget_balance where balance_id='"""+str(p['balance_id'])+"""'
		"""
		rd=pyread(sel)
	else:
		select ="select history_allocation remaining_balance,deduction from tbl_sp_budget_balance_expenses where balance_expenses_id ='"+str(rd[0]['remaining_balance_id'])+"'"
		rd=pyread(select)
	return jsonify(rd)

@query.route('/save_deduction_sp_member', methods=['GET', 'POST'])
@login_required
def save_deduction_sp_member():
	p=json.loads(request.data)
	if p['balance_expenses_id']=="0" or p['balance_expenses_id']==0:
		descr=p['description'].replace("'","''")
		insert="insert into tbl_sp_budget_balance_expenses set deduction='"+str(p['deduction'])+"', balance_id='"+str(p['balance_id'])+"', description='"+str(descr)+"', date_deduction=curdate() ,history_allocation='"+str(p['history_allocation'])+"'"
		cud(insert)
		return jsonify("Succesfuly Saved")
	else:
		descr=p['description'].replace("'","''")
		update="update tbl_sp_budget_balance_expenses set deduction='"+str(p['deduction'])+"', balance_id='"+str(p['balance_id'])+"', description='"+str(descr)+"', date_deduction=curdate() ,history_allocation='"+str(p['history_allocation'])+"' where balance_expenses_id='"+str(p['balance_expenses_id'])+"'"
		cud(update)
		return jsonify("Updated Saved")


@query.route('/get_petition', methods=['GET', 'POST'])
@login_required
def get_petition():
	sel="""
		select *, tcrp.committee_id committee_ids from tbl_petition tp
		left join tbl_committee_ref_petition tcrp on tcrp.petition_id=tp.petition_id
		left join tbl_committee tc on tc.committee_id=tcrp.committee_id
		left join tbl_sp ts on ts.sp_id=tp.sp_id where ts.`status`='ACTIVE'
		GROUP BY tp.petition_id 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_petition_list', methods=['GET', 'POST'])
@login_required
def get_petition_list():
	sel="select * from tbl_petition"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_petition', methods=['GET', 'POST'])
@login_required
def del_petition():
	p=json.loads(request.data)
	delete="delete from tbl_petition where petition_id='"+str(p['petition_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_files" / str(p['petition_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/del_resolution_file_attach', methods=['GET', 'POST'])
@login_required
def del_resolution_file_attach():
	p=json.loads(request.data)
	delete="delete from tbl_resolution_file where resolution_file_id='"+str(p['resolution_file_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution" / str(p['resolution_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/delete_petition_file', methods=['GET', 'POST'])
@login_required
def delete_petition_file():
	p=json.loads(request.data)
	sel="select * from tbl_petition_path where petition_id='"+str(p['petition_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_petition_path where petition_path_id='"+str(p['petition_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_petition_path where petition_path_id='"+str(p['petition_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/del_document_referals_file', methods=['GET', 'POST'])
@login_required
def del_document_referals_file():
	p=json.loads(request.data)
	sel="select * from tbl_documents_refferals_path where documents_refferals_id='"+str(p['documents_refferals_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_documents_refferals_path where documents_refferals_path_id='"+str(p['documents_refferals_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_documents_refferals_path where documents_refferals_path_id='"+str(p['documents_refferals_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")



@query.route('/del_barangay_ordinance_file', methods=['GET', 'POST'])
@login_required
def del_barangay_ordinance_file():
	p=json.loads(request.data)
	sel="select * from tbl_barangay_ordinance_path where barangay_ordinance_id='"+str(p['barangay_ordinance_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_barangay_ordinance_path where barangay_ordinance_path_id='"+str(p['barangay_ordinance_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_barangay_ordinance_path where barangay_ordinance_path_id='"+str(p['barangay_ordinance_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/del_barangay_resolution_file', methods=['GET', 'POST'])
@login_required
def del_barangay_resolution_file():
	p=json.loads(request.data)
	sel="select * from tbl_barangay_resolution_path where barangay_resolution_id='"+str(p['barangay_resolution_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_barangay_resolution_path where barangay_resolution_path_id='"+str(p['barangay_resolution_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_barangay_resolution_path where barangay_resolution_path_id='"+str(p['barangay_resolution_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")



@query.route('/del_executive_order_file', methods=['GET', 'POST'])
@login_required
def del_executive_order_file():
	p=json.loads(request.data)
	sel="select * from tbl_executive_order_path where executive_order_id='"+str(p['executive_order_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_executive_order_path where executive_order_path_id='"+str(p['executive_order_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_executive_order_path where executive_order_path_id='"+str(p['executive_order_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/del_memorandom_file', methods=['GET', 'POST'])
@login_required
def del_memorandom_file():
	p=json.loads(request.data)
	sel="select * from tbl_memorandom_path where memorandom_id='"+str(p['memorandom_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_memorandom_path where memorandom_path_id='"+str(p['memorandom_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_memorandom_path where memorandom_path_id='"+str(p['memorandom_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")

@query.route('/get_petition_path2', methods=['GET', 'POST'])
@login_required
def get_petition_path2():
	p=json.loads(request.data)
	sel="select * from tbl_petition_path where petition_id='"+str(p['petition_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_documents_refferals', methods=['GET', 'POST'])
@login_required
def del_documents_refferals():
	p=json.loads(request.data)
	delete="delete from tbl_documents_refferals where documents_refferals_id='"+str(p['document_referal_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_document_referals" / str(p['document_referal_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/del_barangay_ordinance', methods=['GET', 'POST'])
@login_required
def del_barangay_ordinance():
	p=json.loads(request.data)
	delete="delete from tbl_barangay_ordinance where barangay_ordinance_id='"+str(p['barangay_ordinance_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_barangay_ordinance" / str(p['barangay_ordinance_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/del_barangay_resolution', methods=['GET', 'POST'])
@login_required
def del_barangay_resolution():
	p=json.loads(request.data)
	delete="delete from tbl_barangay_resolution where barangay_resolution_id='"+str(p['barangay_resolution_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_barangay_resolution" / str(p['barangay_resolution_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/del_executive_order', methods=['GET', 'POST'])
@login_required
def del_executive_order():
	p=json.loads(request.data)
	delete="delete from tbl_executive_order where executive_order_id='"+str(p['executive_order_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_executive_order" / str(p['executive_order_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")

@query.route('/del_memorandom', methods=['GET', 'POST'])
@login_required
def del_memorandom():
	p=json.loads(request.data)
	delete="delete from tbl_memorandom where memorandom_id='"+str(p['memorandom_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_memorandom" / str(p['memorandom_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/save_petition_ref_committee', methods=['GET','POST'])
@login_required
def save_petition_ref_committee():
	p=json.loads(request.data)
	insert_ref_petition="""
		insert into tbl_committee_ref_petition set committee_id='"""+str(p['committee_id'])+"""',
		petition_id='"""+str(p['petition_id_main'])+"""', date_reffered=now()
	"""
	cud(insert_ref_petition)
	return jsonify("Succesfuly Saved")


@query.route('/get_committee_petition', methods=['GET', 'POST'])
@login_required
def get_committee_petition():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition tp
		left join tbl_committee_ref_petition tcrp on tcrp.petition_id=tp.petition_id
		where tcrp.committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_petition_committee', methods=['GET', 'POST'])
@login_required
def get_petition_committee():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition tp
		where petition_id='"""+str(p['petition_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_ordinance_committee', methods=['GET', 'POST'])
@login_required
def save_ordinance_committee():
	p=json.loads(request.data)
	insert_committee="insert into tbl_committee_ref_ordinance set  committee_id='"+str(p['committee_id'])+"', ordinance_id='"+str(p['ordinance_id'])+"', date_reffered=now()"
	cud(insert_committee)
	return jsonify("Succesfuly Saved")


@query.route('/save_ordinance', methods=['GET', 'POST'])
@login_required
def save_ordinance():
	p=request.form
	p=json.loads(p['Serialized'])

	descr=p['description'].replace("'","''")
	ordinance_title=p['ordinance_title'].replace("'","''")
	minutes_title=p['minutes_title'].replace("'","''")

	new_lst=(','.join(p['ref_committee'][0]))

	if 'committee_id' in p:
		pass
	else:
		p['committee_id']=0

	if 'category' not in p:
		p['category']=''
	if 'gov_classification' not in p:
		p['gov_classification']=''
	if 'source_of_document' not in p:
		p['source_of_document']=''

	if p['sp_id']=='':
		sel_sp ="select sp_id from tbl_sp where `status`='ACTIVE'"
		r_sp_id=pyread(sel_sp)
		p['sp_id']=r_sp_id[0]['sp_id']

	if p['ordinance_id']=="0" or p['ordinance_id']==0:
		sel_if_exst_ord_no="select count(*) count_ord_num from tbl_ordinance where ordinance_number='"+str(p['ordinance_no'])+"'"
		rd_count=pyread(sel_if_exst_ord_no)

		categories = str(p['categories'][0]).replace("'",'').replace("[","").replace("]","").replace(" ", "")
 
		if rd_count[0]['count_ord_num']==0:
			insert="""
				insert into tbl_ordinance set ordinance_title='"""+str(ordinance_title)+"""', ordinance_number='"""+str(p['ordinance_no'])+"""',
				date_enacted='"""+str(p['date_enacted'])+"""', category='"""+str(categories)+"""', sp_id='"""+str(p['sp_id'])+"""',
				session_id='"""+str(p['session_id'])+"""', tracking_number='"""+str(p['tracking_no'])+"""',
				classification_id='"""+str(p['gov_classification'])+"""', source_of_document='"""+str(p['source_of_document'])+"""', 
				source_document_specify='"""+str(p['source_document_specify'])+"""', `status`='"""+str(p['status_ordinance'])+"""',
				remarks='"""+str(p['remarks'])+"""', description='"""+str(descr)+"""', series_number='"""+str(p['series_number'])+"""',
				type_ord='"""+str(p['type_ord'])+"""'
			"""
			rd=cud_callbackid(insert)

			insert2="""
				insert into tbl_ordinance_status_numbers set original='"""+str(p['original'])+"""',
				ammended_no='"""+str(p['ammended_no'])+"""', repealed_no='"""+str(p['repealed_no'])+"""', 
				superseded_no='"""+str(p['superseded_no'])+"""', missing_ord='"""+str(p['missing_ord'])+"""',
				ordinance_id='"""+str(rd)+"""'
			"""
			cud(insert2)

			if p['ref_committee'][0]:
				for i in p['ref_committee'][0]:
					insert_committee="insert into tbl_committee_ref_ordinance set  committee_id='"+str(i)+"', ordinance_id='"+str(rd)+"', date_reffered=now()"
					cud(insert_committee)

			if 'input_authors' in p:
				for i in p['input_authors']:
					insert_author="insert into tbl_ordinance_author set author='"+str(i)+"', ordinance_id='"+str(rd)+"'"
					cud(insert_author)

			if 'input_co_authors' in p:
				for i in p['input_co_authors']:
					insert_co_author="insert into tbl_ordinance_co_author set co_author='"+str(i)+"', ordinance_id='"+str(rd)+"'"
					cud(insert_co_author)

			if 'input_sponsor' in p:
				for i in p['input_sponsor']:
					insert_sponsor="insert into tbl_ordinance_sponsor set sponsor='"+str(i)+"', ordinance_id='"+str(rd)+"'"
					cud(insert_sponsor)
			x=-1
			y=-1
			z=-1

			for filename_array in request.files:
				split=filename_array.split("[")
				if str(split[0])=="file_attach":
					x=x+1
					file_name="file_attach["+str(x)+"]"
					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_ordinance_files" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_ordinance_files//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename.replace("'","")
						path_location=location.replace("/", "\\\\");
						
						insert2="insert into tbl_ordinance_file set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', ordinance_id='"+str(rd)+"'"
						cud(insert2)
						

					# file committee na ni  ---------------------------------->

				if str(split[0])=="file_committee_ref":
					y=y+1
					file_name_min="file_committee_ref["+str(y)+"]"

					file=request.files[file_name_min]
					n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_files" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_committee_ordinance_files//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename.replace("'","")
						path_location=location.replace("/", "\\\\");

						insert2="insert into tbl_ordinance_file_committee set path='"+str(path_location)+"' , filename='"+str(file.filename.replace("'",""))+"' , ordinance_id='"+str(rd)+"', committee_id='"+str(new_lst)+"'"
						cud(insert2)

				if str(split[0])=="file_veto":
					z=z+1
					file_name_min="file_veto["+str(z)+"]"

					file=request.files[file_name_min]
					n_path = Path(__file__).parent / "../static/uploads/upload_veto_ordinance" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_veto_ordinance//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename.replace("'","")
						path_location=location.replace("/", "\\\\");

						insert_veto="insert into tbl_veto_ordinance set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', ordinance_id='"+str(rd)+"'"
						cud(insert_veto)

			sel_ord="select * from tbl_ordinance where ordinance_id='"+str(rd)+"'"
			rd_ordinance=pyread(sel_ord)

			if p['status_ordinance']=="1":
				doc_status = "Propose Ordinance"
			elif p['status_ordinance']=="2":
				doc_status = "2nd Reading Ordinance"
			elif p['status_ordinance']=="3":
				doc_status = "3rd Reading Ordinance"
			elif p['status_ordinance']=="4":
				doc_status = "3rd Reading Ordinance Excemption"
			elif p['status_ordinance']=="5":
				doc_status = "For mayors Approval"
			elif p['status_ordinance']=="6":
				doc_status = "Approved Ordinance"
			elif p['status_ordinance']=="7":
				doc_status = "Veto Ordinance"
			elif p['status_ordinance']=="8":
				doc_status = "Archive Ordinance"

			if p['tracking_no']:
				select_tracking = """
					select track_gen_id from tbl_document_tracking where tracking_no='"""+str(p['tracking_no'])+"""',
				"""
				rd_sel_tracking = pyread(select_tracking)

				if rd_sel_tracking:
					insert_tracking_status = """
						insert into tbl_document_tracking_status  set track_gen_id='"""+str(rd_sel_tracking[0]['track_gen_id'])+"""', status='Approved', date=now()
					"""
					cud(insert_tracking_status)

			return jsonify("Succesfuly Saved")

		else:
			return jsonify("Ordinance Number Already exists")
	else:
		sel_if_exst_ord_no="""
			select count(*) count_ord_num from tbl_ordinance 
			where ordinance_number='"""+str(p['ordinance_no'])+"""' and 
			ordinance_id!='"""+str(p['ordinance_id'])+"""'
		"""
		rd_count=pyread(sel_if_exst_ord_no)

		# if rd_count[0]['count_ord_num']==0:
			
		# else:
		# 	return jsonify("Ordinance Number Already exists")

		categories = str(p['categories'][0]).replace("'","").replace("[","").replace("]","").replace(" ", "")

		update="""
			update tbl_ordinance set ordinance_title='"""+str(ordinance_title)+"""', ordinance_number='"""+str(p['ordinance_no'])+"""',
			date_enacted='"""+str(p['date_enacted'])+"""',category='"""+str(categories)+"""', sp_id='"""+str(p['sp_id'])+"""',
			session_id='"""+str(p['session_id'])+"""',tracking_number='"""+str(p['tracking_no'])+"""',
			classification_id='"""+str(p['gov_classification'])+"""', source_of_document='"""+str(p['source_of_document'])+"""', 
			source_document_specify='"""+str(p['source_document_specify'])+"""', `status`='"""+str(p['status_ordinance'])+"""',
			remarks='"""+str(p['remarks'])+"""', description='"""+str(descr)+"""',series_number='"""+str(p['series_number'])+"""',
			type_ord='"""+str(p['type_ord'])+"""'
			where ordinance_id='"""+str(p['ordinance_id'])+"""'
		"""
		cud(update)

		update2="""
			update tbl_ordinance_status_numbers set original='"""+str(p['original'])+"""',
			ammended_no='"""+str(p['ammended_no'])+"""', repealed_no='"""+str(p['repealed_no'])+"""', 
			superseded_no='"""+str(p['superseded_no'])+"""', missing_ord='"""+str(p['missing_ord'])+"""'
			where ordinance_id='"""+str(p['ordinance_id'])+"""'
		"""
		cud(update2)


		delete_committee="delete from tbl_committee_ref_ordinance where ordinance_id='"+str(p['ordinance_id'])+"'"
		cud(delete_committee)

		for i in p['ref_committee'][0]:
			insert_committee="insert into tbl_committee_ref_ordinance set  committee_id='"+str(i)+"', ordinance_id='"+str(p['ordinance_id'])+"', date_reffered=now()"
			cud(insert_committee)


		delete_authors="delete from tbl_ordinance_author where ordinance_id='"+str(p['ordinance_id'])+"'"
		cud(delete_authors)

		delete_co_authors="delete from tbl_ordinance_co_author where ordinance_id='"+str(p['ordinance_id'])+"'"
		cud(delete_co_authors)

		delete_sponsor="delete from tbl_ordinance_sponsor where ordinance_id='"+str(p['ordinance_id'])+"'"
		cud(delete_sponsor)

		if 'input_authors' in p:
			for i in p['input_authors']:
				insert_author="insert into tbl_ordinance_author set author='"+str(i)+"', ordinance_id='"+str(p['ordinance_id'])+"'"
				cud(insert_author)

		if 'input_co_authors' in p:
			for i in p['input_co_authors']:
				insert_co_author="insert into tbl_ordinance_co_author set co_author='"+str(i)+"', ordinance_id='"+str(p['ordinance_id'])+"'"
				cud(insert_co_author)

		if 'input_sponsor' in p:
			for i in p['input_sponsor']:
				insert_sponsor="insert into tbl_ordinance_sponsor set sponsor='"+str(i)+"', ordinance_id='"+str(p['ordinance_id'])+"'"
				cud(insert_sponsor)
		x=-1
		y=-1
		z=-1

		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_files_committee_reports" / str(p['ordinance_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_ordinance_files//"+str(p['ordinance_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename.replace("'","")
					path_location=location.replace("/", "\\\\");
					
					insert2="insert into tbl_ordinance_file set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', ordinance_id='"+str(p['ordinance_id'])+"'"
					cud(insert2)
					

				# file committee_ref  ---------------------------------->

			if str(split[0])=="file_committee_ref":
				y=y+1
				file_name_min="file_committee_ref["+str(y)+"]"

				file=request.files[file_name_min]
				n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_files" / str(p['ordinance_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_ordinance_files//"+str(p['ordinance_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					insert2="insert into tbl_ordinance_file_committee set path='"+str(path_location)+"' , filename='"+str(file.filename.replace("'",""))+"' , ordinance_id='"+str(p['ordinance_id'])+"', committee_id='"+str(new_lst)+"'"
					cud(insert2)

			if str(split[0])=="file_veto":
				z=z+1
				file_name_min="file_veto["+str(z)+"]"

				file=request.files[file_name_min]
				n_path = Path(__file__).parent / "../static/uploads/upload_veto_ordinance" / str(p['ordinance_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_veto_ordinance//"+str(p['ordinance_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");

					insert_veto="insert into tbl_veto_ordinance set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', ordinance_id='"+str(p['ordinance_id'])+"'"
					cud(insert_veto)

		sel_ord="select * from tbl_ordinance where ordinance_id='"+str(p['ordinance_id'])+"'"
		rd_ordinance=pyread(sel_ord)

		if p['status_ordinance']=="1":
			doc_status = "Propose Ordinance"
		elif p['status_ordinance']=="2":
			doc_status = "2nd Reading Ordinance"
		elif p['status_ordinance']=="3":
			doc_status = "3rd Reading Ordinance"
		elif p['status_ordinance']=="4":
			doc_status = "3rd Reading Ordinance Excemption"
		elif p['status_ordinance']=="5":
			doc_status = "For mayors Approval"
		elif p['status_ordinance']=="6":
			doc_status = "Approved Ordinance"
		elif p['status_ordinance']=="7":
			doc_status = "Veto Ordinance"
		elif p['status_ordinance']=="8":
			doc_status = "Archive Ordinance"

		if p['tracking_no']:
			select_tracking = """
				select track_gen_id from tbl_document_tracking where tracking_no='"""+str(p['tracking_no'])+"""',
			"""
			rd_sel_tracking = pyread(select_tracking)

			insert_tracking_status = """
				insert into tbl_document_tracking_status  set track_gen_id='"""+str(rd_sel_tracking[0]['track_gen_id'])+"""', status='Approved', date=now()
			"""
			cud(insert_tracking_status)

		return jsonify("Succesfuly Updated")


@query.route('/get_petition_doc', methods=['GET', 'POST'])
@login_required
def get_petition_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition_path tpp
		where petition_id='"""+str(p['petition_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)
	

@query.route('/get_documents_refferals_doc', methods=['GET', 'POST'])
@login_required
def get_documents_refferals_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_documents_refferals_path tdrp
		
		where documents_refferals_id='"""+str(p['documents_refferals_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_barangay_ordinance_doc', methods=['GET', 'POST'])
@login_required
def get_barangay_ordinance_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_barangay_ordinance_path tbop
		where barangay_ordinance_id='"""+str(p['barangay_ordinance_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_barangay_resolution_doc', methods=['GET', 'POST'])
@login_required
def get_barangay_resolution_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_barangay_resolution_path tbrp
		where barangay_resolution_id='"""+str(p['barangay_resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_executive_order_doc', methods=['GET', 'POST'])
@login_required
def get_executive_order_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_executive_order_path teop
		where executive_order_id='"""+str(p['executive_order_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_memorandom_doc', methods=['GET', 'POST'])
@login_required
def get_memorandom_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_memorandom_path tmp
		where memorandom_id='"""+str(p['memorandom_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_petition_path_id', methods=['GET', 'POST'])
@login_required
def get_petition_path_id():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition_path 
		where petition_id='"""+str(p['petition_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_session_', methods=['GET','POST'])
@login_required
def save_session_():
	p=request.form
	p=json.loads(p['data'])

	intro_path = None
	national_anthem_path = None
	prayer_path = None
	recitation_path = None
	privilege_path = None

	remarks = p['session_number'] + " " +p['sp_type'] + " SESSION"

	if p['session_id']==0 or p['session_id']=='0':
		check_session = """
			select count(*) counter from tbl_session where session_number ='"""+str(p['session_number'])+"""'
		"""
		rd = pyread(check_session)

		if rd[0]['counter']==0:
			ins = """insert into tbl_session set 
				session_number ='"""+str(p['session_number'])+"""',
				session_date ='"""+str(p['session_date'])+"""',
				session_opening_prayer='"""+str(p['opening_prayer'])+"""',
				recitation_coun_creed='"""+str(p['couns_creed'])+"""',
				national_anthem='"""+str(p['national_anthem'])+"""',
				closing_prayer='"""+str(p['closing_prayer_lead'])+"""',
				sp_number='"""+str(p['sp_number'])+"""',
				session_type='"""+str(p['sp_type'])+"""'
			"""
			ses_id = cud_callbackid(ins)

			if ses_id != 0:
				if len(p['attendance'])!=0:
					for x in p['attendance']:
						ins_rc = "insert into tbl_session_roll_call set info_id ='"+str(x['info_id'])+"', session_id = '"+str(ses_id)+"', status = '"+str(x['status'])+"'"
						cud(ins_rc)

				if "reading_consid_prev_min" in p:
					for x in p['reading_consid_prev_min']:
						insert_reading_minutes = """
							insert into tbl_session_reading_minutes set session_id='"""+str(ses_id)+"""', minutes_id='"""+str(x['minutes_id'])+"""'
						"""
						cud(insert_reading_minutes)

				if "propose_ord" in p:
					for x in p['propose_ord']:
						insert_p_ref = """
							insert into tbl_session_proposed_ordi set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "propose_reso" in p:
					for x in p['propose_reso']:
						insert_p_ref = """
							insert into tbl_session_proposed_reso set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "petitions_for_refferals" in p:
					for x in p['petitions_for_refferals']:
						print("3")
						prnt_G(x)
						insert_p_ref = """
							insert into tbl_session_petition_for_refferal set session_id='"""+str(ses_id)+"""', type='"""+str(x['type'])+"""' , tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "additional_refferals" in p:
					for x in p['additional_refferals']:
						print("2")
						prnt_G(x)
						insert_p_ref = """
							insert into tbl_session_additional_refferal set session_id='"""+str(ses_id)+"""', type='"""+str(x['type'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "veto_message" in p:
					for x in p['veto_message']:
						print("1")
						insert_p_ref = """
							insert into tbl_session_veto_reading set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "committee_report" in p:
					for x in p['committee_report']:
						insert_p_ref = """
							insert into tbl_session_committee_report set session_id='"""+str(ses_id)+"""', committee_report_no='"""+str(x['committee_report_no'])+"""', 
							committee_id='"""+str(x['committee_id'])+"""'
						"""
						cud(insert_p_ref)

				if "committee_information" in p:
					for x in p['committee_information']:
						insert_p_ref = """
							insert into tbl_session_committee_information set session_id='"""+str(ses_id)+"""', committee_information_no='"""+str(x['committee_information_no'])+"""', 
							committee_id='"""+str(x['committee_id'])+"""'
						"""
						cud(insert_p_ref)

				if "unfinished_bussiness" in p:
					for x in p['unfinished_bussiness']:
						insert_p_ref = """
							insert into tbl_session_unfinished_bussiness set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

				if "bussiness_of_the_day" in p:
					for x in p['bussiness_of_the_day']:
						insert_p_ref = """
							insert into tbl_session_botd set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)
				
				if "urgent" in p:
					for x in p['urgent']:
						prnt_G(x)
						insert_p_ref = """
							insert into tbl_session_urgent set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						update_tracking = """
							update tbl_document_tracking set action_taken=2 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "just_inserted" in p:
					for x in p['just_inserted']:
						prnt_W(x)
						insert_p_ref = """
							insert into tbl_session_just_inserted set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						update_tracking = """
							update tbl_document_tracking set action_taken=2 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

				if "calendar_measure" in p:
					for x in p['calendar_measure']:
						prnt_Y(x)
						insert_p_ref = """
							insert into tbl_session_calendar_measure set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						update_tracking = """
							update tbl_document_tracking set action_taken=3 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='EXCEPTED FROM THREE READING RULE', date=now(),
							remarks = 'EXCEPTED FROM THREE READING RULE'
						"""
						cud(insert_tracking_status)

				if "new_measure" in p:
					for x in p['new_measure']:
						insert_p_ref = """
							insert into tbl_session_new_measure set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

						update_tracking = """
							update tbl_document_tracking set action_taken=3 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='EXCEPTED FROM THREE READING RULE', date=now(),
							remarks = 'EXCEPTED FROM THREE READING RULE'
						"""
						cud(insert_tracking_status)

				if "bussiness_third" in p:
					for x in p['bussiness_third']:
						insert_p_ref = """
							insert into tbl_session_bussiness_third set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_p_ref)

				if "summary" in p:
					for x in p['summary']:
						insert_p_ref = """
							insert into tbl_session_summary_correction set session_id='"""+str(ses_id)+"""', tracking_no='"""+str(x['tracking_no'])+"""',
							new_title='"""+str(x['new_title'])+"""' , old_title = '"""+str(x['old_title'])+"""'
						"""
						cud(insert_p_ref)

				# NO file -- still seeking solution

				if "question_hour" in p:
					for x in p['question_hour']:
						insert_question = """
							insert into tbl_session_question_hour set fullname='"""+str(x['fullname'])+"""', designation='"""+str(x['designation'])+"""', office='"""+str(x['office'])+"""',
							subject='"""+str(x['subject'])+"""', session_id='"""+str(ses_id)+"""'
						"""
						cud(insert_question)

				if 'privilege_hour'in p:
					for x in p['privilege_hour']:
						insert_privilege = """
							insert into tbl_session_previlege_hour set councilor_info_id='"""+str(x['info_id'])+"""', session_id='"""+str(ses_id)+"""'
						"""
						cud(insert_privilege)

				if 'announcement_'in p:
					for x in p['announcement_']:
						insert_announcement = """
							insert into tbl_session_announcement set councilor='"""+str(x['info_id'])+"""', session_id='"""+str(ses_id)+"""',
							announcement='"""+str(x['announcement'])+"""'
						"""
						cud(insert_announcement)
		
		else:
			return jsonify("session number already exists")
		
	else:
		ins = """
			update tbl_session set 
			session_number ='"""+str(p['session_number'])+"""',
			session_date ='"""+str(p['session_date'])+"""',
			session_opening_prayer='"""+str(p['opening_prayer'])+"""',
			recitation_coun_creed='"""+str(p['couns_creed'])+"""',
			national_anthem='"""+str(p['national_anthem'])+"""',
			closing_prayer='"""+str(p['closing_prayer_lead'])+"""',
			sp_number='"""+str(p['sp_number'])+"""',
			session_type='"""+str(p['sp_type'])+"""'
			where session_id = '"""+str(p['session_id'])+"""' 
		"""
		cud(ins)

		if p['attendance']:
			del_q =	"delete from tbl_session_roll_call where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			
			if len(p['attendance'])!=0:
				for x in p['attendance']:
					if x:
						ins_rc = "insert into tbl_session_roll_call set info_id ='"+str(x['info_id'])+"', session_id = '"+str(p['session_id'])+"', status = '"+str(x['status'])+"'"
						cud(ins_rc)

		if "reading_consid_prev_min" in p:
			del_q =	"delete from tbl_session_reading_minutes where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)

			for x in p['reading_consid_prev_min']:
				if x:
					insert_reading_minutes = """
						insert into tbl_session_reading_minutes set session_id='"""+str(p['session_id'])+"""', minutes_id='"""+str(x['minutes_id'])+"""'
					"""
					cud(insert_reading_minutes)

		if "propose_ord" in p:
			del_q =	"delete from tbl_session_proposed_ordi where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['propose_ord']:
				if x:
					insert_p_ref = """
						insert into tbl_session_proposed_ordi set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

		if "propose_reso" in p:
			del_q =	"delete from tbl_session_proposed_reso where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['propose_reso']:
				if x:
					insert_p_ref = """
						insert into tbl_session_proposed_reso set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

		if "petitions_for_refferals" in p:
			del_q =	"delete from tbl_session_petition_for_refferal where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['petitions_for_refferals']:
				if x:
					insert_p_ref = """
						insert into tbl_session_petition_for_refferal set session_id='"""+str(p['session_id'])+"""', type="""+str(x['type'])+""", tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					del_q =	"delete from tbl_document_tracking_refferal where track_gen_id = '"+str(x['tracking_no'])+"' "
					cud(del_q)

					if 'committee_id' in x:
						committees= ", ".join( repr(e) for e in x['committee_id']).replace("'","")
						insert_committee = """
							insert into tbl_document_tracking_refferal set committtee='"""+str(committees)+"""', track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_committee)

		if "additional_refferals" in p:
			del_q =	"delete from tbl_session_additional_refferal where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['additional_refferals']:
				if x:
					insert_p_ref = """
						insert into tbl_session_additional_refferal set session_id='"""+str(p['session_id'])+"""', type="""+str(x['type'])+""", tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					del_q =	"delete from tbl_document_tracking_refferal where track_gen_id = '"+str(x['tracking_no'])+"' "
					cud(del_q)

					if 'committee_id' in x:
						committees= ", ".join( repr(e) for e in x['committee_id']).replace("'","")
						insert_committee = """
							insert into tbl_document_tracking_refferal set committtee='"""+str(committees)+"""', track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(insert_committee)

		if "veto_message" in p:
			del_q =	"delete from tbl_session_veto_reading where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['veto_message']:
				insert_p_ref = """
					insert into tbl_session_veto_reading set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
				"""
				cud(insert_p_ref)

		if "committee_report" in p:
			del_q =	"delete from tbl_session_committee_report where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['committee_report']:
				if x:
					insert_p_ref = """
						insert into tbl_session_committee_report set session_id='"""+str(p['session_id'])+"""', committee_report_no='"""+str(x['committee_report_no'])+"""', 
						committee_id='"""+str(x['committee_id'])+"""'
					"""
					cud(insert_p_ref)
		
		if "committee_information" in p:
			del_q =	"delete from tbl_session_committee_information where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['committee_information']:
				if x:
					insert_p_ref = """
						insert into tbl_session_committee_information set session_id='"""+str(p['session_id'])+"""', committee_information_no='"""+str(x['committee_information_no'])+"""', 
						
					"""
					# committee_id='"""+str(x['committee_id'])+"""'
					cud(insert_p_ref)

		if "unfinished_bussiness" in p:
			del_q =	"delete from tbl_session_unfinished_bussiness where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['unfinished_bussiness']:
				if x:
					insert_p_ref = """
						insert into tbl_session_unfinished_bussiness set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

		if "bussiness_of_the_day" in p:
			del_q =	"delete from tbl_session_botd where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['bussiness_of_the_day']:
				if x:
					insert_p_ref = """
						insert into tbl_session_botd set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

		if "urgent" in p:
			del_q =	"delete from tbl_session_urgent where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['urgent']:
				if x:
					insert_p_ref = """
						insert into tbl_session_urgent set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					sel= """
						select * from tbl_document_tracking_status where track_gen_id='"""+str(x['tracking_no'])+"""'
					"""
					rd = pyread(sel)

					if len(rd)==0:
						update_tracking = """
							update tbl_document_tracking set action_taken=2 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

		if "just_inserted" in p:
			del_q =	"delete from tbl_session_just_inserted where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['just_inserted']:
				if x:
					insert_p_ref = """
						insert into tbl_session_just_inserted set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					sel= """
						select * from tbl_document_tracking_status where track_gen_id='"""+str(x['tracking_no'])+"""'
					"""
					rd = pyread(sel)

					if len(rd)==0:
						update_tracking = """
							update tbl_document_tracking set action_taken=2 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

		if "calendar_measure" in p:
			del_q =	"delete from tbl_session_calendar_measure where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['calendar_measure']:
				if x:
					insert_p_ref = """
						insert into tbl_session_calendar_measure set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					sel= """
						select * from tbl_document_tracking_status where track_gen_id='"""+str(x['tracking_no'])+"""'
					"""
					rd = pyread(sel)

					if len(rd)==0:
						update_tracking = """
							update tbl_document_tracking set action_taken=3 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

		if "new_measure" in p:
			del_q =	"delete from tbl_session_new_measure where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['new_measure']:
				if x:
					insert_p_ref = """
						insert into tbl_session_new_measure set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

					sel= """
						select * from tbl_document_tracking_status where track_gen_id='"""+str(x['tracking_no'])+"""'
					"""
					rd = pyread(sel)

					if len(rd)==0:
						update_tracking = """
							update tbl_document_tracking set action_taken=3 where track_gen_id='"""+str(x['tracking_no'])+"""'
						"""
						cud(update_tracking)

						insert_tracking_status = """
							insert into tbl_document_tracking_status set track_gen_id='"""+str(x['tracking_no'])+"""', status='Calendared', date=now(),
							remarks = '"""+str(remarks)+"""'
						"""
						cud(insert_tracking_status)

		if "bussiness_third" in p:
			del_q =	"delete from tbl_session_bussiness_third where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['bussiness_third']:
				if x:
					insert_p_ref = """
						insert into tbl_session_bussiness_third set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""'
					"""
					cud(insert_p_ref)

		if "summary" in p:
			del_q =	"delete from tbl_session_summary_correction where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['summary']:
				if x:
					insert_p_ref = """
						insert into tbl_session_summary_correction set session_id='"""+str(p['session_id'])+"""', tracking_no='"""+str(x['tracking_no'])+"""',
						new_title='"""+str(x['new_title'])+"""' , old_title = '"""+str(x['old_title'])+"""'
					"""
					cud(insert_p_ref)

		if "question_hour" in p:
			del_q =	"delete from tbl_session_question_hour where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['question_hour']:
				if x:
					insert_question = """
						insert into tbl_session_question_hour set fullname='"""+str(x['fullname'])+"""', designation='"""+str(x['designation'])+"""', office='"""+str(x['office'])+"""',
						subject='"""+str(x['subject'])+"""', session_id='"""+str(p['session_id'])+"""'
					"""
					cud(insert_question)

		if 'privilege_hour'in p:
			del_q =	"delete from tbl_session_previlege_hour where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['privilege_hour']:
				if x:
					insert_privilege = """
						insert into tbl_session_previlege_hour set councilor_info_id='"""+str(x['info_id'])+"""', session_id='"""+str(p['session_id'])+"""'
					"""
					cud(insert_privilege)

		if 'announcement_'in p:
			del_q =	"delete from tbl_session_announcement where session_id = '"+str(p['session_id'])+"' "
			cud(del_q)
			for x in p['announcement_']:
				insert_announcement = """
					insert into tbl_session_announcement set councilor='"""+str(x['info_id'])+"""', session_id='"""+str(p['session_id'])+"""',
					announcement='"""+str(x['announcement'])+"""'
				"""
				cud(insert_announcement)
	
	if p['session_id']==0 or p['session_id']=='0':
		session_id = ses_id
	else:
		session_id = p['session_id']

	for filename_array in request.files:
		file=request.files[filename_array]
		rd=int(round(datetime.now().timestamp()))
		f = filename_array.split("[")[0]

		if f=='intro' or f=='national_anthem' or f=='prayer':
			n_path = Path(__file__).parent / "../static/session_video/"/ str(f) / str(rd)
		else:
			n_path = Path(__file__).parent / "../static/session_files/"/ str(f) / str(rd)
		
		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			if f=='intro' or f=='national_anthem' or f=='prayer':
				location1="session_video/"+ str(f) + "/" + str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\").replace("'","''");
				split_name = str(file.filename).split(".")

				if f=='intro':
					intro_path= path_location.replace("'","''")
				elif f=='national_anthem':
					national_anthem_path = path_location.replace("'","''")
				elif f=='prayer':
					prayer_path = path_location.replace("'","''")
			else:
				location1="session_files/"+ str(f) + "/" + str(rd)
				location1.replace("//", "\\\\");
				location=location1+"//"+filename
				path_location=location.replace("/", "\\\\").replace("'","''");
				split_name = str(file.filename).split(".")

				if f=='recitation_of_councilor':
					insert_files= """
						insert into tbl_session_recitation_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

				elif f=="announcement_file":
					insert_files= """
						insert into tbl_session_announcement_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

				elif f=="question_hour_file":
					insert_files= """
						insert into tbl_session_question_hour_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

				elif f=="privilege_hour_file":
					insert_files= """
						insert into tbl_session_privilege_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

				elif f=="committee_report_file":
					insert_files= """
						insert into tbl_session_committee_report_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

				elif f=="committee_information_file":
					insert_files= """
						insert into tbl_session_committee_information_path set filename='"""+str(file.filename.replace("'","''"))+"""', path='"""+str(path_location)+"""', session_id='"""+str(session_id)+"""'
					"""
					cud(insert_files)

	if p['session_id']==0 or p['session_id']=='0':
		insert_file_path= """
			insert into tbl_session_video set intro_path='"""+str(intro_path)+"""' , national_anthem_path= '"""+str(national_anthem_path)+"""', prayer_path= '"""+str(prayer_path)+"""' , session_id ='"""+str(session_id)+"""'
		"""
		cud(insert_file_path)
	else:
		if intro_path!=None:
			update_file_path= """
				update tbl_session_video set intro_path='"""+str(intro_path)+"""' where session_id ='"""+str(session_id)+"""'
			"""
			cud(update_file_path)
		
		if national_anthem_path!=None:
			update_file_path2= """
				update tbl_session_video set national_anthem_path= '"""+str(national_anthem_path)+"""' where session_id ='"""+str(session_id)+"""'
			"""
			cud(update_file_path2)

		if prayer_path!=None:
			update_file_path3= """
				update tbl_session_video set prayer_path= '"""+str(prayer_path)+"""' where session_id ='"""+str(session_id)+"""'
			"""
			cud(update_file_path3)

	return jsonify("Succesfuly Saved")

@query.route('/get_session_question_hour', methods=['GET', 'POST'])
@login_required
def get_session_question_hour():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_question_hour where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_committee_report', methods=['GET', 'POST'])
@login_required
def get_session_committee_report():
	p=json.loads(request.data)
	sel = """
		select tscr.committee_id, committee, committee_report_no
		from tbl_session_committee_report tscr
		left join tbl_committee tc on tc.committee_id=tscr.committee_id
		where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_committee_information', methods=['GET', 'POST'])
@login_required
def get_session_committee_information():
	p=json.loads(request.data)
	sel = """
		select tsci.committee_id, committee, committee_information_no
		from tbl_session_committee_information tsci
		left join tbl_committee tc on tc.committee_id=tsci.committee_id
		where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/get_session_previlege_hour', methods=['GET', 'POST'])
@login_required
def get_session_previlege_hour():
	p=json.loads(request.data)
	sel = """
		select info_id, concat(tpi.f_name,' ', tpi.m_name,' ', tpi.l_name) fullname
		from tbl_session_previlege_hour tsph
		left join tbl_personal_info tpi on tpi.info_id=tsph.councilor_info_id
		where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_privous_minutes', methods=['GET', 'POST'])
@login_required
def get_session_privous_minutes():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_reading_minutes where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_proposed_ordi', methods=['GET', 'POST'])
@login_required
def get_session_proposed_ordi():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_proposed_ordi where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_proposed_reso', methods=['GET', 'POST'])
@login_required
def get_session_proposed_reso():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_proposed_reso where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_petition_for_refferal', methods=['GET', 'POST'])
@login_required
def get_session_petition_for_refferal():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_petition_for_refferal tspfr
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tspfr.tracking_no 
		where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

# @query.route('/get_session_additional_refferal', methods=['GET', 'POST'])
# @login_required
# def get_session_additional_refferal():
# 	p=json.loads(request.data)
# 	sel = """
# 		select * from tbl_session_additional_refferal tsar
# 		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tsar.tracking_no 
# 		where session_id='"""+str(p['session_id'])+"""'
# 	"""
# 	rd= pyread(sel)
# 	return jsonify(rd)

@query.route('/get_session_code_ref', methods=['GET', 'POST'])
@login_required
def get_session_code_ref():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_code_ref where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_announcement', methods=['GET', 'POST'])
@login_required
def get_session_announcement():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_announcement where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_summary_correction', methods=['GET', 'POST'])
@login_required
def get_session_summary_correction():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_summary_correction where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/get_session_bussiness_third', methods=['GET', 'POST'])
@login_required
def get_session_bussiness_third():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_bussiness_third where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)
	

@query.route('/get_session_new_measure', methods=['GET', 'POST'])
@login_required
def get_session_new_measure():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_new_measure where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_calendar_measure', methods=['GET', 'POST'])
@login_required
def get_session_calendar_measure():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_calendar_measure where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_just_inserted', methods=['GET', 'POST'])
@login_required
def get_session_just_inserted():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_just_inserted where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_urgent', methods=['GET', 'POST'])
@login_required
def get_session_urgent():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_urgent where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_unfinished_bussiness', methods=['GET', 'POST'])
@login_required
def get_session_unfinished_bussiness():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_unfinished_bussiness where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_botd', methods=['GET', 'POST'])
@login_required
def get_session_botd():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_botd where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_session_veto_reading', methods=['GET', 'POST'])
@login_required
def get_session_veto_reading():
	p=json.loads(request.data)
	sel = """
		select * from tbl_session_veto_reading where session_id='"""+str(p['session_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)

@query.route('/get_minutes', methods=['GET', 'POST'])
@login_required
def get_minutes():
	sel="""
		select *, concat(tm.minutes_no,' ', ts.sp_title) title from tbl_minutes tm
		left join tbl_sp ts on ts.sp_id=tm.sp_id
		where status='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/del_minutes', methods=['GET', 'POST'])
@login_required
def del_minutes():
	p=json.loads(request.data)
	delete="delete from tbl_minutes where minutes_id='"+str(p['minutes_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_files_minutes" / str(p['minutes_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/save_minutes', methods=['GET','POST'])
@login_required
def save_minutes():
	p=request.form
	x=request.files

	q=json.loads(p['data'])

	min_id = 0 ;

	if str(p['minutes_id'])==0 or str(p['minutes_id'])=="0":
		insert="""
			insert into tbl_minutes set type='"""+str(p['type_minutes'])+"""' ,date='"""+str(p['date'])+"""',
		 	minutes_no='"""+str(p['minutes_no'])+"""', sp_id='"""+str(p['sp_id'])+"""'
		"""
		rd=cud_callbackid(insert)
		min_id = rd

	else:
		update="""
			update tbl_minutes set type='"""+str(p['type_minutes'])+"""' ,date='"""+str(p['date'])+"""', 
			minutes_no='"""+str(p['minutes_no'])+"""', sp_id='"""+str(p['sp_id'])+"""'
			where minutes_id='"""+str(p['minutes_id'])+"""'
		"""
		cud(update)

		min_id = p['minutes_id']

		delete_movant="delete from tbl_minutes_movant where minutes_id='"+str(p['minutes_id'])+"'"
		cud(delete_movant)

		delete_seconder="delete from tbl_minutes_seconder where minutes_id='"+str(p['minutes_id'])+"'"
		cud(delete_seconder)


	for filename_array in request.files:
		file=request.files[filename_array]

		f = filename_array.split("[")[0]

		if f=='file':
			n_path = Path(__file__).parent / "../static/uploads/upload_files_minutes" / str(min_id)
		if f=='file2':
			n_path = Path(__file__).parent / "../static/uploads/upload_files_minutes2" / str(min_id)

		n_path.resolve()
		
		if file and allowed_file(file.filename):
			filename = custom_secure_filename(file.filename)
			if not Path.exists(n_path):
				Path.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


			if f=='file':
				location1="upload_files_minutes//"+str(min_id)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");

				insert2="insert into tbl_minutes_path set filename='"+str(file.filename.replace("'","''"))+"' ,path='"+str(path_location.replace("'","''"))+"', minutes_id='"+str(min_id)+"'"
				cud(insert2)

			if f=='file2':
				location1="upload_files_minutes2//"+str(min_id)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");

				insert2="insert into tbl_minutes_raw_path set filename='"+str(file.filename.replace("'","''"))+"' ,path='"+str(path_location.replace("'","''"))+"', minutes_id='"+str(min_id)+"'"
				cud(insert2)

	return jsonify("Succesfuly Saved")


@query.route('/get_minutes_doc', methods=['GET', 'POST'])
@login_required
def get_minutes_doc():
	p=json.loads(request.data)
	sel="""
		select *,tc.committee_id committee_ids from tbl_minutes_path tmp
		left join tbl_minutes tm on tm.minutes_id=tmp.minutes_id
		left join tbl_committee tc on tc.committee_id=tm.committee_id
		where tm.minutes_id='"""+str(p['minutes_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_minutes_doc2', methods=['GET', 'POST'])
@login_required
def get_minutes_doc2():
	p=json.loads(request.data)
	sel="""
		select *,tc.committee_id committee_ids from tbl_minutes_raw_path tmp
		left join tbl_minutes tm on tm.minutes_id=tmp.minutes_id
		left join tbl_committee tc on tc.committee_id=tm.committee_id
		where tm.minutes_id='"""+str(p['minutes_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_reports_doc', methods=['GET', 'POST'])
@login_required
def get_committee_reports_doc():
	p=json.loads(request.data)
	sel="""
		select * from tbl_committee_reports_path tcrp
		where committee_reports_id='"""+str(p['committee_reports_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_ordinance_by_status', methods=['GET', 'POST'])
@login_required
def get_ordinance_by_status():
	p=json.loads(request.data)
	sel="""
		select *,tgc.title classification,ts.sp_title,tc.committee, tcro.committee_id as ref_committee
		from tbl_ordinance tbo
		left join tbl_governance_classification tgc on tgc.classification_id=tbo.classification_id
		left join tbl_sp ts on ts.sp_id=tbo.sp_id
		left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		left join tbl_committee tc on tc.committee_id=tcro.committee_id
		left join tbl_ordinance_status_numbers tosn on tosn.ordinance_id=tbo.ordinance_id
		left join tbl_minutes tm on tm.minutes_id=tbo.minutes_id
		WHERE tbo.ordinance_id='"""+str(p['ordinance_id'])+"""'
		GROUP BY tbo.ordinance_id ORDER BY tcro.committee_ref_id DESC
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_ordinance_attach_file', methods=['GET', 'POST'])
@login_required
def get_ordinance_attach_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_ordinance tbo
		inner join tbl_ordinance_file_committee tofc on tofc.ordinance_id=tbo.ordinance_id
		left join tbl_committee_ref_ordinance tcro on tcro.ordinance_id=tbo.ordinance_id
		where tofc.committee_id='"""+str(p['committee_id'])+"""'
		group by tofc.ordinance_file_committee_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_ordinance_minutes', methods=['GET', 'POST'])
@login_required
def get_ordinance_minutes():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_ordinance tmpco
		left join tbl_ordinance tbo on tbo.ordinance_id=tmpco.ordinance_id
		where tmpco.committee_id='"""+str(p['committee_id'])+"""' and tmpco.ordinance_id='"""+str(p['ordinance_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_committee_reports', methods=['GET','POST'])
@login_required
def save_committee_reports():	
	p=request.form
	p=json.loads(p['Serialized'])

	if p['h_committee_report_id']=='0':
		insert = """
			insert into tbl_committee_report set tracking_number='"""+str(p['tracking_number'])+"""', subject='"""+str(p['subject'])+"""',
			committee_number='"""+str(p['committee_number'])+"""', committee_id='"""+str(p['committee_id'])+"""', 
			date_reffered='"""+str(p['date_reffered'])+"""', sp_id = '"""+str(p['sp_id'])+"""'
		"""
		ids = cud_callbackid(insert)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "uploads/upload_committee_report_files"
			location=""+str(loc)+"//"+str(ids)
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				
			os.chdir(cwd)

			insert2="insert into tbl_committee_reports_file set path='"+str(path_location)+"' , filename='"+str(filename.replace("'",""))+"' , committee_reports_id='"+str(ids)+"'"
			cud(insert2)
	else:
		update = """
			update  tbl_committee_report set tracking_number='"""+str(p['tracking_number'])+"""', subject='"""+str(p['subject'])+"""',
			committee_number='"""+str(p['committee_number'])+"""', committee_id='"""+str(p['committee_id'])+"""',
			date_reffered='"""+str(p['date_reffered'])+"""' , sp_id = '"""+str(p['sp_id'])+"""'
			where id='"""+str(p['h_committee_report_id'])+"""'
		"""
		cud(update)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "uploads/upload_committee_report_files"
			location=""+str(loc)+"//"+str(p['h_committee_report_id'])
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				
			os.chdir(cwd)

			insert2="insert into tbl_committee_reports_file set path='"+str(path_location)+"' , filename='"+str(filename.replace("'",""))+"' , committee_reports_id='"+str(p['h_committee_report_id'])+"'"
			cud(insert2)

	return jsonify("Succesfuly Saved")


@query.route('/save_committee_information', methods=['GET','POST'])
@login_required
def save_committee_information():	
	p=request.form
	p=json.loads(p['Serialized'])

	if p['h_committee_information_id']=='0':
		insert = """
			insert into tbl_committee_information set tracking_number='"""+str(p['tracking_number'])+"""', subject='"""+str(p['subject'])+"""',
			committee_number='"""+str(p['committee_number'])+"""', committee_id='"""+str(p['committee_id'])+"""', 
			date_reffered='"""+str(p['date_reffered'])+"""', sp_id = '"""+str(p['sp_id'])+"""'
		"""
		ids = cud_callbackid(insert)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "upload_committee_information_files"
			location=""+str(loc)+"//"+str(ids)
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				
			os.chdir(cwd)

			insert2="insert into tbl_committee_information_file set path='"+str(path_location)+"' , filename='"+str(filename.replace("'",""))+"' , committee_information_id='"+str(ids)+"'"
			cud(insert2)
	else:
		update = """
			update  tbl_committee_information set tracking_number='"""+str(p['tracking_number'])+"""', subject='"""+str(p['subject'])+"""',
			committee_number='"""+str(p['committee_number'])+"""', committee_id='"""+str(p['committee_id'])+"""',
			date_reffered='"""+str(p['date_reffered'])+"""' , sp_id = '"""+str(p['sp_id'])+"""'
			where id='"""+str(p['h_committee_information_id'])+"""'
		"""
		cud(update)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "upload_committee_information_files"
			location=""+str(loc)+"//"+str(p['h_committee_information_id'])
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				
			os.chdir(cwd)

			insert2="insert into tbl_committee_information_file set path='"+str(path_location)+"' , filename='"+str(filename)+"' , committee_information_id='"+str(p['h_committee_information_id'])+"'"
			cud(insert2)

	return jsonify("Succesfuly Saved")


@query.route('/get_all_committee_reports', methods=['GET', 'POST'])
@login_required
def get_all_committee_reports():
	sel="""
		select * from tbl_committee_report tcr
		left join tbl_sp ts on ts.sp_id=tcr.sp_id
		left join tbl_committee tc on tc.committee_id=tcr.committee_id
		where ts.status='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_all_committee_information', methods=['GET', 'POST'])
@login_required
def get_all_committee_information():
	sel="""
		select * from tbl_committee_information tci
		left join tbl_sp ts on ts.sp_id=tci.sp_id
		left join tbl_committee tc on tc.committee_id=tci.committee_id
		where ts.status='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_reports_file', methods=['GET', 'POST'])
@login_required
def get_committee_reports_file():
	p = json.loads(request.data)
	sel= """
		select * from tbl_committee_reports_file where committee_reports_id='"""+str(p['committee_reports_id'])+"""'
	"""
	rd = pyread(sel)
	return jsonify(rd)

@query.route('/get_committee_information_file', methods=['GET', 'POST'])
@login_required
def get_committee_information_file():
	p = json.loads(request.data)
	sel= """
		select * from tbl_committee_information_file where committee_information_id='"""+str(p['committee_information_id'])+"""'
	"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_minutes_file', methods=['GET', 'POST'])
@login_required
def get_committee_minutes_file():
	p = json.loads(request.data)
	sel= """
		select * from tbl_committee_minutes_file where committee_minutes_id='"""+str(p['committee_minutes_id'])+"""'
	"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/delete_committee_report_file', methods=['GET', 'POST'])
@login_required
def delete_committee_report_file():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_reports_file where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/delete_committee_information_file', methods=['GET', 'POST'])
@login_required
def delete_committee_information_file():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_information_file where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/delete_committee_minutes_file', methods=['GET', 'POST'])
@login_required
def delete_committee_minutes_file():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_minutes_file where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/delete_committee_report', methods=['GET', 'POST'])
@login_required
def delete_committee_report():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_report where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/delete_committee_information', methods=['GET', 'POST'])
@login_required
def delete_committee_information():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_information where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/delete_committee_minutes', methods=['GET', 'POST'])
@login_required
def delete_committee_minutes():
	p = json.loads(request.data)
	delete = "delete from tbl_committee_minutes where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/get_all_committee_minutes', methods=['GET', 'POST'])
@login_required
def get_all_committee_minutes():
	sel="""
		select committee_ref_id ids,committee,'Ordinance' typ, ordinance_title title ,
		date_reffered, tcro.committee_id committee_ids, tmpco.ordinance_minutes_committee_id typ_id
		from tbl_committee_ref_ordinance tcro
		left join tbl_committee_ordinance tco on tco.ordinance_id=tcro.ordinance_id
		left join tbl_committee tc on tc.committee_id=tcro.committee_id
		left join tbl_ordinance tbo on tbo.ordinance_id=tcro.ordinance_id
		left join tbl_minutes_path_committee_ordinance tmpco on tmpco.committee_id=tco.committee_id and tmpco.ordinance_id=tco.ordinance_id

		group by tcro.committee_ref_id

		union all

		select committee_ref_petition_id ids,committee,'Petition' typ,title title,date_reffered
		, tcrp.committee_id committee_ids,tmpcp.minutes_path_committee_petition_id typ_id
		from tbl_committee_ref_petition tcrp
		left join tbl_committee_petition tcp on tcp.petition_id=tcrp.petition_id
		left join tbl_committee tc on tc.committee_id=tcrp.committee_id
		left join tbl_petition tp on tp.petition_id=tcrp.petition_id
		left join tbl_minutes_path_committee_petition tmpcp on tmpcp.committee_id=tcrp.committee_id and tmpcp.petition_id=tcrp.petition_id
		group by tcrp.committee_ref_petition_id

		 union all

		 select tcrr.committee_resolution_id ids,committee,'Resolution' typ,resolution_title title,date_reffered
		 , tcrr.committee_id committee_ids,tmpcr.minutes_path_committee_resolution_id typ_id
		 from tbl_committee_ref_resolution tcrr
		 left join tbl_committee_resolution tcr on tcr.resolution_id=tcrr.resolution_id
		 left join tbl_committee tc on tc.committee_id=tcrr.committee_id
		 left join tbl_resolution tr on tr.resolution_id=tcrr.resolution_id
		 left join tbl_minutes_path_committee_resolution tmpcr on tmpcr.committee_id=tcrr.committee_id and tmpcr.resolution_id=tcrr.resolution_id
		 group by tcrr.committee_resolution_id

	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_path_minutes_petition', methods=['GET', 'POST'])
@login_required
def get_file_path_minute():
	p=json.loads(request.data)
	sel="select * from tbl_minutes_path_committee_petition where minutes_path_committee_petition_id='"+str(p['minutes_path_committee_petition_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_path_minutes_ordinance', methods=['GET', 'POST'])
@login_required
def get_file_path_minutes_ordinance():
	p=json.loads(request.data)
	sel="select * from tbl_minutes_path_committee_ordinance where ordinance_minutes_committee_id='"+str(p['ordinance_minutes_committee_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_path_minutes_resolution', methods=['GET', 'POST'])
@login_required
def get_file_path_minutes_resolution():
	p=json.loads(request.data)
	sel="select * from tbl_minutes_path_committee_resolution where minutes_path_committee_resolution_id='"+str(p['minutes_path_committee_resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_ordinance_id_by_committee_ordinance_id', methods=['GET', 'POST'])
@login_required
def get_ordinance_id_by_committee_ordinance_id():
	p=json.loads(request.data)
	if p:
		if p['committee_ordinance_id']!="":
			sel="""
				select ordinance_id from tbl_committee_ordinance where committee_ordinance_id='"""+str(p['committee_ordinance_id'])+"""'
			"""
			rd=pyread(sel)
			return jsonify(rd)
	else:
		return jsonify("error")


@query.route('/get_committee_ordinance_reports_file_for_del', methods=['GET', 'POST'])
@login_required
def get_committee_ordinance_reports_file_for_del():
	p=json.loads(request.data)
	sel="""
		select * ,tcro.committee_id committee_ids from tbl_committee_ref_ordinance tcro
		left join tbl_ordinance_file_committee tofc on tofc.committee_id=tcro.committee_id
		where tcro.committee_id='"""+str(p['committee_id'])+"""'  and
		tcro.ordinance_id='"""+str(p['ordinance_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_committee_resolution_reports_file', methods=['GET', 'POST'])
@login_required
def get_committee_resolution_reports_file():
	p=json.loads(request.data)
	sel="""
		select *,tcrr.committee_id committee_ids from tbl_committee_ref_resolution tcrr
        left join tbl_resolution_file trf on trf.resolution_id=tcrr.resolution_id
		where committee_resolution_id='"""+str(p['committee_resolution_id'])+"""' 
		and tcrr.date_reffered='"""+str(p['date_reffered'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_committee_resolution_reports_file_for_del', methods=['GET', 'POST'])
@login_required
def get_committee_resolution_reports_file_for_del():
	p=json.loads(request.data)
	sel="""
		select *,tcrr.committee_id committee_ids from tbl_committee_ref_resolution tcrr
		left join tbl_resolution_file_committee trfc on trfc.committee_id=tcrr.committee_id
		where tcrr.committee_id='"""+str(p['committee_id'])+"""' and
		tcrr.resolution_id='"""+str(p['resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_committee_petition_reports_file_for_del', methods=['GET', 'POST'])
@login_required
def get_committee_petition_reports_file_for_del():
	p=json.loads(request.data)
	sel="""
		select *,tcrp.committee_id committee_ids from tbl_committee_ref_petition tcrp
		left join tbl_petition_path_committee tppc on tppc.committee_id=tcrp.committee_id
		where  tcrp.committee_id='"""+str(p['committee_id'])+"""' and
		tcrp.petition_id='"""+str(p['petition_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_petition_reports_file', methods=['GET', 'POST'])
@login_required
def get_committee_petition_reports_file():
	p=json.loads(request.data)
	sel="""
		select *,tcrp.committee_id committee_ids from tbl_committee_ref_petition tcrp
		left join tbl_petition_path_committee tppc on tppc.committee_id=tcrp.committee_id
		where committee_ref_petition_id='"""+str(p['committee_ref_petition_id'])+"""' 
		and tcrp.date_reffered='"""+str(p['date_reffered'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_committee_resolution', methods=['GET', 'POST'])
@login_required
def save_committee_resolution():
	p=request.form
	if p['resolution_id']==0 or p['resolution_id']=="0":
		insert="""
			insert into tbl_committee_resolution set resolution_id='"""+str(p['resolution_id_main'])+"""',committee_id='"""+str(p['committee_id'])+"""'
		"""
		rd=cud_callbackid(insert)

		update_resolution="update tbl_resolution set status='"+str(p['status'])+"' where resolution_id='"+str(p['resolution_id_main'])+"'"
		cud(update_resolution)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_resolution_files" / str(p['resolution_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_resolution_files//"+str(p['resolution_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_resolution_file_committee set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""', resolution_id='"""+str(p['resolution_id_main'])+"""',
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":

				select="select minutes_id from tbl_resolution where resolution_id='"+str(p['resolution_id_main'])+"'"
				rd=pyread(select)
				if rd:
					y=y+1
					file_name="file_minutes["+str(y)+"]"
					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_committee_resolution_minutes_files" / str(rd[0]['minutes_id'])
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_committee_resolution_minutes_files//"+str(rd[0]['minutes_id'])
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");
						
						insert2="""
							insert into tbl_minutes_path_committee_resolution  set filename='"""+str(file.filename.replace("'",""))+"""',
							path='"""+str(path_location)+"""', minutes_id='"""+str(rd[0]['minutes_id'])+"""',
							committee_id='"""+str(p['committee_id'])+"""', resolution_id='"""+str(p['resolution_id_main'])+"""'
						"""
						cud(insert2)

		sel="""
			select * from tbl_resolution
			where resolution_id='"""+str(p['resolution_id_main'])+"""'
		"""
		rd_resolution_title=pyread(sel)

		title_track=rd_resolution_title[0]['resolution_title'].replace("'","''")
		if rd_resolution_title[0]['resolution_title']!="":
			doc_status = ""
			# insert_track="""
			# 	insert into tbl_document_tracking set document_id='"""+str(p['resolution_id_main'])+"""', 
			# 	title='"""+str(title_track)+"""',  committee_id='"""+str(p['committee_id'])+"""',
			# 	type_document='"""+str("Resolution")+"""', date=curdate()
			# """
			# cud(insert_track)
		return jsonify("Succesfully Saved")
	else:
		update_resolution="update tbl_resolution set status='"+str(p['status'])+"' where resolution_id='"+str(p['resolution_id_main'])+"'"
		cud(update_resolution)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_resolution_files" / str(p['resolution_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_resolution_files//"+str(p['resolution_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_resolution_file_committee set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""', resolution_id='"""+str(p['resolution_id_main'])+"""',
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":

				select="select minutes_id from tbl_resolution where resolution_id='"+str(p['resolution_id_main'])+"'"
				rd=pyread(select)
				if rd:
					y=y+1
					file_name="file_minutes["+str(y)+"]"
					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_committee_resolution_minutes_files" / str(rd[0]['minutes_id'])
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_committee_resolution_minutes_files//"+str(rd[0]['minutes_id'])
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");
						
						insert2="""
							insert into tbl_minutes_path_committee_resolution  set filename='"""+str(file.filename.replace("'",""))+"""',
							path='"""+str(path_location)+"""', minutes_id='"""+str(rd[0]['minutes_id'])+"""',
							committee_id='"""+str(p['committee_id'])+"""', resolution_id='"""+str(p['resolution_id_main'])+"""'
						"""
						cud(insert2)

		sel="""
			select * from tbl_resolution
			where resolution_id='"""+str(p['resolution_id_main'])+"""'
		"""
		rd_resolution_title=pyread(sel)
		title_track=rd_resolution_title[0]['resolution_title'].replace("'","''")
		if rd_resolution_title[0]['resolution_title']!="":
			doc_status = ""

			# insert_track="""
			# 	insert into tbl_document_tracking set document_id='"""+str(p['resolution_id_main'])+"""', title='"""+str(title_track)+"""', 
			# 	committee_id='"""+str(p['committee_id'])+"""', type_document='"""+str("Resolution")+"""', date=curdate()
			# """
			# cud(insert_track)
		return jsonify("Succesfully Updated")


@query.route('/get_tbl_committee_ref_ordinance', methods=['GET', 'POST'])
@login_required
def get_tbl_committee_ref_ordinance():
	p=json.loads(request.data)
	sel="select * from tbl_committee_ref_ordinance where ordinance_id='"+str(p['ordinance_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_committee_ordinance', methods=['GET', 'POST'])
@login_required
def save_committee_ordinance():
	p=request.form
	if p['ordinance_id']==0 or p['ordinance_id']=="0":
		insert="""insert into tbl_committee_ordinance set  
		ordinance_id='"""+str(p['ordinance_id_main'])+"""', committee_id='"""+str(p['committee_id'])+"""'
		"""
		cud(insert)

		update_ordinance="update tbl_ordinance set status='"+str(p['status'])+"' where ordinance_id='"+str(p['ordinance_id_main'])+"'"
		cud(update_ordinance)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_files" / str(p['ordinance_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_ordinance_files//"+str(p['ordinance_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""insert into tbl_ordinance_file_committee set 
						filename='"""+str(file.filename.replace("'",""))+"""', path='"""+str(path_location)+"""', 
						ordinance_id='"""+str(p['ordinance_id_main'])+"""', committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":

				select="select minutes_id from tbl_ordinance where ordinance_id='"+str(p['ordinance_id_main'])+"'"
				rd=pyread(select)
				if rd:
					y=y+1
					file_name="file_minutes["+str(y)+"]"

					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_minutes_files" / str(rd[0]['minutes_id'])
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_committee_ordinance_minutes_files//"+str(rd[0]['minutes_id'])
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");
						
						insert2="""insert into tbl_minutes_path_committee_ordinance  set 
							filename='"""+str(file.filename.replace("'",""))+"""', path='"""+str(path_location)+"""', 
							minutes_id='"""+str(rd[0]['minutes_id'])+"""', committee_id='"""+str(p['committee_id'])+"""',
							ordinance_id='"""+str(p['ordinance_id_main'])+"""'
						"""
						cud(insert2)
		sel="""
			select * from tbl_ordinance
			where ordinance_id='"""+str(p['ordinance_id_main'])+"""'
		"""
		rd_ordinance_title=pyread(sel)
		title_track=rd_ordinance_title[0]['ordinance_title'].replace("'","''")
		# if rd_ordinance_title[0]['ordinance_title']!="":
		# 	insert_track="""
		# 		insert into tbl_document_tracking set document_id='"""+str(p['ordinance_id_main'])+"""',
		# 		title='"""+str(title_track)+"""', committee_id='"""+str(p['committee_id'])+"""', type_document='"""+str("Ordinance")+"""', date=curdate()
		# 	"""
		# 	cud(insert_track)
		return jsonify("Succesfuly Saved")
	else:

		update_ordinance="update tbl_ordinance set status='"+str(p['status'])+"' where ordinance_id='"+str(p['ordinance_id_main'])+"'"
		cud(update_ordinance)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_files" / str(p['ordinance_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_ordinance_files//"+str(p['ordinance_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_ordinance_file_committee set filename='"""+str(file.filename.replace("'",""))+"""', 
						path='"""+str(path_location)+"""', ordinance_id='"""+str(p['ordinance_id_main'])+"""', 
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":

				select="select minutes_id from tbl_ordinance where ordinance_id='"+str(p['ordinance_id_main'])+"'"
				rd=pyread(select)
				if rd:
					y=y+1
					file_name="file_minutes["+str(y)+"]"

					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_committee_ordinance_minutes_files" / str(rd[0]['minutes_id'])
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = custom_secure_filename(file.filename)
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_committee_ordinance_minutes_files//"+str(rd[0]['minutes_id'])
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");
						
						insert2="""
							insert into tbl_minutes_path_committee_ordinance set filename='"""+str(file.filename.replace("'",""))+"""',
							path='"""+str(path_location)+"""', minutes_id='"""+str(rd[0]['minutes_id'])+"""',
							committee_id='"""+str(p['committee_id'])+"""',ordinance_id='"""+str(p['ordinance_id_main'])+"""'
						"""
						cud(insert2)
		sel="""
			select * from tbl_ordinance
			where ordinance_id='"""+str(p['ordinance_id_main'])+"""'
		"""
		rd_ordinance_title=pyread(sel)
		title_track=rd_ordinance_title[0]['ordinance_title'].replace("'","''")
		# if rd_ordinance_title[0]['ordinance_title']!="":
		# 	insert_track="""
		# 		insert into tbl_document_tracking set document_id='"""+str(p['ordinance_id_main'])+"""',
		# 		title='"""+str(title_track)+"""', committee_id='"""+str(p['committee_id'])+"""', type_document='"""+str("Ordinance")+"""', date=curdate()
		# 	"""
		# 	cud(insert_track)
		return jsonify("Succesfuly Updated")

@query.route('/save_committee_petition', methods=['GET', 'POST'])
@login_required
def save_committee_petition():
	p=request.form
	if p['petition_id']==0 or p['petition_id']=="0":
		insert="""
			insert into tbl_committee_petition set action_taken='"""+str(p['action_taken'])+"""',
			 petition_id='"""+str(p['petition_id_main'])+"""', committee_id='"""+str(p['committee_id'])+"""'
		"""
		cud(insert)
		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_petition_files" / str(p['petition_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_petition_files//"+str(p['petition_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_petition_path_committee set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""',petition_id='"""+str(p['petition_id_main'])+"""',
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":
				y=y+1
				file_name="file_minutes["+str(y)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_petition_minutes_files" / str(p['petition_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_petition_minutes_files//"+str(p['petition_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_minutes_path_committee_petition set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""', petition_id='"""+str(p['petition_id_main'])+"""',
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)


		sel="""
			select * from tbl_petition
			where petition_id='"""+str(p['petition_id_main'])+"""'
		"""
		rd_petition_title=pyread(sel)
		# if rd_petition_title[0]['petition_id']!="":
		# 	insert_track="""
		# 		insert into tbl_document_tracking set document_id='"""+str(p['petition_id_main'])+"""',
		# 		title='"""+str(rd_petition_title[0]['title'])+"""', committee_id='"""+str(p['committee_id'])+"""',
		# 		action_taken='"""+str(p['action_taken'])+"""', type_document='"""+str("Petition")+"""',
		# 		date=curdate()
		# 	"""
		# 	cud(insert_track)
		return jsonify("Succesfuly Saved")
	else:
		update="""
			update tbl_committee_petition set action_taken='"""+str(p['action_taken'])+"""' 
			where petition_id='"""+str(p['petition_id_main'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
		"""
		cud(update)

		x=-1
		y=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_petition_files" / str(p['petition_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_petition_files//"+str(p['petition_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_petition_path_committee set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""', petition_id='"""+str(p['petition_id_main'])+"""',
						committee_id='"""+str(p['committee_id'])+"""'
					"""
					cud(insert2)

			if str(split[0])=="file_minutes":
				y=y+1
				file_name="file_minutes["+str(y)+"]"
				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_committee_petition_minutes_files" / str(p['petition_id_main'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = custom_secure_filename(file.filename)
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_committee_ordinance_minutes_files//"+str(p['petition_id_main'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					
					insert2="""
						insert into tbl_minutes_path_committee_petition set filename='"""+str(file.filename.replace("'",""))+"""',
						path='"""+str(path_location)+"""', petition_id='"""+str(p['petition_id_main'])+"""'
					"""
					cud(insert2)

		sel="""
			select * from tbl_petition
			where petition_id='"""+str(p['petition_id_main'])+"""'
		"""
		rd_petition_title=pyread(sel)

		title_track=rd_petition_title[0]['title'].replace("'","''")
		# if rd_petition_title[0]['petition_id']!="":
		# 	insert_track="""
		# 		insert into tbl_document_tracking set document_id='"""+str(p['petition_id_main'])+"""',
		# 		title='"""+str(title_track)+"""', committee_id='"""+str(p['committee_id'])+"""',
		# 		action_taken='"""+str(p['action_taken'])+"""', type_document='"""+str("Petition")+"""',
		# 		date=curdate()
		# 	"""
		# 	cud(insert_track)
		return jsonify("Succesfuly Updated")


@query.route('/get_committee_resolution_file', methods=['GET', 'POST'])
@login_required
def get_committee_resolution_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_committee_ref_resolution tcrr
		left join tbl_resolution_file_committee trfc on trfc.committee_id=tcrr.committee_id
		where trfc.committee_id='"""+str(p['committee_id'])+"""' 
		and tcrr.resolution_id='"""+str(p['resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/sel_petition_id_tbl_minutes_path_committee_petition', methods=['GET', 'POST'])
@login_required
def sel_petition_id_tbl_minutes_path_committee_petition():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_petition
		where petition_id='"""+str(p['petition_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_ordinance_status', methods=['GET', 'POST'])
@login_required
def get_committee_ordinance_status():
	p=json.loads(request.data)
	sel="""
		select *,tco.ordinance_id tco_ordinance_id 
		from tbl_committee_ordinance tco
		left join tbl_ordinance tbo on tbo.ordinance_id=tco.ordinance_id
		where tbo.ordinance_id='"""+str(p['ordinance_id'])+"""' 
		and tco.committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_resolution_status', methods=['GET', 'POST'])
@login_required
def get_committee_resolution_status():
	p=json.loads(request.data)
	sel="""
		select *,tcr.resolution_id tcr_resolution_id 
		from tbl_committee_resolution tcr
		left join tbl_resolution tr on tr.resolution_id=tcr.resolution_id
		where tr.resolution_id='"""+str(p['resolution_id'])+"""' 
		and tcr.committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_resolution_minutes', methods=['GET', 'POST'])
@login_required
def get_committee_resolution_minutes():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_resolution tpcr
		left join tbl_resolution tr on tr.minutes_id=tpcr.minutes_id
		where tpcr.committee_id='"""+str(p['committee_id'])+"""' and tpcr.resolution_id='"""+str(p['resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/del_budget_councilor_deduction', methods=['GET', 'POST'])
@login_required
def del_budget_councilor_deduction():
	p=json.loads(request.data)
	delete="delete from tbl_sp_budget_balance_expenses where balance_expenses_id='"+str(p['balance_expenses_id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/get_petition_action_taken', methods=['GET', 'POST'])
@login_required
def get_petition_action_taken():
	p=json.loads(request.data)
	sel="""
		select * from tbl_committee_petition tcp
		where petition_id='"""+str(p['petition_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_committee_petition_file', methods=['GET', 'POST'])
@login_required
def get_committee_petition_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition tp
		left join tbl_committee_ref_petition tcrp on tcrp.petition_id=tp.petition_id
		inner join tbl_petition_path_committee tppc on tppc.petition_id=tcrp.petition_id
		where tcrp.committee_id='"""+str(p['committee_id'])+"""' 
		and tp.petition_id='"""+str(p['petition_id'])+"""'
		GROUP BY tp.petition_id,tcrp.committee_id
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_resolution_file', methods=['GET', 'POST'])
@login_required
def get_resolution_file():
	p=json.loads(request.data)
	sel="""
		select *,tmr.title minutes_title,tmr.minutes_id minutes_ids,tcrf.committee_id committee_ids from tbl_resolution tr
		left join tbl_resolution_file trp on trp.resolution_id=tr.resolution_id
		left join tbl_minutes_resolution tmr on tmr.minutes_id=tr.minutes_id
		left join tbl_committee_ref_resolution tcrf on tcrf.resolution_id=tr.resolution_id
		left join tbl_committee tc on tc.committee_id=tcrf.committee_id
		left join tbl_sp ts on ts.sp_id=tr.sp_id 
		where tr.resolution_id='"""+str(p['resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_documents_refferals', methods=['GET', 'POST'])
@login_required
def get_documents_refferals():
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates 
		from tbl_documents_refferals tdrp
		left join tbl_sp ts on ts.sp_id=tdrp.sp_id
		where ts.`status`='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_barangay_ordinance', methods=['GET', 'POST'])
@login_required
def get_barangay_ordinance():
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates from tbl_barangay_ordinance 
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_barangay_resolution', methods=['GET', 'POST'])
@login_required
def get_barangay_resolution():
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates from tbl_barangay_resolution 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_executive_order', methods=['GET', 'POST'])
@login_required
def get_executive_order():
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates from tbl_executive_order 
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_source_document', methods=['GET', 'POST'])
@login_required
def get_source_document():
	sel="""
		select * from tbl_source_of_document 
	"""
	rd=pyread(sel)
	return jsonify(rd)



@query.route('/save_source_document', methods=['POST'])
@login_required
def save_source_document():
    p = request.get_json()
    
    if not p or 'title' not in p or 'id' not in p:
        return jsonify({"error": "Missing required fields"}), 400

    title = p['title']
    doc_id = int(p['id'])

    if doc_id == 0:
        insert_query = """
            INSERT INTO tbl_source_of_document (title)
            VALUES (%s)
        """
        crud(insert_query, (title,))
    else:
        update_query = """
            UPDATE tbl_source_of_document
            SET title = %s
            WHERE id = %s
        """
        crud(update_query, (title, doc_id))

    return jsonify("Successfully Saved")


@query.route('/delete_source_document', methods=['GET', 'POST'])
@login_required
def delete_source_document():
	p = json.loads(request.data)
	delete = """
		delete from tbl_source_of_document where id=%s
	"""
	args= (str(p['id']),)
	crud(delete, args)
	return jsonify("Succesfully Deleted")

@query.route('/get_memorandom', methods=['GET', 'POST'])
@login_required
def get_memorandom():
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates from tbl_memorandom tm left join tbl_sp ts on ts.sp_id=tm.sp_id where ts.`status`='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_documents_refferals', methods=['GET', 'POST'])
@login_required
def save_documents_refferals():
	p=request.form
	title=p['title'].replace("'","''")
	if p['document_referal_id']==0 or p['document_referal_id']=="0":
		insert="""
			insert into tbl_documents_refferals set title='"""+str(title)+"""', date_submitted=curdate(), 
			sp_id='"""+str(p['sp_id'])+"""', type='"""+str(p['type'])+"""'
		"""
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_document_referals"/str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_document_referals//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_documents_refferals_path set filename='"+str(file.filename.replace("'","''"))+"', path='"+str(path_location.replace("'","''"))+"', documents_refferals_id='"+str(rd)+"'"
				cud(insert2)
		return jsonify("Succesfuly Saved")
	else:
		update="""
			update tbl_documents_refferals set title='"""+str(title)+"""', sp_id='"""+str(p['sp_id'])+"""', type='"""+str(p['type'])+"""' 
			where documents_refferals_id='"""+str(p['document_referal_id'])+"""'
		"""
		cud(update)

		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_document_referals" / str(p['document_referal_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_document_referals//"+str(p['document_referal_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				insert2="insert into tbl_documents_refferals_path set filename='"+str(file.filename.replace("'","''"))+"', path='"+str(path_location.replace("'","''"))+"', documents_refferals_id='"+str(p['document_referal_id'])+"'"
				cud(insert2)
		return jsonify("Succesfuly updated")

# 

@query.route('/save_barangay_ordinance', methods=['GET', 'POST'])
@login_required
def save_barangay_ordinance():
	p=request.form
	title=p['title'].replace("'","''")
	description = p['description'].replace("'","''")
	if p['barangay_ordinance_id']==0 or p['barangay_ordinance_id']=="0":
		insert="insert into tbl_barangay_ordinance set title='"+str(title)+"', date_submitted=curdate(), description='"+str(description)+"', brgy_id='"+str(p['brgy_id'])+"'"
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_barangay_ordinance" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_barangay_ordinance//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_barangay_ordinance_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', barangay_ordinance_id='"+str(rd)+"'"
				cud(insert2)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_barangay_ordinance set title='"+str(title)+"',  description='"+str(description)+"', brgy_id='"+str(p['brgy_id'])+"' where barangay_ordinance_id='"+str(p['barangay_ordinance_id'])+"'"
		cud(update)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_barangay_ordinance" / str(p['barangay_ordinance_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_barangay_ordinance//"+str(p['barangay_ordinance_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_barangay_ordinance_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', barangay_ordinance_id='"+str(p['barangay_ordinance_id'])+"'"
				cud(insert2)
		return jsonify("Succesfuly updated")

# save barangay resolution

@query.route('/save_barangay_resolution', methods=['GET', 'POST'])
@login_required
def save_barangay_resolution():
	p=request.form
	title=p['title'].replace("'","''")
	description =p['description'].replace("'","''")
	if p['barangay_resolution_id']==0 or p['barangay_resolution_id']=="0":
		insert="insert into tbl_barangay_resolution set title='"+str(title)+"', date_submitted=curdate(), description='"+str(description)+"', brgy_id='"+str(p['brgy_id'])+"'"
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_barangay_resolution" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_barangay_resolution//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_barangay_resolution_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', barangay_resolution_id='"+str(rd)+"'"
				cud(insert2)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_barangay_resolution set title='"+str(title)+"',  description='"+str(description)+"', brgy_id='"+str(p['brgy_id'])+"' where barangay_resolution_id='"+str(p['barangay_resolution_id'])+"'"
		cud(update)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_barangay_resolution" / str(p['barangay_resolution_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_barangay_resolution//"+str(p['barangay_resolution_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_barangay_resolution_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', barangay_resolution_id='"+str(p['barangay_resolution_id'])+"'"
				cud(insert2)
		return jsonify("Succesfuly updated")

# end barangay resolution

@query.route('/save_executive_order', methods=['GET', 'POST'])
@login_required
def save_executive_order():
	p=request.form
	title=p['title'].replace("'","''")

	if p['executive_order_id']==0 or p['executive_order_id']=="0":
		insert="insert into tbl_executive_order set title='"+str(title)+"', date_submitted=curdate(), sp_id='"+str(p['sp_id'])+"'"
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_executive_order" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_executive_order//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_executive_order_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', executive_order_id='"+str(rd)+"'"
				cud(insert2)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_executive_order set title='"+str(title)+"', sp_id='"+str(p['sp_id'])+"' where executive_order_id='"+str(p['executive_order_id'])+"'"
		cud(update)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_executive_order" / str(p['executive_order_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_executive_order//"+str(p['executive_order_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_executive_order_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', executive_order_id='"+str(p['executive_order_id'])+"'"
				cud(insert2)
		return jsonify("Succesfuly updated")


@query.route('/save_memorandom', methods=['GET', 'POST'])
@login_required
def save_memorandom():
	p=request.form
	title=p['title'].replace("'","''")
	if p['memorandom_id']==0 or p['memorandom_id']=="0":
		insert="insert into tbl_memorandom set title='"+str(title)+"', date_submitted=curdate(), sp_id='"+str(p['sp_id'])+"'"
		rd=cud_callbackid(insert)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_memorandom" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_memorandom//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_memorandom_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', memorandom_id='"+str(rd)+"'"
				cud(insert2)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_memorandom set title='"+str(title)+"', sp_id='"+str(p['sp_id'])+"'  where memorandom_id='"+str(p['memorandom_id'])+"'"
		cud(update)
		for filename_array in request.files:
			file=request.files[filename_array]

			n_path = Path(__file__).parent / "../static/uploads/upload_memorandom" / str(p['memorandom_id'])
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = custom_secure_filename(file.filename)
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_memorandom//"+str(p['memorandom_id'])
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				insert2="insert into tbl_memorandom_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', memorandom_id='"+str(p['memorandom_id'])+"'"
				cud(insert2)
		return jsonify("Succesfuly updated")



	
@query.route('/get_resu_2nd', methods = ['POST','GET'])
@login_required
def get_resu_2nd():
	try:
		sel = "select * from tbl_resolution where status = 1"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_ordinance_2nd', methods = ['POST','GET'])
@login_required
def get_ordinance_2nd():
	try:
		sel = "select * from tbl_ordinance where status = 1"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_resu_urgent', methods = ['POST','GET'])
@login_required
def get_resu_urgent():
	try:
		sel = "select * from tbl_resolution"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_resu_measure', methods = ['POST','GET'])
@login_required
def get_resu_measure():
	try:
		sel = "select * from tbl_resolution where status != 6 and status != 7 and status != 8"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_ordinance_urgent', methods = ['POST','GET'])
@login_required
def get_ordinance_urgent():
	try:
		sel = "select * from tbl_ordinance"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_resolution_file2', methods=['GET', 'POST'])
@login_required
def get_resolution_file2():
	p=json.loads(request.data)
	sel="""
		select * from tbl_resolution_file where resolution_id='"""+str(p['resolution_id'])+"""' 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_ordinance_file', methods=['GET', 'POST'])
@login_required
def get_ordinance_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_ordinance_file where ordinance_id='"""+str(p['ordinance_id'])+"""' 
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_ordinance_veto_file', methods=['GET', 'POST'])
@login_required
def get_ordinance_veto_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_veto_ordinance where ordinance_id='"""+str(p['ordinance_id'])+"""' 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_resolution_veto_file', methods=['GET', 'POST'])
@login_required
def get_resolution_veto_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_veto_resolution where resolution_id='"""+str(p['resolution_id'])+"""' 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_minutes_file_resolution', methods=['GET', 'POST'])
@login_required
def get_minutes_file_resolution():
	p=json.loads(request.data)
	
	sel="""
		select * from tbl_minutes_resolution_path tmrp where tmrp.minutes_id='"""+str(p['minutes_id'])+"""' 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_minutes_file', methods=['GET', 'POST'])
@login_required
def get_minutes_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_ordinance tbo
		inner join tbl_minutes_path tmp on tmp.minutes_id=tbo.minutes_id 
		where tbo.ordinance_id='"""+str(p['ordinance_id'])+"""'  
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_committe_ord_file', methods=['GET', 'POST'])
@login_required
def get_committe_ord_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_ordinance_file_committee tofc
		where tofc.ordinance_id='"""+str(p['ordinance_id'])+"""'  
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_ordinance', methods=['GET', 'POST'])
@login_required
def del_ordinance():
	p=json.loads(request.data)
	delete="delete from tbl_ordinance where ordinance_id='"+str(p['ordinance_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_ordinance_files" / str(p['ordinance_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/del_committee_reports', methods=['GET', 'POST'])
@login_required
def del_committee_reports():
	p=json.loads(request.data)
	delete="delete from tbl_committee_report where id='"+str(p['ids'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/del_resolution', methods=['GET', 'POST'])
@login_required
def del_resolution():
	p=json.loads(request.data)
	delete="delete from tbl_resolution where resolution_id='"+str(p['resolution_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution" / str(p['resolution_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/delete_resolution_minutes_file', methods=['GET', 'POST'])
@login_required
def delete_resolution_minutes_file():
	p=json.loads(request.data)
	delete="delete from tbl_minutes_resolution_path where minutes_res_id='"+str(p['minutes_res_id'])+"'"
	
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution_minutes" / str(p['minutes_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/save_resolution_committee', methods=['GET', 'POST'])
@login_required
def save_resolution_committee():
	p=json.loads(request.data)
	insert_committee_resolution="insert tbl_committee_ref_resolution set committee_id='"+str(p['committee_id'])+"', resolution_id='"+str(p['resolution_id'])+"', date_reffered=now()"
	cud(insert_committee_resolution)
	return jsonify("Succesfuly Saved")


@query.route('/save_resolution', methods=['GET', 'POST'])
@login_required
def save_resolution():
	p=request.form
	p=json.loads(p['Serialized'])

	descr=p['description'].replace("'","''")
	resolution_title=p['resolution_title'].replace("'","''")
	minutes_title=p['minutes_title'].replace("'","''")


	new_lst=(','.join(p['ref_committee'][0]))

	if 'category' not in p:
		p['category']=''
	if 'gov_classification' not in p:
		p['gov_classification']=''
	if 'source_of_document' not in p:
		p['source_of_document']=''

	if p['sp_id']=='':
		sel_sp ="select sp_id from tbl_sp where `status`='ACTIVE'"
		r_sp_id=pyread(sel_sp)
		p['sp_id']=r_sp_id[0]['sp_id']
		
	if p['resolution_id']==0 or p['resolution_id']=="0":

		sel_if_exst_res_no="select count(*) count_res_num from tbl_resolution where resolution_number='"+str(p['resolution_no'])+"'"
		rd_count=pyread(sel_if_exst_res_no)

		categories = str(p['categories'][0]).replace("'",'').replace("[","").replace("]","").replace(" ", "")

		if rd_count[0]['count_res_num']==0:
			insert="""insert into tbl_resolution set resolution_number='"""+str(p['resolution_no'])+"""', 
				resolution_title='"""+str(resolution_title)+"""', date_enacted='"""+str(p['date_enacted'])+"""',
				category='"""+str(categories)+"""', sp_id='"""+str(p['sp_id'])+"""', session_id='"""+str(p['session_id'])+"""',
				tracking_number='"""+str(p['tracking_no'])+"""', classification_id='"""+str(p['gov_classification'])+"""', 
				source_of_document='"""+str(p['source_of_document'])+"""', source_document_specify='"""+str(p['source_document_specify'])+"""',
				remarks='"""+str(p['remarks'])+"""', `status`='"""+str(p['status'])+"""',
				description='"""+str(descr)+"""', series_number='"""+str(p['series_number'])+"""'
			"""
			rd=cud_callbackid(insert)

			for i in p['ref_committee'][0]:
				insert_committee="insert into tbl_committee_ref_resolution set committee_id='"+str(i)+"', resolution_id='"+str(rd)+"', date_reffered=now()"
				cud(insert_committee)

			if 'input_authors' in p:
				for i in p['input_authors']:
					insert_author="insert into tbl_resolution_author set author='"+str(i)+"', resolution_id='"+str(rd)+"'"
					cud(insert_author)

			if 'input_co_authors' in p:
				for i in p['input_co_authors']:
					insert_co_author="insert into tbl_resolution_co_author set co_author='"+str(i)+"', resolution_id='"+str(rd)+"'"
					cud(insert_co_author)

			if 'input_sponsor' in p:
				for i in p['input_sponsor']:
					insert_sponsor="insert into tbl_resolution_sponsor set sponsor='"+str(i)+"', resolution_id='"+str(rd)+"'"
					cud(insert_sponsor)

			if 'input_cosponsor' in p:
				for i in p['input_cosponsor']:
					insert_cosponsor="insert into tbl_resolution_cosponsor set cosponsor='"+str(i)+"', resolution_id='"+str(rd)+"'"
					cud(insert_cosponsor)

			x=-1
			y=-1
			z=-1
			for filename_array in request.files:
				split=filename_array.split("[")
				if str(split[0])=="file_attach":
					x=x+1
					file_name="file_attach["+str(x)+"]"

					file=request.files[filename_array]

					n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = str(custom_secure_filename(file.filename)).replace("'","''")
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_files_resolution//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");
						
						insert2="insert into tbl_resolution_file set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', resolution_id='"+str(rd)+"'"
						cud(insert2)

					# file minutes  ---------------------------------->

				if str(split[0])=="file_minutes":
					y=y+1
					file_name_min="file_minutes["+str(y)+"]"

					file=request.files[file_name_min]
					n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution_minutes" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = str(custom_secure_filename(file.filename)).replace("'","''")
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_files_resolution_minutes//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");

						insert_tbl_minutes_path="insert into tbl_minutes_resolution_path set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', minutes_id='"+str(rd)+"'"
						cud(insert_tbl_minutes_path)


				if str(split[0])=="file_veto":
					z=z+1
					file_name_min="file_veto["+str(z)+"]"

					file=request.files[file_name_min]
					n_path = Path(__file__).parent / "../static/uploads/upload_veto_resolution" / str(rd)
					n_path.resolve()
					
					if file and allowed_file(file.filename):
						filename = str(custom_secure_filename(file.filename)).replace("'","''")
						if not Path.exists(n_path):
							Path.mkdir(n_path)
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						else:
							app.config['UPLOAD_FOLDER']=n_path
							file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

						location1="upload_veto_resolution//"+str(rd)
						location1.replace("//", "\\\\");
						location=location1+"/"+filename
						path_location=location.replace("/", "\\\\");

						insert_veto="insert into tbl_veto_resolution set filename='"+str(file.filename.replace("'",""))+"', path='"+str(path_location)+"', resolution_id='"+str(rd)+"'"
						cud(insert_veto)

			sel_res="select * from tbl_resolution where resolution_id='"+str(rd)+"'"
			rd_reso=pyread(sel_res)

			if p['status']=="1":
				doc_status = "Proposed Resolution"
			elif p['status']=="2":
				doc_status = "2nd Reading Resolution"
			elif p['status']=="3":
				doc_status = "3rd Reading Resolution"
			elif p['status']=="4":
				doc_status = "3rd Reading Resolution Excemption"
			elif p['status']=="5":
				doc_status = "For mayors Approval"
			elif p['status']=="6":
				doc_status = "Approved Resolution"
			elif p['status']=="7":
				doc_status = "Veto Resolution"

			if p['tracking_no']:
				select_tracking = """
					select track_gen_id from tbl_document_tracking where tracking_no='"""+str(p['tracking_no'])+"""',
				"""
				rd_sel_tracking = pyread(select_tracking)

				if len(rd_sel_tracking)>0:
					insert_tracking_status = """
						insert into tbl_document_tracking_status  set track_gen_id='"""+str(rd_sel_tracking[0]['track_gen_id'])+"""', status='Approved', date=now()
					"""
				cud(insert_tracking_status)
			return jsonify("Succesfuly Saved")

		else:
			prnt_B("Resolution Number Already exists")
			return jsonify("Resolution Number Already exists")

	else:
		categories = str(p['categories'][0]).replace("'",'').replace("[","").replace("]","").replace(" ", "")

		update="""update tbl_resolution set resolution_number='"""+str(p['resolution_no'])+"""', resolution_title='"""+str(resolution_title)+"""', 
			date_enacted='"""+str(p['date_enacted'])+"""', category='"""+str(categories)+"""', sp_id='"""+str(p['sp_id'])+"""', session_id='"""+str(p['session_id'])+"""',
			tracking_number='"""+str(p['tracking_no'])+"""', classification_id='"""+str(p['gov_classification'])+"""', source_of_document='"""+str(p['source_of_document'])+"""',
			source_document_specify='"""+str(p['source_document_specify'])+"""', remarks='"""+str(p['remarks'])+"""', 
			status='"""+str(p['status'])+"""',description='"""+str(descr)+"""', series_number='"""+str(p['series_number'])+"""'
			where resolution_id='"""+str(p['resolution_id'])+"""'
		"""
		cud(update)

		# new update

		delete_authors="delete from tbl_resolution_author where resolution_id='"+str(p['resolution_id'])+"'"
		cud(delete_authors)

		delete_co_authors="delete from tbl_resolution_co_author where resolution_id='"+str(p['resolution_id'])+"'"
		cud(delete_co_authors)

		delete_sponsor="delete from tbl_resolution_sponsor where resolution_id='"+str(p['resolution_id'])+"'"
		cud(delete_sponsor)

		delete_committee="delete from tbl_committee_ref_resolution where resolution_id='"+str(p['resolution_id'])+"'"
		cud(delete_committee)

		for i in p['ref_committee'][0]:
			insert_committee="insert into tbl_committee_ref_resolution set  committee_id='"+str(i)+"', resolution_id='"+str(p['resolution_id'])+"', date_reffered=now()"
			cud(insert_committee)


		if 'input_authors' in p:
			for i in p['input_authors']:
				insert_author="insert into tbl_resolution_author set author='"+str(i)+"', resolution_id='"+str(p['resolution_id'])+"'"
				cud(insert_author)

		if 'input_co_authors' in p:
			for i in p['input_co_authors']:
				insert_co_author="insert into tbl_resolution_co_author set co_author='"+str(i)+"', resolution_id='"+str(p['resolution_id'])+"'"
				cud(insert_co_author)

		if 'input_sponsor' in p:
			for i in p['input_sponsor']:
				insert_sponsor="insert into tbl_resolution_sponsor set sponsor='"+str(i)+"', resolution_id='"+str(p['resolution_id'])+"'"
				cud(insert_sponsor)

		if 'input_cosponsor' in p:
			for i in p['input_cosponsor']:
				insert_cosponsor="insert into tbl_resolution_cosponsor set cosponsor='"+str(i)+"', resolution_id='"+str(p['resolution_id'])+"'"
				cud(insert_cosponsor)

		x=-1
		y=-1
		z=-1
		for filename_array in request.files:
			split=filename_array.split("[")
			if str(split[0])=="file_attach":
				x=x+1
				file_name="file_attach["+str(x)+"]"

				file=request.files[filename_array]

				n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution" / str(p['resolution_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = str(custom_secure_filename(file.filename)).replace("'","''")
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_files_resolution//"+str(p['resolution_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					file_ = str(file.filename).replace("'","''")
					insert2="insert into tbl_resolution_file set filename='"+str(file_)+"', path='"+str(path_location)+"', resolution_id='"+str(p['resolution_id'])+"'"
					cud(insert2)

				# file minutes  ---------------------------------->

			if str(split[0])=="file_minutes":
				y=y+1
				file_name_min="file_minutes["+str(y)+"]"

				file=request.files[file_name_min]
				n_path = Path(__file__).parent / "../static/uploads/upload_files_resolution_minutes" / str(p['resolution_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = str(custom_secure_filename(file.filename)).replace("'","''")
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_files_resolution_minutes//"+str(p['resolution_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					file_ = str(file.filename).replace("'","''")
					insert_tbl_minutes_path="insert into tbl_minutes_resolution_path set filename='"+str(file_)+"', path='"+str(path_location)+"', minutes_id='"+str(p['resolution_id'])+"'"
					cud(insert_tbl_minutes_path)

			if str(split[0])=="file_veto":
				z=z+1
				file_name_min="file_veto["+str(z)+"]"

				file=request.files[file_name_min]
				n_path = Path(__file__).parent / "../static/uploads/upload_veto_resolution" / str(p['resolution_id'])
				n_path.resolve()
				
				if file and allowed_file(file.filename):
					filename = str(custom_secure_filename(file.filename)).replace("'","''")
					if not Path.exists(n_path):
						Path.mkdir(n_path)
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					else:
						app.config['UPLOAD_FOLDER']=n_path
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

					location1="upload_veto_resolution//"+str(p['resolution_id'])
					location1.replace("//", "\\\\");
					location=location1+"/"+filename
					path_location=location.replace("/", "\\\\");
					file_ = str(file.filename).replace("'","''")
					insert_veto="insert into tbl_veto_resolution set filename='"+str(file_)+"', path='"+str(path_location)+"', resolution_id='"+str(p['resolution_id'])+"'"
					cud(insert_veto)

		sel_res="select * from tbl_resolution where resolution_id='"+str(p['resolution_id'])+"'"
		rd_reso=pyread(sel_res)

		if p['status']=="1":
			doc_status = "Proposed Resolution"
		elif p['status']=="2":
			doc_status = "2nd Reading Resolution"
		elif p['status']=="3":
			doc_status = "3rd Reading Resolution"
		elif p['status']=="4":
			doc_status = "3rd Reading Resolution Excemption"
		elif p['status']=="5":
			doc_status = "For mayors Approval"
		elif p['status']=="6":
			doc_status = "Approved Resolution"
		elif p['status']=="7":
			doc_status = "Veto Resolution"

		if p['tracking_no']:
			select_tracking = """
				select track_gen_id from tbl_document_tracking where tracking_no='"""+str(p['tracking_no'])+"""',
			"""
			rd_sel_tracking = pyread(select_tracking)

			
			insert_tracking_status = """
				insert into tbl_document_tracking_status  set track_gen_id='"""+str(rd_sel_tracking[0]['track_gen_id'])+"""', status='Approved', date=now()
			"""
			cud(insert_tracking_status)

		return jsonify("Succesfuly Updated")


@query.route('/save_new_password', methods=['GET', 'POST'])
@login_required
def save_new_password():
	p=json.loads(request.data)
	if p['h_user']=="0" or p['h_user']==0:
		if str(p['new_pass'])==str(p['confirm_pass']):
			insert="insert into tbl_login set username='"+str(p['new_username'])+"',password='"+str(p['confirm_pass'])+"',fullname='"+str(p['fullname'])+"',type=1"
			cud(insert)
			return jsonify("Succesfuly Saved")
		else:
			return jsonify("Password did not match")
	else:
		sel="select * from tbl_login where password='"+str(p['old_pass'])+"'"
		rd=pyread(sel)
		if rd:
			if str(rd[0]['username'])!="":
				if str(p['new_pass'])==str(p['confirm_pass']):
					update="update tbl_login set username='"+str(p['new_username'])+"', password='"+str(p['confirm_pass'])+"', fullname='"+str(p['fullname'])+"' where login_id='"+str(p['h_user'])+"'"
					cud(update)
					return jsonify("Succesfuly Updated")
				else:
					return jsonify("Password did not match")
		else:
			return jsonify("Password is incorrect")


@query.route('/delete_user', methods = ['POST','GET'])
@login_required
def delete_user():
	try:
		p  = json.loads(request.data)
		del_f = "delete from tbl_login where login_id = '"+str(p['h_user'])+"'"
		cud(del_f)
		return jsonify("Deleted Succesfuly")
	except Exception as e:
		return e


@query.route('/delete_ordinance_file', methods=['GET', 'POST'])
@login_required
def delete_ordinance_file():
	p=json.loads(request.data)
	sel="select * from tbl_ordinance_file where ordinance_file_id='"+str(p['ordinance_file_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_ordinance_file where ordinance_file_id='"+str(p['ordinance_file_id'])+"'"
			cud(delete)

			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_ordinance_file where ordinance_file_id='"+str(p['ordinance_file_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_resolution_file', methods=['GET', 'POST'])
@login_required
def delete_resolution_file():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_file where resolution_file_id='"+str(p['resolution_file_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_resolution_file where resolution_file_id='"+str(p['resolution_file_id'])+"'"
			cud(delete)

			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_resolution_file where resolution_file_id='"+str(p['resolution_file_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_committee_ordinance_minutes', methods=['GET', 'POST'])
@login_required
def delete_committee_ordinance_minutes():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_ordinance 
		where ordinance_minutes_committee_id='"""+str(p['ordinance_minutes_committee_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_ordinance_minutes_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_minutes_path_committee_ordinance 
				where ordinance_minutes_committee_id='"""+str(p['ordinance_minutes_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_minutes_path_committee_ordinance 
				where ordinance_minutes_committee_id='"""+str(p['ordinance_minutes_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_committee_resolution_minutes', methods=['GET', 'POST'])
@login_required
def delete_committee_resolution_minutes():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_resolution 
		where minutes_path_committee_resolution_id='"""+str(p['minutes_path_committee_resolution_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_resolution_minutes_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_minutes_path_committee_resolution 
				where minutes_path_committee_resolution_id='"""+str(p['minutes_path_committee_resolution_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_minutes_path_committee_resolution 
				where minutes_path_committee_resolution_id='"""+str(p['minutes_path_committee_resolution_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_committee_petition_minutes_file', methods=['GET', 'POST'])
@login_required
def delete_committee_petition_minutes_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_minutes_path_committee_petition 
		where minutes_path_committee_petition_id='"""+str(p['minutes_path_committee_petition_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_petition_minutes_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_minutes_path_committee_petition 
				where minutes_path_committee_petition_id='"""+str(p['minutes_path_committee_petition_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_minutes_path_committee_petition 
				where minutes_path_committee_petition_id='"""+str(p['minutes_path_committee_petition_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")

@query.route('/delete_committee_ordinance_file', methods=['GET', 'POST'])
@login_required
def delete_committee_ordinance_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_ordinance_file_committee 
		where ordinance_id='"""+str(p['ordinance_id'])+"""' and
		committee_id='"""+str(p['committee_id'])+"""' and ordinance_file_committee_id='"""+str(p['ordinance_file_committee_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_ordinance_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_ordinance_file_committee 
				where ordinance_id='"""+str(p['ordinance_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and ordinance_file_committee_id='"""+str(p['ordinance_file_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_ordinance_file_committee 
				where ordinance_id='"""+str(p['ordinance_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and ordinance_file_committee_id='"""+str(p['ordinance_file_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_committee_resolution_file', methods=['GET', 'POST'])
@login_required
def delete_committee_resolution_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_resolution_file_committee 
		where resolution_id='"""+str(p['resolution_id'])+"""' and
		committee_id='"""+str(p['committee_id'])+"""' and resolution_file_committee_id='"""+str(p['resolution_file_committee_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_resolution_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_resolution_file_committee 
				where resolution_id='"""+str(p['resolution_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and resolution_file_committee_id='"""+str(p['resolution_file_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_resolution_file_committee 
				where resolution_id='"""+str(p['resolution_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and resolution_file_committee_id='"""+str(p['resolution_file_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_committee_petition_file', methods=['GET', 'POST'])
@login_required
def delete_committee_petition_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_petition_path_committee 
		where petition_id='"""+str(p['petition_id'])+"""' and
		committee_id='"""+str(p['committee_id'])+"""' and petition_path_committee_id='"""+str(p['petition_path_committee_id'])+"""'
	"""
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / "upload_committee_petition_files"
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="""
				delete from tbl_petition_path_committee 
				where petition_id='"""+str(p['petition_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and petition_path_committee_id='"""+str(p['petition_path_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="""
				delete from tbl_petition_path_committee 
				where petition_id='"""+str(p['petition_id'])+"""' and committee_id='"""+str(p['committee_id'])+"""'
				and petition_path_committee_id='"""+str(p['petition_path_committee_id'])+"""'
			"""
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")


@query.route('/delete_minutes_file', methods=['GET', 'POST'])
@login_required
def delete_minutes_file():
	p=json.loads(request.data)
	delete = """
		delete from tbl_minutes_path where minutes_path_id='"""+str(p['minutes_path_id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly deleted")

@query.route('/delete_minutes_file2', methods=['GET', 'POST'])
@login_required
def delete_minutes_file2():
	p=json.loads(request.data)

	delete = """
		delete from tbl_minutes_raw_path where minutes_path_id='"""+str(p['minutes_path_id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly deleted")


@query.route('/delete_veto_ordinance_file', methods=['GET', 'POST'])
@login_required
def delete_veto_ordinance_file():
	p=json.loads(request.data)
	delete="delete from tbl_veto_ordinance where veto_ordinance_id='"+str(p['veto_ordinance_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_veto_ordinance" / str(p['ordinance_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/delete_veto_resolution_file', methods=['GET', 'POST'])
@login_required
def delete_veto_resolution_file():
	p=json.loads(request.data)
	delete="delete from tbl_veto_resolution where veto_resolution_id='"+str(p['veto_resolution_id'])+"'"
	cud(delete)
	n_path = Path(__file__).parent / "../static/uploads/upload_veto_resolution" / str(p['resolution_id'])
	n_path.resolve()
	if Path.exists(n_path):
		shutil.rmtree(n_path)
	return jsonify("Succesfuly Deleted")


@query.route('/get_session_video', methods = ['GET','POST'])
def get_session_video():
	p=json.loads(request.data)
	sel= """
		select * from tbl_session_video where session_id='"""+str(p['session_id'])+"""'
	"""
	rd = pyread(sel)
	return jsonify(rd)

@query.route('/get_session_data', methods = ['GET','POST'])
def get_session_data():
	try:
		p = json.loads(request.data)
		sel_session = """ SELECT
			* , CONCAT(tpi.f_name,' ',tpi.m_name, ' ', tpi.l_name) as fullname
		FROM
			tbl_session ts
			LEFT JOIN tbl_personal_info tpi ON ts.closing_prayer = tpi.info_id
		WHERE
			session_id ='"""+str(p['session_id'])+"""' """ 
		res_ses = pyread(sel_session)


		sel_roll_call = "select *,CONCAT(tri.f_name,' ',tri.m_name, ' ', tri.l_name) as fullname FROM tbl_session_roll_call tsrc LEFT JOIN tbl_personal_info tri on tsrc.info_id = tri.info_id WHERE tsrc.session_id = '"+str(p['session_id'])+"'"
		res_rl = pyread(sel_roll_call)

		session_data = {
			"sess_data": res_ses,
			"sess_roll_call" : res_rl,
		}
		return jsonify(session_data)
	except Exception as e:
		return e

@query.route('/get_tracking', methods=['GET', 'POST'])
@login_required
def get_tracking():
	sel="select * from tbl_document_tracking"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_committee', methods=['GET', 'POST'])
@login_required
def del_committee():
	p=json.loads(request.data)
	delete="delete from tbl_committee where committee_id='"+str(p['committee_id'])+"'" 
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/delete_accounts', methods=['GET', 'POST'])
@login_required
def delete_accounts():
	p=json.loads(request.data)
	delete="delete from tbl_personal_info where info_id='"+str(p['info_id'])+"'" 
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/get_OOB', methods = ['GET','POST'])
def get_OOB():
	try:
		p = json.loads(request.data)
		sel_session = """ 
			SELECT * , CONCAT(tpi.f_name,' ',tpi.m_name, ' ', tpi.l_name) as fullname
			FROM
				tbl_session ts
				LEFT JOIN tbl_personal_info tpi ON ts.closing_prayer = tpi.info_id
			WHERE
				session_id ='"""+str(p['session_id'])+"""'
		"""
		res_ses = pyread(sel_session)

		if len(res_ses)!=0:
			#  ROLL CALL

			sel_roll_call = "select *,CONCAT(tri.f_name,' ',tri.m_name, ' ', tri.l_name) as fullname FROM tbl_session_roll_call tsrc LEFT JOIN tbl_personal_info tri on tsrc.info_id = tri.info_id WHERE tsrc.session_id = '"+str(res_ses[0]['session_id'])+"'"
			res_rc = pyread(sel_roll_call)

			# reading privious minutes

			sel_priv_min = """
				select concat(tm.minutes_no,' ',ts.sp_title) title ,tm.date dated , tmrp.path document_file 
				from tbl_session_reading_minutes tsrm
				left join tbl_minutes tm on tm.minutes_id=tsrm.minutes_id
				left join tbl_minutes_raw_path tmrp on tmrp.minutes_id=tm.minutes_id
				left join tbl_sp ts on ts.sp_id=tm.sp_id
				where session_id = '"""+str(res_ses[0]['session_id'])+"""'
				group by tsrm.minutes_id
			"""
			res_priv_min = pyread(sel_priv_min)

			# question privilege

			sel_question = """
				select *, (select path from tbl_session_question_hour_path tsqhp
				where tsqhp.session_id='"""+str(res_ses[0]['session_id'])+"""' GROUP BY session_id) file
				from tbl_session_question_hour 
				where session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_ques = pyread(sel_question)

			#  privilege hour
			sel_privilege_hour = """
				select concat(tpi.f_name,' ', tpi.m_name,' ', tpi.l_name) councilor ,
				(select group_concat(path) from tbl_session_privilege_path tspp
				where tspp.session_id='"""+str(res_ses[0]['session_id'])+"""') file
				from tbl_session_previlege_hour tsph
				left join tbl_personal_info tpi on tpi.info_id=tsph.councilor_info_id
				where session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_priv = pyread(sel_privilege_hour)

			# Reading and refferences of bussiness

			# propose ordinance ---- >

			sel_rrb_ord = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 
				where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_proposed_ordi tspo
				left join tbl_document_tracking tdt on tdt.track_gen_id=tspo.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tspo.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_ord = pyread(sel_rrb_ord)

			# end propose ordinance ---- >

			# propose resolution ---- >

			sel_rrb_res = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_proposed_reso tspr
				left join tbl_document_tracking tdt on tdt.track_gen_id=tspr.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tspr.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_res = pyread(sel_rrb_res)

			# end propose resolution ---- >

			# petition ---- >

			sel_rrb_pet = """
				select  tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tspfr.type
				from tbl_session_petition_for_refferal tspfr
				left join tbl_document_tracking tdt on tdt.track_gen_id=tspfr.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tspfr.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_pet = pyread(sel_rrb_pet)

			# end petition ---- >

			# additional petition ---- >

			sel_rrb_addition = """
				select  tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tsar.type
				from tbl_session_additional_refferal tsar
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsar.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsar.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_addition = pyread(sel_rrb_addition)

			# end additional petition ---- >

			# veto message ---- >

			sel_rrb_veto = """
				select  tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee) committee
				from tbl_session_veto_reading tsvr
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsvr.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left join tbl_committee tc on tc.committee_id=tdtr.committtee
				where tsvr.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_veto = pyread(sel_rrb_veto)

			# end veto message ---- >

			# committee report

			sel_rrb_committee_report = """
				select committee, committee_report_no ,
				(select group_concat(path) from tbl_session_committee_report_path tscrp 
				where tscrp.session_id='"""+str(res_ses[0]['session_id'])+"""') file
				from tbl_session_committee_report tscr
				left join tbl_committee tc on tc.committee_id=tscr.committee_id
				where tscr.session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_rrb_committee_report = pyread(sel_rrb_committee_report)

			# end committee report

			# committee information

			sel_rrb_committee_information = """
				select committee, committee_information_no ,
				(select group_concat(path) from tbl_session_committee_information_path tscip 
				where tscip.session_id='"""+str(res_ses[0]['session_id'])+"""') file
				from tbl_session_committee_information tsci
				left join tbl_committee tc on tc.committee_id=tsci.committee_id
				where tsci.session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_rrb_committee_information = pyread(sel_rrb_committee_information)

			# end committee report


			# unfinish bussiness ---- >

			sel_rrb_unfinish = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 
				where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_unfinished_bussiness tsub
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsub.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsub.session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_rrb_unfinish = pyread(sel_rrb_unfinish)

			# end unfinish bussiness ---- >

			# bussiness of the day ---- >

			sel_rrb_botd = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_botd tsb
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsb.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsb.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_botd = pyread(sel_rrb_botd)

			# end bussiness of the day ---- >

			# urgent ---- >

			sel_rrb_urgent = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_urgent tsu
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsu.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsu.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_urgent = pyread(sel_rrb_urgent)

			# end urgent ---- >

			# just inserted ---- >

			sel_rrb_just_inserted = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_just_inserted tsji
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsji.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsji.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_just_inserted = pyread(sel_rrb_just_inserted)

			# end just inserted ---- >


			# calendar measure ---- >

			sel_rrb_calendar_measure = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_calendar_measure tscm
				left join tbl_document_tracking tdt on tdt.track_gen_id=tscm.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tscm.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_calendar_measure = pyread(sel_rrb_calendar_measure)

			# end just inserted ---- >


			# new measure ---- >

			sel_rrb_new_measure = """
				select tdt.track_gen_id,tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee SEPARATOR ' - ') committee, tdt.doc_status
				from tbl_session_new_measure tsnm
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsnm.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
				where tsnm.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_new_measure = pyread(sel_rrb_new_measure)

			# end just inserted ---- >


			# bussiness third ---- >

			sel_rrb_bussiness_third = """
				select  tdt.title,tdt.tracking_no,
				(select group_concat(tdt2.path) x from tbl_document_tracking_path tdt2 where tdt2.track_gen_id = tdt.track_gen_id) document_file,
				group_concat(tc.committee) committee, tdt.doc_status
				from tbl_session_bussiness_third tsbt
				left join tbl_document_tracking tdt on tdt.track_gen_id=tsbt.tracking_no
				left join tbl_document_tracking_path tdtp on tdtp.track_gen_id=tdt.track_gen_id
				left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
				left join tbl_committee tc on tc.committee_id=tdtr.committtee
				where tsbt.session_id = '"""+str(res_ses[0]['session_id'])+"""'
				GROUP BY tdt.track_gen_id
			"""
			res_rrb_bussiness_third = pyread(sel_rrb_bussiness_third)

			# end just inserted ---- >

			# End Reading and refferences of bussiness

			# summary correction

			sel_summary= """
				select tssc.new_title, tssc.old_title , tdt.tracking_no
				from tbl_session_summary_correction tssc
				left join tbl_document_tracking tdt on tdt.track_gen_id=tssc.tracking_no
				where session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_summary = pyread(sel_summary)

			# end summary correction

			# Announcement

			sel_announcement= """
				select CONCAT(tpi.f_name,' ',tpi.m_name, ' ', tpi.l_name) as fullname,announcement ,
				(select group_concat(path) from tbl_session_announcement_path tsap 
				where tsap.session_id='"""+str(res_ses[0]['session_id'])+"""') file
				from tbl_session_announcement tsa
				left join tbl_personal_info tpi on tpi.info_id=tsa.councilor
				where tsa.session_id = '"""+str(res_ses[0]['session_id'])+"""'
			"""
			res_announcement = pyread(sel_announcement)

			# Code refferences

			sel_code= """
				select title, type, path from tbl_documents_refferals tdr
				left join tbl_documents_refferals_path tdrp on tdrp.documents_refferals_id=tdr.documents_refferals_id
			"""
			res_code = pyread(sel_code)

			# end code refferences

			session_data = {
				"sess_data": res_ses,
				"sess_roll_call": res_rc,
				"sess_priv_min" : res_priv_min,
				"sess_question": res_ques,
				"sess_priv_hour": res_priv,
				"sess_reading_ord": res_rrb_ord,
				"sess_reading_res": res_rrb_res,
				"sess_reading_pet": res_rrb_pet,
				"sess_reading_additional_ref": res_rrb_addition,
				"sess_reading_veto": res_rrb_veto,
				"sess_commitee_report": res_rrb_committee_report,
				"sess_commitee_information":res_rrb_committee_information,
				"sess_reading_unfinish":res_rrb_unfinish,
				"sess_reading_botd":res_rrb_botd,
				"sess_reading_urgent":res_rrb_urgent,
				"sess_reading_just_inserted":res_rrb_just_inserted,
				"sess_reading_calendar_measure": res_rrb_calendar_measure,
				"sess_reading_new_measure":res_rrb_new_measure,
				"sess_reading_bussiness_third":res_rrb_bussiness_third,
				"sess_summary":res_summary,
				"sess_announcement": res_announcement, 
				"sess_code_ref": res_code,
			}

			return jsonify(session_data)
		else:
			session_data = {
				"sess_data": [],
			}
			return jsonify(session_data)
	except Exception as e:
		return e


@query.route('/get_calendar_business', methods = ['GET','POST'])
def get_calendar_business():
	try:
		sel_session = """
			SELECT
				* , CONCAT(tpi.f_name,' ',tpi.m_name, ' ', tpi.l_name) as fullname
			FROM
				tbl_session ts
				LEFT JOIN tbl_personal_info tpi ON ts.closing_prayer = tpi.info_id 
				LEFT JOIN tbl_sp tsp ON tsp.sp_id = ts.sp_number
			where tsp.`status`='ACTIVE'
			ORDER BY ts.session_date DESC
		"""
		res_ses = pyread(sel_session)
		return jsonify(res_ses)
	except Exception as e:
		return e

@query.route('/get_minuteReading', methods = ['POST','GET'])
@login_required
def get_minuteReading():
	try:
		p = json.loads(request.data)
		sel = """
			SELECT
				* 
			FROM
				tbl_minutes tm
				LEFT JOIN tbl_minutes_path tmp ON tm.minutes_id = tmp.minutes_id where `date` = '"""+str(p['minutes_date'])+"""'
		"""
		res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		return e

@query.route('/get_councilor_photo', methods=['GET', 'POST'])
@login_required
def get_councilor_photo():
	sel="""
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi on tpi.info_id=sm.sp_mayor
		where status='active' 

		union all
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi2 on tpi2.info_id=sm.sp_vice_mayor
		where status='active'

		union all
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi2 on tpi2.info_id=sm.sp_secretary
		where status='active'

		union all
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi2 on tpi2.info_id=sm.sp_vice_mayor
		where status='active'

		union all
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi2 on tpi2.info_id=sm.sp_vice_mayor
		where status='active'

		union all
		select * from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi2 on tpi2.info_id=sm.sp_vice_mayor
		where status='active'
	""" 
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_third_ordinance', methods = ['POST','GET'])
@login_required
def get_third_ordinance():
	try:
		sel = "select * from tbl_ordinance"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_third_resolution', methods = ['POST','GET'])
@login_required
def get_third_resolution():
	try:
		sel = "select * from tbl_resolution"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_referals', methods = ['POST','GET'])
@login_required
def get_referals():
	try:
		sel = "select * from tbl_documents_refferals"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_commitee', methods = ['POST','GET'])
@login_required
def get_commitee():
	try:
		sel = "select * from tbl_committee"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/save_oob', methods = ['POST','GET'])
@login_required
def save_oob():
	try:
		p =json.loads(request.data)
		if p['session_id']!=0:

			if p['attendance']:
				if len(p['attendance'])!=0:
					for x in p['attendance']:
						upt = "update tbl_session_roll_call set status = '"+str(x['roll_call'])+"' where roll_call_id = '"+str(x['roll_call_id'])+"' and session_id = '"+str(p['session_id'])+"'"
						cud(upt)

			if p['reading']:
				if len(p['reading']):
					for x in p['reading']:
						upt = "update tbl_minutes set movant = '"+str(x['movant'])+"', seconder = '"+str(x['seconder'])+"' where minutes_id = '"+str(x['minutes_id'])+"' "
						cud(upt)

			if p['proposed_ordinance']:
				if len(p['proposed_ordinance'])!=0:
					for x in p['proposed_ordinance']:
						upt = "update tbl_ordinance set committee_id = '"+str(x['committee'])+"'  where ordinance_id = '"+str(x['ordinance_id'])+"' "
						cud(upt)

			if p['proposed_resolution']:
				if len(p['proposed_resolution'])!=0:
					for x in p['proposed_resolution']:
						upt = "update tbl_resolution set committee_id = '"+str(x['committee'])+"'  where resolution_id = '"+str(x['resolution_id'])+"' "
						cud(upt)

			if p['petition']:
				if len(p['petition'])!=0:
					for x in p['petition']:
						# upt = "update tbl_petition set status = '"+str(x['action'])+"'  where petition_id = '"+str(x['petition_id'])+"' "
						# cud(upt)

						if x['committee']:
							upt1 = "update tbl_petition_path_committee set committee_id = '"+str(x['committee'])+"' where petition_id = '"+str(x['petition_id'])+"'"
							cud(upt1)

			if p['sec_ordinance']:
				if len(p['sec_ordinance'])!=0:
					for x in p['sec_ordinance']:
						prnt_B("")
						# upt = "update tbl_ordinance set status = '"+str(x['status'])+"' where ordinance_id = '"+str(x['ordinance_id'])+"' "
						# cud(upt)
			if p['sec_resolution']:
				if len(p['sec_resolution'])!=0:
					for x in p['sec_resolution']:
						prnt_B("")
						# upt = "update tbl_resolution set status = '"+str(x['status'])+"'  where resolution_id = '"+str(x['resolution_id'])+"'"
						# cud(upt)

			if p['urgent_ordinance']:
				if len(p['urgent_ordinance'])!=0:
					for x in p['urgent_ordinance']:
						prnt_B("")
						# upt = "update tbl_ordinance set status = '"+str(x['status'])+"' where ordinance_id = '"+str(x['ordinance_id'])+"' "
						# cud(upt)

			if p['urgent_resolution']:
				if len(p['urgent_resolution'])!=0:

					for x in p['urgent_resolution']:
						prnt_B("third reso nothing")
						# upt = "update tbl_resolution set status = '"+str(x['status'])+"'  where resolution_id = '"+str(x['resolution_id'])+"'"
						# cud(upt)

			if p['third_ordinance']:
				if len(p['third_ordinance'])!=0:
					for x in p['third_ordinance']:
						prnt_B("third ordi nothing")
						# upt = "update tbl_ordinance set status = '"+str(x['status'])+"' where ordinance_id = '"+str(x['ordinance_id'])+"' "
						# cud(upt)

			if p['third_resolution']:
				if len(p['third_resolution'])!=0:
					for x in p['third_resolution']:
						prnt_B("")
						# upt = "update tbl_resolution set status = '"+str(x['status'])+"'  where resolution_id = '"+str(x['resolution_id'])+"'"
						# cud(upt)
			return jsonify({"message":"Session Saved!"})
	except Exception as e:
		return e

@query.route('/get_active_councilor', methods = ['POST','GET'])
@login_required
def get_active_councilor():
	try:
		sel = """
			SELECT
				*,
				CONCAT( tpi.f_name, ' ', tpi.m_name, ' ', tpi.l_name ) fullname 
			FROM
				sp_councilor sc
				LEFT JOIN sp_member sm ON sc.sp_member_id = sm.sp_member_id
				LEFT JOIN tbl_sp ts ON sm.sp_id = ts.sp_id
				LEFT JOIN tbl_personal_info tpi ON tpi.info_id = sc.councilor 
				LEFT JOIN tbl_committee tc ON tc.chairman = CONCAT( tpi.f_name, ' ', tpi.m_name, ' ', tpi.l_name )
			WHERE
				ts.`status` = "Active"
		"""
		res = pyread(sel)


		if res:
			print('in1')
			if len(res)!=0:
				print('in1')
				for x in res:
					print('ordinance')
					sel2 = "select count(*) total from tbl_ordinance where author = '"+str(x['fullname'])+"' and sp_id = '"+str(res[0]['sp_id'])+"'  and `status` = 6"
					res2 = pyread(sel2)
					x['ordinance'] = res2

				for y in res:
					print('reso')
					sel3 = "select count(*) total from tbl_resolution where author  = '"+str(y['fullname'])+"' and sp_id = '"+str(res[0]['sp_id'])+"' and `status` = 6"
					res3 = pyread(sel3)
					y['resolution'] = res3


				for i in res:
					print('petetion')
					sel4 = "select count(*) total from tbl_petition where source_of_document = '"+str(i['fullname'])+"' AND action_taken = 1"
					res4 = pyread(sel4)
					i['petition'] = res4
		return jsonify(res)
	except Exception as e:
		return e

@query.route('/get_minutes_selected', methods = ['POST','GET'])
@login_required
def get_minutes_selected():
	try:
		p = json.loads(request.data)
		res = []
		if p['data_id'] == 1 or p['data_id'] == '1':
			sel = "SELECT resolution_id as ids,resolution_title as title FROM tbl_resolution tr"
			res = pyread(sel)
		elif p['data_id'] == 2 or p['data_id'] == '2':
			# ordinance
			sel = "SELECT ordinance_id as ids,ordinance_title as title FROM tbl_ordinance"	
			res = pyread(sel)
		elif p['data_id'] == 3 or p['data_id'] == '3':
			# petetion
			sel = "SELECT petition_id as ids,title as title FROM tbl_petition"
			res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		return e

@query.route('/get_data_reso_ordi_peti', methods = ['POST', 'GET'])
@login_required
def get_data_reso_ordi_peti():
	try:
		p = json.loads(request.data)
		res = []
		if p['type_id'] == 1 or p['type_id'] == '1':
			# res0
			sel = """
				SELECT
					* 
				FROM
					tbl_resolution tr
					where tr.resolution_id = '"""+str(p['ids'])+"""'
			"""
			res = pyread(sel)
			sel1 = "select * from tbl_minutes_resolution_path where minutes_id = '"+str(res[0]['minutes_id'])+"'"
			res[0]["minutes_data"] = pyread(sel1)
		elif p['type_id'] == 2 or p['type_id'] == '2':
			# ordi
			sel = """
				SELECT
					* 
				FROM
					tbl_ordinance `to`
					where `to`.ordinance_id = '"""+str(p['ids'])+"""'
			"""
			res = pyread(sel)
			sel1 = "select * from tbl_minutes_path where minutes_id = '"+str(res[0]['minutes_id'])+"'"
			res[0]["minutes_data"] = pyread(sel1)
		elif p['type_id'] == 3 or p['type_id'] == '3':
			# petition
			sel = """
				SELECT
					* 
				FROM
					tbl_petition tp
					WHERE
					tp.petition_id = '"""+str(p['ids'])+"""'
			"""
			res = pyread(sel)
			sel1 = "select * from tbl_petition_path where petition_id = '"+str(res[0]['petition_id'])+"'"
			res[0]["petition_data"] = pyread(sel1)
		return jsonify(res)
	except Exception as e:
		return e

@query.route('/get_logo', methods = ['POST','GET'])
def get_logo():
	try:
		sel = "select * from tbl_sp where status = 'Active' "
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_track_document_reso', methods = ['POST','GET'])
@login_required
def get_track_document_reso():
	sel="""
		select *, (case when `status`=1 THEN
			concat("Propose ",' ', "RESOLUTION")
			when `status`=2 THEN
			concat("2nd Reading ",' ', "RESOLUTION")
			when `status`=3 THEN
			concat("3nd Reading ",' ', "RESOLUTION")
			when `status`=4 THEN
			concat("3nd Reading Rule Excemtion ",' ', "RESOLUTION")
			when `status`=5 THEN
			concat("For Mayor's Approval ",' ', "RESOLUTION")
			when `status`=6 THEN
			concat("Approved ",' ', "RESOLUTION")
			when `status`=7 THEN
			concat("Veto ",' ', "RESOLUTION")
			when `status`=8 THEN
			concat("Archived ",' ', "RESOLUTION")
			else
				`status`
			END
		) stats, "RESOLUTION" type_document
		from tbl_resolution tbr
		left join tbl_committee tc on tc.committee_id=tbr.committee_id

	"""
	rd=pyread(sel)
	return jsonify(rd)



@query.route('/get_track_document_pet', methods = ['POST','GET'])
@login_required
def get_track_document_pet():
	sel="""
		select *,(case when `status`=1 THEN
			concat("Propose ",' ', "PETETION")
			when `status`=2 THEN
			concat("2nd Reading ",' ', "PETETION")
			when `status`=3 THEN
			concat("3nd Reading ",' ', "PETETION")
			when `status`=4 THEN
			concat("3nd Reading Rule Excemtion ",' ', "PETETION")
			when `status`=5 THEN
			concat("For Mayor's Approval ",' ', "PETETION")
			when `status`=6 THEN
			concat("Approved ",' ', "PETETION")
			when `status`=7 THEN
			concat("Veto ",' ', "PETETION")
			when `status`=8 THEN
			concat("Archived ",' ', "PETETION")
			else
				`status`
			END
		) stats, "PETETION" type_document
		from tbl_petition tp
		left join tbl_petition_path_committee tppc on tppc.petition_id=tp.petition_id
		left join tbl_committee tc on tc.committee_id=tppc.committee_id
	"""
	rd=pyread(sel)
	return jsonify(rd)



@query.route('/get_track_document_ord', methods = ['POST','GET'])
@login_required
def get_track_document_ord():
	sel="""
		select *,(case when `status`=1 THEN
			concat("Propose ",' ', "ORDINANCE")
			when `status`=2 THEN
			concat("2nd Reading ",' ', "ORDINANCE")
			when `status`=3 THEN
			concat("3nd Reading ",' ', "ORDINANCE")
			when `status`=4 THEN
			concat("3nd Reading Rule Excemtion ",' ', "ORDINANCE")
			when `status`=5 THEN
			concat("For Mayor's Approval ",' ', "ORDINANCE")
			when `status`=6 THEN
			concat("Approved ",' ', "ORDINANCE")
			when `status`=7 THEN
			concat("Veto ",' ', "ORDINANCE")
			when `status`=8 THEN
			concat("Archived ",' ', "ORDINANCE")
			else
				`status`
			END
		) stats, "ORDINANCE" type_document
		from tbl_ordinance tbr
		left join tbl_committee tc on tc.committee_id=tbr.committee_id
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_login', methods = ['POST','GET'])
@login_required
def get_login():
	try:
		sel = "select *, (case when role=1 then 'User' else 'Admin' end) access, GROUP_CONCAT(tla.routes) arr from tbl_login tl left join tbl_login_access tla on tl.login_id=tla.login_id group by tl.login_id"
		rd=pyread(sel)
		return jsonify(rd)
	except Exception as e:
		return e
		
@query.route('/get_report_integrated', methods = ['POST','GET'])
@login_required
def get_report_integrated():
	try:
		p= json.loads(request.data)
		sel = "select * from tbl_document_tracking group by tracking_no"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/delete_budget', methods = ['POST','GET'])
@login_required
def delete_budget():
	try:
		p = json.loads(request.data)
		del_b = "delete from tbl_sp_budget where sp_budget_id = '"+p['budget_id']+"'"
		cud(del_b)
		delete="delete from tbl_sp_budget_balance where sp_budget_id='"+str(p['budget_id'])+"'"
		cud(delete)
		return jsonify("Deleted Succesfuly")
	except Exception as e:
		return e


@query.route('/get_tbl_announcement', methods = ['POST','GET'])
@login_required
def get_tbl_announcement():
	sel="select *, date_format(date_announce,'%W %b-%m-%Y') dated from tbl_announcement"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_announcement', methods = ['POST','GET'])
@login_required
def save_announcement():
	p = json.loads(request.data)
	if p['h_announce_id']=="0" or p['h_announce_id']=="0":
		insert="insert into tbl_announcement set announcement_title='"+str(p['title'])+"', announcement='"+str(p['announcement'])+"', status='"+str(p['status_annoucement'])+"', date_announce=curdate()"
		cud(insert)
		return jsonify("Succesfuly Saved")
	else:
		update="update tbl_announcement set announcement_title='"+str(p['title'])+"', announcement='"+str(p['announcement'])+"', status='"+str(p['status_annoucement'])+"', date_announce=curdate() where announcement_id='"+str(p['h_announce_id'])+"'"
		cud(update)
		return jsonify("Succesfuly Saved")


@query.route('/delete_announcement', methods = ['POST','GET'])
@login_required
def delete_announcement():
	p = json.loads(request.data)
	delete="delete from tbl_announcement where announcement_id='"+str(p['announcement_id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Saved")

@query.route('/get_announcement', methods = ['POST','GET'])
@login_required
def get_announcement():
	try:
		sel = "select * from tbl_announcement where status = 'Active' "
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_all_active_councilor', methods = ['POST','GET'])
@login_required
def get_all_active_councilor():
	try:
		sel = """SELECT
			tpi.info_id,
			concat( f_name, ' ', m_name, ' ', L_name ) fullname 
		FROM
			sp_councilor sc
			LEFT JOIN tbl_personal_info tpi ON sc.councilor = tpi.info_id
			LEFT JOIN sp_member sp ON sp.sp_member_id = sc.sp_member_id
			LEFT JOIN tbl_sp ts ON ts.sp_id = sp.sp_id
		WHERE
			ts.`status` = 'Active'

		UNION

		SELECT
			tpi.info_id,
			concat( f_name, ' ', m_name, ' ', L_name ) fullname 
		FROM
			sp_member sp
			LEFT JOIN tbl_personal_info tpi ON sp.sp_vice_mayor = tpi.info_id
			LEFT JOIN tbl_sp ts ON ts.sp_id = sp.sp_id
		WHERE
			ts.`status` = 'Active'"""
		return jsonify(pyread(sel))
	except Exception as e:
		return e


@query.route('/get_sp_active', methods = ['POST','GET'])
@login_required
def get_sp_active():
	try:
		sel = "select * from tbl_sp"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_sp_active_only', methods = ['POST','GET'])
@login_required
def get_sp_active_only():
	try:
		sel = "select * from tbl_sp where status='ACTIVE'"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_all_sp_title', methods = ['POST','GET'])
@login_required
def get_all_sp_title():
	try:
		sel = "select * from tbl_sp"
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_session_number_by_spTitle', methods = ['POST','GET'])
@login_required
def function():
	try:
		p = json.loads(request.data)
		sel = """
			SELECT
				* 
			FROM
			tbl_session ts
			LEFT JOIN tbl_sp tp ON tp.sp_id = ts.sp_number
		where tp.sp_id = '"""+str(p['sp_id'])+"""' """
		return jsonify(pyread(sel))
	except Exception as e:
		return e

@query.route('/get_session_active', methods = ['POST','GET'])
@login_required
def get_session_active():
	try:
		p = json.loads(request.data)
		sel = """
			SELECT * FROM tbl_session ts
			where ts.sp_number = '"""+str(p['sp_id'])+"""' 
		"""
		return jsonify(pyread(sel))
	except Exception as e:
		return e


@query.route('/update_budget_year', methods = ['POST','GET'])
@login_required
def update_budget_year():
	p=json.loads(request.data)
	upd="update tbl_sp set "
	return jsonify("Succesfully Updated")

@query.route('/get_com_report', methods = ['POST','GET'])
@login_required
def get_com_report():
	try:
		sel = "select * from tbl_committee"
		return jsonify(pyread(sel))
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/send_emails', methods=['POST','GET'])
def send_emails():
	p=json.loads(request.data)
	try:
		email = EmailSender()
		subj = p['subject']
		body = p['body']

		try:
			res = []
			for val in p['file_path']:
				if val != None :
					f = "application\\static\\" + str(val)
					res.append(f)
			files = res
		except KeyError:
			files=[]

		email_to=p['g_email']

		system_email="select * from tbl_gmail"
		rd_email=pyread(system_email)

		if rd_email:
			sender_address= rd_email[0]['email']
			sender_password = rd_email[0]['password']
			email.set_email_data(subj, body, files, email_to, sender_address, sender_password)

			send = email.send_email(p['g_email'])
			if send:
				prnt_Y("Successfully sent email")
				return jsonify({"message":"Successfully sent email", "status": 200})
			else:
			    return jsonify({"message":"ERROR in sending email", "status": 400})
		else:
			return jsonify({"message":"You have no System email", "status": 400})
	except Exception as e:
		return jsonify({"message":"Error occured in sending gmail "+str(e), "status": 400})
	
	

@query.route('/get_code_and_references', methods =['POST','GET'])
@login_required
def get_code_and_references():
	try:
		sel = "select * from tbl_documents_refferals"
		return jsonify(pyread(sel))
	except Exception as e:
		prnt_R(e)
		return e


@query.route('/get_code_and_references_and_file', methods =['POST','GET'])
@login_required
def get_code_and_references_and_file():
	try:
		sel = """
			select title, path value from tbl_documents_refferals tdr
			left join tbl_documents_refferals_path tdrp on tdrp.documents_refferals_id=tdr.documents_refferals_id
		"""
		return jsonify(pyread(sel))
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/save_email', methods=['POST','GET'])
@login_required
def save_email():
	p=json.loads(request.data)
	if p['gmail_id']==0 or p['gmail_id']=="0":
		insert="insert into tbl_gmail set email='"+str(p['email'])+"', password='"+str(p['password'])+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_gmail set email='"+str(p['email'])+"', password='"+str(p['password'])+"' where email_id='"+str(p['gmail_id'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/get_email', methods=['GET'])
@login_required
def get_email():
	sel="select * from tbl_gmail"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_resolution', methods=['GET'])
def get_landing_resolution():
	sel="""
		select *,
		GROUP_CONCAT(DISTINCT trf.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(DISTINCT trf.path SEPARATOR '|') as file_path,
		GROUP_CONCAT(DISTINCT  (CONCAT(tpi.f_name,' ', tpi.m_name, ' ', tpi.l_name)) SEPARATOR ', ' ) as authors,
		GROUP_CONCAT(DISTINCT  (CONCAT(tpi2.f_name,' ', tpi2.m_name, ' ', tpi2.l_name)) SEPARATOR ', ' ) as co_authors,
		GROUP_CONCAT(DISTINCT  (CONCAT(tpi3.f_name,' ', tpi3.m_name, ' ', tpi3.l_name)) SEPARATOR ', ' ) as sponsors
			from tbl_resolution tr
			left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
			left join tbl_resolution_author tra ON tra.resolution_id = tr.resolution_id
			left join tbl_personal_info tpi ON tpi.info_id = tra.author
			left join tbl_resolution_co_author trca ON trca.resolution_id = tr.resolution_id
			left join tbl_personal_info tpi2 ON tpi2.info_id = trca.co_author
			left join tbl_resolution_sponsor trs ON trs.resolution_id = tr.resolution_id
			left join tbl_personal_info tpi3 ON tpi3.info_id = trs.sponsor
			left join tbl_sp tsp on tsp.sp_id=tr.sp_id
		where tsp.`status`='ACTIVE'
		group by tr.resolution_id
		ORDER BY tr.date_enacted DESC
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_ordinance', methods=['GET'])
def get_landing_ordinance():
	sel="""
		select *,
		GROUP_CONCAT(trf.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(trf.path SEPARATOR '|') as file_path,
		GROUP_CONCAT(DISTINCT (CONCAT(tpi.f_name,' ', tpi.m_name, ' ', tpi.l_name)) SEPARATOR ', ' ) as authors,
		GROUP_CONCAT(DISTINCT (CONCAT(tpi2.f_name,' ', tpi2.m_name, ' ', tpi2.l_name)) SEPARATOR ', ' ) as co_authors,
		GROUP_CONCAT(DISTINCT (CONCAT(tpi3.f_name,' ', tpi3.m_name, ' ', tpi3.l_name)) SEPARATOR ', ' ) as sponsors
			from tbl_ordinance tr
			left join tbl_ordinance_file trf on trf.ordinance_id=tr.ordinance_id
			left join tbl_ordinance_author tra ON tra.ordinance_id = tr.ordinance_id
			left join tbl_personal_info tpi ON tpi.info_id = tra.author
			left join tbl_ordinance_co_author trca ON trca.ordinance_id = tr.ordinance_id
			left join tbl_personal_info tpi2 ON tpi2.info_id = trca.co_author
			left join tbl_ordinance_sponsor trs ON trs.ordinance_id = tr.ordinance_id
			left join tbl_personal_info tpi3 ON tpi3.info_id = trs.sponsor
			left join tbl_sp tsp on tsp.sp_id=tr.sp_id
		where tsp.`status`='ACTIVE'
		group by tr.ordinance_id
		ORDER BY tr.date_enacted DESC
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_executive', methods=['GET'])
def get_landing_executive():
	sel="""
		select * ,
		GROUP_CONCAT(teop.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(teop.path SEPARATOR '|') as file_path
		
		from tbl_executive_order teo
		left join tbl_executive_order_path teop on teop.executive_order_id=teo.executive_order_id
		left join tbl_sp ts on ts.sp_id=teo.sp_id
		where ts.`status`='ACTIVE'
		group by teo.executive_order_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_memorandom', methods=['GET'])
def get_landing_memorandom():
	sel="""
		select *,
		GROUP_CONCAT(tmp.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(tmp.path SEPARATOR '|') as file_path
		from tbl_memorandom tm
		left join tbl_memorandom_path tmp on tmp.memorandom_id=tm.memorandom_id
		left join tbl_sp ts on ts.sp_id=tm.sp_id
		where ts.`status`='ACTIVE'
		group by tm.memorandom_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_code_and_references', methods =['POST','GET'])
def get_landing_code_and_references():
	try:
		sel = """
			select *,
			GROUP_CONCAT(tdrp.filename SEPARATOR '|') as file_name,
			GROUP_CONCAT(tdrp.path SEPARATOR '|') as file_path
			from tbl_documents_refferals tdr
			left join tbl_documents_refferals_path tdrp on tdrp.documents_refferals_id=tdr.documents_refferals_id
			left join tbl_sp ts on ts.sp_id=tdr.sp_id
			where ts.`status`='ACTIVE'
			group by tdr.documents_refferals_id

		"""
		return jsonify(pyread(sel))
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/get_landing_barangay_ordinance', methods=['GET'])
def get_landing_barangay_ordinance():
	sel="""
		select *,concat('(Barangay ',tb.barangay,') ',tbo.title) title ,
		GROUP_CONCAT(tbop.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(tbop.path SEPARATOR '|') as file_path
		from tbl_barangay_ordinance tbo
		left join tbl_barangay_ordinance_path tbop on tbop.barangay_ordinance_id=tbo.barangay_ordinance_id
		left join tbl_barangay tb on tb.brgy_id=tbo.brgy_id
		group by tbo.barangay_ordinance_id
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_landing_barangay_resolution', methods=['GET'])
def get_landing_barangay_resolution():
	sel="""
		select *,concat('(Barangay ',tb.barangay,') ',tbr.title) title ,
		GROUP_CONCAT(tbrp.filename SEPARATOR '|') as file_name,
		GROUP_CONCAT(tbrp.path SEPARATOR '|') as file_path
		from tbl_barangay_resolution tbr
		left join tbl_barangay_resolution_path tbrp on tbrp.barangay_resolution_id=tbr.barangay_resolution_id
		left join tbl_barangay tb on tb.brgy_id=tbr.brgy_id
		group by tbr.barangay_resolution_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_landing_minutes', methods=['GET'])
def get_landing_minutes():
	sel="""
		select * from tbl_minutes tm
		left join tbl_minutes_path tmp on tmp.minutes_id=tm.minutes_id
		group by tm.minutes_id
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/remove_visitor', methods = ['POST'])
@login_required
def remove_visitor():
	try:
		p = json.loads(request.data)
		del_q = "delete from tbl_session_visitor where visitor_id = '"+str(p['visitor_id'])+"'"
		cud(del_q)
		return jsonify("success")
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/remove_privilege', methods = ['POST'])
@login_required
def remove_privilege():
	try:
		p = json.loads(request.data);
		del_q = "delete from tbl_session_previlege_hour where previlege_hour_id = '"+str(p['priv_id'])+"'"
		cud(del_q)
		return jsonify("success")
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/get_city_name', methods=['GET'])
def get_city_name():
	sel="""
		SELECT
			tci.config_info_id,
			tci.city_name,
			tci.vice_mayors_corner,
			tci.mission,
			tci.vission,
			CONCAT(tpi.f_name,'', tpi.m_name,'',tpi.l_name) fullname,
			tci.province,
			tci.type,
			ts.sp_title,
			ts.sp_id,
			tci.show_council_data
		FROM
			tbl_config_info tci
			join sp_member sm
			join tbl_personal_info tpi ON sm.sp_vice_mayor = tpi.info_id
			join tbl_sp ts ON ts.sp_id = sm.sp_id where ts.`status` = 'ACTIVE' 
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/save_city_name', methods=['POST','GET'])
@login_required
def save_city_name():
	p=json.loads(request.data)
	if p['h_config_info_id1']==0 or p['h_config_info_id1']=="0":
		insert="insert into tbl_config_info set city_name='"+str(p['city_name'])+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_config_info set city_name='"+str(p['city_name'])+"' where config_info_id='"+str(p['h_config_info_id1'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/save_province', methods=['POST','GET'])
@login_required
def save_province():
	p=json.loads(request.data)
	if p['h_config_info_id1']==0 or p['h_config_info_id1']=="0":
		insert="insert into tbl_config_info set province='"+str(p['province'])+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_config_info set province='"+str(p['province'])+"' where config_info_id='"+str(p['h_config_info_id1'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/save_v_mayor_corner', methods=['POST','GET'])
@login_required
def save_v_mayor_corner():
	p=json.loads(request.data)
	if p['h_config_info_id1']==0 or p['h_config_info_id1']=="0":
		insert="insert into tbl_config_info set vice_mayors_corner='"+str(p['vice_mayors_corner'])+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_config_info set vice_mayors_corner='"+str(p['vice_mayors_corner'])+"' where config_info_id='"+str(p['h_config_info_id1'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/save_mission', methods=['POST','GET'])
@login_required
def save_mission():
	p=json.loads(request.data)
	mission = p['mission'].replace("'","")
	if p['h_config_info_id1']==0 or p['h_config_info_id1']=="0":
		insert="insert into tbl_config_info set mission='"+str(mission)+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_config_info set mission='"+str(mission)+"' where config_info_id='"+str(p['h_config_info_id1'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/save_vission', methods=['POST','GET'])
@login_required
def save_vission():
	p=json.loads(request.data)
	if p['h_config_info_id1']==0 or p['h_config_info_id1']=="0":
		insert="insert into tbl_config_info set vission='"+str(p['vission'])+"'"
		cud(insert)
		return jsonify("Successfully saved")
	else:
		update="update tbl_config_info set vission='"+str(p['vission'])+"' where config_info_id='"+str(p['h_config_info_id1'])+"'"
		cud(update)
		return jsonify("Successfully updated")


@query.route('/get_landing_announcement', methods=['GET'])
@login_required
def get_landing_announcement():
	sel="select * from tbl_announcement where status='active'"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_vice_photo', methods=['GET'])
@login_required
def get_vice_photo():
	sel="""
		select * from tbl_sp sp
		left join sp_member sm on sm.sp_id=sp.sp_id
		left join tbl_personal_info tpi on tpi.info_id=sm.sp_vice_mayor
		where status='active'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_resolution', methods=['POST','GET'])
@login_required
def get_file_resolution():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_file where resolution_id='"+str(p['resolution_id'])+"'"

	sel="""
		select * from tbl_resolution_file,(select filename minutes_filename, path minutes_path from tbl_resolution tr
		LEFT JOIN tbl_minutes_resolution_path tmrp on tmrp.minutes_id=tr.minutes_id
		WHERE  tr.resolution_id='"""+str(p['resolution_id'])+"""') nt
		where resolution_id='"""+str(p['resolution_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_tracking_legislative', methods=['POST','GET'])
@login_required
def get_tracking_legislative():
	p=json.loads(request.data)
	sel="""
		select * from tbl_document_tracking_status where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_tracking_document_report', methods=['POST','GET'])
@login_required
def get_tracking_document_report():
	p=json.loads(request.data)
	sel="""
		select * from tbl_document_tracking tdt 
		left join tbl_committee tc on tc.committee_id=tdt.committee_id
		where tracking_no='"""+str(p['tracking_no'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_petition', methods=['POST','GET'])
@login_required
def get_file_petition():
	p=json.loads(request.data)
	sel="select * from tbl_petition_path where petition_id='"+str(p['petition_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_file_executive', methods=['POST','GET'])
@login_required
def get_file_executive():
	p=json.loads(request.data)
	sel="select * from tbl_executive_order_path where executive_order_id='"+str(p['executive_order_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_memorandom', methods=['POST','GET'])
@login_required
def get_file_memorandom():
	p=json.loads(request.data)
	sel="select * from tbl_memorandom_path where memorandom_id='"+str(p['memorandom_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_barangay_ordinance', methods=['POST','GET'])
@login_required
def get_file_barangay_ordinance():
	p=json.loads(request.data)
	sel="select * from tbl_barangay_ordinance_path where barangay_ordinance_id='"+str(p['barangay_ordinance_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_barangay_resolution', methods=['POST','GET'])
@login_required
def get_file_barangay_resolution():
	p=json.loads(request.data)
	sel="select * from tbl_barangay_resolution_path where barangay_resolution_id='"+str(p['barangay_resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_file_minutes', methods=['POST','GET'])
@login_required
def get_file_minutes():
	p=json.loads(request.data)
	sel="select * from tbl_minutes_path where minutes_id='"+str(p['minutes_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)	

@query.route('/get_comm_reports', methods = ['POST','GET'])
@login_required
def get_comm_reports():
	try:
		p = json.loads(request.data)
		sel_ordi = """
			SELECT
				`to`.ordinance_id,
				`to`.ordinance_title,
					tofm.committee_id
			FROM
				tbl_ordinance_file_committee tofm
				LEFT JOIN tbl_ordinance `to` ON tofm.ordinance_id = `to`.ordinance_id
			WHERE
				`to`.ordinance_title !="" and  tofm.committee_id = '"""+str(p['commitee_id'])+"""'
				GROUP BY tofm.ordinance_id 
		"""
		res_ordi = pyread(sel_ordi)

		# sel reso
		sel_reso = """
			SELECT
				ts.resolution_id,
				ts.resolution_title,
				tsfm.committee_id
			FROM
				tbl_resolution_file_committee tsfm
				LEFT JOIN tbl_resolution ts ON tsfm.resolution_id = ts.resolution_id
			WHERE
				ts.resolution_title !='' and tsfm.committee_id = '"""+str(p['commitee_id'])+"""'
				GROUP BY tsfm.resolution_id 
		"""
		res_reso = pyread(sel_reso)

		sel_peti = """
			SELECT
				tp.petition_id,
				tp.title,
				tppc.committee_id
			FROM
				tbl_petition_path_committee tppc
				LEFT JOIN tbl_petition tp ON tppc.petition_id = tp.petition_id
			WHERE
				tp.title != "" and  tppc.committee_id = '"""+str(p['commitee_id'])+"""'
				GROUP BY tppc.petition_id 
		"""
		res_peti = pyread(sel_peti)

		data = {"ordi":res_ordi,"reso":res_reso,"peti":res_peti}  
		return jsonify(data)
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/get_city_logo', methods=['POST','GET'])
@login_required
def get_city_logo():
	sel="select * from tbl_sp where `status`='active'"
	rd=pyread(sel)
	if rd:
		return jsonify(rd)
	else:
		return jsonify("No City Logo Uploaded")


@query.route('/get_tbl_config_info', methods=['POST','GET'])
@login_required
def get_tbl_config_info():
	sel="select * from tbl_config_info"
	rd=pyread(sel)
	if rd:
		return jsonify(rd)

@query.route('/get_current_sp_secretary', methods=['POST','GET'])
@login_required
def get_current_sp_secretary():
	sel="""
		select *, concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) secretary from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi on tpi.info_id=sm.sp_secretary
		where `status`='active'
	"""
	rd=pyread(sel)
	if rd:
		return jsonify(rd)


@query.route('/get_active_referrals', methods=['POST','GET'])
@login_required
def get_active_referrals():
	p=json.loads(request.data)

	if p['session_id']=="":
		p['session_id']="0"

	if 'sp_id' in p and p['committee_id']!="0" and p['session_id']!="0":
		sel="""
			select committee,ordinance_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_ordinance tbo
			left join tbl_committee_ref_ordinance tcr on tcr.ordinance_id=tbo.ordinance_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tbo.session_id
			left join tbl_ordinance_author toa on toa.ordinance_id=tbo.ordinance_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where  tcr.committee_id='"""+str(p['committee_id'])+"""' and tbo.sp_id='"""+str(p['sp_id'])+"""' and tbo.session_id='"""+str(p['session_id'])+"""'
			group by tbo.ordinance_id

			union

			select committee,resolution_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_resolution tr
			left join tbl_committee_ref_resolution tcr on tcr.resolution_id=tr.resolution_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tr.session_id
			left join tbl_resolution_author toa on toa.resolution_id=tr.resolution_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where  tcr.committee_id='"""+str(p['committee_id'])+"""' and tr.sp_id='"""+str(p['sp_id'])+"""' and tr.session_id='"""+str(p['session_id'])+"""'
			group by tr.resolution_id
		"""

	if 'sp_id' in p and p['committee_id']!="0" and p['session_id']=="0":
		sel="""
			select committee,ordinance_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_ordinance tbo
			left join tbl_committee_ref_ordinance tcr on tcr.ordinance_id=tbo.ordinance_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tbo.session_id
			left join tbl_ordinance_author toa on toa.ordinance_id=tbo.ordinance_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where  tcr.committee_id='"""+str(p['committee_id'])+"""' and tbo.sp_id='"""+str(p['sp_id'])+"""'
			group by tbo.ordinance_id

			union

			select committee,resolution_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_resolution tr
			left join tbl_committee_ref_resolution tcr on tcr.resolution_id=tr.resolution_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tr.session_id
			left join tbl_resolution_author toa on toa.resolution_id=tr.resolution_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where  tcr.committee_id='"""+str(p['committee_id'])+"""' and tr.sp_id='"""+str(p['sp_id'])+"""'
			group by tr.resolution_id
		"""

	if 'sp_id' in p and p['committee_id']=="0" and p['session_id']=="0":
		sel="""
			select committee,ordinance_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_ordinance tbo
			left join tbl_committee_ref_ordinance tcr on tcr.ordinance_id=tbo.ordinance_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tbo.session_id
			left join tbl_ordinance_author toa on toa.ordinance_id=tbo.ordinance_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where tbo.sp_id='"""+str(p['sp_id'])+"""'
			group by tbo.ordinance_id

			union

			select committee,resolution_title title,session_date,group_concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) authors
			from tbl_resolution tr
			left join tbl_committee_ref_resolution tcr on tcr.resolution_id=tr.resolution_id
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_session tb on tb.session_id=tr.session_id
			left join tbl_resolution_author toa on toa.resolution_id=tr.resolution_id
			left join tbl_personal_info tpi on tpi.info_id=toa.author
			where  tcr.committee_id='"""+str(p['committee_id'])+"""'
			group by tr.resolution_id
		"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/get_attendance_report_by', methods=['POST','GET'])
@login_required
def get_attendance_report_by():
	p=json.loads(request.data)
	if p['type'] == "2":
		sel = """
			select *, concat(tpi.f_name, ' ', tpi.m_name, ' ', tpi.l_name) fullname,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE (tsrc.`status`=0 or tsrc.`status`=4) and 
					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
					and tsrc.info_id=tsrc1.info_id
			) present,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=1 and 
					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
					and tsrc.info_id=tsrc1.info_id
			) absent,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=2 and 
					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
					and tsrc.info_id=tsrc1.info_id
			) `leave`,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=3 and 
					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
					and tsrc.info_id=tsrc1.info_id
			) `travel`,
			" " remarks
			from tbl_session_roll_call tsrc1 
			left join tbl_session ts on ts.session_id=tsrc1.session_id
			left join tbl_personal_info tpi on tpi.info_id=tsrc1.info_id
			inner join sp_member sm on sm.sp_id=ts.sp_number
			inner join sp_councilor sc on sc.sp_member_id=sm.sp_member_id
			where session_date BETWEEN '{}' AND '{}'
			group by tsrc1.info_id order by sc.sp_councilor
		""".format(p['month_from'], p['month_to'])
		rd = pyread(sel)

		count_query = """
			SELECT COUNT(*) as session_count
			FROM tbl_session
			WHERE session_date BETWEEN '{}' AND '{}'
		""".format(p['month_from'], p['month_to'])
	else:
		sel = """
			select session_type, concat(tpi.f_name, ' ', tpi.m_name, ' ', tpi.l_name) fullname,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE (tsrc.`status`=0 or tsrc.`status`=4)
					and ts.session_id='"""+str(p['session_id'])+"""'
					and tsrc.info_id=tsrc1.info_id
			) present,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=1
					and ts.session_id='"""+str(p['session_id'])+"""'
					and tsrc.info_id=tsrc1.info_id
			) absent,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=2
					and ts.session_id='"""+str(p['session_id'])+"""'
					and tsrc.info_id=tsrc1.info_id
			) `leave`,
			(select count(*) present
					from tbl_session_roll_call tsrc 
					left join tbl_session ts on ts.session_id=tsrc.session_id
					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
					WHERE tsrc.`status`=3
					and ts.session_id='"""+str(p['session_id'])+"""'
					and tsrc.info_id=tsrc1.info_id
			) `travel`,
			" " remarks
			from tbl_session_roll_call tsrc1 
			left join tbl_session ts on ts.session_id=tsrc1.session_id
			left join tbl_personal_info tpi on tpi.info_id=tsrc1.info_id
			inner join sp_member sm on sm.sp_id=ts.sp_number
			inner join sp_councilor sc on sc.sp_member_id=sm.sp_member_id
			where ts.session_id='{}'
			group by tsrc1.info_id 
		""".format(p['session_id'])
		rd = pyread(sel)

		count_query = """
			SELECT COUNT(*) as session_count
			FROM tbl_session
			WHERE session_id = '{}'
		""".format(p['session_id'])

	count_result = pyread(count_query)
	count_session_table = count_result[0]['session_count'] if count_result else 0

	return jsonify(rd, count_session_table)


# @query.route('/get_attendance_report_by', methods=['POST','GET'])
# @login_required
# def get_attendance_report_by():
# 	p=json.loads(request.data)
# 	if p['type']=="2":
# 		sel= """
# 			select *,concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) fullname,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE (tsrc.`status`=0 or tsrc.`status`=4) and 
# 					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
# 					and tsrc.info_id=tsrc1.info_id
# 			) present,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=1 and 
# 					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
# 					and tsrc.info_id=tsrc1.info_id
# 			) absent,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=2 and 
# 					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
# 					and tsrc.info_id=tsrc1.info_id
# 			) `leave`,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=3 and 
# 					(session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
# 					and tsrc.info_id=tsrc1.info_id
# 			) `travel`,
# 			" " remarks
# 			from tbl_session_roll_call tsrc1 
# 			left join tbl_session ts on ts.session_id=tsrc1.session_id
# 			left join tbl_personal_info tpi on tpi.info_id=tsrc1.info_id
# 			where (session_date BETWEEN '"""+str(p['month_from'])+"""' AND '"""+str(p['month_to'])+"""')
# 			group by tsrc1.info_id
# 		"""
# 		rd=pyread(sel)
# 	else:
# 		sel="""
# 			select *,concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) fullname,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE (tsrc.`status`=0 or tsrc.`status`=4)
# 					and ts.session_id='"""+str(p['session_id'])+"""'
# 					and tsrc.info_id=tsrc1.info_id
# 			) present,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=1
# 					and ts.session_id='"""+str(p['session_id'])+"""'
# 					and tsrc.info_id=tsrc1.info_id
# 			) absent,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=2
# 					and ts.session_id='"""+str(p['session_id'])+"""'
# 					and tsrc.info_id=tsrc1.info_id
# 			) `leave`,
# 			(select count(*) present
# 					from tbl_session_roll_call tsrc 
# 					left join tbl_session ts on ts.session_id=tsrc.session_id
# 					left join tbl_personal_info tpi on tpi.info_id=tsrc.info_id
# 					WHERE tsrc.`status`=3
# 					and ts.session_id='"""+str(p['session_id'])+"""'
# 					and tsrc.info_id=tsrc1.info_id
# 			) `travel`,
# 			" " remarks
# 			from tbl_session_roll_call tsrc1 
# 			left join tbl_session ts on ts.session_id=tsrc1.session_id
# 			left join tbl_personal_info tpi on tpi.info_id=tsrc1.info_id
# 			where ts.session_id='"""+str(p['session_id'])+"""'
# 			group by tsrc1.info_id
# 		"""
# 		rd=pyread(sel)
# 	return jsonify(rd)

# @query.route('/get_master_list_sp_members', methods=['POST','GET'])
# @login_required
# def get_master_list_sp_members():
# 	p=json.loads(request.data)
# 	sel="""
# 		select *, concat(tpi_mayor.f_name,' ',tpi_mayor.m_name,' ',tpi_mayor.l_name) mayor_fullname,tpi_mayor.phone mayor_phone,tpi_mayor.email mayor_email,tpi_mayor.address mayor_address,
# 		concat(tpi_vmayor.f_name,' ',tpi_vmayor.m_name,' ',tpi_vmayor.l_name) vmayor_fullname,tpi_vmayor.phone vmayor_phone,tpi_vmayor.email vmayor_email,tpi_vmayor.address vmayor_address,
# 		concat(tpi_sec.f_name,' ',tpi_sec.m_name,' ',tpi_sec.l_name) sec_fullname,tpi_sec.phone sec_phone,tpi_sec.email sec_email,tpi_sec.address sec_address,
# 		concat(tpi_coun.f_name,' ',tpi_coun.m_name,' ',tpi_coun.l_name) councilors,tpi_coun.phone coun_phone,tpi_coun.email coun_email,tpi_coun.address coun_address
# 		from tbl_sp ts
# 		left join sp_member sm on ts.sp_id=sm.sp_id
# 		left join sp_councilor sc on sm.sp_member_id=sc.sp_member_id
# 		left join tbl_personal_info tpi_mayor on tpi_mayor.info_id=sp_mayor
# 		left join tbl_personal_info tpi_vmayor on tpi_vmayor.info_id=sp_vice_mayor
# 		left join tbl_personal_info tpi_sec on tpi_sec.info_id=sp_secretary
# 		left join tbl_personal_info tpi_coun on tpi_coun.info_id=sc.councilor
# 		where ts.sp_id='"""+str(p['sp_id'])+"""' group by sc.sp_councilor
# 	"""
# 	rd=pyread(sel)
# 	return jsonify(rd)

@query.route('/get_master_list_sp_members', methods=['POST', 'GET'])
@login_required
def get_master_list_sp_members():
    p = json.loads(request.data)

    sp_id = p.get("sp_id")
    if not sp_id:
        return jsonify({"error": "Missing sp_id"}), 400

    # Main SP info (mayor, v-mayor, sec)
    sp_info_query = """
        SELECT 
            ts.sp_id,
            CONCAT(tpi_mayor.f_name, ' ', tpi_mayor.m_name, ' ', tpi_mayor.l_name) AS mayor_fullname,
            tpi_mayor.phone AS mayor_phone,
            tpi_mayor.email AS mayor_email,
            tpi_mayor.address AS mayor_address,

            CONCAT(tpi_vmayor.f_name, ' ', tpi_vmayor.m_name, ' ', tpi_vmayor.l_name) AS vmayor_fullname,
            tpi_vmayor.phone AS vmayor_phone,
            tpi_vmayor.email AS vmayor_email,
            tpi_vmayor.address AS vmayor_address,

            CONCAT(tpi_sec.f_name, ' ', tpi_sec.m_name, ' ', tpi_sec.l_name) AS sec_fullname,
            tpi_sec.phone AS sec_phone,
            tpi_sec.email AS sec_email,
            tpi_sec.address AS sec_address
        FROM tbl_sp ts
        LEFT JOIN tbl_personal_info tpi_mayor ON tpi_mayor.info_id = ts.sp_mayor
        LEFT JOIN tbl_personal_info tpi_vmayor ON tpi_vmayor.info_id = ts.sp_vice_mayor
        LEFT JOIN tbl_personal_info tpi_sec ON tpi_sec.info_id = ts.sp_secretary
        WHERE ts.sp_id = %s
    """

    # Councilors list
    councilors_query = """
        SELECT 
            CONCAT(tpi.f_name, ' ', tpi.m_name, ' ', tpi.l_name) AS fullname,
            tpi.phone,
            tpi.email,
            tpi.address
        FROM sp_member sm
        LEFT JOIN sp_councilor sc ON sc.sp_member_id = sm.sp_member_id
        LEFT JOIN tbl_personal_info tpi ON tpi.info_id = sc.councilor
        WHERE sm.sp_id = %s
    """

    # Execute queries
    sp_info = rd_query(sp_info_query, (sp_id,))
    councilors = rd_query(councilors_query, (sp_id,))

    return jsonify({
        "sp_info": sp_info[0] if sp_info else {},
        "councilors": councilors
    })

@query.route('/get_category_resolution', methods=['POST','GET'])
@login_required
def get_category_resolution():
	sel="""
		select tc.category_id,tc.title 
		from tbl_resolution tr 
		left join tbl_category tc on tc.category_id=tr.category
		group by tc.title
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_author_resolution', methods=['POST','GET'])
@login_required
def get_author_resolution():
	sel="""
		select * from tbl_resolution group by author
	"""
	rd=pyread(sel)
	return jsonify(rd)


# @query.route('/get_enacted_ordinance_by_period', methods=['POST','GET'])
# @login_required
# def get_enacted_ordinance_by_period():
# 	p=json.loads(request.data)

# 	flag = 1;

# 	if 'category' not in p:
# 		p['category'] = '0'

# 	if p['from']!='' and p['to']!='' and p['author']=="0" and p['category']=='0':
# 		prnt_R(1)
# 		where = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where_1 = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where_2 = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE'
# 		"""
	
# 	if (p['from']=='' and p['to']=='') and p['author']=="0" and p['category']=='0':
# 		prnt_R(2)
# 		flag=1
# 		where = """
# 			where tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where_1 = """
# 			where tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where_2 = """
# 			where tor.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where tor.`status`=6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']!='' and p['to']!='' and p['category']!='0' and p['author']=="0":
# 		prnt_G(3)
# 		where = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tor.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 		"""

# 		where_1 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tor.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 		"""

# 		where_2 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tor.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 		"""

# 	if p['from']!='' and p['from']!='' and p['category']!='0' and p['author']!="0":
# 		prnt_G(4)
# 		flag= 2
# 		where = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			toa.author='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where_1 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			toca.co_author='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where_2 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			tos.sponsor='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tor.`status`=6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']=='' and p['to']=='' and p['category']=='0' and  p['author']!="0":
# 		prnt_G(6)
# 		flag = 2
# 		where = """
# 			where toa.author='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tor.ordinance_id
# 		"""
# 		where_1 = """
# 			where toca.co_author='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tor.ordinance_id
# 		"""
# 		where_2 = """
# 			where tos.sponsor='"""+str(p['author'])+"""' and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tor.ordinance_id
# 		"""

# 	if p['from']=='' and p['to']=='' and p['author']=="0" and p['category']!='0':
# 		prnt_G(8)
# 		flag = 1
# 		where = """
# 			where  FIND_IN_SET('"""+str(p['category'])+"""', category) and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 		"""

# 		where_1 = """
# 			where  FIND_IN_SET('"""+str(p['category'])+"""', category) and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 		"""

# 		where_2 = """
# 			where  FIND_IN_SET('"""+str(p['category'])+"""', category) and tor.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where  FIND_IN_SET('"""+str(p['category'])+"""', category) and tor.status = 6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']=='' and p['to']=='' and p['author']!="0" and p['category']!='0':
# 		prnt_R(9)
# 		flag = 2
# 		where = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and toa.author='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""
# 		where_1 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and toca.co_author='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""
# 		where_2 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and tos.sponsor='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""

# 	if p['from']!='' and p['to']!='' and p['author']!="0":
# 		prnt_R(10)
# 		flag = 2
# 		where = """
# 			where toa.author='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""
# 		where_1 = """
# 			where toca.co_author='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""
# 		where_2 = """
# 			where tos.sponsor='"""+str(p['author'])+"""' 
# 			and tor.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tor.ordinance_id
# 		"""
	
# 	if flag == 1:
# 		prnt_B(11111)
# 		# sel = """
# 		# 	select ordinance_id, ordinance_number , title, group_concat(type) people, date_enacted,path from 
# 		# 	(
# 		# 		(
# 		# 			select tor.ordinance_id, tor.ordinance_number , ordinance_title title, 
# 		# 			group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Author)') type,
# 		# 			date_enacted,path
# 		# 			from tbl_ordinance tor
# 		# 			left join tbl_ordinance_author toa on toa.ordinance_id=tor.ordinance_id
# 		# 			left join tbl_sp ts on ts.sp_id = tor.sp_id
# 		# 			left join tbl_personal_info tei on tei.info_id=toa.author
# 		# 			left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 		# 			"""+str(where)+"""
# 		# 		)

# 		# 		union 

# 		# 		(
# 		# 			select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, 
# 		# 			group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Co-Author)') type,
# 		# 			date_enacted,path
# 		# 			from tbl_ordinance tor
# 		# 			left join tbl_ordinance_co_author toca on toca.ordinance_id=tor.ordinance_id
# 		# 			left join tbl_sp ts on ts.sp_id = tor.sp_id
# 		# 			left join tbl_personal_info tei on tei.info_id=toca.co_author
# 		# 			left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 		# 			"""+str(where_1)+"""
# 		# 		)

# 		# 		union

# 		# 		(
# 		# 			select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, 
# 		# 			group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Sponsor)') type,
# 		# 			date_enacted,path
# 		# 			from tbl_ordinance tor
# 		# 			left join tbl_ordinance_sponsor tos on tos.ordinance_id=tor.ordinance_id
# 		# 			left join tbl_sp ts on ts.sp_id = tor.sp_id
# 		# 			left join tbl_personal_info tei on tei.info_id=tos.sponsor
# 		# 			left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 		# 			"""+str(where_2)+"""
# 		# 		)

# 		# 		union 
					
# 		# 		(
# 		# 			select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, null type, date_enacted,path
# 		# 			from tbl_ordinance tor
# 		# 			left join tbl_sp ts on ts.sp_id = tor.sp_id
# 		# 			left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 		# 			"""+str(where2)+"""
# 		# 		)
# 		# 	) ntbl where ordinance_id is not null GROUP BY ordinance_id
# 		# """
# 		sel = """
# 		SELECT ordinance_id, ordinance_number, title, GROUP_CONCAT(type SEPARATOR ', ') AS people, date_enacted, path
# 		FROM (
# 			(
# 				SELECT 
# 					tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
# 					CONCAT(tei.f_name, ' ', tei.l_name, ' ', tei.m_name, ' (Author)') AS type,
# 					date_enacted, path
# 				FROM tbl_ordinance tor
# 				LEFT JOIN tbl_ordinance_author toa ON toa.ordinance_id = tor.ordinance_id
# 				LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
# 				LEFT JOIN tbl_personal_info tei ON tei.info_id = toa.author
# 				LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
# 				""" + str(where) + """
# 			)

# 			UNION ALL

# 			(
# 				SELECT 
# 					tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
# 					CONCAT(tei.f_name, ' ', tei.l_name, ' ', tei.m_name, ' (Co-Author)') AS type,
# 					date_enacted, path
# 				FROM tbl_ordinance tor
# 				LEFT JOIN tbl_ordinance_co_author toca ON toca.ordinance_id = tor.ordinance_id
# 				LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
# 				LEFT JOIN tbl_personal_info tei ON tei.info_id = toca.co_author
# 				LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
# 				""" + str(where_1) + """
# 			)

# 			UNION ALL

# 			(
# 				SELECT 
# 					tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
# 					CONCAT(tei.f_name, ' ', tei.l_name, ' ', tei.m_name, ' (Sponsor)') AS type,
# 					date_enacted, path
# 				FROM tbl_ordinance tor
# 				LEFT JOIN tbl_ordinance_sponsor tos ON tos.ordinance_id = tor.ordinance_id
# 				LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
# 				LEFT JOIN tbl_personal_info tei ON tei.info_id = tos.sponsor
# 				LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
# 				""" + str(where_2) + """
# 			)

# 			UNION ALL

# 			(
# 				SELECT 
# 					tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
# 					NULL AS type,
# 					date_enacted, path
# 				FROM tbl_ordinance tor
# 				LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
# 				LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
# 				""" + str(where2) + """
# 			)
# 		) ntbl
# 		WHERE ordinance_id IS NOT NULL
# 		GROUP BY ordinance_id, ordinance_number, title, date_enacted, path
# 		"""

# 		prnt_R(sel)
# 	elif flag == 2:
# 		prnt_B(222222)
# 		sel = """
# 			select ordinance_id, ordinance_number ,title,group_concat(type) people, date_enacted,path from 
# 			(
# 				(
# 					select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Author)') type,
# 					date_enacted,path
# 					from tbl_ordinance tor
# 					left join tbl_ordinance_author toa on toa.ordinance_id=tor.ordinance_id
# 					left join tbl_sp ts on ts.sp_id = tor.sp_id
# 					left join tbl_personal_info tei on tei.info_id=toa.author
# 					left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 					"""+str(where)+"""
# 				)

# 				union 

# 				(
# 					select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Co-Author)') type,
# 					date_enacted,path
# 					from tbl_ordinance tor
# 					left join tbl_ordinance_co_author toca on toca.ordinance_id=tor.ordinance_id
# 					left join tbl_sp ts on ts.sp_id = tor.sp_id
# 					left join tbl_personal_info tei on tei.info_id=toca.co_author
# 					left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 					"""+str(where_1)+"""
# 				)

# 				union

# 				(
# 					select tor.ordinance_id, tor.ordinance_number ,ordinance_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Sponsor)') type,
# 					date_enacted,path
# 					from tbl_ordinance tor
# 					left join tbl_ordinance_sponsor tos on tos.ordinance_id=tor.ordinance_id
# 					left join tbl_sp ts on ts.sp_id = tor.sp_id
# 					left join tbl_personal_info tei on tei.info_id=tos.sponsor
# 					left join tbl_ordinance_file tof on tof.ordinance_id=tor.ordinance_id
# 					"""+str(where_2)+"""
# 				)
# 			) ntbl where ordinance_id is not null GROUP BY ordinance_id
# 		"""
# 	rd=pyread(sel)
# 	return jsonify(rd)




@query.route('/get_enacted_ordinance_by_period', methods=['POST', 'GET'])
@login_required
def get_enacted_ordinance_by_period():
    p = json.loads(request.data)
    p['category'] = p.get('category', '0')
    flag = 1

    # Determine flag
    if p['author'] != "0":
        flag = 2
    if p['category'] == '0' and p['author'] == "0":
        flag = 1

    def date_clause():
        return f"(date_enacted BETWEEN '{p['from']}' AND '{p['to']}')" if p['from'] and p['to'] else ""

    def category_clause():
        return f"FIND_IN_SET('{p['category']}', category)" if p['category'] != '0' else ""

    def person_where_clause(role_col, alias):
        conds = [
            f"{alias}.{role_col} = '{p['author']}'" if p['author'] != "0" else "",
            category_clause(),
            "tor.status = 6",
            "ts.status = 'ACTIVE'",
            "tei.info_id IS NOT NULL",
            date_clause()
        ]
        return "WHERE " + " AND ".join([c for c in conds if c])

    def no_person_where_clause():
        conds = [
            date_clause(),
            category_clause(),
            "tor.status = 6",
            "ts.status = 'ACTIVE'"
        ]
        return "WHERE " + " AND ".join([c for c in conds if c])

    def person_sql(role, join_table, role_col, alias):
        return f"""
            SELECT tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
                CONCAT(tei.f_name, ' ', tei.l_name, ' ', tei.m_name, ' ({role})') AS type,
                date_enacted, path
            FROM tbl_ordinance tor
            LEFT JOIN {join_table} {alias} ON {alias}.ordinance_id = tor.ordinance_id
            LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
            LEFT JOIN tbl_personal_info tei ON tei.info_id = {alias}.{role_col}
            LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
            {person_where_clause(role_col, alias)}
        """

    def no_person_sql():
        return f"""
            SELECT tor.ordinance_id, tor.ordinance_number, ordinance_title AS title,
                NULL AS type, date_enacted, path
            FROM tbl_ordinance tor
            LEFT JOIN tbl_sp ts ON ts.sp_id = tor.sp_id
            LEFT JOIN tbl_ordinance_file tof ON tof.ordinance_id = tor.ordinance_id
            {no_person_where_clause()}
        """

    if flag == 1:
        prnt_B(11111)
        sel = f"""
            SELECT ordinance_id, ordinance_number, title,
                GROUP_CONCAT(type SEPARATOR ', ') AS people, date_enacted, path
            FROM (
                {person_sql("Author", "tbl_ordinance_author", "author", "toa")}
                UNION ALL
                {person_sql("Co-Author", "tbl_ordinance_co_author", "co_author", "toca")}
                UNION ALL
                {person_sql("Sponsor", "tbl_ordinance_sponsor", "sponsor", "tos")}
                UNION ALL
                {no_person_sql()}
            ) ntbl
            WHERE ordinance_id IS NOT NULL
            GROUP BY ordinance_id, ordinance_number, title, date_enacted, path
        """
        prnt_R(sel)
    else:
        prnt_B(222222)
        sel = f"""
            SELECT ordinance_id, ordinance_number, title,
                GROUP_CONCAT(type) AS people, date_enacted, path
            FROM (
                {person_sql("Author", "tbl_ordinance_author", "author", "toa")}
                UNION
                {person_sql("Co-Author", "tbl_ordinance_co_author", "co_author", "toca")}
                UNION
                {person_sql("Sponsor", "tbl_ordinance_sponsor", "sponsor", "tos")}
            ) ntbl
            WHERE ordinance_id IS NOT NULL
            GROUP BY ordinance_id
        """

    rd = pyread(sel)
    return jsonify(rd)



# @query.route('/get_adopted_resolution_by_period', methods=['POST','GET'])
# @login_required
# def get_adopted_resolution_by_period():
# 	p=json.loads(request.data)

# 	flag = 1;

# 	if 'category' not in p:
# 		p['category'] = '0'

# 	if p['from']!='' and p['to']!='' and p['author']=="0" and p['category']=='0':
# 		prnt_R(1)
# 		where = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_1 = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_2 = """ 
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE'
# 			GROUP BY tr.resolution_id
# 		"""
# 	if (p['from']=='' and p['to']=='') and p['author']=="0" and p['category']=='0':
# 		prnt_R(2)
# 		flag=1
# 		where = """
# 			where tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_1 = """
# 			where tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_2 = """
# 			where tr.`status`=6 and ts.status='ACTIVE' and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where2 ="""
# 			where tr.`status`=6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']!='' and p['to']!='' and p['category']!='0' and p['author']=="0":
# 		prnt_G(3)
# 		where = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tr.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_1 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tr.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_2 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and
# 			tr.status = 6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE' and FIND_IN_SET('"""+str(p['category'])+"""', category)
# 			GROUP BY tr.resolution_id
# 		"""

# 	if p['from']!='' and p['from']!='' and p['category']!='0' and p['author']!="0":
# 		prnt_G(4)
# 		flag= 2
# 		where = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			tra.author='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where_1 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			trca.co_author='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where_2 = """
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""') and 
# 			trs.sponsor='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and FIND_IN_SET('"""+str(p['category'])+"""', category) and tei.info_id is not null
# 		"""

# 		where2 ="""
# 			where (date_enacted BETWEEN '"""+str(p['from'])+"""' AND '"""+str(p['to'])+"""')
# 			and tr.`status`=6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']=='' and p['to']=='' and p['category']=='0' and  p['author']!="0":
# 		prnt_G(6)
# 		flag = 2
# 		where = """
# 			where tra.author='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tr.resolution_id
# 		"""
# 		where_1 = """
# 			where trca.co_author='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tr.resolution_id
# 		"""
# 		where_2 = """
# 			where trs.sponsor='"""+str(p['author'])+"""' and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null group by tr.resolution_id
# 		"""

# 	if p['from']=='' and p['to']=='' and p['author']=="0" and p['category']!='0':
# 		prnt_G(8)
# 		flag = 1
# 		where = """
# 			where  FIND_IN_SET('"""+str(p['category'])+"""', category) and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_1 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where_2 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and tr.status = 6 and ts.status='ACTIVE'
# 			and tei.info_id is not null
# 			GROUP BY tr.resolution_id
# 		"""

# 		where2 ="""
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and tr.status = 6 and ts.status='ACTIVE'
# 		"""

# 	if p['from']=='' and p['to']=='' and p['author']!="0" and p['category']!='0':
# 		prnt_R(9)
# 		flag = 2
# 		where = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and tra.author='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""
# 		where_1 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and trca.co_author='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""
# 		where_2 = """
# 			where FIND_IN_SET('"""+str(p['category'])+"""', category) and trs.sponsor='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""

# 	if p['from']!='' and p['to']!='' and p['author']!="0":
# 		prnt_R(10)
# 		flag = 2
# 		where = """
# 			where tra.author='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""
# 		where_1 = """
# 			where trca.co_author='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""
# 		where_2 = """
# 			where trs.sponsor='"""+str(p['author'])+"""' 
# 			and tr.status = 6 and ts.status='ACTIVE' and tei.info_id is not null
# 			group by tr.resolution_id
# 		"""
# 	if flag == 1:
# 		sel = """
# 			select resolution_id, resolution_number ,title,group_concat(type) people, date_enacted,path from 
# 			(
# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Author)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_author tra on tra.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=tra.author
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where)+"""
# 				)

# 				union 

# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Co-Author)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_co_author trca on trca.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=trca.co_author
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where_1)+"""
# 				)

# 				union

# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Sponsor)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_sponsor trs on trs.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=trs.sponsor
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where_2)+"""
# 				)

# 				union 
					
# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, null type, date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where2)+"""
# 				)
# 			) ntbl where resolution_id is not null GROUP BY resolution_id
# 		"""
# 	elif flag == 2:
# 		sel = """
# 			select resolution_id, resolution_number ,title,group_concat(type) people, date_enacted,path from 
# 			(
# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Author)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_author tra on tra.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=tra.author
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where)+"""
# 				)

# 				union 

# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Co-Author)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_co_author trca on trca.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=trca.co_author
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where_1)+"""
# 				)

# 				union

# 				(
# 					select tr.resolution_id, tr.resolution_number ,resolution_title title, 
# 					group_concat(Distinct tei.f_name,' ', tei.l_name,' ',tei.m_name, ' (Sponsor)') type,
# 					date_enacted,path
# 					from tbl_resolution tr
# 					left join tbl_resolution_sponsor trs on trs.resolution_id=tr.resolution_id
# 					left join tbl_sp ts on ts.sp_id = tr.sp_id
# 					left join tbl_personal_info tei on tei.info_id=trs.sponsor
# 					left join tbl_resolution_file trf on trf.resolution_id=tr.resolution_id
# 					"""+str(where_2)+"""
# 				)
# 			) ntbl where resolution_id is not null GROUP BY resolution_id
# 		"""
# 	rd=pyread(sel)
# 	return jsonify(rd)


@query.route('/get_adopted_resolution_by_period', methods=['POST', 'GET'])
@login_required
def get_adopted_resolution_by_period():
    p = json.loads(request.data)
    p['category'] = p.get('category', '0')
    flag = 1

    def date_clause():
        return f"(date_enacted BETWEEN '{p['from']}' AND '{p['to']}')" if p['from'] and p['to'] else ""

    def category_clause():
        return f"FIND_IN_SET('{p['category']}', category)" if p['category'] != '0' else ""

    def person_where_clause(role_col, alias):
        conds = [
            f"{alias}.{role_col} = '{p['author']}'" if p['author'] != "0" else "",
            category_clause(),
            "tr.status = 6",
            "ts.status = 'ACTIVE'",
            "tei.info_id IS NOT NULL",
            date_clause()
        ]
        return "WHERE " + " AND ".join([c for c in conds if c])

    def no_person_where_clause():
        conds = [
            date_clause(),
            category_clause(),
            "tr.status = 6",
            "ts.status = 'ACTIVE'"
        ]
        return "WHERE " + " AND ".join([c for c in conds if c])

    def person_sql(role, join_table, role_col, alias):
        return f"""
            SELECT tr.resolution_id, tr.resolution_number, resolution_title AS title,
                CONCAT(tei.f_name, ' ', tei.l_name, ' ', tei.m_name, ' ({role})') AS type,
                date_enacted, path
            FROM tbl_resolution tr
            LEFT JOIN {join_table} {alias} ON {alias}.resolution_id = tr.resolution_id
            LEFT JOIN tbl_sp ts ON ts.sp_id = tr.sp_id
            LEFT JOIN tbl_personal_info tei ON tei.info_id = {alias}.{role_col}
            LEFT JOIN tbl_resolution_file trf ON trf.resolution_id = tr.resolution_id
            {person_where_clause(role_col, alias)}
        """

    def no_person_sql():
        return f"""
            SELECT tr.resolution_id, tr.resolution_number, resolution_title AS title,
                NULL AS type, date_enacted, path
            FROM tbl_resolution tr
            LEFT JOIN tbl_sp ts ON ts.sp_id = tr.sp_id
            LEFT JOIN tbl_resolution_file trf ON trf.resolution_id = tr.resolution_id
            {no_person_where_clause()}
        """

    if p['author'] != "0":
        flag = 2
    if p['author'] == "0" and p['category'] == '0':
        flag = 1

    if flag == 1:
        prnt_G("Flag 1: General search including 'no author'")
        sel = f"""
            SELECT resolution_id, resolution_number, title,
                GROUP_CONCAT(type SEPARATOR ', ') AS people, date_enacted, path
            FROM (
                {person_sql("Author", "tbl_resolution_author", "author", "tra")}
                UNION ALL
                {person_sql("Co-Author", "tbl_resolution_co_author", "co_author", "trca")}
                UNION ALL
                {person_sql("Sponsor", "tbl_resolution_sponsor", "sponsor", "trs")}
                UNION ALL
                {no_person_sql()}
            ) ntbl
            WHERE resolution_id IS NOT NULL
            GROUP BY resolution_id, resolution_number, title, date_enacted, path
        """
    else:
        prnt_G("Flag 2: Author-focused search")
        sel = f"""
            SELECT resolution_id, resolution_number, title,
                GROUP_CONCAT(type SEPARATOR ', ') AS people, date_enacted, path
            FROM (
                {person_sql("Author", "tbl_resolution_author", "author", "tra")}
                UNION
                {person_sql("Co-Author", "tbl_resolution_co_author", "co_author", "trca")}
                UNION
                {person_sql("Sponsor", "tbl_resolution_sponsor", "sponsor", "trs")}
            ) ntbl
            WHERE resolution_id IS NOT NULL
            GROUP BY resolution_id, resolution_number, title, date_enacted, path
        """

    rd = pyread(sel)
    return jsonify(rd)



@query.route('/get_author_ordinance', methods=['POST','GET'])
@login_required
def get_author_ordinance():
	sel="""
		select * from tbl_ordinance group by author
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_category_ordinance', methods=['POST','GET'])
@login_required
def get_category_ordinance():
	sel="""
		select tc.category_id,tc.title 
		from tbl_ordinance tbo
		left join tbl_category tc on tc.category_id=tbo.category
		group by tc.title
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_councilor_ordinance', methods = ['POST', 'GET'])
@login_required
def get_councilor_ordinance():
	try:
		p = json.loads(request.data)
		sel = "SELECT * FROM tbl_ordinance `to` LEFT JOIN tbl_sp ts ON `to`.sp_id = ts.sp_id WHERE ts.`status` = 'Active' and `to`.author = '"+p['name']+"' and `to`.status = 6"
		res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		prnt_R(e)
		return e
	return jsonify()


@query.route('/get_councilor_reso',methods = ['POST','GET'])
@login_required
def get_councilor_reso():
	try:
		p = json.loads(request.data)
		sel = "select * from tbl_resolution tr LEFT JOIN tbl_sp ts ON tr.sp_id = ts.sp_id WHERE ts.`status` = 'Active' and tr.author = '"+p['name']+"' and tr.status = 6"
		res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		prnt_R(e)
		return e


@query.route('/get_councilor_petition',methods = ['POST','GET'])
@login_required
def get_councilor_petition():
	try:
		p = json.loads(request.data)
		sel = "select * from tbl_petition where source_of_document = '"+p['name']+"' and action_taken = 1"
		res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/get_barangay', methods = ['POST','GET'])
@login_required
def get_barangay():
	try:
		sel = "select * from tbl_barangay"
		res = pyread(sel)
		return jsonify(res)
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/save_barangay', methods = ['POST','GET'])
@login_required
def save_barangay():
	try:
		p = json.loads(request.data)
		if p['brgy_id']!=0:
			upt = "update tbl_barangay set barangay = '"+str(p['brgy'])+"' where brgy_id = '"+str(p['brgy_id'])+"'"
			cud(upt)
			msg = "Updated Succesfuly"
		else:
			ins = "insert into tbl_barangay set barangay = '"+str(p['brgy'])+"'"
			cud(ins)
			msg = "Inserted Succesfuly"

		return jsonify(msg)

	except Exception as e:
		prnt_R(e)
		return e

@query.route('/delete_brgy', methods = ['POST','GET'])
@login_required
def delete_brgy():
	try:
		p = json.loads(request.data)
		del_q = "delete from tbl_barangay where brgy_id = '"+str(p['brgy_id'])+"'"
		cud(del_q)
		return jsonify("deleted")
	except Exception as e:
		prnt_R(e)
		return e

@query.route('/get_barangay_ordinance_report', methods=['GET', 'POST'])
@login_required
def get_barangay_ordinance_report():
	p=json.loads(request.data)
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates 
		from tbl_barangay_ordinance tbo
		left join tbl_barangay_ordinance_path tbop on tbop.barangay_ordinance_id=tbo.barangay_ordinance_id
		left join tbl_barangay tb on tb.brgy_id=tbo.brgy_id
		where tbo.brgy_id='"""+str(p['brgy_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_barangay_resolution_report', methods=['GET', 'POST'])
@login_required
def get_barangay_resolution_report():
	p=json.loads(request.data)
	sel="""
		select *, date_format(date_submitted,'%a %M, %d %Y') dates 
		from tbl_barangay_resolution tbr
		left join tbl_barangay_resolution_path tbrp on tbrp.barangay_resolution_id=tbr.barangay_resolution_id
		left join tbl_barangay tb on tb.brgy_id=tbr.brgy_id
		where tbr.brgy_id='"""+str(p['brgy_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)



@query.route('/send_image', methods=['GET', 'POST'])
@login_required
def send_image():
	p=request.form
	cwd = os.getcwd()
	file=request.files['file']
	scan_image=file
	os.chdir('application')
	os.chdir('static')
	if file.filename == '':
		prnt_Y('No file selected for uploading')
		return jsonify("Please select proper image")
	else:
		location="bg_image//image//"
		location.replace("//", "\\\\");
		if not os.path.exists(location):
			os.mkdir('bg_image')
			os.chdir('bg_image')
			os.mkdir('image')
			app.config['UPLOADED_PHOTOS_DEST'] = 'image'
			app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
			photos = UploadSet('photos', IMAGES)
			configure_uploads(app, photos)
			filer = photos.save(scan_image)
		else:
			os.chdir('bg_image')
			app.config['UPLOADED_PHOTOS_DEST'] = "image"
			app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
			photos = UploadSet('photos', IMAGES)
			configure_uploads(app, photos)
			filer = photos.save(scan_image)

		file_ = str(file.filename).replace("'","''")
		path=location + file_
		insert="replace into tbl_bg_image set bg_id=1, path='"+str(path)+"', color_title='"+str(p['color'])+"'"
		cud(insert)

		os.chdir(cwd) 
		return jsonify("Successfully Saved")
		

@query.route('/update_color', methods=['GET', 'POST'])
@login_required
def update_color():
	p=json.loads(request.data)
	update="update tbl_bg_image set color_title='"+str(p['color_title'])+"' where bg_id=1"
	cud(update)
	select="select * from tbl_bg_image where bg_id=1"
	rd=pyread(select)
	return jsonify(rd)


@query.route('/get_author_resolutions', methods=['GET', 'POST'])
@login_required
def get_author_resolutions():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_author where resolution_id='"+str(p['resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_co_author_resolutions', methods=['GET', 'POST'])
@login_required
def get_co_author_resolutions():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_co_author where resolution_id='"+str(p['resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_sponsor_resolutions', methods=['GET', 'POST'])
@login_required
def get_sponsor_resolutions():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_sponsor where resolution_id='"+str(p['resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_cosponsor_resolutions', methods=['GET', 'POST'])
@login_required
def get_cosponsor_resolutions():
	p=json.loads(request.data)
	sel="select * from tbl_resolution_cosponsor where resolution_id='"+str(p['resolution_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_author_ordinances', methods=['GET', 'POST'])
@login_required
def get_author_ordinances():
	p=json.loads(request.data)
	sel="select * from tbl_ordinance_author where ordinance_id='"+str(p['ordinance_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_co_author_ordinance', methods=['GET', 'POST'])
@login_required
def get_co_author_ordinance():
	p=json.loads(request.data)
	sel="select * from tbl_ordinance_co_author where ordinance_id='"+str(p['ordinance_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_sponsor_ordinance', methods=['GET', 'POST'])
@login_required
def get_sponsor_ordinance():
	p=json.loads(request.data)
	sel="select * from tbl_ordinance_sponsor where ordinance_id='"+str(p['ordinance_id'])+"'"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_info', methods=['GET', 'POST'])
@login_required
def get_committee_info():
	p=json.loads(request.data)
	sel="""
		select *, concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) co_chairmans 
		from tbl_committee tc
		left join tbl_personal_info tpi on tpi.info_id=tc.co_chairman
		where committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_member_info', methods=['GET', 'POST'])
@login_required
def get_committee_member_info():
	p=json.loads(request.data)
	sel="""
		select *,concat(tpi.f_name,' ',tpi.m_name,' ',tpi.l_name) fullname 
		from tbl_committee_members tcm
		left join tbl_personal_info tpi on tpi.info_id=tcm.committee_members
		where committee_id='"""+str(p['committee_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_bg', methods=['GET', 'POST'])
@login_required
def get_bg():
	sel="select * from tbl_bg_image"
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_ref_code', methods = ['POST','GET'])
@login_required
def get_ref_code():
	try:
		sel_code_ref = """
			SELECT
				*,
				tdrp.path f_path 
			FROM
				tbl_documents_refferals tdr
				LEFT JOIN tbl_documents_refferals_path tdrp ON tdrp.documents_refferals_id = tdr.documents_refferals_id
			"""
		sel_ref_code = pyread(sel_code_ref)
		return jsonify(sel_ref_code)
	except Exception as e:
		raise



@query.route('/save_background', methods = ['POST','GET'])
@login_required
def save_background():
	for filename_array in request.files:
		file=request.files[filename_array]

		n_path = Path(__file__).parent / "../static/uploads/gallery"
		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				
			location1="gallery//"
			location1.replace("//", "\\\\");
			location=location1+"/"+filename
			path_location=location.replace("/", "\\\\");
			insert="insert into tbl_gallery set path='"+str(path_location)+"'"
			cud(insert)

	return jsonify("Succesfuly Saved")
	

@query.route('/get_gallery_carousel', methods = ['POST','GET'])
@login_required
def get_gallery_carousel():
	sel="""
		select * from tbl_gallery
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/del_gallery_carousel', methods=['GET', 'POST'])
@login_required
def del_gallery_carousel():
	p=json.loads(request.data)
	delete="delete from tbl_gallery where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")

@query.route('/get_login_data', methods = ['POST','GET'])
@login_required
def get_login_data():
	sel="""
		select *, tpi_vmayor.img vmayor, tpi_sec.img secretary,
		concat(tpi_vmayor.f_name,' ', tpi_vmayor.m_name,' ', tpi_vmayor.l_name) vmayor_name,
		concat(tpi_sec.f_name,' ', tpi_sec.m_name,' ', tpi_sec.l_name) sec_name
		from tbl_sp ts
		left join sp_member sm on sm.sp_id=ts.sp_id
		left join tbl_personal_info tpi_vmayor on tpi_vmayor.info_id=sm.sp_vice_mayor

		left join tbl_personal_info tpi_sec on tpi_sec.info_id=sm.sp_secretary
		where ts.status="ACTIVE"
	"""
	rd=pyread(sel)
	return jsonify(rd)



@query.route('/get_location_system', methods = ['POST','GET'])
def get_location_system():
	sel="""
		select *,(case when (tci.type is null or tci.type='') then 'SANGGUNIANG BAYAN' else 'SANGGUNIANG PANLUNGSOD' end) types from tbl_config_info tci
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking', methods = ['POST','GET'])
@login_required
def get_document_tracking():
	sel="""
		select * from tbl_document_tracking tdt
		group by tracking_no ORDER BY tdt.date DESC
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking_not_approved', methods = ['POST','GET'])
@login_required
def get_document_tracking_not_approved():
	sel="""
		select * from tbl_document_tracking tdt
		where action_taken!="6"
		group by tracking_no ORDER BY tdt.date DESC
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking_refferal', methods = ['POST','GET'])
@login_required
def get_document_tracking_refferal():
	p = json.loads(request.data)
	sel="""
		select * from tbl_document_tracking_refferal where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_citezen_charter', methods = ['POST','GET'])
@login_required
def get_citezen_charter():
	sel="""
		select * from tbl_citezen_charter_path
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_rules_and_procedure', methods = ['POST','GET'])
@login_required
def get_rules_and_procedure():
	sel="""
		select * from tbl_rules_and_procedure
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_album_title', methods = ['POST','GET'])
@login_required
def save_album_title():
	p=json.loads(request.data)
	insert="insert into tbl_album_gallery set album_name='"+str(p['album'])+"', date_gen=now()"
	cud(insert)
	return jsonify("Successfully Saved")


@query.route('/get_album_title', methods = ['POST','GET'])
@login_required
def get_album_title():
	sel="""
		select *, date_format(date_gen, '%Y-%m-%d %r') date_gens,
		(select count(filename) from tbl_album_gallery_photo tagp2 WHERE tagp2.gallery_id=tag.gallery_id) count_images,
		(select path from tbl_album_gallery_photo tagp2 WHERE tagp2.gallery_id=tag.gallery_id limit 1) thumbnails
		from tbl_album_gallery tag
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/del_gallery_album', methods = ['POST','GET'])
@login_required
def del_gallery_album():
	p=json.loads(request.data)
	delete="""
		delete from tbl_album_gallery where gallery_id='"""+str(p['id'])+"""'
	"""
	cud(delete)
	return jsonify("Successfully Deleted")


@query.route('/get_gallery_images', methods = ['POST','GET'])
@login_required
def get_gallery_images():
	p=json.loads(request.data)
	sel="""
		select *, tagp.id pic_id from tbl_album_gallery tag
		left join tbl_album_gallery_photo tagp on tag.gallery_id=tagp.gallery_id
		where tag.gallery_id='"""+str(p['gallery_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_album_images', methods=['GET', 'POST'])
@login_required
def save_album_images():
	p=request.form
	for filename_array in request.files:
		file=request.files[filename_array]

		n_path = Path(__file__).parent / "../static/uploads/upload_albums" / str(p['gallery_id'])
		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				
			location1="upload_albums//"+str(p['gallery_id'])
			location1.replace("//", "\\\\");
			location=location1+"/"+filename
			path_location=location.replace("/", "\\\\");
			file_ = str(file.filename).replace("'","''")
			insert2="insert into tbl_album_gallery_photo set filename='"+str(file_)+"', path='"+str(path_location)+"', gallery_id='"+str(p['gallery_id'])+"', date=now()"
			cud(insert2)

	return jsonify("Succesfuly Saved")



@query.route('/save_citezen_charter', methods = ['POST','GET'])
@login_required
def save_citezen_charter():
	p=request.form
	for filename_array in request.files:
		file=request.files[filename_array]

		rd=int(round(datetime.now().timestamp()))

		n_path = Path(__file__).parent / "../static/uploads/upload_citezen_charter" / str(rd)
		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				
			location1="upload_citezen_charter//"+str(rd)
			location1.replace("//", "\\\\");
			location=location1+"/"+filename
			path_location=location.replace("/", "\\\\");
			split_name = str(file.filename).split(".")
			insert2="insert into tbl_citezen_charter_path set filename='"+str(split_name[0])+"', date_gen=now() ,path='"+str(path_location)+"'"
			cud(insert2)
	return jsonify("Succesfuly Saved")



@query.route('/del_citezen_charter_file', methods=['GET', 'POST'])
@login_required
def del_citezen_charter_file():
	p=json.loads(request.data)
	delete="delete from tbl_citezen_charter_path where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/save_rules_and_procedure', methods=['GET', 'POST'])
@login_required
def save_rules_and_procedure():
	f = request.form
	p=json.loads(f['Serialized'])
	if p['id']=="0":
		insert="""
			insert into tbl_rules_and_procedure set title='"""+str(p['title'])+"""', rules='"""+str(f['rules'])+"""', date_gen=now()
		"""
		cud(insert)
		return jsonify("Succesfuly Saved")
	else:
		update="""
			update tbl_rules_and_procedure set title='"""+str(p['title'])+"""', rules='"""+str(f['rules'])+"""', date_gen=now() where id='"""+str(p['id'])+"""'
		"""
		cud(update)
		return jsonify("Succesfuly Updated")


@query.route('/del_rules_and_procedure_file', methods=['GET', 'POST'])
@login_required
def del_rules_and_procedure_file():
	p=json.loads(request.data)
	delete="""
		delete from tbl_rules_and_procedure where id='"""+str(p['id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/get_download_center', methods=['GET', 'POST'])
@login_required
def get_download_center():
	sel="""
		select * from tbl_download_center_path
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_download_center', methods=['GET', 'POST'])
@login_required
def save_download_center():
	f=request.form
	p=json.loads(f['Serialized'])

	if p['id']=="0":
		for filename_array in request.files:
			file=request.files[filename_array]

			rd=int(round(datetime.now().timestamp()))

			n_path = Path(__file__).parent / "../static/uploads/upload_download_center" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_download_center//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				split_name = str(file.filename).split(".")
				insert2="insert into tbl_download_center_path set filename='"+str(split_name[0])+"', description='"+str(p['title'])+"' ,date_gen=now() ,path='"+str(path_location)+"'"
				cud(insert2)
	else:
		for filename_array in request.files:
			file=request.files[filename_array]

			rd=int(round(datetime.now().timestamp()))

			n_path = Path(__file__).parent / "../static/uploads/upload_download_center" / str(rd)
			n_path.resolve()

			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(n_path):
					os.mkdir(n_path)
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=n_path
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location1="upload_download_center//"+str(rd)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				
				split_name = str(file.filename).split(".")
				update="update tbl_download_center_path set filename='"+str(split_name[0])+"', description='"+str(p['title'])+"' ,date_gen=now() ,path='"+str(path_location)+"' where id='"+str(p['id'])+"'"
				cud(update)

	return jsonify("Succesfuly Saved")


@query.route('/del_download_center_file', methods=['GET', 'POST'])
@login_required
def del_download_center_file():
	p=json.loads(request.data)
	delete="""
		delete from tbl_download_center_path where id='"""+str(p['id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly Deleted")



@query.route('/del_pic', methods=['GET', 'POST'])
@login_required
def del_pic():
	p=json.loads(request.data)
	delete="""
		delete from tbl_album_gallery_photo where id='"""+str(p['id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/get_inventory_ordinances', methods=['GET', 'POST'])
@login_required
def get_inventory_ordinances():
	sel="""
		select *,
		(case 
			when source_of_document=1 then 
				"SANGUNUIAN FILES"
			when source_of_document=2 then 
				"SANGUNUIAN PANLALAWIGAN"
			else
				source_document_specify
		end) document_source ,

		(case when `status`=1 THEN
			concat("Propose ",' ', "ORDINANCE")
			when `status`=2 THEN
			concat("2nd Reading ",' ', "ORDINANCE")
			when `status`=3 THEN
			concat("3nd Reading ",' ', "ORDINANCE")
			when `status`=4 THEN
			concat("3nd Reading Rule Excemtion ",' ', "ORDINANCE")
			when `status`=5 THEN
			concat("For Mayor's Approval ",' ', "ORDINANCE")
			when `status`=6 THEN
			concat("Approved ",' ', "ORDINANCE")
			when `status`=7 THEN
			concat("Veto ",' ', "ORDINANCE")
			when `status`=8 THEN
			concat("Archived ",' ', "ORDINANCE")
			else
				`status`
			END
		) stats
		from tbl_ordinance tbo
		left join tbl_ordinance_status_numbers tosn on tosn.ordinance_id=tbo.ordinance_id
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/changeSystemType', methods=['GET', 'POST'])
@login_required
def changeSystemType():
	p=json.loads(request.data)
	upd="update tbl_config_info set type ='"+str(p['checktype'])+"', show_council_data='"+str(p['show_council_data'])+"' "
	cud(upd)
	return jsonify("Succesfuly Updated")


@query.route('/update_activeSp', methods=['GET', 'POST'])
@login_required
def update_activeSp():
	p=json.loads(request.data)
	upd="update tbl_sp set status='INACTIVE' where sp_id!='"+str(p['sp_id'])+"'"
	cud(upd)
	upd2="update tbl_sp set status='ACTIVE' where sp_id='"+str(p['sp_id'])+"'"
	cud(upd2)
	return jsonify("Succesfuly Updated")


@query.route('/count_documents', methods=['GET', 'POST'])
@login_required
def count_documents():
	sel1="""
		select count(*) total from tbl_ordinance t left join tbl_sp ts on ts.sp_id=t.sp_id where ts.`status`='ACTIVE'
	"""
	rd1=pyread(sel1)

	sel2="""
		select count(*) total from tbl_resolution t left join tbl_sp ts on ts.sp_id=t.sp_id where ts.`status`='ACTIVE'
	"""
	rd2=pyread(sel2)

	sel3="""
		select count(*) total from tbl_minutes t left join tbl_sp ts on ts.sp_id=t.sp_id where ts.`status`='ACTIVE'
	"""
	rd3=pyread(sel3)

	sel4="""
		select count(*) total from tbl_memorandom t left join tbl_sp ts on ts.sp_id=t.sp_id where ts.`status`='ACTIVE'
	"""
	rd4=pyread(sel4)

	sel5="""
		select count(*) total from tbl_petition t left join tbl_sp ts on ts.sp_id=t.sp_id where ts.`status`='ACTIVE'
	"""
	rd5=pyread(sel5)
	
	return jsonify(ordinance=rd1[0], resolution=rd2[0], minutes=rd3[0] , memorandom=rd4[0], petition=rd5[0])



@query.route('/save_role', methods=['GET', 'POST'])
@login_required
def save_role():
	p=json.loads(request.data)

	update ="update tbl_login set role='"+str(p['role_access'])+"' where login_id='"+str(p['login_id'])+"'"
	cud(update)

	delete = "delete from tbl_login_access where login_id='"+str(p['login_id'])+"'"
	cud(delete)

	if 'session' in p:
		insert ="insert into tbl_login_access set routes='/sessions', login_id='"+str(p['login_id'])+"'"
		cud(insert)
	if 'ordinance' in p:
		arr = ['/view_ordinance', '/proposed_ordinance', '/2nd_ordinance', '/3rd_ordinance', '/3rd_ordinance_exemption', '/for_approval_ordinance',
		 '/approval_ordinance', '/veto_ordinance', '/archive_ordinance']

		for i in arr:
			insert ="insert into tbl_login_access set routes='"+str(i)+"', login_id='"+str(p['login_id'])+"'"
			cud(insert)

	if 'resolution' in p:
		arr = ['/resolution', '/proposed_resolution', '/2nd_resolution', '/3rd_resolution', '/3rd_resolution_exemption', '/for_approval_resolution',
		 '/approval_resolution', '/veto_resolution', '/archive_resolution']
		for i in arr:
			insert ="insert into tbl_login_access set routes='"+str(i)+"', login_id='"+str(p['login_id'])+"'"
			cud(insert)

	if 'petition' in p:
		insert ="insert into tbl_login_access set routes='/petition', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'minutes' in p:
		insert ="insert into tbl_login_access set routes='/minutes', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'document_tracking' in p:
		insert ="insert into tbl_login_access set routes='/document_tracking', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'sp_budget' in p:
		arr = ['/sp_budget', '/capital_oultay', '/sp_member_deduction']

		for i in arr:
			insert ="insert into tbl_login_access set routes='"+str(i)+"', login_id='"+str(p['login_id'])+"'"
			cud(insert)

	if 'configuration' in p:
		arr = ['/sangunian', '/accounts', '/announcement', '/announcement', '/governance_classification', '/category', '/user',
		'/gmail_account', '/info', '/barangay', '/background']

		for i in arr:
			insert ="insert into tbl_login_access set routes='"+str(i)+"', login_id='"+str(p['login_id'])+"'"
			cud(insert)

	if 'committee' in p:
		insert ="insert into tbl_login_access set routes='/committee', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'gallery_albums' in p:
		insert ="insert into tbl_login_access set routes='/gallery_albums', login_id='"+str(p['login_id'])+"'"
		cud(insert)
	
	if 'executive_order' in p:
		insert ="insert into tbl_login_access set routes='/executive_order', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'memorandom' in p:
		insert ="insert into tbl_login_access set routes='/memorandom', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'barangay_ordinance' in p:
		insert ="insert into tbl_login_access set routes='/barangay_ordinance', login_id='"+str(p['login_id'])+"'"
		cud(insert)
	
	if 'barangay_resolution' in p:
		insert ="insert into tbl_login_access set routes='/barangay_resolution', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'documents_refferals' in p:
		insert ="insert into tbl_login_access set routes='/documents_refferals', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'reports' in p:
		insert ="insert into tbl_login_access set routes='/reports', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	if 'profiling_ordinance' in p:
		insert ="insert into tbl_login_access set routes='/profiling_ordinance', login_id='"+str(p['login_id'])+"'"
		cud(insert)
	
	if 'citezen_charter' in p:
		insert ="insert into tbl_login_access set routes='/citezen_charter', login_id='"+str(p['login_id'])+"'"
		cud(insert)
	
	
	if 'rules_and_procedure' in p:
		insert ="insert into tbl_login_access set routes='/rules_and_procedure', login_id='"+str(p['login_id'])+"'"
		cud(insert)


	if 'download_center' in p:
		insert ="insert into tbl_login_access set routes='/download_center', login_id='"+str(p['login_id'])+"'"
		cud(insert)

	return jsonify("Succesfuly Updated")


@query.route('/pre_register', methods=['GET', 'POST'])
@login_required
def pre_register():
	f=request.form
	p=json.loads(f['Serialized'])

	insert_gmail="insert into tbl_gmail set email='"+str(p['email'])+"', password='"+str(p['gmail_pass'])+"'"
	cud(insert_gmail)

	insert_login="insert into tbl_login set username='"+str(p['username'])+"', password='"+str(p['password'])+"', role='2', fullname='"+str(p['fullname'])+"'"
	cud(insert_login)

	insert_config="insert into tbl_config_info set city_name='"+str(p['city'])+"', type=1"
	cud(insert_config)

	sp_year = str(p['sp_from'])+"-"+str(p['sp_to'])
	insert_sp="insert into tbl_sp set sp_title='"+str(p['sp_title'])+"', sp_year='"+str(sp_year)+"', `status`='ACTIVE' "
	ids = cud_callbackid(insert_sp)

	insert_member= "insert into sp_member set sp_mayor='"+str(p['mayor'])+"', sp_vice_mayor='"+str(p['vmayor'])+"', sp_secretary='"+str(p['sec'])+"', sp_id='"+str(ids)+"'"
	ids_member =cud_callbackid(insert_member)

	for i in p['council_name']:
		print(i['council_name'])
		insert_council = "insert into sp_councilor set councilor = '"+str(i['council_name'])+"', sp_member_id= '"+str(ids_member)+"'"
		cud(insert_council)


	for filename_array in request.files:
		file=request.files[filename_array]

		n_path = Path(__file__).parent / "../static/uploads/upload_sp_logo" / str(ids)
		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				
			location1="upload_sp_logo//"+str(ids)
			location1.replace("//", "\\\\");
			location=location1+"/"+filename
			path_location=location.replace("/", "\\\\");
			
			split_name = str(file.filename).split(".")
			insert2="update tbl_sp set city_logo='"+str(path_location)+"' where sp_id='"+str(ids)+"'"
			cud(insert2)

	return jsonify("Succesfuly Inserted")


@query.route('/save_document_tracking', methods=['GET', 'POST'])
@login_required
def save_document_tracking():
	f=request.form
	p=json.loads(f['Serialized'])
	title=p['title'].replace("'","''")

	if p['h_document_tracking']==0 or p['h_document_tracking']=="0":
		insert="""
			insert into tbl_document_tracking set tracking_no='"""+str(p['tracking_no'])+"""', 
			date=now() , title='"""+str(p['title'])+"""', refferals_from='"""+str(p['refferal_from'])+"""', 
			action_taken = '1'
		"""
		rd=cud_callbackid(insert)
		ids = rd
	else:
		update="""
			update tbl_document_tracking set tracking_no='"""+str(p['tracking_no'])+"""', date=now() , title='"""+str(title)+"""' , 
			refferals_from='"""+str(p['refferal_from'])+"""', action_taken = '1'
			where track_gen_id='"""+str(p['h_document_tracking'])+"""'
		"""
		cud(update)
		ids = p['h_document_tracking']

	for filename_array in request.files:
		file=request.files[filename_array]

		f = filename_array.split("[")[0]

		if f=='file':
			n_path = Path(__file__).parent / "../static/uploads/upload_document_tracking" / str(ids)

		n_path.resolve()

		if file and allowed_file(file.filename):
			filename = str(custom_secure_filename(file.filename)).replace("'","''")
			if not os.path.exists(n_path):
				os.mkdir(n_path)
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				app.config['UPLOAD_FOLDER']=n_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			if f=='file':
				location1="upload_document_tracking//"+str(ids)
				location1.replace("//", "\\\\");
				location=location1+"/"+filename
				path_location=location.replace("/", "\\\\");
				split_name = str(file.filename).split(".")

				if split_name:
					query = "insert tbl_document_tracking_path set path='"+str(path_location.replace("'","''"))+"', filename='"+str(split_name[0].replace("'","''"))+"', track_gen_id='"+str(ids)+"'"
					insert2=query
					cud(insert2)

	return jsonify("Succesfuly Saved")


@query.route('/delete_document_tracking', methods=['GET', 'POST'])
@login_required
def delete_document_tracking():
	p= json.loads(request.data)
	delete = """
		delete from tbl_document_tracking  where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly Deleted")


@query.route('/get_document_tracking_file', methods=['GET', 'POST'])
@login_required
def get_document_tracking_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_document_tracking_path tmp
		where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_document_tracking_raw_file', methods=['GET', 'POST'])
@login_required
def get_document_tracking_raw_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_document_tracking_path_raw tmp
		where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/del_document_tracking_file', methods=['GET', 'POST'])
@login_required
def del_document_tracking_file():
	p=json.loads(request.data)
	sel="select * from tbl_document_tracking_path where documents_path_id='"+str(p['documents_path_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_document_tracking_path where documents_path_id='"+str(p['documents_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_document_tracking_path where documents_path_id='"+str(p['documents_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")

@query.route('/del_document_tracking_raw_file', methods=['GET', 'POST'])
@login_required
def del_document_tracking_raw_file():
	p=json.loads(request.data)
	sel="select * from tbl_document_tracking_path_raw where documents_path_id='"+str(p['documents_path_id'])+"'"
	rd=pyread(sel)
	if rd:
		n_path = Path(__file__).parent / "../static/uploads/" / rd[0]['path']
		n_path.resolve()
		if Path(n_path).is_file():
			Path(n_path).unlink()
			delete="delete from tbl_document_tracking_path_raw where documents_path_id='"+str(p['documents_path_id'])+"'"
			cud(delete)
			return jsonify("Succesfuly Deleted")
		else:
			delete="delete from tbl_document_tracking_path_raw where documents_path_id='"+str(p['documents_path_id'])+"'"
			cud(delete)
			return jsonify("File does not exist")
	else:
		return jsonify("Not exists in database")

@query.route('/get_active_councilors', methods = ['POST','GET'])
@login_required
def get_active_councilors():
	sel = """
		SELECT
			tpi.info_id,
			concat( f_name, ' ', m_name, ' ', L_name ) fullname,
			sc.sp_councilor
		FROM
			sp_councilor sc
			LEFT JOIN tbl_personal_info tpi ON sc.councilor = tpi.info_id
			LEFT JOIN sp_member sp ON sp.sp_member_id = sc.sp_member_id
			LEFT JOIN tbl_sp ts ON ts.sp_id = sp.sp_id
		WHERE
		ts.`status` = 'Active'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_coucilor_assign', methods=['GET', 'POST'])
@login_required
def save_coucilor_assign():
	p=json.loads(request.data)
	if p['ids']==0 or p['ids']=='0':
		insert = """
			insert into sp_assignment set sp_assign='"""+str(p['title'])+"""', sp_councilor='"""+str(p['sp_councilor'])+"""'
		"""
		cud(insert)
	else:
		update = """
			update sp_assignment set sp_assign='"""+str(p['title'])+"""', sp_councilor='"""+str(p['sp_councilor'])+"""' where id='"""+str(p['id'])+"""'
		"""
		cud(update)
	return jsonify("Succesfuly Saved")



@query.route('/get_councilor_assignment', methods = ['POST','GET'])
@login_required
def get_councilor_assignment():
	sel = """
		select *, concat( f_name, ' ', m_name, ' ', L_name ) fullname
		from sp_assignment spa
		left join sp_councilor sc on sc.sp_councilor=spa.sp_councilor
		LEFT JOIN tbl_personal_info tpi ON sc.councilor = tpi.info_id
		LEFT JOIN sp_member sp ON sp.sp_member_id = sc.sp_member_id
		LEFT JOIN tbl_sp ts ON ts.sp_id = sp.sp_id
		where ts.`status` = 'Active'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/del_councilor_assign', methods = ['POST','GET'])
@login_required
def del_councilor_assign():
	p = json.loads(request.data)
	delete="delete from sp_assignment where id='"+str(p['id'])+"'"
	cud(delete)
	return jsonify('Succesfuly Deleted')


@query.route('/get_specific_data_councilor', methods = ['POST','GET'])
@login_required
def get_specific_data_councilor():
	p = json.loads(request.data)
	sel = """
		select * from sp_councilor sc
		left join tbl_personal_info tpi on tpi.info_id=sc.councilor
		where sp_councilor='"""+str(p['sp_councilor'])+"""' 
	"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_reports_information', methods = ['POST','GET'])
@login_required
def get_committee_reports_information():
	p = json.loads(request.data)

	if p['type']=="1":
		sel = """
			select *, group_concat(DISTINCT path) file 
			from tbl_committee_report tcr
			left join tbl_committee tc on tc.committee_id=tcr.committee_id
			left join tbl_committee_reports_file rcrf on rcrf.committee_reports_id=tcr.id
			where tcr.sp_id='"""+str(p['sp_id'])+"""' and tcr.committee_id='"""+str(p['committee_id'])+"""'
			group by tcr.id
		"""
	else:
		sel = """
			select * , group_concat(DISTINCT path) file
			from tbl_committee_information  tci
			left join tbl_committee tc on tc.committee_id=tci.committee_id
			left join tbl_committee_information_file rcif on rcif.committee_information_id=tci.id
			where tci.sp_id='"""+str(p['sp_id'])+"""' and tci.committee_id='"""+str(p['committee_id'])+"""'
			group by tci.id
		"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_minutes_reports', methods = ['POST','GET'])
@login_required
def get_committee_minutes_reports():
	p = json.loads(request.data)

	sel = """
		select *, group_concat(DISTINCT path) file 
		from tbl_committee_minutes tcr
		left join tbl_committee tc on tc.committee_id=tcr.committee_id
		left join tbl_committee_minutes_file rcrf on rcrf.committee_minutes_id=tcr.id
		where tcr.sp_id='"""+str(p['sp_id'])+"""' and tcr.committee_id='"""+str(p['committee_id'])+"""'
		group by tcr.id
	"""
	rd = pyread(sel)
	return jsonify(rd)

@query.route('/get_councilor_info_documents', methods = ['POST','GET'])
@login_required
def get_councilor_info_documents():
	p = json.loads(request.data)
	sel= """
		select ordinance_title title, date_enacted, ordinance_number, 'Author' type 
		from tbl_ordinance_author toa
		left join tbl_ordinance tord on tord.ordinance_id=toa.ordinance_id
		where toa.author='"""+str(p['info_id'])+"""' and tord.ordinance_number is not null

		union

		select ordinance_title title, date_enacted, ordinance_number, 'Sponsor' type 
		from tbl_ordinance_sponsor toa
		left join tbl_ordinance tord on tord.ordinance_id=toa.ordinance_id
		where toa.sponsor='"""+str(p['info_id'])+"""' and tord.ordinance_number is not null

	"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/get_committee_minutes', methods = ['POST','GET'])
@login_required
def get_committee_minutes():
	p = json.loads(request.data)
	sel= """
		select * from tbl_committee_minutes tme
		left join tbl_committee tc on tc.committee_id=tme.committee_id
		left join tbl_sp ts on ts.sp_id = tme.sp_id
		where ts.status='ACTIVE'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/save_committee_minutes', methods = ['POST','GET'])
@login_required
def save_committee_minutes():
	p=request.form
	p=json.loads(p['Serialized'])

	if p['h_committee_minutes_id']=='0':
		insert = """
			insert into tbl_committee_minutes set tracking_number='"""+str(p['tracking_number'])+"""', 
			subject='"""+str(p['subject'])+"""', committee_id='"""+str(p['committee_id'])+"""', 
			date='"""+str(p['date'])+"""', sp_id = '"""+str(p['sp_id'])+"""'
		"""
		ids = cud_callbackid(insert)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "upload_committee_minutes"
			location=""+str(loc)+"//"+str(ids)
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
			os.chdir(cwd)

			insert2="insert into tbl_committee_minutes_file set path='"+str(path_location)+"' , filename='"+str(filename.replace("'",""))+"' , committee_minutes_id='"+str(ids)+"'"
			cud(insert2)
	else:
		update = """
			update  tbl_committee_minutes set tracking_number='"""+str(p['tracking_number'])+"""', subject='"""+str(p['subject'])+"""',
			committee_id='"""+str(p['committee_id'])+"""', date='"""+str(p['date'])+"""' , sp_id = '"""+str(p['sp_id'])+"""'
			where id='"""+str(p['h_committee_minutes_id'])+"""'
		"""
		cud(update)

		for filename_array in request.files:
			file=request.files[filename_array]
			cwd = os.getcwd()
			os.chdir(cwd)
			os.chdir('application')
			os.chdir('static')
			loc = "upload_committee_minutes"
			location=""+str(loc)+"//"+str(p['h_committee_minutes_id'])
			location.replace("//", "\\\\");
			if file and allowed_file(file.filename):
				filename = str(custom_secure_filename(file.filename)).replace("'","''")
				if not os.path.exists(location):
					os.mkdir(location)
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				else:
					app.config['UPLOAD_FOLDER']=location
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					
				location=location+"/"+filename
				path_location=location.replace("/", "\\\\");
			os.chdir(cwd)

			insert2="insert into tbl_committee_minutes_file set path='"+str(path_location)+"' , filename='"+str(filename.replace("'",""))+"' , committee_minutes_id='"+str(p['h_committee_minutes_id'])+"'"
			cud(insert2)

	return jsonify("Succesfuly Saved")


@query.route('/get_session_list_report', methods = ['POST','GET'])
@login_required
def get_session_list_report():
	p=json.loads(request.data)
	
	if 'term' in p:
		pass
	else:
		p['term']=0

	if 'type' in p:
		if p['type']=='':
			p['type']=0
			pass
	else:
		p['type']=0

	if p['from']:
		pass
	else:
		p['from']=0

	if p['to']:
		pass
	else:
		p['to']=0

	if p['type']==0 and p['term']==0 and p['from']==0 and p['to']==0:
		prnt_R(1)
		sel= """
			select * from tbl_session order
		"""
	elif p['type']!=0 and p['term']!=0 and p['from']!=0 and p['to']!=0:
		prnt_R(2)
		sel= """
			select * from tbl_session 
			where (session_date between '"""+str(p['from'])+"""' and '"""+str(p['to'])+"""') 
			and sp_number='"""+str(p['term'])+"""' and session_type='"""+str(p['type'])+"""'
		"""
	elif p['type']!=0 and p['term']==0 and p['from']==0 and p['to']==0:
		prnt_R(3)
		sel= """
			select * from tbl_session 
			where session_type='"""+str(p['type'])+"""'
		"""
	elif p['type']!=0 and p['term']!=0 and p['from']==0 and p['to']==0:
		prnt_R(4)
		sel= """
			select * from tbl_session 
			where session_type='"""+str(p['type'])+"""' and sp_number='"""+str(p['term'])+"""'
		"""
	elif p['type']==0 and p['term']!=0 and p['from']==0 and p['to']==0:
		prnt_R(5)
		sel= """
			select * from tbl_session 
			where sp_number='"""+str(p['term'])+"""'
		"""
	elif p['type']==0 and p['term']!=0 and p['from']!=0 and p['to']!=0:
		prnt_R(6)
		sel= """
			select * from tbl_session 
			where (session_date between '"""+str(p['from'])+"""' and '"""+str(p['to'])+"""') 
			and sp_number='"""+str(p['term'])+"""'
		"""
	elif p['type']!=0 and p['term']==0 and p['from']!=0 and p['to']!=0:
		prnt_R(7)
		sel= """
			select * from tbl_session 
			where (session_date between '"""+str(p['from'])+"""' and '"""+str(p['to'])+"""') 
			and session_type='"""+str(p['type'])+"""'
		"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/get_recitation_file', methods = ['POST','GET'])
@login_required
def get_recitation_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_session_recitation_path where session_id='"""+str(p['session_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_reading_file', methods = ['POST','GET'])
@login_required
def get_reading_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_session_reading_path where session_id='"""+str(p['session_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_privilege_hour_file', methods = ['POST','GET'])
@login_required
def get_privilege_hour_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_session_privilege_path where session_id='"""+str(p['session_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_announcement_file', methods = ['POST','GET'])
@login_required
def get_announcement_file():
	p=json.loads(request.data)
	sel="""
		select * from tbl_session_announcement_path where session_id='"""+str(p['session_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

	

@query.route('/get_attendance_by_session', methods = ['POST','GET'])
@login_required
def get_attendance_by_session():
	p=json.loads(request.data)
	sel_roll_call = "select *, CONCAT(tri.f_name,' ',tri.m_name, ' ', tri.l_name) as fullname FROM tbl_session_roll_call tsrc LEFT JOIN tbl_personal_info tri on tsrc.info_id = tri.info_id WHERE tsrc.session_id = '"+str(p['session_id'])+"'"
	rd = pyread(sel_roll_call)
	return jsonify(rd)


@query.route('/get_session_attendance', methods = ['POST','GET'])
@login_required
def get_session_attendance():
	p=json.loads(request.data)
	sel_roll_call = """
		select CONCAT(tri.f_name,' ',tri.m_name, ' ', tri.l_name) as fullname , tsrc.info_id, roll_call_id,
		session_id, status
		FROM tbl_session_roll_call tsrc
		LEFT JOIN tbl_personal_info tri on tsrc.info_id = tri.info_id 
		WHERE tsrc.session_id = '"""+str(p['session_id'])+"""'
	"""
	rd = pyread(sel_roll_call)
	return jsonify(rd)


@query.route('/save_session_attendance', methods = ['POST','GET'])
@login_required
def save_session_attendance():
	p=json.loads(request.data)
	for i in p['rollCall']:
		if i:
			if i['id']!='':
				update = """
					update tbl_session_roll_call set status='"""+str(i['status'])+"""' 
					where roll_call_id='"""+str(i['id'])+"""' and session_id='"""+str(p['session_id'])+"""'
				"""
				cud(update)
			else:
				insert = """
				 	insert into tbl_session_roll_call set status='"""+str(i['status'])+"""',
				 	session_id='"""+str(p['session_id'])+"""', info_id='"""+str(i['info_id'])+"""'
				"""
				cud(insert)
	return jsonify(p)


@query.route('/delete_people_attendance', methods = ['POST','GET'])
@login_required
def delete_people_attendance():
	p=json.loads(request.data)
	delete="""
		delete from tbl_session_roll_call where roll_call_id='"""+str(p['id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfully deleted")


@query.route('/delete_session', methods = ['POST','GET'])
@login_required
def delete_session():
	p=json.loads(request.data)
	delete = """
		delete from tbl_session where session_id='"""+str(p['session_id'])+"""'
	"""
	cud(delete)
	return jsonify("Succesfuly Deleted")



@query.route('/save_propose', methods = ['POST','GET'])
def save_propose():
	p=json.loads(request.data)
	select  = "select action_taken from tbl_document_tracking where track_gen_id="+str(p['track_gen_id'])+" "
	rd = pyread(select)

	if rd[0]['action_taken']=="1":
		update = """
			update tbl_document_tracking set action_taken = 2, doc_status='' where track_gen_id='"""+str(p['track_gen_id'])+"""'
		"""
		cud(update)

		delete_ref = """
			delete from tbl_document_tracking_refferal where track_gen_id='"""+str(p['track_gen_id'])+"""'
		"""
		cud(delete_ref)

	f_committee = ""
	for index, i in enumerate(p['committee_ids'][0]):
		f_committee = f_committee +"committee_id="+str(i)+" or "
		if index==(len(p['committee_ids'][0])-1):
			f_committee = f_committee + "committee_id="+str(i)+""

	select_committee = """
		select group_concat(committee) committees from tbl_committee where """+str(f_committee)+"""
	"""
	rd_com = pyread(select_committee)

	n_committe = str(p['committee_ids'][0]).replace('[','').replace(']','').replace('\'','').replace('\"','')

	insert = """
		insert into tbl_document_tracking_refferal set track_gen_id='"""+str(p['track_gen_id'])+"""',
		committtee='"""+str(n_committe)+"""'
	"""
	cud(insert)

	insert_status = """
		insert into tbl_document_tracking_status set track_gen_id='"""+str(p['track_gen_id'])+"""',
		status='Approved as 1st Reading and Reffered to Committee', remarks='"""+str(rd_com[0]['committees'])+"""', date=now()
	"""
	cud(insert_status)

	sel = """
		select group_concat(tc.committee SEPARATOR ' - ') committee from tbl_document_tracking tdt
		left join tbl_session_proposed_ordi tspo on tdt.track_gen_id=tspo.tracking_no
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
		left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
		where tdt.track_gen_id = '"""+str(p['track_gen_id'])+"""'

	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/save_second', methods = ['POST','GET'])
@login_required
def save_second():
	p=json.loads(request.data)
	select  = "select action_taken from tbl_document_tracking where track_gen_id="+str(p['track_gen_id'])+" "
	rd = pyread(select)

	if rd[0]['action_taken']=="2":
		update = """
			update tbl_document_tracking set action_taken = 3, doc_status='' where track_gen_id='"""+str(p['track_gen_id'])+"""'
		"""
		cud(update)

		delete_ref = """
			delete from tbl_document_tracking_refferal where track_gen_id='"""+str(p['track_gen_id'])+"""'
		"""
		cud(delete_ref)

	f_committee = ""
	for index, i in enumerate(p['committee_ids'][0]):
		f_committee = f_committee +"committee_id="+str(i)+" or "
		if index==(len(p['committee_ids'][0])-1):
			f_committee = f_committee + "committee_id="+str(i)+""

	select_committee = """
		select group_concat(committee) committees from tbl_committee where """+str(f_committee)+"""
	"""
	rd_com = pyread(select_committee)

	n_committe = str(p['committee_ids'][0]).replace('[','').replace(']','').replace('\'','').replace('\"','')

	insert = """
		insert into tbl_document_tracking_refferal set track_gen_id='"""+str(p['track_gen_id'])+"""',
		committtee='"""+str(n_committe)+"""'
	"""
	cud(insert)

	insert_status = """
		insert into tbl_document_tracking_status set track_gen_id='"""+str(p['track_gen_id'])+"""',
		status='Approved as 2nd Reading and Reffered to Committee', remarks='"""+str(rd_com[0]['committees'])+"""', date=now()
	"""
	cud(insert_status)

	sel = """
		select group_concat(tc.committee SEPARATOR ' - ') committee from tbl_document_tracking tdt
		left join tbl_session_proposed_ordi tspo on tdt.track_gen_id=tspo.tracking_no
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
		left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
		where tdt.track_gen_id = '"""+str(p['track_gen_id'])+"""'

	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/disapproved_proposed', methods = ['POST','GET'])
@login_required
def disapproved_proposed():
	p=json.loads(request.data)
	update = """
		update tbl_document_tracking set action_taken=1, doc_status = 1 where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(update)

	delete = "delete from tbl_document_tracking_refferal where track_gen_id="+str(p['track_gen_id'])+""
	cud(delete)

	insert_status = """
		insert into tbl_document_tracking_status set track_gen_id='"""+str(p['track_gen_id'])+"""',
		status='Disapproved', remarks='Disapproved', date=now()
	"""
	cud(insert_status)

	sel = """
		select group_concat(tc.committee SEPARATOR ' - ') committee from tbl_document_tracking tdt
		left join tbl_session_proposed_ordi tspo on tdt.track_gen_id=tspo.tracking_no
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
		left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
		where tdt.track_gen_id = '"""+str(p['track_gen_id'])+"""'

	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking_where_trackgenId', methods = ['POST','GET'])
def get_document_tracking_where_trackgenId():
	p=json.loads(request.data)
	sel = """
		select * from tbl_document_tracking tdt
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
		where tdt.track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd = pyread(sel)
	return jsonify(rd)


@query.route('/update_proposed', methods = ['POST','GET'])
@login_required
def update_proposed():
	p=json.loads(request.data)
	delete_ref = """
		delete from tbl_document_tracking_refferal where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(delete_ref)

	n_committe = str(p['committee_ids'][0]).replace('[','').replace(']','').replace('\'','').replace('\"','')

	f_committee = ""
	for index, i in enumerate(p['committee_ids'][0]):
		f_committee = f_committee +"committee_id="+str(i)+" or "
		if index==(len(p['committee_ids'][0])-1):
			f_committee = f_committee + "committee_id="+str(i)+""

	select_committee = """
		select group_concat(committee) committees from tbl_committee where """+str(f_committee)+"""
	"""
	rd_com = pyread(select_committee)

	n_committe = str(p['committee_ids'][0]).replace('[','').replace(']','').replace('\'','').replace('\"','')

	insert = """
		insert into tbl_document_tracking_refferal set track_gen_id='"""+str(p['track_gen_id'])+"""',
		committtee='"""+str(n_committe)+"""'
	"""
	cud(insert)

	insert_status = """
		insert into tbl_document_tracking_status set track_gen_id='"""+str(p['track_gen_id'])+"""',
		status='Change of Reffered Committee', remarks='"""+str(rd_com[0]['committees'])+"""', date=now()
	"""
	cud(insert_status)

	sel = """
		select group_concat(tc.committee SEPARATOR ' - ') committee from tbl_document_tracking tdt
		left join tbl_session_proposed_ordi tspo on tdt.track_gen_id=tspo.tracking_no
		left join tbl_document_tracking_refferal tdtr on tdtr.track_gen_id=tdt.track_gen_id
		left JOIN tbl_committee tc ON FIND_IN_SET(tc.committee_id, REPLACE(tdtr.committtee, " ", ""))
		where tdt.track_gen_id = '"""+str(p['track_gen_id'])+"""'

	"""
	rd= pyread(sel)

	return jsonify(rd)


@query.route('/approve_document', methods = ['POST','GET'])
def approve_document():
	p=json.loads(request.data)
	if p['status']=="1":
		n = "1st"
	elif p['status']=="2":
		n = "2nd"
	elif p['status']=="3":
		n = "3rd"
	stat = "Approved as " + n + " reading"
	upd = """
		update tbl_document_tracking set action_taken='"""+str(int(p['status'])+1)+"""' where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(upd)

	insert_status = """
		insert into tbl_document_tracking_status set track_gen_id='"""+str(p['track_gen_id'])+"""',
		status='"""+str(stat)+"""', remarks='Approved', date=now()
	"""
	cud(insert_status)
	return jsonify("Succesfuly Saved")



@query.route('/cancel_document', methods = ['POST','GET'])
@login_required
def cancel_document():
	p=json.loads(request.data)
	if p['status']=="1":
		n = "1st"
	elif p['status']=="2":
		n = "2nd"
	elif p['status']=="3":
		n = "3rd"

	stat = "Approved as " + n + " reading"

	upd = """
		update tbl_document_tracking set action_taken='"""+str(int(p['status']))+"""' where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(upd)

	delete = """
		delete from tbl_document_tracking_status where track_gen_id='"""+str(p['track_gen_id'])+"""' and 
		status='"""+str(stat)+"""'
	"""
	cud(delete)

	return jsonify("Succesfuly Canceled")


@query.route('/get_document_status_tracking', methods = ['POST','GET'])
def get_document_status_tracking():
	p=json.loads(request.data)
	sel = """
		select * from tbl_document_tracking where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd= pyread(sel)
	return jsonify(rd)


@query.route('/save_doc_authors', methods = ['POST','GET'])
@login_required
def save_doc_authors():
	p= request.form
	p=json.loads(p['Serialized'])

	if p['track_gen_id']==0:
		prnt_Y("insert")
	else:
		prnt_Y("update")
		delete_author = "delete from tbl_document_tracking_author where track_gen_id='"+str(p['track_gen_id'])+"'"
		cud(delete_author)
		delete_coauthor = "delete from tbl_document_tracking_coauthor where track_gen_id='"+str(p['track_gen_id'])+"'"
		cud(delete_coauthor)
		delete_sponsor = "delete from tbl_document_tracking_sponsor where track_gen_id='"+str(p['track_gen_id'])+"'"
		cud(delete_sponsor)
		delete_cosponsor = "delete from tbl_document_tracking_cosponsor where track_gen_id='"+str(p['track_gen_id'])+"'"
		cud(delete_cosponsor)

	if "input_authors" in p:
		for i in p['input_authors']:
			insert_author = """
				insert into tbl_document_tracking_author set councilor='"""+str(i)+"""', track_gen_id='"""+str(p['track_gen_id'])+"""'
			"""
			cud(insert_author)

	if "input_coauthors" in p:
		for i in p['input_coauthors']:
			insert_coauthors = """
				insert into tbl_document_tracking_coauthor set councilor='"""+str(i)+"""', track_gen_id='"""+str(p['track_gen_id'])+"""'
			"""
			cud(insert_coauthors)

	if "input_sponsors" in p:
		for i in p['input_sponsors']:
			insert_sponsors = """
				insert into tbl_document_tracking_sponsor set councilor='"""+str(i)+"""', track_gen_id='"""+str(p['track_gen_id'])+"""'
			"""
			cud(insert_sponsors)

	if "input_cosponsors" in p:
		for i in p['input_cosponsors']:
			insert_cosponsors = """
				insert into tbl_document_tracking_cosponsor set councilor='"""+str(i)+"""', track_gen_id='"""+str(p['track_gen_id'])+"""'
			"""
			cud(insert_cosponsors)
	return jsonify("Succesfuly Saved")



@query.route('/get_document_tracking_authors', methods = ['POST','GET'])
@login_required
def get_document_tracking_authors():
	p=json.loads(request.data)
	sel= """
		select * from tbl_document_tracking_author where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking_coauthors', methods = ['POST','GET'])
@login_required
def get_document_tracking_coauthors():
	p=json.loads(request.data)
	sel= """
		select * from tbl_document_tracking_coauthor where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_document_tracking_sponsor', methods = ['POST','GET'])
@login_required
def get_document_tracking_sponsor():
	p=json.loads(request.data)
	sel= """
		select * from tbl_document_tracking_sponsor where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)

@query.route('/get_document_tracking_cosponsor', methods = ['POST','GET'])
@login_required
def get_document_tracking_cosponsor():
	p=json.loads(request.data)
	sel= """
		select * from tbl_document_tracking_cosponsor where track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/reffer_back_document', methods = ['POST','GET'])
@login_required
def reffer_back_document():
	p=json.loads(request.data)
	insert = """
		insert into tbl_document_tracking_status set date=now(), status='Reffered back', track_gen_id='"""+str(p['track_gen_id'])+"""'
	"""
	cud(insert)
	return jsonify("Success")



@query.route('/get_codification_ordinance', methods = ['POST','GET'])
@login_required
def get_codification_ordinance():
	p=json.loads(request.data)
	if p['status']==1:
		if "category" in p and p['category']!="":
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
				where tbo.category='"""+str(p['category'])+"""'
			"""
		else:
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
			"""
		
	elif p['status']==2:
		if "category" in p and p['category']!="":
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
				where (tosn.original=1 or tosn.ammended_no!='') and tbo.category='"""+str(p['category'])+"""'
			"""
		else:
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
				where (tosn.original=1 or tosn.ammended_no!='')
			"""
	else:
		if "category" in p and p['category']!="":
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
				where (repealed_no!='' or obsolet_ord!='') and tbo.category='"""+str(p['category'])+"""'
			"""
		else:
			sel="""
				select tbo.ordinance_number , tbo.date_enacted, tbo.ordinance_title,
				(case when original=1 then 'original' when ammended_no!='' then 'ammended' when repealed_no!='' then 'repealed' when superseded_no!='' then 'superseded' when missing_ord then 'missing' when obsolet_ord then 'obsolet' else 'unassigned' end) `status`,
				'' remarks
				from tbl_ordinance tbo
				left join tbl_ordinance_status_numbers tosn on tbo.ordinance_id=tosn.ordinance_id
				left join tbl_category tc on tc.category_id=tbo.category
				where (repealed_no!='' or obsolet_ord!='')
			"""
	rd=pyread(sel)
	return jsonify(rd)


@query.route('/get_access_role', methods = ['POST','GET'])
@login_required
def get_access_role():
	p=json.loads(request.data)
	sel= """
		select * from tbl_login_access where login_id=%s
	"""
	args=(str(p['login_id']),)
	rd=rd_query(sel,args)
	prnt_R(rd)
	return jsonify(rd)