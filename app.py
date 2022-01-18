from flask import Flask, render_template, flash, session, request, redirect, make_response
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import yaml
import os
from datetime import datetime, timedelta
import pytz
import string
import random
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import pdfkit

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

UPLOAD_FOLDER_CARDID = 'static/images/card_id/'
UPLOAD_FOLDER_CANDIDATE = 'static/images/candidate/'
UPLOAD_FOLDER_VOTER = 'static/images/voter/'
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER_CARDID'] = UPLOAD_FOLDER_CARDID
app.config['UPLOAD_FOLDER_CANDIDATE'] = UPLOAD_FOLDER_CANDIDATE
app.config['UPLOAD_FOLDER_VOTER'] = UPLOAD_FOLDER_VOTER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# os.environ['TZ'] = 'Asia/Makassar'
# datetime.tzset()
IST = pytz.timezone('Asia/Makassar')
# 2022-01-17 06:03:11.817757+08:00

# path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
# config_pdfkit = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# ROUTE ========================================================================

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login/', methods = ['GET', 'POST'])
def appLogin():
    try:
        if session['login'] == True and (session['role'] == 'admin' or session['role'] == 'organizer'):
            flash('Anda telah Login', 'secondary')
            return redirect('/' + session['role'] + '/dashboard/')
        else:
            return login()
    except:
        return login()

@app.route('/logout/')
def appLogout():
    logout()
    flash('Anda berhasil Logout', 'secondary')
    return redirect('/')

@app.route('/registration/', methods = ['GET', 'POST'])
def appRegistration():
    try:
        if session['login'] == True and (session['role'] == 'admin' or session['role'] == 'organizer'):
            flash('Anda telah Login', 'secondary')
            return redirect('/' + session['role'] + '/dashboard/')
        else:
            return registration()
    except:
        return registration()

@app.route('/admin/dashboard/')
def appAdminDashboard():
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_dashboard()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/organizer/', methods = ['GET', 'POST'])
def appAdminOrganizer():
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_organizer()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/voting/delete/<string:id_user>/<string:id_voting>/')
def appAdminVotingDelete(id_user, id_voting):
    try:
        if session['login'] == True and session['role'] == 'admin':
            get_delete('voting', id_voting)
            flash('Data Voting berhasil dihapus', 'secondary')
            return redirect('/admin/organizer/{}'.format(id_user))
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/<string:data>/<string:action>/<string:id>/')
def appAdminOrganizerAction(data, action, id):
    try:
        if session['login'] == True and session['role'] == 'admin':
            if data == 'organizer':
                if action == 'approve' or action == 'active' or action == 'inactive':
                    verify_organizer(action, id)
                elif action == 'delete':
                    get_delete(data, id)
                    flash('Data Organizer berhasil dihapus', 'secondary')

            if data == 'voting':
                if action == 'delete':
                    get_delete(data, id)
                    flash('Data Voting berhasil dihapus', 'secondary')
                elif action == 'report':
                    return get_report(id)

            if data == 'problem':
                if action == 'delete':
                    get_delete(data, id)
                    flash('Data Pertanyaan dan Keluhan berhasil dihapus', 'warning')
            return redirect('/admin/{}/'.format(data))
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/organizer/<string:id>/')
def appAdminOrganizerDetail(id):
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_organizer_detail(id)
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/voting/')
def appAdminVoting():
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_voting()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/voting/<string:id>/')
def appAdminVotingDetail(id):
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_voting_detail(id)
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/voting/<string:id_voting>/<string:data>/delete/<string:id>/')
def appAdminVotingAction(id_voting, data, id):
    try:
        if session['login'] == True and session['role'] == 'admin':
            if data == 'candidate':
                table = 'c_' + id_voting
            if data == 'voter':
                table = 'v_' + id_voting
            get_delete_cv(table, data, id)
            flash('Data {} berhasil dihapus'.format(data.capitalize()), 'secondary')
            return redirect('/admin/voting/{}/'.format(id_voting))
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/validate/voting/<string:id_voting>/')
def appValidateVoting(id_voting):
    try:
        if session['login'] == True and (session['role'] == 'admin' or session['role'] == 'organizer'):
            validate_voting(id_voting)
            flash('Data Hasil Voting berhasil divalidasi', 'secondary')
            return redirect('/' + session['role'] + '/voting/report/' + id_voting +'/')
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/report/voting/<string:id_voting>/')
def appReportVoting(id_voting):
    try:
        if session['login'] == True and (session['role'] == 'admin' or session['role'] == 'organizer'):
            status = check_idle(id_voting)
            if status:
                validate_voting(id_voting)
                return report_voting(id_voting)
            else:
                flash('Kegiatan Voting belum selesai dilaksanakan', 'warning')
                return redirect('/' + session['role'] + '/voting/report/' + id_voting + '/')
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/admin/problem/', methods = ['GET', 'POST'])
def appAdminProblem():
    try:
        if session['login'] == True and session['role'] == 'admin':
            return admin_problem()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route("/getdata/<string:data>/<string:id>/")
def appGetData(data, id):
    try:
        if session['login'] == True and (session['role'] == 'admin' or session['role'] == 'organizer'):
            if data == 'voting':
                voting = get_voting(id)
                return voting
            elif data == 'problem':
                if session['role'] == 'admin':
                    problem = get_problem_admin(id)
                elif session['role'] == 'organizer':
                    problem = get_problem_cv(id)
                return problem
        elif session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
            if data == 'candidate':
                table = 'c_' + session['id_voting']
                candidate = get_cv(table, data, id)
                return candidate
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route("/getdata/problem/<string:id_voting>/<string:id_problem>/")
def appGetDataProblem(id_voting, id_problem):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            problem = get_problem_organizer(id_voting, id_problem)
            return problem
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/dashboard/', methods = ['GET', 'POST'])
def appOrganizerDashboard():
    try:
        if session['login'] == True and session['role'] == 'organizer':
            return organizer_dashboard()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/voting/')
def appOrganizerVoting():
    try:
        if session['login'] == True and session['role'] == 'organizer':
            return organizer_voting()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')


@app.route('/organizer/voting/<string:id>/', methods = ['GET', 'POST'])
def appOrganizerVotingDetail(id):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            return organizer_voting_detail(id)
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/voting/<string:action>/<string:id>/')
def appOrganizerAction(action, id):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            if action == 'delete':
                get_delete('voting', id)
                flash('Data Voting berhasil dihapus', 'secondary')
                return redirect('/organizer/voting/')
            elif action == 'report':
                return get_report(id)
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route("/getdata/<string:data>/<string:id_voting>/<string:id>")
def appGetDataCV(data, id_voting, id):
    try:
        if session['login'] == True and (session['role'] == 'organizer'):
            if data == 'candidate':
                table = 'c_' + id_voting
            elif data == 'voter':
                table = 'v_' + id_voting

            dataEdit = get_cv(table, data, id)
            return dataEdit

        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/voting/<string:id_voting>/<string:data>/<string:action>/<string:id>/')
def appOrganizerVotingAction(id_voting, data, action, id):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            if data == 'candidate':
                table = 'c_' + id_voting
            if data == 'voter':
                table = 'v_' + id_voting

            if action == 'delete':
                get_delete_cv(table, data, id)
                flash('Data {} berhasil dihapus'.format(data.capitalize()), 'secondary')
            elif action == 'block':
                set_status_cv(table, data, action, id)
                flash('Hak pilih dinonaktifkan', 'warning')
            elif action == 'allow':
                set_status_cv(table, data, action, id)
                flash('Hak pilih diaktifkan', 'secondary')
            return redirect('/organizer/voting/{}/'.format(id_voting))
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/problem/', methods = ['GET', 'POST'])
def appOrganizerProblem():
    try:
        if session['login'] == True and session['role'] == 'organizer':
            return organizer_problem()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/voting/<string:id_voting>/problem/delete/<string:id_problem>/')
def appOrganizerVotingProblemDelete(id_voting, id_problem):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            get_delete('problem', id_problem)
            flash('Data Pertanyaan dan Keluhan berhasil dihapus', 'secondary')
            return redirect('/organizer/voting/{}/'.format(id_voting))
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route('/organizer/problem/delete/<string:id_problem>/')
def appOrganizerProblemDelete(id_problem):
    try:
        if session['login'] == True and session['role'] == 'organizer':
            get_delete('problem', id_problem)
            flash('Data Pertanyaan dan Keluhan berhasil dihapus', 'secondary')
            return redirect('/organizer/problem/')
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/login/')

@app.route("/voting-page/", methods = ['GET', 'POST'])
def appVotingPage():
    try:
        if session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
            return voting_page()
        else:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/voting-page/login/')
    except:
        flash('Login terlebih dahulu', 'warning')
        return redirect('/voting-page/login/')

@app.route("/voting-page/login/", methods = ['GET', 'POST'])
def appVotingPageLanding():
    try:
        if session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
            flash('Anda telah Login', 'secondary')
            return redirect('/voting-page/')
        else:
            flash('Masukkan ID Voting terlebih dahulu', 'warning')
            return voting_landing()
    except:
        return voting_landing()

@app.route("/voting-page/login/<string:id>/", methods = ['GET', 'POST'])
def appVotingPageLogin(id):
    try:
        if session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
            flash('Anda telah Login', 'secondary')
            return redirect('/voting-page/')
        else:
            flash('Login terlebih dahulu', 'warning')
            return voting_login(id)
    except:
        return voting_login(id)

@app.route("/voting-page/login/<string:id_voting>/<string:username>/<string:password>/", methods = ['GET', 'POST'])
def appVotingPageLoginCredential(id_voting, username, password):
    try:
        if session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
            flash('Anda telah Login', 'secondary')
            return redirect('/voting-page/')
        else:
            flash('Login terlebih dahulu', 'warning')
            return voting_login(id)
    except:
        return voting_login_credential(id_voting, username, password)

# @app.route("/voting-page/keluhan/", methods = ['GET', 'POST'])
# def appVotingPageKeluhan():
#     try:
#         if session['login'] == True and (session['role'] == 'candidate' or session['role'] == 'voter'):
#             return voting_keluhan()
#         else:
#             return redirect('/voting-page/login/')
#     except:
#         return redirect('/voting-page/login/')

@app.route("/live-count/<string:id>/")
def appLiveCount(id):
    viewer = get_viewer(id)
    if viewer == 'on':
        return live_count(id)
    elif viewer == 'off':
        try:
            if session['login'] == True:
                return live_count(id)
            else:
                flash('Login terlebih dahulu', 'warning')
                return redirect('/voting-page/login/{}/'.format(id))
        except:
            flash('Login terlebih dahulu', 'warning')
            return redirect('/voting-page/login/{}/'.format(id))

@app.route('/voting-page/logout/')
def appVotingPageLogout():
    logout()
    flash('Anda berhasil Logout', 'secondary')
    return redirect('/voting-page/login/')

# MAIN FUNCTION ================================================================

def login():
    core = {'title':'Login Organizer'}
    if request.method == 'POST':
        user = request.form
        email = user['email']
        password = user['password']

        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT id_user, name, pass, role FROM user WHERE email = %s", [email])
        if resultValue > 0:
            loginData = cur.fetchone()
            cur.close()
            if check_password_hash(loginData['pass'], password):
                session['login'] = True
                session['id_user'] = loginData['id_user']
                session['role'] = loginData['role']
                session['name'] = loginData['name']
                flash('Selamat datang ' + session['name'] + '! Anda berhasil Login', 'secondary')
            else:
                flash('Email/kata sandi salah!', 'warning')
                return render_template('login.html', core = core)
        else:
            flash('Akun tidak ditemukan!', 'warning')
            return render_template('login.html', core = core)
        return redirect('/' + session['role'] + '/dashboard/')
    return render_template('login.html', core = core)

def logout():
    session.clear()
    return True

def registration():
    core = {'title':'Registrasi Akun'}
    if request.method == 'POST':
        user = request.form
        if user['password'] != user['confirm_password']:
            flash('Kata sandi tidak sama! Silahkan ulangi kembali', 'warning')
            return render_template('registration.html', core = core)

        id_user = generate_id()
        name = user['name']
        email = user['email']
        number = user['number']
        passhash = generate_password_hash(user['password'])
        address = user['address']
        institution = user['institution']
        created_at = str(datetime.now())

        if 'card_id' not in request.files:
            flash('Tidak dapat memuat Foto Kartu ID', 'warning')
            return redirect(request.url)
        image = request.files['card_id']
        if image.filename == '':
            flash('Tidak ada foto yang dipilih', 'warning')
            return redirect(request.url)
        if image and allowed_image(image.filename):
            filename = secure_filename(str(id_user) + '_' + created_at)
            image.save(os.path.join(app.config['UPLOAD_FOLDER_CARDID'], filename))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user(id_user, name, email, number, pass, address, institution, card_id, created_at) "\
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_user, name, email, number, passhash, address, institution, filename, created_at))
            mysql.connection.commit()
            cur.close()
            flash('Akun Organizer berhasil dibuat! Silahkan Login untuk melanjutkan', 'secondary')
            return redirect('/login/')
        else:
            flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
            return redirect(request.url)
    return render_template('registration.html', core = core)

def admin_dashboard():
    core = {'title':'Panel Admin', 'subtitle':'Dashboard', 'aside':True, 'page':['Dashboard']}
    organizer = {}
    organizer['total'] = count_organizer_total()
    organizer['new'] = count_organizer_new()
    voting = {}
    voting['total'] = count_voting_total()
    voting['disactive'] = count_voting_disactive()
    voting['active'] = count_voting_active()
    voting['finish'] = count_voting_finish()
    votingDetails = get_voting_dashboard()
    now = datetime.now() + timedelta(hours = 8)
    return render_template('adminDashboard.html', core = core, organizer = organizer, voting = voting, votingDetails = votingDetails, now = now)

def admin_organizer():
    core = {'title':'Panel Admin', 'subtitle':'Kelola Organizer', 'aside':True, 'page':['Kelola Organizer']}
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'reject-message':
            id_user = data['id_user']
            message = data['message']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE user SET message = %s WHERE id_user = %s", (message, id_user))
            mysql.connection.commit()
            cur.close()
            verify_organizer('reject', id_user)
        return redirect(request.url)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_user, name, email, number, institution, address, card_id, status, message FROM user WHERE role = 'organizer' ORDER BY created_at DESC")
    if resultValue > 0:
        organizers = cur.fetchall()
        cur.close()
        return render_template('adminOrganizer.html', core = core, organizers = organizers)
    return render_template('adminOrganizer.html', core = core, organizers = None)

def admin_organizer_detail(id):
    core = {'title':'Panel Admin', 'subtitle':'Data Profil Organizer', 'aside':True, 'page':['Kelola Organizer', 'Detail Organizer']}
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_user, name, email, number, institution, address, card_id, status, message FROM user WHERE id_user = %s", [id])
    if resultValue > 0:
        userDetail = cur.fetchone()
    resultValue = cur.execute("SELECT id_voting, name, voting_desc, date_start, date_end FROM voting WHERE id_user = %s ORDER BY created_at DESC", [id])
    if resultValue > 0:
        userVotings = cur.fetchall()
    else:
        userVotings = None
    cur.close()
    now = datetime.now()
    voting = count_voting_detail(id)
    return render_template('adminOrganizerDetail.html', core = core, userDetail = userDetail, userVotings = userVotings, voting = voting, now = now)

def admin_voting():
    core = {'title':'Panel Admin', 'subtitle':'Kelola Voting', 'aside':True, 'page':['Kelola Voting']}
    now = datetime.now()
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, id_user, name, voting_desc, date_start, date_end FROM voting ORDER BY created_at DESC")
    if resultValue > 0:
        votings = cur.fetchall()
        for voting in votings:
            resultValue = cur.execute("SELECT name FROM user WHERE id_user = %s", [voting['id_user']])
            voting['organizer'] = cur.fetchone()['name']
        cur.close()
        return render_template('adminVoting.html', core = core, userVotings = votings, now = now)
    return render_template('adminVoting.html', core = core, userVotings = None, now = now)

def admin_voting_detail(id):
    core = {'title':'Panel Admin', 'subtitle':'Data Candidate & Voter', 'aside':True, 'page':['Kelola Voting', 'Detail Voting']}
    now = datetime.now()
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, id_user, name, voting_desc, date_start, date_end, candidate, voter, viewer, last_checked FROM voting WHERE id_voting = %s", [id])
    if resultValue > 0:
        votingDetail = cur.fetchone()
        cname = True if 'cname' in votingDetail['candidate'] else False
        cdesc = True if 'cdesc' in votingDetail['candidate'] else False
        cavatar = True if 'cavatar' in votingDetail['candidate'] else False
        vname = True if 'vname' in votingDetail['voter'] else False
        vdesc = True if 'vdesc' in votingDetail['voter'] else False
        vavatar = True if 'vavatar' in votingDetail['voter'] else False
        data = {'cdesc':cdesc, 'cavatar':cavatar, 'vdesc':vdesc, 'vavatar':vavatar}
    resultValue = cur.execute("SELECT name FROM user WHERE id_user = %s", [votingDetail['id_user']])
    votingDetail['organizer'] = cur.fetchone()['name']
    resultValue = cur.execute("SELECT id_candidate, id_voting, name, {}{} status FROM {} ORDER BY created_at DESC".format('description,' if cdesc == True else '', 'avatar,' if cavatar == True else '', 'c_' + id))
    if resultValue > 0:
        votingCandidates = cur.fetchall()
    else:
        votingCandidates = None
    resultValue = cur.execute("SELECT id_voter, id_voting, name, {}{} status FROM {} ORDER BY created_at DESC".format('description,' if vdesc == True else '', 'avatar,' if vavatar == True else '', 'v_' + id))
    if resultValue > 0:
        votingVoters = cur.fetchall()
    else:
        votingVoters = None
    cur.close()
    total = count_cv(id)
    return render_template('adminVotingDetail.html', core = core, now = now, data = data, total = total, votingDetail = votingDetail, votingCandidates = votingCandidates, votingVoters = votingVoters)

def get_report(id):
    core = {'title':'Panel ' + 'Admin' if session['role'] == 'admin' else 'Organizer', 'subtitle':'Data Hasil Voting', 'aside':True, 'page':['Kelola Voting', 'Hasil Voting']}
    now = datetime.now()
    votingDetail = get_voting(id)
    votingCounts = get_count(id)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_hash, id_candidate, encrypted, created_at, status FROM h_{}".format(id))
    if resultValue > 0:
        votingReports = cur.fetchall()
    else:
        votingReports = None
    cur.close()
    return render_template("votingReport.html", core = core, now = now, votingDetail = votingDetail, votingCounts = votingCounts, votingReports = votingReports)

def report_voting(id_voting):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, id_user, name, voting_desc, date_start, date_end FROM voting WHERE id_voting = '{}'".format(id_voting))
    if resultValue > 0:
        votingDetail = cur.fetchone()
    else:
        votingDetail = None
    resultValue = cur.execute("SELECT name, email, number, address FROM user WHERE id_user = '{}'".format(votingDetail['id_user']))
    if resultValue > 0:
        userDetail = cur.fetchone()
    else:
        userDetail = None
    rresultValue = cur.execute("SELECT id_hash, id_candidate, created_at, status FROM h_{}".format(id_voting))
    if resultValue > 0:
        reportLogs = cur.fetchall()
    else:
        reportLogs = None
    cur.close
    reportDetails = get_report_finish(id_voting)
    rendered = render_template('reportPdf.html', votingDetail = votingDetail, userDetail = userDetail, reportDetails = reportDetails, reportLogs = reportLogs)
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.75in',
        'margin-bottom': '0.5in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
        'footer-right':'[page] dari [topage] halaman',
        'footer-left':datetime.now().strftime('%d/%m/%Y %I:%M %p'),
        'footer-font-size':10,
        'no-outline':None
    }
    css = ['static/styles/css/bootstrap.min.css', 'static/styles/css/soft-ui-dashboard.min.css']
    pdf = pdfkit.from_string(rendered, False, options = options, css = css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; laporan.pdf'

    return response

def admin_problem():
    core = {'title':'Panel Admin', 'subtitle':'Pertanyaan dan Keluhan', 'aside':True, 'page':['Pertanyaan dan Keluhan']}
    now = datetime.now()
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'respond':
            problem = data
            id_problem = problem['id_problem']
            respond = problem['respond']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE problem SET respond = %s WHERE id_problem = %s",(respond, id_problem))
            mysql.connection.commit()
            cur.close()
            flash('Tanggapan berhasil dikirim', 'secondary')
            return redirect(request.url)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT p.*, u.name AS organizer, v.name AS voting FROM problem p INNER JOIN user u ON p.id_user = u.id_user INNER JOIN voting v ON p.id_voting = v.id_voting WHERE msg_to = 'Admin' ORDER BY p.msg_created DESC")
    if resultValue > 0:
        organizerProblems = cur.fetchall()
    else:
        organizerProblems = None

    return render_template('adminProblem.html', core = core, organizerProblems = organizerProblems)

def organizer_dashboard():
    core = {'title':'Panel Organizer', 'subtitle':'Dashboard', 'aside':True, 'page':['Dashboard']}
    now = datetime.now()
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'create-voting':
            id_voting = generate_id()
            id_user = session['id_user']
            name = data['name']
            voting_desc = data['voting_desc']
            date_start, date_end = (data['datetimes']).split(' - ')
            date_start = convert_datetime('mtl', date_start)
            date_end = convert_datetime('mtl', date_end)
            candidate = str(data.getlist('candidate'))
            voter = str(data.getlist('voter'))
            viewer = data['viewer_access'] if 'viewer_access' in data else 'off'
            created_at = str(datetime.now())
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO voting(id_voting, id_user, name, voting_desc, date_start, date_end, candidate, voter, viewer, created_at) "\
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_voting, id_user, name, voting_desc, date_start, date_end, candidate, voter, viewer, created_at))
            mysql.connection.commit()

            table_candidate = 'c_' + id_voting
            table_voter = 'v_' + id_voting
            table_hash = 'h_' + id_voting

            cur.execute("CREATE TABLE {} (id_candidate VARCHAR(40) NOT NULL, id_voting VARCHAR(40) NOT NULL, username VARCHAR(40) NOT NULL, pass VARCHAR(40) NOT NULL, name VARCHAR(255) NOT NULL, description LONGTEXT, avatar VARCHAR(40), status VARCHAR(40), validator VARCHAR(255), created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "\
            "PRIMARY KEY (id_candidate), FOREIGN KEY (id_voting) REFERENCES voting(id_voting))".format(table_candidate))
            mysql.connection.commit()

            cur.execute("CREATE TABLE {} (id_voter VARCHAR(40) NOT NULL, id_voting VARCHAR(40) NOT NULL, username VARCHAR(40) NOT NULL, pass VARCHAR(40) NOT NULL, name VARCHAR(40) NOT NULL, description LONGTEXT, avatar VARCHAR(40), status VARCHAR(40), validator VARCHAR(255), created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "\
            "PRIMARY KEY (id_voter), FOREIGN KEY (id_voting) REFERENCES voting(id_voting))".format(table_voter))
            mysql.connection.commit()

            cur.execute("CREATE TABLE {} (id_hash VARCHAR(40) NOT NULL, id_voting VARCHAR(40) NOT NULL, id_candidate VARCHAR(40) NOT NULL, role VARCHAR(40) NOT NULL, encrypted VARCHAR(255) NOT NULL, status VARCHAR(40) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "\
            "PRIMARY KEY (id_hash), FOREIGN KEY (id_voting) REFERENCES voting(id_voting), FOREIGN KEY (id_candidate) REFERENCES {}(id_candidate))".format(table_hash, table_candidate))
            mysql.connection.commit()
            cur.close()

            flash('Voting berhasil dibuat!', 'secondary')
            return redirect(request.url)
        elif data['submit'] == 'change-cardid':
            if 'card_id' not in request.files:
                flash('Tidak dapat memuat Foto Kartu ID')
                return redirect(request.url)
            image = request.files['card_id']
            if image.filename == '':
                flash('Tidak ada foto yang dipilih')
                return redirect(request.url)
            if image and allowed_image(image.filename):
                filename = get_cardid(session['id_user'])
                image.save(os.path.join(app.config['UPLOAD_FOLDER_CARDID'], filename))
                cur = mysql.connection.cursor()
                cur.execute("UPDATE user SET status = 'pending' WHERE id_user = %s", [session['id_user']])
                mysql.connection.commit()
                cur.close()
                flash('Kartu ID berhasil diperbaharui', 'secondary')
                return redirect(request.url)
            else:
                flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
                return redirect(request.url)
        elif data['submit'] == 'change-pass':
            current_pass = data['current_pass']
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT pass FROM user WHERE id_user = %s", [session['id_user']])
            if resultValue > 0:
                old_pass = cur.fetchone()['pass']
                cur.close()
                if check_password_hash(old_pass, current_pass):
                    new_pass = data['new_pass']
                    confirm_new_pass = data['confirm_new_pass']
                    if new_pass != confirm_new_pass:
                        flash('Kata sandi baru tidak sama! Silahkan ulangi kembali', 'warning')
                        return redirect(request.url)
                    passhash = generate_password_hash(new_pass)
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE user SET pass = %s WHERE id_user = %s", (passhash, session['id_user']))
                    mysql.connection.commit()
                    cur.close()
                else:
                    flash('Kata sandi saat ini salah! Silahkan ulangi kembali', 'warning')
                    return redirect(request.url)
            flash('Kata sandi berhasil diperbaharui', 'secondary')
            return redirect(request.url)
        elif data['submit'] == 'change-profile':
            name = data['name']
            email = data['email']
            number = data['number']
            address = data['address']
            institution = data['institution']
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT name, email, number, institution, address FROM user WHERE id_user = %s", [session['id_user']])
            if resultValue > 0:
                user = cur.fetchone()
            if name == user['name'] and email == user['email'] and number == user['number'] and address == user['address'] and institution == user['institution']:
                cur.close()
                flash('Tidak ada perubahan data', 'warning')
                return redirect(request.url)
            else:
                cur.execute("UPDATE user SET name = %s, email = %s, number = %s, address = %s, institution = %s, status = 'pending', message = '[Perubahan Profil]' WHERE id_user = %s", (name, email, number, address, institution, session['id_user']))
                mysql.connection.commit()
                cur.close()
                flash('Profil Akun berhasil diperbaharui', 'secondary')
                return redirect(request.url)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT name, email, number, pass, institution, address, status, message, card_id FROM user WHERE id_user = %s", [session['id_user']])
    if resultValue > 0:
        userData = cur.fetchone()
    resultValue = cur.execute("SELECT v.id_voting, v.name, v.voting_desc, v.date_start, v.date_end FROM voting v INNER JOIN user u ON v.id_user = u.id_user WHERE u.id_user = %s AND NOT u.status = 'inactived' ORDER BY v.created_at DESC", [session['id_user']])
    if resultValue > 0:
        userVotings = cur.fetchall()
    else:
        userVotings = None
    cur.close()
    voting = count_voting_detail(session['id_user'])
    return render_template('organizerDashboard.html', core = core, now = now, userData = userData, votingDetails = userVotings, voting = voting)

def organizer_voting():
    core = {'title':'Panel Organizer', 'subtitle':'Kelola Voting', 'aside':True, 'page':['Kelola Voting']}
    now = datetime.now()
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT v.id_voting, v.name, v.voting_desc, v.date_start, v.date_end FROM voting v INNER JOIN user u ON v.id_user = u.id_user WHERE u.id_user = '{}' AND NOT u.status = 'inactived' ORDER BY v.created_at DESC".format(session['id_user']))
    if resultValue > 0:
        userVotings = cur.fetchall()
        cur.close()
        return render_template('organizerVoting.html', core = core, userVotings = userVotings, now = now)
    return render_template('organizerVoting.html', core = core, userVotings = None, now = now)

def organizer_voting_detail(id):
    core = {'title':'Panel Organizer', 'subtitle':'Kelola Voting', 'aside':True, 'page':['Kelola Voting', 'Data Candidate dan Voter']}
    now = datetime.now()
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'edit-voting':
            voting = data
            id_voting = id
            name = voting['name']
            voting_desc = voting['voting_desc']
            date_start, date_end = (voting['datetimes']).split(' - ')
            date_start = convert_datetime('mtl', date_start)
            date_end = convert_datetime('mtl', date_end)
            candidate = str(voting.getlist('candidate'))
            voter = str(voting.getlist('voter'))
            viewer = voting['viewer_access'] if 'viewer_access' in voting else 'off'
            cur = mysql.connection.cursor()
            cur.execute("UPDATE voting SET name = %s, voting_desc = %s, date_start = %s, date_end = %s, candidate = %s, voter = %s, viewer = %s "\
            "WHERE id_voting = %s", (name, voting_desc, date_start, date_end, candidate, voter, viewer, id_voting))
            mysql.connection.commit()
            cur.close()
            flash('Data Voting berhasil diperbaharui', 'secondary')
            return redirect(request.url)
        elif data['submit'] == 'add-candidate':
            candidate = data
            id_candidate = generate_id()
            id_voting = id
            username = 'C-' + generate_id()
            password = generate_id(size = 12)
            name = candidate['name']
            created_at = str(datetime.now())

            if 'cdesc' in candidate:
                description = candidate['cdesc']
                cdesc = True
            else:
                cdesc = False

            if 'cavatar' in request.files:
                image = request.files['cavatar']
                if image.filename == '':
                    flash('Tidak ada foto yang dipilih', 'warning')
                    return redirect(request.url)
                if image and allowed_image(image.filename):
                    filename = secure_filename(str(id_candidate) + '_' + created_at)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER_CANDIDATE'], filename))
                    cavatar = True
                else:
                    flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
                    return redirect(request.url)
            else:
                cavatar = False

            cur = mysql.connection.cursor()
            sql = ("INSERT INTO c_" + id_voting + "(id_candidate, id_voting, username, pass, name, " + ('description, ' if cdesc else '') + ('avatar, ' if cavatar else '') + "created_at) "\
            "VALUES(%s, %s, %s, %s, %s, " + ('%s, ' if cdesc else '') + ('%s, ' if cavatar else '') + "%s)")
            if cdesc and cavatar:
                cur.execute(sql, (id_candidate, id_voting, username, password, name, description, filename, created_at))
            elif cdesc:
                cur.execute(sql, (id_candidate, id_voting, username, password, name, description, created_at))
            elif cavatar:
                cur.execute(sql, (id_candidate, id_voting, username, password, name, filename, created_at))
            else:
                cur.execute(sql, (id_candidate, id_voting, username, password, name, created_at))

            mysql.connection.commit()
            cur.close()
            flash('Data Candidate berhasil ditambahkan', 'secondary')
            return redirect(request.url)

        elif data['submit'] == 'add-voter':
            voter = data
            id_voter = generate_id()
            id_voting = id
            username = 'V-' + generate_id()
            password = generate_id(size = 12)
            name = voter['name']
            created_at = str(datetime.now())

            if 'vdesc' in voter:
                description = voter['vdesc']
                vdesc = True
            else:
                vdesc = False

            if 'vavatar' in request.files:
                image = request.files['vavatar']
                if image.filename == '':
                    flash('Tidak ada foto yang dipilih', 'warning')
                    return redirect(request.url)
                if image and allowed_image(image.filename):
                    filename = secure_filename(str(id_voter) + '_' + created_at)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER_VOTER'], filename))
                    vavatar = True
                else:
                    flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
                    return redirect(request.url)
            else:
                vavatar = False

            cur = mysql.connection.cursor()
            sql = ("INSERT INTO v_" + id_voting + "(id_voter, id_voting, username, pass, name, " + ('description, ' if vdesc else '') + ('avatar, ' if vavatar else '') + "created_at) "\
            "VALUES(%s, %s, %s, %s, %s, " + ('%s, ' if vdesc else '') + ('%s, ' if vavatar else '') + "%s)")
            if vdesc and vavatar:
                cur.execute(sql, (id_voter, id_voting, username, password, name, description, filename, created_at))
            elif vdesc:
                cur.execute(sql, (id_voter, id_voting, username, password, name, description, created_at))
            elif vavatar:
                cur.execute(sql, (id_voter, id_voting, username, password, name, filename, created_at))
            else:
                cur.execute(sql, (id_voter, id_voting, username, password, name, created_at))

            mysql.connection.commit()
            cur.close()
            flash('Data Voter berhasil ditambahkan', 'secondary')
            return redirect(request.url)

        elif data['submit'] == 'edit-candidate':
            candidate = data
            id_voting = id
            table = 'c_' + id_voting
            id_candidate = candidate['id_candidate']
            name = candidate['name']
            created_at = str(datetime.now())
            if 'cdesc' in candidate:
                description = candidate['cdesc']
                cdesc = True
            else:
                cdesc = False

            cur = mysql.connection.cursor()

            if 'cavatar' in request.files:
                image = request.files['cavatar']
                if image.filename != '':
                    if image and allowed_image(image.filename):
                        avatarname = cur.execute("SELECT avatar FROM {} WHERE id_candidate = '{}'".format(table, id_candidate))
                        if avatarname > 0:
                            filename = cur.fetchone()
                            filename = filename['avatar']
                            if filename == None:
                                filename = secure_filename(str(id_candidate) + '_' + created_at)
                        image.save(os.path.join(app.config['UPLOAD_FOLDER_CANDIDATE'], filename))
                        cur.execute("UPDATE {} SET avatar = '{}' WHERE id_candidate = '{}'".format(table, filename, id_candidate))
                        mysql.connection.commit()
                    else:
                        flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
                        return redirect(request.url)

            sql = ("UPDATE " + table + " SET name = %s" + (', description = %s' if cdesc else '') + " WHERE id_candidate = %s")

            if cdesc:
                cur.execute(sql, (name, description, id_candidate))
            else:
                cur.execute(sql, (name, id_candidate))

            mysql.connection.commit()
            cur.close()
            flash('Data Candidate berhasil diperbaharui', 'secondary')
            return redirect(request.url)

        elif data['submit'] == 'edit-voter':
            voter = data
            id_voting = id
            table = 'v_' + id_voting
            id_voter = voter['id_voter']
            name = voter['name']
            created_at = str(datetime.now())
            if 'vdesc' in voter:
                description = voter['vdesc']
                vdesc = True
            else:
                vdesc = False

            cur = mysql.connection.cursor()

            if 'vavatar' in request.files:
                image = request.files['vavatar']
                if image.filename != '':
                    if image and allowed_image(image.filename):
                        avatarname = cur.execute("SELECT avatar FROM {} WHERE id_voter = '{}'".format(table, id_voter))
                        if avatarname > 0:
                            filename = cur.fetchone()
                            filename = filename['avatar']
                            if filename == None:
                                filename = secure_filename(str(id_voter) + '_' + created_at)
                        image.save(os.path.join(app.config['UPLOAD_FOLDER_VOTER'], filename))
                        cur.execute("UPDATE {} SET avatar = '{}' WHERE id_voter = '{}'".format(table, filename, id_voter))
                        mysql.connection.commit()
                    else:
                        flash('Ekstensi foto yang diijinkan adalah (png, jpg, jpeg)', 'warning')
                        return redirect(request.url)

            sql = ("UPDATE " + table + " SET name = %s" + (', description = %s' if vdesc else '') + " WHERE id_voter = %s")

            if vdesc:
                cur.execute(sql, (name, description, id_voter))
            else:
                cur.execute(sql, (name, id_voter))

            mysql.connection.commit()
            cur.close()
            flash('Data Voter berhasil diperbaharui', 'secondary')
            return redirect(request.url)

        elif data['submit'] == 'respond':
            problem = data
            id_problem = problem['id_problem']
            respond = problem['respond']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE problem SET respond = %s WHERE id_problem = %s",(respond, id_problem))
            mysql.connection.commit()
            cur.close()
            flash('Tanggapan berhasil dikirim', 'secondary')
            return redirect(request.url)

        elif data['submit'] == 'tell-problem':
            id_problem = generate_id()
            id_user = session['id_user']
            id_voting = id
            message = data['problem']
            msg_from = 'Organizer'
            msg_to = 'Admin'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO problem(id_problem, id_user, id_voting, msg_from, msg_to, message) VALUES(%s, %s, %s, %s, %s, %s)", (id_problem, id_user, id_voting, msg_from, msg_to, message))
            mysql.connection.commit()
            cur.close()
            flash('Pertanyaan dan keluhan berhasil dikirim', 'secondary')
            return redirect(request.url)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, name, voting_desc, date_start, date_end, candidate, voter, viewer, last_checked FROM voting WHERE id_voting = %s", [id])
    if resultValue > 0:
        votingDetail = cur.fetchone()
        cname = True if 'cname' in votingDetail['candidate'] else False
        cdesc = True if 'cdesc' in votingDetail['candidate'] else False
        cavatar = True if 'cavatar' in votingDetail['candidate'] else False
        vname = True if 'vname' in votingDetail['voter'] else False
        vdesc = True if 'vdesc' in votingDetail['voter'] else False
        vavatar = True if 'vavatar' in votingDetail['voter'] else False
        data = {'cdesc':cdesc, 'cavatar':cavatar, 'vdesc':vdesc, 'vavatar':vavatar}
    resultValue = cur.execute("SELECT id_candidate, id_voting, username, pass, name, {}{} status FROM {} ORDER BY created_at DESC".format('description,' if data['cdesc'] == True else '', 'avatar,' if data['cavatar'] == True else '', 'c_' + id))
    if resultValue > 0:
        votingCandidates = cur.fetchall()
    else:
        votingCandidates = None
    resultValue = cur.execute("SELECT id_voter, id_voting, username, pass, name, {}{} status FROM {} ORDER BY created_at DESC".format('description,' if data['vdesc'] == True else '', 'avatar,' if data['vavatar'] == True else '', 'v_' + id))
    if resultValue > 0:
        votingVoters = cur.fetchall()
    else:
        votingVoters = None
    resultValue = cur.execute("SELECT p.*, c.name AS Candidate, v.name AS Voter FROM problem p LEFT JOIN c_{} c ON p.id_user = c.id_candidate LEFT JOIN v_{} v ON p.id_user = v.id_voter WHERE p.id_voting = '{}' and p.msg_to = 'Organizer' ORDER BY p.msg_created DESC".format(id, id, id))
    if resultValue > 0:
        problems_cv = cur.fetchall()
    else:
        problems_cv = None
    resultValue = cur.execute("SELECT * FROM problem WHERE id_user = %s AND id_voting = %s ORDER BY msg_created DESC", (session['id_user'], id))
    if resultValue > 0:
        userProblems = cur.fetchall()
    else:
        userProblems = None
    cur.close()
    total = count_cv(id)
    return render_template('organizerVotingDetail.html', core = core, now = now, data = data, total = total, votingDetail = votingDetail, votingCandidates = votingCandidates, votingVoters = votingVoters, problems_cv = problems_cv, userProblems = userProblems)

def organizer_problem():
    core = {'title':'Panel Organizer', 'subtitle':'Pertanyaan dan Keluhan', 'aside':True, 'page':['Pertanyaan dan Keluhan']}
    now = datetime.now()
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'respond':
            problem = data
            id_problem = problem['id_problem']
            respond = problem['respond']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE problem SET respond = %s WHERE id_problem = %s",(respond, id_problem))
            mysql.connection.commit()
            cur.close()
            flash('Tanggapan berhasil dikirim', 'secondary')
            return redirect(request.url)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT p.*, v.name AS voting FROM problem p INNER JOIN voting v ON p.id_voting = v.id_voting WHERE p.msg_to = 'Admin' AND p.id_user = '{}' ORDER BY p.msg_created DESC".format(session['id_user']))
    if resultValue > 0:
        organizerProblems = cur.fetchall()
    else:
        organizerProblems = None

    votingLists = get_voting_list(session['id_user'])
    if votingLists != None:
        votingProblems = []
        for votingList in votingLists:
            voting = {}
            voting['id_voting'] = votingList['id_voting']
            voting['name'] = votingList['name']
            id = votingList['id_voting']
            resultValue = cur.execute("SELECT p.*, c.name AS Candidate, v.name AS Voter FROM problem p LEFT JOIN c_{} c ON p.id_user = c.id_candidate LEFT JOIN v_{} v ON p.id_user = v.id_voter WHERE p.id_voting = '{}' and p.msg_to = 'Organizer' ORDER BY p.msg_created DESC".format(id, id, id))
            if resultValue > 0:
                voting['problem'] = cur.fetchall()
                solved = True
                for problem in voting['problem']:
                    if problem['respond'] == None:
                        solved = False
                voting['solved'] = solved
            else:
                voting['problem'] = None
            votingProblems.append(voting)
    else:
        votingProblems = None
    cur.close()
    empty = True
    if votingProblems != None:
        votingProblems = tuple(votingProblems)
        empty = all(voting['problem'] == None for voting in votingProblems)
    return render_template('organizerProblem.html', core = core, now = now, organizerProblems = organizerProblems, votingProblems = votingProblems, empty = empty)

def voting_landing():
    core = {'title':'Login Candidate/Voter'}
    now = datetime.now()
    if request.method == 'POST':
        voting = request.form
        id_voting = voting['id_voting']
        return redirect('/voting-page/login/' + id_voting +'/')
    return render_template('votingLanding.html', core = core)

def voting_login_credential(id_voting, username, password):
    temp = username.split('-')[0]
    role = 'candidate' if temp == 'C' else 'voter'
    table = ('c_' + id_voting) if temp == 'C' else ('v_' + id_voting)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_{}, name, id_voting, status FROM {} WHERE username = '{}' AND pass = '{}'".format(role, table, username, password))
    if resultValue > 0:
        loginData = cur.fetchone()
        cur.close()
        session['login'] = True
        session['id_user'] = loginData['id_' + role]
        session['role'] = role
        session['id_voting'] = loginData['id_voting']
        session['status'] = loginData['status']
        session['name'] = loginData['name']
        flash('Selamat datang ' + session['name'] + '! Anda berhasil Login', 'secondary')
    else:
        flash('Username/kata sandi salah!', 'warning')
        return render_template('votingLogin.html')
    return redirect('/voting-page/')

def voting_login(id):
    core = {'title':'Login Voting'}
    now = datetime.now()
    if request.method == 'POST':
        user = request.form
        username = user['username']
        temp = username.split('-')[0]
        role = 'candidate' if temp == 'C' else 'voter'
        table = ('c_' + id) if temp == 'C' else ('v_' + id)
        password = user['password']

        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT id_{}, name, id_voting, status FROM {} WHERE username = '{}' AND pass = '{}'".format(role, table, username, password))
        if resultValue > 0:
            loginData = cur.fetchone()
            cur.close()
            session['login'] = True
            session['id_user'] = loginData['id_' + role]
            session['role'] = role
            session['id_voting'] = loginData['id_voting']
            session['status'] = loginData['status']
            session['name'] = loginData['name']
            flash('Selamat datang ' + session['name'] + '! Anda berhasil Login', 'secondary')
        else:
            flash('Username/kata sandi salah!', 'warning')
            return render_template('votingLogin.html')
        return redirect('/voting-page/')

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, name, voting_desc, date_start, date_end FROM voting WHERE id_voting = '{}'".format(id))
    if resultValue > 0:
        voting = cur.fetchone()
        cur.close()
        viewer = get_viewer(id)
        return render_template('votingLogin.html', voting = voting, core = core, now = now, viewer = viewer)
    else:
        flash('Kegiatan Voting tidak ditemukan!', 'warning')
        return redirect('/voting-page/login/')

def voting_page():
    core = {'title':'Halaman Voting', 'subtitle':'Halaman Voting', 'page':['Halaman Voting']}
    now = datetime.now()
    if request.method == 'POST':
        data = request.form
        if data['submit'] == 'vote-candidate':
            id_candidate = data['id_candidate']
            vote_hash(id_candidate)
            flash('Pilihan Anda berhasil disimpan', 'secondary')
        elif data['submit'] == 'tell-problem':
            id_problem = generate_id()
            id_user = session['id_user']
            id_voting = session['id_voting']
            message = data['problem']
            msg_from = 'Voter' if session['role'] == 'voter' else 'Candidate'
            msg_to = 'Organizer'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO problem(id_problem, id_user, id_voting, msg_from, msg_to, message) VALUES(%s, %s, %s, %s, %s, %s)", (id_problem, id_user, id_voting, msg_from, msg_to, message))
            mysql.connection.commit()
            flash('Pertanyaan dan keluhan berhasil dikirim', 'secondary')
        return redirect('/voting-page/')

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT voting.id_user, voting.name, voting.voting_desc, voting.date_start, voting.date_end, voting.candidate, user.name AS"\
    " organizer FROM voting INNER JOIN user ON voting.id_user = user.id_user WHERE voting.id_voting = '{}'".format(session['id_voting']))
    if resultValue > 0:
        voting = cur.fetchone()
        date_now = datetime.now()
        date_start = voting['date_start']
        date_end = voting['date_end']
        voting['date_start'] = convert_datetime('lts', voting['date_start'])
        voting['date_end'] = convert_datetime('lts', voting['date_end'])
        voting['cdesc'] = True if 'cdesc' in voting['candidate'] else False
        voting['cavatar'] = True if 'cavatar' in voting['candidate'] else False
        event = {}
        event['start'] = str(date_start - date_now)[0] == '-'
        event['finish'] = str(date_end - date_now)[0] == '-'

    resultValue = cur.execute("SELECT name, description, avatar, username, pass, status FROM {}_{} WHERE id_{} = '{}'".format((session['role'])[0], session['id_voting'], session['role'], session['id_user']))
    userData = cur.fetchone()

    session['status'] = userData['status']

    resultValue = cur.execute("SELECT * FROM problem WHERE id_user = %s ORDER BY msg_created DESC", [session['id_user']])
    if resultValue > 0:
        userProblems = cur.fetchall()
    else:
        userProblems = None

    resultValue = cur.execute("SELECT id_candidate, name, description, avatar FROM c_{}".format(session['id_voting']))
    if resultValue > 0:
        candidates = cur.fetchall()
        cur.close()
    else:
        candidates = None
    return render_template('votingPage.html', core = core, now = now, voting = voting, candidates = candidates, event = event, userData = userData, userProblems = userProblems)

def live_count(id):
    core = {'title':'Halaman Voting', 'subtitle':'Live Count Voting', 'page':['Halaman Voting', 'Live Count']}
    now = datetime.now()
    votingDetail = get_voting(id)
    votingCounts = get_count(id)
    return render_template("liveCount.html", core = core, now = now, votingDetail = votingDetail, votingCounts = votingCounts, id_voting = id)


# SUPPORT FUNCTION =============================================================

def allowed_image(filename):
    ext = filename.rsplit('.',1)[1].lower()
    val = '.' in filename and ext in ALLOWED_EXTENSIONS
    return val

def generate_id(size = 8, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def convert_datetime(option, datestring):
    if option == 'mtl':
        return str(datetime.strptime(datestring, '%d/%m/%Y %I:%M %p'))
    if option == 'ltm':
        return str(datestring)
    if option == 'lts':
        return str(datetime.strftime(datestring, '%d/%m/%Y %I:%M %p'))
        return str(datestring)

def count_organizer_total():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_user) AS total FROM user WHERE role = 'organizer'")
    if resultValue > 0:
        total = cur.fetchone()['total']
        cur.close()
    else:
        total = '0'
    return total

def count_organizer_new():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_user) AS new FROM user WHERE role = 'organizer' and status = 'pending' and message = '[Akun Baru]'")
    if resultValue > 0:
        new = cur.fetchone()['new']
        cur.close()
    else:
        new = '0'
    return new

def count_voting_total():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_voting) AS total FROM voting")
    if resultValue > 0:
        total = cur.fetchone()['total']
        cur.close()
    else:
        total = '0'
    return total

def count_voting_disactive():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_voting) AS disactive FROM voting WHERE date_start > CURRENT_TIMESTAMP")
    if resultValue > 0:
        disactive = cur.fetchone()['disactive']
        cur.close()
    else:
        disactive = '0'
    return disactive

def count_voting_active():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_voting) AS active FROM voting WHERE date_start <= CURRENT_TIMESTAMP and date_end > CURRENT_TIMESTAMP")
    if resultValue > 0:
        active = cur.fetchone()['active']
        cur.close()
    else:
        active = '0'
    return active

def count_voting_finish():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_voting) AS finish FROM voting WHERE date_end <= CURRENT_TIMESTAMP")
    if resultValue > 0:
        finish = cur.fetchone()['finish']
        cur.close()
    else:
        finish = '0'
    return finish

def get_voting_dashboard():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT v.id_voting, v.name, v.date_start, v.date_end, u.name AS organizer, u.email, u.institution FROM voting v INNER JOIN user u ON v.id_user = u.id_user WHERE (MONTH(v.date_end) >= MONTH(CURRENT_TIMESTAMP) AND YEAR(v.date_start) = YEAR(CURRENT_TIMESTAMP)) OR YEAR(v.date_start) > YEAR(CURRENT_TIMESTAMP)")
    if resultValue > 0:
        votingDetails = cur.fetchall()
        cur.close()
    else:
        votingDetails = None
    return votingDetails

def verify_organizer(action, id):
    if action == 'approve':
        verify = 'approved'
    elif action == 'reject':
        verify = 'disproved'
    elif action == 'active':
        verify = 'pending'
    elif action == 'inactive':
        verify = 'inactived'
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user SET status = %s WHERE id_user = %s", (verify, id))
    mysql.connection.commit()
    cur.close()
    if action == 'approve':
        flash('Akun telah diterima', 'secondary')
    elif action == 'reject':
        flash('Akun telah ditolak', 'danger')
    elif action == 'active':
        flash('Akun telah diaktifkan', 'info')
    elif action == 'inactive':
        flash('Akun telah dinonaktifkan', 'warning')
    return True

def count_voting_detail(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(id_voting) AS total FROM voting WHERE id_user = '{}'".format(id))
    if resultValue > 0:
        total = cur.fetchone()['total']
    else:
        total = '0'
    resultValue = cur.execute("SELECT COUNT(id_voting) AS disactive FROM voting WHERE date_start > CURRENT_TIMESTAMP AND id_user = '{}'".format(id))
    if resultValue > 0:
        disactive = cur.fetchone()['disactive']
    else:
        disactive = '0'
    resultValue = cur.execute("SELECT COUNT(id_voting) AS active FROM voting WHERE (date_start <= CURRENT_TIMESTAMP and date_end > CURRENT_TIMESTAMP) AND id_user = '{}'".format(id))
    if resultValue > 0:
        active = cur.fetchone()['active']
    else:
        active = '0'
    resultValue = cur.execute("SELECT COUNT(id_voting) AS finish FROM voting WHERE date_end <= CURRENT_TIMESTAMP AND id_user = '{}'".format(id))
    if resultValue > 0:
        finish = cur.fetchone()['finish']
    else:
        finish = '0'
    cur.close()
    voting = {'total':total, 'disactive':disactive, 'active':active, 'finish':finish}
    return voting

def count_cv(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT COUNT(*) AS candidate FROM c_{}".format(id))
    if resultValue > 0:
        candidate = cur.fetchone()['candidate']
    else:
        candidate = '0'
    resultValue = cur.execute("SELECT COUNT(*) AS voter FROM v_{}".format(id))
    if resultValue > 0:
        voter = cur.fetchone()['voter']
    else:
        voter = '0'
    total = {'candidate':candidate, 'voter':voter}
    return total

def get_cardid(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT card_id FROM user WHERE id_user = %s", [id])
    if resultValue > 0:
        card_id = cur.fetchone()
        cur.close()
        return (card_id['card_id'])
    return None

def get_voting_list(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_voting, name FROM voting WHERE id_user = %s", [id])
    if resultValue > 0:
        votingList = cur.fetchall()
        cur.close()
        return votingList
    return None

def get_delete(table, id):
    if table == 'voting':
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE h_{}".format(id))
        mysql.connection.commit()
        data = cur.execute("SELECT avatar FROM c_{}".format(id))
        if data > 0:
            candidates = cur.fetchall()
            for candidate in candidates:
                if candidate['avatar'] != None:
                    get_delete_img('candidate', candidate['avatar'])
        cur.execute("DROP TABLE c_{}".format(id))
        mysql.connection.commit()
        data = cur.execute("SELECT avatar FROM v_{}".format(id))
        if data > 0:
            voters = cur.fetchall()
            for voter in voters:
                if voter['avatar'] != None:
                    get_delete_img('voter', voter['avatar'])
        cur.execute("DROP TABLE v_{}".format(id))
        mysql.connection.commit()
        cur.execute("DELETE FROM problem WHERE id_voting = '{}'".format(id))
        mysql.connection.commit()
        cur.execute("DELETE FROM voting WHERE id_voting = '{}'".format(id))
        mysql.connection.commit()
        cur.close()
    elif table == 'organizer':
        get_delete_img(table, get_cardid(id))
        votingList = get_voting_list(id)
        if votingList != None:
            for voting in votingList:
                get_delete('voting', voting['id_voting'])
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM user WHERE id_user = %s", [id])
        mysql.connection.commit()
        cur.close()
    elif table == 'problem':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM problem WHERE id_problem = %s", [id])
        mysql.connection.commit()
        cur.close()
    return True

def get_delete_cv(table, data, id):
    cur = mysql.connection.cursor()
    avatar = cur.execute("SELECT avatar FROM {} WHERE id_{} = '{}'".format(table, data, id))
    if avatar > 0:
        avatar = cur.fetchone()
        avatar = avatar['avatar']
        if avatar != None:
            get_delete_img(data, avatar)
    cur.execute("DELETE FROM {} WHERE id_{} = '{}'".format(table, data, id))
    mysql.connection.commit()
    cur.close()
    return True

def get_delete_img(data, filename):
    if data == 'organizer':
        img_path = app.config['UPLOAD_FOLDER_CARDID']
    elif data == 'candidate':
        img_path = app.config['UPLOAD_FOLDER_CANDIDATE']
    elif data == 'voter':
        img_path = app.config['UPLOAD_FOLDER_VOTER']
    os.remove(os.path.join(img_path, filename))
    return True

def set_status_cv(table, data, status, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE {} SET status = ".format(table) + ("'blocked'" if status == 'block' else 'NULL') + " WHERE id_{} = '{}'".format(data, id))
    mysql.connection.commit()
    cur.close()
    return True

def get_voting(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM voting WHERE id_voting = %s", [id])
    if resultValue > 0:
        votingData = cur.fetchone()
        cur.close()
        votingData['cname'] = True if 'cname' in votingData['candidate'] else False
        votingData['cdesc'] = True if 'cdesc' in votingData['candidate'] else False
        votingData['cavatar'] = True if 'cavatar' in votingData['candidate'] else False
        votingData['vname'] = True if 'vname' in votingData['voter'] else False
        votingData['vdesc'] = True if 'vdesc' in votingData['voter'] else False
        votingData['vavatar'] = True if 'vavatar' in votingData['voter'] else False
        return votingData
    return None

def check_idle(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT date_end FROM voting WHERE id_voting = '{}'".format(id))
    if resultValue > 0:
        date_end = cur.fetchone()['date_end']
        date_now = datetime.now()
        cur.close()
        if date_end < date_now:
            return True
        else:
            return False
    else:
        cur.close()
        return False

def get_report_finish(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT c.name, c.id_candidate, COUNT(h.id_candidate) as res FROM c_{} c LEFT JOIN h_{} h ON c.id_candidate = h.id_candidate GROUP BY c.id_candidate ORDER BY res DESC".format(id, id))
    if resultValue > 0:
        report = []
        candidates = cur.fetchall()
        for candidate in candidates:
            cur.execute("SELECT COUNT(id_candidate) as valid FROM h_{} WHERE id_candidate = '{}' AND status = 'checked'".format(id, candidate['id_candidate']))
            candidate['valid'] = cur.fetchone()['valid']
            cur.execute("SELECT COUNT(id_candidate) as invalid FROM h_{} WHERE id_candidate = '{}' AND status = 'rejected'".format(id, candidate['id_candidate']))
            candidate['invalid'] = cur.fetchone()['invalid']
            report.append(candidate)
        report = tuple(report)
        cur.close()
        return report
    else:
        cur.close()
        return None

def get_problem_admin(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT p.id_problem, p.id_user, p.message, u.name FROM problem p INNER JOIN user u ON p.id_user = u.id_user WHERE id_problem = %s", [id])
    if resultValue > 0:
        problem = cur.fetchone()
        cur.close()
        return problem
    return None

def get_problem_organizer(id_voting, id_problem):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT p.id_problem, p.id_user, p.message, p.msg_from, c.name AS Candidate, v.name AS Voter FROM problem p LEFT JOIN c_{} c ON p.id_user = c.id_candidate LEFT JOIN v_{} v ON p.id_user = v.id_voter WHERE id_problem = '{}'".format(id_voting, id_voting, id_problem))
    if resultValue > 0:
        problem = cur.fetchone()
        cur.close()
        return problem
    return None

def get_cv(table, data, id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_{}, name, description, avatar FROM {} WHERE id_{} = '{}'".format(data, table, data, id))
    if resultValue > 0:
        editData = cur.fetchone()
        cur.close()
        return editData
    return None

def get_viewer(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT viewer FROM voting WHERE id_voting = '{}'".format(id))
    if resultValue > 0:
        viewer = cur.fetchone()
        viewer = viewer['viewer']
    else:
        viewer = None
    cur.close()
    return viewer

# VOTING FUNCTION ==============================================================

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(msg, main_key, key):
    main_key = hashlib.sha256(main_key.encode("utf-8")).digest()
    main_iv = Random.new().read(AES.block_size)
    msg = str.encode(pad(msg))
    cipher = AES.new(main_key, AES.MODE_CBC, main_iv)
    encrypted = base64.b64encode(cipher.encrypt(msg))
    validator = generate_validator(key, encrypted, main_iv)
    return ([bytes.decode(encrypted), bytes.decode(validator)])

def generate_validator(key, encrypted, msg):
    key = hashlib.sha256(key.encode("utf-8")).digest()
    iv = get_iv(encrypted)
    iv = str.encode(iv.encode().hex())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    validator = base64.b64encode(cipher.encrypt(msg))
    return validator

def decrypt(encrypted, validator, key, main_key):
    key = hashlib.sha256(key.encode("utf-8")).digest()
    iv = get_iv(encrypted)
    iv = str.encode(iv.encode().hex())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    validator = base64.b64decode(validator)
    main_iv = cipher.decrypt(validator)
    main_key = hashlib.sha256(main_key.encode("utf-8")).digest()
    encrypted = base64.b64decode(encrypted)
    plain = AES.new(main_key, AES.MODE_CBC, main_iv)
    msg = unpad(plain.decrypt(encrypted))
    msg = (bytes.decode(msg)).split('-')
    return msg

def get_iv(seed):
    random.seed(seed)
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    iv = ''.join(random.choice(chars) for _ in range(8))
    return iv

def vote_hash(id_candidate):
    id_hash = generate_id()
    id_user = session['id_user']
    id_voting = session['id_voting']
    encrypted, validator = encrypt(id_user + '-' + id_candidate, id_user, id_hash)
    status = 'voted'
    table_hash = 'h_' + id_voting
    role = session['role']
    table_user = ('v_' if role == 'voter' else 'c_') + id_voting

    date_now = datetime.now()
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT date_start, date_end FROM voting WHERE id_voting = '{}'".format(id_voting))
    if resultValue > 0:
        event_date = cur.fetchone()
        date_start = event_date['date_start']
        date_end = event_date['date_end']

    event = {}
    event['start'] = str(date_start - date_now)[0] == '-'
    event['finish'] = str(date_end - date_now)[0] == '-'

    if event['start'] == True and event['finish'] == False:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO {}(id_hash, id_voting, id_candidate, role, encrypted, status) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(table_hash, id_hash, id_voting, id_candidate, role, encrypted, status))
        mysql.connection.commit()
        cur.execute("UPDATE {} SET status = '{}', validator = '{}' WHERE id_{} = '{}'".format(table_user, id_hash, validator, role, id_user))
        mysql.connection.commit()
        cur.close()
        session['status'] = id_hash

    return True

def get_count(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT c.id_candidate, c.name, c.description, c.avatar, COUNT(h.id_candidate) AS result FROM c_{} c LEFT JOIN h_{} h ON c.id_candidate = h.id_candidate GROUP BY c.id_candidate ORDER BY result DESC".format(id, id))
    if resultValue > 0:
        votingResults = cur.fetchall()
    else:
        votingResults = None
    cur.close()
    return votingResults

def validate_voting(id_voting):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_hash, id_voting, id_candidate, role, encrypted FROM h_{}".format(id_voting))
    if resultValue > 0:
        votingHash = cur.fetchall()
        for vote in votingHash:
            validate_hash(vote)
    now = datetime.now()
    cur.execute("UPDATE voting SET last_checked = '{}' WHERE id_voting = '{}'".format(now, id_voting))
    mysql.connection.commit()
    cur.close()
    return True

def validate_hash(vote):
    id_hash = vote['id_hash']
    id_voting = vote['id_voting']
    id_candidate = vote['id_candidate']
    role = vote['role']
    encrypted = vote['encrypted']
    table = ('v_' if role == 'voter' else 'c_') + id_voting
    table_hash = 'h_' + id_voting

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT id_{}, validator FROM {} WHERE status = '{}'".format(role, table, id_hash))
    if resultValue > 0:
        userData = cur.fetchone()
        id_user = userData['id_' + role]
        validator = userData['validator']

        try:
            dataUser, dataCandidate = decrypt(encrypted, validator, id_hash, id_user)
            if dataUser == id_user and dataCandidate == id_candidate:
                cur.execute("UPDATE {} SET status = 'checked' WHERE id_hash = '{}'".format(table_hash, id_hash))
            else:
                cur.execute("UPDATE {} SET status = 'rejected' WHERE id_hash = '{}'".format(table_hash, id_hash))
        except:
            cur.execute("UPDATE {} SET status = 'rejected' WHERE id_hash = '{}'".format(table_hash, id_hash))
    else:
        cur.execute("UPDATE {} SET status = 'rejected' WHERE id_hash = '{}'".format(table_hash, id_hash))
    mysql.connection.commit()
    cur.close()
    return True

# MAIN PROGRAM =================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
