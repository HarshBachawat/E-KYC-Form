from flask import Flask,Blueprint,render_template, redirect, url_for, request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,login_required,current_user,login_user, logout_user
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
from ocr import imgToStr
from fill_form import fill_form
from automated_email import send_email

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    return render_template('login.html')

@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/profile')
@login_required
def profile():
    user_status = UserDetails.query.filter_by(user_id=current_user.id).first()
    if user_status:
        user_status = user_status.status
    else:
        user_status = 0
    return render_template('profile.html',name=current_user.name,status=user_status)

@main_blueprint.route('/upload',methods=['POST'])
@login_required
def upload():
    pan=request.files["pan_img"]
    aadhar1=request.files["aadhar1_img"]
    aadhar2=request.files["aadhar2_img"]
    file_name = time.strftime("%Y%m%d-%H%M%S")
    pan_file = secure_filename(file_name+'_pan.jpg')
    aadhar1_file = secure_filename(file_name+'_aadhar1.jpg')
    aadhar2_file = secure_filename(file_name+'_aadhar2.jpg')
    pan.save(os.path.join(uploads_dir, pan_file))
    aadhar1.save(os.path.join(uploads_dir, aadhar1_file))
    aadhar2.save(os.path.join(uploads_dir, aadhar2_file))
    pan_details = imgToStr('Pan',pan_file)
    aadhar1_details = imgToStr('Aadhar1',aadhar1_file)
    aadhar2_details = imgToStr('Aadhar2',aadhar2_file)

    if pan_details['status'] and aadhar1_details['status'] and aadhar2_details['status']:
        flag = 0

        if pan_details['fname'].lower()==aadhar1_details['fname'].lower() and pan_details['lname'].lower()==aadhar1_details['lname'].lower():
            flag = 1
        else:
            flag = 1
        if flag:
            (user_id,fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode) = (current_user.id,aadhar1_details['fname'],aadhar1_details['lname'],
                        pan_details['fat_name'],aadhar1_details['gender'],pan_details['dob'],aadhar1_details['doc_no'],pan_details['doc_no'],
                        aadhar2_details['city'],aadhar2_details['state'],aadhar2_details['pincode'])
            fn = father_name
            father_name = fn[0]+fn[1:].lower()
            details = UserDetails(user_id,fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode,file_name,0)
            db.session.add(details)
            db.session.commit()
            # fill_form(fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode)
            
            return jsonify(status=1,fname=fname,lname=lname,father_name=father_name,dob=dob,gender=gender,pan_no=pan_no,aadhar_no=aadhar_no,
                city=city,state=state,pincode=pincode)
        else:
            return jsonify(status=0,error='Error: Names on the documents do not match')
    else:
        return jsonify(status=0,error='Error: Problem with one of the images. Please reupload and try again')

@main_blueprint.route('/fill_form',methods=['POST'])
@login_required
def complete():
    details = request.get_json()
    (fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode) = (details['fname'],details['lname'],details['father_name'],
        details['gender'],details['dob'],details['aadhar_no'],details['pan_no'],details['city'],details['state'],details['pincode'])
    form = fill_form(fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode)
    if form:
        user = UserDetails.query.filter_by(user_id=current_user.id).first()
        user.status = 1
        db.session.commit()
        email = send_email(current_user.email,fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode)
        return jsonify(status=1,msg='You Have Successfully Completed your E-KYC Application')
    else:
        return jsonify(status=0,msg='Error: Internet Connection/Timeout Error')
    

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_details = db.relationship('UserDetails',uselist=False,backref='user',lazy=True)

class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    father_name = db.Column(db.String(50))
    gender = db.Column(db.String(8))
    dob = db.Column(db.String(10))
    aadhar_no = db.Column(db.String(14))
    pan_no = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(30))
    pincode = db.Column(db.String(6))
    file_prefix = db.Column(db.String(18))
    status = db.Column(db.Integer)

    def __init__(self,user_id,fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode,file_name,status):
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.father_name = father_name
        self.gender = gender
        self.dob = dob
        self.aadhar_no = aadhar_no
        self.pan_no = pan_no
        self.city = city
        self.state = state
        self.pincode = pincode
        self.file_name = file_name
        self.status = status


app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.create_all()

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')