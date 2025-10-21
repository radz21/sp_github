from flask import redirect, url_for, render_template, request, jsonify, json, session, request
from . import main
from models.routes_database import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
import shutil
from pathlib import Path, PurePath

imp_folders = [
	'upload_barangay_ordinance',
	'upload_barangay_resolution',
	'upload_city_logo',
	'upload_committee_ordinance_files',
	'upload_committee_ordinance_minutes_files',
	'upload_committee_petition_files',
	'upload_committee_petition_minutes_files',
	'upload_committee_resolution_files',
	'upload_committee_resolution_minutes_files',
	'upload_document_referals',
	'upload_executive_order',
	'upload_files',
	'upload_files_minutes',
	'upload_files_resolution',
	'upload_files_resolution_minutes',
	'upload_memorandom',
	'upload_ordinance_files',
	'upload_priv_hour',
	'upload_sp_logo',
	'upload_veto_ordinance',
	'upload_visitor_file',
	'upload_download_center',
	'upload_albums',
	'upload_files_committee_reports',
	'upload_citezen_charter',
	'upload_document_tracking',
	'upload_committee_report_files',
	'upload_committee_information_files',
	'upload_committee_minutes',
	'upload_committee_report_files',
	'upload_files_minutes2',
	'emp_photo',
	'gallery',
	'upload_albums',
	'upload_document_tracking',
	'recitation_of_councilor'
]

insert = "SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))"
cud(insert)

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'index' in session:
        	if session['sessioned_role']=="2":
        		return f(*args, **kws)
        	else:
	        	lists=session['obj']
	        	x = get_access(lists)
	        	if x:
	        		return f(*args, **kws)
	        	else:
	        		return redirect(url_for('main.not_allowed')) 
        else:
        	return redirect(url_for('main.logins'))  
    return decorated_function


def get_access(lists):
	current_route = request.url_rule
	flag = False
	for i in lists:
		if str(i)==str(current_route):
			return True
	return False


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kws):
		if 'index' in session:
			return f(*args, **kws)
		else:
			return redirect(url_for('main.logins'))
	return decorated_function
	

@main.route('/not_allowed_to_access_this_page')
def not_allowed():
	return render_template('errors/error500.html')


@main.route('/landing', methods=['GET', 'POST'])
def landing_page():
	sel_announcement = "SELECT * from tbl_announcement"
	rd_announcement = pyread(sel_announcement)
	prnt_G(type(json.dumps(rd_announcement)))
	return render_template('/landing_page/home.html', data=rd_announcement)


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	session_data=session['data']
	return render_template('index.html', data=session_data)

@main.route('/sessions', methods=['GET', 'POST'])
@authorize
def sessions():
	session_data=session['data']
	return render_template('index.html', data=session_data)


@main.route('/document_tracking', methods=['GET', 'POST'])
@authorize
def document_tracking():
	session_data=session['data']
	return render_template('index.html', data=session_data)

	
@main.route('/announcements', methods=['GET', 'POST'])
def announcements():
	sel_announcement = "SELECT * from tbl_announcement"
	rd_announcement = pyread(sel_announcement)
	return render_template('/landing_page/announcement.html', data = rd_announcement)


@main.route('/committee', methods=['GET', 'POST'])
@authorize
def committee():
	session_data=session['data']
	return render_template('config/comitee.html', data=session_data)


@main.route('/', methods=['GET', 'POST'])
def layout():
	if 'index' in session:
		return redirect(url_for('main.home'))
	else:
		print("You're not in session please login first")
		return render_template('login.html')

@main.route('/committees', methods=['GET', 'POST'])
def committees():
	sel_info="""
		select *,
		CONCAT(tpi.f_name, " ", tpi.m_name, " ", tpi.l_name) as co_chair
		from tbl_committee tc
		left join tbl_personal_info tpi ON tc.co_chairman = tpi.info_id
		left join tbl_sp ts on ts.sp_id=tc.sp_id
		where ts.`status`='ACTIVE' 
	"""
	rd_info = pyread(sel_info)
	
	for x in rd_info:
		sel_council= """
			SELECT *, CONCAT(tpi.f_name,' ', tpi.m_name, ' ', tpi.l_name) as fullname from tbl_committee_members tcm 
			LEFT JOIN tbl_personal_info tpi ON tpi.info_id = tcm.committee_members 
			left join tbl_committee tc on tc.committee_id=tcm.committee_id
			where tc.committee_id = '"""+str(x['committee_id'])+"""'
		"""
		rd_sel_council = pyread(sel_council)
		x['members']  = rd_sel_council
	return render_template('/landing_page/committees.html', data=rd_info)


@main.route('/sp_members', methods=['GET', 'POST'])
def sp_members():
	sel_info="""
		select *
		from tbl_sp ts
		left join sp_member sm ON sm.sp_id = ts.sp_id
	"""
	rd_info = pyread(sel_info)
	
	for x in rd_info:
		sel_council= """
			SELECT *, CONCAT(tpi.f_name,' ', tpi.m_name, ' ', tpi.l_name) as fullname 
			from sp_councilor sc 
			LEFT JOIN tbl_personal_info tpi ON tpi.info_id = sc.councilor
			left join sp_assignment sa on sa.sp_councilor=sc.sp_councilor
			where sc.sp_member_id = '"""+str(x['sp_member_id'])+"""' 
		"""
		rd_sel_council = pyread(sel_council)
		x['councilors']  = rd_sel_council

	sel_config = "select * from tbl_config_info"
	rdx = pyread(sel_config)

	return render_template('/landing_page/sp_members.html',data=rd_info, config = rdx)


@main.route('/mission_vision', methods=['GET', 'POST'])
def mission_vision():
	sel_info = "SELECT * from tbl_config_info"
	rd_info = pyread(sel_info)
	return render_template('/landing_page/mission_vision.html', data=rd_info)


@main.route('/secretariat', methods=['GET', 'POST'])
def secretariat():
	sel_info="""
		select *, CONCAT(tpi.f_name," ", tpi.m_name, " ", tpi.l_name) as fullname
		from tbl_sp ts
		left join sp_member sm ON sm.sp_id = ts.sp_id
		left join tbl_personal_info tpi ON tpi.info_id = sm.sp_secretary
	"""
	rd_info = pyread(sel_info)
	return render_template('/landing_page/secretariat.html', data=rd_info)


@main.route('/land_rules_and_procedure', methods=['GET', 'POST'])
def land_rules_and_procedure():
	sel_info="""
		select * from tbl_rules_and_procedure

	"""
	rd_info = pyread(sel_info)
	return render_template('/landing_page/rules_procedure.html', data=rd_info)

@main.route('/land_citizens_charter', methods=['GET', 'POST'])
def land_citizens_charter():
	sel_info="""
		select * from tbl_citezen_charter_path

	"""
	rd_info = pyread(sel_info)
	return render_template('/landing_page/citizens_charter.html', data=rd_info)

@main.route('/vice_mayor_page', methods=['GET', 'POST'])
def vice_mayor_page():
	sel_info="""
		select *, CONCAT(tpi.f_name," ", tpi.m_name, " ", tpi.l_name) as fullname
		from tbl_sp ts
		left join sp_member sm ON sm.sp_id = ts.sp_id
		left join tbl_personal_info tpi ON tpi.info_id = sm.sp_vice_mayor

	"""
	rd_info = pyread(sel_info)
	return render_template('/landing_page/vice_mayor.html', data=rd_info)

@main.route('/gallery', methods=['GET', 'POST'])
def gallery():
	sel_info="""
		select * from tbl_album_gallery
	"""
	rd_album = pyread(sel_info)

	for x in rd_album:
		sel_album_gal = "select * from tbl_album_gallery_photo where gallery_id ='"+ str(x['gallery_id']) +"' "
		rd_album_gallery = pyread(sel_album_gal)
		x['gallery'] = rd_album_gallery
	return render_template('/landing_page/gallery.html', data = rd_album)


@main.route('/get_gallery', methods=['GET', 'POST'])
def get_gallery():
	
	sel_info="""
		select * from tbl_gallery
	"""
	rd_info = pyread(sel_info)

	sel = """
		SELECT
			tci.config_info_id,
			tci.city_name,
			tci.vice_mayors_corner,
			tci.mission,
			tci.vission,
			CONCAT(tpi.f_name,' ', tpi.m_name,' ',tpi.l_name) fullname,
			tci.province,
			(case when (tci.type is null or tci.type='') then 'SANGGUNIANG BAYAN' else 'SANGGUNIANG PANLUNGSOD' end) types
		FROM
			tbl_config_info tci
			join sp_member sm
			join tbl_personal_info tpi ON sm.sp_vice_mayor = tpi.info_id
			join tbl_sp ts ON ts.sp_id = sm.sp_id where ts.`status` = 'ACTIVE'
	"""
	rd_info2 = pyread(sel)
	if rd_info2:
		if rd_info:
			rd_info.append(rd_info2)
	return jsonify(rd_info)

@main.route('/dl_files', methods=['GET', 'POST'])
def dl_files():
	sel_info="""
		select *
		from tbl_download_center_path
	"""
	rd_info = pyread(sel_info)
	return render_template('/landing_page/download_center.html', data = rd_info)

@main.route('/logout')
def logout():
  session.clear()
  print("session clear")
  return render_template('auth/sign-in.html')

@main.route('/login')
def logins():
	for i in imp_folders:
		n_path = Path(__file__).parent / "../static/uploads/" / str(i)
		n_path.resolve()
		if not os.path.exists(n_path):
			print("not exist")
			os.mkdir(n_path)
			print("folder "+ i +" created")
		else:
			pass
	return render_template('auth/sign-in.html')

@main.route('/sangunian', methods=['GET', 'POST'])
@authorize
def sangunian():
	session_data=session['data']
	return render_template('config/Sanguniang panglungsod.html', data=session_data)


@main.route('/assign', methods=['GET', 'POST'])
@authorize
def assign():
	session_data=session['data']
	return render_template('config/assign.html', data=session_data)

@main.route('/comitee', methods=['GET', 'POST'])
@authorize
def comitee():
	session_data=session['data']
	return render_template('config/comitee.html', data=session_data)
	

@main.route('/accounts', methods=['GET', 'POST'])
@authorize
def accounts():
	session_data=session['data']
	return render_template('config/accounts.html', data=session_data)
	

@main.route('/announcement', methods=['GET', 'POST'])
@authorize
def announcement():
	session_data=session['data']
	return render_template('config/announcement.html', data=session_data)
	

@main.route('/sp_budget', methods=['GET', 'POST'])
@authorize
def sp_budget():
	session_data=session['data']
	return render_template('budget/sp_budget.html', data=session_data)
	

@main.route('/capital_oultay', methods=['GET', 'POST'])
@authorize
def capital_oultay():
	session_data=session['data']
	return render_template('budget/capital_oultay.html', data=session_data)
	

@main.route('/sp_member_deduction', methods=['GET', 'POST'])
@authorize
def sp_member_deduction():
	session_data=session['data']
	return render_template('budget/sp_member_deduction.html', data=session_data)
	

@main.route('/appropriation_ordinance', methods=['GET', 'POST'])
@authorize
def appropriation_ordinance():
	session_data=session['data']
	return render_template('ordinance/appropriation.html', data=session_data)
	
@main.route('/proposed_ordinance', methods=['GET', 'POST'])
@authorize
def proposed_ordinance():
	session_data=session['data']
	return render_template('ordinance/proposed_ordinance.html', data=session_data)
	

@main.route('/2nd_ordinance', methods=['GET', 'POST'])
@authorize
def ordinance2():
	session_data=session['data']
	return render_template('ordinance/2nd_reading.html', data=session_data)
	

@main.route('/3rd_ordinance', methods=['GET', 'POST'])
@authorize
def ordinance3():
	session_data=session['data']
	return render_template('ordinance/3rd_reading.html', data=session_data)
	

@main.route('/3rd_ordinance_exemption', methods=['GET', 'POST'])
@authorize
def ordinance_exemption():
	session_data=session['data']
	return render_template('ordinance/3rd_reading_exemption.html', data=session_data)
	

@main.route('/for_approval_ordinance', methods=['GET', 'POST'])
@authorize
def for_approval_ordinance():
	session_data=session['data']
	return render_template('ordinance/for_approval_ordinance.html', data=session_data)

@main.route('/approval_ordinance', methods=['GET', 'POST'])
@authorize
def approval_ordinance():
	session_data=session['data']
	return render_template('ordinance/approved_ordinance.html', data=session_data)

@main.route('/veto_ordinance', methods=['GET', 'POST'])
@authorize
def Veto_ordinance():
	session_data=session['data']
	return render_template('ordinance/veto_ordinance.html', data=session_data)
	

@main.route('/archive_ordinance', methods=['GET', 'POST'])
@authorize
def archive_ordinance():
	session_data=session['data']
	return render_template('ordinance/archive_ordinance.html', data=session_data)
	

@main.route('/view_ordinance', methods=['GET', 'POST'])
@authorize
def view_ordinance():
	session_data=session['data']
	return render_template('ordinance/view_ordinance.html', data=session_data)
	

@main.route('/governance_classification', methods=['GET', 'POST'])
@authorize
def governance_classification():
	session_data=session['data']
	return render_template('config/governance_classification.html', data=session_data)
	

@main.route('/category', methods=['GET', 'POST'])
@authorize
def category():
	session_data=session['data']
	return render_template('config/category.html', data=session_data)





@main.route('/order_of_business', methods=['GET', 'POST'])
@authorize
def order_of_business():
	session_data=session['data']
	return render_template('sessions/order_of_business.html', data=session_data)

@main.route('/petition', methods=['GET', 'POST'])
@authorize
def petition():
	session_data=session['data']
	return render_template('petition/petition.html', data=session_data)

@main.route('/minutes', methods=['GET', 'POST'])
@authorize
def minutes():
	session_data=session['data']
	return render_template('minutes/minutes.html', data=session_data)
	

@main.route('/resolution', methods=['GET', 'POST'])
@authorize
def resolution():
	session_data=session['data']
	return render_template('resolution/resolution.html', data=session_data)
	

@main.route('/proposed_resolution', methods=['GET', 'POST'])
@authorize
def proposed_resolution():
	session_data=session['data']
	return render_template('resolution/proposed_resolution.html', data=session_data)
	

@main.route('/2nd_resolution', methods=['GET', 'POST'])
@authorize
def resolution_2nd():
	session_data=session['data']
	return render_template('resolution/2nd_reading_resolution.html', data=session_data)

@main.route('/3rd_resolution', methods=['GET', 'POST'])
@authorize
def resolution_3rd():
	session_data=session['data']
	return render_template('resolution/3rd_reading_resolution.html', data=session_data)
	

@main.route('/3rd_resolution_exemption', methods=['GET', 'POST'])
@authorize
def resolution_3rd_exemp():
	session_data=session['data']
	return render_template('resolution/3rd_reading_excemp.html', data=session_data)
	

@main.route('/for_approval_resolution', methods=['GET', 'POST'])
@authorize
def for_approval_resolution():
	session_data=session['data']
	return render_template('resolution/for_approval_resolution.html', data=session_data)
	

@main.route('/approved_resolution', methods=['GET', 'POST'])
@authorize
def approved_resolution():
	session_data=session['data']
	return render_template('resolution/approved_resolution.html', data=session_data)
	

@main.route('/veto_resolution', methods=['GET', 'POST'])
@authorize
def veto_resolution():
	session_data=session['data']
	return render_template('resolution/veto_resolution.html', data=session_data)
	

@main.route('/archive_resolution', methods=['GET', 'POST'])
@authorize
def archive_resolution():
	session_data=session['data']
	return render_template('resolution/archived_resolution.html', data=session_data)
	

@main.route('/documents_refferals', methods=['GET', 'POST'])
@authorize
def documents_refferals():
	session_data=session['data']
	return render_template('documents_refferals/documents_refferals.html', data=session_data)
	

@main.route('/user', methods=['GET', 'POST'])
@authorize
def user():
	session_data=session['data']
	return render_template('user/user.html', data=session_data)

@main.route('/executive_order', methods=['GET', 'POST'])
@authorize
def executive_order():
	session_data=session['data']
	return render_template('executive_order/executive_order.html', data=session_data)

@main.route('/memorandom', methods=['GET', 'POST'])
@authorize
def memorandom():
	session_data=session['data']
	return render_template('memorandom/memorandom.html', data=session_data)

@main.route('/view_committee_reports', methods=['GET', 'POST'])
@authorize
def view_committee_reports():
	session_data=session['data']
	return render_template('committee_reports/view_committee_reports.html', data=session_data)
	

@main.route('/view_committee_minutes', methods=['GET', 'POST'])
@authorize
def view_committee_minutes():
	session_data=session['data']
	return render_template('committee_reports/view_committee_minutes.html', data=session_data)


@main.route('/gmail_account', methods=['GET', 'POST'])
@authorize
def gmail_account():
	session_data=session['data']
	return render_template('user/gmail_account.html', data=session_data)

@main.route('/info', methods=['GET', 'POST'])
@authorize
def info():
	session_data=session['data']
	return render_template('config/info.html', data=session_data)

@main.route('/reports', methods=['GET', 'POST'])
@authorize
def reports():
	session_data=session['data']
	return render_template('reports/reports.html', data=session_data)


@main.route('/commiittee_reports_information', methods=['GET', 'POST'])
@authorize
def commiittee_reports_information():
	session_data=session['data']
	return render_template('reports/commiittee_reports_information.html', data=session_data)


@main.route('/barangay', methods=['GET', 'POST'])
@authorize
def barangay():
	session_data=session['data']
	return render_template('config/barangay.html', data=session_data)


@main.route('/barangay_ordinance', methods=['GET', 'POST'])
@authorize
def barangay_ordinance():
	session_data=session['data']
	return render_template('barangay/barangay_ordinance.html', data=session_data)


@main.route('/barangay_resolution', methods=['GET', 'POST'])
@authorize
def barangay_resolution():
	session_data=session['data']
	return render_template('barangay/barangay_resolution.html', data=session_data)


@main.route('/background', methods=['GET', 'POST'])
@authorize
def background():
	session_data=session['data']
	return render_template('config/updload_background.html', data=session_data)



@main.route('/gallery_albums', methods=['GET', 'POST'])
@authorize
def gallery_albums():
	session_data=session['data']
	return render_template('gallery_albums/gallery_albums.html', data=session_data)


@main.route('/albums', methods=['GET', 'POST'])
@authorize
def albums():
	session_data=session['data']
	return render_template('gallery_albums/albums.html', data=session_data)
		

@main.route('/rules_and_procedure', methods=['GET', 'POST'])
@authorize
def rules_and_procedure():
	session_data=session['data']
	return render_template('rules_and_procedure/rules_and_procedure.html', data=session_data)


@main.route('/citezen_charter', methods=['GET', 'POST'])
@authorize
def citezen_charter():
	session_data=session['data']
	return render_template('citezen_charter/citezen_charter.html', data=session_data)


@main.route('/profiling_ordinance', methods=['GET', 'POST'])
@authorize
def profiling_ordinance():
	session_data=session['data']
	return render_template('profiling_ordinance/profiling_ordinance.html', data=session_data)


@main.route('/download_center', methods=['GET', 'POST'])
@authorize
def download_center():
	session_data=session['data']
	return render_template('download_center/download_center.html', data=session_data)

@main.route('/view_committee_info', methods=['GET', 'POST'])
@authorize
def view_committee_info():
	session_data=session['data']
	return render_template('committee_reports/committee_information.html', data=session_data)

@main.route('/codification_reports', methods=['GET', 'POST'])
@authorize
def codification_reports():
	session_data=session['data']
	return render_template('codification_reports/codification_reports.html', data=session_data)

@main.route('/meetings', methods=['GET', 'POST'])
@authorize
def meetings():
	session_data=session['data']
	return render_template('meetings/meetings.html', data=session_data)

@main.route('/login', methods=['GET','POST'])
def login():
	p=json.loads(request.data)
	sel="""
			select tl.login_id, fullname, tla.routes, tl.role from tbl_login tl
			left join tbl_login_access tla on tla.login_id=tl.login_id
			where tl.username='"""+str(p['username'])+"""' and tl.password='"""+str(p['password'])+"""'
		"""
	rd=pyread(sel)
	if rd:
		if rd!="":
			session['index']=True
			session['sessioned_user']=str(rd[0]['login_id'])
			session['sessioned_role']=rd[0]['role']
			session['data']=rd[0]
			thislist = []
			for x in range(len(rd)):
				thislist.append(rd[x]['routes'])
			session['obj'] = thislist
			return jsonify({"result":"pass","rd":rd})
		else:
			return jsonify("Invalid")
	else:
		return jsonify("Invalid")