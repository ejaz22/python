from flask import Flask,render_template,request,redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
import escrow,imst
import os,glob,sys
sys.path.append('/prod/user/Users/xyz/imst_app/')

# configs & i/o
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/prod/user/Users/xyz/imst_app/upload/'
input_path = '/prod/user/Users/xyz/imst_app/input/'
output_path = '/prod/user/Users/xyz/imst_app/output/'

# clear I/O files
def clear_io():
	[os.remove(f) for f in glob.glob(input_path+'*')]
	[os.remove(f) for f in glob.glob(output_path+'*')]

# index route       
@app.route("/")
def index():
    clear_io()
    return render_template('index.html')

# upload input files
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    clear_io()
    if request.method == 'POST':
    	uploaded_files = request.files.getlist('file[]')
    	
    	for f in uploaded_files:
    	    f_name = secure_filename(f.filename)
    	    f.save(os.path.join(app.config['UPLOAD_FOLDER'],f_name))
    	        	
    	return render_template('confirm.html', f= [f for f in os.listdir(input_path) if not f.startswith('.')])
    
    return redirect(url_for('index.html'))
 
# run the process script   
@app.route('/run_process')
def run_process():
    if '630.txt' in os.listdir(input_path):
    
        try:
            escrow.process_script()
        except Exception as e:
            return render_template('input_error.html')
    
    else:
        try:
            imst.process_script()
        except Exception as e:
            return render_template('input_error.html', exc = str(e))
  
    
    return render_template('download.html', files = os.listdir(output_path))

# handle error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# run app
if __name__ == "__main__":
	app.run(host="10.37.204.148",port="7009")
