# Lab 13-2-1
# Arsenie Sarmiento, 12/6/23
# ads0417@arastudent.ac.nz

# Demerit Points Calculator

import os
from flask import Flask, render_template, request, flash

SUCCESS_MSG = 'success'
WARNING_MSG = 'warning'
KEY_SIZE = 24
HTML_TEMPLATE = 'flask_app_template.html'

# Create Flask instance and set the session key
app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(KEY_SIZE)

def get_demerit_points(driving_speed,speed_limit,holiday_period = False):
    """ Calculates demerit points for driving speed violation. No value validation. """

    # Mandatory penalty, penalty points
    speed_diff = driving_speed - speed_limit
    
    if speed_diff <= 10 and speed_diff > 0:
        penalty_points = 10
    elif speed_diff > 10 and speed_diff <= 20:
        penalty_points = 20
    elif speed_diff > 20 and speed_diff <= 30:
        penalty_points = 30
    elif speed_diff > 30:
        penalty_points = 50
        

    else:
        penalty_points = 0
        mandatory_penalty = False
            
################################
        
    if holiday_period == True:
        speed_thresh = 4 # IT IS HOLIDAY
    else:
        speed_thresh = 5 # IT IS NOT HOLIDAY

################################
        
    if speed_diff > speed_thresh:
        mandatory_penalty = True
        
    else:
        #penalty_points = 0
        mandatory_penalty = False

    return (mandatory_penalty,penalty_points)
    
# 404 handler
@app.errorhandler(404) 
def page_not_found(e): 
  return render_template('flask_app_error_webpage.html')
 
@app.route('/', methods = ['POST', 'GET'])
def home():
    """ Home page handler """

    print(f'DEBUG. Function received http method type: {request.method}')
    
    if request.method == 'POST':
        # Get the data that has been sent via http post
        drv_speed = request.form.get('form_driving_speed')
        lmt_speed = request.form.get('form_speed_limit')
        holiday_tckbx = request.form.get('holiday_tickbox')
        print(f'{holiday_tckbx=}')
              
        if drv_speed != '' and lmt_speed != '':
            # Data has been submitted on both fields (Driving speed & Speed limit)
            
            if drv_speed.replace('.','').isdigit() and lmt_speed.replace('.','').isdigit():
                # Checking if numerical fields are digits, regardless of the number of the decimal points. Otherwise, inform user accordingly.
                
                dot_counter_driving = (str(drv_speed)).count('.')
                dot_counter_limit = (str(lmt_speed)).count('.')
                # Validating entered numerical values by dot counting. Handling multiple dots input.
                # Driving  speed values must only have 1 (float) or 0 dots (integer). Speed limit values must have 0 (integer).
                
                
                if dot_counter_driving == 1 and dot_counter_limit == 0:
                    drv_speed = float(drv_speed)
                    lmt_speed = int(lmt_speed)
                    
                elif drv_speed.count('.') == 0 and lmt_speed.count('.') == 0:
                    drv_speed = int(drv_speed)
                    lmt_speed = int(lmt_speed)
                    
                else:
                # Entered numeric values outside conditions. Preventing get_demerit_points function operations. 
                    flash(f'Please ented valid values only. Integers or floats for Driving Speed. Integers only for Speed Limit.', WARNING_MSG)
                    return render_template(HTML_TEMPLATE, form_driving_speed=drv_speed, form_speed_limit=lmt_speed, holiday_tickbox=holiday_tckbx)

                if holiday_tckbx == 'on':
                    holiday_bool = True
                    # Setting corresponding boolean values for when 'Holiday period' box is ticked; triggering appropriate speed threshold (4km/h or 5km/h). 
                    
                else:
                    holiday_bool = False
                    
                # Compare the values received and return the results to the browser
                msg = get_demerit_points(drv_speed, lmt_speed,holiday_bool)
                penalty_category,penalty_score = msg
                
                if drv_speed <= lmt_speed:
                # Not speeding
                    string_txt = f'{drv_speed}km/h in a {lmt_speed}km/h zone is not speeding.'
                    flash(string_txt, SUCCESS_MSG)
                else:   
                    if penalty_category == True:
                    # Speeding and above speed threshold.
                        penalty_type = 'mandatory'
                
                    else:
                    # Speeding and below speed threshold.
                        penalty_type = 'discretional'
                
                    string_txt = f'The {penalty_type} penalty for driving at {drv_speed}km/h in a {lmt_speed}km/h zone is {penalty_score} points.'
                    flash(string_txt, WARNING_MSG)
                
                return render_template(HTML_TEMPLATE, form_driving_speed=drv_speed, form_speed_limit=lmt_speed, holiday_tickbox=holiday_tckbx)


            else:
                # Not digits
                flash(f'Numbers only please.', WARNING_MSG)
        else:
            # Not all the data was received
            if drv_speed != '' and lmt_speed == '': #lmt_speed(Speed limit) is EMPTY)
                flash('Please enter a speed limit.', WARNING_MSG)
            
            elif drv_speed == '' and  lmt_speed != '': #drv_speed(driving speed) is EMPTY)
                flash('Please enter a driving speed.', WARNING_MSG)
            
            else:
                flash('Please enter a driving speed and speed limit.', WARNING_MSG)
        return render_template(HTML_TEMPLATE, form_driving_speed=drv_speed, form_speed_limit=lmt_speed, holiday_tickbox=holiday_tckbx)   

    return render_template(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()


